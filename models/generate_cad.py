#!/usr/bin/env python3
"""
Parametric 3D CAD & Semi-Realistic Rendering Generator for FoilSkiff.
Primary Reference Hull: True Kit Navigator 300 (300 x 155 cm, 60 cm inside beam, Ø460 mm tubes,
closed continuous bow tube, factory Tru-Alu rigid transom, 31 kg bare hull).
Secondary Open-Bow Reference: True Kit Discovery 330 (330 cm, open square bow, full rigid O-Frame).

Zero external Python dependencies (pure Python 3 standard library + optional OpenSCAD CLI).

Generates 5 interactive binary 3D STL CAD models, 5 shaded 3D isometric SVGs, and 5 OpenSCAD PNGs:
  1. models/01_navigator300_step_out_flying_keel.stl + renders/01-navigator300-step-out-3d.png + diagrams/00-navigator300-3d-cad.svg
  2. models/02_switchblade_pod.stl                   + renders/02-switchblade-pod-3d.png       + diagrams/06-switchblade-3d-cad.svg
  3. models/03_stol_flaperon_pod.stl                 + renders/03-stol-flaperon-pod-3d.png     + diagrams/07-stol-flaperons-3d-cad.svg
  4. models/04_navigator300_retracted_beaching.stl   + renders/04-navigator300-retracted-3d.png+ diagrams/08-navigator300-retracted-3d.svg
  5. models/05_discovery330_oframe_step_out.stl      + renders/05-discovery330-oframe-3d.png   + diagrams/11-discovery330-oframe-3d-cad.svg
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
C_TRANSOM_ALU = (176, 188, 202)
C_DYNEEMA = (220, 38, 38)
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

    def add_tube_along_path(self, path_pts_radii, color, n=16, alpha=1.0, stl=True, cap_ends=True):
        """Sweep a circular tube along a 3D centerline path [(x, y, z, r), ...]."""
        rings = []
        k_len = len(path_pts_radii)
        for idx, (x, y, z, r) in enumerate(path_pts_radii):
            if idx == 0:
                t_vec = v_sub(path_pts_radii[1][:3], (x, y, z))
            elif idx == k_len - 1:
                t_vec = v_sub((x, y, z), path_pts_radii[-2][:3])
            else:
                t_vec = v_sub(path_pts_radii[idx + 1][:3], path_pts_radii[idx - 1][:3])
            t_vec = v_norm(t_vec)
            up = (0.0, 0.0, 1.0) if abs(t_vec[2]) < 0.92 else (1.0, 0.0, 0.0)
            b_vec = v_norm(v_cross(t_vec, up))
            n_vec = v_norm(v_cross(b_vec, t_vec))
            ring = []
            for i in range(n):
                a = 2 * math.pi * i / n
                ca, sa = math.cos(a), math.sin(a)
                px = x + r * (ca * b_vec[0] + sa * n_vec[0])
                py = y + r * (ca * b_vec[1] + sa * n_vec[1])
                pz = z + r * (ca * b_vec[2] + sa * n_vec[2])
                ring.append((px, py, pz))
            rings.append(ring)
        self.add_loft(rings, color, alpha=alpha, stl=stl, cap_ends=cap_ends)

    def add_cylinder_y(self, cx, y0, y1, cz, r, color, n=12, alpha=1.0, stl=True):
        rings = [
            [(cx + r * math.cos(2 * math.pi * i / n), y0, cz + r * math.sin(2 * math.pi * i / n)) for i in range(n)],
            [(cx + r * math.cos(2 * math.pi * i / n), y1, cz + r * math.sin(2 * math.pi * i / n)) for i in range(n)],
        ]
        self.add_loft(rings, color, alpha, stl)

    def add_rod(self, p0, p1, r, color, n=8, alpha=1.0, stl=True):
        self.add_tube_along_path([(p0[0], p0[1], p0[2], r), (p1[0], p1[1], p1[2], r)], color, n=n, alpha=alpha, stl=stl)


def add_navigator_300_hull(mb: MeshBuilder, tube_alpha=0.40, stl_hull=True):
    """
    Semi-realistic True Kit Navigator 300 (PRIMARY HULL):
      - LOA: 300 cm (X = -1500 .. +1500 mm)
      - External Beam: 155 cm -> Tube centers at Y = +/-545 mm, Tube Ø = 460 mm (r = 230 mm)
      - Inside Beam: 60 cm (600 mm clear between tubes; floor tuck-under width ~680 mm)
      - Closed Continuous Curved Inflatable Bow Tube (sweeping upward at front over tunnel inlet!)
      - Factory Tru-Alu Rigid Aluminum Transom spanning between tubes at X = +1040 mm (open tunnel underneath!)
      - Drop-In 2-Piece Rigid Spine Floor (680 x 1,850 mm) + Transom-Clamped Hybrid C-Frame Twin Rails
        + 6 mm Dyneema Bow-D-Ring Tieback Sling (zero cantilever, zero holes!)
    """
    # Continuous U-shaped inflatable tube path: Port stern cone -> Port tube -> Curved upswept Closed Bow -> Stbd tube -> Stbd stern cone
    path = [
        (1490, -545, 0, 45),
        (1360, -545, 0, 175),
        (1100, -545, 0, 230),
        (450, -545, 0, 230),
        (-300, -545, 0, 230),
        (-780, -545, 18, 226),
        (-1060, -490, 62, 212),
        (-1280, -340, 118, 196),
        (-1410, -140, 152, 188),
        (-1445, 0, 162, 186),     # Raised closed rounded bow apex (open tunnel air inlet underneath!)
        (-1410, 140, 152, 188),
        (-1280, 340, 118, 196),
        (-1060, 490, 62, 212),
        (-780, 545, 18, 226),
        (-300, 545, 0, 230),
        (450, 545, 0, 230),
        (1100, 545, 0, 230),
        (1360, 545, 0, 175),
        (1490, 545, 0, 45),
    ]
    mb.add_tube_along_path(path, C_TUBE_GREY, n=18, alpha=tube_alpha, stl=stl_hull, cap_ends=True)

    # Outer dark grey rub-strake wrapping continuously around port side, closed bow, and starboard side
    strake_path = []
    for x, y, z, r in path[1:-1]:
        if abs(y) > 450 and x > -900:
            sy = y + math.copysign(r + 6, y)
            strake_path.append((x, sy, z, 18))
        else:
            # Wrap around curved bow nose outward
            ang = math.atan2(y, x + 900)
            strake_path.append((x + (r + 6) * math.cos(ang), y + (r + 6) * math.sin(ang), z, 18))
    mb.add_tube_along_path(strake_path, C_RUB_STRAKE, n=8, alpha=min(0.85, tube_alpha + 0.35), stl=stl_hull, cap_ends=True)

    # Factory Tru-Alu Rigid Aluminum Transom Plate (X = +1035..+1065, Y = -450..+450, Z = -8..+350, notched for short-shaft outboard!)
    mb.add_box(1035, 1065, -455, 455, -8, 260, C_TRANSOM_ALU, alpha=0.88, stl=stl_hull)
    mb.add_box(1035, 1065, -455, -180, 260, 335, C_TRANSOM_ALU, alpha=0.88, stl=stl_hull)
    mb.add_box(1035, 1065, 180, 455, 260, 335, C_TRANSOM_ALU, alpha=0.88, stl=stl_hull)

    # Two standard True Kit Navigator aluminum cockpit seats (visual only)
    mb.add_box(-520, -320, -490, 490, 170, 192, C_SEAT, alpha=0.50, stl=False)
    mb.add_box(320, 520, -490, 490, 170, 192, C_SEAT, alpha=0.50, stl=False)

    # Factory Bow Towing D-Ring under raised bow nose (X = -1420, Y = 0, Z = -25)
    mb.add_box(-1435, -1400, -28, 28, -42, -12, C_KEVLAR, 1.0, stl=True)

    # Drop-In 2-Piece Rigid Spine Floor for Navigator 300 (680 mm wide x 1,850 mm long, X = -860..+990, Z = +3..+30)
    mb.add_box(-860, 60, -340, 340, 3, 30, C_CARBON, 1.0, stl=True)
    mb.add_box(70, 990, -340, 340, 3, 30, C_CARBON, 1.0, stl=True)
    mb.add_box(58, 72, -335, 335, 1, 33, C_KEVLAR, 1.0, stl=True)  # Midship latch bar

    # Navigator 300 Transom-Clamped Hybrid C-Frame Twin Rails (2x 50x20 mm Alu rails spaced 250 mm apart, X = -830..+1090, Z = -22..-2)
    for sy in (-125, 125):
        mb.add_box(-830, 1095, sy - 22, sy + 22, -22, -2, C_ALU, 1.0, stl=True)
    # Transom C-Clamp vertical riser hooking right onto factory Tru-Alu transom (zero holes!)
    mb.add_box(1065, 1095, -160, 160, -22, 160, C_ALU, 1.0, stl=True)
    mb.add_box(1005, 1095, -160, 160, 140, 168, C_ALU, 1.0, stl=True)  # Over-transom clamp lip
    mb.add_box(990, 1035, -160, 160, 28, 155, C_ALU, 1.0, stl=True)    # Inside transom clamp jaw tying to Spine Floor!
    # Front crossbar tying the two rails at X = -830
    mb.add_box(-835, -805, -148, 148, -22, -2, C_ALU, 1.0, stl=True)

    # 6 mm High-Modulus Dyneema Bow-D-Ring Tieback Sling (kills front cantilever with ZERO holes in closed bow!)
    mb.add_rod((-820, -125, -12), (-1415, 0, -28), 7.5, C_DYNEEMA, n=8, alpha=1.0, stl=True)
    mb.add_rod((-820, 125, -12), (-1415, 0, -28), 7.5, C_DYNEEMA, n=8, alpha=1.0, stl=True)


def add_discovery_330_hull(mb: MeshBuilder, tube_alpha=0.40, stl_hull=True):
    """Secondary Open-Bow Reference: True Kit Discovery 330 (330 cm, open square bow, full rigid Bow-to-Transom O-Frame)."""
    stations = [
        (-1650, 22, 165, 40), (-1520, 125, 130, 30), (-1320, 195, 78, 14),
        (-1020, 230, 16, 0), (-400, 230, 0, 0), (500, 230, 0, 0),
        (1150, 230, 0, 0), (1420, 180, 0, 0), (1560, 55, 0, 0),
    ]
    n = 18
    for side in (-1, 1):
        sy = side * 620
        rings, strake_rings = [], []
        for x, r, zc, yin in stations:
            y_c = sy - side * yin
            rings.append([(x, y_c + r * math.cos(2 * math.pi * i / n), zc + r * math.sin(2 * math.pi * i / n)) for i in range(n)])
            yo = y_c + side * (r + 5)
            strake_rings.append([(x, yo - side * 8, zc - 22), (x, yo, zc - 18), (x, yo, zc + 18), (x, yo - side * 8, zc + 22)])
        mb.add_loft(rings, C_TUBE_GREY, alpha=tube_alpha, stl=stl_hull)
        mb.add_loft(strake_rings, C_RUB_STRAKE, alpha=min(0.85, tube_alpha + 0.35), stl=stl_hull)

    mb.add_cylinder_y(1080, -450, 450, 145, 22, C_ALU, n=10, alpha=0.92, stl=stl_hull)
    mb.add_cylinder_y(1080, -450, 450, 55, 18, C_ALU, n=10, alpha=0.92, stl=stl_hull)
    mb.add_box(-150, 110, -560, 560, 162, 185, C_SEAT, alpha=0.50, stl=False)
    mb.add_box(-950, -6, -410, 410, 3, 30, C_CARBON, 1.0, stl=True)
    mb.add_box(6, 950, -410, 410, 3, 30, C_CARBON, 1.0, stl=True)
    mb.add_box(-8, 8, -405, 405, 1, 33, C_KEVLAR, 1.0, stl=True)
    # Full Rigid Bow-to-Transom O-Frame
    for sy in (-135, 135):
        mb.add_box(-990, 990, sy - 25, sy + 25, -22, -2, C_ALU, 1.0, stl=True)
    for sx in (-990, 968):
        mb.add_box(sx, sx + 22, -165, 165, -22, 33, C_ALU, 1.0, stl=True)


def add_flying_keel_pod(mb: MeshBuilder, dx=0.0, dz=-780.0, pod_h=80.0, with_motors=True):
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
                ring.append((dx + x, ry * math.copysign(abs(ca) ** 0.85, ca), dz + rz * math.copysign(abs(sa) ** 0.85, sa)))
            out.append(ring)
        return out

    mb.add_loft(make_rings(stations[:3]), C_KEVLAR, 1.0, stl=True)
    mb.add_loft(make_rings(stations[2:]), C_CARBON, 1.0, stl=True)

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
                mb.add_quad(
                    (dx + 675, sy, dz), (dx + 686, sy + 18 * math.cos(ang + 0.5), dz + 18 * math.sin(ang + 0.5)),
                    (dx + 680, sy + 88 * math.cos(ang), dz + 88 * math.sin(ang)),
                    (dx + 672, sy + 18 * math.cos(ang - 0.5), dz + 18 * math.sin(ang - 0.5)),
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


def add_4x_blades(mb: MeshBuilder, z_top=-22.0, z_bot=-780.0, fold_deg=0.0, x_front=-450.0, x_rear=310.0, y_half=122.0):
    blade_sec = naca4_section(0.0, 0.0, 0.15, 60.0, n=10)
    L = abs(z_top - z_bot)
    th = math.radians(fold_deg)
    sx_dir, sz_dir = math.sin(th), -math.cos(th)
    cx_dir, cz_dir = math.cos(th), math.sin(th)
    for bx in (x_front, x_rear):
        for sy in (-y_half, y_half):
            rings = []
            for s_pos in (0.0, L * 0.5, L):
                ring = []
                for xl, yl in blade_sec:
                    xc = xl - 30.0
                    ring.append((bx + s_pos * sx_dir + xc * cx_dir, sy + yl, z_top + s_pos * sz_dir + xc * cz_dir))
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
            ring.append((x_off + xs * math.cos(rad) + zs * math.sin(rad), y, dz - xs * math.sin(rad) + zs * math.cos(rad)))
        rings.append(ring)
    mb.add_loft(rings, C_WING_UP, 1.0, stl=True)
    mb.add_box(dx + 300, dx + 330, -125, 125, dz - 5, dz + 5, C_ALU, 1.0, stl=True)


def add_plane_grid(mb: MeshBuilder, z_val, color, alpha, wx0=-1750, wx1=1700, wy0=-1050, wy1=1050, n=7):
    for ix in range(n):
        for iy in range(n):
            xa = wx0 + (wx1 - wx0) * ix / n
            xb = wx0 + (wx1 - wx0) * (ix + 1) / n
            ya = wy0 + (wy1 - wy0) * iy / n
            yb = wy0 + (wy1 - wy0) * (iy + 1) / n
            mb.add_quad((xa, ya, z_val), (xb, ya, z_val), (xb, yb, z_val), (xa, yb, z_val), color, alpha, stl=False)


def write_binary_stl(mb: MeshBuilder, path: Path, desc: str):
    stl_tris = [t for t in mb.tris if t[5]]
    header = desc.encode("ascii", "ignore")[:80].ljust(80, b" ")
    with open(path, "wb") as f:
        f.write(header)
        f.write(struct.pack("<I", len(stl_tris)))
        for p0, p1, p2, _, _, _ in stl_tris:
            n = v_norm(v_cross(v_sub(p1, p0), v_sub(p2, p0)))
            f.write(struct.pack("<3f3f3f3fH", *n, *p0, *p1, *p2, 0))
    print(f"STL: {path.name:44s} | {len(stl_tris):4d} tris | {path.stat().st_size/1024:5.1f} KB")


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
        projected.append((depth, q0, q1, q2, f"rgb({min(255,int(col[0]*shade))},{min(255,int(col[1]*shade))},{min(255,int(col[2]*shade))})", alpha, is_stl))
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
    print(f"SVG: {path.name:44s} | {path.stat().st_size/1024:5.1f} KB")


def render_openscad_png(mb: MeshBuilder, png_path: Path, camera: str, imgsize="1400,860"):
    openscad = shutil.which("openscad") or "/opt/homebrew/bin/openscad"
    if not Path(openscad).exists():
        print("OpenSCAD not found; skipping PNG render for", png_path.name)
        return
    RENDERS_DIR.mkdir(parents=True, exist_ok=True)
    groups = defaultdict(list)
    for p0, p1, p2, col, alpha, _ in mb.tris:
        groups[(col, round(alpha, 2))].append((p0, p1, p2))

    ordered_keys = sorted(groups.keys(), key=lambda k: (-k[1], k[0]))
    scad_lines = ["// Auto-generated multi-material OpenSCAD render scene for FoilSkiff\n"]
    for (r, g, b), alpha in ordered_keys:
        tris = groups[((r, g, b), alpha)]
        pt_map, pts, faces = {}, [], []
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
    res = subprocess.run(
        [openscad, f"--imgsize={imgsize}", "--colorscheme=Tomorrow", f"--camera={camera}", "-o", str(png_path), str(tmp_scad)],
        capture_output=True, text=True,
    )
    if res.returncode == 0 and png_path.exists():
        print(f"PNG: {png_path.name:44s} | {png_path.stat().st_size/1024:5.1f} KB (OpenSCAD)")
    else:
        print(f"OpenSCAD render failed for {png_path.name}: {res.stderr[:200]}")


# ---------------------------------------------------------------------------
# MODEL 1 (PRIMARY): True Kit Navigator 300 + Hybrid C-Frame + Step-Out Pod
# ---------------------------------------------------------------------------
def build_model_01_navigator300():
    mb = MeshBuilder()
    add_navigator_300_hull(mb, tube_alpha=0.38, stl_hull=True)
    add_4x_blades(mb, z_top=-22, z_bot=-780, fold_deg=0, x_front=-440, x_rear=320, y_half=122)
    add_upper_step_out_wing(mb, dx=0, dz=-310, x_le=-460)
    add_flying_keel_pod(mb, dx=0, dz=-780)
    add_lower_wings(mb, dx=0, dz=-790, half_span=670, root_chord=115)
    add_plane_grid(mb, -380.0, C_WATER, 0.16)
    write_binary_stl(mb, MODELS_DIR / "01_navigator300_step_out_flying_keel.stl", "FoilSkiff 01 (PRIMARY): True Kit Navigator 300 + Step-Out Flying-Keel (mm)")
    callouts = [
        ((-1410, 0, 150), "left", 102, 235, "Closed Curved Bow Tube (3+1 Ch.)", "True Kit Navigator 300 • 300×155 cm, 31 kg"),
        ((-1120, 62, -20), "left", 215, 240, "6 mm Dyneema Bow-D-Ring Sling", "Eliminates front cantilever • Zero hull holes!"),
        ((-420, 480, -310), "left", 345, 230, "Upper Step-Out Booster Wing", "+1,400 cm² • Flies IN AIR >9 kn!"),
        ((-635, 0, -780), "left", 485, 235, "20 mm Kevlar Crush-Nose Cone", "Ahead of 26 L swappable battery bay"),
        ((1050, -300, 220), "right", 104, 800, "Factory Tru-Alu Rigid Transom", "Hybrid C-Frame clamps directly (0 holes!)"),
        ((320, -122, -450), "right", 232, 805, "4× Side-Straddling Blades", "60×9 mm • Fits 600 mm inside tunnel cleanly"),
        ((640, -135, -780), "right", 392, 795, "2× Flipsky 65161 Tailcone Pods", "CAN-bus 360° differential steering"),
        ((-150, -640, -780), "right", 510, 810, "1,350 cm² Lower Thin Wings", "t/c = 10% • 30.8 nm @ 15.5 kn"),
    ]
    render_3d_svg(
        mb, DIAG_DIR / "00-navigator300-3d-cad.svg",
        "3D CAD Model 1 (PRIMARY): True Kit Navigator 300 + Step-Out Flying-Keel Pod",
        "300×155 cm (60 cm inside beam, Ø460 mm tubes) • Tru-Alu Transom-Clamped Hybrid C-Frame + Bow-D-Ring Dyneema Sling",
        callouts, az_deg=-138, el_deg=20, scale=0.295, z_center=300,
        footer="Interactive 3D STL: models/01_navigator300_step_out_flying_keel.stl (click on GitHub to orbit/zoom or 3D-print at 1:15 scale)",
    )
    render_openscad_png(mb, RENDERS_DIR / "01-navigator300-step-out-3d.png", "0,0,-300,76,0,224,4950")


# ---------------------------------------------------------------------------
# MODEL 2: Flush-Nested Top-Deck Switchblade Wing Pod (Fits Navigator & Discovery)
# ---------------------------------------------------------------------------
def build_model_02_switchblade():
    mb = MeshBuilder()
    for sy in (-125, 125):
        mb.add_box(-760, 760, sy - 22, sy + 22, -22, -2, C_ALU, 1.0, stl=True)
    add_4x_blades(mb, z_top=-22, z_bot=-620, fold_deg=0, x_front=-480, x_rear=310, y_half=122)
    add_flying_keel_pod(mb, dx=0, dz=-620, pod_h=90.0)
    add_lower_wings(mb, dx=0, dz=-640, half_span=620, root_chord=108, x_le=-170)

    mb.add_box(-435, -365, -112, 112, -578, -564, C_CARBON_DARK, 1.0, stl=True)
    sw_sec = naca4_section(0.02, 0.4, 0.12, 105.0, n=10)
    for side in (-1, 1):
        rings = []
        for dist in (40, 110, 350, 620, 790):
            taper = 1.0 - 0.18 * (dist / 790.0) ** 2
            rings.append([(-415 + xl * taper, side * dist, -575 + zl * taper) for xl, zl in sw_sec])
        mb.add_loft(rings, C_WING_UP, 1.0, stl=True)
        mb.add_box(-405, -385, side * 35 - 10, side * 35 + 10, -582, -560, C_KEVLAR, 1.0, stl=True)
        mb.add_box(-415, 265, side * 52 - 48, side * 52 + 48, -576, -569, C_FLAP_L, 0.25, stl=False)

    write_binary_stl(mb, MODELS_DIR / "02_switchblade_pod.stl", "FoilSkiff 02: Flush-Nested Top-Deck Switchblade Wing Pod (mm)")
    callouts = [
        ((-400, 680, -575), "left", 130, 255, "Switchblade Blades Deployed (+1,300 cm²)", "2× 680×105×13 mm UD carbon • 1.58 m span"),
        ((-400, 0, -570), "left", 255, 255, "70 mm Carbon Overhang Bridge", "Reacts upward lift in pure compression!"),
        ((-635, 0, -620), "left", 425, 245, "90 mm Lifting Battery-Fuselage", "+10 mm height preserves full 26 L bay"),
        ((-480, -122, -300), "right", 130, 795, "4× Blades at x=170 & x=960 mm", "790 mm unobstructed sweep arc between pairs"),
        ((40, -50, -572), "right", 265, 795, "Flush Top-Deck Recess (Translucent)", "0 cm² extra wet area when closed @ >9 kn!"),
        ((-120, -580, -635), "right", 420, 800, "1,250 cm² Fixed Lower Thin Wings", "30.8 nm @ 15.5 kn • 32.3 lbf @ 22 kn (best pod!)"),
    ]
    render_3d_svg(
        mb, DIAG_DIR / "06-switchblade-3d-cad.svg",
        "3D CAD Model 2: Flush-Nested Top-Deck Switchblade Wing Pod (Navigator & Discovery)",
        "Zero surface-piercing chop risk • Blades nest 100% flush into fuselage roof at >9 kn (0 cm² extra wet area)",
        callouts, az_deg=-134, el_deg=26, scale=0.38, z_center=340,
        footer="Interactive 3D STL: models/02_switchblade_pod.stl (universal pod module for Navigator 300 & Discovery 330)",
    )
    render_openscad_png(mb, RENDERS_DIR / "02-switchblade-pod-3d.png", "-50,0,-350,60,0,228,3650")


# ---------------------------------------------------------------------------
# MODEL 3: Submerged Split STOL Flaperons (Fits Navigator & Discovery)
# ---------------------------------------------------------------------------
def build_model_03_stol_flaperons():
    mb = MeshBuilder()
    mb.add_box(-760, 760, -240, 240, 4, 24, C_CARBON, 0.85, stl=True)
    for sy in (-125, 125):
        mb.add_box(-760, 760, sy - 22, sy + 22, -22, -2, C_ALU, 1.0, stl=True)
        mb.add_box(275, 345, sy - 20, sy + 20, 24, 66, C_KEVLAR, 1.0, stl=True)
        mb.add_box(338, 346, sy - 3, sy + 3, -648, 35, C_PUSHROD, 1.0, stl=True)

    add_4x_blades(mb, z_top=-22, z_bot=-620, fold_deg=0, x_front=-420, x_rear=310, y_half=122)
    add_flying_keel_pod(mb, dx=0, dz=-620, pod_h=80.0)
    add_lower_wings(mb, dx=0, dz=-622, half_span=525, root_chord=100, x_le=-245)

    fl_sec = naca4_section(0.02, 0.4, 0.11, 62.0, n=10)
    for side, deg, col in [(-1, 18.0, C_FLAP_L), (1, -8.0, C_FLAP_R)]:
        rad = math.radians(deg)
        rings = []
        for dist in (115, 320, 545):
            y = side * dist
            rings.append([(-92 + (xl - 12.4) * math.cos(rad) + zl * math.sin(rad), y, -652 - (xl - 12.4) * math.sin(rad) + zl * math.cos(rad)) for xl, zl in fl_sec])
        mb.add_loft(rings, col, 1.0, stl=True)
        mb.add_box(-92, 342, side * 124 - 4, side * 124 + 4, -648, -640, C_PUSHROD, 1.0, stl=True)

    write_binary_stl(mb, MODELS_DIR / "03_stol_flaperon_pod.stl", "FoilSkiff 03: Submerged Split STOL Flaperon Active-Control Pod (mm)")
    callouts = [
        ((310, 125, 50), "left", 118, 250, "2× Dry Deck IP67 Brushless Servos", "70–80 kg·cm (~$60 ea.) safely ABOVE water"),
        ((-100, 480, -648), "left", 275, 250, "Starboard 250 cm² Flaperon (-8° Up)", "Differential left/right = Active Roll & Banked Turns"),
        ((-635, 0, -620), "left", 445, 245, "Submerged 400 mm Deep Permanently", "Zero surface-piercing ventilation in 2 ft chop!"),
        ((342, -125, -310), "right", 145, 790, "4 mm Stainless Pushrods", "Tucked in rear blade trailing-edge grooves"),
        ((-180, -480, -625), "right", 315, 800, "Compact 1,000 cm² Speed Main Wing", "Shrunk span • 29.8 nm @ 15.5 kn"),
        ((-92, -480, -660), "right", 455, 795, "Port 250 cm² STOL Flaperon (+18° Down)", "Junkers slot jet (CL_max ≈ 2.0) • 20% failsafe pivot"),
    ]
    render_3d_svg(
        mb, DIAG_DIR / "07-stol-flaperons-3d-cad.svg",
        "3D CAD Model 3: Submerged Split STOL Flaperons (1,000 + 2×250 cm² Active Control)",
        "Shown in differential roll/bank (+18° Port / -8° Starboard) • Dry-deck servos + 4 mm pushrods (~$160 active BOM)",
        callouts, az_deg=-138, el_deg=23, scale=0.41, z_center=320,
        footer="Interactive 3D STL: models/03_stol_flaperon_pod.stl (universal pod module for Navigator 300 & Discovery 330)",
    )
    render_openscad_png(mb, RENDERS_DIR / "03-stol-flaperon-pod-3d.png", "20,0,-330,66,0,224,2950")


# ---------------------------------------------------------------------------
# MODEL 4 (PRIMARY): True Kit Navigator 300 Retracted Beaching Mode (85° Fold)
# ---------------------------------------------------------------------------
def build_model_04_navigator300_retracted():
    mb = MeshBuilder()
    add_navigator_300_hull(mb, tube_alpha=0.42, stl_hull=True)
    # Place front/rear pivots slightly forward so 85° folded pod tucks cleanly inside the 300 cm hull & clears Tru-Alu transom!
    dx_pod, _ = add_4x_blades(mb, z_top=-20, z_bot=-580, fold_deg=85.0, x_front=-620, x_rear=140, y_half=122)
    add_flying_keel_pod(mb, dx=dx_pod * 0.78, dz=-56.0, pod_h=80.0)
    add_lower_wings(mb, dx=dx_pod * 0.78, dz=-66.0, half_span=650, root_chord=112)
    add_plane_grid(mb, -232.0, C_SAND, 0.32, n=6)

    write_binary_stl(mb, MODELS_DIR / "04_navigator300_retracted_beaching.stl", "FoilSkiff 04 (PRIMARY): True Kit Navigator 300 Retracted 85-deg Beaching (mm)")
    callouts = [
        ((-1410, 0, 150), "left", 112, 235, "Navigator 300 Closed Bow on Sand", "Ø460 mm tubes sit cleanly on beach (Z = -232 mm)"),
        ((-360, 122, -45), "left", 248, 240, "4× Side-Straddling Blades Folded 85°", "60 mm chords fold BESIDE 80 mm pod (zero stack!)"),
        ((dx_pod * 0.78 - 480, 0, -56), "left", 425, 240, "Pod Stays 100% Horizontal!", "Tucked cleanly between 250 mm rails @ Z = -96 mm"),
        ((1050, -240, 180), "right", 122, 800, "Clears Beneath Tru-Alu Transom!", "Pod slides smoothly under open-bottom transom"),
        ((dx_pod * 0.78 + 620, -135, -56), "right", 285, 795, "Props Protected Inside Rear Cones", "Within 300 cm LOA, high & dry above sand"),
        ((150, -400, -165), "right", 455, 800, "~135–140 mm (5.5\") Sand Clearance!", "Zero nose-plowing or PVC ceiling collision"),
    ]
    render_3d_svg(
        mb, DIAG_DIR / "08-navigator300-retracted-3d.svg",
        "3D CAD Model 4 (PRIMARY): True Kit Navigator 300 Retracted Beaching Mode (85° Fold)",
        "4× Side-Straddling Blades fold flat beside the 80 mm pod beneath the Tru-Alu transom — ~5.5\" clear above flat sand!",
        callouts, az_deg=-138, el_deg=14, scale=0.295, z_center=120,
        footer="Interactive 3D STL: models/04_navigator300_retracted_beaching.stl (click on GitHub to inspect under-tunnel clearance in 3D)",
    )
    # Eye-level open-transom / side-quarter view showing under-transom & tunnel sand clearance clearly!
    render_openscad_png(mb, RENDERS_DIR / "04-navigator300-retracted-3d.png", "40,0,-95,93,0,248,4150")


# ---------------------------------------------------------------------------
# MODEL 5 (SECONDARY REFERENCE): True Kit Discovery 330 Open-Bow Full O-Frame
# ---------------------------------------------------------------------------
def build_model_05_discovery330():
    mb = MeshBuilder()
    add_discovery_330_hull(mb, tube_alpha=0.40, stl_hull=True)
    add_4x_blades(mb, z_top=-22, z_bot=-780, fold_deg=0, x_front=-450, x_rear=310, y_half=124)
    add_upper_step_out_wing(mb, dx=0, dz=-310)
    add_flying_keel_pod(mb, dx=0, dz=-780)
    add_lower_wings(mb, dx=0, dz=-790, half_span=670, root_chord=115)
    add_plane_grid(mb, -380.0, C_WATER, 0.16)
    write_binary_stl(mb, MODELS_DIR / "05_discovery330_oframe_step_out.stl", "FoilSkiff 05 (Secondary): True Kit Discovery 330 Open-Bow Full O-Frame (mm)")
    callouts = [
        ((-500, 0, 28), "left", 104, 240, "Drop-In 2-Piece Rigid Spine Floor", "Universal 650 mm Spine Core + Discovery width strips"),
        ((-980, 135, -10), "left", 205, 225, "Full Rigid Bow-to-Transom O-Frame", "Wraps BOTH open square bow & open transom!"),
        ((-420, 480, -310), "left", 340, 230, "Upper Step-Out Booster Wing", "+1,400 cm² • Flies IN AIR >9 kn!"),
        ((-635, 0, -780), "left", 482, 235, "Identical Swappable Flying-Keel Pod", "100% interchangeable between Navigator & Discovery"),
        ((950, -620, 120), "right", 108, 810, "True Kit Discovery 330 (Open Bow)", "330 cm landing-craft hull / Takacat LX equivalent"),
        ((310, -124, -460), "right", 232, 810, "4× Side-Straddling Blades", "60×9 mm • Folds to ~90 mm flat!"),
        ((640, -135, -780), "right", 392, 795, "2× Flipsky 65161 Tailcone Pods", "CAN-bus 360° differential steering"),
        ((-150, -640, -780), "right", 508, 810, "1,350 cm² Lower Thin Wings", "t/c = 10% • 30.8 nm @ 15.5 kn"),
    ]
    render_3d_svg(
        mb, DIAG_DIR / "11-discovery330-oframe-3d-cad.svg",
        "3D CAD Model 5 (Secondary Open-Bow Ref): True Kit Discovery 330 + Full O-Frame",
        "Demonstrates full rigid Bow-to-Transom O-Frame wrapping open square bow (also applies to Takacat LX)",
        callouts, az_deg=-140, el_deg=20, scale=0.285, z_center=300,
        footer="Interactive 3D STL: models/05_discovery330_oframe_step_out.stl (secondary open-bow hull reference)",
    )
    render_openscad_png(mb, RENDERS_DIR / "05-discovery330-oframe-3d.png", "0,0,-310,77,0,222,5200")


if __name__ == "__main__":
    # Clean superseded Discovery-primary filenames before regenerating clean 01..05 set
    for old_f in [
        MODELS_DIR / "01_step_out_flying_keel_truekit.stl",
        MODELS_DIR / "04_retracted_beaching_truekit.stl",
        DIAG_DIR / "00-foil-skiff-3d-cad.svg",
        DIAG_DIR / "08-retracted-beaching-3d.svg",
        RENDERS_DIR / "01-step-out-truekit-3d.png",
        RENDERS_DIR / "04-retracted-beaching-3d.png",
    ]:
        if old_f.exists():
            old_f.unlink()

    build_model_01_navigator300()
    build_model_02_switchblade()
    build_model_03_stol_flaperons()
    build_model_04_navigator300_retracted()
    build_model_05_discovery330()
    print("All 5 3D STL models, 5 annotated 3D SVGs, and 5 OpenSCAD PNG renders generated successfully.")
