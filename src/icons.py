"""Icon theme: Survey Corps green folders (recoloured from Papirus) + emblem start icons.

usage: icons.py <repo root> <path to Papirus icon theme>
"""
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from emblem import standalone  # noqa: E402

COLOR_VARIANTS = ("adwaita|black|blue|bluegrey|breeze|brown|carmine|cyan|darkcyan|deeporange|green|grey|indigo|"
                  "magenta|nordic|orange|palebrown|paleorange|pink|red|teal|violet|white|yaru|yellow")
SKIP = re.compile(rf"^folder-({COLOR_VARIANTS})(-|\.svg)")
WANT = re.compile(r"^(folder|user-|inode-directory)")
SIZES = ["16x16", "22x22", "24x24", "32x32", "48x48", "64x64", "96x96", "128x128"]

RECOLOR = {"#cccccc": "#2c5238", "#e4e4e4": "#427a52", "#ffffff": "#e8dcc4", "#4f4f4f": "#1b3022"}
RECOLOR_16 = {"#e4e4e4": "#79a883", "#dfdfdf": "#79a883"}

START_NAMES = ["start-here", "start-here-kde", "start-here-kde-plasma", "start-here-archlinux",
               "start-here-symbolic", "distributor-logo", "distributor-logo-archlinux", "archlinux-logo"]


def recolor(svg, table):
    return re.sub(r"#[0-9a-fA-F]{6}", lambda m: table.get(m.group(0).lower(), m.group(0)), svg)


def main(root, papirus):
    out = os.path.join(root, "icons", "AttackOnTitan")
    if os.path.isdir(out):
        shutil.rmtree(out)
    dirs = []
    for size in SIZES:
        src = os.path.join(papirus, size, "places")
        if not os.path.isdir(src):
            continue
        dst = os.path.join(out, size, "places")
        os.makedirs(dst)
        dirs.append((f"{size}/places", int(size.split("x")[0])))
        table = RECOLOR_16 if size == "16x16" else RECOLOR
        for name in sorted(os.listdir(src)):
            if not WANT.match(name) or SKIP.match(name):
                continue
            real = os.path.realpath(os.path.join(src, name))
            with open(real) as f:
                data = f.read()
            with open(os.path.join(dst, name), "w") as f:
                f.write(recolor(data, table))
    # the emblem replaces the application launcher / distro logo
    sc = os.path.join(out, "scalable", "apps")
    os.makedirs(sc)
    dirs.append(("scalable/apps", 0))
    with open(os.path.join(sc, "start-here.svg"), "w") as f:
        f.write(standalone(256))
    for n in START_NAMES[1:]:
        os.symlink("start-here.svg", os.path.join(sc, f"{n}.svg"))
    lines = ["[Icon Theme]", "Name=Attack on Titan", "Comment=Survey Corps folders on top of Papirus-Dark",
             "Inherits=Papirus-Dark,breeze-dark,hicolor", "Example=folder",
             "Directories=" + ",".join(d for d, _ in dirs), ""]
    for d, s in dirs:
        lines.append(f"[{d}]")
        if s:
            lines += [f"Size={s}", "Context=Places", "Type=Fixed"]
        else:
            lines += ["Size=256", "MinSize=16", "MaxSize=512", "Context=Applications", "Type=Scalable"]
        lines.append("")
    with open(os.path.join(out, "index.theme"), "w") as f:
        f.write("\n".join(lines))
    subprocess.run(["rsvg-convert", "-w", "256", os.path.join(out, "64x64", "places", "folder.svg"),
                    "-o", os.path.join(root, "build", "folder-preview.png")], check=False)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
