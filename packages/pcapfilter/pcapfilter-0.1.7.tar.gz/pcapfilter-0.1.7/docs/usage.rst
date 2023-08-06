=====
Usage
=====

.. click:: pcapfilter.cli:main
   :prog: pcapfilter
   :show-nested:

The basic usage is::

    INPUT | pcapfilter [options] | OUTPUT

Where INPUT is a package capture provider, such as `tcpdump` and OUTPUT is some program
able to conusme pcap from stdin.

For example, capturing packets from interface en0 (INPUT) and showing the results in wireshark (OUTPUT)::

    tcpdump -i en0  -s0 -w - | pcapfilter -vm myfilter.py | wireshark -k -i -

You can use ssh packet capture from your router and display it in `Wireshark`_ ::

    ssh router "tcpdump -i eth1.2 -i br-lan -s0 -w - " | pcapfilter -vm main.py | wireshark -k -i -

.. _Wireshark: https://www.wireshark.org/


As a docker image
-----------------

You need to provide a volume where your filter file is defined::

    INPUT | docker run --rm -i -v $(pwd):/shared pcapfilter pcapfilter -vm /shared/main.py | OUTPUT


Defining a filter
-----------------

A filter is a python module (or file ending in .py) that has a function called `packet_filter`.
This funcion receives an argument named `pkg`
If `None` is returned, then the package is **discarded**.

If the packet is returned (modified or not) it will be sent to the OUTPUT.

