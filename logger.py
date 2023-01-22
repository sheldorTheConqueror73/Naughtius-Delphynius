from util import get_current_time_and_date as get_time_and_date, get_current_time as get_time


class Logger:
    LOG_FILE = None
    LOGGER_ACTIVE = True
    def __init__(self, log_dir: str):
        if Logger.LOG_FILE is None and Logger.LOGGER_ACTIVE:
            try:
                Logger.LOG_FILE = open(f"{log_dir} log.txt", 'w')
            except:
                Logger.LOG_FILE = None
                Logger.LOGGER_ACTIVE = False
    def __del__(self):
        if Logger.LOG_FILE is None:
            return
        Logger.LOG_FILE.close()
        Logger.LOG_FILE = None

    def log(self, prefix, msg, timestamp=False, print_msg=False):
        if print_msg:
            print(msg)
        if Logger.LOG_FILE is None:
            return False
        Logger.LOG_FILE.write(f"{prefix} {f'[{get_time()}] ' if timestamp else ''}{msg}\n")
        Logger.LOG_FILE.flush()
        return True

    def log_info(self, msg, timestamp=False, print_msg=False):
        return self.log("[INFO]", msg, timestamp, print_msg)

    def log_debug(self, msg, timestamp=False, print_msg=False):
        return self.log("[debug]", msg, timestamp, print_msg)

    def log_err(self, msg, timestamp=False, print_msg=False):
        return self.log("[ERROR]", msg, timestamp, print_msg)

    def log_panic(self, msg, timestamp=False, print_msg=False):
        return self.log("[PANIC]", msg, timestamp, print_msg)
