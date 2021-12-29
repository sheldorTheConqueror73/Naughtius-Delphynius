from scapy.all import *
import info
MODE_ARP = 1
ARP_WHO_HAS =1
def arp_scan(host, current):
    p = Ether(dst=ETHER_BROADCAST)/ARP(op=ARP_WHO_HAS,pdst=current, psrc=host)
    return srp1(p, timeout = 0.001, verbose =0) #shortest response time was  0.00000035


SCAN_DIC = {MODE_ARP: arp_scan}

def scan(host, start, end, mode=MODE_ARP):
    discovered = []
    method = SCAN_DIC[mode]
    valid, current =info.get_next_address(start, end, start)
    while valid:
        current_string=info.to_string(current)
        response = method(host, current_string)
        if response is not None and ARP in response:
            #print(f'discovered {current_string}')
            print(current_string)
            discovered.append((current,))
        valid, current = info.get_next_address(start, end, start)
    return discovered
