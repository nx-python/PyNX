import imgui
import imguihelper
import os
import _nx
import runpy
import sys
from imgui.integrations.nx import NXRenderer
from nx.utils import clear_terminal
from io import StringIO
import contextlib
import logging

sys.argv = [""]  # workaround needed for runpy

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

@contextlib.contextmanager
def stderrIO(stderr=None):
    old = sys.stdout
    if stderr is None:
        stderr = StringIO()
    sys.stderr = stderr
    yield stderr
    sys.stderr = old

class Terminal():
    def colorToFloat(self, t):
        nt = ()
        for v in t:
            nt += ((1 / 255) * v,)
        return nt

    def __str__(self):
        return "Terminal for the switch, made by PuffDip"

    def __init__(self):
        logging.basicConfig(filename='terminal.log', format='%(levelname)s:%(message)s', level=logging.ERROR)
        # (r, g, b)
        self.KEY_COLOR = self.colorToFloat((230, 126, 34))
        self.KEY_FUNC_COLOR = self.colorToFloat((196, 107, 29))

        self.TILED_DOUBLE = 1

        self.renderer = NXRenderer()
        self.currentDir = os.getcwd()

        self.CONSOLE_TEXT = "Python {} on Nintendo Switch".format(sys.version)
        self.version_number = '0.1'
        self.keyboard_toggled = False
        self.setting_toggle = False
        self.user_input = [self.CONSOLE_TEXT]
        self.CAPS = False
        self.SYS = False
        self.TAB = False
        self.command = '\n>>>'

        self.keyboard = [
            ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='],
            ['TAB', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']'],
            ['SYS', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'', '\\'],
            ['SHIFT', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/']
        ]

        self.sys_keyboard = [
            ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+'],
            ['TAB', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '{', '}'],
            ['SYS', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ':', '"', '|'],
            ['SHIFT', 'z', 'x', 'c', 'v', 'b', 'n', 'm', '<', '>', '?']
        ]

    def run_code(self, code):
        code = code.replace('>>>', '')
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        redirected_output = sys.stdout = StringIO()
        redirected_error = sys.stderr = StringIO()

        ns_globals = {}
        ns_locals = {}
        out, err, exc = None, None, None

        try:
            exec(code, ns_globals, ns_locals)
        except:
            import traceback
            exc = traceback.format_exc()

        out = redirected_output.getvalue()
        err = redirected_error.getvalue()

        # reset outputs to the original values
        sys.stdout = old_stdout
        sys.stderr = old_stderr

        return out, err, exc

    def run_python_module(self, path: str):
        # clear both buffers
        imguihelper.clear()
        imguihelper.clear()
        _nx.gfx_set_mode(self.TILED_DOUBLE)
        clear_terminal()
        runpy.run_path(path, run_name='__main__')
        # _nx.gfx_set_mode(LINEAR_DOUBLE)
        imguihelper.initialize()

    def shift_key(self):
        if self.CAPS:
            self.CAPS = False
        else:
            self.CAPS = True

    def sys_key(self):
        if self.SYS:
            self.SYS = False
        else:
            self.SYS = True

    def settings(self):
        if self.setting_toggle:
            self.setting_toggle = False
        else:
            self.setting_toggle = True

    def keyboard_key(self, key:str, same_line=False, *, default:str=None, color=None):
        if same_line:
            imgui.same_line()

        if self.CAPS:
            key = key.upper()

        if color is None:
            color = self.KEY_COLOR

        imgui.push_style_color(imgui.COLOR_BUTTON, *color)
        if imgui.button(key, width=80, height=60):
            if default is None:
                if self.command == '':
                    self.command = key
                else:
                    self.command = self.command + key
            elif default == 'SHIFT':
                self.shift_key()
            elif default == 'SYS':
                self.sys_key()
            elif default == 'TAB':
                if self.TAB == False:
                    self.command = self.command.replace('>>>', '>>>\n')
                    self.TAB = True
                self.command = self.command + '    '
        imgui.pop_style_color(1)

    def main(self):
        while True:
            self.renderer.handleinputs()
            imgui.new_frame()

            self.width, self.height = self.renderer.io.display_size
            imgui.set_next_window_size(self.width, self.height)
            imgui.set_next_window_position(0, 0)
            # Header
            imgui.begin("",
                        flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_SAVED_SETTINGS
                        )

            imgui.text("PyNx Terminal By PuffDip" + " - V" + str(self.version_number))

            # Body
            if self.keyboard_toggled or self.setting_toggle:
                imgui.begin_child("region", -5, -430, border=True)
            else:
                imgui.begin_child("region", -5, -110, border=True)
            imgui.text("\n\n".join(self.user_input) + self.command)
            imgui.end_child()

            imgui.begin_group()
            if not self.setting_toggle:
                # Keyboard
                try:
                    if self.keyboard_toggled:
                        if self.SYS:
                            keyboard = self.sys_keyboard
                        else:
                            keyboard = self.keyboard

                        for rows in keyboard:
                            for row in rows:
                                if row == 'TAB' or row == 'SYS' or row == 'SHIFT':
                                    self.keyboard_key(row, False, default=row, color=self.KEY_FUNC_COLOR)
                                elif row == '`' or row == '~':
                                    self.keyboard_key(row, False)
                                else:
                                    self.keyboard_key(row, True)

                        imgui.same_line()

                        imgui.push_style_color(imgui.COLOR_BUTTON, *self.KEY_FUNC_COLOR)
                        if imgui.button("ENTER", width=175, height=60):
                            self.command = self.command + "\n"
                        imgui.pop_style_color(1)

                        imgui.push_style_color(imgui.COLOR_BUTTON, *self.KEY_FUNC_COLOR)
                        if imgui.button("SPACE", width=970, height=50):
                            self.command = self.command + " "
                        imgui.pop_style_color(1)

                        imgui.same_line()

                        imgui.push_style_color(imgui.COLOR_BUTTON, *self.KEY_FUNC_COLOR)
                        if imgui.button("CLEAR", width=80, height=50):
                            self.command = '\n>>>'
                        imgui.pop_style_color(1)

                        imgui.same_line()

                        imgui.push_style_color(imgui.COLOR_BUTTON, *self.KEY_FUNC_COLOR)
                        if imgui.button("BACKSPACE", width=150, height=50):
                            self.command = self.command[:-1]
                        imgui.pop_style_color(1)

                except Exception as e:
                    logging.error(e)
                    self.CONSOLE_TEXT = str(e)
                    self.user_input.append(self.CONSOLE_TEXT)
            else:
                # Settings
                try:
                    imgui.push_style_color(imgui.COLOR_BUTTON, *self.KEY_FUNC_COLOR)
                    if imgui.button("File System", width=150, height=50):
                        self.run_python_module('main.py')
                    imgui.pop_style_color(1)
                except Exception as e:
                    logging.error(e)
                    self.CONSOLE_TEXT = str(e)
                    self.user_input.append(self.CONSOLE_TEXT)

            imgui.end_group()

            # Command line
            imgui.text("Keyboard: {} | Shift: {} | SYS: {}".format(self.keyboard_toggled, self.CAPS, self.SYS))

            imgui.begin_child(
                "Input", height=70, width=-500, border=True,
                flags=imgui.WINDOW_ALWAYS_VERTICAL_SCROLLBAR
            )
            command = self.command
            imgui.text(command)
            imgui.end_child()

            # Buttons
            imgui.same_line()

            imgui.push_style_color(imgui.COLOR_BUTTON, *self.KEY_COLOR)
            if imgui.button("Keyboard", width=200, height=60):
                if self.keyboard_toggled:
                    self.keyboard_toggled = False
                else:
                    self.keyboard_toggled = True
                    if self.setting_toggle:
                        self.setting_toggle = False
            imgui.pop_style_color(1)

            imgui.same_line()

            imgui.push_style_color(imgui.COLOR_BUTTON, *self.KEY_COLOR)
            if imgui.button("Confirm", width=200, height=60):
                if self.TAB:
                    self.TAB = False

                out, err, exc = self.run_code(command)

                if out:
                    self.CONSOLE_TEXT = out
                if err:
                    self.CONSOLE_TEXT = err
                if exc:
                    self.CONSOLE_TEXT = exc

                self.user_input.append(command)
                self.user_input.append(self.CONSOLE_TEXT)
                self.command = '\n>>>'
            imgui.pop_style_color(1)

            imgui.same_line()

            imgui.push_style_color(imgui.COLOR_BUTTON, *self.KEY_FUNC_COLOR)
            if imgui.button("S", width=40, height=40):
                self.settings()
            imgui.pop_style_color(1)

            imgui.end()
            imgui.render()
            self.renderer.render()

        self.renderer.shutdown()
