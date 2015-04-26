%global commit cbeb7d8a4880
%lib_package x265 51

Summary: H.265/HEVC encoder
Name: x265
Version: 1.6
Release: 3%{?dist}
URL: http://x265.org/
Source0: https://bitbucket.org/multicoreware/x265/get/%{version}.tar.bz2
# source/Lib/TLibCommon - BSD
# source/Lib/TLibEncoder - BSD
# everything else - GPLv2+
License: GPLv2+ and BSD
BuildRequires: cmake
BuildRequires: yasm >= 1.2.0
%lib_dependencies

%description
The primary objective of x265 is to become the best H.265/HEVC encoder
available anywhere, offering the highest compression efficiency and the
highest performance on a wide variety of hardware platforms.

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

%files
%{_bindir}/x265
%doc doc/*
%{_pkgdocdir}/COPYING


%changelog
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
