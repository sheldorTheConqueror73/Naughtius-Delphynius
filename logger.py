from util import get_current_time as get_time


class Logger:
    LOG_FILE = None
    LOGGER_ACTIVE = True

    def __init__(self, log_dir: str):
        if Logger.LOG_FILE is None and Logger.LOGGER_ACTIVE:
            try:
                Logger.LOG_FILE = open(f"{log_dir} log.txt", 'w')
            except OSError:
                Logger.LOG_FILE = None
                Logger.LOGGER_ACTIVE = False

    def __del__(self):
        if Logger.LOG_FILE is None:
            return
        Logger.LOG_FILE.close()
        Logger.LOG_FILE = None
        Logger.LOGGER_ACTIVE = False

    def log(self, prefix, msg, timestamp=False, print_msg=False, redir=None):
        if print_msg:
            print(msg)
        if Logger.LOG_FILE is None:
            return False
        Logger.LOG_FILE.write(f"{prefix} {f'[{get_time()}] ' if timestamp else ''}{msg}\n")
        Logger.LOG_FILE.flush()
        if redir:
            pass  # write function for redir here
        return True

    def log_info(self, msg, timestamp=False, print_msg=False, redir=None):
        return self.log("[INFO]", msg, timestamp, print_msg, redir)

    def log_debug(self, msg, timestamp=False, print_msg=False, redir=None):
        return self.log("[debug]", msg, timestamp, print_msg, redir)

    def log_err(self, msg, timestamp=False, print_msg=False, redir=None):
        return self.log("[ERROR]", msg, timestamp, print_msg, redir)

    def log_panic(self, msg, timestamp=False, print_msg=False, redir=None):
        return self.log("[PANIC]", msg, timestamp, print_msg, redir)
