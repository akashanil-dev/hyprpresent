PREFIX ?= /usr/local
DESTDIR ?=
BINDIR = $(DESTDIR)$(PREFIX)/bin
DOCDIR = $(DESTDIR)$(PREFIX)/share/doc/hyprpresent
LICENSEDIR = $(DESTDIR)$(PREFIX)/share/licenses/hyprpresent

.PHONY: install uninstall check

install:
	install -Dm755 bin/hyprpresent $(BINDIR)/hyprpresent
	install -Dm755 bin/hyprpresent-daemon $(BINDIR)/hyprpresent-daemon
	install -Dm644 README.md $(DOCDIR)/README.md
	install -Dm644 CHANGELOG.md $(DOCDIR)/CHANGELOG.md
	install -Dm644 contrib/hyprland.lua $(DOCDIR)/examples/hyprland.lua
	install -Dm644 contrib/waybar-module.jsonc $(DOCDIR)/examples/waybar-module.jsonc
	install -Dm644 contrib/config.json $(DOCDIR)/examples/config.json
	install -Dm644 LICENSE $(LICENSEDIR)/LICENSE

uninstall:
	rm -f $(BINDIR)/hyprpresent $(BINDIR)/hyprpresent-daemon
	rm -rf $(DOCDIR) $(LICENSEDIR)

check:
	bash -n bin/hyprpresent
	bash -n bin/hyprpresent-daemon
