Name:           gdl
Version:        0.8.10
Release:        1%{?dist}
Summary:        GNU Data Language

Group:          Applications/Engineering
License:        GPL
URL:            http://gnudatalanguage.sourceforge.net/
Source0:        http://dl.sf.net/gnudata/%{name}-%{version}.tar.gz
Patch0:         gdl-0.8.10-hdf5.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  readline-devel, ncurses-devel
BuildRequires:  gsl-devel, plplot-devel, ImageMagick-c++-devel
BuildRequires:  netcdf-devel, hdf5-devel, hdf-devel, libjpeg-devel
BuildRequires:  python-devel, python-numarray, python-matplotlib
#Requires:       

%description
A free IDL (Interactive Data Language) compatible incremental compiler
(ie. runs IDL programs). IDL is a registered trademark of Research
Systems Inc.


%prep
%setup -q
%patch -p1 -b .orig


%build
%configure --disable-static \
           INCLUDES="-I/usr/include/netcdf-3 -I/usr/include/hdf" \
           LIBS="-L%{_libdir}/netcdf-3 -L%{_libdir}/hdf -L/usr/X11R6/%{_lib}"
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
* Fri Aug 19 2005 - Orion Poplawski <orion@cora.nwra.com> - 0.8.10-1
- Initial Fedora Extras version
