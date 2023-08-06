#!/usr/bin/env python3

import sys
import time

try:
    import tkinter
    native = False          # do not use Linux native programs
except Exception:
    import subprocess
    native = True           # use Linux native


def get_screen_width(width=True, height=False):
    """
    Summary:
        Uses TKinter module in the standard library to find screen dimensions
    Args:
        :width (bool):  If True, return screen width in columns (DEFAULT)
        :height (bool): If True, return screen height in rows
    Returns:
        Screen width, height, TYPE: int
    """
    if native:
        cols = subprocess.getoutput('tput cols')
        rows = subprocess.getoutput('tput lines')
    else:
        root = Tkinter.Tk()
        cols = root.winfo_screenwidth()
        rows = root.winfo_screenheight()

    if height:
        return int(rows)
    elif width and height:
        return int(cols), int(rows)
    return int(cols)


def progress_meter(width=None, delay=0.1, icon='.'):
    """
    Summary:
        Graphical progress meter
    Args:
        :icon (str): Character to print in pattern
        :width (int): Width of pattern to print (columns)
        :delay (int): Delay between prints (seconds)
    Returns:
        stdout pattern
    """
    if width is None:
        stop = (get_screen_width() / 3)
        print(f'stop is: {stop}')
    else:
        stop = width

    for i in range(0,stop + 1):

        if i == 0:
            sys.stdout.write('\t%s' % icon)
            time.sleep(delay)

        elif i > stop:
            sys.stdout.write('\n')
            i = 0

        else:
            sys.stdout.write('%s' % icon)
            time.sleep(delay)

print('Width is: %d' % get_screen_width())
print('Ht is: %d' % get_screen_width(width=False, height=True))
progress_meter(width=80)
