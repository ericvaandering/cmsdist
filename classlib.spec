### RPM external classlib 3.1.3
%define online %(case %cmsplatf in (*onl_*_*) echo true;; (*) echo false;; esac)
Source: http://lat.web.cern.ch/lat/exports/%n-%realversion.tar.bz2
Patch0: classlib-3.1.3-gcc46
Patch1: classlib-3.1.3-sl6

Requires: bz2lib 
Requires: pcre 
Requires: xz
%if "%online" != "true"
Requires: openssl
Requires: zlib 
%else
Requires: onlinesystemtools
%endif

%prep
%setup -n %n-%realversion
%patch0 -p1
%patch1 -p1

%build
./configure --prefix=%i                         \
  --with-zlib-includes=$ZLIB_ROOT/include       \
  --with-zlib-libraries=$ZLIB_ROOT/lib          \
  --with-bz2lib-includes=$BZ2LIB_ROOT/include   \
  --with-bz2lib-libraries=$BZ2LIB_ROOT/lib      \
  --with-pcre-includes=$PCRE_ROOT/include       \
  --with-pcre-libraries=$PCRE_ROOT/lib          \
  --with-openssl-includes=$OPENSSL_ROOT/include \
  --with-openssl-libraries=$OPENSSL_ROOT/lib	\
  --with-lzma-includes=$XZ_ROOT/include         \
  --with-lzma-libraries=$XZ_ROOT/lib	

perl -p -i -e '
  s{-llzo2}{}g;
  !/^\S+: / && s{\S+LZO((C|Dec)ompressor|Constants|Error)\S+}{}g' \
 Makefile

make %makeprocesses

%install
make %makeprocesses install
