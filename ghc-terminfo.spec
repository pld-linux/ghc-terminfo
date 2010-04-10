%define	pkgname	terminfo
Summary:	Haskell bindings to the terminfo library
Name:		ghc-%{pkgname}
Version:	0.3.1.2
Release:	1
License:	BSD
Group:		Development/Languages
Source0:	http://hackage.haskell.org/packages/archive/%{pkgname}/%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	5840d32cc06109d23ebda5509fb242a9
URL:		http://hackage.haskell.org/package/%{pkgname}/
BuildRequires:	ghc >= 6.10
BuildRequires:	ncurses-devel
%requires_eq	ghc
Requires:	ncurses-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		libsubdir	ghc-%(/usr/bin/ghc --numeric-version)/%{pkgname}-%{version}

%description
This library provides an interface to the terminfo database
(via bindings to the curses library). Terminfo allows POSIX
systems to interact with a variety of terminals using
a standard set of capabilities. 

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.lhs configure -v2 \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--libsubdir=%{libsubdir} \
	--docdir=%{_docdir}/%{name}-%{version} \
	--configure-option="--with-curses-includes=/usr/include/ncursesw"

runhaskell Setup.lhs build
runhaskell Setup.lhs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
rm -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc

runhaskell Setup.lhs register \
	--gen-pkg-config=$RPM_BUILD_ROOT/%{_libdir}/%{libsubdir}/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/bin/ghc-pkg update %{_libdir}/%{libsubdir}/%{pkgname}.conf

%postun
if [ "$1" = "0" ]; then
	/usr/bin/ghc-pkg unregister %{pkgname}-%{version}
fi

%files
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/html
%{_libdir}/%{libsubdir}
