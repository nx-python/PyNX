# Pynx

**nx-python** is an ecosystem for developing and running Python homebrew applications on the Nintendo Switch. **Pynx** serves as the entry point to running Python apps on your Switch. It is a homebrew app that contains a port of the CPython interpreter and allows you to run Python applications from the Homebrew Menu. Just name your application `main.py` and place it next to the `pynx.nro`, and it will be executed as soon as you launch Pynx from the Homebrew Menu. Currently, **only Python 2.7 is supported**.

## Running Pynx on your Switch

You don't have to compile Pynx, you can [just grab a release build](https://github.com/nx-python/Pynx/releases) and copy the content of the ZIP archive into the `/switch` folder on your SD card. Pynx will appear on the Homebrew Menu.

## Compiling Pynx

Compile Pynx using `make`. This will create a `Pynx` directory and build everything in there. Compiling might take a while, grab a coffee or whatever in the meantime if you like. Afterwards, create a distributable version using `make dist`. It will appear in the `build` directory.

## Having an issue?

If you encounter a problem, make sure to [join our Discord](https://discord.gg/5Ga2Whf) and tell us about it, or, alternatively, you can use GitHub's [issue tracker](https://github.com/nx-python/Pynx/issues) to report an issue.
