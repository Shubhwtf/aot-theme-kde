"""Procedural Attack on Titan wallpapers: SVG scene -> rsvg-convert -> grain/vignette."""
import math
import os
import random
import subprocess
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from emblem import emblem_defs, emblem_svg_group  # noqa: E402

W, H = 3840, 2160
FONT = "Cinzel"


def svg(body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}"><defs>{defs}</defs>{body}</svg>')


def blur(fid, sd):
    return (f'<filter id="{fid}" x="-300%" y="-300%" width="700%" height="700%">'
            f'<feGaussianBlur stdDeviation="{sd}"/></filter>')


def lingrad(gid, stops, x2=0, y2=1):
    s = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
    return f'<linearGradient id="{gid}" x1="0" y1="0" x2="{x2}" y2="{y2}">{s}</linearGradient>'


def radgrad(gid, stops, cx=0.5, cy=0.5, r=0.5):
    s = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
    return f'<radialGradient id="{gid}" cx="{cx}" cy="{cy}" r="{r}">{s}</radialGradient>'


def steam(rng, cx, cy, spread_x, spread_y, n, rmin, rmax, color, op, fid="steam"):
    """Rising plume: puffs drift upward and widen with height."""
    out = []
    for _ in range(n):
        rise = abs(rng.gauss(0, spread_y))
        x = cx + rng.gauss(0, spread_x * (0.35 + rise / (spread_y * 2.5)))
        y = cy - rise
        r = rng.uniform(rmin, rmax) * (0.7 + rise / (spread_y * 2))
        out.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r:.0f}" ry="{r * 0.75:.0f}" fill="{color}" '
                   f'opacity="{op * rng.uniform(0.35, 1):.2f}" filter="url(#{fid})"/>')
    return "".join(out)


def titan_bust(cx, base, s):
    """Head-and-shoulders silhouette; base = y where shoulders are cut off."""
    def p(x, y):
        return f"{cx + x * s:.1f},{base + y * s:.1f}"
    return (f"M{p(-2.0, 0.2)} C{p(-1.8, -0.35)} {p(-1.1, -0.52)} {p(-0.58, -0.6)} "
            f"C{p(-0.44, -0.66)} {p(-0.42, -0.74)} {p(-0.47, -0.8)} "
            f"C{p(-0.5, -0.92)} {p(-0.52, -1.08)} {p(-0.56, -1.3)} "
            f"C{p(-0.6, -1.5)} {p(-0.52, -1.9)} {p(-0.3, -2.04)} "
            f"C{p(-0.15, -2.1)} {p(0.15, -2.1)} {p(0.3, -2.04)} "
            f"C{p(0.52, -1.9)} {p(0.6, -1.5)} {p(0.56, -1.3)} "
            f"C{p(0.52, -1.08)} {p(0.5, -0.92)} {p(0.47, -0.8)} "
            f"C{p(0.42, -0.74)} {p(0.44, -0.66)} {p(0.58, -0.6)} "
            f"C{p(1.1, -0.52)} {p(1.8, -0.35)} {p(2.0, 0.2)} Z")


def titan_body(cx, ground, h, rng):
    """Full standing figure silhouette, height h, feet at ground."""
    u = h / 8.0
    sway = rng.uniform(-0.12, 0.12)
    arm = rng.uniform(-0.15, 0.25)
    bulk = rng.uniform(0.9, 1.2)
    right = [(0.22, 6.95), (0.25, 6.7), (0.5, 6.62), (0.95 * bulk, 6.5),
             (1.25 * bulk, 6.42), (1.35 * bulk, 6.1), (1.3 * bulk, 5.8),
             (1.45 * bulk + arm, 5.0), (1.45 * bulk + arm, 4.3), (1.38 * bulk + arm, 3.6),
             (1.36 * bulk + arm, 3.1), (1.42 * bulk + arm, 2.8), (1.35 * bulk + arm, 2.5),
             (1.25 * bulk + arm, 2.4), (1.12 * bulk + arm, 2.5), (1.1 * bulk + arm, 2.75),
             (1.08 * bulk + arm, 3.2), (1.1 * bulk + arm * 0.6, 3.6), (1.05 * bulk + arm * 0.3, 4.2),
             (1.0 * bulk, 4.7), (0.98 * bulk, 5.0), (0.92 * bulk, 5.2),
             (0.8 * bulk, 4.6), (0.68 * bulk, 4.3), (0.7 * bulk, 3.9),
             (0.75 * bulk, 3.6), (0.8 * bulk, 3.3), (0.75 * bulk, 3.0),
             (0.72, 2.0), (0.62, 1.0), (0.58, -0.1), (0.4, -0.12), (0.2, -0.12), (0.12, -0.1),
             (0.15, 1.0), (0.12, 2.2), (0.0, 2.9)]

    def pt(x, y):
        return f"{cx + (x + sway * y) * u:.1f},{ground - y * u:.1f}"
    d = f"M{pt(*right[0])}"
    for i in range(1, len(right) - 2, 3):
        d += f" C{pt(*right[i])} {pt(*right[i + 1])} {pt(*right[i + 2])}"
    left = [(-x, y) for x, y in reversed(right)]
    for i in range(1, len(left) - 2, 3):
        d += f" C{pt(*left[i])} {pt(*left[i + 1])} {pt(*left[i + 2])}"
    d += "Z"
    hx, hy = pt(0, 7.45).split(",")
    return (f'<path d="{d}"/><ellipse cx="{hx}" cy="{hy}" rx="{0.42 * u:.1f}" ry="{0.56 * u:.1f}"/>'
            f'<path d="M{pt(-0.24, 7.0)} L{pt(0.24, 7.0)} L{pt(0.22, 6.6)} L{pt(-0.22, 6.6)}Z"/>')


# ---------------------------------------------------------------- scenes

def scene_wall_maria(rng):
    wall_top = 1330
    defs = (lingrad("sky", [(0, "#0d0807", 1), (0.35, "#3a0f0b", 1), (0.62, "#8f2a14", 1),
                            (0.8, "#d9782d", 1), (0.9, "#f0b45e", 1), (1, "#f6cf86", 1)])
            + radgrad("sun", [(0, "#fff1c8", 1), (0.12, "#ffd890", 0.95), (0.35, "#f08a3a", 0.35), (1, "#d9782d", 0)])
            + lingrad("wall", [(0, "#4a3a30", 1), (0.04, "#2a211c", 1), (1, "#0f0c0a", 1)])
            + lingrad("haze", [(0, "#f0b45e", 0.3), (1, "#f0b45e", 0)])
            + blur("steam", 38) + blur("steamBig", 80) + blur("rim", 14) + blur("soft", 6)
            + '<filter id="stone"><feTurbulence type="fractalNoise" baseFrequency="0.004 0.03" numOctaves="4" seed="7"/>'
              '<feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.55 -0.12"/>'
              '<feComposite in2="SourceGraphic" operator="in"/></filter>')
    b = [f'<rect width="{W}" height="{H}" fill="url(#sky)"/>']
    b.append(f'<circle cx="1920" cy="1180" r="1100" fill="url(#sun)"/>')
    # distant cloud bands
    for i in range(14):
        y = rng.uniform(250, 1000)
        b.append(f'<ellipse cx="{rng.uniform(0, W):.0f}" cy="{y:.0f}" rx="{rng.uniform(500, 1200):.0f}" '
                 f'ry="{rng.uniform(18, 50):.0f}" fill="#1a0b08" opacity="{rng.uniform(0.25, 0.55):.2f}" filter="url(#steam)"/>')
    # colossal titan rim light + steam
    cx, s = 1920, 400
    for px in (-1.3, -0.6, 0, 0.6, 1.3):
        b.append(steam(rng, cx + px * s, wall_top - (0.4 if abs(px) > 1 else 1.6) * s, 120, 420, 26, 70, 170, "#f6c88a", 0.16, "steamBig"))
    b.append(f'<path d="{titan_bust(cx, wall_top + 40, s)}" fill="none" stroke="#ffb35a" stroke-width="34" '
             f'opacity="0.9" filter="url(#rim)"/>')
    b.append(f'<path d="{titan_bust(cx, wall_top + 40, s)}" fill="#1b0f0b"/>')
    # muscle striation hints and glowing eyes
    for k in range(-5, 6):
        x = cx + k * s * 0.075
        b.append(f'<path d="M{x:.0f},{wall_top - s * 1.98:.0f} Q{x + k * 6:.0f},{wall_top - s * 1.2:.0f} '
                 f'{x + k * 14:.0f},{wall_top - s * 0.85:.0f}" stroke="#3a1a12" stroke-width="7" fill="none" opacity="0.8"/>')
    for ex in (-0.22, 0.22):
        ey = wall_top - s * 1.5
        b.append(f'<ellipse cx="{cx + ex * s:.0f}" cy="{ey:.0f}" rx="{s * 0.13:.0f}" ry="{s * 0.07:.0f}" fill="#0c0605"/>')
        b.append(f'<ellipse cx="{cx + ex * s:.0f}" cy="{ey:.0f}" rx="30" ry="11" fill="#ffcf7a" filter="url(#soft)"/>')
        b.append(f'<ellipse cx="{cx + ex * s:.0f}" cy="{ey:.0f}" rx="12" ry="5" fill="#fff4dc"/>')
    mt, mb = wall_top - s * 1.1, wall_top - s * 0.86
    b.append(f'<rect x="{cx - s * 0.34:.0f}" y="{mt:.0f}" width="{s * 0.68:.0f}" height="{mb - mt:.0f}" rx="18" fill="#0c0605"/>')
    for k in range(-7, 7):
        x = cx + (k + 0.5) * s * 0.046
        tw = s * 0.038
        curve = abs(k + 0.5) ** 2 * 0.9
        b.append(f'<rect x="{x - tw / 2:.0f}" y="{mt + 4 + curve:.0f}" width="{tw:.0f}" height="{(mb - mt) * 0.42:.0f}" rx="5" fill="#8a6a50"/>')
        b.append(f'<rect x="{x - tw / 2:.0f}" y="{mb - 4 - (mb - mt) * 0.42 - curve * 0.5:.0f}" width="{tw:.0f}" height="{(mb - mt) * 0.42:.0f}" rx="5" fill="#7a5a44"/>')
    for side in (-1, 1):
        b.append(f'<path d="M{cx + side * s * 0.36:.0f},{mt - 30:.0f} Q{cx + side * s * 0.5:.0f},{mt + 40:.0f} '
                 f'{cx + side * s * 0.4:.0f},{mb + 30:.0f}" stroke="#4a2418" stroke-width="10" fill="none"/>')
    b.append(steam(rng, cx, wall_top - 40, 650, 220, 55, 50, 150, "#ffd9a0", 0.22))
    # the wall
    b.append(f'<rect x="0" y="{wall_top}" width="{W}" height="{H - wall_top}" fill="url(#wall)"/>')
    b.append(f'<rect x="0" y="{wall_top}" width="{W}" height="{H - wall_top}" fill="#000" filter="url(#stone)"/>')
    for row in range(1, 14):
        y = wall_top + row ** 1.45 * 9
        b.append(f'<line x1="0" y1="{y:.0f}" x2="{W}" y2="{y:.0f}" stroke="#000" stroke-width="2" opacity="0.35"/>')
    b.append(f'<rect x="0" y="{wall_top - 6}" width="{W}" height="10" fill="#f6c27a" opacity="0.85" filter="url(#soft)"/>')
    b.append(f'<rect x="0" y="{wall_top - 2}" width="{W}" height="4" fill="#ffe2a8"/>')
    # cannons on the wall top
    for x in range(140, W, 380):
        b.append(f'<rect x="{x}" y="{wall_top - 22}" width="46" height="22" fill="#120c0a"/>'
                 f'<rect x="{x + 30}" y="{wall_top - 18}" width="60" height="9" fill="#120c0a"/>')
    b.append(f'<rect x="0" y="{wall_top}" width="{W}" height="380" fill="url(#haze)" opacity="0.35"/>')
    # Shiganshina rooftops in the foreground
    rooftops = []
    x = -50
    while x < W + 50:
        w = rng.uniform(110, 260)
        h = rng.uniform(200, 420)
        top = H - h
        peak = top - rng.uniform(50, 120)
        rooftops.append(f'M{x:.0f},{H} L{x:.0f},{top:.0f} L{x + w / 2:.0f},{peak:.0f} L{x + w:.0f},{top:.0f} L{x + w:.0f},{H} Z')
        if rng.random() < 0.5:
            chx = x + rng.uniform(0.15, 0.7) * w
            rooftops.append(f'M{chx:.0f},{peak + 40:.0f} h22 v-70 h-22 Z')
        x += w - rng.uniform(0, 20)
    tx = 2900
    rooftops.append(f'M{tx},{H} V1560 L{tx + 60},1440 L{tx + 120},1560 V{H} Z')
    rooftops.append(f'M{tx + 50},1440 V1370 h20 V1440 Z')
    b.append(f'<path d="{" ".join(rooftops)}" fill="#0a0706"/>')
    for _ in range(40):
        wx, wy = rng.uniform(0, W), rng.uniform(1880, 2080)
        b.append(f'<rect x="{wx:.0f}" y="{wy:.0f}" width="12" height="18" fill="#f0a24a" opacity="{rng.uniform(0.3, 0.8):.2f}"/>')
    # birds
    for _ in range(9):
        bx, by, bs = rng.uniform(600, 3300), rng.uniform(300, 800), rng.uniform(10, 22)
        b.append(f'<path d="M{bx - bs:.0f},{by - bs * 0.4:.0f} Q{bx - bs * 0.4:.0f},{by - bs * 0.5:.0f} {bx:.0f},{by:.0f} '
                 f'Q{bx + bs * 0.4:.0f},{by - bs * 0.5:.0f} {bx + bs:.0f},{by - bs * 0.4:.0f}" stroke="#140906" '
                 f'stroke-width="4" fill="none"/>')
    return svg("".join(b), defs)


def scene_wings(rng):
    defs = (radgrad("bg", [(0, "#2a221c", 1), (0.55, "#14110f", 1), (1, "#070605", 1)], cy=0.45, r=0.75)
            + radgrad("halo", [(0, "#c9a14a", 0.16), (1, "#c9a14a", 0)])
            + emblem_defs(30)
            + '<filter id="leather"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="3"/>'
              '<feColorMatrix values="0 0 0 0 0.6  0 0 0 0 0.5  0 0 0 0 0.4  0 0 0 0.09 0"/></filter>')
    b = [f'<rect width="{W}" height="{H}" fill="url(#bg)"/>',
         f'<rect width="{W}" height="{H}" filter="url(#leather)"/>',
         f'<circle cx="1920" cy="960" r="900" fill="url(#halo)"/>',
         emblem_svg_group(1920, 960, 1080, glow="#c9a14a"),
         f'<text x="1920" y="1700" text-anchor="middle" font-family="{FONT}" font-size="64" font-weight="700" '
         f'letter-spacing="34" fill="#c9a14a">SHINZOU WO SASAGEYO</text>',
         f'<line x1="1420" y1="1770" x2="2420" y2="1770" stroke="#c9a14a" stroke-width="2" opacity="0.6"/>',
         f'<text x="1920" y="1840" text-anchor="middle" font-family="{FONT}" font-size="34" '
         f'letter-spacing="22" fill="#b3a68f" opacity="0.8">DEDICATE YOUR HEART</text>']
    return svg("".join(b), defs)


def scene_rumbling(rng):
    ground = 1500
    defs = (lingrad("sky", [(0, "#070303", 1), (0.4, "#2e0907", 1), (0.72, "#8a1a10", 1),
                            (0.9, "#e0682a", 1), (1, "#f2a050", 1)])
            + lingrad("dust", [(0, "#c8602a", 0.0), (0.25, "#9a4020", 0.65), (1, "#1a0b07", 1)])
            + lingrad("gfade", [(0, "#0b0504", 0), (1, "#0b0504", 1)])
            + blur("steam", 30) + blur("dustB", 60) + blur("far", 3) + blur("rimR", 10))
    b = [f'<rect width="{W}" height="{H}" fill="url(#sky)"/>']
    for i in range(10):
        b.append(f'<ellipse cx="{rng.uniform(0, W):.0f}" cy="{rng.uniform(150, 900):.0f}" rx="{rng.uniform(600, 1400):.0f}" '
                 f'ry="{rng.uniform(25, 70):.0f}" fill="#120404" opacity="{rng.uniform(0.3, 0.6):.2f}" filter="url(#dustB)"/>')
    layers = [(0.1, 260, "#6e2414", 40), (0.22, 420, "#4e180f", 26), (0.4, 640, "#2c0d09", 15), (0.7, 1050, "#150605", 6)]
    for depth, h, col, n in layers:
        gy = ground - (1 - depth) * 120
        xs = sorted(rng.uniform(-100, W + 100) for _ in range(n))
        figs = []
        for x in xs:
            hh = h * rng.uniform(0.85, 1.15)
            figs.append(titan_body(x, gy, hh, rng))
            b.append(steam(rng, x, gy - hh * 0.8, hh * 0.08, hh * 0.3, 8, hh * 0.04, hh * 0.09, "#f0a070", 0.14))
        flt = ' filter="url(#far)"' if depth < 0.3 else ""
        if depth > 0.3:
            b.append(f'<g fill="#ff8a40" opacity="0.45" filter="url(#rimR)">{"".join(figs)}</g>')
        b.append(f'<g fill="{col}" stroke="{col}"{flt}>{"".join(figs)}</g>')
        b.append(f'<rect x="0" y="{gy - h * 0.35:.0f}" width="{W}" height="{H}" fill="url(#dust)" opacity="0.55" '
                 f'filter="url(#dustB)"/>')
    b.append(f'<rect x="0" y="{ground}" width="{W}" height="{H - ground}" fill="url(#dust)"/>')
    b.append(f'<rect x="0" y="{ground - 100}" width="{W}" height="{H - ground + 100}" fill="url(#gfade)"/>')
    # a lone scout on the cliff for scale
    b.append(f'<path d="M0,{H} L0,1760 C300,1720 600,1700 900,1745 C1050,1770 1150,1840 1300,1900 '
             f'C1400,1950 1500,2050 1560,{H} Z" fill="#060302"/>')
    sx, sy = 760, 1712
    b.append(f'<g fill="#060302"><ellipse cx="{sx}" cy="{sy - 78}" rx="9" ry="11"/>'
             f'<path d="M{sx - 12},{sy - 66} L{sx + 12},{sy - 66} L{sx + 30},{sy - 8} L{sx + 8},{sy - 18} '
             f'L{sx + 6},{sy} L{sx - 6},{sy} L{sx - 8},{sy - 18} L{sx - 34},{sy - 4} Z"/>'
             f'<rect x="{sx + 10}" y="{sy - 50}" width="22" height="4" transform="rotate(-25 {sx + 10} {sy - 50})"/></g>')
    return svg("".join(b), defs)


def scene_paths(rng):
    defs = (lingrad("sky", [(0, "#03050c", 1), (0.6, "#0b1428", 1), (1, "#1a2c4a", 1)])
            + radgrad("glow", [(0, "#cfe9ff", 0.55), (0.3, "#7fb2e6", 0.18), (1, "#3d6ea5", 0)])
            + lingrad("sand", [(0, "#16223a", 1), (1, "#05070d", 1)])
            + lingrad("beam", [(0, "#cfe9ff", 0), (0.6, "#cfe9ff", 0.25), (1, "#eaf6ff", 0.7)])
            + blur("g1", 4) + blur("g2", 16) + blur("g3", 50))
    b = [f'<rect width="{W}" height="{H}" fill="url(#sky)"/>']
    for _ in range(900):
        x, y = rng.uniform(0, W), rng.uniform(0, H * 0.8)
        r = rng.choice([1, 1, 1.5, 2, 2.5])
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#dbeaff" opacity="{rng.uniform(0.2, 0.9):.2f}"/>')
    b.append('<circle cx="1920" cy="900" r="1300" fill="url(#glow)"/>')
    # the coordinate tree of light
    lines = []

    def branch(x, y, ang, ln, wd, depth):
        if depth == 0 or ln < 8:
            return
        x2 = x + math.cos(ang) * ln
        y2 = y - math.sin(ang) * ln
        mx = (x + x2) / 2 + rng.uniform(-ln, ln) * 0.12
        my = (y + y2) / 2 + rng.uniform(-ln, ln) * 0.12
        lines.append((f"M{x:.0f},{y:.0f} Q{mx:.0f},{my:.0f} {x2:.0f},{y2:.0f}", wd))
        k = 2 if depth > 3 else rng.choice([2, 2, 3])
        for i in range(k):
            na = ang + rng.uniform(-0.55, 0.55) + (i - (k - 1) / 2) * 0.35
            branch(x2, y2, na, ln * rng.uniform(0.68, 0.8), wd * 0.68, depth - 1)

    branch(1920, 1720, math.pi / 2, 330, 46, 11)
    for ang in (-0.2, 0.25, math.pi + 0.2, math.pi - 0.25):
        branch(1920, 1720, ang, 260, 22, 7)
    d_all = "".join(f'<path d="{d}" stroke-width="{w:.1f}"/>' for d, w in lines)
    g = 'fill="none" stroke-linecap="round"'
    b.append(f'<g {g} stroke="#7fb2e6" opacity="0.6" filter="url(#g3)">{d_all}</g>')
    b.append(f'<g {g} stroke="#a9d3ff" opacity="0.8" filter="url(#g2)">{d_all}</g>')
    b.append(f'<g {g} stroke="#eaf6ff" filter="url(#g1)">{d_all}</g>')
    b.append('<rect x="1880" y="0" width="80" height="1000" fill="url(#beam)" filter="url(#g3)"/>')
    b.append('<rect x="1916" y="0" width="8" height="1000" fill="url(#beam)" filter="url(#g1)"/>')
    # dunes
    for i, (y0, col) in enumerate([(1650, "#101a2e"), (1780, "#0b1324"), (1920, "#060a14")]):
        pts = [f"M0,{H}", f"L0,{y0}"]
        for x in range(0, W + 200, 200):
            pts.append(f"L{x},{y0 + 50 * math.sin(x / (500 + i * 170) + i * 2) + 20 * math.sin(x / 130 + i):.0f}")
        pts.append(f"L{W},{H} Z")
        b.append(f'<path d="{" ".join(pts)}" fill="{col}"/>')
    for _ in range(140):
        x, y = rng.gauss(1920, 500), rng.uniform(1400, 2000)
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rng.uniform(2, 5):.1f}" fill="#cfe9ff" '
                 f'opacity="{rng.uniform(0.2, 0.7):.2f}" filter="url(#g1)"/>')
    return svg("".join(b), defs)


SCENES = {
    "WallMaria": ("Wall Maria", scene_wall_maria),
    "WingsOfFreedom": ("Wings of Freedom", scene_wings),
    "Rumbling": ("The Rumbling", scene_rumbling),
    "Paths": ("Paths", scene_paths),
}


def finish(png_in, out_dir, seed):
    img = np.asarray(Image.open(png_in).convert("RGB")).astype(np.float32)
    h, w, _ = img.shape
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    vign = 1 - 0.38 * np.clip(d - 0.45, 0, None) ** 1.6
    img *= vign[..., None]
    noise = np.random.default_rng(seed).normal(0, 5.5, (h, w, 1))
    img = np.clip(img + noise, 0, 255).astype(np.uint8)
    im = Image.fromarray(img)
    os.makedirs(out_dir, exist_ok=True)
    im.save(os.path.join(out_dir, "3840x2160.jpg"), quality=90, optimize=True, progressive=True)
    im.resize((2560, 1440), Image.LANCZOS).save(os.path.join(out_dir, "2560x1440.jpg"), quality=90, optimize=True)
    im.resize((1920, 1080), Image.LANCZOS).save(os.path.join(out_dir, "1920x1080.jpg"), quality=92, optimize=True)
    return im


def main(root, only=None):
    tmp = os.path.join(root, "build")
    os.makedirs(tmp, exist_ok=True)
    for i, (key, (name, fn)) in enumerate(SCENES.items()):
        if only and key not in only:
            continue
        src = os.path.join(tmp, f"{key}.svg")
        png = os.path.join(tmp, f"{key}.png")
        open(src, "w").write(fn(random.Random(1000 + i)))
        subprocess.run(["rsvg-convert", src, "-o", png], check=True)
        pkg = os.path.join(root, "wallpapers", f"AttackOnTitan-{key}")
        im = finish(png, os.path.join(pkg, "contents", "images"), i)
        im.resize((640, 360), Image.LANCZOS).save(os.path.join(pkg, "contents", "screenshot.jpg"), quality=88)
        open(os.path.join(pkg, "metadata.json"), "w").write(
            '{\n  "KPlugin": {\n    "Authors": [{"Name": "Shubhwtf"}],\n'
            f'    "Id": "AttackOnTitan-{key}",\n    "License": "CC-BY-SA-4.0",\n'
            f'    "Name": "AoT — {name}"\n  }}\n}}\n')
        print("built", key)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:] or None)
