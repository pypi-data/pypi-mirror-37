from io import BytesIO
from scapy.all import Ether, IP, UDP, TCP
from scapy.all import ICMP, IP, TCP, UDP, Ether, PcapNgReader, PcapWriter, PcapReader

class PreloadedPcapWriter:
    """
    Holds a file with some packages
    """
    def __init__(self, initial_content=None, writer_class=PcapWriter):
        if not initial_content:
            initial_content = []
        self.file_obj = BytesIO()
        self._writer = writer_class(self.file_obj)

        for packet in initial_content:
            self._writer.write(packet)

        self.file_obj.seek(0)

class ReadablePcapWriter:

    def __init__(self):
        self.file_obj = BytesIO()

    def __getattr__(self, name):
        return object.__getattribute__(self.file_obj, name)

    def get_contents(self):
        self.file_obj.seek(0)
        reader = PcapNgReader(self.file_obj)
        for pkg in reader:
            yield pkg


def assert_same_packet(p1, p2, layers=None):
    if not layers:
        layers = (Ether, IP, TCP, UDP)
    for layer in layers:
        if layer in p1:
            if not layer in p2:
                raise AssertionError(
                    '{} present in 1st packet but not in 2nd'.format(layer)
                )
            assert bytes(p1[layer]) == bytes(p2[layer])
