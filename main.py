import sys
from glob import glob
import os
import runpy
import time
import _nx
import nx
from nx.utils import AnsiMenu, clear_terminal


sys.argv = [""]  # workaround needed for runpy

TILED_DOUBLE = 1
MAIN_PY = 'main.py'
PYNX_DIR_PATH = os.getcwd()


def run_python_module(path: str):
    runpy.run_path(path, run_name='__main__')
    _nx.gfx_set_mode(TILED_DOUBLE)
    print("{} exited.".format(selected))


def confirmation_prompt(program_name: str):
    name = program_name[:-3] if program_name.endswith('.py') else program_name
    name = name[:-1] if name.endswith(os.sep) else name
    print("Do you want to execute the Python program {}?\n"
          "Press A to confirm, B to cancel.".format(name))
    while True:
        nx.refresh_inputs()
        if nx.p1.a_button.is_pressed:
            return True
        elif nx.p1.b_button.is_pressed:
            return False
        time.sleep(0.01)


if __name__ == '__main__':
    while True:
        clear_terminal()
        dirs = ["../"] + glob("*/")
        scripts = glob("*.py")
        if os.getcwd() == PYNX_DIR_PATH and MAIN_PY in scripts:
            scripts.remove(MAIN_PY)
        for _dir in dirs:
            if os.path.isfile(os.path.join(_dir, MAIN_PY)):
                dirs.replace(_dir, _dir[:-1])
        listing = dirs + scripts
        file_menu = AnsiMenu(listing)
        print("Listing for {}:".format(os.getcwd()))
        selected = listing[file_menu.query()]
        clear_terminal()
        if selected in dirs:
            os.chdir(selected)
            if os.path.isfile(MAIN_PY) and not selected == '../' and not os.getcwd() == PYNX_DIR_PATH:
                response = confirmation_prompt(selected)
                clear_terminal()
                if response is True:
                    run_python_module(MAIN_PY)
                    os.chdir(os.pardir)
        else:
            response = confirmation_prompt(selected)
            clear_terminal()
            if response is True:
                run_python_module(selected)
