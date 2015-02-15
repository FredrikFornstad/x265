%global commit 9f0324125f53

Summary: H.265/HEVC encoder
Name: x265
Version: 1.5
Release: 1%{?dist}
URL: http://x265.org/
Source0: https://bitbucket.org/multicoreware/x265/get/%{version}.tar.bz2
# source/Lib/TLibCommon - BSD
# source/Lib/TLibEncoder - BSD
# everything else - GPLv2+
License: GPLv2+ and BSD
BuildRequires: cmake
BuildRequires: yasm

%description
The primary objective of x265 is to become the best H.265/HEVC encoder
available anywhere, offering the highest compression efficiency and the
highest performance on a wide variety of hardware platforms.

This package contains the command line encoder.

%package libs
Summary: H.265/HEVC encoder library

%description libs
The primary objective of x265 is to become the best H.265/HEVC encoder
available anywhere, offering the highest compression efficiency and the
highest performance on a wide variety of hardware platforms.

This package contains the shared library.

%package devel
Summary: H.265/HEVC encoder library development files
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
The primary objective of x265 is to become the best H.265/HEVC encoder
available anywhere, offering the highest compression efficiency and the
highest performance on a wide variety of hardware platforms.

This package contains the shared library development files.

%prep
%setup -q -n multicoreware-%{name}-%{commit}
# tests are crashing on x86 if linked against shared libx265
f=doc/uncrustify/drag-uncrustify.bat
tr -d '\r' < ${f} > ${f}.unix && \
touch -r ${f} ${f}.unix && \
mv ${f}.unix ${f}

%build
%cmake -G "Unix Makefiles" \
 -DCMAKE_SKIP_RPATH:BOOL=YES \
 -DENABLE_TESTS:BOOL=ON \
 source
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
rm %{buildroot}%{_libdir}/libx265.a
install -Dpm644 COPYING %{buildroot}%{_pkgdocdir}/COPYING

%ifnarch %{arm}
%check
LD_LIBRARY_PATH=$(pwd) test/TestBench
%endif

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%{_bindir}/x265

%files libs
%dir %{_pkgdocdir}
%{_pkgdocdir}/COPYING
%{_libdir}/libx265.so.43

%files devel
%doc doc/*
%{_includedir}/x265.h
%{_includedir}/x265_config.h
%{_libdir}/libx265.so
%{_libdir}/pkgconfig/x265.pc

%changelog
* Sat Feb 14 2015 Fredrik Fornstad <fredrik.fornstad@gmail.com> 1.5-1
- Initial build for ClearOS
- Spec file based on RPMFusion spec file 1.2-6 for Fedora 21
