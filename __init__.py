import os
from datetime import datetime
from cudatext import *

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_happy_new_year.ini')

last_start = 0


def is_december():
    return int(datetime.now().strftime('%m')) == 12


def get_ymd():
    return datetime.now().strftime('%y%m%d')


def get_last_start():
    global last_start
    last_start = ini_read(fn_config, 'options', 'last_start', str(last_start))

    if (int(last_start) == 0):
        last_start = get_ymd()
        out_msg()

    return last_start


def out_msg():
    now = datetime.today()
    ny = datetime(int(datetime.now().strftime('%Y')) + 1, 1, 1)
    d = ny - now
    mm, ss = divmod(d.seconds, 60)
    hh, mm = divmod(mm, 60)
    res = '{} days {} hours {} minutes {} seconds'.format(d.days, hh, mm, ss)

    msg_box('There are left until the New Year: ' + res, MB_OK)


class Command:
    def on_start(self, ed_self):
        if (is_december()):
            global last_start
            if (get_ymd() != get_last_start()):
                last_start = get_ymd()
                out_msg()

        ini_write(fn_config, 'options', 'last_start', str(last_start))

    def config(self):
        file_open(fn_config)
