# PyNX

**nx-python** is an ecosystem for developing and running Python homebrew applications on the Nintendo Switch. **PyNX** serves as the entry point to running Python apps on your Switch. It is a homebrew app that contains a port of the CPython interpreter and allows you to run Python applications from the Homebrew Menu. Just name your application `main.py` and place it next to the `PyNX.nro`, and it will be executed as soon as you launch PyNX from the Homebrew Menu. Currently, **Python 3.5 is supported**.

## Running PyNX on your Switch

You don't have to compile PyNX, you can [just grab a release build](https://github.com/nx-python/PyNX/releases) and copy the content of the ZIP archive into the `/switch` folder on your SD card. PyNX will appear on the Homebrew Menu.

## Compiling PyNX

Compile PyNX using `make`. This will create a `build` directory and build everything in there. Compiling might take a while, grab a coffee or whatever in the meantime if you like. Afterwards, create a distributable version using `make dist`. It will appear in the `build` directory.

## Documentation

Documentation can be found on [ReadTheDocs](https://nx-python.readthedocs.io/en/latest/).

## Having an issue?

If you encounter a problem, make sure to [join our Discord](https://discord.gg/5Ga2Whf) and tell us about it, or, alternatively, you can use GitHub's [issue tracker](https://github.com/nx-python/PyNX/issues) to report an issue.
