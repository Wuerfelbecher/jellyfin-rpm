# unoffical jellyfin RPM

The RPM package for fedora requires some additional repos as dotnet and ffmpeg are not in the main repositories.

```shell
# dotnet required for runtime and building the RPM
$ sudo dnf copr enable @dotnet-sig/dotnet
# ffmpeg from RPMfusion free 
$ sudo dnf install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
```

## TODO
- [ ] CentOS/RHEL - Package
- [ ] OpenSUSE