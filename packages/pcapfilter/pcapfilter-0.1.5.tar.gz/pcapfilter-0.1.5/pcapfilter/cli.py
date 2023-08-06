# -*- coding: utf-8 -*-

"""Console script for pcapfilter."""
import sys
import click
import logging

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)

STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setLevel(logging.DEBUG)
STREAM_HANDLER.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
from .pcapfilter import run_filter

def show_docker_help():
    click.echo(
        click.style(
            "To run pcapfilter inside docker and use your module function you\n"
            "must ensure that you're not using some python package that was\n"
            "bundled in the image.\n"
            "\n",
            fg='red'
        )
    )
    click.echo(
        "tcpdump -i en0  -s0 -w - | docker run --rm -i -v $(pwd):/shared pcapfilter pcapfilter -vm /shared/main.py | wireshark -k -i -"
        "\n\n"
        "The main.py should contain a function like:\n"
    )
    click.echo(
        click.style(
            "from scapy.all import *\n"
            "from logging import getLogger\n"
            "\n"
            "LOG = getLogger(__name__)\n"
            "def packet_filter(packet):\n"
            "    # Do something useful, return None to filter or modify contents with scapy\n"
            "    return pkg\n",
            fg='green'
        )
    )
    click.echo('\n')


@click.command(
    help="Read packet capture data (pcap) stream from stdin, apply a function and write to stdout."
    "Example (capture from INTERFACE and display in Wireshark): "
    "tcpdump -i INTERFACE -s0 -w - | pcapfilter -m myfiltermodule.py | wireshark -k -i -"
)
@click.option(
    "-m",
    "--module",
    type=str,
    default="",
    help="A python module name that contains a packet_filter(packet). More info at https://pcapfilter.readthedocs.io/en/latest/usage.html#defining-a-filter",
)
@click.option("-v", "--verbose", is_flag=True, help="Show log messages (defaults to STDERR)")
@click.option("-o", "--oldpcap", is_flag=True, help="Use old pcap for input")
@click.option("-r", "--reload", is_flag=True, help="Reloads the module upon changes")
@click.option("-d", "--docker-help", is_flag=True, help="Shows help when running from docker")
def main(module, verbose, oldpcap, reload, docker_help):
    # Delay scapy import until it's necessary, since it takes some time
    if docker_help:
        show_docker_help()
        return
    if verbose:
        LOGGER.addHandler(STREAM_HANDLER)

    if not oldpcap:
        LOGGER.info("Using PcapNgReader")
        from scapy.all import PcapNgReader as Reader
    else:
        LOGGER.info("Using PcapReader")
        from scapy.all import PcapReader as Reader
    from scapy.all import PcapWriter as Writer

    run_filter(
        reader_class=Reader,
        writer_class=Writer,
        module=module,
        reload=reload,
    )

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
