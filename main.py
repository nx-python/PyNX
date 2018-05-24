import sys
from glob import glob
import os
import runpy
import time
import _nx
import nx
from nx.utils import AnsiMenu


sys.argv = [""]  # workaround needed for runpy

TILED_DOUBLE = 1
MAIN_PY = 'main.py'
PYNX_DIR_PATH = os.getcwd()


def run_python_module(path: str):
    runpy.run_path(path, run_name='__main__')
    _nx.gfx_set_mode(TILED_DOUBLE)
    print("{} exited.".format(selected), flush=True)


def clear_screen():
    sys.stdout.buffer.write(b"\x1b[2J")
    sys.stdout.buffer.flush()


def confirmation_prompt(program_name: str):
    name = program_name[:-3] if program_name.endswith('.py') else program_name
    name = name[:-1] if name.endswith(os.sep) else name
    print("Do you want to execute the Python program {}?\n"
          "Press A to confirm, B to cancel.".format(name), flush=True)
    while True:
        nx.refresh_inputs()
        if nx.p1.a_button.is_pressed:
            return True
        elif nx.p1.b_button.is_pressed:
            return False
        time.sleep(0.01)


if __name__ == '__main__':
    while True:
        clear_screen()
        dirs = ["../"] + glob("*/")
        scripts = glob("*.py")
        if os.getcwd() == PYNX_DIR_PATH and MAIN_PY in scripts:
            scripts.remove(MAIN_PY)
        listing = dirs + scripts
        file_menu = AnsiMenu(listing)
        print("Listing for {}:".format(os.getcwd()), flush=True)
        selected = listing[file_menu.query()]
        clear_screen()
        if selected in dirs:
            os.chdir(selected)
            if os.path.isfile(MAIN_PY) and not selected == '../' and not os.getcwd() == PYNX_DIR_PATH:
                response = confirmation_prompt(selected)
                clear_screen()
                if response is True:
                    run_python_module(MAIN_PY)
                    os.chdir(os.pardir)
        else:
            response = confirmation_prompt(selected)
            clear_screen()
            if response is True:
                run_python_module(selected)
