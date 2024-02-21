import netifaces
import psutil
import subprocess
from scapy.all import *

class cmdError(Exception):
    def __int__(self,msg, code):
        super(cmdError, self).__int__(msg)
        self.code=code



ADDRESS_LENGTH = 4
ARP_WHO_HAS = 1
MODE_ON = True
MODE_OFF = False
MODE_MONITR = 'monitor'
MODE_MANAGED = 'managed'
def get_interface_data(os_name):
    addrs = psutil.net_if_addrs()
    for interface in addrs:
        iface_name = interface.lower()
        if os_name == 'nt':
            if "wi-fi" in iface_name or 'ethernet' in iface_name:
                interface_data = addrs[interface][1]
                if interface_data.address.split('.')[0] == '10' or interface_data.address.split('.')[0] == '192':
                    return True, interface_data[1], interface_data[2], None
        else:
            if iface_name != 'lo' and len(interface) == 6:
                interface_data = addrs[interface][0]
                return True, interface_data[1], interface_data[2], interface

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
    except:
        return False


def is_local(host, mask, net_addr):
    temp = []
    for i in range(ADDRESS_LENGTH):
        temp.append(mask[i] & host[i])
    return temp == net_addr


def query_arp(address):
    result = subprocess.run(f"arping {address} -f -c 10", shell=True,
                            stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    try:
        mac = result.stdout.decode().split('[')[1].split(']')[0]
        return mac
    except IndexError as e:
        return None


def get_gateway():
    gateway_ipv4 = netifaces.gateways()['default']
    if not gateway_ipv4:
        return None, None
    gateway_ipv4 = gateway_ipv4[2][0]
    gateway_mac = query_arp(gateway_ipv4)
    return gateway_mac, gateway_ipv4


# need to add support for multi iface
def linux_get_iface_data():
    result = subprocess.run(['iw', 'dev'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Extract the wireless interface names from the output
    output = result.stdout.decode('utf-8')
    lines = output.split('\n')
    wifi_interfaces = []
    iface = ""
    for line in lines:
        if 'Interface' in line:
            iface = line.split(' ')[1]
        if 'channel' in line:
            wifi_interfaces.append((iface, line.split(' ')[1]))
    # Get information about the first wireless interface
    if len(wifi_interfaces) > 0:
        result = subprocess.run(['iw', 'dev', wifi_interfaces[0][0], 'link'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        lines = output.split('\n')
        for line in lines:
            if 'Connected to' in line:
                bssid = line.split(' ')[2]

        # Return the wireless interface name, BSSID, and channel
        return wifi_interfaces[0][0], bssid, wifi_interfaces[0][1]
    else:
        return None, None, None


def toogle_monitor_mode(interface, mode=MODE_ON):
    result = subprocess.run(["sudo", "ifconfig", interface, "down"])
    if result.returncode == 1:
        raise cmdError(msg=f"cannot disable interface {interface}", code=-1)
    if mode == MODE_ON:
        result = subprocess.run(["sudo", "ifconfig",interface, f"mode {MODE_MONITR}"])
        if result.returncode == 1:
            raise cmdError(msg=f"cannot set interface {interface} to monitor mode", code=-2)
    else:
        result = subprocess.run(["sudo", "ifconfig",interface, f'mode {MODE_MANAGED}'])
        if result.returncode == 1:
            raise cmdError(msg=f"cannot set interface {interface} to managed mode", code=-3)
    result = subprocess.run(["sudo", "ifconfig",interface, "up"])
    if result.returncode == 1:
        raise cmdError(msg=f"cannot enable interface {interface}", code=-4)
