%global commit 981e3bfef16a
%global x265lib 95

Summary: H.265/HEVC encoder
Name: x265
Version: 2.1
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

%build
%ifnarch i686
mkdir -p 10bit 12bit

cd 12bit
%cmake -G "Unix Makefiles" -DCMAKE_SKIP_RPATH:BOOL=YES -DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=ON -DENABLE_PIC:BOOL=ON \
 -DENABLE_TESTS:BOOL=ON -DHIGH_BIT_DEPTH=ON -DEXPORT_C_API=OFF -DENABLE_SHARED=OFF -DENABLE_CLI=OFF -DMAIN12=ON ../source
make %{?_smp_mflags}

cd ../10bit
%cmake -G "Unix Makefiles" -DCMAKE_SKIP_RPATH:BOOL=YES -DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=ON -DENABLE_PIC:BOOL=ON \
 -DENABLE_TESTS:BOOL=ON -DHIGH_BIT_DEPTH=ON -DEXPORT_C_API=OFF -DENABLE_SHARED=OFF -DENABLE_CLI=OFF ../source
make %{?_smp_mflags}

cd ..
ln -sf 10bit/libx265.a libx265_main10.a
ln -sf 12bit/libx265.a libx265_main12.a
%cmake -G "Unix Makefiles" -DCMAKE_SKIP_RPATH:BOOL=YES -DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=ON -DENABLE_PIC:BOOL=ON -DENABLE_SHARED=ON \
 -DENABLE_TESTS:BOOL=ON -DEXTRA_LIB="x265_main10.a;x265_main12.a" -DEXTRA_LINK_FLAGS=-L. -DLINKED_10BIT=ON -DLINKED_12BIT=ON source
make %{?_smp_mflags}

# rename the 8bit library, then combine all three into libx265.a
mv libx265.a libx265_main.a

# On Linux, we use GNU ar to combine the static libraries together
ar -M <<EOF
CREATE libx265.a
ADDLIB libx265_main.a
ADDLIB libx265_main10.a
ADDLIB libx265_main12.a
SAVE
END
EOF

%else 

%cmake -G "Unix Makefiles" -DCMAKE_SKIP_RPATH:BOOL=YES -DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=ON -DENABLE_PIC:BOOL=ON -DENABLE_SHARED=ON \
 -DENABLE_TESTS:BOOL=ON source
make %{?_smp_mflags}

%endif

%install
make DESTDIR=%{buildroot} install
# We do not want the static lib in ClearOS
rm %{buildroot}%{_libdir}/libx265*.a
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
* Wed Sep 28 2016 Fredrik Fornstad <fredrik.fornstad@gmail.com> 2.1-1
- New upstream release

* Sat Aug 20 2016 Fredrik Fornstad <fredrik.fornstad@gmail.com> 2.0-1
- New upstream release

* Tue Feb 2 2016 Fredrik Fornstad <fredrik.fornstad@gmail.com> 1.9-2
- Building x265 as multilib with 8bit (default), 10bit and 12bit support

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
