Summary:	TellStick controlling library
Name:		telldus-core
Version:	2.1.0
Release:	1
License:	LGPLv2.1+
Group:		System/Configuration/Boot and Init
Source0:	http://download.telldus.se/TellStick/Software/telldus-core/%{name}-%{version}.tar.gz
Source1:	telldusd.init
Patch0:		telldus-core-2.1.0-get-ftdi-includedir-from-pkgconfig.patch
Patch1:		telldus-core-2.1.0-fix-libdir-path,patch
Patch2:		telldus-core-2.1.0-run-under-dedicated-user.patch
URL:		http://developer.telldus.se
BuildRequires:	pkgconfig(libftdi) pkgconfig(libconfuse)

%define	major	2
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname -d %{name}

%description
Telldus Core is the driver and tools for controlling a Telldus Technologies
TellStick. It does not containing any GUI tools which makes it suitable for
server use.

%package -n	%{libname}
Summary:	Library for telldus-core
Group:		System/Libraries

%package -n	%{devname}
Summary:	Development files for developing programs against telldus-core
Group:		Development/C
Requires:	%{libname} = %{EVRD}

%description -n	%{devname}

%prep
%setup -q
%patch0 -p1 -b .ftdi_inc~
%patch1 -p1 -b .libdir~
%patch2 -p1 -b .deduser~

%build
%cmake -DGENERATE_MAN:BOOL=ON
# parallel build broken :/
make

%install
%makeinstall_std -C build
install -m755 %{SOURCE1} -D %{buildroot}%{_initrddir}/telldusd

%pre
%_pre_useradd telldusd / /sbin/nologin

%post
%{_post_service telldusd}

%preun
%{_preun_service telldusd}

%files
%doc AUTHORS README
%config(noreplace) %{_sysconfdir}/tellstick.conf
%{_sysconfdir}/udev/rules.d/05-tellstick.rules
%{_initrddir}/telldusd
%{_bindir}/tdtool
%{_sbindir}/tdadmin
%{_sbindir}/telldusd
%{_mandir}/man1/tdtool.1*
%{_mandir}/man1/tdadmin.1*
%{_mandir}/man1/telldusd.1*
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/helpers/
%{_datadir}/%{name}/helpers/udev.sh
%config %{_var}/state/telldus-core.conf

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{devname}
%{_includedir}/%{name}.h
%{_libdir}/*.so

