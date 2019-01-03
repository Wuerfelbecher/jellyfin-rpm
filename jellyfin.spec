%global debug_package %{nil}
Name:           jellyfin
Version:        3.5.2
Release:        1%{?dist}
Summary:        The Free Software Media Browser.
%global         upstream_version v%{version}-5
License:        GPLv2
URL:            https://jellyfin.media
Source0:        https://github.com/%{name}/%{name}/archive/%{upstream_version}.zip
Source1:        jellyfin.service
Source2:        jellyfin.env
Source3:        jellyfin.sudoers
Source4:        restart.sh

%{?systemd_requires}
BuildRequires:  systemd
Requires(pre):  shadow-utils
BuildRequires:  libcurl-devel, fontconfig-devel, freetype-devel, openssl-devel, glibc-devel
Requires:       libcurl, fontconfig, freetype, openssl, glibc
# Requirements not packaged in main repos
# COPR @dotnet-sig/dotnet
BuildRequires:  dotnet >= 2.1.302
Requires:       dotnet >= 2.1.302
# RPMfusion free
Requires:       ffmpeg

%description
Jellyfin is a free software media system that puts you in control of managing and streaming your media.


%prep
%autosetup

%build

%install
export DOTNET_CLI_TELEMETRY_OPTOUT=1
pushd jellyfin
    dotnet publish --configuration Release --output='%{buildroot}%{_libdir}/jellyfin' --self-contained --runtime linux-x64
    %{__install} -D -m 0644 LICENSE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE
    %{__install} -D -m 0644 debian/conf/jellyfin.service.conf %{buildroot}%{_sysconfdir}/systemd/system/%{name}.service.d/override.conf
popd
mkdir -p %{buildroot}%{_bindir}
tee %{buildroot}%{_bindir}/jellyfin << EOF
#!/bin/sh
dotnet_cmd=\$(command -v dotnet)
exec \$dotnet_cmd %{_libdir}/%{name}/%{name}.dll \${@}
EOF
mkdir -p %{buildroot}%{_sharedstatedir}/jellyfin
%{__install} -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
%{__install} -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%{__install} -D -m 0600 %{SOURCE3} %{buildroot}%{_sysconfdir}/sudoers.d/%{name}
%{__install} -D -m 0750 %{SOURCE4} %{buildroot}%{_libexecdir}/%{name}/restart.sh

%files
%{_libdir}/%{name}/dashboard-ui
%attr(755,root,root) %{_bindir}/%{name}
%attr(644,root,root) %{_libdir}/%{name}/*.json
%attr(644,root,root) %{_libdir}/%{name}/*.pdb
%attr(755,root,root) %{_libdir}/%{name}/*.dll
%attr(755,root,root) %{_libdir}/%{name}/*.so
%attr(755,root,root) %{_libdir}/%{name}/*.a
%attr(755,root,root) %{_libdir}/%{name}/createdump
%attr(755,root,root) %{_libdir}/%{name}/jellyfin
%attr(644,root,root) %{_libdir}/%{name}/sosdocsunix.txt
%attr(644,root,root) %{_unitdir}/%{name}.service
%attr(600,root,root) %{_sysconfdir}/sudoers.d/%{name}
%attr(750,root,root) %{_libexecdir}/%{name}/restart.sh
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/systemd/system/%{name}.service.d/override.conf

%attr(-,jellyfin,jellyfin) %dir %{_sharedstatedir}/jellyfin
%license LICENSE

%pre
getent group jellyfin >/dev/null || groupadd -r jellyfin
getent passwd jellyfin >/dev/null || \
    useradd -r -g jellyfin -d %{_sharedstatedir}/jellyfin -s /sbin/nologin \
    -c "Jellyfin default user" jellyfin
exit 0

%post
%systemd_post jellyfin.service

%preun
%systemd_preun jellyfin.service

%postun
%systemd_postun_with_restart jellyfin.service

%changelog
* Thu Jan 03 2019 Thomas Büttner <thomas@vergesslicher.tech> 3.5.2-1
- Initial RPM package
