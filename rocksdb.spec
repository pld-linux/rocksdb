# TODO: hdfs/java
#
# Conditional build:
%bcond_with	tests		# build with tests
%bcond_without	static_libs	# don't build static libraries

Summary:	RocksDB: A Persistent Key-Value Store for Flash and RAM Storage
Summary(pl.UTF-8):	RocksDB - trwała baza danych klucz-wartość dla pamięci Flash i RAM
Name:		rocksdb
Version:	4.13.5
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/facebook/rocksdb/releases
Source0:	https://github.com/facebook/rocksdb/archive/%{name}-%{version}.tar.gz
# Source0-md5:	f94191cf37221c4541dfb4d7f544651e
Patch0:		%{name}-libdir.patch
Patch1:		make-programs.patch
Patch2:		%{name}-jemalloc.patch
Patch3:		%{name}-detect-flags.patch
URL:		http://rocksdb.org/
BuildRequires:	bzip2-devel
BuildRequires:	gflags-devel
# libtcmalloc also supported, but jemalloc is preferred
BuildRequires:	jemalloc-devel
%ifarch i386 i486
BuildRequires:	libatomic-devel
%endif
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	lz4-devel >= 1:1.7
BuildRequires:	numactl-devel
BuildRequires:	snappy-devel
BuildRequires:	zlib-devel
BuildRequires:	zstd-devel >= 0.8.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# std::__once_call, std::__once_callable non-function symbols
%define		skip_post_check_so	librocksdb.so.*

%description
RocksDB is a Persistent Key-Value Store for Flash and RAM Storage.

%description -l pl.UTF-8
RocksDB to trwała baza danych klucz-wartość dla pamięci Flash i RAM.

%package devel
Summary:	Header files for RocksDB library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki RocksDB
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel >= 6:4.7

%description devel
Header files for RocksDB library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki RocksDB.

%package static
Summary:	Static RocksDB library
Summary(pl.UTF-8):	Statyczna biblioteka RocksDB
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static RocksDB library.

%description static -l pl.UTF-8
Statyczna biblioteka RocksDB.

%prep
%setup -q -n %{name}-%{name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%ifarch i386 i486
PLATFORM_LDFLAGS="-latomic" \
%endif
%{__make} shared_lib %{?with_static_libs:static_lib} programs %{?with_tests:check} \
	AM_DEFAULT_VERBOSITY=1 \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	EXTRA_CFLAGS="$(pkg-config --cflags liblz4)" \
	OPT="%{rpmcflags} %{!?debug:-DNDEBUG}" \
	PORTABLE=1 \
	%{!?with_debug:DEBUG_LEVEL=0}
	WARNING_FLAGS="%{rpmcppflags} -Wall"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	%{!?with_debug:DEBUG_LEVEL=0} \
	INSTALL_PATH=$RPM_BUILD_ROOT%{_prefix} \
	INSTALL_LIBDIR=$RPM_BUILD_ROOT%{_libdir}

# reduntant symlink
%{__rm} $RPM_BUILD_ROOT%{_libdir}/librocksdb.so.4

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS DEFAULT_OPTIONS_HISTORY.md DUMP_FORMAT.md HISTORY.md LANGUAGE-BINDINGS.md LICENSE PATENTS README.md ROCKSDB_LITE.md USERS.md
%attr(755,root,root) %{_libdir}/librocksdb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librocksdb.so.4.13

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librocksdb.so
%{_includedir}/rocksdb

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/librocksdb.a
%endif
