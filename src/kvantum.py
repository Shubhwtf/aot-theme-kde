"""Kvantum theme: KvArcDark (GPL, by Tsu Jan) re-forged in Survey Corps colours.

usage: kvantum.py <repo root> [/usr/share/Kvantum/KvArcDark]
"""
import colorsys
import os
import re
import sys

NAME = "AttackOnTitan"
ACCENTS = {  # blue/purple accents -> crimson / brass
    "#5294e2": "#b8302a", "#58acff": "#d23a2f", "#4693e6": "#a8211b", "#3176bf": "#8f2420",
    "#009dff": "#7fa8d4", "#b74aff": "#c9a14a", "#9e4fff": "#c07a9a",
}
GENERAL = {
    "window.color": "#141110", "base.color": "#110f0d", "alt.base.color": "#161311",
    "button.color": "#231e1a", "light.color": "#3a322b", "mid.light.color": "#2a241f",
    "dark.color": "#070605", "mid.color": "#0c0a09", "highlight.color": "#a8211b",
    "inactive.highlight.color": "#5e1410", "text.color": "#e8dcc4", "window.text.color": "#e8dcc4",
    "button.text.color": "#e8dcc4", "disabled.text.color": "#e8dcc473", "tooltip.text.color": "#e8dcc4",
    "highlight.text.color": "#fff6e6", "link.color": "#7fa8d4", "link.visited.color": "#c07a9a",
    "progress.indicator.text.color": "#fff6e6",
}


def warm(hexcol):
    low = hexcol.lower()
    if low in ACCENTS:
        return ACCENTS[low]
    r, g, b = (int(low[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    if s > 0.45 and l > 0.2 and l < 0.8:  # stray saturated colour: pull toward crimson
        h, s = 0.01, 0.62
    elif l < 0.5:
        l = max(0.02, (l - 0.2) * 0.75 + 0.07) if l > 0.12 else l * 0.6
        h, s = 0.07, 0.16
    else:
        h, s = 0.11, 0.38
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return "#%02x%02x%02x" % (round(r * 255), round(g * 255), round(b * 255))


def main(root, src="/usr/share/Kvantum/KvArcDark"):
    out = os.path.join(root, "kvantum", NAME)
    os.makedirs(out, exist_ok=True)
    svg = open(os.path.join(src, "KvArcDark.svg")).read()
    svg = re.sub(r"#[0-9a-fA-F]{6}\b", lambda m: warm(m.group(0)), svg)
    open(os.path.join(out, f"{NAME}.svg"), "w").write(svg)

    cfg = open(os.path.join(src, "KvArcDark.kvconfig")).read()
    cfg = re.sub(r"#[0-9a-fA-F]{6}\b", lambda m: warm(m.group(0)), cfg)
    for k, v in GENERAL.items():
        cfg = re.sub(rf"(?m)^{re.escape(k)}=.*$", f"{k}={v}", cfg)
    cfg = re.sub(r"(?m)^blur_translucent=.*$", "blur_translucent=true", cfg)
    cfg = re.sub(r"(?m)^(text\.(normal|focus|press|toggle)\.color)=white$", r"\1=#e8dcc4", cfg)
    header = "# Attack on Titan Kvantum theme, derived from KvArcDark by Tsu Jan (GPL-3.0)\n"
    open(os.path.join(out, f"{NAME}.kvconfig"), "w").write(header + cfg)


if __name__ == "__main__":
    main(*sys.argv[1:])
