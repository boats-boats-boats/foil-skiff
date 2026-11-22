#!/usr/bin/env python3
"""
Parametric 3D CAD & Semi-Realistic Rendering Generator for FoilSkiff.
Zero external dependencies (pure Python 3 standard library).

Generates 4 interactive binary 3D STL CAD models (in millimeters, GitHub 3D viewer ready)
and 4 matching shaded 3D isometric engineering SVG renderings:
  1. models/01_step_out_flying_keel_truekit.stl  + diagrams/00-foil-skiff-3d-cad.svg
  2. models/02_switchblade_pod.stl               + diagrams/06-switchblade-3d-cad.svg
  3. models/03_stol_flaperon_pod.stl             + diagrams/07-stol-flaperons-3d-cad.svg
  4. models/04_retracted_beaching_truekit.stl    + diagrams/08-retracted-beaching-3d.svg
"""

import html
import math
import shutil
import struct
import subprocess
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent.parent
MODELS_DIR = ROOT / "models"
DIAG_DIR = ROOT / "diagrams"
RENDERS_DIR = ROOT / "renders"
FONT = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'

# Material RGB palette
C_CARBON = (40, 54, 72)
C_CARBON_DARK = (24, 34, 48)
C_KEVLAR = (234, 179, 8)
C_ALU = (148, 163, 184)
C_WING_LOW = (14, 132, 199)
C_WING_UP = (13, 148, 136)
C_FLAP_L = (56, 189, 248)
C_FLAP_R = (249, 115, 22)
C_MOTOR = (51, 65, 85)
C_PROP = (56, 189, 248)
C_PUSHROD = (220, 38, 38)
C_TUBE_GREY = (212, 220, 230)
C_RUB_STRAKE = (51, 65, 85)
C_SEAT = (71, 85, 105)
C_WATER = (56, 189, 248)
C_SAND = (238, 206, 140)


def v_sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def v_cross(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def v_dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def v_norm(a):
    l = math.sqrt(a[0] ** 2 + a[1] ** 2 + a[2] ** 2)
    return (a[0] / l, a[1] / l, a[2] / l) if l > 1e-12 else (0.0, 0.0, 1.0)


def naca4_section(m, p, t, chord, n=16):
    up, lo = [], []
    for i in range(n + 1):
        beta = math.pi * i / n
        xc = 0.5 * (1.0 - math.cos(beta))
        yt = 5 * t * (0.2969 * math.sqrt(max(xc, 0)) - 0.1260 * xc - 0.3516 * xc**2 + 0.2843 * xc**3 - 0.1036 * xc**4)
        if m == 0 or p == 0:
            yc, dyc = 0.0, 0.0
        elif xc < p:
            yc = m / (p**2) * (2 * p * xc - xc**2)
            dyc = 2 * m / (p**2) * (p - xc)
        else:
            yc = m / ((1 - p) ** 2) * ((1 - 2 * p) + 2 * p * xc - xc**2)
            dyc = 2 * m / ((1 - p) ** 2) * (p - xc)
        th = math.atan(dyc)
        up.append(((xc - yt * math.sin(th)) * chord, (yc + yt * math.cos(th)) * chord))
        lo.append(((xc + yt * math.sin(th)) * chord, (yc - yt * math.cos(th)) * chord))
    return up + list(reversed(lo[1:-1]))


class MeshBuilder:
    def __init__(self):
        self.tris = []  # (p0, p1, p2, rgb, alpha, include_in_stl)

    def add_tri(self, p0, p1, p2, color=C_CARBON, alpha=1.0, stl=True):
        self.tris.append((p0, p1, p2, color, alpha, stl))

    def add_quad(self, p0, p1, p2, p3, color=C_CARBON, alpha=1.0, stl=True):
        self.add_tri(p0, p1, p2, color, alpha, stl)
        self.add_tri(p0, p2, p3, color, alpha, stl)

    def add_box(self, x0, x1, y0, y1, z0, z1, color, alpha=1.0, stl=True):
        v = [
            (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
            (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1),
        ]
        for a, b, c, d in [
            (0, 3, 2, 1), (4, 5, 6, 7),
            (0, 1, 5, 4), (2, 3, 7, 6),
            (0, 4, 7, 3), (1, 2, 6, 5),
        ]:
            self.add_quad(v[a], v[b], v[c], v[d], color, alpha, stl)

    def add_loft(self, rings, color, alpha=1.0, stl=True, cap_ends=True):
        m = len(rings[0])
        for r in range(len(rings) - 1):
            r0, r1 = rings[r], rings[r + 1]
            for i in range(m):
                j = (i + 1) % m
                self.add_quad(r0[i], r0[j], r1[j], r1[i], color, alpha, stl)
        if cap_ends:
            for ring, rev in [(rings[0], True), (rings[-1], False)]:
                ctr = (
                    sum(p[0] for p in ring) / m,
                    sum(p[1] for p in ring) / m,
                    sum(p[2] for p in ring) / m,
                )
                for i in range(m):
                    j = (i + 1) % m
                    self.add_tri(ctr, ring[j], ring[i], color, alpha, stl) if rev else self.add_tri(ctr, ring[i], ring[j], color, alpha, stl)

    def add_cylinder_x(self, x0, x1, cy, cz, r, color, n=12, alpha=1.0, stl=True):
        rings = [
            [(x0, cy + r * math.cos(2 * math.pi * i / n), cz + r * math.sin(2 * math.pi * i / n)) for i in range(n)],
            [(x1, cy + r * math.cos(2 * math.pi * i / n), cz + r * math.sin(2 * math.pi * i / n)) for i in range(n)],
        ]
        self.add_loft(rings, color, alpha, stl)

    def add_cylinder_y(self, cx, y0, y1, cz, r, color, n=12, alpha=1.0, stl=True):
        rings = [
            [(cx + r * math.cos(2 * math.pi * i / n), y0, cz + r * math.sin(2 * math.pi * i / n)) for i in range(n)],
            [(cx + r * math.cos(2 * math.pi * i / n), y1, cz + r * math.sin(2 * math.pi * i / n)) for i in range(n)],
        ]
        self.add_loft(rings, color, alpha, stl)


def add_true_kit_hull(mb: MeshBuilder, tube_alpha=0.42, stl_hull=True):
    """Semi-realistic True Kit Discovery 330 open-bow, open-transom inflatable catamaran (mm)."""
    # Twin Ø460 mm upswept open-bow pontoons (Y = +/-620 mm, X = -1650..+1550 -> 3.2 m LOA)
    stations = [
        (-1650, 22, 165, 40),
        (-1520, 125, 130, 30),
        (-1320, 195, 78, 14),
        (-1020, 230, 16, 0),
        (-400, 230, 0, 0),
        (500, 230, 0, 0),
        (1150, 230, 0, 0),
        (1420, 180, 0, 0),
        (1560, 55, 0, 0),
    ]
    n = 18
    for side in (-1, 1):
        sy = side * 620
        rings = []
        strake_rings = []
        for x, r, zc, yin in stations:
            y_c = sy - side * yin
            ring = []
            for i in range(n):
                a = 2 * math.pi * i / n
                ring.append((x, y_c + r * math.cos(a), zc + r * math.sin(a)))
            rings.append(ring)
            # Outer rub-strake strip along outer equator
            yo = y_c + side * (r + 5)
            strake_rings.append([(x, yo - side * 8, zc - 22), (x, yo, zc - 18), (x, yo, zc + 18), (x, yo - side * 8, zc + 22)])
        mb.add_loft(rings, C_TUBE_GREY, alpha=tube_alpha, stl=stl_hull)
        mb.add_loft(strake_rings, C_RUB_STRAKE, alpha=min(0.85, tube_alpha + 0.35), stl=stl_hull)

    # Open tubular transom frame (X = +1080, upper & lower crossbars connecting tubes above tunnel)
    mb.add_cylinder_y(1080, -450, 450, 145, 22, C_ALU, n=10, alpha=0.92, stl=stl_hull)
    mb.add_cylinder_y(1080, -450, 450, 55, 18, C_ALU, n=10, alpha=0.92, stl=stl_hull)

    # Midship cockpit aluminum bench seat (X = -150..+110, Z = +170)
    mb.add_box(-150, 110, -560, 560, 162, 185, C_SEAT, alpha=0.55, stl=False)

    # Drop-In 2-Piece Rigid Spine Floor (X = -950..+950, Y = -410..+410, Z = +3..+30)
    mb.add_box(-950, -6, -410, 410, 3, 30, C_CARBON, 1.0, stl=True)
    mb.add_box(6, 950, -410, 410, 3, 30, C_CARBON, 1.0, stl=True)
    mb.add_box(-8, 8, -405, 405, 1, 33, C_KEVLAR, 1.0, stl=True)  # Midship latch bar

    # Full Bow-to-Transom Twin-Rail O-Frame (Y = +/-135 mm -> 270 mm spacing, 50x20 mm rails, Z = -22..-2)
    for sy in (-135, 135):
        mb.add_box(-990, 990, sy - 25, sy + 25, -22, -2, C_ALU, 1.0, stl=True)
    for sx in (-990, 968):
        mb.add_box(sx, sx + 22, -165, 165, -22, 33, C_ALU, 1.0, stl=True)


def add_flying_keel_pod(mb: MeshBuilder, dx=0.0, dz=-780.0, pod_h=80.0, with_motors=True):
    """Streamlined 1,300 x 220 x pod_h mm flattened lifting-body battery-fuselage + Kevlar nose + twin 65161 pods."""
    n_ang = 20
    rz_s = pod_h / 2.0
    stations = [
        (-650, 12, rz_s * 0.20), (-625, 58, rz_s * 0.62), (-560, 96, rz_s * 0.90), (-480, 110, rz_s),
        (220, 110, rz_s), (380, 92, rz_s * 0.85), (520, 58, rz_s * 0.60), (620, 28, rz_s * 0.35), (650, 10, rz_s * 0.15)
    ]
    def make_rings(st_list):
        out = []
        for x, ry, rz in st_list:
            ring = []
            for i in range(n_ang):
                a = 2 * math.pi * i / n_ang
                ca, sa = math.cos(a), math.sin(a)
                y = ry * math.copysign(abs(ca) ** 0.85, ca)
                z = dz + rz * math.copysign(abs(sa) ** 0.85, sa)
                ring.append((dx + x, y, z))
            out.append(ring)
        return out

    mb.add_loft(make_rings(stations[:3]), C_KEVLAR, 1.0, stl=True)
    mb.add_loft(make_rings(stations[2:]), C_CARBON, 1.0, stl=True)

    # Aft Horizontal Stabilizer
    st_sec = naca4_section(0.0, 0.0, 0.10, 72.0, n=10)
    st_rings = []
    for y in (-240, -140, 0, 140, 240):
        taper = 1.0 - 0.30 * (abs(y) / 240.0) ** 1.5
        st_rings.append([(dx + 545 + 15 * (1 - taper) + xl * taper, y, dz + zl * taper) for xl, zl in st_sec])
    mb.add_loft(st_rings, C_WING_LOW, 1.0, stl=True)

    if with_motors:
        for sy in (-135, 135):
            pod_rings = []
            for x, r in [(500, 10), (520, 32.5), (650, 32.5), (672, 22), (682, 8)]:
                pod_rings.append([(dx + x, sy + r * math.cos(2 * math.pi * i / 12), dz + r * math.sin(2 * math.pi * i / 12)) for i in range(12)])
            mb.add_loft(pod_rings, C_MOTOR, 1.0, stl=True)
            for k in range(3):
                ang = math.radians(k * 120 + 25)
                by = sy + 88 * math.cos(ang)
                bz = dz + 88 * math.sin(ang)
                mb.add_quad(
                    (dx + 675, sy, dz), (dx + 686, sy + 18 * math.cos(ang + 0.5), dz + 18 * math.sin(ang + 0.5)),
                    (dx + 680, by, bz), (dx + 672, sy + 18 * math.cos(ang - 0.5), dz + 18 * math.sin(ang - 0.5)),
                    C_PROP, 0.95, stl=True,
                )


def add_lower_wings(mb: MeshBuilder, dx=0.0, dz=-790.0, half_span=670.0, root_chord=115.0, x_le=-220.0):
    lo_sec = naca4_section(0.02, 0.4, 0.10, root_chord, n=12)
    ys = [-half_span, -half_span * 0.78, -half_span * 0.48, -110, 110, half_span * 0.48, half_span * 0.78, half_span]
    rings = []
    for y in ys:
        u = abs(y) / half_span
        taper = 1.0 - 0.42 * (u**1.8)
        sweep = 45 * (u**1.3)
        dih = 26 * (u**2.2)
        rings.append([(dx + x_le + sweep + xl * taper, y, dz + dih + zl * taper) for xl, zl in lo_sec])
    mb.add_loft(rings, C_WING_LOW, 1.0, stl=True)


def add_4x_blades(mb: MeshBuilder, z_top=-22.0, z_bot=-780.0, fold_deg=0.0, x_front=-450.0, x_rear=310.0):
    """4x Ultra-Slim Side-Straddling Tandem Blades (60x9 mm NACA 0015) at Y = +/-124 mm, optionally folded aft by fold_deg."""
    blade_sec = naca4_section(0.0, 0.0, 0.15, 60.0, n=10)
    L = abs(z_top - z_bot)
    th = math.radians(fold_deg)
    # Direction vector along strut from top pin toward pod: (+sin(th), 0, -cos(th))
    # Normal vector along chord (pointing aft): (+cos(th), 0, +sin(th))
    sx_dir, sz_dir = math.sin(th), -math.cos(th)
    cx_dir, cz_dir = math.cos(th), math.sin(th)
    for bx in (x_front, x_rear):
        for sy in (-124, 124):
            rings = []
            for s_pos in (0.0, L * 0.5, L):
                ring = []
                for xl, yl in blade_sec:
                    # Shift chord origin so pivot is near trailing edge at top (xl - 30)
                    xc = xl - 30.0
                    px = bx + s_pos * sx_dir + xc * cx_dir
                    pz = z_top + s_pos * sz_dir + xc * cz_dir
                    ring.append((px, sy + yl, pz))
                rings.append(ring)
            mb.add_loft(rings, C_CARBON_DARK, 1.0, stl=True)
    return (L * sx_dir, z_top + L * sz_dir)


def add_upper_step_out_wing(mb: MeshBuilder, dx=0.0, dz=-310.0, x_le=-470.0):
    up_sec = naca4_section(0.025, 0.4, 0.14, 140.0, n=12)
    rings = []
    rad = math.radians(2.5)
    for y in (-500, -350, -125, 125, 350, 500):
        taper = 1.0 - 0.25 * (abs(y) / 500.0) ** 2
        x_off = dx + x_le + 18 * (1 - taper)
        ring = []
        for xl, zl in up_sec:
            xs, zs = xl * taper, zl * taper
            xr = xs * math.cos(rad) + zs * math.sin(rad)
            zr = -xs * math.sin(rad) + zs * math.cos(rad)
            ring.append((x_off + xr, y, dz + zr))
        rings.append(ring)
    mb.add_loft(rings, C_WING_UP, 1.0, stl=True)
    # Aft box-portal tie bar
    mb.add_box(dx + 300, dx + 330, -125, 125, dz - 5, dz + 5, C_ALU, 1.0, stl=True)


def add_water_plane(mb: MeshBuilder, z_w=-380.0):
    n = 8
    wx0, wx1, wy0, wy1 = -1750, 1700, -1050, 1050
    for ix in range(n):
        for iy in range(n):
            xa = wx0 + (wx1 - wx0) * ix / n
            xb = wx0 + (wx1 - wx0) * (ix + 1) / n
            ya = wy0 + (wy1 - wy0) * iy / n
            yb = wy0 + (wy1 - wy0) * (iy + 1) / n
            mb.add_quad((xa, ya, z_w), (xb, ya, z_w), (xb, yb, z_w), (xa, yb, z_w), C_WATER, 0.16, stl=False)


def add_sand_plane(mb: MeshBuilder, z_s=-232.0):
    n = 6
    wx0, wx1, wy0, wy1 = -1750, 1700, -1050, 1050
    for ix in range(n):
        for iy in range(n):
            xa = wx0 + (wx1 - wx0) * ix / n
            xb = wx0 + (wx1 - wx0) * (ix + 1) / n
            ya = wy0 + (wy1 - wy0) * iy / n
            yb = wy0 + (wy1 - wy0) * (iy + 1) / n
            mb.add_quad((xa, ya, z_s), (xb, ya, z_s), (xb, yb, z_s), (xa, yb, z_s), C_SAND, 0.32, stl=False)


def write_binary_stl(mb: MeshBuilder, path: Path, desc: str):
    stl_tris = [t for t in mb.tris if t[5]]
    header = desc.encode("ascii", "ignore")[:80].ljust(80, b" ")
    with open(path, "wb") as f:
        f.write(header)
        f.write(struct.pack("<I", len(stl_tris)))
        for p0, p1, p2, _, _, _ in stl_tris:
            n = v_norm(v_cross(v_sub(p1, p0), v_sub(p2, p0)))
            f.write(struct.pack("<3f3f3f3fH", *n, *p0, *p1, *p2, 0))
    print(f"STL: {path.name:40s} | {len(stl_tris):4d} tris | {path.stat().st_size/1024:5.1f} KB")


def render_3d_svg(mb: MeshBuilder, path: Path, title: str, subtitle: str, callouts, az_deg=-140, el_deg=21, scale=0.29, z_center=320, footer="", W=1040, H=620):
    az, el = math.radians(az_deg), math.radians(el_deg)
    ca, sa, ce, se = math.cos(az), math.sin(az), math.cos(el), math.sin(el)
    light = v_norm((-0.52, 0.46, 0.72))

    def project(p):
        x, y, z = p[0], p[1], p[2] + z_center
        x1 = x * ca - y * sa
        y1 = x * sa + y * ca
        y2 = y1 * ce - z * se
        z2 = y1 * se + z * ce
        cam = 5200.0
        persp = cam / (cam - y2)
        return (W * 0.50 + x1 * scale * persp, H * 0.53 - z2 * scale * persp, y2)

    projected = []
    for p0, p1, p2, col, alpha, is_stl in mb.tris:
        n = v_norm(v_cross(v_sub(p1, p0), v_sub(p2, p0)))
        q0, q1, q2 = project(p0), project(p1), project(p2)
        depth = (q0[2] + q1[2] + q2[2]) / 3.0
        shade = 0.36 + 0.64 * abs(v_dot(n, light))
        r = min(255, int(col[0] * shade))
        g = min(255, int(col[1] * shade))
        b = min(255, int(col[2] * shade))
        projected.append((depth, q0, q1, q2, f"rgb({r},{g},{b})", alpha, is_stl))
    projected.sort(key=lambda item: item[0])

    s = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs>
    <linearGradient id="bg3d" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="100%" stop-color="#EFF6FF"/>
    </linearGradient>
    <marker id="arr3d" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#0F172A"/>
    </marker>
    <style>
      text {{ font-family: {FONT}; }}
      .t {{ font-size: 18px; font-weight: 700; fill: #0F172A; }}
      .s {{ font-size: 12px; fill: #475569; }}
      .l {{ font-size: 11px; font-weight: 700; fill: #0F172A; }}
      .ls {{ font-size: 10px; fill: #475569; }}
    </style>
  </defs>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12" fill="url(#bg3d)" stroke="#CBD5E1" stroke-width="1.5"/>
  <text x="24" y="30" class="t">{html.escape(title)}</text>
  <text x="24" y="48" class="s">{html.escape(subtitle)}</text>
'''
    for _, q0, q1, q2, fill_rgb, alpha, is_stl in projected:
        stroke = fill_rgb if is_stl else "none"
        sw = "0.45" if is_stl else "0"
        s += f'  <polygon points="{q0[0]:.1f},{q0[1]:.1f} {q1[0]:.1f},{q1[1]:.1f} {q2[0]:.1f},{q2[1]:.1f}" fill="{fill_rgb}" fill-opacity="{alpha:.2f}" stroke="{stroke}" stroke-width="{sw}"/>\n'

    for pt3, side, ly, lx_end, head, sub in callouts:
        px, py, _ = project(pt3)
        tx, anchor = (26, "start") if side == "left" else (W - 26, "end")
        s += f'  <line x1="{lx_end}" y1="{ly}" x2="{px:.1f}" y2="{py:.1f}" stroke="#0F172A" stroke-width="1.2" marker-end="url(#arr3d)"/>\n'
        s += f'  <circle cx="{px:.1f}" cy="{py:.1f}" r="3" fill="#FBBF24" stroke="#0F172A" stroke-width="1"/>\n'
        s += f'  <text x="{tx}" y="{ly-2}" text-anchor="{anchor}" class="l">{html.escape(head)}</text>\n'
        s += f'  <text x="{tx}" y="{ly+11}" text-anchor="{anchor}" class="ls">{html.escape(sub)}</text>\n'

    if footer:
        s += f'  <text x="24" y="{H-16}" class="ls">{html.escape(footer)}</text>\n'
    s += "</svg>\n"
    path.write_text(s)
    print(f"SVG: {path.name:40s} | {path.stat().st_size/1024:5.1f} KB")


def render_openscad_png(mb: MeshBuilder, png_path: Path, camera: str, imgsize="1400,860"):
    """Export a multi-material colored .scad file and render a crisp 3D PNG with OpenSCAD if installed."""
    openscad = shutil.which("openscad") or "/opt/homebrew/bin/openscad"
    if not Path(openscad).exists():
        print("OpenSCAD not found; skipping PNG render for", png_path.name)
        return
    RENDERS_DIR.mkdir(parents=True, exist_ok=True)
    # Group triangles by (rgb, alpha), rendering opaque groups FIRST and translucent LAST (proper OpenGL blending)
    groups = defaultdict(list)
    for p0, p1, p2, col, alpha, _ in mb.tris:
        groups[(col, round(alpha, 2))].append((p0, p1, p2))

    ordered_keys = sorted(groups.keys(), key=lambda k: (-k[1], k[0]))
    scad_lines = ["// Auto-generated multi-material OpenSCAD render scene for FoilSkiff\n"]
    for (r, g, b), alpha in ordered_keys:
        tris = groups[((r, g, b), alpha)]
        pt_map = {}
        pts = []
        faces = []
        for p0, p1, p2 in tris:
            f_idx = []
            for p in (p0, p1, p2):
                kp = (round(p[0], 2), round(p[1], 2), round(p[2], 2))
                if kp not in pt_map:
                    pt_map[kp] = len(pts)
                    pts.append(kp)
                f_idx.append(pt_map[kp])
            faces.append(f_idx)
        pts_str = ",".join(f"[{x},{y},{z}]" for x, y, z in pts)
        faces_str = ",".join(f"[{a},{b_i},{c}]" for a, b_i, c in faces)
        scad_lines.append(
            f"color([{r/255:.3f},{g/255:.3f},{b/255:.3f},{alpha:.2f}]) "
            f"polyhedron(points=[{pts_str}], faces=[{faces_str}], convexity=6);\n"
        )

    tmp_scad = Path("/tmp") / f"{png_path.stem}.scad"
    tmp_scad.write_text("".join(scad_lines))
    cmd = [
        openscad,
        f"--imgsize={imgsize}",
        "--colorscheme=Tomorrow",
        f"--camera={camera}",
        "-o", str(png_path),
        str(tmp_scad),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and png_path.exists():
        print(f"PNG: {png_path.name:40s} | {png_path.stat().st_size/1024:5.1f} KB (OpenSCAD)")
    else:
        print(f"OpenSCAD render failed for {png_path.name}: {res.stderr[:200]}")


# ---------------------------------------------------------------------------
# MODEL 1: Primary Step-Out Flying-Keel Pod on Semi-Realistic True Kit 330
# ---------------------------------------------------------------------------
def build_model_01_step_out():
    mb = MeshBuilder()
    add_true_kit_hull(mb, tube_alpha=0.40, stl_hull=True)
    add_4x_blades(mb, z_top=-22, z_bot=-780, fold_deg=0)
    add_upper_step_out_wing(mb, dx=0, dz=-310)
    add_flying_keel_pod(mb, dx=0, dz=-780)
    add_lower_wings(mb, dx=0, dz=-790, half_span=670, root_chord=115)
    add_water_plane(mb, z_w=-380)
    write_binary_stl(mb, MODELS_DIR / "01_step_out_flying_keel_truekit.stl", "FoilSkiff 01: Primary Step-Out Flying-Keel Pod on True Kit 330 (mm)")
    callouts = [
        ((-500, 0, 28), "left", 104, 240, "Drop-In 2-Piece Rigid Spine Floor", "Zero glue/holes • Replaces air floor"),
        ((-980, 135, -10), "left", 205, 225, "Bow-to-Transom Twin-Rail O-Frame", "2× 50×20 mm Alu rails (~3.5 kg)"),
        ((-420, 480, -310), "left", 340, 230, "Upper Step-Out Booster Wing", "+1,400 cm² • Flies IN AIR >9 kn!"),
        ((-635, 0, -780), "left", 482, 235, "20 mm Kevlar Crush-Nose Cone", "Ahead of 26 L swappable battery bay"),
        ((950, -620, 120), "right", 108, 810, "True Kit Discovery 330 Hull", "Ø460 mm tubes + rub-strakes + open bow"),
        ((310, -124, -460), "right", 232, 810, "4× Side-Straddling Blades", "60×9 mm • Folds to ~90 mm flat!"),
        ((640, -135, -780), "right", 392, 795, "2× Flipsky 65161 Tailcone Pods", "CAN-bus 360° differential steering"),
        ((-150, -640, -780), "right", 508, 810, "1,350 cm² Lower Thin Wings", "t/c = 10% • 30.8 nm @ 15.5 kn"),
    ]
    render_3d_svg(
        mb, DIAG_DIR / "00-foil-skiff-3d-cad.svg",
        "3D CAD Model 1: Primary Step-Out Flying-Keel Pod on True Kit Discovery 330",
        "True-scale millimeter assembly flying 6\"–8\" above cruise waterline (Upper Step-Out Wing clear in dry air!)",
        callouts, az_deg=-140, el_deg=20, scale=0.285, z_center=300,
        footer="Interactive 3D STL: models/01_step_out_flying_keel_truekit.stl (click on GitHub to orbit/zoom or 3D-print at 1:15 scale)",
    )
    render_openscad_png(mb, RENDERS_DIR / "01-step-out-truekit-3d.png", "0,0,-310,77,0,222,5200")


# ---------------------------------------------------------------------------
# MODEL 2: Flush-Nested Top-Deck Switchblade Wing Pod (Deployed 3D CAD)
# ---------------------------------------------------------------------------
def build_model_02_switchblade():
    mb = MeshBuilder()
    # O-Frame rail segment above pod
    for sy in (-135, 135):
        mb.add_box(-760, 760, sy - 22, sy + 22, -22, -2, C_ALU, 1.0, stl=True)
    # 4x blades at x=-480 (170 mm from nose, cleanly ahead of switchblade LE!) & x=+310 (960 mm from nose)
    add_4x_blades(mb, z_top=-22, z_bot=-620, fold_deg=0, x_front=-480, x_rear=310)
    # Slightly taller 90 mm pod (+10 mm for 13 mm flush top recess)
    add_flying_keel_pod(mb, dx=0, dz=-620, pod_h=90.0)
    add_lower_wings(mb, dx=0, dz=-640, half_span=620, root_chord=108, x_le=-170)

    # Flush top pocket rim & 70 mm Carbon Overhang Bridge (X = -435..-365, Z = -576..-565)
    mb.add_box(-435, -365, -112, 112, -578, -564, C_CARBON_DARK, 1.0, stl=True)
    # Two DEPLOYED 680x105x13 mm Switchblade UD Carbon Wings sweeping out at X = -415..-310, Z = -575!
    sw_sec = naca4_section(0.02, 0.4, 0.12, 105.0, n=10)
    for side in (-1, 1):
        rings = []
        for dist in (40, 110, 350, 620, 790):
            taper = 1.0 - 0.18 * (dist / 790.0) ** 2
            y = side * dist
            rings.append([(-415 + xl * taper, y, -575 + zl * taper) for xl, zl in sw_sec])
        mb.add_loft(rings, C_WING_UP, 1.0, stl=True)
        # Pivot boss pin marker
        mb.add_box(-405, -385, side * 35 - 10, side * 35 + 10, -582, -560, C_KEVLAR, 1.0, stl=True)
        # Ghost closed-position outline inside roof recess (visual only!)
        mb.add_box(-415, 265, side * 52 - 48, side * 52 + 48, -576, -569, C_FLAP_L, 0.25, stl=False)

    write_binary_stl(mb, MODELS_DIR / "02_switchblade_pod.stl", "FoilSkiff 02: Flush-Nested Top-Deck Switchblade Wing Pod (mm)")
    callouts = [
        ((-400, 680, -575), "left", 130, 255, "Switchblade Blades Deployed (+1,300 cm²)", "2× 680×105×13 mm UD carbon • 1.58 m span"),
        ((-400, 0, -570), "left", 255, 255, "70 mm Carbon Overhang Bridge", "Reacts upward lift in pure compression!"),
        ((-635, 0, -620), "left", 425, 245, "90 mm Lifting Battery-Fuselage", "+10 mm height preserves full 26 L bay"),
        ((-480, -124, -300), "right", 130, 795, "4× Blades at x=170 & x=960 mm", "790 mm unobstructed sweep arc between pairs"),
        ((40, -50, -572), "right", 265, 795, "Flush Top-Deck Recess (Translucent)", "0 cm² extra wet area when closed @ >9 kn!"),
        ((-120, -580, -635), "right", 420, 800, "1,250 cm² Fixed Lower Thin Wings", "30.8 nm @ 15.5 kn • 32.3 lbf @ 22 kn (best pod!)"),
    ]
    render_3d_svg(
        mb, DIAG_DIR / "06-switchblade-3d-cad.svg",
        "3D CAD Model 2: Flush-Nested Top-Deck Switchblade Wing Pod (Deployed + Flush Recess)",
        "Zero surface-piercing chop risk • Blades nest 100% flush into fuselage roof at >9 kn (0 cm² extra wet area)",
        callouts, az_deg=-134, el_deg=26, scale=0.38, z_center=340,
        footer="Interactive 3D STL: models/02_switchblade_pod.stl (click on GitHub to inspect the 70 mm overhang bridge & sweep clearance in 3D)",
    )
    render_openscad_png(mb, RENDERS_DIR / "02-switchblade-pod-3d.png", "-50,0,-350,60,0,228,3650")


# ---------------------------------------------------------------------------
# MODEL 3: Submerged Split STOL Flaperon Pod (1,000 + 2x250 cm² Active Control)
# ---------------------------------------------------------------------------
def build_model_03_stol_flaperons():
    mb = MeshBuilder()
    # Spine Floor deck tray with 2 dry IP67 brushless servos mounted on top!
    mb.add_box(-760, 760, -240, 240, 4, 24, C_CARBON, 0.85, stl=True)
    for sy in (-135, 135):
        mb.add_box(-760, 760, sy - 22, sy + 22, -22, -2, C_ALU, 1.0, stl=True)
        # Dry IP67 80 kg-cm brushless servo above rear blade!
        mb.add_box(275, 345, sy - 20, sy + 20, 24, 66, C_KEVLAR, 1.0, stl=True)
        # 4 mm stainless pushrod running down rear blade trailing-edge groove!
        mb.add_box(338, 346, sy - 3, sy + 3, -648, 35, C_PUSHROD, 1.0, stl=True)

    add_4x_blades(mb, z_top=-22, z_bot=-620, fold_deg=0, x_front=-420, x_rear=310)
    add_flying_keel_pod(mb, dx=0, dz=-620, pod_h=80.0)
    # Compact 1,000 cm² High-Speed Main Wing (1,050 mm span x 100 mm chord, LE at x=-245 for crisp visible STOL slot gap!)
    add_lower_wings(mb, dx=0, dz=-622, half_span=525, root_chord=100, x_le=-245)

    # Split Port & Starboard 250 cm² STOL Slotted Flaperons (450 x 55 mm ea., slightly below & behind main wing!)
    # Show differential deflection: Port (Y<0) pitched +18 deg DOWN (takeoff/bank), Starboard (Y>0) pitched -8 deg UP!
    fl_sec = naca4_section(0.02, 0.4, 0.11, 62.0, n=10)
    for side, deg, col in [(-1, 18.0, C_FLAP_L), (1, -8.0, C_FLAP_R)]:
        rad = math.radians(deg)
        rings = []
        for dist in (115, 320, 545):
            y = side * dist
            ring = []
            for xl, zl in fl_sec:
                xp = xl - 12.4
                xr = xp * math.cos(rad) + zl * math.sin(rad)
                zr = -xp * math.sin(rad) + zl * math.cos(rad)
                ring.append((-92 + xr, y, -652 + zr))
            rings.append(ring)
        mb.add_loft(rings, col, 1.0, stl=True)
        mb.add_box(-92, 342, side * 124 - 4, side * 124 + 4, -648, -640, C_PUSHROD, 1.0, stl=True)

    write_binary_stl(mb, MODELS_DIR / "03_stol_flaperon_pod.stl", "FoilSkiff 03: Submerged Split STOL Flaperon Active-Control Pod (mm)")
    callouts = [
        ((310, 135, 50), "left", 118, 250, "2× Dry Deck IP67 Brushless Servos", "70–80 kg·cm (~$60 ea.) safely ABOVE water"),
        ((-100, 480, -648), "left", 275, 250, "Starboard 250 cm² Flaperon (-8° Up)", "Differential left/right = Active Roll & Banked Turns"),
        ((-635, 0, -620), "left", 445, 245, "Submerged 400 mm Deep Permanently", "Zero surface-piercing ventilation in 2 ft chop!"),
        ((342, -135, -310), "right", 145, 790, "4 mm Stainless Pushrods", "Tucked in rear blade trailing-edge grooves"),
        ((-180, -480, -625), "right", 315, 800, "Compact 1,000 cm² Speed Main Wing", "Shrunk span • 29.8 nm @ 15.5 kn"),
        ((-98, -480, -660), "right", 455, 795, "Port 250 cm² STOL Flaperon (+18° Down)", "Junkers slot jet (CL_max ≈ 2.0) • 20% failsafe pivot"),
    ]
    render_3d_svg(
        mb, DIAG_DIR / "07-stol-flaperons-3d-cad.svg",
        "3D CAD Model 3: Submerged Split STOL Flaperons (1,000 + 2×250 cm² Active Control)",
        "Shown in differential roll/bank (+18° Port / -8° Starboard) • Dry-deck servos + 4 mm pushrods (~$160 active BOM)",
        callouts, az_deg=-138, el_deg=23, scale=0.41, z_center=320,
        footer="Interactive 3D STL: models/03_stol_flaperon_pod.stl (click on GitHub to inspect the split STOL slot gap & pushrod linkage)",
    )
    render_openscad_png(mb, RENDERS_DIR / "03-stol-flaperon-pod-3d.png", "20,0,-330,66,0,224,2950")


# ---------------------------------------------------------------------------
# MODEL 4: Retracted / Folded Beaching Configuration on True Kit 330
# ---------------------------------------------------------------------------
def build_model_04_retracted():
    mb = MeshBuilder()
    add_true_kit_hull(mb, tube_alpha=0.44, stl_hull=True)
    # Fold all 4x 60x9 mm side-straddling blades 84 deg AFT!
    # Vertical drop of 758 mm strut at 84 deg = 79 mm -> pod centerline at Z = -22 - 79 = -101 (bottom = -141 mm?
    # Note: with 550 mm strut length on beaching fold (86 deg) -> pod center at Z = -56, bottom at -96 mm -> +136 mm above -232 mm sand!)
    dx_pod, dz_pod = add_4x_blades(mb, z_top=-20, z_bot=-580, fold_deg=85.0, x_front=-580, x_rear=180)
    # Pod shifted back by dx_pod, tucked right at Z = -68 mm (bottom at -108 mm -> +124 mm / 4.9" clear of flat sand!)
    add_flying_keel_pod(mb, dx=dx_pod * 0.85, dz=-56.0, pod_h=80.0)
    add_lower_wings(mb, dx=dx_pod * 0.85, dz=-66.0, half_span=650, root_chord=112)
    add_sand_plane(mb, z_s=-232.0)

    write_binary_stl(mb, MODELS_DIR / "04_retracted_beaching_truekit.stl", "FoilSkiff 04: Retracted 85-deg Beaching Mode on True Kit 330 (mm)")
    callouts = [
        ((-1200, 620, 60), "left", 118, 235, "True Kit Discovery 330 on Flat Sand", "Ø460 mm tubes sit cleanly on beach (Z = -232 mm)"),
        ((-320, 124, -45), "left", 250, 235, "4× Side-Straddling Blades Folded 85°", "60 mm chords fold BESIDE 80 mm pod (zero stack!)"),
        ((dx_pod * 0.85 - 500, 0, -56), "left", 425, 240, "Pod Stays 100% Horizontal!", "Tucked UP between O-Frame rails at Z = -96 mm"),
        ((980, -135, 10), "right", 130, 800, "3:1 Retraction Line & Transom Bridge", "One-person lift into tunnel for 6\" beaching"),
        ((dx_pod * 0.85 + 620, -135, -56), "right", 285, 795, "Props & Tailcone High & Dry", "Protected inside tunnel above waterline/sand"),
        ((200, -450, -165), "right", 455, 800, "~135–140 mm (5.5\") Sand Clearance!", "Zero nose-plowing or ceiling collision"),
    ]
    render_3d_svg(
        mb, DIAG_DIR / "08-retracted-beaching-3d.svg",
        "3D CAD Model 4: Retracted Beaching Mode (85° Parallelogram Fold on True Kit 330)",
        "4× Side-Straddling Blades fold flat beside the 80 mm pod — leaving ~5.5\" clear air above flat beach sand!",
        callouts, az_deg=-138, el_deg=14, scale=0.285, z_center=120,
        footer="Interactive 3D STL: models/04_retracted_beaching_truekit.stl (click on GitHub to inspect under-tunnel clearance in 3D)",
    )
    render_openscad_png(mb, RENDERS_DIR / "04-retracted-beaching-3d.png", "0,0,-100,94,0,250,4200")


if __name__ == "__main__":
    build_model_01_step_out()
    build_model_02_switchblade()
    build_model_03_stol_flaperons()
    build_model_04_retracted()
    old_stl = MODELS_DIR / "foil_skiff_pod.stl"
    if old_stl.exists():
        old_stl.unlink()
    print("All 4 3D STL CAD models and 4 shaded 3D isometric SVGs generated successfully.")
