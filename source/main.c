#include <stdio.h>
#include <switch.h>

#include <nxpy/Python.h>

#define MAINPY "main.py"

int main(int argc, char *argv[])
{
	gfxInitDefault();
	consoleInit(NULL);
	consoleDebugInit(debugDevice_CONSOLE);

	printf("Args:\n");
	for (int i=0; i<argc; i++) {
		printf("%s\n", argv[i]);
	}

	socketInitializeDefault();

	Py_NoSiteFlag = 1;
	Py_IgnoreEnvironmentFlag = 1;
	Py_NoUserSiteDirectory = 1;
	//Py_VerboseFlag += 1;

	Py_SetPythonHome(L"./");

	Py_Initialize();
	
	/* Print some info */
	printf("Python %s on %s\n", Py_GetVersion(), Py_GetPlatform());
	
	/* set up import path */
	PyObject *sysPath = PySys_GetObject("path");
	PyObject *path = PyUnicode_FromString("./");
	PyList_Insert(sysPath, 0, path);

	FILE * mainpy = fopen(MAINPY, "r");

	if (mainpy == NULL) {
		printf("Error: could not open " MAINPY "\n");
	} else {
		/* execute main.py */
		PyRun_AnyFile(mainpy, MAINPY);
	}

	Py_DECREF(path); /* are these decrefs needed? Are they in the right place? */
	Py_DECREF(sysPath);

	Py_Finalize();

	while(appletMainLoop()) {

		hidScanInput();

		u32 kDown = hidKeysDown(CONTROLLER_P1_AUTO);

		/* Can't crash on exit if there's no exit button :P */
		//if (kDown & KEY_PLUS) break; // break in order to return to hbmenu

		gfxFlushBuffers();
		gfxSwapBuffers();
		gfxWaitForVsync();
	}

	socketExit();
	gfxExit();

	return 0;
}
