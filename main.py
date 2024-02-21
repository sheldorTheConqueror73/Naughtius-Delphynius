#!/usr/bin/python3
import subprocess
import sys

import net_info
import net_scan
import net_attack
import logger
import device_info
import os
import argparse
import keyboard

ALL_GOOD = 0
ARGS_INAVL = -1
NET_ERR = -2
NO_ACCESS = -3
IO_ERR = -4
NO_TARGET = -5

def read_key():
    return keyboard.read_key()


def spinner():
    while True:
        for cursor in '|/—\\':
            yield cursor


# spin = spinner()


banner = r"""
 _   _                   _     _   _           
| \ | | __ _ _   _  __ _| |__ | |_(_)_   _ ___ 
|  \| |/ _` | | | |/ _` | '_ \| __| | | | / __|
| |\  | (_| | |_| | (_| | | | | |_| | |_| \__ \
|_| \_|\__,_|\__,_|\__, |_| |_|\__|_|\__,_|___/
 __  __            |___/                       
|  \/  | __ ___  _(_)_ __ ___  _   _ ___       
| |\/| |/ _` \ \/ / | '_ ` _ \| | | / __|      
| |  | | (_| |>  <| | | | | | | |_| \__ \      
|_|  |_|\__,_/_/\_\_|_| |_| |_|\__,_|___/      
"""

parser = argparse.ArgumentParser(description="security multitool")
parser.add_argument('-o', '--operation', choices=['scan', 'deauth'], help="operation to execute")
parser.add_argument('-m', '--mode', choices=['arp', 'syn', 'wifi'], help="operation mode")
parser.add_argument('-t', '--target', help='target', nargs='+')
parser.add_argument('-d', '--duration', help='duration of operation')

try:
    args = parser.parse_args()
    if args.target is not None and len(args.target) not in (1, 2):
        parser.error("target arguments must one or or two host IDs/ipv4 address")
except Exception as err:
    exit(ARGS_INAVL)

if len(sys.argv) == 1:
    pass  # start in UI mode
else:
    pass  # start in command mode

VENDORS_FILE = 'vendors.txt'
OS_WIN = "nt"
APP_NAME = "Naughtius-Maximus"
STORAGE_DIR = f"{os.getenv('APPDATA')}\\{APP_NAME}\\" if os.name == OS_WIN \
    else f"/opt/.{APP_NAME}/"
CURR_DIR = os.getcwd()
log = logger.Logger(STORAGE_DIR)
log.log_info(f"{APP_NAME} starting", True, True)

if os.getuid() != 0:
    log.log_err("root access required.... exiting", print_msg=True)
    exit(NO_ACCESS)

print(banner)

if os.environ.get('SUDO_USER'):
    USER = os.environ['SUDO_USER']
else:
    USER = os.environ['USER']
result = subprocess.run(f"sudo runuser -l {USER} -c'aplay {CURR_DIR}/resources/scooby_laugh.wav'", shell=True,
                        stderr=subprocess.PIPE, stdout=subprocess.PIPE)

if result.returncode == 1:
    print(result.stderr, USER)
    print("EXTINGFDG")
    #exit(IO_ERR)

#check for dependencies

target_bank = []

gateway_mac, gateway_ip = net_info.get_gateway()
if not gateway_ip:
    log.log_err("no network tedcted. exiting....", False, True)
    exit(NET_ERR)

if not os.path.exists(STORAGE_DIR):
    try:
        os.mkdir(STORAGE_DIR)
    except:
        print(f"cannot create {STORAGE_DIR} \n exiting")
        exit(IO_ERR)

log.log_info("getting network data", True)
valid, host, mask, iface_name = net_info.get_interface_data(os.name)
if valid is False:
    log.log_err("could not obtain interface info", True, True)
    log.log_info(f"{APP_NAME} exiting", True, True)
    exit(NET_ERR)
log.log_debug(f"host is {host}, mask is {mask}")

"""
log.log_info('trying to anble monitor mode', False, True)
try:
    net_info.toogle_monitor_mode(iface_name.strip())
    log.log_info('monitor mode enabled', False, True)
except net_info.cmdError as e:
    log.log_info(e.msg, False, True)
"""

log.log_info("calculating network range", True, True)
net_addr, net_broadcast = net_info.calc_network_span(host, mask)
log.log_debug(f"network address {net_info.to_string(net_addr)}, broadcast {net_info.to_string(net_broadcast)}", True,
              True)

# main loop
net_scan.module_init(host, log)
device_info.module_init(STORAGE_DIR, VENDORS_FILE)
net_attack.module_init(log)

if not os.path.isfile(STORAGE_DIR + VENDORS_FILE):
    log.log_info("no vendor table found... updating vendor table", False, True)
    device_info.update_vendors()
    log.log_info("update complete", False, True)

discovered_hosts = []
operation = args.operation
mode = args.mode




def scan():
    global discovered_hosts
    if operation == 'scan':
        if mode == 'arp':
            discovered_hosts = net_scan.scan_net(net_addr, net_broadcast)
            log.log_debug(f"{len(discovered_hosts)} hosts discovered", True, True)
            print()
            for i, device in enumerate(discovered_hosts):
                vendor = device_info.resolve_mac(device['mac'])
                name = device_info.get_name(device['ipv4'])
                log.log_debug(f"{i + 1}\tip: {device['ipv4']:<15}\tMAC: {device['mac']:<17}\t{vendor:<30}\t{name}",
                              True,
                              True)

        elif mode == 'syn':
            ports = []
            if args.target[0].isdigit():
                pass  # handle persistent target selection
            elif net_info.validate_ipv4_address(args.target[0]):
                open_ports = net_scan.port_scan(net_addr, mask, args.target[0])
            else:
                log.log_err("invalid ip/target number")
                exit(ARGS_INAVL)


def deauth():
    if mode == 'bluetooth':
        print('not implemented yet')
        pass

    elif mode == 'wifi':
        if args.target == 'all':
            net_attack.wifi_deauth_all(gateway_mac)
        elif net_info.validate_ipv4_address(args.target[0]):
            target_mac = net_info.query_arp(args.target[0])
            if not  target_mac:
                log.log_err(f"cannot resolve mac addresss for target {args.target[0]}", print_msg=True)
                exit(NO_TARGET)
            net_attack.send_deauth(target_mac, iface_name, gateway_mac)
        elif args.target.isdigit():
            pass  # handle persistent target selection




MENU_OPS = {'deauth':deauth , 'scan': scan}

MENU_OPS[operation]();

log.log_info(f"{APP_NAME} exiting", True, False)
exit(ALL_GOOD)
