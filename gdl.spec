%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           gdl
Version:        0.9
Release:        0.9.rc3%{?dist}
Summary:        GNU Data Language

Group:          Applications/Engineering
License:        GPLv2+
URL:            http://gnudatalanguage.sourceforge.net/
Source0:        http://downloads.sourceforge.net/gnudatalanguage/%{name}-%{version}rc3.tar.gz
# Made with makecvstarball
#Source0:        http://downloads.sourceforge.net/gnudatalanguage/%{name}-%{version}rc2-20090603.tar.bz2
Source1:        gdl.csh
Source2:        gdl.sh
Source3:        makecvstarball
# Build with system antlr library.  Request for upstream change here:
# https://sourceforge.net/tracker/index.php?func=detail&aid=2685215&group_id=97659&atid=618686
Patch3:         gdl-0.9rc3-antlr.patch
Patch4:         gdl-0.9rc2-20090504-antlr-auto.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#RHEL doesn't have the needed antlr version/headers, old plplot
%if !0%{?rhel}
BuildRequires:  antlr
%define plplot_config %{nil}
%else
%define plplot_config --enable-oldplplot
%endif
BuildRequires:  readline-devel, ncurses-devel
BuildRequires:  gsl-devel, plplot-devel, ImageMagick-c++-devel
BuildRequires:  netcdf-devel, hdf5-devel, libjpeg-devel
BuildRequires:  python-devel, python-numarray, python-matplotlib
BuildRequires:  fftw-devel, hdf-static, hdf-devel, proj-devel
BuildRequires:  autoconf, automake, libtool
# Needed to pull in drivers
Requires:       plplot
Requires:       %{name}-common = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}


%description
A free IDL (Interactive Data Language) compatible incremental compiler
(ie. runs IDL programs). IDL is a registered trademark of Research
Systems Inc.


%package        common
Summary:        Common files for GDL
Group:          Applications/Engineering
Requires:       %{name}-runtime = %{version}-%{release}
%if !0%{?rhel}
BuildArch:      noarch
%endif

%description    common
Common files for GDL


%prep
%setup -q -n %{name}-%{version}rc3
%if !0%{?rhel}
%patch3 -p1 -b .antlr
%patch4 -p1 -b .antlr-auto
%endif
%if !0%{?rhel}
rm -rf src/antlr
%endif
rm ltmain.sh
autoreconf --install


%build
export CPPFLAGS="-DH5_USE_16_API"
%configure --disable-dependency-tracking --disable-static --with-fftw \
           %{plplot_config} \
           INCLUDES="-I/usr/include/netcdf -I/usr/include/hdf" \
           LIBS="-L%{_libdir}/hdf"
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -r $RPM_BUILD_ROOT%{_libdir}

# Install the library
install -d -m 0755 $RPM_BUILD_ROOT/%{_datadir}
cp -r src/pro $RPM_BUILD_ROOT/%{_datadir}/gdl

# Install the profile file to set GDL_PATH
install -d -m 0755 $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d
install -m 0644 %SOURCE1 $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d
install -m 0644 %SOURCE2 $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d


%check
cd testsuite
echo ".r test_suite" | ../src/gdl


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING HACKING NEWS README TODO
%config(noreplace) %{_sysconfdir}/profile.d/gdl.*sh
%{_bindir}/gdl

%files common
%defattr(-,root,root,-)
%{_datadir}/gdl/


%changelog
* Tue Dec  8 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 0.9-0.9.rc3
- Explicitly BR hdf-static in accordance with the Packaging
  Guidelines (hdf-devel is still static-only).

* Wed Nov 11 2009 - Orion Poplawski <orion@cora.nwra.com> - 0.9-0.8.rc3
- Rebuild for netcdf-4.1.0

* Thu Oct 15 2009 - Orion Poplawski <orion@cora.nwra.com> - 0.9-0.7.rc3
- Update to 0.9rc3
- Drop gcc43, ppc64, friend patches fixed upstream
- Add source for makecvstarball
- Rebase antlr patch, add automake source version
- Add conditionals for EPEL builds
- Add %%check section

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-0.6.rc2.20090312
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 16 2009 - Orion Poplawski <orion@cora.nwra.com> - 0.9-0.5.rc2.20090312
- Back off building python module until configure macro is updated

* Thu Mar 12 2009 - Orion Poplawski <orion@cora.nwra.com> - 0.9-0.4.rc2.20090312
- Update to 0.9rc2 cvs 20090312
- Rebase antlr patch
- Rebuild for new ImageMagick

* Thu Feb 26 2009 - Orion Poplawski <orion@cora.nwra.com> - 0.9-0.3.rc2.20090224
- Build python module
- Move common code to noarch common sub-package

* Tue Feb 24 2009 - Orion Poplawski <orion@cora.nwra.com> - 0.9-0.2.rc2.20090224
- Update to 0.9rc2 cvs 20090224
- Fix release tag
- Drop ImageMagick patch fixed upstream
- Add patch to compile with gcc 4.4.0 - needs new friend statement
- Don't build included copy of antlr, use system version

* Fri Jan 23 2009 - Orion Poplawski <orion@cora.nwra.com> - 0.9-0.rc2.1
- Update to 0.9rc2 based cvs

* Sun Nov 30 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.9-0.rc1.4.1
- Rebuild for Python 2.6

* Fri Sep  5 2008 - Orion Poplawski <orion@cora.nwra.com> - 0.9-0.rc1.4
- Add a requires on plplot to pull in drivers (bug#458277)

* Fri May 16 2008 - Orion Poplawski <orion@cora.nwra.com> - 0.9-0.rc1.3
- Update to latest cvs
- Add patch to handle new ImageMagick
- Update netcdf locations

* Mon Apr 28 2008 - Orion Poplawski <orion@cora.nwra.com> - 0.9-0.rc1.2
- Rebuild for new ImageMagick

* Sat Apr  5 2008 - Orion Poplawski <orion@cora.nwra.com> - 0.9-0.rc1.1
- Update to 0.9rc1

* Mon Mar 17 2008 - Orion Poplawski <orion@cora.nwra.com> - 0.9-0.pre6.2
- Update cvs patch to latest cvs

* Tue Mar 4 2008 - Orion Poplawski <orion@cora.nwra.com> - 0.9-0.pre6.1
- Rebuild for gcc 4.3, and add patch for gcc 4.3 support
- Add patch to build against plplot 5.9.0
- Add cvs patch to update to latest cvs

* Fri Nov  1 2007 - Orion Poplawski <orion@cora.nwra.com> - 0.9-0.pre6
- Update to 0.9pre6

* Tue Aug 21 2007 - Orion Poplawski <orion@cora.nwra.com> - 0.9-0.pre5.2
- Add patch to fix build on ppc64

* Tue Aug 21 2007 - Orion Poplawski <orion@cora.nwra.com> - 0.9-0.pre5.1
- Update license tag to GPLv2+
- Rebuild for BuildID

* Mon Jul  9 2007 - Orion Poplawski <orion@cora.nwra.com> - 0.9-0.pre5
- Update to 0.9pre5

* Tue May 22 2007 - Orion Poplawski <orion@cora.nwra.com> - 0.9-0.pre4.2
- Rebuild for netcdf 3.6.2 with shared libraries

* Tue Jan  9 2007 - Orion Poplawski <orion@cora.nwra.com> - 0.9-0.pre4.1
- Package the library routines and point to them by default

* Fri Jan  5 2007 - Orion Poplawski <orion@cora.nwra.com> - 0.9-0.pre4
- Update to 0.9pre4

* Mon Dec 18 2006 - Orion Poplawski <orion@cora.nwra.com> - 0.9-0.pre3.4
- Add patch for configure to handle python 2.5

* Thu Dec 14 2006 - Jef Spaleta <jspaleta@gmail.com> - 0.9-0.pre3.3
- Bump and build for python 2.5

* Wed Nov 22 2006 - Orion Poplawski <orion@cora.nwra.com> - 0.9-0.pre3.2
- Update to 0.9pre3

* Wed Oct  3 2006 - Orion Poplawski <orion@cora.nwra.com> - 0.9-0.pre3.1
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 19 2006 - Orion Poplawski <orion@cora.nwra.com> - 0.9-0.pre3
- Rebuild for FC6
- Add patch for specialization error caught by gcc 4.1.1

* Thu Jun 29 2006 - Orion Poplawski <orion@cora.nwra.com> - 0.9-0.pre2
- Update to 0.9pre2

* Sun Jun 11 2006 - Orion Poplawski <orion@cora.nwra.com> - 0.9-0.pre.1
- Rebuild for ImageMagick so bump

* Mon Apr  3 2006 - Orion Poplawski <orion@cora.nwra.com> - 0.9-0.pre
- Update to 0.9pre

* Fri Feb 24 2006 - Orion Poplawski <orion@cora.nwra.com> - 0.8.11-4
- Add --with-fftw to configure

* Thu Feb  2 2006 - Orion Poplawski <orion@cora.nwra.com> - 0.8.11-3
- Enable hdf for ppc
- Change fftw3 to fftw

* Tue Jan  3 2006 - Orion Poplawski <orion@cora.nwra.com> - 0.8.11-2
- Rebuild

* Mon Nov 21 2005 - Orion Poplawski <orion@cora.nwra.com> - 0.8.11-1
- Upstream 0.8.11
- Remove hdf patch fixed upstream
- Remove X11R6 lib path - not needed with modular X

* Wed Nov 16 2005 - Orion Poplawski <orion@cora.nwra.com> - 0.8.10-4
- Update for new ImageMagick version

* Thu Sep 22 2005 - Orion Poplawski <orion@cora.nwra.com> - 0.8.10-3
- Disable hdf with configure on ppc

* Thu Sep 22 2005 - Orion Poplawski <orion@cora.nwra.com> - 0.8.10-2
- Don't include hdf support on ppc

* Fri Aug 19 2005 - Orion Poplawski <orion@cora.nwra.com> - 0.8.10-1
- Initial Fedora Extras version
