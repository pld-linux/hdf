#
# Conditional build:
%bcond_without	szip	# build without SZIP support
#
Summary:	Hierarchical Data Format library
Summary(pl.UTF-8):	Biblioteka HDF (Hierarchical Data Format)
Name:		hdf
Version:	4.2.15
Release:	1
Epoch:		1
Group:		Libraries
License:	Nearly BSD, but changed sources must be marked
Source0:	https://support.hdfgroup.org/ftp/HDF/releases/HDF%{version}/src/hdf-%{version}.tar.bz2
# Source0-md5:	27ab87b22c31906883a0bfaebced97cb
Source1:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-man-pages.tar.bz2
# Source1-md5:	607df78cacc131b37dfdb443e61e789a
Patch0:		%{name}-shared.patch
Patch1:		%{name}-morearchs.patch
Patch2:		%{name}-link.patch
Patch3:		%{name}-szip.patch
Patch4:		%{name}-tirpc.patch
URL:		http://portal.hdfgroup.org/display/HDF4/HDF4
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gcc-fortran
BuildRequires:	groff
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libtirpc-devel
BuildRequires:	libtool >= 2:1.4d-3
%{?with_szip:BuildRequires:	szip-devel >= 2.0}
BuildRequires:	which
BuildRequires:	zlib-devel >= 1.1.4
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

%description -l pl.UTF-8
HDF jest wieloobiektowym formatem plików ułatwiającym przenoszenie
różnych danych naukowych pomiędzy różnymi komputerami i systemami
operacyjnymi. Aktualnie obsługiwane są m.in. Cray, HP, Vax, Sun, IBM
RS/6000, Silicon Graphics, Macintosh i IBM PC. HDF zawiera interfejsy
do Fortranu i C oraz narzędzia do przygotowywania plików z danymi.
Biblioteka pozwala na przechowywanie i odczytywanie skompresowanych
lub nie 8-bitowych i 24-bitowych obrazków z paletą, wielowymiarowych
zestawów danych itp.

%package devel
Summary:	HDF library development package
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki HDF
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	libjpeg-devel >= 6b
Requires:	libtirpc-devel
%{?with_szip:Requires:	szip-devel >= 2.0}
Requires:	zlib-devel >= 1.1.4

%description devel
Header files for HDF library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki HDF.

%package static
Summary:	HDF static library
Summary(pl.UTF-8):	Statyczna biblioteka HDF
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static version of HDF library.

%description static -l pl.UTF-8
Statyczna wersja biblioteki HDF.

%package progs
Summary:	HDF utilities
Summary(pl.UTF-8):	Narzędzia do plików HDF
Group:		Applications/File
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description progs
Utilities to convert from/to HDF format.

%description progs -l pl.UTF-8
Narzędzia do konwersji z i do formatu HDF.

%package examples
Summary:	HDF example programs (source code)
Summary(pl.UTF-8):	Przykładowe programy dla biblioteki HDF (w postaci źródłowej)
Group:		Documentation

%description examples
HDF example programs (source code).

%description examples -l pl.UTF-8
Przykładowe programy dla biblioteki HDF (w postaci źródłowej).

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
# need to pass F77 to override F77=g77 in config/linux-gnu
%configure \
%ifarch x32
	F77="x86_64-pld-linux-gnux32-gfortran" \
%else
	F77="%{_target_cpu}-pld-linux-gfortran" \
%endif
	--enable-shared \
	%{?with_szip:--with-szlib}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_mandir}/man{3,7},%{_includedir}/hdf}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	EXAMPLETOPDIR=$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version} \
	EXAMPLEDIR=$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/c \

%{__mv} $RPM_BUILD_ROOT%{_includedir}/*.{h,inc,f90} $RPM_BUILD_ROOT%{_includedir}/hdf

cp -p man/gr_chunk.3 $RPM_BUILD_ROOT%{_mandir}/man3
%{__mv} $RPM_BUILD_ROOT%{_mandir}/man1/hdf.1 $RPM_BUILD_ROOT%{_mandir}/man7/hdf.7

# resolve conflict with netcdf
for i in ncdump ncgen ; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/$i $RPM_BUILD_ROOT%{_bindir}/hdf$i
	%{__mv} $RPM_BUILD_ROOT%{_mandir}/man1/$i.1 $RPM_BUILD_ROOT%{_mandir}/man1/hdf$i.1
done

bzip2 -dc %{SOURCE1} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}
%{__rm} $RPM_BUILD_ROOT%{_mandir}/README.hdf-man-pages
%{__rm} $RPM_BUILD_ROOT%{_mandir}/diff.*

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README.txt release_notes/{HISTORY,RELEASE,bugs_fixed,misc_docs}.txt
%attr(755,root,root) %{_libdir}/libdf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdf.so.0
%attr(755,root,root) %{_libdir}/libmfhdf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmfhdf.so.0
%{_libdir}/libhdf4.settings

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdf.so
%attr(755,root,root) %{_libdir}/libmfhdf.so
%{_libdir}/libdf.la
%{_libdir}/libmfhdf.la
%{_includedir}/hdf
%{_mandir}/man3/gr_chunk.3*
%{_mandir}/man7/hdf.7*

%files static
%defattr(644,root,root,755)
%{_libdir}/libdf.a
%{_libdir}/libmfhdf.a

%files progs
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gif2hdf
%attr(755,root,root) %{_bindir}/h4cc
%attr(755,root,root) %{_bindir}/h4fc
%attr(755,root,root) %{_bindir}/h4redeploy
%attr(755,root,root) %{_bindir}/hdf24to8
%attr(755,root,root) %{_bindir}/hdf2gif
%attr(755,root,root) %{_bindir}/hdf2jpeg
%attr(755,root,root) %{_bindir}/hdf8to24
%attr(755,root,root) %{_bindir}/hdfcomp
%attr(755,root,root) %{_bindir}/hdfed
%attr(755,root,root) %{_bindir}/hdfimport
%attr(755,root,root) %{_bindir}/hdfls
%attr(755,root,root) %{_bindir}/hdfncdump
%attr(755,root,root) %{_bindir}/hdfncgen
%attr(755,root,root) %{_bindir}/hdfpack
%attr(755,root,root) %{_bindir}/hdftopal
%attr(755,root,root) %{_bindir}/hdftor8
%attr(755,root,root) %{_bindir}/hdfunpac
%attr(755,root,root) %{_bindir}/hdiff
%attr(755,root,root) %{_bindir}/hdp
%attr(755,root,root) %{_bindir}/hrepack
%attr(755,root,root) %{_bindir}/jpeg2hdf
%attr(755,root,root) %{_bindir}/paltohdf
%attr(755,root,root) %{_bindir}/r8tohdf
%attr(755,root,root) %{_bindir}/ristosds
%attr(755,root,root) %{_bindir}/vmake
%attr(755,root,root) %{_bindir}/vshow
%{_mandir}/man1/fp2hdf.1*
%{_mandir}/man1/gif2hdf.1*
%{_mandir}/man1/hdf24to8.1*
%{_mandir}/man1/hdf2gif.1*
%{_mandir}/man1/hdf2jpeg.1*
%{_mandir}/man1/hdf8to24.1*
%{_mandir}/man1/hdfcomp.1*
%{_mandir}/man1/hdfed.1*
%{_mandir}/man1/hdfls.1*
%{_mandir}/man1/hdfncdump.1*
%{_mandir}/man1/hdfncgen.1*
%{_mandir}/man1/hdfpack.1*
%{_mandir}/man1/hdftopal.1*
%{_mandir}/man1/hdftor8.1*
%{_mandir}/man1/hdp.1*
%{_mandir}/man1/jpeg2hdf.1*
%{_mandir}/man1/paltohdf.1*
%{_mandir}/man1/r8tohdf.1*
%{_mandir}/man1/ristosds.1*
%{_mandir}/man1/vmake.1*
%{_mandir}/man1/vshow.1*

%files examples
%defattr(644,root,root,755)
%dir %{_examplesdir}/%{name}-%{version}
%{_examplesdir}/%{name}-%{version}/README
%attr(755,root,root) %{_examplesdir}/%{name}-%{version}/run-all-ex.sh
%dir %{_examplesdir}/%{name}-%{version}/c
%{_examplesdir}/%{name}-%{version}/c/*.c
%{_examplesdir}/%{name}-%{version}/c/*.f
%attr(755,root,root) %{_examplesdir}/%{name}-%{version}/c/run-c-ex.sh
%attr(755,root,root) %{_examplesdir}/%{name}-%{version}/c/run-fortran-ex.sh
