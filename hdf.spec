Summary:	Hierarchical Data Format library
Summary(pl):	Biblioteka HDF (Hierarchical Data Format)
Name:		hdf
Version:	4.2r0
Release:	1
Group:		Libraries
License:	Nearly BSD, but changed sources must be marked
Source0:	ftp://ftp.ncsa.uiuc.edu/HDF/HDF/HDF_Current/src/HDF%{version}.tar.gz
# Source0-md5:	3cede01c62864f5a902ef8e06a525aae
Source1:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-man-pages.tar.bz2
# Source1-md5:	607df78cacc131b37dfdb443e61e789a
Patch0:		%{name}-shared.patch
Patch1:		%{name}-opt.patch
Patch2:		%{name}-morearchs.patch
URL:		http://hdf.ncsa.uiuc.edu/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gcc-g77
BuildRequires:	groff
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libtool >= 2:1.4d-3
BuildRequires:	which
BuildRequires:	zlib-devel >= 1.1.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HDF is a multi-object file format that facilitates the transfer of
various types of scientific data between machines and operating
systems. Machines currently supported include the Cray, HP, Vax, Sun,
IBM RS/6000, Silicon Graphics, Macintosh, and IBM PC computers. HDF
allows self-definitions of data content and easy extensibility for
future enhancements or compatibility with other standard formats. HDF
includes Fortran and C calling interfaces,and utilities to prepare raw
image of data files or for use with other NCSA software. The HDF
library contains interfaces for storing and retrieving compressed or
uncompressed 8-bit and 24-bit raster images with palettes,
n-Dimensional scientific datasets and binary tables. An interface is
also included that allows arbitray grouping of other HDF objects.

%description -l pl
HDF jest wieloobiektowym formatem plików u³atwiaj±cym przenoszenie
ró¿nych danych naukowych pomiêdzy ró¿nymi komputerami i systemami
operacyjnymi. Aktualnie obs³ugiwane s± m.in. Cray, HP, Vax, Sun, IBM
RS/6000, Silicon Graphics, Macintosh i IBM PC. HDF zawiera interfejsy
do Fortranu i C oraz narzêdzia do przygotowywania plików z danymi.
Biblioteka pozwala na przechowywanie i odczytywanie skompresowanych
lub nie 8-bitowych i 24-bitowych obrazków z palet±, wielowymiarowych
zestawów danych itp.

%package devel
Summary:	HDF library development package
Summary(pl):	Pliki nag³ówkowe biblioteki HDF
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libjpeg-devel
Requires:	zlib-devel

%description devel
Header files for HDF library.

%description devel -l pl
Pliki nag³ówkowe biblioteki HDF.

%package static
Summary:	HDF static library
Summary(pl):	Statyczna biblioteka HDF
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of HDF library.

%description static -l pl
Statyczna wersja biblioteki HDF.

%package progs
Summary:	HDF utilities
Summary(pl):	Narzêdzia do plików HDF
Group:		Applications/File
Requires:	%{name} = %{version}-%{release}

%description progs
Utilities to convert from/to HDF format.

%description progs -l pl
Narzêdzia do konwersji z i to formatu HDF.

%prep
%setup -q -n HDF%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%ifarch ppc ppc64 sparc sparcv9 sparc64
%{__perl} -pi -e 's/^SWAP.*$/SWAP=/' config/mh-linux
%endif

%build
cp -f /usr/share/automake/config.* hdf/fmpool
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_mandir}/man{3,7},%{_includedir}/hdf}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_includedir}/*.{h,inc,f90} $RPM_BUILD_ROOT%{_includedir}/hdf

install man/gr_chunk.3 $RPM_BUILD_ROOT%{_mandir}/man3
mv -f $RPM_BUILD_ROOT%{_mandir}/man1/hdf.1 $RPM_BUILD_ROOT%{_mandir}/man7/hdf.7

# resolve conflict with netcdf
for i in ncdump ncgen ; do
	mv -f $RPM_BUILD_ROOT%{_bindir}/$i $RPM_BUILD_ROOT%{_bindir}/hdf$i
	mv -f $RPM_BUILD_ROOT%{_mandir}/man1/$i.1 $RPM_BUILD_ROOT%{_mandir}/man1/hdf$i.1
done

bzip2 -dc %{SOURCE1} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README release_notes/*
%attr(755,root,root) %{_libdir}/libdf.so.*.*
%attr(755,root,root) %{_libdir}/libmfhdf.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdf.so
%attr(755,root,root) %{_libdir}/libmfhdf.so
%{_libdir}/libdf.la
%{_libdir}/libmfhdf.la
# static-only stub
%{_libdir}/libudport.a
%{_includedir}/hdf
%{_mandir}/man[37]/*

%files static
%defattr(644,root,root,755)
%{_libdir}/libdf.a
%{_libdir}/libmfhdf.a

%files progs
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*
