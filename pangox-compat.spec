#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	System for layout and rendering of internationalized text - X11 backend
Summary(pl.UTF-8):	System renderowania międzynarodowego tekstu - backend X11
Name:		pangox-compat
Version:	0.0.2
Release:	1
License:	LGPL v2+
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/pangox-compat/0.0/%{name}-%{version}.tar.xz
# Source0-md5:	7bcbd0187f03e1e27af9a81e07249c33
Patch0:		%{name}-xfonts.patch
Patch1:		%{name}-arch_confdir.patch
URL:		http://www.pango.org/
BuildRequires:	autoconf >= 2.59-9
BuildRequires:	automake >= 1:1.9
BuildRequires:	glib2-devel >= 1:2.32.0
BuildRequires:	libtool
BuildRequires:	pango-devel >= 1:1.32.0
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
Requires:	glib2 >= 1:2.32.0
Requires:	pango >= 1:1.32.0
Obsoletes:	pangox
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if "%{_lib}" != "lib"
%define		libext		%(lib="%{_lib}"; echo ${lib#lib})
%define		_sysconfdir	/etc/pango%{libext}
%else
%define		_sysconfdir	/etc/pango
%endif

%description
This is a compatibility library providing the obsolete pangox library
that is not shipped by Pango itself anymore.

%description -l pl.UTF-8
Ten pakiet istnieje dla kompatybilności, zawiera przestarzałą
bibliotekę pangox, która już nie jest dostarczana wraz z pakietem
Pango.

%package devel
Summary:	Development files for pangox library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki pangox
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.32.0
Requires:	pango >= 1:1.32.0
Requires:	xorg-lib-libX11-devel
Obsoletes:	pangox-devel

%description devel
Development files for pangox library.

%description devel -l pl.UTF-8
Pliki programistyczne biblioteki pangox.

%package static
Summary:	Static pangox library
Summary(pl.UTF-8):	Statyczna biblioteka pangox
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	pangox-static
Conflicts:	pango-static < 1:1.32.0

%description static
Static pangox library.

%description static -l pl.UTF-8
Statyczna biblioteka pangox.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libpangox-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpangox-1.0.so.0
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pangox.aliases

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpangox-1.0.so
%{_libdir}/libpangox-1.0.la
%{_pkgconfigdir}/pangox.pc
%{_includedir}/pango-1.0/pango/pangox.h

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libpangox-1.0.a
%endif
