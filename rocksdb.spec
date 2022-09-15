# TODO: hdfs/java
#
# Conditional build:
%bcond_with	tests		# build with tests
%bcond_with	benchmark	# enable Google Benchmark
%bcond_without	static_libs	# don't build static libraries
%bcond_without	tbb		# Threading Building Blocks support

Summary:	RocksDB: A Persistent Key-Value Store for Flash and RAM Storage
Summary(pl.UTF-8):	RocksDB - trwała baza danych klucz-wartość dla pamięci Flash i RAM
Name:		rocksdb
Version:	6.29.5
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/facebook/rocksdb/releases
Source0:	https://github.com/facebook/rocksdb/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	be498cd7125f2a38059609469adf147f
Patch0:		%{name}-detect-flags.patch
Patch1:		%{name}-pc.patch
URL:		https://rocksdb.org/
BuildRequires:	bzip2-devel >= 1.0.8
BuildRequires:	gflags-devel
%{?with_benchmark:BuildRequires:	google-benchmark-devel}
# libtcmalloc also supported, but jemalloc is preferred
BuildRequires:	jemalloc-devel
%ifarch i386 i486
BuildRequires:	libatomic-devel
%endif
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	liburing-devel
BuildRequires:	lz4-devel >= 1:1.9.2
BuildRequires:	numactl-devel
BuildRequires:	rpmbuild(macros) >= 1.734
BuildRequires:	snappy-devel >= 1.1.8
%{?with_tbb:BuildRequires:	tbb-devel}
BuildRequires:	zlib-devel >= 1.2.11
BuildRequires:	zstd-devel >= 1.4.4
Requires:	bzip2 >= 1.0.8
Requires:	lz4 >= 1:1.9.2
Requires:	snappy >= 1.1.8
Requires:	zlib >= 1.2.11
Requires:	zstd >= 1.4.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
%setup -q
%patch0 -p1
%patch1 -p1

%build
%if %{without benchmark}
export ROCKSDB_DISABLE_BENCHMARK=1
%endif
%if %{without tbb}
export ROCKSDB_DISABLE_TBB=1
%endif

%ifarch i386 i486
PLATFORM_LDFLAGS="-latomic" \
%endif
%{__make} shared_lib %{?with_static_libs:static_lib} tools tools_lib %{?with_tests:check} \
	AM_DEFAULT_VERBOSITY=1 \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	%{!?with_debug:DEBUG_LEVEL=0} \
	EXTRA_CFLAGS="$(pkg-config --cflags liblz4)" \
	OPT="%{rpmcflags} %{!?debug:-DNDEBUG}" \
	PORTABLE=1 \
	USE_RTTI=1 \
	WARNING_FLAGS="%{rpmcppflags} -Wall"

%install
rm -rf $RPM_BUILD_ROOT

%if %{without benchmark}
export ROCKSDB_DISABLE_BENCHMARK=1
%endif
%if %{without tbb}
export ROCKSDB_DISABLE_TBB=1
%endif

ls -la

%{__make} install \
	%{!?with_debug:DEBUG_LEVEL=0} \
	PORTABLE=1 \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir}

ls -la

# reduntant symlink
%{__rm} $RPM_BUILD_ROOT%{_libdir}/librocksdb.so.6

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS DEFAULT_OPTIONS_HISTORY.md DUMP_FORMAT.md HISTORY.md LANGUAGE-BINDINGS.md LICENSE.leveldb README.md ROCKSDB_LITE.md USERS.md
%attr(755,root,root) %{_libdir}/librocksdb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librocksdb.so.6.29

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librocksdb.so
%{_includedir}/rocksdb
%{_pkgconfigdir}/rocksdb.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/librocksdb.a
%endif
