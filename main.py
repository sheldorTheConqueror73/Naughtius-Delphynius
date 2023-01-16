import net_info
import net_scan
import logger
import platform
import os

OS_WIN = "Windows"
OS_LINUX = "Linux"
APP_NAME = "Naughtius-Maximus"
STORAGE_DIR = f"/opt/{APP_NAME}/" if platform.system() == OS_LINUX \
    else f"{os.getenv('APPDATA')}\\{APP_NAME}\\"

log = logger.Logger(STORAGE_DIR)

log.log_info(f"{APP_NAME} started", timestamp=True, print_msg=True)
if not os.path.exists(STORAGE_DIR):
    try:
        os.mkdir(STORAGE_DIR)
    except:
        print(f"cannot create {STORAGE_DIR} \n exiting")
        exit(-1)

valid, host, mask = net_info.get_interface_data()
if valid is False:
    print("could not obtain intercae info")
    exit(-1)

start, end = net_info.calc_network_span(host, mask)
discovered = net_scan.scan(host,start,end)
print(f"{len(discovered)} hosts discovered")

