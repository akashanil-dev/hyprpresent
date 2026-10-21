Name:           hyprpresent
Version:        1.0.0
Release:        1%{?dist}
Summary:        Windows-style projector modes (Win+P) for Hyprland

License:        MIT
URL:            https://github.com/akashanil-dev/hyprpresent
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make

Requires:       bash
Requires:       coreutils
Requires:       gawk
Requires:       jq
Requires:       procps-ng
Requires:       socat
Requires:       util-linux-core
Requires:       wl-mirror
# Not in Fedora's own repos: comes from a COPR (sdegler/hyprland) or a source
# build, so it's only recommended. `hyprpresent check` reports a version that
# is too old.
Recommends:     hyprland >= 0.55.0
Recommends:     swaybg
Recommends:     librsvg2-tools
Recommends:     qrencode
Recommends:     pulseaudio-utils
Suggests:       fuzzel
Suggests:       ddcutil
Suggests:       libnotify
Suggests:       waybar

%description
Duplicate without stretching, Extend, Second screen only, Laptop screen only
with a name card, and Match the TV, from a menu in your launcher. Saved modes
come back when a display is plugged in again, nothing reloads your Hyprland
config to switch, and the sound output and DDC/CI brightness can be changed too.
Needs Hyprland 0.55 or newer with a Lua config.

%prep
%autosetup -n %{name}-%{version}

%build
# Shell scripts: nothing to build.

%install
%make_install PREFIX=%{_prefix}

%files
%{_bindir}/hyprpresent
%{_bindir}/hyprpresent-daemon
%license %{_datadir}/licenses/%{name}/LICENSE
%doc %{_docdir}/%{name}/

%changelog
* Wed Oct 21 2026 Akash A <akashanil084@gmail.com> - 1.0.0-1
- First release
