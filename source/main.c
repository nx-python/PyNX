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

	/* Calculate absolute home dir */
	char cwd[PATH_MAX];
	getcwd(cwd, sizeof(cwd));
	/* Strip the leading sdmc: to workaround a bug somewhere... */
	char *stripped_cwd = strchr(cwd, '/');
	if (stripped_cwd == NULL) stripped_cwd = cwd;

	Py_SetPythonHome(Py_DecodeLocale(stripped_cwd, NULL));

	Py_Initialize();

	/* Print some info */
	printf("Python %s on %s\n", Py_GetVersion(), Py_GetPlatform());
	
	/* set up import path */
	PyObject *sysPath = PySys_GetObject("path");
	PyObject *path = PyUnicode_FromString("");
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

		if (kDown & KEY_PLUS) break; // break in order to return to hbmenu

		gfxFlushBuffers();
		gfxSwapBuffers();
		gfxWaitForVsync();
	}

	socketExit();
	gfxExit();

	return 0;
}
