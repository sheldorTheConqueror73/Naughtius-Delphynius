import netifaces
import psutil
from scapy.all import *
ADDRESS_LENGTH = 4
ARP_WHO_HAS = 1

def get_interface_data(os_name):
    addrs = psutil.net_if_addrs()
    for interface in addrs:
        iface_name =interface.lower()
        if os_name == 'nt':
            if "wi-fi" in iface_name or 'ethernet' in iface_name:
                interface_data = addrs[interface][1]
                if interface_data.address.split('.')[0] == '10' or interface_data.address.split('.')[0] == '192':
                    return True, interface_data[1], interface_data[2]
        else:
            if iface_name != 'lo' and len(interface) == 6:
                interface_data = addrs[interface][0]
                return True, interface_data[1], interface_data[2]

    return False, None, None


# maybe use socket instead?
def to_ipv4(address):
    return [int(i) for i in address.split('.')]


def to_string(address):
    return "".join([str(address[i // 2]) if not i % 2 else '.' for i in range(2 * ADDRESS_LENGTH - 1)])


def calc_network_span(host, mask):
    host_addr = to_ipv4(host)
    net_mask = to_ipv4(mask)
    net_start = [host_addr[i] & net_mask[i] for i in range(ADDRESS_LENGTH)]
    net_end = [(host_addr[i] | (~net_mask[i])) & 0xff for i in range(ADDRESS_LENGTH)]
    return net_start, net_end


def get_next_address(start, end, current):
    for i in range(ADDRESS_LENGTH - 1, 0, -1):
        if current[i] != 255:
            current[i] += 1
            break
        else:
            current[i] = 0

    if end == current:
        return False, None
    return True, current


def validate_ipv4_address(address):
    try:
        socket.inet_aton(address)
        return True
    except :
        return False


def is_local(host, mask, net_addr):
    temp = []
    for i in range(ADDRESS_LENGTH):
        temp.append(mask[i] & host[i])
    return temp == net_addr

def query_arp(address):
    p = Ether(dst=ETHER_BROADCAST) / ARP(op=ARP_WHO_HAS, pdst=address)
    response = srp1(p, timeout=0.001, verbose=0)
    if response and ARP in response:
        return response[ARP].hwsrc
    return None
def get_gateway():
    gateway_ipv4 = netifaces.gateways()['default'][2][0]
    gateway_mac = query_arp(gateway_ipv4)
    return gateway_mac, gateway_ipv4
