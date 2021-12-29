from scapy.all import *
from info import get_next_address as get_next
MODE_ARP = 1

def arp_scan(start, end, current):


SCAN_DIC = {MODE_ARP: arp_scan}

def scan(start, end, mode=MODE_ARP):
    method = SCAN_DIC[mode]
    valid, current = get_next(start, end, start)
    while valid:


