=====
Usage
=====

To use pcapfilter commandline you need to provide pcap stdin and pcap stdout::

    tcpdump -i en0  -s0 -w - | pcapfilter -vm myfilter.py | wireshark -k -i -
