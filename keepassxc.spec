Name: keepassxc
Version: 2.3.1
Release: 0%{?dist}
Summary: Cross-platform password manager
Group: User Interface/Desktops
License: Boost and BSD and CC0 and GPLv3 and LGPLv2 and LGPLv2+ and LGPLv3+ and Public Domain
URL: https://keepassxc.org/
Source0: https://github.com/keepassxreboot/keepassxc/releases/download/%{version}/keepassxc-%{version}-src.tar.xz
BuildRequires:  desktop-file-utils
BuildRequires:  qt5-qtbase-devel >= 5.2
BuildRequires:  qt5-qttools-devel >= 5.2
BuildRequires:  libXi-devel
BuildRequires:  libXtst-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  zlib-devel
BuildRequires:  libyubikey-devel
BuildRequires:  ykpers-devel
BuildRequires:  libgcrypt-devel >= 1.6
BuildRequires:  libargon2-devel
BuildRequires:  libcurl-devel
BuildRequires:  cmake >= 3.1


%description
KeePassXC is a community fork of KeePassX
KeePassXC is an application for people with extremely high demands on secure
personal data management.
KeePassXC saves many different information e.g. user names, passwords, urls,
attachemts and comments in one single database. For a better management
user-defined titles and icons can be specified for each single entry.
Furthermore the entries are sorted in groups, which are customizable as well.
The integrated search function allows to search in a single group or the
complete database.
KeePassXC offers a little utility for secure password generation. The password
generator is very customizable, fast and easy to use. Especially someone who
generates passwords frequently will appreciate this feature.
The complete database is always encrypted either with AES (alias Rijndael) or
Twofish encryption algorithm using a 256 bit key. Therefore the saved
information can be considered as quite safe.

%global debug_package %{nil} 
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
	-DWITH_XC_YUBIKEY=ON \
	-DWITH_XC_AUTOTYPE=ON \
	-DCMAKE_BUILD_TYPE=Release
 
make %{?_smp_mflags}
 
%install
cd build
make install DESTDIR=%{buildroot}
 
desktop-file-install \
	--dir %{buildroot}%{_datadir}/applications \
	--delete-original \
	--add-mime-type application/x-keepassxc \
	%{buildroot}%{_datadir}/applications/org.keepassxc.KeePassXC.desktop
 
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
update-desktop-database &> /dev/null ||:
 
%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null ||:

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
desktop-file-validate %{_datadir}/applications/org.keepassxc.KeePassXC.desktop &> /dev/null || :

%files
%doc CHANGELOG
%license COPYING LICENSE*
%{_bindir}/keepassxc
%{_bindir}/keepassxc-cli
%{_datadir}/keepassxc
%{_datadir}/applications/*.desktop
%{_datadir}/mimelnk/application/*.desktop
%{_datadir}/mime/packages/*.xml
%{_datadir}/metainfo/*.xml
%{_datadir}/icons/hicolor/*
%{_mandir}/man1/keepassxc-cli.1.gz
%{_libdir}/keepassxc/*.so
 
%changelog
* Tue Mar 06 2018 Bugzy Little <bugzylittle@gmail.com> - 2.3.1-0
- Update to v2.3.1

* Fri Dec 15 2017 Bugzy Little <bugzylittle@gmail.com> - 2.2.4-0
- Update to v2.2.4

* Sun Oct 22 2017 Bugzy Little <bugzylittle@gmail.com> - 2.2.2-0
- Update to v2.2.2

* Sun Oct 01 2017 Bugzy Little <bugzylittle@gmail.com> - 2.2.1-0
- Update to v2.2.1

* Sun Jun 25 2017 Bugzy Little <bugzylittle@gmail.com> - 2.2.0-0
- Update to v2.2.0

* Sun Apr 9 2017 Bugzy Little <bugzylittle@gmail.com> - 2.1.4-0
- Change discription to match official package
- Modifying release tag so that there is no conflict with official package

* Sun Apr 9 2017 Bugzy Little <bugzylittle@gmail.com> - 2.1.4-1
- Update to v2.1.4

* Fri Feb 24 2017 Bugzy Little <bugzylittle@gmail.com> - 2.1.3-1
- Update to v2.1.3

* Fri Feb 24 2017 Bugzy Little <bugzylittle@gmail.com> - 2.1.2-5
- Fix if conditions
- trigger update

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
