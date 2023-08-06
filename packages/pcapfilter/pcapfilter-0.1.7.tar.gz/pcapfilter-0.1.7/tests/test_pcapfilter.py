#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pytest_click import cli_runner
# Packet generation
from scapy.all import ICMP, IP, TCP, UDP, Ether, PcapNgReader, PcapWriter, PcapReader
from .utils import (
    PreloadedPcapWriter,
    ReadablePcapWriter,
    assert_same_packet,
)
from pcapfilter.pcapfilter import run_filter
from unittest import mock


def test_pcap_in_out(cli_runner):
    with mock.patch('pcapfilter.pcapfilter.LOGGER') as LOGGER:

        initial = Ether() / IP() / TCP()
        input_holder = PreloadedPcapWriter(
            initial_content=[initial]
        )
        output_holder = ReadablePcapWriter()

        retval = run_filter(
            reader_class=PcapNgReader,
            writer_class=PcapWriter,
            module=None,
            _input=input_holder.file_obj,
            _output=output_holder.file_obj,
        )
        assert retval == 0
        output = next(output_holder.get_contents())
        assert_same_packet(initial, output)
