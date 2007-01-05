Name:           gdl
Version:        0.9
Release:        0.pre4%{?dist}
Summary:        GNU Data Language

Group:          Applications/Engineering
License:        GPL
URL:            http://gnudatalanguage.sourceforge.net/
Source0:        http://dl.sf.net/gnudata/%{name}-%{version}pre4.tar.gz
Patch1:         gdl-0.9pre3-python25.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  readline-devel, ncurses-devel
BuildRequires:  gsl-devel, plplot-devel, ImageMagick-c++-devel
BuildRequires:  netcdf-devel, hdf5-devel, libjpeg-devel
BuildRequires:  python-devel, python-numarray, python-matplotlib
BuildRequires:  fftw-devel, hdf-devel, proj-devel


%description
A free IDL (Interactive Data Language) compatible incremental compiler
(ie. runs IDL programs). IDL is a registered trademark of Research
Systems Inc.


%prep
%setup -q -n %{name}-%{version}pre4
%patch1 -p1 -b .python25


%build
%configure --disable-dependency-tracking --disable-static --with-fftw \
           INCLUDES="-I/usr/include/netcdf-3 -I/usr/include/hdf" \
           LIBS="-L%{_libdir}/netcdf-3 -L%{_libdir}/hdf"
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -r $RPM_BUILD_ROOT/%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING HACKING NEWS PYTHON.txt README TODO
%{_bindir}/gdl


%changelog
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
