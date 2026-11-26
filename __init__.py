import os
from datetime import datetime
from cudatext import *
import locale
import random

from cudax_lib import get_translation
_ = get_translation(__file__)

class Command:
    fn_config = None
    only_in_december = 1
    tree = None
    title = 'HappyNewYear!'

    def on_start2(self, ed_self):
        self.fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_happy_new_year.ini')
        self.only_in_december = self.get_only_in_december()
        if not self.only_in_december:
            self.init_panel()
        else:
            if self.is_december():
                self.init_panel()

    def get_only_in_december(self):
        only_in_december = ini_read(self.fn_config, 'options', 'only_in_december', '-')
        if (only_in_december == '-'):
            ini_write(self.fn_config, 'options', 'only_in_december', str(self.only_in_december))
        if only_in_december == '-' or only_in_december == '1':
            return True
        else:
            return False

    def word_division(self, text, count = 3):
        words = text.split()
        i = 0
        words_ = ''
        res = []
        for word in words:
            i = i + 1
            words_ = words_ + word + ' '
            if i == count:
                res.append(words_)
                i = 0
                words_ = ''
        len_ = len(words) - len(res) * 3
        if (len_ > 0):
            words_ = ''
            for word_ in words[len(words) - len_:len(words)]:
                words_ = words_ + word_ + ' '
            res.append(words_)

        return res

    def get_random_line(self):
        fn = 'ru.txt' if 'ru' in locale.getlocale()[0] else 'en.txt'
        path = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'data' + os.sep + fn
        if os.path.isfile(path):
            with open(path, 'r', encoding = 'utf-8') as file:
                lines = file.readlines()
                if not lines:
                    return None
                line = random.choice(lines).rstrip('\n')
                res = self.word_division(line)

                return res
        else:
            print(f'error: file "{fn}" not found')

    def get_days(self):
        return '{}'.format((datetime(int(datetime.now().strftime('%Y')) + 1, 1, 1) - datetime.today()).days)

    def get_msg(self):
        return self.word_division(_('There are left until the New Year (days)') + ': ' + self.get_days())

    def is_december(self):
        return int(datetime.now().strftime('%m')) == 12

    def init_panel(self):
        btn_h_ = ''
        for item in app_proc(PROC_SIDEPANEL_ENUM_ALL, ''):
            if item['cap'] == self.title:
                btn_h_ = item['btn_h']
        if btn_h_ != '':
            button_proc(btn_h_, BTN_SET_OVERLAY, '0')

        self.h_dlg = dlg_proc(0, DLG_CREATE)

        n = dlg_proc(self.h_dlg, DLG_CTL_ADD, prop='treeview')
        dlg_proc(self.h_dlg, DLG_CTL_PROP_SET, index=n, prop={
            'name': 'tree',
            'a_r': ('',']'),
            'a_b': ('',']')
        })

        self.tree = dlg_proc(self.h_dlg, DLG_CTL_HANDLE, index=n)
        tree_proc(self.tree, TREE_PROP_SHOW_ROOT, text='0')

        dlg_proc(self.h_dlg, DLG_SCALE)
        tree_proc(self.tree, TREE_THEME)

        app_proc(PROC_SIDEPANEL_ADD_DIALOG, (
            self.title,
            self.h_dlg,
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img', 'hny.png')
        ))

        btn_h_ = ''
        for item in app_proc(PROC_SIDEPANEL_ENUM_ALL, ''):
            if item['cap'] == self.title:
                btn_h_ = item['btn_h']
        if btn_h_ != '':
            button_proc(btn_h_, BTN_SET_OVERLAY, self.get_days())

        app_proc(PROC_SIDEPANEL_ACTIVATE, (self.title, True))

        res1 = self.get_msg()
        if res1:
            for i in res1:
                tree_proc(self.tree, TREE_ITEM_ADD, index=-1, text=i)
            tree_proc(self.tree, TREE_ITEM_ADD, index=-1, text='* * *')
        res2 = self.get_random_line()
        if res2:
            for i in res2:
                tree_proc(self.tree, TREE_ITEM_ADD, index=-1, text=i)

    def config(self):
        file_open(self.fn_config)
