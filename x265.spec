%global commit 1d3b6e448e01
%global x265lib 79

Summary: H.265/HEVC encoder
Name: x265
Version: 1.9
Release: 1%{?dist}
URL: http://x265.org/
Source0: https://bitbucket.org/multicoreware/x265/get/%{version}.tar.bz2
# source/Lib/TLibCommon - BSD
# source/Lib/TLibEncoder - BSD
# everything else - GPLv2+
License: GPLv2+ and BSD
Group: System Environment/Libraries
BuildRequires: cmake
BuildRequires: yasm >= 1.2.0
Requires: x265-libs = %{version}

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

%description
The primary objective of x265 is to become the best H.265/HEVC encoder
available anywhere, offering the highest compression efficiency and the
highest performance on a wide variety of hardware platforms.

This package contains the command line encoder.

%package libs
Summary: H.265/HEVC encoder library
Group: Development/Libraries
Obsoletes: libx265_%{x265lib}, x265-libs_68, x265-libs_59

%description libs
The primary objective of x265 is to become the best H.265/HEVC encoder
available anywhere, offering the highest compression efficiency and the
highest performance on a wide variety of hardware platforms.

This package contains the shared library.

%package devel
Summary: H.265/HEVC encoder library development files
Group: Development/Libraries
Requires: %{name}-libs = %{version}-%{release}

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

%post devel -p /sbin/ldconfig

%postun devel -p /sbin/ldconfig

%files
%{_bindir}/x265

%files libs
%dir %{_pkgdocdir}
%{_pkgdocdir}/COPYING
%{_libdir}/libx265.so.*

%files devel
%doc doc/*
%{_includedir}/x265.h
%{_includedir}/x265_config.h
%{_libdir}/libx265.so
%{_libdir}/pkgconfig/x265.pc

%changelog
* Fri Jan 29 2016 Fredrik Fornstad <fredrik.fornstad@gmail.com> 1.9-1
- New upstream release and new lib naming after discussion with ClearOS team

* Fri Oct 9 2015 Fredrik Fornstad <fredrik.fornstad@gmail.com> 1.8-1
- New upstream release

* Sat Jun 13 2015 Fredrik Fornstad <fredrik.fornstad@gmail.com> 1.7-2
- Removed ATrpms style and dependencies to comply with ClearOS policy

* Tue May 19 2015 Fredrik Fornstad <fredrik.fornstad@gmail.com> 1.7-1
- New upstream release

* Wed May 6 2015 Fredrik Fornstad <fredrik.fornstad@gmail.com> 1.6-4
- Added buildrequirement atrpms-rpm-config

* Sun Apr 26 2015 Fredrik Fornstad <fredrik.fornstad@gmail.com> 1.6-3
- Adjusted spec file to build rpm in ATrpms style

* Sat Apr 18 2015 Fredrik Fornstad <fredrik.fornstad@gmail.com> 1.6-2
- Defined pkgconfig to enable builds when pkgconfig has not been declared (ClearOS 7 Beta1) without errors

* Mon Apr 6 2015 Fredrik Fornstad <fredrik.fornstad@gmail.com> 1.6-1
- New upstream release
- Specified required yasm version for build

* Mon Apr 6 2015 Fredrik Fornstad <fredrik.fornstad@gmail.com> 1.5-2
- Changed build so that libx265.so will be a protocol version specific rpm so that an update of x265 will not break old dependencies

* Sat Feb 14 2015 Fredrik Fornstad <fredrik.fornstad@gmail.com> 1.5-1
- Initial build for ClearOS
- Spec file based on RPMFusion spec file 1.2-6 for Fedora 21
