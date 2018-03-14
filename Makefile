#---------------------------------------------------------------------------------
.SUFFIXES:
#---------------------------------------------------------------------------------

ifeq ($(strip $(DEVKITPRO)),)
$(error "Please set DEVKITPRO in your environment. export DEVKITPRO=<path to>/devkitpro")
endif

TOPDIR ?= $(CURDIR)
include $(DEVKITPRO)/libnx/switch_rules


#---------------------------------------------------------------------------------
# options for code generation
#---------------------------------------------------------------------------------
ARCH	:=	-march=armv8-a -mtune=cortex-a57 -mtp=soft -fPIE

CFLAGS	:=	-g -Wall -O2 -ffunction-sections \
			$(ARCH) $(DEFINES)

CXXFLAGS	:= $(CFLAGS) -fno-rtti -fno-exceptions -std=gnu++11

ASFLAGS	:=	-g $(ARCH)
LDFLAGS	=	-specs=$(DEVKITPRO)/libnx/switch.specs -g $(ARCH) -Wl,-Map,$(notdir $*.map)

LIBS	:= -lnx

#---------------------------------------------------------------------------------
# list of directories containing libraries, this must be the top level containing
# include and lib
#---------------------------------------------------------------------------------

LIBDIRS	:= $(PORTLIBS) $(LIBNX)
export INCLUDE    :=    $(foreach dir,$(LIBDIRS),-I$(dir)/include) \
            -I$(CURDIR)/$(BUILD)
CFLAGS    +=    $(INCLUDE) -DSWITCH


ifndef PYVERS
	PYVERS := 2.7.12
endif

ANAME  := libpython$(shell echo $(PYVERS) | sed 's/\([0-9]*\.\([0-9]*\)\).*/\1/').a

OUTDIR := nxpy$(PYVERS)

PYDIR  := Python-$(PYVERS)
PYLINK := https://www.python.org/ftp/python/$(PYVERS)/Python-$(PYVERS).tgz
PYFILE := py.tgz

.PHONY: all clean


all: distfPY

distfPY: linkPY
	@[ -d "$(OUTDIR)" ] || mkdir -p $(OUTDIR)
	@[ -d "$(OUTDIR)/include" ] || mkdir -p $(OUTDIR)/include
	@[ -d "$(OUTDIR)/include/nxpy" ] || mkdir -p $(OUTDIR)/include/nxpy
	@[ -d "$(OUTDIR)/lib" ] || mkdir -p $(OUTDIR)/lib
	cp $(ANAME) $(OUTDIR)/lib/
	cp $(PYDIR)/Include/* $(OUTDIR)/include/nxpy
	cp $(PYDIR)/pyconfig.h $(OUTDIR)/include/nxpy/
	cp $(PYDIR)/Lib/socket.py $(PYDIR)/Lib/socket.pyX
	cat $(PYDIR)/Lib/socket.pyX | sed 's/'"'"'getpeername'"'"', //g' >$(PYDIR)/Lib/socket.py
	rm $(PYDIR)/Lib/socket.pyX
	cd $(PYDIR)/Lib && ls *.py -1 | xargs zip ../../$(OUTDIR)/python.zip && find json/ encodings/ -type f | xargs zip ../../$(OUTDIR)/python.zip

	touch distfPY

linkPY: soospatchPY
	cd $(PYDIR) && make LIBRARY="$(ANAME)" LDLIBRARY="$(ANAME)" $(ANAME) && cd .. && cp $(PYDIR)/$(ANAME) . && touch linkPY

soospatchPY: compilePY
	cp $(PYDIR)/pyconfig.h $(PYDIR)/pyconfig.h_old
	cat $(PYDIR)/pyconfig.h_old | sed 's/^\([^#][^#]*#undef PY_FORMAT_LONG_LONG.*\)/\#define PY_FORMAT_LONG_LONG \"ll\" \1/' | sed 's/^\(#define socklen_t int\)/#undef socklen_t/' | sed 's/^\(#define socklen_t int\)/#undef socklen_t/' | sed 's/^\(struct servent {char*s_name;char**s_aliases;int s_port;char*s_proto;};\)/\/\/\1/' | sed 's/^\(struct protoent{char*p_name;char**p_aliases;int p_proto;};\)/\/\/\1/'  | sed 's/^\([^#][^#]*#undef HAVE_FSTATVFS.*\)/\#undef HAVE_FSTATVFS \1/' | sed 's/#define HAVE_\(LSTAT\|POLL\|UNAME\|WAIT3\|WAIT4\|WAITPID\|ALARM\|DLFCN_H\|DLOPEN\|DYNAMIC_LOADING\|GETC_UNLOCKED\|GETENTROPY\|GETITIMER\|GETPWENT\|MMAP\|OPENPTY\|PAUSE\|READLINK\|SETITIMER\|SIGACTION\|SIGINTERRUPT\|TERMIOS_H\|EXECV\|FORK\|GETEGID\|GETEUID\|GETGID\|GETPPID\|GETUID\|KILL\|PIPE\|POPEN\|SYSTEM\|TTYNAME\|SYMLINK\|UTIME_H\|FDATASYNC\|TZNAME\|DECL_TZNAME\|WORKING_TZSET\).*/#undef HAVE_\1/g' | sed 's/^#define HAVE_\(STATVFS\|SYS_STATVFS_H\|FDATASYNC\|SYMLINK\|EXECV\|FORK\|GETEGID\|GETEUID\|GETGID\|GETPPID\|GETUID\|KILL\|PIPE\|POPEN\|SYSTEM\|TTYNAME\|SYMLINK\|UTIME_H\|FDATASYNC\|TZNAME\|DECL_TZNAME\|WORKING_TZSET\).*/#undef HAVE_\1/' | sed 's/^\([^#][^#]*#undef HAVE_SELECT.*\)/\#define HAVE_SELECT \1/' | sed 's/^\([^#][^#]*#undef HAVE_GETADDRINFO.*\)/struct servent {char*s_name;char**s_aliases;int s_port;char*s_proto;};\nstruct protoent{char*p_name;char**p_aliases;int p_proto;};\n#define SOCK_RAW 3\n#define SOCK_SEQPACKET 5\n#define IN_CLASSA_NSHIFT 24 \1/g' >$(PYDIR)/pyconfig.h
	cp $(PYDIR)/Modules/posixmodule.c $(PYDIR)/Modules/posixmodule.c_old
	cat $(PYDIR)/Modules/posixmodule.c_old | sed 's/\(^[^rt]*time_t atime, mtime;.*\)/return NULL; \1/' | sed 's/\(^[^ri]*i = (int)umask(i);.*\)/return NULL; \1/' | sed 's/^\([^#][^#]*#undef HAVE_FSTATVFS.*\)/\#undef HAVE_FSTATVFS \1/' | sed 's/#define HAVE_\(EXECV\|FORK\|GETEGID\|GETEUID\|GETGID\|GETPPID\|GETUID\|KILL\|PIPE\|POPEN\|SYSTEM\|TTYNAME\|SYMLINK\|UTIME_H\|FDATASYNC\).*/#undef HAVE_\1/g' | sed 's/^#define HAVE_\(STATVFS\|SYS_STATVFS_H\|FDATASYNC\|FTIME\|SYMLINK\|EXECV\|FORK\|GETEGID\|GETEUID\|GETGID\|GETPPID\|GETUID\|KILL\|PIPE\|POPEN\|SYSTEM\|TTYNAME\|SYMLINK\|UTIME_H\|FDATASYNC\).*/#undef HAVE_\1/' >$(PYDIR)/Modules/posixmodule.c
	cp $(PYDIR)/Modules/socketmodule.c $(PYDIR)/Modules/socketmodule.c_old
	cat $(PYDIR)/Modules/socketmodule.c_old | sed 's/                             sizeof(addr->sa_data)/                             28/g' >$(PYDIR)/Modules/socketmodule.c
	#cp $(PYDIR)/Objects/exceptions.c $(PYDIR)/Objects/exceptions.c_old
	#cat $(PYDIR)/Objects/exceptions.c_old | sed 's/ESHUTDOWN/110/g' >$(PYDIR)/Objects/exceptions.c
	#cp $(PYDIR)/Python/pytime.c $(PYDIR)/Python/pytime.c_old
	#cat $(PYDIR)/Python/pytime.c_old | sed 's/CLOCK_MONOTONIC/(clockid_t)4/g' >$(PYDIR)/Python/pytime.c
	cp $(PYDIR)/Makefile $(PYDIR)/Makefile_old
	cat $(PYDIR)/Makefile_old | sed 's/^\(Python\/\$(DYNLOADFILE) \\\)/#Python\/\$(DYNLOADFILE) \\/' >$(PYDIR)/Makefile
	touch soospatchPY

compilePY: extractedPY patchPY
	cd $(PYDIR) && ./configure CC="$(CC)" CXX="$(CXX)" AS="$(AS)" AR="$(AR)" OBJCOPY="$(OBJCOPY)" STRIP="$(STRIP)" NM="$(NM)" RANLIB="$(RANLIB)" CFLAGS="$(CFLAGS)" CXXFLAGS="$(CXXFLAGS)" ASFLAGS="$(ASFLAGS)" LDFLAGS="$(LDFLAGS)" CONFIG_SITE="config.site" --disable-shared --without-threads --without-doc-strings --disable-ipv6 --host=aarch64-none-elf --build=`./config.guess` && cd .. && touch compilePY

patchPY:
	cp $(PYDIR)/configure $(PYDIR)/configure_old
	cat $(PYDIR)/configure_old | sed 's/	\*\-\*\-linux\*)/	\*\-\*\-linux\*\|aarch64\-none\-elf)/g' >$(PYDIR)/configure
	echo ac_cv_file__dev_ptmx=no >$(PYDIR)/config.site
	echo ac_cv_file__dev_ptc=no >>$(PYDIR)/config.site
	echo ac_cv_lib_dl_dlopen=no >>$(PYDIR)/config.site
	cp $(PYDIR)/Modules/Setup.dist $(PYDIR)/Modules/Setup.dist_old
	cat $(PYDIR)/Modules/Setup.dist_old | sed 's/^\([^#].* pwdmodule\.c.*\)/#\1/' | sed 's/^#\(array\|cmath\|math\|_struct\|operator\|_random\|_collections\|itertools\|strop\|unicodedata\|_io\|_csv\|_md5\|_sha\|_sha256\|_sha512\|binascii\|zlib\|select\|cStringIO\|time\|_functools\|_socket\|datetime\|_bisect\)\(.*\)/\1\2/' | sed "s#\\(zlib[^\$$]*\\)\$$(prefix)\\([^\$$]*\\)\$$(exec_prefix)\\(.*\\)#\1$(DEVKITPRO)/portlibs/armv8-a\2$(DEVKITPRO)/portlibs/armv8-a\3#" >$(PYDIR)/Modules/Setup.dist
	
	touch patchPY

extractedPY: $(PYFILE)
	tar xfzv $(PYFILE) && touch extractedPY

$(PYFILE): 
	wget -O "$(PYFILE)" "$(PYLINK)" || curl -Lo "$(PYFILE)" "$(PYLINK)"

clean:
	@rm -rf $(PYDIR) $(PYFILE) patchPY extractedPY compilePY linkPY distfPY soospatchPY libpython*.a


#---------------------------------------------------------------------------------
# TARGET is the name of the output
# BUILD is the directory where object files & intermediate files will be placed
# SOURCES is a list of directories containing source code
# DATA is a list of directories containing data files
# INCLUDES is a list of directories containing header files
# EXEFS_SRC is the optional input directory containing data copied into exefs, if anything this normally should only contain "main.npdm".
#
# NO_ICON: if set to anything, do not use icon.
# NO_NACP: if set to anything, no .nacp file is generated.
# APP_TITLE is the name of the app stored in the .nacp file (Optional)
# APP_AUTHOR is the author of the app stored in the .nacp file (Optional)
# APP_VERSION is the version of the app stored in the .nacp file (Optional)
# APP_TITLEID is the titleID of the app stored in the .nacp file (Optional)
# ICON is the filename of the icon (.jpg), relative to the project folder.
#   If not set, it attempts to use one of the following (in this order):
#     - <Project name>.jpg
#     - icon.jpg
#     - <libnx folder>/default_icon.jpg
#---------------------------------------------------------------------------------
TARGET		:=	$(notdir $(CURDIR))
BUILD		:=	build
SOURCES		:=	source
DATA		:=	data
INCLUDES	:=	include
EXEFS_SRC	:=	exefs_src
APP_TITLEID	:=	Pynx
APP_AUTHOR	:=	nx-python Authors, Python Software Foundation
APP_VERSION	:=	0.1.0-alpha

#---------------------------------------------------------------------------------
# no real need to edit anything past this point unless you need to add additional
# rules for different file extensions
#---------------------------------------------------------------------------------
ifneq ($(BUILD),$(notdir $(CURDIR)))
#---------------------------------------------------------------------------------

export OUTPUT	:=	$(CURDIR)/$(TARGET)
export TOPDIR	:=	$(CURDIR)

export VPATH	:=	$(foreach dir,$(SOURCES),$(CURDIR)/$(dir)) \
			$(foreach dir,$(DATA),$(CURDIR)/$(dir))

export DEPSDIR	:=	$(CURDIR)/$(BUILD)

CFILES		:=	$(foreach dir,$(SOURCES),$(notdir $(wildcard $(dir)/*.c)))
CPPFILES	:=	$(foreach dir,$(SOURCES),$(notdir $(wildcard $(dir)/*.cpp)))
SFILES		:=	$(foreach dir,$(SOURCES),$(notdir $(wildcard $(dir)/*.s)))
BINFILES	:=	$(foreach dir,$(DATA),$(notdir $(wildcard $(dir)/*.*)))

#---------------------------------------------------------------------------------
# use CXX for linking C++ projects, CC for standard C
#---------------------------------------------------------------------------------
ifeq ($(strip $(CPPFILES)),)
#---------------------------------------------------------------------------------
	export LD	:=	$(CC)
#---------------------------------------------------------------------------------
else
#---------------------------------------------------------------------------------
	export LD	:=	$(CXX)
#---------------------------------------------------------------------------------
endif
#---------------------------------------------------------------------------------

export OFILES	:=	$(addsuffix .o,$(BINFILES)) \
			$(CPPFILES:.cpp=.o) $(CFILES:.c=.o) $(SFILES:.s=.o)

export INCLUDE	:=	$(foreach dir,$(INCLUDES),-I$(CURDIR)/$(dir)) \
			$(foreach dir,$(LIBDIRS),-I$(dir)/include) \
			-I$(CURDIR)/$(BUILD)

export LIBPATHS	:=	$(foreach dir,$(LIBDIRS),-L$(dir)/lib)

export BUILD_EXEFS_SRC := $(TOPDIR)/$(EXEFS_SRC)

ifeq ($(strip $(ICON)),)
	icons := $(wildcard *.jpg)
	ifneq (,$(findstring $(TARGET).jpg,$(icons)))
		export APP_ICON := $(TOPDIR)/$(TARGET).jpg
	else
		ifneq (,$(findstring icon.jpg,$(icons)))
			export APP_ICON := $(TOPDIR)/icon.jpg
		endif
	endif
else
	export APP_ICON := $(TOPDIR)/$(ICON)
endif

ifeq ($(strip $(NO_ICON)),)
	export NROFLAGS += --icon=$(APP_ICON)
endif

ifeq ($(strip $(NO_NACP)),)
	export NROFLAGS += --nacp=$(CURDIR)/$(TARGET).nacp
endif

ifneq ($(APP_TITLEID),)
	export NACPFLAGS += --titleid=$(APP_TITLEID)
endif

.PHONY: $(BUILD) clean all

#---------------------------------------------------------------------------------
all: $(BUILD)

$(BUILD):
	@[ -d $@ ] || mkdir -p $@
	@$(MAKE) --no-print-directory -C $(BUILD) -f $(CURDIR)/Makefile

#---------------------------------------------------------------------------------
clean:
	@echo clean ...
	@rm -fr $(BUILD) $(TARGET).pfs0 $(TARGET).nso $(TARGET).nro $(TARGET).nacp $(TARGET).elf


#---------------------------------------------------------------------------------
else
.PHONY:	all

DEPENDS	:=	$(OFILES:.o=.d)

#---------------------------------------------------------------------------------
# main targets
#---------------------------------------------------------------------------------
all	:	$(OUTPUT).pfs0 $(OUTPUT).nro

$(OUTPUT).pfs0	:	$(OUTPUT).nso

$(OUTPUT).nso	:	$(OUTPUT).elf

ifeq ($(strip $(NO_NACP)),)
$(OUTPUT).nro	:	$(OUTPUT).elf $(OUTPUT).nacp
else
$(OUTPUT).nro	:	$(OUTPUT).elf
endif

$(OUTPUT).elf	:	$(OFILES)

#---------------------------------------------------------------------------------
# you need a rule like this for each extension you use as binary data
#---------------------------------------------------------------------------------
%.bin.o	:	%.bin
#---------------------------------------------------------------------------------
	@echo $(notdir $<)
	@$(bin2o)

-include $(DEPENDS)

#---------------------------------------------------------------------------------------
endif
#---------------------------------------------------------------------------------------
