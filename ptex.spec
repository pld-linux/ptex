#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

Summary:	Ptex - texture mapping system by Walt Disney Animation Studios
Summary(pl.UTF-8):	Ptex - system odwzorowywania tekstur z Walt Disney Animation Studios
Name:		ptex
Version:	2.4.1
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/wdas/ptex/releases
Source0:	https://github.com/wdas/ptex/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	2830df5248e87a3ac2e12228ba4ce549
URL:		http://ptex.us/
BuildRequires:	cmake >= 3.8.0
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Ptex is a texture mapping system developed by Walt Disney Animation
Studios for production-quality rendering:
- No UV assignment is required; Ptex applies a separate texture to
  each face of a subdivision or polygon mesh.
- The Ptex file format can efficiently store hundreds of thousands of
  texture images in a single file.
- The Ptex API provides cached file I/O and high-quality filtering -
  everything that is needed to easily add Ptex support to a
  production-quality renderer or texture authoring application.

%description -l pl.UTF-8
Ptex to system odwzorowywania tekstur stworzony przez Walt Disney
Animation Studios do renderowania z jakością produkcyjną:
- Nie wymaga przypisań UV; stosuje osobną teksturę dla każdej ściany
  podziału lub siatki wielokątnej.
- Format plików Ptex może wydajnie przechowywać setki tysięcy obrazów
  tekstur w pojedynczym pliku.
- API Ptex udostępnia operacje we/wy z buforowaniem oraz wysokiej
  jakości filtrowanie - to wystarczy, żeby dodać obsługę plików Ptex do
  renderera o jakości produkcyjnej lub aplikacji do tworzenia tekstur.

%package devel
Summary:	Header files for Ptex library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Ptex
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel
Requires:	zlib-devel

%description devel
Header files for Ptex library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Ptex.

%package static
Summary:	Static Ptex library
Summary(pl.UTF-8):	Statyczna biblioteka Ptex
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Ptex library.

%description static -l pl.UTF-8
Statyczna biblioteka Ptex.

%package apidocs
Summary:	Ptex API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki Ptex
Group:		Documentation
BuildArch:	noarch

%description apidocs
API and internal documentation for Ptex library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Ptex.

%prep
%setup -q

# see CMakeLists.txt:34-38 (if (NOT DEFINED PTEX_VER) ...)
echo %{version} > version

%build
mkdir build
cd build
%cmake ..

%{__make}

%if %{with apidocs}
%{__make} doxygen
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE src/doc/filterfootprint.txt
%attr(755,root,root) %{_bindir}/ptxinfo
%attr(755,root,root) %{_libdir}/libPtex.so.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libPtex.so
%{_includedir}/Ptex*.h
%{_datadir}/cmake/Ptex

%files static
%defattr(644,root,root,755)
%{_libdir}/libPtex.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc src/doc/ptex/*.{css,html,js,png}
%endif
