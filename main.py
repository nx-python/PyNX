import imgui
import imguihelper
import os
import _nx
import runpy
import sys
import time
from imgui.integrations.nx import NXRenderer
from nx.utils import clear_terminal
import traceback

sys.argv = [""]  # workaround needed for runpy

def colorToFloat(t):
    nt = ()
    for v in t:
        nt += ((1/255) * v, )
    return nt

# (r, g, b)
FOLDER_COLOR = colorToFloat((230, 126, 34))
PYFILE_COLOR = colorToFloat((46, 204, 113))
FILE_COLOR = colorToFloat((41, 128, 185))

ERROR = ""

TILED_DOUBLE = 1
def run_python_module(path: str):
    global ERROR
    # clear both buffers
    imguihelper.clear()
    imguihelper.clear()
    _nx.gfx_set_mode(TILED_DOUBLE)
    clear_terminal()
    try:
        runpy.run_path(path, run_name='__main__')
    except Exception as e:
        ERROR = traceback.format_exc()
    imguihelper.initialize()


def main():
    global ERROR
    renderer = NXRenderer()
    currentDir = os.getcwd()

    while True:
        renderer.handleinputs()

        imgui.new_frame()

        width, height = renderer.io.display_size
        imgui.set_next_window_size(width, height)
        imgui.set_next_window_position(0, 0)
        imgui.begin("", 
            flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_SAVED_SETTINGS
        )
        imgui.text("Welcome to PyNX!")
        imgui.text("Touch is supported")
        imgui.text("Current dir: " + os.getcwd())

        if os.getcwd() != "sdmc:/":
            imgui.push_style_color(imgui.COLOR_BUTTON, *FOLDER_COLOR)
            if imgui.button("../", width=200, height=60):
                os.chdir("..")
            imgui.pop_style_color(1)
        
        dirs = []
        files = []
        for e in os.listdir():
            if os.path.isdir(e):
                dirs.append(e)
            else:
                files.append(e)
        
        dirs = sorted(dirs)
        files = sorted(files)

        for e in dirs:
            imgui.push_style_color(imgui.COLOR_BUTTON, *FOLDER_COLOR)
            if imgui.button(e + "/", width=200, height=60):
                os.chdir(e)
            imgui.pop_style_color(1)

        for e in files:
            if e.endswith(".py"):
                imgui.push_style_color(imgui.COLOR_BUTTON, *PYFILE_COLOR)
            else:
                imgui.push_style_color(imgui.COLOR_BUTTON, *FILE_COLOR)

            if imgui.button(e, width=200, height=60) and e.endswith(".py"):
                run_python_module(e)
            
            imgui.pop_style_color(1)

        
        imgui.end()

        if ERROR:
            imgui.set_next_window_size(width, height)
            imgui.set_next_window_position(0, 0)
            imgui.begin("ERROR", 
                flags=imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_SAVED_SETTINGS
            )
            imgui.text(str(ERROR))
            if imgui.button("OK", width=200, height=60):
                ERROR = ""
            imgui.end()

        imgui.render()
        renderer.render()

    renderer.shutdown()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        imguihelper.clear()
        imguihelper.clear()
        _nx.gfx_set_mode(TILED_DOUBLE)
        clear_terminal()
        traceback.print_exc()
