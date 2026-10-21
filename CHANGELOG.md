# Changelog

## 1.0.0

First release: the projector modes of the
[Present the Screen](https://github.com/akashanil-dev/omarchy-present) Omarchy
plugin (1.1.2) for any Hyprland 0.55+ with a Lua config.

- Laptop screen only, Duplicate, Extend, Second screen only and Match the TV,
  plus where an extended display sits, its size, the sound output and DDC/CI
  brightness.
- `hyprpresent pick` shows them in fuzzel, walker, wofi, rofi, tofi, bemenu or
  wmenu, or any dmenu-style command.
- `hyprpresent-daemon` follows Hyprland's events with socat: saved modes come
  back on plug-in, a new display opens the picker, and runtime rules are
  re-applied after config reloads.
- The card in Laptop screen only is drawn as an SVG and shown with swaybg.
- `hyprpresent status --waybar` for a Waybar module.
- Changes from the plugin: no dimming layer (brightness is DDC/CI only), and
  only hyprpresent's own wl-mirror is ever stopped.
