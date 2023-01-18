from scapy.all import *
import threading
import net_info
import logger

MODE_ARP = 1
ARP_WHO_HAS = 1
ARP_IS_AT = 2
discovered = []
device_ip = ""
log = None
is_initialized = False

def module_init(host, main_log: logger.Logger):
    """
    initializes scan modules
    :param host: ip address of local device
    :param main_log: logger
    """
    global device_ip, log, is_initialized
    device_ip = host
    log = main_log
    is_initialized = True


def arp_scan(host, current):
    p = Ether(dst=ETHER_BROADCAST) / ARP(op=ARP_WHO_HAS, pdst=current, psrc=host)
    return srp1(p, timeout=0.001, verbose=0)  # shortest response time was  0.00000035


SCAN_DIC = {MODE_ARP: arp_scan}


def scan(start, end, mode=MODE_ARP):
    if not is_initialized:
        return []
    global discovered
    discovered = []
    stop_event = threading.Event()
    t = threading.Thread(target=sniff_arp, args=(stop_event,))
    t.start()
    method = SCAN_DIC[mode]
    valid, current = net_info.get_next_address(start, end, start)
    while valid:
        current_string = net_info.to_string(current)
        response = method(device_ip, current_string)
        valid, current = net_info.get_next_address(start, end, start)

    stop_event.set()
    t.join()
    log.log_info("scan complete")
    return discovered


def handle_arp_response(frame):
    ip = frame[ARP].psrc
    mac = frame[ARP].hwsrc
    log.log_debug(f'discovered {ip} \t MAC: {mac}', True)
    if (ip, mac) not in discovered and ip != device_ip:
        discovered.append((ip, mac))


def sniff_arp(stop_event):
    log.log_info("arp listener up")
    while not stop_event.is_set():
        answers = sniff(lfilter=lambda x: ARP in x and x[ARP].op == ARP_IS_AT, prn=handle_arp_response, store=0,
                        timeout=3)
    log.log_info("arp listener stopped")
