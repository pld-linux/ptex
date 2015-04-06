#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
#
Summary:	Ptex - texture mapping system by Walt Disney Animation Studios
Summary(pl.UTF-8):	Ptex - system odwzorowywania tekstur z Walt Disney Animation Studios
Name:		ptex
Version:	2.0.42
Release:	2
License:	BSD
Group:		Libraries
# (not precisely: see github for releases, then fetch appropriate tarball)
#Source0Download: https://github.com/wdas/ptex
Source0:	https://github.com/wdas/ptex/tarball/v%{version}?/%{name}-%{version}.tar.gz
# Source0-md5:	80181532ab9ef9dcc729344f45415c8b
URL:		http://ptex.us/
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libstdc++-devel
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
  jakości filtrowanie - to wystarczy, żeby dodać obsługę plików Ptex
  do renderera o jakości produkcyjnej lub aplikacji do tworzenia
  tekstur.

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

%description apidocs
API and internal documentation for Ptex library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Ptex.

%prep
%setup -q -n wdas-ptex-7e2cb22

%build
%{__make} -j1 -C src/ptex \
	CXX="%{__cxx}" \
	DEBUG="%{rpmcxxflags} %{rpmcppflags} -fPIC -DNDEBUG"

%{__make} -j1 -C src/utils \
	CXX="%{__cxx}" \
	DEBUG="%{rpmcxxflags} %{rpmcppflags} -DNDEBUG"

%if %{with apidocs}
# make doc generates source docs, not just API; invoke doxygen manually
#%{__make} -C src/doc
cd src/doc
install -d ../../install/apidocs/ptex
doxygen Doxyfile_API_only
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C src/ptex install \
	INSTALLDIR=$RPM_BUILD_ROOT%{_prefix} \
	LIBDIR=%{_lib}

%{__make} -C src/utils install \
	INSTALLDIR=$RPM_BUILD_ROOT%{_prefix}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc src/doc/{FilterFootprint.html,License.txt}
%attr(755,root,root) %{_bindir}/ptxinfo
%attr(755,root,root) %{_libdir}/libPtex.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/Ptex*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libPtex.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc apidocs/*.{css,html,js,png}
%endif
