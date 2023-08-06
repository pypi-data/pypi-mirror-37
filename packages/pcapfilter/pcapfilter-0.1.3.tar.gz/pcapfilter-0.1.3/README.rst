===========
PCap Filter
===========


.. image:: https://img.shields.io/pypi/v/pcapfilter.svg
        :target: https://pypi.python.org/pypi/pcapfilter

.. image:: https://img.shields.io/travis/D3f0/pcapfilter.svg
        :target: https://travis-ci.org/D3f0/pcapfilter

.. image:: https://readthedocs.org/projects/pcapfilter/badge/?version=latest
        :target: https://pcapfilter.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/D3f0/pcapfilter/shield.svg
     :target: https://pyup.io/repos/github/D3f0/pcapfilter/
     :alt: Updates



Python package for packet filtering and manipulation using scapy

.. image:: ./imgs/pcapfilter.svg


* Free software: MIT license
* Documentation: https://pcapfilter.readthedocs.io.


Features
--------

* Define your filters in Python
* Pipe your output to Wireshark or TShark for visualization
* Manipulate the payloads using Python's 3 byte regxes
* Save results to pcap files
* Work in progress *live reload* of your filter file

Credits
-------

This project relies on the power of Scapy_ for either filtering or payload modification.
This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Scapy: https://scapy.net/
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
