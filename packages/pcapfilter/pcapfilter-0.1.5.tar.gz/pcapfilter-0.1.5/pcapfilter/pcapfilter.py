# -*- coding: utf-8 -*-

"""
tcpdump -i en0  -s0 -w - | pcapfilter -m mymodule.py | wireshark -k -i -

In a OpenWRT enabled router something like this could be used:
ssh router "tcpdump -i eth1.2 -i br-lan -s0 -w - " | pcapfilter -m mymodule.py | wireshark -k -i -
"""
import imp
import logging
import os
from pathlib import Path
from queue import Queue
import logging
import sys
from typing import Any, Callable
from datetime import datetime, timedelta
from scapy.error import Scapy_Exception

try:
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer
    WATCHDOG_ENABLED = True
except ImportError:
    WATCHDOG_ENABLED = False


LOGGER = logging.getLogger()


NOTIFICATION_QUEUE = Queue(maxsize=1)


def start_observer(module):
    '''
    Starts the file observer if available and injects notifies
    the main loop though the NOTIFICATION_QUEUE.
    '''
    if not WATCHDOG_ENABLED:
        LOGGER.info('Cannot start observer, watchdog module not available')
        return

    module_path = Path(module.__file__)
    module_abspath = module_path.absolute()
    module_dir = module_path.cwd().absolute()

    class ModuleEventHandler(FileSystemEventHandler):
        def on_modified(self, event):
            if Path(event.src_path).absolute() == module_abspath:
                if not NOTIFICATION_QUEUE.full():
                    LOGGER.info("Notifying reload of: %s", module_abspath)
                    NOTIFICATION_QUEUE.put(1)


    file_event_handler = ModuleEventHandler()
    observer = Observer()
    observer.schedule(
        file_event_handler,
        module_dir,
        recursive=False
    )
    observer.start()
    return observer, file_event_handler

def _extract(mod, name):
    callback = getattr(mod, name, None)
    if not callable(callback):
        LOGGER.warning(
            f"{module_name} does not have a callable {callback_name} function"
        )
    return callback

def import_module_and_callback(module_name: str, callback_name: str = 'packet_filter') -> (Any, Callable):
    '''
    Returns the module and the callback. The module is used for autoreload.
    '''
    module, callback = None, None
    if module_name:
        if module_name.endswith('.py') and os.path.exists(module_name):
            LOGGER.info(f"Loading plain file {module_name}")
            sys.path.append(os.path.dirname(module_name))
            module_name, _ = os.path.splitext(os.path.basename(module_name))
        if callable(module_name):
            callback = module_name
        else:
            try:
                module = __import__(module_name)
                callback = _extract(module, callback_name)
            except ImportError as e:
                LOGGER.info(f"Could not import {module_name}")
    return module, callback

def reload_module_and_callback(module: Any, callback_name: str = 'packet_filter') -> Callable:
    new_mod = imp.reload(module)
    callback = _extract(module, callback_name)
    return new_mod, callback


def run_filter(
    reader_class: object,
    writer_class: object,
    module: str,
    reload: bool = False,
    _input=sys.stdin.buffer,
    _output=sys.stdout.buffer,
):
    """
    Process packets inserted from _input through a function and wirte
    them to _output
    """
    module, callback = import_module_and_callback(module)
    if reload and module:
        _reloader = start_observer(module)
    try:
        LOGGER.info("Creating reader")
        reader = reader_class(_input)
        writer = writer_class(_output)
        LOGGER.info("Creating writer")
    except KeyboardInterrupt:
        LOGGER.info("Existed before fully opening the stream")
        return -1
    except Scapy_Exception:
        LOGGER.error("Could not read pcap form stdin")
        return -2

    # Counters
    last = current = datetime.now()
    delta = timedelta(seconds=1)
    count = 0

    while True:
        try:
            source = reader.read_packet()
            new_package = callback(source)
            if not new_package:
                continue
            writer.write(new_package)
            if reload and NOTIFICATION_QUEUE.full():
                module, callback = reload_module_and_callback(module)
                NOTIFICATION_QUEUE.get()
            # Stats
            count += 1
            current = datetime.now()
            if current - last >= delta:
                LOGGER.info(f"Packets processed in last second: {count}")
                count = 0
                last = current

        except (KeyboardInterrupt, BrokenPipeError) as e:
            LOGGER.info(f"Stopping...")
            break
        except Scapy_Exception:
            LOGGER.error("Could not read pcap form stdin")
            return -2
        except Exception as e:
            LOGGER.exception(
                "Aborting execution due errors in function. "
                "Hit Ctrl-C if prompt does not return."
            )
            return -3
    return 0
