"""Aurorae window decoration: dark leather titlebar, crimson accent, diamond buttons."""
import os
import sys

NAME = "AttackOnTitan"
P = 18          # shadow padding
R = 9           # corner radius
B = 1           # side/bottom border
TOP_EDGE, TITLE, BOTTOM_EDGE = 5, 24, 5
T = TOP_EDGE + TITLE + BOTTOM_EDGE
LW = P + R      # width of left/right column elements
BH = P + R      # height of bottom row elements
BTN = 18

PAL = {
    "active": dict(top="#211c18", bot="#171310", line="#a8211b", hi="#c9a14a", border="#2e2722", body="#141110"),
    "inactive": dict(top="#16130f", bot="#120f0d", line="#2e2722", hi="#3a322b", border="#211c18", body="#110f0d"),
}


def shadow_defs():
    return ('<radialGradient id="sc" r="1" cx="1" cy="1">'
            '<stop offset="0" stop-color="#000" stop-opacity=".55"/>'
            '<stop offset=".35" stop-color="#000" stop-opacity=".22"/>'
            '<stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>'
            '<radialGradient id="sc2" r="1" cx="0" cy="1">'
            '<stop offset="0" stop-color="#000" stop-opacity=".55"/>'
            '<stop offset=".35" stop-color="#000" stop-opacity=".22"/>'
            '<stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>'
            '<radialGradient id="sc3" r="1" cx="1" cy="0">'
            '<stop offset="0" stop-color="#000" stop-opacity=".55"/>'
            '<stop offset=".35" stop-color="#000" stop-opacity=".22"/>'
            '<stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>'
            '<radialGradient id="sc4" r="1" cx="0" cy="0">'
            '<stop offset="0" stop-color="#000" stop-opacity=".55"/>'
            '<stop offset=".35" stop-color="#000" stop-opacity=".22"/>'
            '<stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>'
            '<linearGradient id="sl" x1="1" x2="0"><stop offset="0" stop-color="#000" stop-opacity=".55"/>'
            '<stop offset=".35" stop-color="#000" stop-opacity=".22"/><stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>'
            '<linearGradient id="sr" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity=".55"/>'
            '<stop offset=".35" stop-color="#000" stop-opacity=".22"/><stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>'
            '<linearGradient id="st" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#000" stop-opacity=".4"/>'
            '<stop offset=".35" stop-color="#000" stop-opacity=".15"/><stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>'
            '<linearGradient id="sb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".6"/>'
            '<stop offset=".35" stop-color="#000" stop-opacity=".25"/><stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>')


def frame(prefix, ox, oy, c, shadow=True):
    """Nine-slice frame laid out at (ox, oy). prefix e.g. 'decoration' or 'decoration-inactive'."""
    p = P if shadow else 0
    r = R if shadow else 0
    lw = p + (R if shadow else B)
    bh = p + (R if shadow else B)
    top_h = p + T
    mid = 40
    out = []
    gid = f"tb-{prefix}"
    out.append(f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
               f'<stop offset="{p / top_h:.4f}" stop-color="{c["top"]}"/>'
               f'<stop offset="1" stop-color="{c["bot"]}"/></linearGradient>')
    xs = [ox, ox + lw, ox + lw + mid]
    ys = [oy, oy + top_h, oy + top_h + mid]
    ws = [lw, mid, lw]
    hs = [top_h, mid, bh]
    names = [["topleft", "top", "topright"], ["left", "center", "right"], ["bottomleft", "bottom", "bottomright"]]
    for row in range(3):
        for col in range(3):
            x, y, w, h = xs[col], ys[row], ws[col], hs[row]
            nm = names[row][col]
            g = [f'<g id="{prefix}-{nm}">',
                 f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none"/>']
            # shadow
            if shadow:
                if nm == "topleft":
                    g.append(f'<rect x="{x}" y="{y + p}" width="{p}" height="{h - p}" fill="url(#sl)"/>')
                    g.append(f'<rect x="{x}" y="{y}" width="{w}" height="{p}" fill="url(#sc)"/>')
                elif nm == "topright":
                    g.append(f'<rect x="{x + w - p}" y="{y + p}" width="{p}" height="{h - p}" fill="url(#sr)"/>')
                    g.append(f'<rect x="{x}" y="{y}" width="{w}" height="{p}" fill="url(#sc2)"/>')
                elif nm == "top":
                    g.append(f'<rect x="{x}" y="{y}" width="{w}" height="{p}" fill="url(#st)"/>')
                elif nm == "left":
                    g.append(f'<rect x="{x}" y="{y}" width="{p}" height="{h}" fill="url(#sl)"/>')
                elif nm == "right":
                    g.append(f'<rect x="{x + w - p}" y="{y}" width="{p}" height="{h}" fill="url(#sr)"/>')
                elif nm == "bottom":
                    g.append(f'<rect x="{x}" y="{y + h - p}" width="{w}" height="{p}" fill="url(#sb)"/>')
                elif nm == "bottomleft":
                    g.append(f'<rect x="{x}" y="{y}" width="{p}" height="{h - p}" fill="url(#sl)"/>')
                    g.append(f'<rect x="{x}" y="{y + h - p}" width="{w}" height="{p}" fill="url(#sc3)"/>')
                elif nm == "bottomright":
                    g.append(f'<rect x="{x + w - p}" y="{y}" width="{p}" height="{h - p}" fill="url(#sr)"/>')
                    g.append(f'<rect x="{x}" y="{y + h - p}" width="{w}" height="{p}" fill="url(#sc4)"/>')
            # window body
            if row == 0:
                if col == 0:
                    d = (f"M{x + p},{y + h} V{y + p + r} A{r},{r} 0 0 1 {x + p + r},{y + p} H{x + w} V{y + h} Z")
                    g.append(f'<path d="{d}" fill="{c["border"]}"/>')
                    d = (f"M{x + p + B},{y + h} V{y + p + r} A{r - B},{r - B} 0 0 1 {x + p + r},{y + p + B} H{x + w} V{y + h} Z")
                    g.append(f'<path d="{d}" fill="url(#{gid})"/>')
                    g.append(f'<path d="M{x + p + r * 0.3:.1f},{y + p + r * 0.3:.1f} A{r},{r} 0 0 1 {x + p + r},{y + p} H{x + w}" '
                             f'stroke="{c["line"]}" stroke-width="2" fill="none"/>')
                elif col == 2:
                    d = (f"M{x},{y + h} V{y + p} H{x + w - p - r} A{r},{r} 0 0 1 {x + w - p},{y + p + r} V{y + h} Z")
                    g.append(f'<path d="{d}" fill="{c["border"]}"/>')
                    d = (f"M{x},{y + h} V{y + p + B} H{x + w - p - r} A{r - B},{r - B} 0 0 1 {x + w - p - B},{y + p + r} V{y + h} Z")
                    g.append(f'<path d="{d}" fill="url(#{gid})"/>')
                    g.append(f'<path d="M{x},{y + p} H{x + w - p - r} A{r},{r} 0 0 1 {x + w - p - r * 0.3:.1f},{y + p + r * 0.3:.1f}" '
                             f'stroke="{c["line"]}" stroke-width="2" fill="none"/>')
                else:
                    g.append(f'<rect x="{x}" y="{y + p}" width="{w}" height="{h - p}" fill="{c["border"]}"/>')
                    g.append(f'<rect x="{x}" y="{y + p + B}" width="{w}" height="{h - p - B}" fill="url(#{gid})"/>')
                    g.append(f'<rect x="{x}" y="{y + p}" width="{w}" height="2" fill="{c["line"]}"/>')
                    g.append(f'<rect x="{x}" y="{y + p + 2}" width="{w}" height="1" fill="{c["hi"]}" opacity=".18"/>')
                # separator under the title
                sx0 = x + (p + B if col == 0 else 0)
                sx1 = x + w - (p + B if col == 2 else 0)
                g.append(f'<rect x="{sx0}" y="{y + h - 1}" width="{sx1 - sx0}" height="1" fill="#000" opacity=".45"/>')
            elif row == 1:
                if col == 0:
                    g.append(f'<rect x="{x + p}" y="{y}" width="{w - p}" height="{h}" fill="{c["border"]}"/>')
                    g.append(f'<rect x="{x + p + B}" y="{y}" width="{w - p - B}" height="{h}" fill="{c["body"]}"/>')
                elif col == 2:
                    g.append(f'<rect x="{x}" y="{y}" width="{w - p}" height="{h}" fill="{c["border"]}"/>')
                    g.append(f'<rect x="{x}" y="{y}" width="{w - p - B}" height="{h}" fill="{c["body"]}"/>')
                else:
                    g.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c["body"]}"/>')
            else:
                x0 = x + (p if col == 0 else 0)
                x1 = x + w - (p if col == 2 else 0)
                g.append(f'<rect x="{x0}" y="{y}" width="{x1 - x0}" height="{h - p}" fill="{c["border"]}"/>')
                ix0 = x + (p + B if col == 0 else 0)
                ix1 = x + w - (p + B if col == 2 else 0)
                g.append(f'<rect x="{ix0}" y="{y}" width="{ix1 - ix0}" height="{h - p - B}" fill="{c["body"]}"/>')
            g.append("</g>")
            out.append("".join(g))
    return "\n".join(out), (xs[2] + lw - ox, ys[2] + bh - oy)


def decoration_svg():
    parts = [shadow_defs()]
    oy = 0
    for prefix, pal, sh in (("decoration", "active", True), ("decoration-inactive", "inactive", True),
                            ("decoration-maximized", "active", False), ("decoration-maximized-inactive", "inactive", False)):
        s, (w, h) = frame(prefix, 0, oy, PAL[pal], sh)
        parts.append(s)
        oy += h + 20
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="200" height="{oy}" viewBox="0 0 200 {oy}">'
            f'<defs>{parts[0]}</defs>' + "".join(parts[1:]) + "</svg>")


# ---------------------------------------------------------------- buttons

BTN_COLORS = {"close": "#b8302a", "maximize": "#c9a14a", "restore": "#c9a14a", "minimize": "#4f8a5f",
              "alldesktops": "#4a78a8", "keepabove": "#8a7a68", "keepbelow": "#8a7a68",
              "shade": "#8a7a68", "help": "#8a7a68"}


def glyph(kind, cx, cy, col):
    s = 3.2
    st = f'stroke="{col}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" fill="none"'
    if kind == "close":
        return f'<path d="M{cx - s},{cy - s} L{cx + s},{cy + s} M{cx + s},{cy - s} L{cx - s},{cy + s}" {st}/>'
    if kind == "maximize":
        return f'<path d="M{cx - s},{cy + s * 0.6} L{cx},{cy - s * 0.7} L{cx + s},{cy + s * 0.6}" {st}/>'
    if kind == "restore":
        return f'<path d="M{cx},{cy - s} L{cx + s},{cy} L{cx},{cy + s} L{cx - s},{cy} Z" {st}/>'
    if kind == "minimize":
        return f'<path d="M{cx - s},{cy - s * 0.6} L{cx},{cy + s * 0.7} L{cx + s},{cy - s * 0.6}" {st}/>'
    if kind == "alldesktops":
        return f'<circle cx="{cx}" cy="{cy}" r="1.8" fill="{col}"/>'
    if kind in ("keepabove", "keepbelow"):
        dy = -1 if kind == "keepabove" else 1
        return (f'<path d="M{cx - s},{cy - dy * s * 0.2} L{cx},{cy + dy * -s} L{cx + s},{cy - dy * s * 0.2} '
                f'M{cx - s},{cy + dy * s * 0.9} L{cx},{cy - dy * s * 0.1} L{cx + s},{cy + dy * s * 0.9}" {st}/>')
    if kind == "shade":
        return f'<path d="M{cx - s},{cy - s * 0.5} H{cx + s}" {st}/>'
    return f'<text x="{cx}" y="{cy + 3}" font-size="8" text-anchor="middle" fill="{col}">?</text>'


def diamond(cx, cy, r, fill, stroke, sw=1.0, op=1.0):
    return (f'<path d="M{cx},{cy - r} L{cx + r},{cy} L{cx},{cy + r} L{cx - r},{cy} Z" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}" opacity="{op}"/>')


def button_svg(kind):
    col = BTN_COLORS[kind]
    states = []
    for i, st in enumerate(["active", "hover", "pressed", "inactive", "deactivated"]):
        x0 = i * (BTN + 4)
        cx, cy = x0 + BTN / 2, BTN / 2
        g = [f'<g id="{st}-center"><rect x="{x0}" y="0" width="{BTN}" height="{BTN}" fill="none"/>']
        if st == "active":
            g.append(diamond(cx, cy, 6.2, col, "#00000088"))
            g.append(diamond(cx, cy - 1.2, 3.2, "#ffffff", "none", op=0.12))
        elif st == "hover":
            g.append(diamond(cx, cy, 8.2, col, "#f6e7c8", 1.2))
            g.append(glyph(kind, cx, cy, "#1a1210"))
        elif st == "pressed":
            g.append(diamond(cx, cy, 7.4, "#5e1410" if kind == "close" else "#3a322b", col, 1.4))
            g.append(glyph(kind, cx, cy, "#f6e7c8"))
        elif st == "inactive":
            g.append(diamond(cx, cy, 5.6, "#3a322b", "#00000066"))
        else:
            g.append(diamond(cx, cy, 5.6, "#2a2420", "none", op=0.6))
        g.append("</g>")
        states.append("".join(g))
    w = 5 * (BTN + 4)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{BTN}" viewBox="0 0 {w} {BTN}">'
            + "".join(states) + "</svg>")


RC = f"""[General]
ActiveTextColor=232,220,196
InactiveTextColor=122,110,96
TitleAlignment=Center
TitleVerticalAlignment=Center
Animation=180
UseTextShadow=false
Shadow=false
DecorationPosition=0

[Layout]
BorderLeft={B}
BorderRight={B}
BorderBottom={B}
TitleEdgeTop={TOP_EDGE + 1}
TitleEdgeBottom={BOTTOM_EDGE - 1}
TitleEdgeLeft=10
TitleEdgeRight=10
TitleEdgeTopMaximized={TOP_EDGE + 1}
TitleEdgeBottomMaximized={BOTTOM_EDGE - 1}
TitleEdgeLeftMaximized=8
TitleEdgeRightMaximized=8
TitleBorderLeft=8
TitleBorderRight=8
TitleHeight={TITLE}
ButtonWidth={BTN}
ButtonHeight={BTN}
ButtonSpacing=6
ButtonMarginTop=3
ExplicitButtonSpacer=10
PaddingTop={P}
PaddingBottom={P}
PaddingLeft={P}
PaddingRight={P}
"""

METADATA = f"""[Desktop Entry]
Name=Attack on Titan
Comment=Survey Corps window decoration
X-KDE-PluginInfo-Author=Shubhwtf
X-KDE-PluginInfo-Name={NAME}
X-KDE-PluginInfo-Version=1.0
X-KDE-PluginInfo-License=GPLv3
X-KDE-PluginInfo-EnabledByDefault=true
X-Plasma-API=declarativeappletscript
"""


def main(root):
    d = os.path.join(root, "aurorae", NAME)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "decoration.svg"), "w").write(decoration_svg())
    for k in BTN_COLORS:
        open(os.path.join(d, f"{k}.svg"), "w").write(button_svg(k))
    open(os.path.join(d, f"{NAME}rc"), "w").write(RC)
    open(os.path.join(d, "metadata.desktop"), "w").write(METADATA)


if __name__ == "__main__":
    main(sys.argv[1])
