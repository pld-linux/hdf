Summary:	Hierarchical Data Format library
Summary(pl):	Biblioteka HDF (Hierarchical Data Format)
Name:		hdf
Version:	4.1r5
Release:	2
Group:		Libraries
License:	Nearly BSD, but changed sources must be marked
Source0:	ftp://ftp.ncsa.uiuc.edu/HDF/HDF/HDF_Current/tar/HDF%{version}.tar.gz
Source1:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-man-pages.tar.bz2
Patch0:		%{name}-system-libs.patch
Patch1:		%{name}-strdup.patch
Patch2:		%{name}-shared.patch
URL:		http://hdf.ncsa.uiuc.edu/
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gcc-g77
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libtool >= 0:1.4.2
BuildRequires:	zlib-devel >= 1.1.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
ExclusiveArch:	%{ix86} alpha

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
Requires:	%{name} = %{version}

%description devel
Header files for HDF library.

%description devel -l pl
Pliki nag³ówkowe biblioteki HDF.

%package static
Summary:	HDF static library
Summary(pl):	Statyczna biblioteka HDF
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static version of HDF library.

%description static -l pl
Statyczna wersja biblioteki HDF.

%package progs
Summary:	HDF utilities
Summary(pl):	Narzêdzia do plików HDF
Group:		Applications/File
Requires:	%{name} = %{version}

%description progs
Utilities to convert from/to HDF format.

%description progs -l pl
Narzêdzia do konwersji z i to formatu HDF.

%prep
%setup -q -n HDF%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
./configure %{_target_platform} \
	--prefix=%{_prefix} --exec-prefix=%{_exec_prefix}

# libtool 1.4d requires --tag for g77, but doesn't have good tag for g77
grep -q -e '--tag' `which libtool` && LTTAG="--tag=dummy"

%{__make} CFLAGS="%{rpmcflags} -ansi -D_BSD_SOURCE -DHAVE_NETCDF" \
	FFLAGS="%{rpmcflags}" YACC="bison -y" LTTAG="$LTTAG"

# avoid relinking
cd mfhdf/libsrc
sed -e '/^relink_command/d' libmfhdf.la > libmfhdf.la.tmp
mv -f libmfhdf.la.tmp libmfhdf.la

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_mandir}/man{3,7},%{_includedir}/hdf}

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	exec_prefix=$RPM_BUILD_ROOT%{_exec_prefix} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	infodir=$RPM_BUILD_ROOT%{_infodir}

mv -f $RPM_BUILD_ROOT%{_includedir}/*.{h,inc,f90} $RPM_BUILD_ROOT%{_includedir}/hdf

install man/gr_chunk.3 $RPM_BUILD_ROOT%{_mandir}/man3
mv -f $RPM_BUILD_ROOT%{_mandir}/man1/hdf.1 $RPM_BUILD_ROOT%{_mandir}/man7/hdf.7

# resolve conflict with netcdf and move manuals to FHS location
# NOTE: don't let adapter change %%{_prefix}/man to %%{_mandir}
for i in ncdump ncgen ; do
	mv -f $RPM_BUILD_ROOT%{_bindir}/$i $RPM_BUILD_ROOT%{_bindir}/hdf$i
	mv -f $RPM_BUILD_ROOT/usr/man/man1/$i.1 $RPM_BUILD_ROOT%{_mandir}/man1/hdf$i.1
done

# remove unwanted path from libtool script
cat $RPM_BUILD_ROOT%{_libdir}/libmfhdf.la | \
	awk '/^dependency_libs/ { gsub("-L[ \t]*[^ \t]*/\.libs ","") } //' \
	> $RPM_BUILD_ROOT%{_libdir}/libmfhdf.la.tmp
mv -f $RPM_BUILD_ROOT%{_libdir}/libmfhdf.la.tmp $RPM_BUILD_ROOT%{_libdir}/libmfhdf.la

bzip2 -dc %{SOURCE1} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README release_notes/bugs* release_notes/ABOUT*
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%doc release_notes/compile*
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/hdf
%{_mandir}/man[37]/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files progs
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*
