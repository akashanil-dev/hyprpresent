# hyprpresent

Windows-style projector modes (Win + P) for [Hyprland](https://hypr.land). Plug
in a projector or TV, press `SUPER + P`, pick a mode from your launcher.
Duplicate never stretches, nothing ever reloads your config, and the display
you plugged in keeps its mode the next time.

| Mode | What you get |
|---|---|
| **1 Laptop screen only** | The external display shows a card: your name, site, a QR code and the time. |
| **2 Duplicate** | The external shows your laptop screen, scaled to fit with black bars. Nothing is stretched, and neither screen changes resolution. |
| **3 Extend** | A second desktop to the left, right, above or below. |
| **4 Second screen only** | The laptop screen is turned off. |
| **5 Match the TV** | Like Duplicate, but no black bars: the laptop's desktop shrinks to the TV's shape, flush with the bottom of the screen, and exactly that part fills the TV. |

It also switches where the sound goes, sets the brightness of monitors that
take DDC/CI, and can show the mode in Waybar. It's a few shell scripts and
small tools; there's no toolkit to install.

On [Omarchy](https://omarchy.org), use the
[Present the Screen](https://github.com/akashanil-dev/omarchy-present) plugin
instead: the same modes with a graphical picker and a bar icon. Don't run both.

## Why

Presenting from Hyprland usually goes wrong in a few ways:

- **Mirroring stretches.** Hyprland's `mirror` copies your laptop's pixels onto
  the other display as they are, so a 16:10 laptop on a 16:9 projector comes out
  squashed. hyprpresent's Duplicate keeps each display at its own native
  resolution and letterboxes your screen instead, the way Windows does.
- **Text is tiny or huge.** Hyprland's `auto` scale guesses from the physical
  size the display reports, which TVs and projectors often get wrong.
  hyprpresent scales every display so it looks like a 1080p screen: 4K → 2,
  1440p → 1.33, 1080p or lower → 1.
- **Switching drops the TV.** Some TVs answer a config reload's extra modeset by
  dropping off HDMI until they're power-cycled. hyprpresent changes displays at
  runtime and never reloads the config to switch.

## Requirements

- **Hyprland 0.55 or newer, with a Lua config** (`~/.config/hypr/hyprland.lua`).
  hyprpresent applies its display rules with `hyprctl eval`, which only exists
  under a Lua config. On an older Hyprland, or with a `hyprland.conf`, it stops
  and says so. Run `hyprpresent check` to see.
- `bash`, `jq`, `socat` and `util-linux` (for `flock`)
- [`wl-mirror`](https://github.com/Ferdi265/wl-mirror), for Duplicate and
  Match the TV. The other modes work without it.
- A launcher with a dmenu mode, for the picker: `fuzzel`, `walker`, `wofi`,
  `rofi`, `tofi`, `bemenu` or `wmenu`. The first one installed is used, or set
  your own (see [The picker](#the-picker)).

Optional:

| Package | For |
|---|---|
| `swaybg` | The card in Laptop screen only. Without it the display still stays on, showing your wallpaper. |
| `librsvg` (`rsvg-convert`) | The card's text and QR code. Without it the card is a plain colour. |
| `qrencode` | The QR code on the card |
| `libpulse` (`pactl`) | Switching the sound output. Already there on PipeWire and PulseAudio desktops. |
| `ddcutil` | Brightness of monitors that take DDC/CI. Needs the `i2c-dev` kernel module: `echo i2c-dev \| sudo tee /etc/modules-load.d/i2c-dev.conf`, then reboot. |
| `libnotify` (`notify-send`) | Notifications when a mode changes or something fails |
| `waybar` | Showing the mode in the bar |

On Arch, everything except a launcher:

```bash
sudo pacman -S --needed jq socat wl-mirror swaybg librsvg qrencode libpulse libnotify
```

On Fedora (Hyprland itself comes from a COPR, see below):

```bash
sudo dnf install jq socat wl-mirror swaybg librsvg2-tools qrencode pulseaudio-utils libnotify
```

## Install

On Arch, build the package from this repository's PKGBUILD (an AUR package
will follow; AUR registration is paused for now):

```bash
git clone https://github.com/akashanil-dev/hyprpresent.git
cd hyprpresent/packaging
makepkg -si
```

On Fedora 43 or newer, from the release's RPM. Hyprland isn't in Fedora's own
repositories; [sdegler/hyprland](https://copr.fedorainfracloud.org/coprs/sdegler/hyprland/)
has current versions:

```bash
sudo dnf copr enable sdegler/hyprland     # skip if you already have Hyprland 0.55+
sudo dnf install https://github.com/akashanil-dev/hyprpresent/releases/download/v1.0.0/hyprpresent-1.0.0-1.fc44.noarch.rpm
sudo dnf install fuzzel                   # or another launcher, for the picker
```

Or from a checkout:

```bash
git clone https://github.com/akashanil-dev/hyprpresent.git
cd hyprpresent
sudo make install            # into /usr/local; PREFIX=~/.local make install for just you
```

## Setup

Add two lines to your Hyprland config, `~/.config/hypr/hyprland.lua` or a file
it includes:

```lua
hl.on("hyprland.start", function() hl.exec_cmd("hyprpresent-daemon") end)
hl.bind("SUPER + P", hl.dsp.exec_cmd("hyprpresent pick"))
```

`SUPER + P` matches Windows. If your config already binds it (Hyprland's
example config uses it for "pseudo"), add `hl.unbind("SUPER + P")` before the
`hl.bind` line, or pick another key.

The daemon starts with your next login. To start it now without logging out:

```bash
setsid -f hyprpresent-daemon
```

## What happens when you plug in

- **A display seen before** gets its saved mode, position and size back.
- **A new display** starts in Duplicate and the picker opens.
- **Unplugging** returns everything to the laptop screen, including turning it
  back on after Second screen only.
- **Closing the lid** in Duplicate, if your setup turns the laptop screen off
  then, makes the external your main screen; opening it goes back to Duplicate.

While Duplicate is on, the session doesn't go idle, so a talk isn't
interrupted by your screen locker. Locking by hand still works.

A display whose native mode is below 50Hz (a TV's 4K@30, for example) is
driven at its largest mode of 50Hz or more instead.

## The picker

`hyprpresent pick` lists the modes in your launcher, with a ✓ next to the
current one. Type a number (`2`) to jump to a mode. Below the modes:

- **Extend direction…**: where an extended display sits.
- **Size…**: bigger, smaller, or back to the automatic size. The menu comes
  back after each step until you close it.
- **Sound…**: every sound output that's plugged in, named after the display for
  HDMI. Your choice is remembered for that display.
- **Brightness…**: only for monitors that take DDC/CI (most TVs don't).
- **Don't manage this display**: hands it back to your own Hyprland config, for
  a desk monitor you've already set up.

To use a launcher hyprpresent doesn't know, or other options for one it does,
set `menu` in `~/.config/hyprpresent/config.json` (or `$HYPRPRESENT_MENU`). It
gets the entries on stdin and prints the chosen one; `$HYPRPRESENT_PROMPT`
holds the title:

```json
{ "menu": "fuzzel --dmenu --width 40 --prompt \"$HYPRPRESENT_PROMPT: \"" }
```

Everything is also a command:

```bash
hyprpresent set duplicate       # duplicate | match | extend | external | internal | ignore
hyprpresent position up         # right | left | up | down
hyprpresent scale up            # up | down | reset
hyprpresent audio               # sound outputs as JSON
hyprpresent audio set '<id>'
hyprpresent brightness down     # up | down | reset
hyprpresent title "Back at 3:15"
hyprpresent status              # the display and its saved mode, as JSON
```

## Match the TV

The laptop panel keeps its native resolution (laptop panels take no other), but
a strip at the top is reserved so the desktop below it has the TV's shape: on a
16:10 laptop and a 16:9 TV, about a tenth of the height. A top bar sits in that
strip, so it doesn't show on the TV. A window that goes fullscreen is held
inside the shaped area, while the app still behaves as fullscreen, so slides
fill the TV. Choosing another mode or unplugging gives the laptop its full
height back. With a projector narrower than the laptop (4:3), Match the TV
works like Duplicate.

## The card

In **Laptop screen only** the projector keeps its signal and shows a card,
instead of being switched off. Some TVs drop off HDMI when their signal stops
and stay gone until power-cycled; this way they never do, and switching back is
instant. Set it up under `card` in `~/.config/hyprpresent/config.json`:

```json
{
  "card": {
    "name": "Your Name",
    "site": "example.dev",
    "title": "",
    "clock": true
  }
}
```

| Key | Shows |
|---|---|
| `title` | A line above your name, for the room: "Back at 3:15", the talk's title. `hyprpresent title` sets it. |
| `name` | Your name, large |
| `site` | Under your name, and as a QR code to `https://` that site |
| `qr` | A different link for the QR code; `""` for none |
| `clock` | The time and date in the corner (`false` to hide) |
| `clock24` | `true` or `false` to force a 24- or 12-hour clock; by default your locale decides |
| `background`, `foreground`, `accent` | Colours, as `#rrggbb` |
| `font` | A font family; `sans-serif` by default |

Changes show up within a couple of seconds. With no `card` settings, the card
is a large clock. It's redrawn every minute, and drifts a few pixels each time
so nothing burns into a TV left on all day.

## Waybar

```jsonc
"custom/hyprpresent": {
  "exec": "hyprpresent status --waybar",
  "return-type": "json",
  "interval": 5,
  "format": "{}",
  "on-click": "hyprpresent pick"
}
```

The module shows the mode while an external display is connected and hides
otherwise. Its CSS class is the mode (`#custom-hyprpresent.duplicate`, ...).
[contrib/waybar-module.jsonc](contrib/waybar-module.jsonc) has a version with
icons.

## How it works

- **No config files are edited.** Display rules are applied at runtime with
  `hyprctl eval`. A config reload drops them, and the daemon applies them again
  right after.
- **Duplicate and Match the TV** use wl-mirror. The external display runs at its
  native mode, placed far away from the laptop display so the cursor and new
  windows can't land on it, and wl-mirror fills it on a workspace of its own
  (`hyprpresent`), so your numbered workspaces stay on the laptop. If wl-mirror
  exits unexpectedly, it's restarted.
- **The laptop screen** is switched off and on at runtime, never with a config
  reload. A config reload turns it back on; the daemon turns it off again if
  Second screen only is still chosen.
- **A mode is only saved once it works.** If the display drops out while
  switching, hyprpresent goes back to the previous mode and says so, rather than
  restoring a broken one at the next plug-in.
- **Displays are matched by connector** (`HDMI-A-1`, `DP-2`, ...). A TV that
  comes up without its name (its EDID read failed) keeps the mode last used on
  that port, and the laptop screen stays on until it reports a usable mode.
- **The daemon** listens on Hyprland's event socket with `socat` for displays
  being added or removed, config reloads and fullscreen windows. It waits for a
  burst of events to settle before acting.

Files it writes:

| Path | Contents |
|---|---|
| `~/.local/state/hyprpresent/displays.json` | Each display's saved mode, position, size, sound output and brightness |
| `~/.local/state/hyprpresent/hyprpresent.log` | What happened and when, trimmed to a few hundred lines |
| `$XDG_RUNTIME_DIR/hyprpresent/` | Locks, the rules applied in this session, and the card's images |

It reads `~/.config/hyprpresent/config.json`, and `hyprpresent title` writes to
it. Choosing a sound output changes the default output (and if needed the sound
card's profile) through PipeWire or PulseAudio.

Nothing runs as root, and nothing reaches the network.

## Troubleshooting

- **"hyprpresent needs Hyprland 0.55 or newer with a Lua config".** Your
  Hyprland is older, or it's reading `hyprland.conf`. Hyprland 0.55+ uses
  `hyprland.lua` when it exists; see Hyprland's wiki for moving your config.
- **Nothing happens when you plug in.** Check the daemon is running:
  `pgrep -af hyprpresent-daemon`. Start it by hand to see any error:
  `hyprpresent-daemon`.
- **Something looks wrong on a projector.** Look at `hyprpresent.log` (see
  above) and include it in an issue.
- **The TV isn't detected, or hyprpresent says no display is connected while
  one is plugged in.** Run `journalctl -k | grep -i hpd`. A line like `HPD
  interrupt storm detected on connector HDMI-A-1` means the TV flapped its
  connection and the graphics driver stopped listening to it. Turn the TV off at
  the wall for ten seconds and plug it back in, or suspend and resume.
- **A desk monitor lost its custom layout.** Open the picker with that monitor
  connected and choose **Don't manage this display**.

## Remove

```bash
sudo make uninstall          # or: sudo pacman -R hyprpresent, or: sudo dnf remove hyprpresent
rm -rf ~/.local/state/hyprpresent ~/.config/hyprpresent
hyprctl reload
```

Then delete the two lines from your Hyprland config. The reload drops any
display rules hyprpresent applied.

## Development

`bin/hyprpresent` holds all the logic and `bin/hyprpresent-daemon` reacts to
Hyprland's events. To try it without a second display, create a virtual one
with a connector-like name, which hyprpresent counts like a real display:

```bash
hyprctl output create headless HDMI-A-9
# ...
hyprctl output remove HDMI-A-9
```

Virtual outputs with other names (`HEADLESS-2`) only count after
`touch ~/.local/state/hyprpresent/include-headless`.

## License

[MIT](LICENSE)
