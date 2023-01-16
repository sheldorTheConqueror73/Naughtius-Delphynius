import psutil

ADDRESS_LENGTH = 4


def get_interface_data():
    addrs = psutil.net_if_addrs()
    for interface in addrs:
        if "wi-fi" in interface.lower() or 'ethernet' in interface.lower():
            interface_data = addrs[interface][1]
            if interface_data.address.split('.')[0] == '10' or interface_data.address.split('.')[0] == '192':
                return True, interface_data[1], interface_data[2]
    return False, None, None


def to_ipv4(address):
    return [int(i) for i in address.split('.')]


def to_string(address):
    return "".join([str(address[i//2]) if not i % 2 else '.' for i in range(2 * ADDRESS_LENGTH - 1)])


def calc_network_span(host, mask):
    host_addr = to_ipv4(host)
    net_mask = to_ipv4(mask)
    net_start = [host_addr[i] & net_mask[i] for i in range(ADDRESS_LENGTH)]
    net_end = [(host_addr[i] | (~net_mask[i])) & 0xff for i in range(ADDRESS_LENGTH)]
    print(f" calculating net info\n net start :{to_string(net_start)} \n net end: {to_string(net_end)}" )
    return net_start, net_end

def get_next_address(start, end, current):
    for i in range(ADDRESS_LENGTH-1, 0, -1):
        if current[i] != 255:
            current[i] += 1
            break
        else:
            current[i] = 0

    if end == current:
        return False, None
    return True, current

