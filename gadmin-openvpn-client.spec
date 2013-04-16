# if I fix the string literal errors according to the wiki Problems
# page, it crashes on startup - AdamW 2009/01
%define Werror_cflags %nil

Summary:	A GTK+ administation tool for OpenVPN (client)
Name:		gadmin-openvpn-client
Version:	0.1.5
Release:	3
License:	GPLv3+
Group:		System/Configuration/Networking
URL:		http://www.gadmintools.org/
Source0:	http://mange.dynalias.org/linux/gadmin-openvpn/client/%{name}-%{version}.tar.gz
Source1:	%{name}.pam
BuildRequires:	gtk+2-devel
BuildRequires:	imagemagick
BuildRequires:	desktop-file-utils
Requires:	openvpn
Requires:	usermode-consoleonly
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Gadmin-OpenVPN-client is a fast and easy to use GTK+ administration tool for
OpenVPN (client use).

%prep
%setup -q

%build
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std

install -d %{buildroot}%{_sysconfdir}/%{name}

# pam auth
install -d %{buildroot}%{_sysconfdir}/pam.d/
install -d %{buildroot}%{_sysconfdir}/security/console.apps

install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/%{name}
install -m 644 etc/security/console.apps/%{name} %{buildroot}%{_sysconfdir}/security/console.apps/%{name}

## locales
%find_lang %{name}

# Mandriva Icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
convert -geometry 48x48 pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/48x48/%{name}.png
convert -geometry 32x32 pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/32x32/%{name}.png
convert -geometry 16x16 pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/16x16/%{name}.png

mkdir -p %{buildroot}%{_datadir}/applications
sed -i -e 's,%{name}.png,%{name},g' desktop/%{name}.desktop
sed -i -e 's,GADMIN-OPENVPN-Client,Gadmin-OpenVPN-client,g' desktop/%{name}.desktop
mv desktop/%{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-install --vendor="" \
    --remove-category="Application" \
    --add-category="Settings;Network;GTK;" \
    --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

# Prepare usermode entry
mkdir -p %{buildroot}%{_bindir}
mv %{buildroot}%{_sbindir}/%{name} %{buildroot}%{_sbindir}/%{name}.real
ln -s %{_bindir}/consolehelper %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
cat > %{buildroot}%{_sysconfdir}/security/console.apps/%{name} <<_EOF_
USER=root
PROGRAM=%{_sbindir}/%{name}.real
SESSION=true
FALLBACK=false
_EOF_

rm -rf %{buildroot}%{_datadir}/doc/%{name}



%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,0755)
%doc COPYING AUTHORS ChangeLog
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}
%dir %{_sysconfdir}/%{name}
%{_bindir}/%{name}
%{_sbindir}/%{name}.real
%{_datadir}/pixmaps/*.png
%{_datadir}/pixmaps/%{name}/*.png
%{_datadir}/applications/*
%{_iconsdir}/hicolor/*/%{name}.png



%changelog
* Sun May 22 2011 Funda Wang <fwang@mandriva.org> 0.1.5-1mdv2011.0
+ Revision: 676972
- update to new version 0.1.5

* Tue Mar 15 2011 Stéphane Téletchéa <steletch@mandriva.org> 0.1.4-1
+ Revision: 645175
- update to new version 0.1.4

* Sat Dec 25 2010 Funda Wang <fwang@mandriva.org> 0.1.3-1mdv2011.0
+ Revision: 624782
- update to new version 0.1.3

* Sun Aug 29 2010 Funda Wang <fwang@mandriva.org> 0.1.2-1mdv2011.0
+ Revision: 574139
- update to new version 0.1.2

* Sat Feb 27 2010 Funda Wang <fwang@mandriva.org> 0.1.1-1mdv2010.1
+ Revision: 512359
- new version 0.1.1

* Thu Jan 07 2010 Emmanuel Andry <eandry@mandriva.org> 0.0.8-1mdv2010.1
+ Revision: 487296
- New version 0.0.8

* Fri Sep 11 2009 Emmanuel Andry <eandry@mandriva.org> 0.0.7-1mdv2010.0
+ Revision: 438454
- New version 0.0.7

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 0.0.3-2mdv2010.0
+ Revision: 437633
- rebuild

* Sun Jan 04 2009 Adam Williamson <awilliamson@mandriva.org> 0.0.3-1mdv2009.1
+ Revision: 324195
- import gadmin-openvpn-client


