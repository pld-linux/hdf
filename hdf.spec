#
# Conditional build:
%bcond_without	java	# Java JNI interface
%bcond_without	szip	# SZIP compression support
#
Summary:	Hierarchical Data Format library
Summary(pl.UTF-8):	Biblioteka HDF (Hierarchical Data Format)
Name:		hdf
%define	basever	4.2.16
%define	subver	2
Version:	%{basever}.%{subver}
%define	origver	%{basever}-%{subver}
Release:	1
Epoch:		1
Group:		Libraries
License:	BSD-like
# latest releases listed at https://support.hdfgroup.org/downloads/index.html
Source0:	https://hdf-wordpress-1.s3.amazonaws.com/wp-content/uploads/manual/HDF4/HDF%{origver}/src/hdf-%{origver}.tar.bz2
# Source0-md5:	82f834cd6217ea2ae71e035268674f7e
Source1:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-man-pages.tar.bz2
# Source1-md5:	607df78cacc131b37dfdb443e61e789a
Patch0:		%{name}-shared.patch
Patch1:		%{name}-types.patch
Patch3:		%{name}-szip.patch
Patch5:		%{name}-opt.patch
URL:		https://www.hdfgroup.org/solutions/hdf4/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gcc-fortran
BuildRequires:	groff
%{?with_java:BuildRequires:	jdk}
%{?with_szip:BuildRequires:	libaec-szip-devel >= 1.0}
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libtirpc-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	rpmbuild(macros) >= 1.750
BuildRequires:	which
BuildRequires:	zlib-devel >= 1.1.4
%{?with_szip:Requires:	libaec-szip >= 1.0}
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
%{?with_szip:Requires:	libaec-szip-devel >= 1.0}
Requires:	libjpeg-devel >= 6b
Requires:	libtirpc-devel
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

%package -n java-hdf
Summary:	Java HDF Interface (JHI)
Summary(pl.UTF-8):	Interfejs HDF do Javy (JHI)
Group:		Libraries/Java
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	java-slf4j >= 1.7.25

%description -n java-hdf
The Java Native Interface to the standard HDF library.

%description -n java-hdf -l pl.UTF-8
Natywny interfejs Javy (JNI) do biblioteki standardowej HDF.

%package -n java-hdf-javadoc
Summary:	Javadoc documentation for Java HDF Interface (JHI)
Summary(pl.UTF-8):	Dokumentacja javadoc do interfejsu HDF do Javy (JHI)
Group:		Documentation

%description -n java-hdf-javadoc
Javadoc documentation for Java HDF Interface (JHI).

%description -n java-hdf-javadoc -l pl.UTF-8
Dokumentacja javadoc do interfejsu HDF do Javy (JHI).

%prep
%setup -q -n %{name}-%{origver}
%patch -P0 -p1
%patch -P1 -p1
%patch -P3 -p1
%patch -P5 -p1

%ifarch x32
ln -s linux-gnu config/linux-gnux32
%endif

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
# need to pass F77 to override F77=g77 in config/linux-gnu
%ifarch x32
%define	gfortran	x86_64-pld-linux-gnux32-gfortran
%else
%define	gfortran	%{_target_cpu}-pld-linux-gfortran
%endif
%configure \
	F77="%{gfortran}" \
	--enable-fortran \
	%{?with_java:--enable-java} \
	--enable-shared \
	--disable-silent-rules \
	%{?with_szip:--with-szlib}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_mandir}/man{3,7},%{_includedir}/hdf}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	EXAMPLETOPDIR=$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version} \
	EXAMPLEDIR=$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/c \
	hdf_javadir=%{_javadir}

%{__mv} $RPM_BUILD_ROOT%{_includedir}/*.{h,inc,f90} $RPM_BUILD_ROOT%{_includedir}/hdf

cp -p man/gr_chunk.3 $RPM_BUILD_ROOT%{_mandir}/man3
%{__mv} $RPM_BUILD_ROOT%{_mandir}/man1/hdf.1 $RPM_BUILD_ROOT%{_mandir}/man7/hdf.7

# resolve conflict with netcdf
for i in ncdump ncgen ; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/$i $RPM_BUILD_ROOT%{_bindir}/hdf$i
	%{__mv} $RPM_BUILD_ROOT%{_mandir}/man1/$i.1 $RPM_BUILD_ROOT%{_mandir}/man1/hdf$i.1
done

%if %{with java}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libhdf_java.{la,a}
ln -sf jarhdf-%{origver}.jar $RPM_BUILD_ROOT%{_javadir}/jarhdf.jar
install -d $RPM_BUILD_ROOT%{_javadocdir}
cp -pr java/src/javadoc $RPM_BUILD_ROOT%{_javadocdir}/hdflib
%endif

bzip2 -dc %{SOURCE1} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}
%{__rm} $RPM_BUILD_ROOT%{_mandir}/README.hdf-man-pages
%{__rm} $RPM_BUILD_ROOT%{_mandir}/diff.*

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n java-hdf -p /sbin/ldconfig
%postun	-n java-hdf -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README.md release_notes/{HISTORY,RELEASE,bugs_fixed,misc_docs}.txt
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

%if %{with java}
%files -n java-hdf
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhdf_java.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhdf_java.so.0
%attr(755,root,root) %{_libdir}/libhdf_java.so
%{_javadir}/jarhdf-%{origver}.jar
%{_javadir}/jarhdf.jar

%files -n java-hdf-javadoc
%defattr(644,root,root,755)
%{_javadocdir}/hdflib
%endif
