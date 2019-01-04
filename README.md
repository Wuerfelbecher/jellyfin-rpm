# unoffical jellyfin RPM

## ffmpeg

The RPM package for Fedora/CentOS requires some additional repos aa ffmpeg is not in the main repositories.

```shell
# ffmpeg from RPMfusion free
# Fedora
$ sudo dnf install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
# CentOS 7 
$ sudo yum localinstall --nogpgcheck https://download1.rpmfusion.org/free/el/rpmfusion-free-release-7.noarch.rpm
```

## In-App service control

A sample sudoers-policy is located at `/usr/share/jellyfin/jellyfin-sudoers` which you need to review and copy to `/etc/sudoers.d`.
Use `install -D -m 0600 -o root -g root /usr/share/jellyfin/jellyfin-sudoers /etc/sudoers.d/jellyfin-sudoers` for the right permissions.
Finally uncomment JELLYFIN_RESTART_OPT in /etc/sysconfig/jellyfin and restart the service.


## Building with dotnet

Jellyfin is build with `--self-contained` so no dotnet required for runtime.

```shell
# dotnet required for building the RPM
# Fedora
$ sudo dnf copr enable @dotnet-sig/dotnet
# CentOS
$ sudo rpm -Uvh https://packages.microsoft.com/config/rhel/7/packages-microsoft-prod.rpm
```

## TODO

- [x] CentOS/RHEL - Package
- [ ] OpenSUSE