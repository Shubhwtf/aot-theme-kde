#!/usr/bin/env bash
# Attack on Titan theme for KDE Plasma 6 — installer
# https://github.com/Shubhwtf/aot-theme-kde
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA="${XDG_DATA_HOME:-$HOME/.local/share}"
CONF="${XDG_CONFIG_HOME:-$HOME/.config}"
LNF=com.github.shubhwtf.attackontitan
WALLPAPER=AttackOnTitan-WallMaria

red=$'\e[38;2;210;58;47m'; brass=$'\e[38;2;201;161;74m'; dim=$'\e[38;2;122;110;96m'; off=$'\e[0m'
say()  { printf '%s◆%s %s\n' "$red" "$off" "$*"; }
note() { printf '  %s%s%s\n' "$dim" "$*" "$off"; }

usage() {
    cat <<EOF
${brass}SHINZOU WO SASAGEYO${off} — Attack on Titan for KDE Plasma 6

usage: ./install.sh [options]

  (no option)      install every user-level component into ~/.local/share and ~/.config
  --apply          install, then switch the desktop to the theme (configs are backed up first)
  --kvantum        with --apply: use the Kvantum widget style instead of Breeze
  --wallpaper ID   with --apply: WallMaria | WingsOfFreedom | Rumbling | Paths (default WallMaria)
  --system         (run with sudo) install the SDDM, GRUB and Plymouth themes
  -h, --help       show this help
EOF
}

APPLY=0; KVANTUM=0; SYSTEM=0
while [[ $# -gt 0 ]]; do
    case "$1" in
        --apply) APPLY=1 ;;
        --kvantum) KVANTUM=1 ;;
        --wallpaper) WALLPAPER="AttackOnTitan-$2"; shift ;;
        --system) SYSTEM=1 ;;
        -h|--help) usage; exit 0 ;;
        *) usage; exit 1 ;;
    esac
    shift
done

copy_dir() {  # copy_dir <src> <dest-parent>; replaces only our own directory
    mkdir -p "$2"
    rm -rf "${2:?}/$(basename "$1")"
    cp -r "$1" "$2/"
}

# ------------------------------------------------------------------ system
install_system() {
    [[ $EUID -eq 0 ]] || { echo "--system needs root: sudo ./install.sh --system"; exit 1; }

    say "SDDM login theme"
    copy_dir "$SRC/sddm/AttackOnTitan" /usr/share/sddm/themes
    mkdir -p /etc/sddm.conf.d
    printf '[Theme]\nCurrent=AttackOnTitan\n' > /etc/sddm.conf.d/zz-attack-on-titan.conf

    if [[ -d /boot/grub ]]; then
        say "GRUB theme"
        copy_dir "$SRC/grub/AttackOnTitan" /boot/grub/themes
        cp -n /etc/default/grub /etc/default/grub.aot-backup || true
        if grep -q '^#\?GRUB_THEME=' /etc/default/grub; then
            sed -i 's|^#\?GRUB_THEME=.*|GRUB_THEME="/boot/grub/themes/AttackOnTitan/theme.txt"|' /etc/default/grub
        else
            echo 'GRUB_THEME="/boot/grub/themes/AttackOnTitan/theme.txt"' >> /etc/default/grub
        fi
        grub-mkconfig -o /boot/grub/grub.cfg
    else
        note "no /boot/grub, skipping GRUB"
    fi

    if command -v plymouth-set-default-theme >/dev/null; then
        say "Plymouth boot splash"
        copy_dir "$SRC/plymouth/attack-on-titan" /usr/share/plymouth/themes
        plymouth-set-default-theme attack-on-titan
        if grep -qE '^HOOKS=.*\bplymouth\b' /etc/mkinitcpio.conf 2>/dev/null; then
            mkinitcpio -P
        else
            note "add 'plymouth' to HOOKS in /etc/mkinitcpio.conf (after systemd/udev),"
            note "add 'splash' to your kernel cmdline, then run: sudo mkinitcpio -P"
        fi
    fi
    say "System themes installed."
}

# ------------------------------------------------------------------ user
install_user() {
    say "Fonts"
    mkdir -p "$DATA/fonts"
    cp "$SRC/fonts/Cinzel.ttf" "$DATA/fonts/"
    fc-cache -f "$DATA/fonts" >/dev/null 2>&1 || true

    say "Color scheme, Plasma style, global theme"
    mkdir -p "$DATA/color-schemes"
    cp "$SRC/color-schemes/AttackOnTitan.colors" "$DATA/color-schemes/"
    copy_dir "$SRC/plasma/desktoptheme/AttackOnTitan" "$DATA/plasma/desktoptheme"
    copy_dir "$SRC/plasma/look-and-feel/$LNF" "$DATA/plasma/look-and-feel"

    say "Window decoration"
    copy_dir "$SRC/aurorae/AttackOnTitan" "$DATA/aurorae/themes"

    say "Icons"
    copy_dir "$SRC/icons/AttackOnTitan" "$DATA/icons"

    say "Wallpapers"
    for w in "$SRC"/wallpapers/*/; do copy_dir "${w%/}" "$DATA/wallpapers"; done

    say "Kvantum"
    copy_dir "$SRC/kvantum/AttackOnTitan" "$CONF/Kvantum"

    say "Terminals"
    mkdir -p "$DATA/konsole" "$CONF/kitty/themes" "$CONF/btop/themes" "$CONF/neofetch"
    cp "$SRC/terminal/konsole/AttackOnTitan.colorscheme" "$SRC/terminal/konsole/AttackOnTitan.profile" "$DATA/konsole/"
    cp "$SRC/terminal/kitty/attack-on-titan.conf" "$CONF/kitty/themes/"
    cp "$SRC/terminal/btop/attack-on-titan.theme" "$CONF/btop/themes/"
    cp "$SRC/terminal/neofetch/aot.txt" "$CONF/neofetch/"
}

backup() {
    BK="$HOME/.aot-backup-$(date +%Y%m%d-%H%M%S)"
    mkdir -p "$BK"
    for f in kdeglobals kwinrc plasmarc ksplashrc kscreenlockerrc kcminputrc konsolerc \
             plasma-org.kde.plasma.desktop-appletsrc Kvantum kitty btop neofetch; do
        [[ -e "$CONF/$f" ]] && cp -a "$CONF/$f" "$BK/"
    done
    [[ -d "$DATA/konsole" ]] && cp -a "$DATA/konsole" "$BK/konsole-profiles"
    say "Backed up your configs to $BK"
}

apply_theme() {
    backup
    local kw=kwriteconfig6
    command -v $kw >/dev/null || kw=kwriteconfig5

    say "Applying global theme"
    plasma-apply-lookandfeel -a "$LNF" >/dev/null || true
    plasma-apply-colorscheme AttackOnTitan >/dev/null || true
    plasma-apply-desktoptheme AttackOnTitan >/dev/null || true
    $kw --file kdeglobals --group Icons --key Theme AttackOnTitan
    $kw --file kwinrc --group org.kde.kdecoration2 --key library org.kde.kwin.aurorae.v2
    $kw --file kwinrc --group org.kde.kdecoration2 --key theme __aurorae__svg__AttackOnTitan
    $kw --file ksplashrc --group KSplash --key Engine KSplashQML
    $kw --file ksplashrc --group KSplash --key Theme "$LNF"

    if [[ $KVANTUM -eq 1 ]]; then
        $kw --file kdeglobals --group KDE --key widgetStyle kvantum
        mkdir -p "$CONF/Kvantum"
        printf '[General]\ntheme=AttackOnTitan\n' > "$CONF/Kvantum/kvantum.kvconfig"
    fi

    say "Wallpaper + lock screen"
    local img="$DATA/wallpapers/$WALLPAPER/contents/images/3840x2160.jpg"
    plasma-apply-wallpaperimage "$img" >/dev/null || true
    $kw --file kscreenlockerrc --group Greeter --group Wallpaper --group org.kde.image --group General --key Image "file://$img"

    say "Terminals"
    local prof
    prof=$(kreadconfig6 --file konsolerc --group "Desktop Entry" --key DefaultProfile 2>/dev/null || true)
    if [[ -n "$prof" && -f "$DATA/konsole/$prof" && "$prof" != AttackOnTitan.profile ]]; then
        $kw --file "$DATA/konsole/$prof" --group Appearance --key ColorScheme AttackOnTitan
    else
        $kw --file konsolerc --group "Desktop Entry" --key DefaultProfile AttackOnTitan.profile
    fi
    if [[ -f "$CONF/kitty/kitty.conf" ]] && ! grep -q 'themes/attack-on-titan.conf' "$CONF/kitty/kitty.conf"; then
        printf '\n# Attack on Titan theme\ninclude themes/attack-on-titan.conf\n' >> "$CONF/kitty/kitty.conf"
        pkill -USR1 -x kitty 2>/dev/null || true
    fi
    if [[ -f "$CONF/btop/btop.conf" ]]; then
        sed -i 's|^color_theme = .*|color_theme = "attack-on-titan"|' "$CONF/btop/btop.conf"
    fi

    qdbus6 org.kde.KWin /KWin reconfigure >/dev/null 2>&1 || qdbus org.kde.KWin /KWin reconfigure >/dev/null 2>&1 || true
    say "Done. Dedicate your heart."
    note "Log out and back in once so every app picks up the new style."
    note "For the login screen, GRUB and boot splash: sudo ./install.sh --system"
}

if [[ $SYSTEM -eq 1 ]]; then
    install_system
    exit 0
fi

install_user
if [[ $APPLY -eq 1 ]]; then
    apply_theme
else
    note "Installed. Pick 'Attack on Titan' in System Settings › Colors & Themes, or run ./install.sh --apply"
fi
