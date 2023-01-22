import mac_vendor_lookup
import socket

mac = None
is_initialized = False
cache_file = ''
default_gateway = ''


def module_init(storage_dir, file_name):
    global mac, is_initialized, cache_file, default_gateway
    cache_file = file_name
    mac_vendor_lookup.BaseMacLookup.cache_path = storage_dir + cache_file
    mac = mac_vendor_lookup.MacLookup()
    is_initialized = True


def update_vendors():
    if mac is None:
        return False
    mac.update_vendors()
    return True


def resolve_mac(address):
    if mac is None:
        return False
    try:
        return mac.lookup(address)
    except mac_vendor_lookup.VendorNotFoundError:
        return 'UNKNOWN VENDOR'


def get_name(addr):
    try:
        return socket.gethostbyaddr(addr)[0]
    except:
        return 'UNKNOWN NAME'
