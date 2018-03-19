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

PYCONFIG_DIR := ../python_config

LIBDIRS	:= $(PORTLIBS) $(LIBNX)
export INCLUDE    :=    $(foreach dir,$(LIBDIRS),-I$(dir)/include) \
            -I$(CURDIR)/$(BUILD)
CFLAGS    +=    $(INCLUDE) -DSWITCH


ifndef PYVERS
	PYVERS := 3.5.3
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
	cd $(PYDIR)/Lib && ls *.py -1 | xargs zip ../../$(OUTDIR)/python.zip && find json/ encodings/ html/ http/ test/ urllib/ collections/ email/ sqlite3/ logging/ xml/ -type f | xargs zip ../../$(OUTDIR)/python.zip

	touch distfPY

linkPY: soospatchPY
	cd $(PYDIR) && make $(MAKEFLAGS) LIBRARY="$(ANAME)" LDLIBRARY="$(ANAME)" $(ANAME) && cd .. && cp $(PYDIR)/$(ANAME) . && touch linkPY

soospatchPY: compilePY
	cp $(PYCONFIG_DIR)/pyconfig.h $(PYDIR)/
	cp $(PYCONFIG_DIR)/intrcheck.c $(PYDIR)/Parser/
	cp $(PYCONFIG_DIR)/pytime.c $(PYDIR)/Python/
	cp $(PYCONFIG_DIR)/random.c $(PYDIR)/Python/
	cp $(PYCONFIG_DIR)/fileutils.c $(PYDIR)/Python/
	cp $(PYCONFIG_DIR)/fileutils.c $(PYDIR)/Modules/
	cp $(PYDIR)/Modules/posixmodule.c $(PYDIR)/Modules/posixmodule.c_old
	cat $(PYDIR)/Modules/posixmodule.c_old | sed 's/return utime(path, time)/errno=ENOENT; return -1/g' | sed 's/define LSTAT lstat/define LSTAT stat/' | sed '1s/^/#include <sys\/socket.h>/' | sed 's/access(path->narrow, mode)/1/' | sed 's/\(^[^rt]*time_t atime, mtime;.*\)/return NULL; \1/' | sed 's/\(^[^ri]*int i = (int)umask(mask);.*\)/int i=0; return NULL;/' | sed 's/^\([^#][^#]*#undef HAVE_FSTATVFS.*\)/\#undef HAVE_FSTATVFS \1/' | sed 's/#define HAVE_\(EXECV\|FORK\|GETEGID\|GETEUID\|GETGID\|GETPPID\|GETUID\|KILL\|PIPE\|POPEN\|SYSTEM\|TTYNAME\|SYMLINK\|UTIME_H\|FDATASYNC\).*/#undef HAVE_\1/g' | sed 's/^#define HAVE_\(STATVFS\|SYS_STATVFS_H\|FDATASYNC\|FTIME\|SYMLINK\|EXECV\|FORK\|GETEGID\|GETEUID\|GETGID\|GETPPID\|GETUID\|KILL\|PIPE\|POPEN\|SYSTEM\|TTYNAME\|SYMLINK\|UTIME_H\|FDATASYNC\).*/#undef HAVE_\1/' >$(PYDIR)/Modules/posixmodule.c
	cp $(PYDIR)/Modules/socketmodule.c $(PYDIR)/Modules/socketmodule.c_old
	cat $(PYDIR)/Modules/socketmodule.c_old | sed 's/send(s->sock_fd, buf, len, flags);/send(s->sock_fd, buf, len<4096?len:4096, flags);/g' | sed 's/                             sizeof(addr->sa_data)/                             28/g' >$(PYDIR)/Modules/socketmodule.c
	cp $(PYDIR)/Objects/exceptions.c $(PYDIR)/Objects/exceptions.c_old
	cat $(PYDIR)/Objects/exceptions.c_old | sed 's/ESHUTDOWN/EPIPE/g' >$(PYDIR)/Objects/exceptions.c
	cp $(PYDIR)/Python/pytime.c $(PYDIR)/Python/pytime.c_old
	cat $(PYDIR)/Python/pytime.c_old | sed 's/CLOCK_MONOTONIC/(clockid_t)4/g' >$(PYDIR)/Python/pytime.c
	cp $(PYDIR)/Makefile $(PYDIR)/Makefile_old
	cat $(PYDIR)/Makefile_old | sed 's/-Werror=declaration-after-statement//' | sed 's/Python\/$$(DYNLOADFILE) \\/\\/' >$(PYDIR)/Makefile
	touch soospatchPY

compilePY: extractedPY patchPY
	cd $(PYDIR) && ./configure CC="$(CC)" CXX="$(CXX)" AS="$(AS)" AR="$(AR)" OBJCOPY="$(OBJCOPY)" STRIP="$(STRIP)" NM="$(NM)" RANLIB="$(RANLIB)" CFLAGS="$(CFLAGS)" CXXFLAGS="$(CXXFLAGS)" ASFLAGS="$(ASFLAGS)" LDFLAGS="$(LDFLAGS)" CONFIG_SITE="config.site" --disable-shared --without-threads --without-doc-strings --without-signal-module --disable-ipv6 --host=aarch64-none-elf --build=`./config.guess` && cd .. && touch compilePY

patchPY:
	cp $(PYDIR)/configure $(PYDIR)/configure_old
	cat $(PYDIR)/configure_old | sed 's/	\*\-\*\-linux\*)/	\*\-\*\-linux\*\|aarch64\-none\-elf)/g' >$(PYDIR)/configure
	echo ac_cv_file__dev_ptmx=no >$(PYDIR)/config.site
	echo ac_cv_file__dev_ptc=no >>$(PYDIR)/config.site
	echo ac_cv_lib_dl_dlopen=no >>$(PYDIR)/config.site
	cp $(PYDIR)/Modules/Setup.dist $(PYDIR)/Modules/Setup.dist_old
	cat $(PYDIR)/Modules/Setup.dist_old | sed 's/^\([^#].* pwdmodule\.c.*\)/#\1/' | sed 's/^#\(array\|cmath\|math\|_struct\|operator\|_random\|_collections\|itertools\|signal\|strop\|unicodedata\|_io\|_csv\|_md5\|_sha\|_sha256\|_sha512\|binascii\|select\|cStringIO\|time\|_functools\|_socket\|datetime\|_bisect\)\(.*\)/\1\2/' | sed "s#\\(zlib[^\$$]*\\)\$$(prefix)\\([^\$$]*\\)\$$(exec_prefix)\\(.*\\)#\1$(DEVKITPRO)/portlibs/switch\2$(DEVKITPRO)/portlibs/switch\3#" >$(PYDIR)/Modules/Setup.dist
	
	touch patchPY

extractedPY: $(PYFILE)
	tar xfzv $(PYFILE) && touch extractedPY

$(PYFILE): 
	wget -O "$(PYFILE)" "$(PYLINK)" || curl -Lo "$(PYFILE)" "$(PYLINK)"

clean:
	@rm -rf $(PYDIR) $(PYFILE) patchPY extractedPY compilePY linkPY distfPY soospatchPY libpython*.a
