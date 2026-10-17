#!/usr/bin/env bash
# Removes the Attack on Titan theme files and switches back to Breeze Dark.
# Your backups in ~/.aot-backup-* are left untouched.
set -euo pipefail
DATA="${XDG_DATA_HOME:-$HOME/.local/share}"
CONF="${XDG_CONFIG_HOME:-$HOME/.config}"

if [[ "${1:-}" == "--system" ]]; then
    [[ $EUID -eq 0 ]] || { echo "run with sudo"; exit 1; }
    rm -rf /usr/share/sddm/themes/AttackOnTitan /etc/sddm.conf.d/zz-attack-on-titan.conf
    if [[ -d /boot/grub/themes/AttackOnTitan ]]; then
        rm -rf /boot/grub/themes/AttackOnTitan
        sed -i 's|^GRUB_THEME="/boot/grub/themes/AttackOnTitan/theme.txt"|#GRUB_THEME="/path/to/gfxtheme"|' /etc/default/grub
        grub-mkconfig -o /boot/grub/grub.cfg
    fi
    if [[ -d /usr/share/plymouth/themes/attack-on-titan ]]; then
        plymouth-set-default-theme breeze 2>/dev/null || plymouth-set-default-theme bgrt || true
        rm -rf /usr/share/plymouth/themes/attack-on-titan
    fi
    exit 0
fi

plasma-apply-lookandfeel -a org.kde.breezedark.desktop >/dev/null 2>&1 || true
kwriteconfig6 --file kwinrc --group org.kde.kdecoration2 --key library org.kde.breeze
kwriteconfig6 --file kwinrc --group org.kde.kdecoration2 --key theme Breeze
[[ "$(kreadconfig6 --file kdeglobals --group KDE --key widgetStyle)" == kvantum ]] && \
    kwriteconfig6 --file kdeglobals --group KDE --key widgetStyle Breeze

rm -rf "$DATA/color-schemes/AttackOnTitan.colors" "$DATA/plasma/desktoptheme/AttackOnTitan" \
       "$DATA/plasma/look-and-feel/com.github.shubhwtf.attackontitan" "$DATA/aurorae/themes/AttackOnTitan" \
       "$DATA/icons/AttackOnTitan" "$DATA"/wallpapers/AttackOnTitan-* "$CONF/Kvantum/AttackOnTitan" \
       "$DATA/konsole/AttackOnTitan.colorscheme" "$DATA/konsole/AttackOnTitan.profile" \
       "$CONF/kitty/themes/attack-on-titan.conf" "$CONF/btop/themes/attack-on-titan.theme"
[[ -f "$CONF/kitty/kitty.conf" ]] && sed -i '/# Attack on Titan theme/d; /include themes\/attack-on-titan.conf/d' "$CONF/kitty/kitty.conf"
qdbus6 org.kde.KWin /KWin reconfigure >/dev/null 2>&1 || true
echo "Removed. Restore your old configs from ~/.aot-backup-* if you want them back."
