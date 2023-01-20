import net_info
import net_scan
import logger
import device_info
import platform
import os
import argparse

parser = argparse.ArgumentParser(description="security multitool")
parser.add_argument('-o', '--operation', help="operation to execute", required=True)
parser.add_argument('-m', '--mode', help="operation mode")
parser.add_argument('-t', '--target', help='target', nargs='+')

try:
    args = parser.parse_args()
    if args.target is not None and len(args.target) not in (1, 2):
        parser.error("target arguments must or or two host numbers/ ipv4 address")
except Exception as err:
    exit(-2)

VENDORS_FILE = 'vendors.txt'
OS_WIN = "Windows"
APP_NAME = "Naughtius-Maximus"
STORAGE_DIR = f"{os.getenv('APPDATA')}\\{APP_NAME}\\" if platform.system() == OS_WIN \
    else f"/opt/{APP_NAME}/"

if not os.path.exists(STORAGE_DIR):
    try:
        os.mkdir(STORAGE_DIR)
    except:
        print(f"cannot create {STORAGE_DIR} \n exiting")
        exit(-1)

log = logger.Logger(STORAGE_DIR)
log.log_info(f"{APP_NAME} starting", True, True)

log.log_info("getting network data", True)
valid, host, mask = net_info.get_interface_data()
if valid is False:
    log.log_err("could not obtain interface info", True, True)
    log.log_info(f"{APP_NAME} exiting", True, True)
    exit(-1)

log.log_debug(f"host is {host}, mask is {mask}")

log.log_info("calculating network range", True, True)
net_addr, net_broadcast = net_info.calc_network_span(host, mask)
log.log_debug(f"network address {net_info.to_string(net_addr)}, broadcast {net_info.to_string(net_broadcast)}", True, True)

# main loop
# add support for argv
net_scan.module_init(host, log)
device_info.module_init(STORAGE_DIR, VENDORS_FILE)

if not os.path.isfile(STORAGE_DIR + VENDORS_FILE):
    log.log_info("no vendor table found... updating vendor table", False, True)
    device_info.update_vendors()
    log.log_info("update complete", False, True)

discovered = []
operation = args.operation

if operation == 'scan':
    if args.mode == 'arp':
        discovered = net_scan.scan_net(net_addr, net_broadcast)
        log.log_debug(f"{len(discovered)} hosts discovered", True, True)
        print()
        for i, device in enumerate(discovered):
            log.log_debug(f"{i + 1}\tip: {device[0]:<15}\tMAC: {device[1]:<17}\t{device_info.resolve_mac(device[1])}",
                          True, True)
    elif args.mode == 'syn':
        ports = []
        if args.target is None or len(args.target) != 1:
            log.log_err("you must select one target to scan", False, True)
            exit(-1)
        if args.target[0].isdigit():
            pass  # handle persistent target selection
        elif net_info.validate_ipv4_address(args.target[0]):
            open_ports = net_scan.port_scan(net_addr, mask, args.target[0])
        else:
            log.log_err("invalid ip/target number")
            exit(-1)

elif operation == 'deauth':
    if args.mode == 'bluetooth':
        pass
    elif args.mode == 'wifi':
        pass

log.log_info(f"{APP_NAME} exiting", True, False)
exit(0)
