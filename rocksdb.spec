Summary:	RocksDB: A Persistent Key-Value Store for Flash and RAM Storage
Summary(pl.UTF-8):	RocksDB - trwała baza danych klucz-wartość dla pamięci Flash i RAM
Name:		rocksdb
Version:	3.9
Release:	1
License:	BSD
Group:		Libraries
Source0:	https://github.com/facebook/rocksdb/archive/%{name}-%{version}.tar.gz
# Source0-md5:	395a614e0e9ef67b40714d819379f4c0
Patch0:		%{name}-libdir.patch
URL:		http://rocksdb.org/
BuildRequires:	bzip2-devel
BuildRequires:	gflags-devel
%ifarch i386 i486
BuildRequires:	libatomic-devel
%endif
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libtcmalloc-devel
BuildRequires:	lz4-devel
BuildRequires:	snappy-devel
BuildRequires:	zlib-devel
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
%setup -q -n %{name}-%{name}-%{version}
%patch0 -p1

%build
%ifarch i386 i486
PLATFORM_LDFLAGS="-latomic" \
%endif
%{__make} all shared_lib \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	OPT="%{rpmcflags} %{!?debug:-DNDEBUG}" \
	WARNING_FLAGS="%{rpmcppflags} -Wall"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL_PATH=$RPM_BUILD_ROOT%{_prefix} \
	INSTALL_LIBDIR=$RPM_BUILD_ROOT%{_libdir} \

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc HISTORY.md LICENSE PATENTS README.md ROCKSDB_LITE.md
%attr(755,root,root) %{_libdir}/librocksdb.so

%files devel
%defattr(644,root,root,755)
%doc doc/*
%{_includedir}/rocksdb

%files static
%defattr(644,root,root,755)
%{_libdir}/librocksdb.a
