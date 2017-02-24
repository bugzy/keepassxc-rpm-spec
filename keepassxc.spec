Name: keepassxc
Version: 2.1.2
Release: 4%{?dist}
Summary: Cross-platform password manager
Group: User Interface/Desktops
License: GPLv2+
URL: https://keepassxreboot.github.io/
Source0: https://github.com/keepassxreboot/keepassxc/releases/download/%{version}/keepassxc-%{version}-src.tar.xz
BuildRequires: qt5-qtbase-devel > 5.1
BuildRequires: qt5-linguist
BuildRequires: libXtst-devel
BuildRequires: ImageMagick
BuildRequires: desktop-file-utils
BuildRequires: cmake
BuildRequires: liboath
BuildRequires: liboath-devel
%if 0%{?el7}
BuildRequires: libgcrypt16-devel
%else
BuildRequires: libgcrypt-devel
%endif
BuildRequires: libmicrohttpd-devel
BuildRequires: qjson-devel
BuildRequires: libevent-devel
BuildRequires: libsecret-devel
BuildRequires: qt5-qtx11extras-devel
Requires: hicolor-icon-theme
%if 0%{?el7}
Requires: libgcrypt16
%else
Requires: libgcrypt
%endif
Requires: libmicrohttpd 
Requires: libevent
Requires: zlib
Requires: libXi
Requires: libXtst
Requires: qt5-qtx11extras
 
%description
KeePassXC is a community fork of KeePassX, the cross-platform port of KeePass for Windows. Every feature is cross-platform and tested to give users the same feel on each operating system, including the loved auto-type feature.

 
%prep
%setup -qn %{name}-%{version}

%build
mkdir build
cd build
cmake .. \
	-DCMAKE_INSTALL_PREFIX=/usr \
	-DCMAKE_VERBOSE_MAKEFILE=OFF \
	-DWITH_TESTS=OFF \
	-DWITH_XC_HTTP=ON \
	-DWITH_XC_AUTOTYPE=ON
 
make %{?_smp_mflags}
 
%install
cd build
make install DESTDIR=%{buildroot}
 
desktop-file-install \
	--dir %{buildroot}%{_datadir}/applications \
	--delete-original \
	--add-mime-type application/x-keepass \
	%{buildroot}%{_datadir}/applications/%{name}.desktop
 
# Associate KDB* files
cat > x-keepassxc.desktop << EOF
[Desktop Entry]
Comment=
Hidden=false
Icon=keepassxc.png
MimeType=application/x-keepassxc
Patterns=*.kdb;*.KDB;*.kdbx;*.KDBX*
Type=MimeType
EOF
install -D -m 644 -p x-keepassxc.desktop \
	%{buildroot}%{_datadir}/mimelnk/application/x-keepassxc.desktop

%find_lang keepassx --with-qt

%check
ctest -V %{?_smp_mflags}

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
touch --no-create %{_datadir}/mime/packages &> /dev/null || :
update-desktop-database &> /dev/null ||:
 
%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    touch --no-create %{_datadir}/mime/packages &> /dev/null || :
    update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
fi
update-desktop-database &> /dev/null ||:

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
desktop-file-validate %{_datadir}/applications/keepassxc.desktop &> /dev/null || :

%files
%doc CHANGELOG
%license COPYING LICENSE*
%{_bindir}/keepassxc
%{_datadir}/keepassxc
%{_datadir}/applications/*.desktop
%{_datadir}/mimelnk/application/*.desktop
%{_datadir}/mime/packages/*.xml
%{_datadir}/icons/hicolor/*
%{_libdir}/keepassxc/*.so
 
%changelog
* Mon Feb 20 2017 Toni Spets <toni.spets@iki.fi> - 2.1.2-4
- Use official tar.xz as the source
- Depend on libgcrypt16 package on C7

* Fri Feb 17 2017 Bugzy Little <bugzylittle@gmail.com> - 2.1.2
- Fix conflict with keepassx by renaming mime

* Fri Feb 17 2017 Bugzy Little <bugzylittle@gmail.com> - 2.1.2
- Update to v2.1.2

* Mon Feb 13 2017 Bugzy Little <bugzylittle@gmail.com> - 2.1.1
- Update to v2.1.1
- Remove tests
- compile with autotype

* Mon Feb 13 2017 Bugzy Little <bugzylittle@gmail.com> - 2.1.0
- Update to v2.1.1

* Wed Feb 1 2017 Bugzy Little <bugzylittle@gmail.com> - 2.1.0
- Update to v2.1.0

* Mon Dec 19 2016 Bugzy Little <bugzylittle@gmail.com> - 2.0.3
- Initial build for keepassxc v2.0.3
- initial package
