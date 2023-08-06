=====
Usage
=====

To use pcapfilter commandline you need to provide pcap stdin and pcap stdout::

    tcpdump -i en0  -s0 -w - | pcapfilter -vm myfilter.py | wireshark -k -i -

You can use ssh packet capture from your router and display it in `Wireshark`_ ::

    ssh router "tcpdump -i eth1.2 -i br-lan -s0 -w - " | pcapfilter -vm main.py | wireshark -k -i -

.. _Wireshark: https://www.wireshark.org/
