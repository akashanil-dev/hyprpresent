-- hyprpresent: add to ~/.config/hypr/hyprland.lua, or a file it includes.

-- Watch for displays being plugged in, and keep their modes after config reloads.
hl.on("hyprland.start", function() hl.exec_cmd("hyprpresent-daemon") end)

-- The picker on SUPER + P, as on Windows. Remove the unbind if nothing else uses it.
hl.unbind("SUPER + P")
hl.bind("SUPER + P", hl.dsp.exec_cmd("hyprpresent pick"))
