import net_info
import net_scan
import logger
import device_info
import platform
import os

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

log.log_info("calculating network range",True, True)
start, end = net_info.calc_network_span(host, mask)
log.log_debug(f"network address {net_info.to_string(start)}, broadcast {net_info.to_string(end)}",True, True)

net_scan.module_init(host,log)

discovered = net_scan.scan(start, end)
log.log_debug(f"{len(discovered)} hosts discovered", True, True)

device_info.module_init(STORAGE_DIR)
print()
for i,device in enumerate(discovered):
    log.log_debug(f"{i+1}\tip: {device[0]:<15}\tMAC: {device[1]:<17}\t{device_info.resolve_mac(device[1])}",True, True)
print()

log.log_info(f"{APP_NAME} exiting", True, True)
exit(0)