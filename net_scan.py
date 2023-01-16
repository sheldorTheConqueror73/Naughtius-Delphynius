from scapy.all import *
import threading
import net_info

MODE_ARP = 1
ARP_WHO_HAS = 1
ARP_IS_AT = 2
discovered = []


def arp_scan(host, current):
    p = Ether(dst=ETHER_BROADCAST) / ARP(op=ARP_WHO_HAS, pdst=current, psrc=host)
    return srp1(p, timeout=0.001, verbose=0)  # shortest response time was  0.00000035


SCAN_DIC = {MODE_ARP: arp_scan}


def scan(host, start, end, mode=MODE_ARP):
    global discovered
    discovered = []
    stop_event = threading.Event()
    t = threading.Thread(target=sniff_arp, args=(stop_event,))
    t.start()
    method = SCAN_DIC[mode]
    valid, current = net_info.get_next_address(start, end, start)
    while valid:
        current_string = net_info.to_string(current)
        response = method(host, current_string)
        valid, current = net_info.get_next_address(start, end, start)

    stop_event.set()
    t.join()
    print("scan complete")
    return discovered


def handle_arp_response(frame):
    ip = frame[ARP].psrc
    mac = frame[ARP].hwsrc
    print(f'discovered {ip} \t MAC: {mac}')
    if (ip, mac) not in discovered:
        discovered.append((ip, mac))



def sniff_arp(stop_event):
    print("arp listener up")
    while not stop_event.is_set():
        answers = sniff(lfilter=lambda x: ARP in x and x[ARP].op == ARP_IS_AT, prn=handle_arp_response, store=0, timeout=3)
    print("arp listener stopped")