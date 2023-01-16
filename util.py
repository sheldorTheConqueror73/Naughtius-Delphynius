import datetime


def get_current_time_and_date():
    return str(datetime.datetime.now()).split('.')[0]


def get_current_time():
    return get_current_time_and_date().split(' ')[1]
