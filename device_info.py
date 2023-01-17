from mac_vendor_lookup import MacLookup, BaseMacLookup

mac = None
is_initialized = False
CHACHE_FILE = 'vendors.txt'


def module_init(storage_dir):
    global mac, is_initialized
    BaseMacLookup.cache_path = storage_dir + CHACHE_FILE
    mac = MacLookup()
    is_initialized = True


def update_vendors():
    if mac is None:
        return False
    mac.update_vendors()
    return True


def resolve_mac(address):
    if mac is None:
        return False
    return mac.lookup(address)
