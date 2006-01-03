Name:           gdl
Version:        0.8.11
Release:        2%{?dist}
Summary:        GNU Data Language

Group:          Applications/Engineering
License:        GPL
URL:            http://gnudatalanguage.sourceforge.net/
Source0:        http://dl.sf.net/gnudata/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  readline-devel, ncurses-devel
BuildRequires:  gsl-devel, plplot-devel, ImageMagick-c++-devel
BuildRequires:  netcdf-devel, hdf5-devel, libjpeg-devel
BuildRequires:  python-devel, python-numarray, python-matplotlib
BuildRequires:  fftw3-devel
%ifnarch ppc ppc64
BuildRequires:  hdf-devel
%define hdfconfig %{nil}
%define hdfinclude "-I/usr/include/hdf"
%define hdflib "-L%{_libdir}/hdf"
%else
%define hdfconfig "--with-hdf=no"
%define hdfinclude %{nil}
%define hdflib %{nil}
%endif


%description
A free IDL (Interactive Data Language) compatible incremental compiler
(ie. runs IDL programs). IDL is a registered trademark of Research
Systems Inc.


%prep
%setup -q


%build
%configure --disable-static %{hdfconfig} \
           INCLUDES="-I/usr/include/netcdf-3 %{hdfinclude}" \
           LIBS="-L%{_libdir}/netcdf-3 %{hdflib}"
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
