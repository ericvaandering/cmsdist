### RPM external xrootd 3.1.0
## INITENV +PATH LD_LIBRARY_PATH %i/lib64
%define online %(case %cmsplatf in (*onl_*_*) echo true;; (*) echo false;; esac)

Source: http://xrootd.cern.ch/cgi-bin/cgit.cgi/xrootd/snapshot/%n-%{realversion}.tar.gz
Patch0: xrootd-gcc44
Patch1: xrootd-5.30.00-fix-gcc46
Patch2: xrootd-3.1.0-fix-read-after-read
Patch3: xrootd-3.1.0-fixed-library-location-all-os
Patch4: xrootd-3.1.0-client-send-moninfo

%if "%online" != "true"
Requires: openssl zlib
%else
Requires: onlinesystemtools
%endif
Requires: cmake gcc

%prep 
%setup -n %n-%{realversion}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p0
%patch4 -p1

# need to fix these from xrootd git
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' src/XrdMon/cleanup.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' src/XrdMon/loadRTDataToMySQL.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' src/XrdMon/xrdmonCollector.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' src/XrdMon/prepareMySQLStats.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' src/XrdMon/xrdmonCreateMySQL.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' src/XrdMon/xrdmonLoadMySQL.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' src/XrdMon/xrdmonPrepareStats.pl

%build
mkdir build
cd build

SOLIB_EXT=so
if [[ %cmsplatf == osx* ]]; then
  SOLIB_EXT=dylib
fi

# By default xrootd has perl, fuse, krb5, readline, and crypto enabled.
# libfuse and libperl are not produced by CMSDIST.
cmake ../ \
  -DCMAKE_INSTALL_PREFIX=%i \
  -DOPENSSL_ROOT_DIR=${OPENSSL_ROOT} \
  -DZLIB_INCLUDE_DIR:PATH=${ZLIB_ROOT}/include \
  -DZLIB_LIBRARY:FILEPATH=${ZLIB_ROOT}/lib/libz.${SOLIB_EXT} \
  -DENABLE_PERL=FALSE \
  -DENABLE_FUSE=FALSE \
  -DENABLE_KRB5=TRUE \
  -DENABLE_READLINE=TRUE \
  -DENABLE_CRYPTO=TRUE

# Use makeprocess macro, it uses compiling_processes defined by
# build configuration file or build argument
make %makeprocesses VERBOSE=1

%install
cd build
make install
cd ..

%define strip_files %i/lib
%define keep_archives true

