# -*- coding: utf-8 -*-

FILTER_TEMPLATE = """\
from scapy.all import *
from logging import getLogger

LOG = getLogger(__name__)


def packet_filter(packet):

    #if IP in packet and UDP in packet:
    #   LOG.info('Package has UDP data')
    #if IP in packet and TCP in packet:
    #   LOG.info('Package has TCP data')

    return packet
"""
