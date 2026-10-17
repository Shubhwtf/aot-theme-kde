"""Wings of Freedom style emblem, drawn from scratch as SVG."""
import math

WHITE = "#efe6d4"
BLUE = "#3d6ea5"
BLUE_DARK = "#24466f"
WHITE_DARK = "#b9ad97"


def feather(root, angle, length, width, bend):
    """A single pointed feather blade growing from root at angle (degrees)."""
    rx, ry = root
    a = math.radians(angle)
    ux, uy = math.cos(a), -math.sin(a)
    nx, ny = -uy, ux
    tip = (rx + ux * length + nx * bend, ry + uy * length + ny * bend)
    c1 = (rx + ux * length * 0.35 + nx * width, ry + uy * length * 0.35 + ny * width)
    c2 = (rx + ux * length * 0.8 + nx * (width * 0.7 + bend), ry + uy * length * 0.8 + ny * (width * 0.7 + bend))
    c3 = (rx + ux * length * 0.75 - nx * width * 0.15 + nx * bend, ry + uy * length * 0.75 - ny * width * 0.15 + ny * bend)
    c4 = (rx + ux * length * 0.3 - nx * width * 0.35, ry + uy * length * 0.3 - ny * width * 0.35)
    f = lambda p: f"{p[0]:.1f},{p[1]:.1f}"
    return (f"M{f(root)} C{f(c1)} {f(c2)} {f(tip)} C{f(c3)} {f(c4)} {f(root)}Z")


def _mix(a, b, t):
    ca = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    cb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(ca, cb))


def _bez(p0, p1, p2, t):
    return ((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
            (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1])


def wing(root, span, height, n=10, mirror=False):
    """Feathers hang off a curved leading edge; returns (feather paths, arm path)."""
    sx = -1 if mirror else 1
    p0 = root
    p1 = (root[0] + sx * span * 0.15, root[1] - height * 1.05)
    p2 = (root[0] + sx * span, root[1] - height)
    paths = []
    for i in reversed(range(n)):
        t = 0.12 + 0.88 * i / (n - 1)
        r = _bez(p0, p1, p2, t)
        ang = -105 + 135 * t ** 1.15
        if mirror:
            ang = 180 - ang
        ln = span * (0.6 + 0.5 * t ** 1.2)
        wd = span * (0.2 + 0.06 * t)
        paths.append(feather(r, ang, ln, wd, sx * span * 0.05 if not mirror else -sx * span * 0.05))
    # arm / coverts band along the leading edge
    pts_top = [_bez(p0, p1, p2, k / 20) for k in range(21)]
    pts_bot = []
    for k in range(21):
        t = k / 20
        x, y = _bez(p0, p1, p2, t)
        th = span * 0.11 * (1 - t) ** 0.8 + span * 0.015
        pts_bot.append((x + sx * th * 0.35, y + th))
    f = lambda p: f"{p[0]:.1f},{p[1]:.1f}"
    arm = "M" + " L".join(f(p) for p in pts_top + list(reversed(pts_bot))) + "Z"
    return paths, arm


def emblem_svg_group(cx, cy, size, white=WHITE, blue=BLUE, shield=True,
                     shield_fill="#1a1613", shield_stroke="#c9a14a", glow=None):
    """Return an SVG <g> with the emblem centred at (cx, cy); size = total height."""
    s = size / 1000.0
    out = [f'<g transform="translate({cx},{cy}) scale({s:.4f})">']
    if shield:
        sh = ("M0,-500 C140,-470 300,-450 420,-455 C430,-150 400,180 0,500 "
              "C-400,180 -430,-150 -420,-455 C-300,-450 -140,-470 0,-500Z")
        if glow:
            out.append(f'<path d="{sh}" fill="none" stroke="{glow}" stroke-width="40" '
                       f'opacity="0.35" filter="url(#emblemGlow)"/>')
        out.append(f'<path d="{sh}" fill="{shield_fill}" stroke="{shield_stroke}" stroke-width="16"/>')
        inner = ("M0,-462 C130,-435 270,-418 384,-421 C392,-140 362,160 0,456 "
                 "C-362,160 -392,-140 -384,-421 C-270,-418 -130,-435 0,-462Z")
        out.append(f'<path d="{inner}" fill="none" stroke="{shield_stroke}" stroke-width="4" opacity="0.55"/>')
    # white wing sweeps left behind, blue wing sweeps right in front
    for col, dark, root, mirror in ((white, "#00000040", (46, 70), True),
                                    (blue, "#00000060", (-46, 112), False)):
        feathers, arm = wing(root, 228, 300, mirror=mirror)
        for i, d in enumerate(feathers):
            shade = _mix(col, "#000000", 0.18 * ((i + 1) % 2))
            out.append(f'<path d="{d}" fill="{shade}" stroke="{dark}" stroke-width="6" stroke-linejoin="round"/>')
        out.append(f'<path d="{arm}" fill="{col}" stroke="{dark}" stroke-width="6" stroke-linejoin="round"/>')
    out.append("</g>")
    return "\n".join(out)


def emblem_defs(blur=18):
    return (f'<filter id="emblemGlow" x="-50%" y="-50%" width="200%" height="200%">'
            f'<feGaussianBlur stdDeviation="{blur}"/></filter>')


def standalone(size=1024, shield=True, bg=None, **kw):
    bgrect = f'<rect width="{size}" height="{size}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
            f'viewBox="0 0 {size} {size}"><defs>{emblem_defs()}</defs>{bgrect}'
            f'{emblem_svg_group(size / 2, size / 2, size * 0.92, shield=shield, **kw)}</svg>')


if __name__ == "__main__":
    import sys
    open(sys.argv[1], "w").write(standalone())
