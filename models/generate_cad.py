#!/usr/bin/env python3
"""
Parametric 3D CAD & Semi-Realistic Rendering Generator for FoilSkiff.
Primary Reference Hull: True Kit Navigator 300 (300 x 155 cm, 60 cm inside beam, Ø460 mm tubes,
closed continuous bow tube, factory Tru-Alu rigid transom, 31 kg bare hull).
Secondary Open-Bow Reference: True Kit Discovery 330 (330 cm, open square bow, full rigid O-Frame).

Zero external Python dependencies (pure Python 3 standard library + optional OpenSCAD CLI).

Generates 10 interactive binary 3D STL CAD models, 10 shaded 3D isometric SVGs, and 10 OpenSCAD PNGs:
  1. models/01_navigator300_stol_flaperons.stl       + renders/01-navigator300-stol-3d.png          + diagrams/00-navigator300-3d-cad.svg
  2. models/02_switchblade_pod.stl                   + renders/02-switchblade-pod-3d.png            + diagrams/06-switchblade-3d-cad.svg
  3. models/03_stol_flaperon_pod.stl                 + renders/03-stol-flaperon-pod-3d.png          + diagrams/07-stol-flaperons-3d-cad.svg
  4. models/04_navigator300_retracted_beaching.stl   + renders/04-navigator300-retracted-3d.png     + diagrams/08-navigator300-retracted-3d.svg
  5. models/05_discovery330_oframe_stol.stl          + renders/05-discovery330-oframe-3d.png        + diagrams/11-discovery330-oframe-3d-cad.svg
  6. models/06_navigator300_lr_8020_sweetspot.stl    + renders/06-navigator300-lr-8020-3d.png       + diagrams/13-navigator300-lr-8020-3d-cad.svg
  7. models/07_navigator300_lr_max_range.stl         + renders/07-navigator300-lr-max-range-3d.png  + diagrams/14-navigator300-lr-max-range-3d-cad.svg
  8. models/08_lr_pod_closeup.stl                    + renders/08-lr-pod-closeup-3d.png             + diagrams/15-lr-pod-closeup-3d-cad.svg
  9. models/09_modular_hard_deck_seating.stl         + renders/09-modular-deck-seating-3d.png       + diagrams/17-modular-deck-seating-3d-cad.svg
 10. models/10_morphing_stol_staggerwing_pod.stl     + renders/10-morphing-stol-staggerwing-3d.png  + diagrams/19-morphing-stol-staggerwing-3d-cad.svg
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


def add_contoured_deck_and_underplate(mb: MeshBuilder, stations_deck, stations_under, latch_x=65.0):
    """
    Lofted contoured 2-piece Hard Deck (top Spine Floor) and contoured under-hull carriage plate/rails
    following BOTH the curved bow planform AND the upward bow rocker bend (NOT flat rectangles!).
    Zero protruding boxes above the top deck!
    """
    rear_st = [s for s in stations_deck if s[0] >= latch_x]
    front_st = [s for s in stations_deck if s[0] <= latch_x]

    def loft_slab(st_list, col, alpha=1.0, stl=True):
        rings = []
        for x, hw, zb, zt in st_list:
            bev = min(22.0, hw * 0.25)
            rings.append([
                (x, -hw + bev, zb),
                (x, hw - bev, zb),
                (x, hw, (zb + zt) * 0.5),
                (x, hw - bev * 0.5, zt),
                (x, -hw + bev * 0.5, zt),
                (x, -hw, (zb + zt) * 0.5),
            ])
        mb.add_loft(rings, col, alpha=alpha, stl=stl)

    loft_slab(rear_st, C_CARBON, 1.0, stl=True)
    loft_slab(front_st, C_CARBON, 1.0, stl=True)
    hw_l = rear_st[0][1] - 10
    mb.add_box(latch_x - 6, latch_x + 6, -hw_l, hw_l, 2, 31, C_KEVLAR, 1.0, stl=True)
    loft_slab(stations_under, C_ALU, 1.0, stl=True)


def add_flush_ltracks(mb: MeshBuilder, z_top=30.0, x0=-680.0, x1=890.0, y_track=195.0):
    """
    Twin marine-anodized flush-recessed L-Track / T-Track mounting rails (390 mm center spacing,
    100% flush with Hard Deck top surface — ZERO trip hazard when chairs are unclipped!).
    Supports 0 chairs (open deck), 1 chair (Solo @ CoG), or 2 chairs (Tandem Long-Range).
    """
    for sy in (-y_track, y_track):
        mb.add_box(x0, x1, sy - 16, sy + 16, z_top - 4, z_top + 1.5, C_ALU, 1.0, stl=True)
        # Inner recessed slot stripe
        mb.add_box(x0 + 8, x1 - 8, sy - 6, sy + 6, z_top + 1.0, z_top + 2.0, C_CARBON_DARK, 1.0, stl=False)


def add_low_sit_chair(mb: MeshBuilder, x_hip=0.0, z_deck=63.0, y_track=195.0, with_armrest_helm=False):
    """
    Ergonomic low-slung touring chair (Hobie Vantage / recumbent kayak style, ~2.5 kg):
      - Width: 430 mm (fits cleanly inside Navigator 300 600 mm tunnel with 85 mm/side tube clearance!)
      - Seat pan: ~125 mm above Hard Deck (lowers crew CoG ~250 mm & drops head behind bow dodger!)
      - Reclined 22 deg lumbar backrest + 4x gold spring-loaded L-Track double-stud quick-release feet
      - Optional starboard armrest wireless thumb-throttle + 2-axis steering/trim joystick pod!
    """
    hw = 212.0  # 424 mm total chair width
    z_pan_back = z_deck + 118.0
    z_pan_front = z_deck + 148.0  # Slight ergonomic thigh-support tilt!
    # 1. Tubular anodized aluminum frame & 4x quick-release L-Track double-stud feet
    for side in (-1, 1):
        yt = side * y_track
        # Lower L-Track slide shoe + gold quick-release locking studs (front & rear)
        mb.add_box(x_hip - 225, x_hip + 145, yt - 13, yt + 13, z_deck, z_deck + 16, C_ALU, 1.0, stl=True)
        mb.add_box(x_hip - 210, x_hip - 175, yt - 15, yt + 15, z_deck + 14, z_deck + 28, C_KEVLAR, 1.0, stl=True)
        mb.add_box(x_hip + 95, x_hip + 130, yt - 15, yt + 15, z_deck + 14, z_deck + 28, C_KEVLAR, 1.0, stl=True)
        # Front & rear A-frame risers from L-Track shoes to ergonomic seat frame
        mb.add_rod((x_hip - 190, yt, z_deck + 14), (x_hip - 245, side * hw, z_pan_front), 10.0, C_ALU, n=8, alpha=1.0, stl=True)
        mb.add_rod((x_hip + 110, yt, z_deck + 14), (x_hip + 115, side * hw, z_pan_back), 10.0, C_ALU, n=8, alpha=1.0, stl=True)
        # Side seat frame rail
        mb.add_rod((x_hip - 245, side * hw, z_pan_front), (x_hip + 115, side * hw, z_pan_back), 11.0, C_ALU, n=8, alpha=1.0, stl=True)
        # Reclined 22 deg ergonomic backrest side upright (+430 mm tall!)
        mb.add_rod((x_hip + 115, side * hw, z_pan_back), (x_hip + 280, side * (hw - 12), z_pan_back + 400), 11.0, C_ALU, n=8, alpha=1.0, stl=True)

    # Top headrest crossbar & front thigh bolster tube
    mb.add_cylinder_y(x_hip + 280, -(hw - 12), hw - 12, z_pan_back + 400, 11.0, C_ALU, n=8, alpha=1.0, stl=True)
    mb.add_cylinder_y(x_hip - 245, -hw, hw, z_pan_front, 11.0, C_ALU, n=8, alpha=1.0, stl=True)

    # 2. Contoured breathable mesh / molded carbon seat pan (lofted!)
    pan_st = [
        (x_hip - 242, hw - 8, z_pan_front - 6, z_pan_front + 12),
        (x_hip - 80, hw - 6, z_pan_front - 18, z_pan_front),
        (x_hip + 112, hw - 8, z_pan_back - 8, z_pan_back + 10),
    ]
    pan_rings = [[(x, -w, zb), (x, w, zb), (x, w, zt), (x, -w, zt)] for x, w, zb, zt in pan_st]
    mb.add_loft(pan_rings, C_SEAT, 0.96, stl=True)

    # 3. Contoured reclined lumbar backrest sling/shell (lofted 22 deg recline with gentle lumbar curve!)
    back_st = [
        (x_hip + 118, hw - 10, z_pan_back + 14),
        (x_hip + 168, hw - 12, z_pan_back + 145),   # Ergonomic lumbar support curve
        (x_hip + 225, hw - 15, z_pan_back + 275),
        (x_hip + 276, hw - 18, z_pan_back + 394),
    ]
    b_rings = [[(x - 10, -w, z), (x - 10, w, z), (x + 10, w, z), (x + 10, -w, z)] for x, w, z in back_st]
    mb.add_loft(b_rings, C_SEAT, 0.96, stl=True)

    # 4. Optional Integrated Starboard (Right-Hand facing -X bow -> +Y!) Armrest Wireless Helm Pod
    if with_armrest_helm:
        ya = hw + 12.0  # Right hand (Starboard = +Y when facing bow -X!)
        z_arm = z_pan_back + 175.0
        mb.add_rod((x_hip + 150, hw, z_pan_back + 115), (x_hip + 130, ya, z_arm), 8.5, C_ALU, n=8, alpha=1.0, stl=True)
        mb.add_rod((x_hip - 125, hw, z_pan_front), (x_hip - 120, ya, z_arm), 8.5, C_ALU, n=8, alpha=1.0, stl=True)
        mb.add_box(x_hip - 155, x_hip + 138, ya - 22, ya + 22, z_arm - 10, z_arm + 14, C_CARBON_DARK, 1.0, stl=True)
        mb.add_box(x_hip - 175, x_hip - 120, ya - 20, ya + 20, z_arm + 12, z_arm + 40, C_FLAP_R, 1.0, stl=True)
        mb.add_rod((x_hip - 148, ya, z_arm + 38), (x_hip - 158, ya, z_arm + 84), 6.5, C_KEVLAR, n=8, alpha=1.0, stl=True)


def add_navigator_300_hull(mb: MeshBuilder, tube_alpha=0.38, stl_hull=True, deck_thick=28.0, with_bow_dodger=False, show_bench_seats=True, with_ltracks=True):
    """
    Semi-realistic True Kit Navigator 300 (PRIMARY HULL):
      - LOA: 300 cm, External Beam: 155 cm, Inside Beam: 60 cm, Tube Ø460 mm
      - Contoured 2-Piece Rigid Hard Deck (28 mm standard OR 60 mm Dual-Pack Battery-Floor) + Flush Recessed Twin L-Tracks
      - Optional Low-Profile Curved Bow Spray Dodger (Swap #4 Aero Trim for 60-75 nm expedition runs)
      - Factory Tru-Alu Rigid Aluminum Transom + 6 mm Dyneema Bow-D-Ring Sling (ZERO protruding boxes above deck!)
    """
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
        (-1445, 0, 162, 186),
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

    strake_path = []
    for x, y, z, r in path[1:-1]:
        if abs(y) > 450 and x > -900:
            sy = y + math.copysign(r + 6, y)
            strake_path.append((x, sy, z, 18))
        else:
            ang = math.atan2(y, x + 900)
            strake_path.append((x + (r + 6) * math.cos(ang), y + (r + 6) * math.sin(ang), z, 18))
    mb.add_tube_along_path(strake_path, C_RUB_STRAKE, n=8, alpha=min(0.85, tube_alpha + 0.35), stl=stl_hull, cap_ends=True)

    mb.add_box(1035, 1065, -455, 455, -8, 260, C_TRANSOM_ALU, alpha=0.88, stl=stl_hull)
    mb.add_box(1035, 1065, -455, -180, 260, 335, C_TRANSOM_ALU, alpha=0.88, stl=stl_hull)
    mb.add_box(1035, 1065, 180, 455, 260, 335, C_TRANSOM_ALU, alpha=0.88, stl=stl_hull)

    if show_bench_seats:
        mb.add_box(-520, -320, -490, 490, 170, 192, C_SEAT, alpha=0.45, stl=False)
        mb.add_box(320, 520, -490, 490, 170, 192, C_SEAT, alpha=0.45, stl=False)

    # Factory Bow Towing D-Ring under raised curved bow nose
    mb.add_box(-1455, -1420, -28, 28, 8, 36, C_KEVLAR, 1.0, stl=True)

    # Contoured 2-Piece Hard Deck (28 mm standard OR 60 mm Dry Battery-Floor housing 5.38 kWh EVE LF105 cells!)
    dt = deck_thick
    deck_stations = [
        (-1245, 95, 86, 86 + min(dt, 32.0)),
        (-1160, 185, 62, 62 + min(dt, 38.0)),
        (-1030, 268, 34, 34 + min(dt, 48.0)),
        (-880, 322, 12, 12 + dt),
        (-720, 340, 3, 3 + dt),
        (60, 340, 3, 3 + dt),
        (72, 340, 3, 3 + dt),
        (990, 340, 3, 3 + dt),
    ]
    under_stations = [
        (-1175, 115, 52, 62),
        (-1030, 148, 22, 32),
        (-880, 154, -2, 10),
        (-720, 152, -16, -2),
        (1095, 152, -16, -2),
    ]
    add_contoured_deck_and_underplate(mb, deck_stations, under_stations, latch_x=66.0)

    if with_ltracks:
        add_flush_ltracks(mb, z_top=3.0 + dt, x0=-680.0, x1=890.0, y_track=195.0)

    # Visual gold accent band on 60 mm Dual-Pack Battery-Floor edges so the 5.38 kWh deck pack is unmistakably clear!
    if deck_thick >= 50.0:
        mb.add_box(-680, 380, -342, 342, 18, 46, C_KEVLAR, 0.90, stl=False)

    for sy in (-125, 125):
        mb.add_box(-740, 1095, sy - 22, sy + 22, -24, -12, C_ALU, 1.0, stl=True)
    mb.add_box(1065, 1095, -160, 160, -24, 160, C_ALU, 1.0, stl=True)
    mb.add_box(1005, 1095, -160, 160, 140, 168, C_ALU, 1.0, stl=True)
    mb.add_box(990, 1035, -160, 160, 28, 155, C_ALU, 1.0, stl=True)

    mb.add_rod((-1170, -88, 56), (-1435, 0, 22), 7.5, C_DYNEEMA, n=8, alpha=1.0, stl=True)
    mb.add_rod((-1170, 88, 56), (-1435, 0, 22), 7.5, C_DYNEEMA, n=8, alpha=1.0, stl=True)

    # Optional Swap #4: Low-Profile Aerodynamic Bow Spray Dodger over the curved closed bow tube!
    if with_bow_dodger:
        dodger_st = [
            (-1460, 160, 330, 345),
            (-1320, 395, 315, 435),
            (-1080, 525, 275, 520),
            (-760, 565, 240, 585),
            (-480, 560, 232, 600),
        ]
        n_arc = 10
        d_rings = []
        for x, hw, z_base, z_crown in dodger_st:
            ring = []
            for i in range(n_arc + 1):
                a = math.pi * i / n_arc
                y = -hw * math.cos(a)
                z = z_base + (z_crown - z_base) * (math.sin(a) ** 0.78)
                ring.append((x, y, z))
            # Close arch back along thin 10 mm shell underside
            for i in range(n_arc, -1, -1):
                a = math.pi * i / n_arc
                y = -hw * math.cos(a)
                z = z_base + (z_crown - z_base) * (math.sin(a) ** 0.78) - 10.0
                ring.append((x, y, z))
            d_rings.append(ring)
        mb.add_loft(d_rings, C_WING_UP, alpha=0.45, stl=stl_hull)
        # Sleek aluminum arch frame hoop at aft edge of dodger
        arch_pts = []
        for i in range(n_arc + 1):
            a = math.pi * i / n_arc
            arch_pts.append((-480, -560 * math.cos(a), 232 + 368 * (math.sin(a) ** 0.78), 11))
        mb.add_tube_along_path(arch_pts, C_ALU, n=8, alpha=0.95, stl=stl_hull, cap_ends=True)


def add_discovery_330_hull(mb: MeshBuilder, tube_alpha=0.38, stl_hull=True):
    """Secondary Open-Bow Reference: True Kit Discovery 330 with Contoured Bow-Bent Hard Deck & Full O-Frame."""
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
    mb.add_box(-150, 110, -560, 560, 162, 185, C_SEAT, alpha=0.45, stl=False)

    deck_stations = [
        (-1240, 345, 62, 88),
        (-1060, 395, 22, 48),
        (-860, 410, 3, 30),
        (-6, 410, 3, 30),
        (6, 410, 3, 30),
        (950, 410, 3, 30),
    ]
    under_stations = [
        (-1245, 162, 48, 59),
        (-1060, 162, 8, 19),
        (-860, 162, -16, -2),
        (990, 162, -16, -2),
    ]
    add_contoured_deck_and_underplate(mb, deck_stations, under_stations, latch_x=0.0)
    for sy in (-135, 135):
        mb.add_box(-860, 990, sy - 24, sy + 24, -24, -12, C_ALU, 1.0, stl=True)
    mb.add_box(-1265, -1240, -165, 165, 48, 92, C_ALU, 1.0, stl=True)
    mb.add_box(968, 990, -165, 165, -24, 34, C_ALU, 1.0, stl=True)


def add_flying_keel_pod(mb: MeshBuilder, dx=0.0, dz=-702.0, pod_h=80.0, with_motors=True, shell_alpha=1.0):
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
    mb.add_loft(make_rings(stations[2:]), C_CARBON, shell_alpha, stl=True)

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


def add_stol_flaperons_and_servos(mb: MeshBuilder, dx=0.0, dz=-702.0, deg_port=14.0, deg_stbd=14.0, linked_fold=False, show_internal=False):
    """
    PRIMARY WING ARCHITECTURE: Compact 1,000 cm² Main Wing + 2x 250 cm² Independent Split Junkers STOL Flaperons
    driven directly by 2x IP67 70-80 kg·cm brushless servos SEALED INSIDE THE FLYING-KEEL POD via Ø8 mm double-O-ring
    stainless torque tubes (ZERO protruding boxes above top Hard Deck, ZERO external brackets/hinges sticking out of hull!).
    When linked_fold=True, Main Wing folds TRUE 90° straight aft inside the 12 mm lower belly channel (200 mm inside 220 mm pod!)
    and flaperons fold TRUE 90° straight aft inside the 13 mm upper roof channel (220 mm total dart — fits between 250 mm rails!).
    """
    add_lower_wings(mb, dx=dx, dz=dz - (42.0 if linked_fold else 14.0), half_span=525.0, root_chord=100.0, x_le=-245.0, linked_fold=linked_fold)

    fl_sec = naca4_section(0.02, 0.4, 0.11, 60.0, n=10)
    piv_x = dx - 92.0
    piv_z = dz - 30.0

    # Flush Ø8 mm sealed direct-drive stainless torque tube along piv_z (ZERO protruding brackets outside hull!)
    mb.add_cylinder_y(piv_x, -116, 116, piv_z, 4.5, C_PUSHROD, n=10, alpha=1.0, stl=True)
    for side, deg, col in [(-1, deg_port, C_FLAP_L), (1, deg_stbd, C_FLAP_R)]:
        # Flush CNC double-O-ring cheek seal collar tucked cleanly inside the pod shoulder
        mb.add_cylinder_y(piv_x, side * 96, side * 112, piv_z, 7.0, C_CARBON_DARK, n=10, alpha=1.0, stl=True)
        rad = math.radians(0.0 if linked_fold else deg)
        if not linked_fold:
            rings = []
            for dist in (108, 320, 545):
                y = side * dist
                rings.append([(piv_x + (xl - 12.0) * math.cos(rad) + zl * math.sin(rad), y, piv_z - (xl - 12.0) * math.sin(rad) + zl * math.cos(rad)) for xl, zl in fl_sec])
            mb.add_loft(rings, col, 1.0, stl=True)
        else:
            # True 90° Upper Roof Fold Channel (13 mm recess): embedded rotating IP68 servo commands 0.0° flat-lock & rotates 90° WITH blade!
            flap_len = 435.0
            roof_z = dz + 40.0
            rings = []
            for frac in (0.0, 0.5, 1.0):
                bx = dx - 205.0 + frac * flap_len
                rings.append([(bx, side * 44.0 + side * (xl - 30.0), roof_z + zl) for xl, zl in fl_sec])
            mb.add_loft(rings, col, 1.0, stl=True)

    if show_internal:
        for side in (-1, 1):
            mb.add_box(piv_x - 24, piv_x + 24, side * 52 - 18, side * 52 + 18, dz - 36, dz + 8, C_KEVLAR, 1.0, stl=False)
            mb.add_rod((piv_x, side * 52, piv_z), (piv_x, side * 112, piv_z), 5.0, C_PUSHROD, n=8, alpha=1.0, stl=False)
        mb.add_box(piv_x + 36, piv_x + 108, -32, 32, dz - 10, dz + 16, C_WING_UP, 1.0, stl=False)
        mb.add_box(piv_x + 122, piv_x + 235, -68, 68, dz - 34, dz - 6, C_ALU, 1.0, stl=False)


def add_lower_wings(mb: MeshBuilder, dx=0.0, dz=-712.0, half_span=670.0, root_chord=115.0, x_le=-220.0, linked_fold=False):
    lo_sec = naca4_section(0.02, 0.4, 0.10, root_chord, n=12)
    if not linked_fold:
        ys = [-half_span, -half_span * 0.78, -half_span * 0.48, -96, 96, half_span * 0.48, half_span * 0.78, half_span]
        rings = []
        for y in ys:
            u = abs(y) / half_span
            taper = 1.0 - 0.42 * (u**1.8)
            sweep = 45 * (u**1.3)
            dih = 26 * (u**2.2)
            rings.append([(dx + x_le + sweep + xl * taper, y, dz + dih + zl * taper) for xl, zl in lo_sec])
        mb.add_loft(rings, C_WING_LOW, 1.0, stl=True)
    else:
        # True 90° Lower Belly Fold Channel (12 mm recess): pivots at y = ±54 mm -> 2×100 mm = 200 mm flush inside 220 mm pod!
        wing_len = half_span - 54.0
        x_piv = dx + x_le + 22.0
        for side in (-1, 1):
            rings = []
            for frac in (0.0, 0.45, 0.80, 1.0):
                u = (54.0 + frac * wing_len) / half_span
                taper = 1.0 - 0.42 * (u**1.8)
                bx = x_piv + frac * wing_len
                rings.append([(bx, side * 54.0 + side * (xl - root_chord * 0.5) * taper, dz + zl * taper) for xl, zl in lo_sec])
            mb.add_loft(rings, C_WING_LOW, 1.0, stl=True)


def add_4x_blades(mb: MeshBuilder, z_top=-22.0, z_bot=-702.0, fold_deg=0.0, x_front=-540.0, x_rear=220.0, y_half=122.0):
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
            # Visible gold hinge pins at TOP rail pivot & BOTTOM pod pivot
            mb.add_cylinder_y(bx, sy - 16, sy + 16, z_top, 9.0, C_KEVLAR, n=10, alpha=1.0, stl=True)
            mb.add_cylinder_y(bx + L * sx_dir, sy - 16, sy + 16, z_top + L * sz_dir, 9.0, C_KEVLAR, n=10, alpha=1.0, stl=True)
    return (L * sx_dir, z_top + L * sz_dir)


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
# MODEL 1 (PRIMARY): True Kit Navigator 300 + Split STOL Flaperons (Internal Pod Servos)
# ---------------------------------------------------------------------------
def build_model_01_navigator300():
    mb = MeshBuilder()
    add_navigator_300_hull(mb, tube_alpha=0.36, stl_hull=True)
    x_f, x_r = -540.0, 220.0
    z_top, z_bot = -22.0, -702.0  # L = 680 mm
    add_4x_blades(mb, z_top=z_top, z_bot=z_bot, fold_deg=0.0, x_front=x_f, x_rear=x_r, y_half=122)
    add_flying_keel_pod(mb, dx=-160.0, dz=z_bot)
    add_stol_flaperons_and_servos(mb, dx=-160.0, dz=z_bot, deg_port=15.0, deg_stbd=-6.0, linked_fold=False, show_internal=False)
    add_plane_grid(mb, -370.0, C_WATER, 0.16)
    write_binary_stl(mb, MODELS_DIR / "01_navigator300_stol_flaperons.stl", "FoilSkiff 01 (PRIMARY): True Kit Navigator 300 + Split STOL Flaperons (mm)")
    callouts = [
        ((-1210, 0, 102), "left", 96, 235, "Bow-Contoured Hard Deck & Under-Plate", "Follows bow rocker & curve • ZERO boxes above deck!"),
        ((-1290, 52, 42), "left", 204, 240, "6 mm Dyneema Bow-D-Ring Sling", "Ties bow ski-nose to D-ring • Zero hull holes!"),
        ((-540, 122, -370), "left", 332, 230, "Clean Wave Zone (Zero Surface Wing!)", "Only 9 mm blades pierce chop (~4 lbf, 0 wave slam)"),
        ((-795, 0, -702), "left", 478, 235, "20 mm Kevlar Crush-Nose Cone", "Ahead of 26 L bay + internal IP67 flaperon servos"),
        ((1050, -300, 220), "right", 96, 800, "Factory Tru-Alu Rigid Transom", "Hybrid C-Frame clamps directly (0 holes!)"),
        ((220, -122, -320), "right", 225, 805, "4× Side-Straddling Blades (60×9 mm)", "Clean 4-bar parallelogram — 0 external pushrods!"),
        ((480, -135, -702), "right", 385, 795, "2× Flipsky 65161 Tailcone Pods", "CAN-bus 360° differential steering"),
        ((-252, -450, -734), "right", 506, 810, "PRIMARY: Split STOL Flaperons", "1,000 + 2×250 cm² • 400 mm deep • 29.8 nm @ 15.5 kn"),
    ]
    render_3d_svg(
        mb, DIAG_DIR / "00-navigator300-3d-cad.svg",
        "3D CAD Model 1 (PRIMARY): True Kit Navigator 300 + Split STOL Flaperons",
        "Bow-contoured Hard Deck & Under-Hull Hybrid C-Frame • Internal pod servos (0 deck boxes) • 400 mm deep ocean-safe foil",
        callouts, az_deg=-138, el_deg=20, scale=0.295, z_center=280,
        footer="Interactive 3D STL: models/01_navigator300_stol_flaperons.stl (click on GitHub to orbit/zoom or 3D-print at 1:15 scale)",
    )
    render_openscad_png(mb, RENDERS_DIR / "01-navigator300-stol-3d.png", "-40,0,-280,76,0,224,4900")


# ---------------------------------------------------------------------------
# MODEL 2 (SECONDARY WING): Flush-Nested Top-Deck Switchblade Wing Pod
# ---------------------------------------------------------------------------
def build_model_02_switchblade():
    mb = MeshBuilder()
    # Bow-contoured dark carbon Hard Deck (100% flush!) + contoured under-hull rail plate
    deck_st = [
        (-1050, 220, 48, 72),
        (-900, 295, 18, 42),
        (-740, 320, 3, 28),
        (60, 320, 3, 28),
        (72, 320, 3, 28),
        (760, 320, 3, 28),
    ]
    under_st = [(-1040, 130, 38, 48), (-900, 148, 8, 18), (-740, 152, -16, -2), (760, 152, -16, -2)]
    add_contoured_deck_and_underplate(mb, deck_st, under_st, latch_x=66.0)
    for sy in (-125, 125):
        mb.add_box(-740, 760, sy - 22, sy + 22, -24, -12, C_ALU, 1.0, stl=True)
    add_4x_blades(mb, z_top=-22, z_bot=-620, fold_deg=0, x_front=-480, x_rear=310, y_half=122)
    add_flying_keel_pod(mb, dx=0, dz=-620, pod_h=90.0)
    add_lower_wings(mb, dx=0, dz=-640, half_span=620, root_chord=108, x_le=-170)

    # Sleek flush-recessed carbon overhang bridge tucked cleanly into the 90 mm pod roof contour (z = -584..-575, y = ±88!)
    mb.add_box(-425, -365, -88, 88, -584, -575, C_CARBON_DARK, 1.0, stl=True)
    sw_sec = naca4_section(0.02, 0.4, 0.12, 105.0, n=10)
    for side in (-1, 1):
        rings = []
        for dist in (40, 110, 350, 620, 790):
            taper = 1.0 - 0.18 * (dist / 790.0) ** 2
            rings.append([(-415 + xl * taper, side * dist, -582 + zl * taper) for xl, zl in sw_sec])
        mb.add_loft(rings, C_WING_UP, 1.0, stl=True)
        mb.add_cylinder_y(-395, side * 35 - 8, side * 35 + 8, -580, 6.0, C_KEVLAR, n=10, alpha=1.0, stl=True)
        mb.add_box(-415, 255, side * 46 - 40, side * 46 + 40, -585, -577, C_FLAP_L, 0.28, stl=False)

    write_binary_stl(mb, MODELS_DIR / "02_switchblade_pod.stl", "FoilSkiff 02 (SECONDARY WING): Flush-Nested Top-Deck Switchblade Pod (mm)")
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
        "3D CAD Model 2 (SECONDARY WING): Flush-Nested Top-Deck Switchblade Pod",
        "Deep-submerged range/speed alternative • Blades nest 100% flush into roof >9 kn (0 cm² extra wet area, 0 wave slam)",
        callouts, az_deg=-134, el_deg=26, scale=0.38, z_center=340,
        footer="Interactive 3D STL: models/02_switchblade_pod.stl (secondary wing module for Navigator 300 & Discovery 330)",
    )
    render_openscad_png(mb, RENDERS_DIR / "02-switchblade-pod-3d.png", "-50,0,-350,60,0,228,3650")


# ---------------------------------------------------------------------------
# MODEL 3 (PRIMARY POD CLOSE-UP): Split STOL Flaperons w/ Internal Pod Servos
# ---------------------------------------------------------------------------
def build_model_03_stol_flaperons():
    mb = MeshBuilder()
    # Contoured bow-upswept Hard Deck (100% FLUSH top surface — ZERO servo boxes above deck!) + contoured under-plate
    deck_st = [
        (-1050, 220, 48, 72),
        (-900, 295, 18, 42),
        (-740, 320, 3, 28),
        (60, 320, 3, 28),
        (72, 320, 3, 28),
        (760, 320, 3, 28),
    ]
    under_st = [(-1040, 130, 38, 48), (-900, 148, 8, 18), (-740, 152, -16, -2), (760, 152, -16, -2)]
    add_contoured_deck_and_underplate(mb, deck_st, under_st, latch_x=65.0)
    for sy in (-125, 125):
        mb.add_box(-740, 760, sy - 22, sy + 22, -24, -12, C_ALU, 1.0, stl=True)

    add_4x_blades(mb, z_top=-22, z_bot=-620, fold_deg=0, x_front=-420, x_rear=310, y_half=122)
    # Translucent pod shell in visual render so the 2x INTERNAL IP67 servos + IMU + VESCs inside the pod are clearly visible!
    add_flying_keel_pod(mb, dx=0, dz=-620, pod_h=80.0, shell_alpha=0.42)
    add_stol_flaperons_and_servos(mb, dx=0, dz=-620, deg_port=18.0, deg_stbd=-8.0, linked_fold=False, show_internal=True)

    write_binary_stl(mb, MODELS_DIR / "03_stol_flaperon_pod.stl", "FoilSkiff 03 (PRIMARY POD): Split STOL Flaperons w/ Internal Pod Servos (mm)")
    callouts = [
        ((-980, 0, 56), "left", 104, 245, "100% Flush Bow-Contoured Hard Deck", "ZERO servo boxes or holes above top deck!"),
        ((-100, 460, -648), "left", 252, 245, "Starboard 250 cm² Flaperon (-8° Up)", "Differential left/right = Active Roll & Banked Turns"),
        ((-92, 52, -616), "left", 408, 245, "2× IP67 Servos SEALED INSIDE Pod!", "70–80 kg·cm + Ø8 mm double-O-ring torque tubes"),
        ((310, -122, -310), "right", 125, 795, "Clean Struts (0 External Pushrods!)", "No pushrod drag, kelp snags, or fold binding"),
        ((-180, -470, -624), "right", 295, 800, "Compact 1,000 cm² Speed Main Wing", "400 mm deep • 29.8 nm @ 15.5 kn"),
        ((-92, -470, -658), "right", 448, 795, "Port 250 cm² STOL Flaperon (+18° Down)", "Junkers slot jet (CL_max ≈ 2.0) • 20% failsafe pivot"),
    ]
    render_3d_svg(
        mb, DIAG_DIR / "07-stol-flaperons-3d-cad.svg",
        "3D CAD Model 3 (PRIMARY POD): Split STOL Flaperons + Internal Pod Servos",
        "Differential roll/bank (+18° Port / -8° Stbd) • Translucent pod shows internal IP67 servos + IMU (ZERO deck boxes!)",
        callouts, az_deg=-138, el_deg=23, scale=0.39, z_center=310,
        footer="Interactive 3D STL: models/03_stol_flaperon_pod.stl (PRIMARY universal pod for Navigator 300 & Discovery 330)",
    )
    render_openscad_png(mb, RENDERS_DIR / "03-stol-flaperon-pod-3d.png", "20,0,-320,66,0,224,3100")


# ---------------------------------------------------------------------------
# MODEL 4 (PRIMARY): True Kit Navigator 300 Retracted Beaching Mode (86.5° Fold)
# ---------------------------------------------------------------------------
def build_model_04_navigator300_retracted():
    mb = MeshBuilder()
    add_navigator_300_hull(mb, tube_alpha=0.38, stl_hull=True)
    x_f, x_r = -540.0, 220.0
    z_top, z_bot = -22.0, -702.0  # L = 680 mm
    fold = 86.5
    dx_bot, z_pod = add_4x_blades(mb, z_top=z_top, z_bot=z_bot, fold_deg=fold, x_front=x_f, x_rear=x_r, y_half=122)
    dx_pod = -160.0 + dx_bot
    add_flying_keel_pod(mb, dx=dx_pod, dz=z_pod, pod_h=95.0)
    add_stol_flaperons_and_servos(mb, dx=dx_pod, dz=z_pod, deg_port=0.0, deg_stbd=0.0, linked_fold=True, show_internal=False)
    add_plane_grid(mb, -232.0, C_SAND, 0.32, n=6)

    write_binary_stl(mb, MODELS_DIR / "04_navigator300_retracted_beaching.stl", "FoilSkiff 04 (PRIMARY): True Kit Navigator 300 Retracted 86.5-deg Beaching (mm)")
    callouts = [
        ((-1210, 0, 102), "left", 102, 235, "Bow-Contoured Hard Deck & Ski-Plate", "Follows curved bow up to D-ring • 0 boxes above deck"),
        ((-200, 122, -45), "left", 242, 240, "4× Side-Straddling Blades Folded 86.5°", "1-Button BEACH MODE drops Strut & Foil servo pins to 0%!"),
        ((dx_pod - 550, 0, z_pod), "left", 425, 240, "95 mm Pod + Upper/Lower 90° Channels", "100% intact 26 L dry bay • Dyneema pulley fold (0 motors!)"),
        ((1050, -240, 180), "right", 112, 800, "Clears Beneath Tru-Alu Transom!", "220 mm folded dart fits cleanly BETWEEN 250 mm rails!"),
        ((dx_pod + 620, -135, z_pod), "right", 275, 795, "Props Protected Inside Rear Cones", "Folded wings stop well ahead of props • High & dry"),
        ((150, -350, -168), "right", 455, 800, "~130–140 mm (5.1–5.5\") Sand Clear!", "True 90° flush wings inside 220 mm pod (zero overhang!)"),
    ]
    render_3d_svg(
        mb, DIAG_DIR / "08-navigator300-retracted-3d.svg",
        "3D CAD Model 4 (PRIMARY): True Kit Navigator 300 Retracted Beaching Mode (86.5° Fold)",
        "True 90° Upper/Lower Fold Channels (220 mm dart fits between 250 mm rails!) • 1-Button BEACH MODE • ~5.1–5.5\" clear!",
        callouts, az_deg=-138, el_deg=14, scale=0.295, z_center=120,
        footer="Interactive 3D STL: models/04_navigator300_retracted_beaching.stl (click on GitHub to inspect under-tunnel clearance in 3D)",
    )
    render_openscad_png(mb, RENDERS_DIR / "04-navigator300-retracted-3d.png", "40,0,-85,94,0,242,4100")


# ---------------------------------------------------------------------------
# MODEL 5 (SECONDARY HULL REF): True Kit Discovery 330 Open-Bow Full O-Frame
# ---------------------------------------------------------------------------
def build_model_05_discovery330():
    mb = MeshBuilder()
    add_discovery_330_hull(mb, tube_alpha=0.38, stl_hull=True)
    x_f, x_r = -540.0, 220.0
    z_top, z_bot = -22.0, -702.0
    add_4x_blades(mb, z_top=z_top, z_bot=z_bot, fold_deg=0.0, x_front=x_f, x_rear=x_r, y_half=124)
    add_flying_keel_pod(mb, dx=-160.0, dz=z_bot)
    add_stol_flaperons_and_servos(mb, dx=-160.0, dz=z_bot, deg_port=15.0, deg_stbd=-6.0, linked_fold=False, show_internal=False)
    add_plane_grid(mb, -370.0, C_WATER, 0.16)
    write_binary_stl(mb, MODELS_DIR / "05_discovery330_oframe_stol.stl", "FoilSkiff 05 (Secondary Hull): True Kit Discovery 330 + Split STOL Pod (mm)")
    callouts = [
        ((-1180, 0, 75), "left", 104, 240, "Bow-Contoured Hard Deck & O-Frame", "Follows bow rocker & wraps open square bow"),
        ((-540, 124, -370), "left", 240, 230, "Clean Wave Zone (Zero Surface Wing!)", "Only 9 mm vertical blades slice chop"),
        ((-795, 0, -702), "left", 475, 235, "Identical Swappable STOL Pod", "100% interchangeable between Navigator & Discovery"),
        ((950, -620, 120), "right", 108, 810, "True Kit Discovery 330 (Open Bow)", "330 cm landing-craft hull / Takacat LX equivalent"),
        ((220, -124, -310), "right", 232, 810, "4× Side-Straddling Blades (60×9 mm)", "Internal pod servos = 0 external pushrods"),
        ((480, -135, -702), "right", 392, 795, "2× Flipsky 65161 Tailcone Pods", "CAN-bus 360° differential steering"),
        ((-252, -450, -734), "right", 508, 810, "PRIMARY: Split STOL Flaperons", "1,000 + 2×250 cm² • 29.8 nm @ 15.5 kn"),
    ]
    render_3d_svg(
        mb, DIAG_DIR / "11-discovery330-oframe-3d-cad.svg",
        "3D CAD Model 5 (Secondary Open-Bow Ref): True Kit Discovery 330 + Split STOL Pod",
        "Bow-contoured Hard Deck & Full Rigid O-Frame wrapping open square bow (also applies to Takacat LX)",
        callouts, az_deg=-140, el_deg=20, scale=0.285, z_center=280,
        footer="Interactive 3D STL: models/05_discovery330_oframe_stol.stl (secondary open-bow hull reference)",
    )
    render_openscad_png(mb, RENDERS_DIR / "05-discovery330-oframe-3d.png", "-40,0,-290,77,0,222,5200")


def add_2x_center_recessed_struts(mb: MeshBuilder, z_top=-22.0, z_bot=-702.0, x_front=-540.0, x_rear=220.0):
    """
    Swap #3 (Lowest Pivoting Drag): 2x Hollow Carbon 100x18 mm Recessed Center Tandem Struts (9.1 lbf vs 11.4 lbf).
    Includes full asymmetric-load & one-sided impact trunnion hardware:
      - Upper End: Anti-splay bridge plate + 260 mm tapered T-Head yoke + full-width Ø16 mm SS axle across BOTH 250 mm rails
        + orange UHMW/bronze thrust washers (8.3x lower pin bearing load, zero sideways binding during kick-up!).
      - Lower End: 180 mm flared pod saddle T-foot inside the 55 mm top recess + full-width Ø16 mm SS axle anchored into
        twin 6 mm G10/carbon full-height internal pod bulkheads + Delrin kick-up shear fuse!
    """
    strut_sec = naca4_section(0.0, 0.0, 0.18, 100.0, n=12)
    for bx in (x_front, x_rear):
        # Upper Anti-Splay Bridge Plate + Tapered 250 mm T-Head Yoke
        mb.add_box(bx - 36, bx + 42, -150, 150, z_top - 4, z_top + 6, C_ALU, 1.0, stl=True)
        mb.add_box(bx - 22, bx + 38, -102, 102, z_top - 32, z_top - 4, C_CARBON_DARK, 1.0, stl=True)
        # Full-width Ø16 mm upper stainless axle spanning BOTH 250 mm rails (offset to TE +24 mm)
        mb.add_cylinder_y(bx + 24, -152, 152, z_top - 14, 8.5, C_KEVLAR, n=10, alpha=1.0, stl=True)
        # Orange flanged UHMW/bronze thrust washers reacting +/-220 kgf lateral impact thrust against rails!
        for sy in (-106, 106):
            mb.add_box(bx + 10, bx + 38, sy - 4, sy + 4, z_top - 28, z_top - 2, C_FLAP_R, 1.0, stl=True)
        # Hollow 100x18 mm carbon center strut
        rings = []
        for z_pos in (z_top - 10, (z_top + z_bot) * 0.5, z_bot + 16):
            rings.append([(bx + xl - 50.0, yl, z_pos) for xl, yl in strut_sec])
        mb.add_loft(rings, C_CARBON_DARK, 1.0, stl=True)
        # Lower 180 mm Recessed Pod Saddle T-Foot + Full-Width Ø16 mm Axle (offset to LE -24 mm)
        mb.add_box(bx - 42, bx + 12, -82, 82, z_bot + 2, z_bot + 30, C_CARBON_DARK, 1.0, stl=True)
        mb.add_cylinder_y(bx - 24, -100, 100, z_bot + 16, 8.5, C_KEVLAR, n=10, alpha=1.0, stl=True)
        # Twin 6 mm G10/carbon full-height internal pod bulkhead cheek plates + orange thrust washers
        for sy in (-88, 88):
            mb.add_box(bx - 48, bx + 18, sy - 5, sy + 5, z_bot - 34, z_bot + 34, C_WING_UP, 0.85, stl=False)
            mb.add_box(bx - 36, bx - 12, sy - (6 if sy > 0 else -12) + (-6 if sy < 0 else 0), sy + (0 if sy > 0 else 6), z_bot + 4, z_bot + 28, C_FLAP_R, 1.0, stl=True)
    # Front strut Wet IP68 Servo Variable-Preload Roller Lock (0% BEACH / 50% Shoal / 100% Cruise ~140 kgf @ 0 W!)
    # Gold IP68 75 kg·cm servo + cam/rocker block under front anti-splay bridge + red hardened 316 SS roller on LE tang
    mb.add_box(x_front - 110, x_front - 58, -26, 26, z_top - 30, z_top - 4, C_KEVLAR, 1.0, stl=True)
    mb.add_box(x_front - 58, x_front - 28, -20, 20, z_top - 28, z_top - 16, C_ALU, 1.0, stl=True)      # Solid Cruise Stop
    mb.add_cylinder_y(x_front - 46, -18, 18, z_top - 10, 5.5, C_PUSHROD, n=10, alpha=1.0, stl=True)    # 20° Roller Pin
    # Crab-pot line cutter notch at LE/pod junction
    mb.add_box(x_front - 64, x_front - 46, -6, 6, z_bot + 34, z_bot + 64, C_FLAP_R, 1.0, stl=True)


def add_single_centerline_prop_and_rudder(mb: MeshBuilder, dx=0.0, dz=-702.0, show_internal=False):
    """
    Swap #1 (Biggest Range Win — ~50% of gain!): Single Centerline Flipsky 65161 Tailcone Pod +
    10" x 11" High-Pitch 2-Blade CNC Prop (~78-80% prop efficiency, -3.5 lbf drag) +
    Compact Vertical Tailfin & Hinged Rudder Flap driven directly by internal aft pod servo!
    """
    # Centerline Flipsky 65161 motor housing integrated cleanly into tapered fuselage tailcone
    pod_rings = []
    for x, r in [(540, 34), (665, 32.5), (710, 26), (735, 16), (748, 6)]:
        pod_rings.append([(dx + x, r * math.cos(2 * math.pi * i / 14), dz + r * math.sin(2 * math.pi * i / 14)) for i in range(14)])
    mb.add_loft(pod_rings, C_MOTOR, 1.0, stl=True)

    # Large 10" (Ø254 mm -> r = 127 mm) High-Pitch 2-Blade CNC Foiling Propeller!
    for k in range(2):
        ang = math.radians(k * 180 + 78)
        ca, sa = math.cos(ang), math.sin(ang)
        pa, qa = math.cos(ang + 0.35), math.sin(ang + 0.35)
        pb, qb = math.cos(ang - 0.35), math.sin(ang - 0.35)
        mb.add_quad(
            (dx + 716, 12 * pa, dz + 12 * qa),
            (dx + 732, 68 * pa, dz + 68 * qa),
            (dx + 724, 127 * ca, dz + 127 * sa),
            (dx + 706, 52 * pb, dz + 52 * qb),
            C_PROP, 0.98, stl=True,
        )
        mb.add_quad(
            (dx + 716, 12 * pa, dz + 12 * qa),
            (dx + 706, 52 * pb, dz + 52 * qb),
            (dx + 724, 127 * ca, dz + 127 * sa),
            (dx + 732, 68 * pa, dz + 68 * qa),
            C_WING_LOW, 0.98, stl=True,
        )

    # Compact Vertical Tailfin (fixed forward spar) + Hinged Rudder Flap (deflected +12 deg for visual clarity!)
    fin_sec = naca4_section(0.0, 0.0, 0.12, 70.0, n=10)
    fin_rings = []
    for z_off in (30, 105, 175):
        taper = 1.0 - 0.30 * ((z_off - 30) / 145.0)
        fin_rings.append([(dx + 465 + 18 * (1 - taper) + xl * taper, yl * taper, dz + z_off) for xl, yl in fin_sec])
    mb.add_loft(fin_rings, C_CARBON_DARK, 1.0, stl=True)

    # Orange trailing-edge rudder flap (deflected +14 deg right)
    rud_sec = naca4_section(0.0, 0.0, 0.11, 46.0, n=8)
    r_rad = math.radians(14.0)
    rud_rings = []
    for z_off in (32, 105, 172):
        taper = 1.0 - 0.30 * ((z_off - 32) / 140.0)
        x_p = dx + 538 + 6 * (1 - taper)
        rud_rings.append([(x_p + xl * taper * math.cos(r_rad) - yl * taper * math.sin(r_rad), xl * taper * math.sin(r_rad) + yl * taper * math.cos(r_rad), dz + z_off) for xl, yl in rud_sec])
    mb.add_loft(rud_rings, C_FLAP_R, 1.0, stl=True)
    # Gold rudder hinge shaft exiting pod top through double-O-ring seal
    mb.add_cylinder_y(dx + 538, -8, 8, dz + 28, 7.0, C_KEVLAR, n=8, alpha=1.0, stl=True)

    if show_internal:
        # Internal IP67 aft rudder/elevator servo + 1x Flipsky 75100 VESC (saves weight & $95!) + 2x IP68 Battery Cartridges
        mb.add_box(dx + 470, dx + 528, -22, 22, dz - 18, dz + 22, C_KEVLAR, 1.0, stl=False)   # Aft Rudder Servo
        mb.add_box(dx + 345, dx + 455, -52, 52, dz - 36, dz - 6, C_ALU, 1.0, stl=False)       # 1x 75100 VESC (bottom-skin cooled)
        mb.add_box(dx + 260, dx + 332, -32, 32, dz - 12, dz + 16, C_WING_UP, 1.0, stl=False)  # ESP32 + 6-DOF BNO085 IMU
        # Front & Mid swappable IP68 battery cartridges (translucent blue/teal inside 26 L bay)
        mb.add_box(dx - 455, dx - 140, -82, 82, dz - 28, dz + 24, C_WING_LOW, 0.72, stl=False)
        mb.add_box(dx - 115, dx + 220, -82, 82, dz - 28, dz + 24, C_WING_UP, 0.72, stl=False)


# ---------------------------------------------------------------------------
# MODEL 6 (LONG-RANGE 80/20 SWEET SPOT — TANDEM 2-CHAIR MODE): 65-79 nm LiFePO4
# ---------------------------------------------------------------------------
def build_model_06_lr_8020():
    mb = MeshBuilder()
    # Dual-Pack 60 mm Contoured Battery-Floor Hard Deck + Flush L-Tracks + Bow Spray Dodger + 2 Tandem Low-Sit Chairs!
    add_navigator_300_hull(mb, tube_alpha=0.35, stl_hull=True, deck_thick=60.0, with_bow_dodger=True, show_bench_seats=False, with_ltracks=True)
    # 2 Inline Tandem Ergonomic Low-Sit Chairs locked onto flush L-Tracks (424 mm wide inside 600 mm tunnel!)
    add_low_sit_chair(mb, x_hip=-320.0, z_deck=63.0, y_track=195.0, with_armrest_helm=False)  # Front passenger
    add_low_sit_chair(mb, x_hip=420.0, z_deck=63.0, y_track=195.0, with_armrest_helm=True)    # Aft pilot w/ armrest helm!
    x_f, x_r = -540.0, 220.0
    z_top, z_bot = -22.0, -702.0
    add_4x_blades(mb, z_top=z_top, z_bot=z_bot, fold_deg=0.0, x_front=x_f, x_rear=x_r, y_half=122)
    add_flying_keel_pod(mb, dx=-160.0, dz=z_bot, with_motors=False)
    add_single_centerline_prop_and_rudder(mb, dx=-160.0, dz=z_bot, show_internal=False)
    add_lower_wings(mb, dx=-160.0, dz=z_bot - 14.0, half_span=750.0, root_chord=104.0, x_le=-245.0)
    fl_sec = naca4_section(0.02, 0.4, 0.11, 58.0, n=10)
    piv_x, piv_z = -160.0 - 92.0, z_bot - 30.0
    mb.add_cylinder_y(piv_x, -116, 116, piv_z, 4.5, C_PUSHROD, n=10, alpha=1.0, stl=True)
    for side, deg, col in [(-1, 14.0, C_FLAP_L), (1, -5.0, C_FLAP_R)]:
        mb.add_cylinder_y(piv_x, side * 96, side * 112, piv_z, 7.0, C_CARBON_DARK, n=10, alpha=1.0, stl=True)
        rad = math.radians(deg)
        rings = [[(piv_x + (xl - 11.6) * math.cos(rad) + zl * math.sin(rad), side * dist, piv_z - (xl - 11.6) * math.sin(rad) + zl * math.cos(rad)) for xl, zl in fl_sec] for dist in (108, 340, 560)]
        mb.add_loft(rings, col, 1.0, stl=True)
    add_plane_grid(mb, -370.0, C_WATER, 0.16)

    write_binary_stl(mb, MODELS_DIR / "06_navigator300_lr_8020_sweetspot.stl", "FoilSkiff 06 (LR 80/20 Tandem 2-Chair): Navigator 300 65-79 nm (mm)")
    callouts = [
        ((-1050, 0, 500), "left", 96, 235, "Bow Spray Dodger + 2× Low-Sit Chairs", "Tandem 424 mm chairs on flush L-Tracks (-250 mm CoG!)"),
        ((-320, 342, 32), "left", 204, 240, "60 mm Dual-Pack Hard Deck + L-Tracks", "10.8 kWh LiFePO4 • 100% flush when chairs unclipped!"),
        ((-310, 690, -692), "left", 345, 235, "Swap #2: AR 13.5 Wide Main Wing (1.50 m)", "Cuts induced drag ~30% + keeps Split STOL control!"),
        ((-795, 0, -702), "left", 478, 235, "26 L Flying-Keel Pod (5.38 kWh)", "Internal STOL & rudder servos — 0 deck boxes!"),
        ((270, -225, 395), "right", 96, 800, "Aft Pilot Chair + Armrest Helm Pod", "Thumb-throttle & joystick move with the chair!"),
        ((220, -122, -320), "right", 225, 805, "Keeps Easy 4× Side-Straddling Blades!", "60×9 mm • Zero pod cut-out, 5.5\" sand clearance"),
        ((380, 0, -565), "right", 370, 795, "Compact Tailfin & Internal-Servo Rudder", "Clean steering without 2nd motor drag"),
        ((575, 0, -702), "right", 495, 805, "Swap #1: Single 65161 + 10\" CNC 2-Blade", "65 nm @ 15.5 kn • 79 nm @ 12 kn (10.8 kWh LFP)"),
    ]
    render_3d_svg(
        mb, DIAG_DIR / "13-navigator300-lr-8020-3d-cad.svg",
        "3D CAD Model 6 (LR 80/20 Tandem 2-Chair): True Kit Navigator 300 (65–79 nm)",
        "2 inline ergonomic low-sit chairs on flush L-Tracks + Single 65161 (10\" prop), AR 13.5 Split STOL, 60 mm deck & bow dodger",
        callouts, az_deg=-138, el_deg=20, scale=0.285, z_center=245,
        footer="Interactive 3D STL: models/06_navigator300_lr_8020_sweetspot.stl (Tandem 2-Chair 80/20 Long-Range Build)",
    )
    render_openscad_png(mb, RENDERS_DIR / "06-navigator300-lr-8020-3d.png", "-40,0,-210,74,0,224,5200")


def add_linked_fold_root_box(mb: MeshBuilder, dx=0.0, dz_wing=-638.0, x_le=-220.0):
    """
    True 90° Lower Belly Fold Channel (12 mm recess) + Wet IP68 Servo Variable-Preload Roller Lock:
      - 12 mm recessed UHMW-lined Overhang Bridge under pod belly: 40 mm inboard wing roots carry 100% of lift/roll (~35 MPa)!
      - 2× Ø16 mm vertical stainless root pivot pins at y = ±54 mm + intermeshing 90° stainless gear sectors at y = ±18 mm.
      - Wet IP68 75 kg·cm servo + 12 mm over-center cam + 37 kgf grease-booted spring + 3.5:1 rocker + 20° hardened 316 SS roller
        (0% Fold/Deploy ↔ 50% Reef ~45 kgf ↔ 100% Cruise ~85 kgf tip / ~170 kgf center @ 0 W hold!).
        BOTH halves fold true 90° straight aft flush inside the 220 mm pod (204 mm total, 179 mm ahead of prop!).
    """
    x_piv = dx + x_le + 22.0
    # 12 mm recessed Lower Fold Channel Overhang Bridge under pod belly (212 mm wide inside 220 mm pod)
    mb.add_box(dx + x_le - 14.0, dx + x_le + 114.0, -106.0, 106.0, dz_wing - 9.0, dz_wing + 11.0, C_ALU, 0.94, stl=True)
    # 2× Gold Ø16 mm vertical stainless root pivot pins at y = ±54 mm + meshed 90° gear sectors at y = ±18 mm
    for side in (-1, 1):
        mb.add_rod((x_piv, side * 54.0, dz_wing - 13.0), (x_piv, side * 54.0, dz_wing + 15.0), 8.0, C_KEVLAR, n=10, alpha=1.0, stl=True)
        mb.add_rod((x_piv, side * 18.0, dz_wing - 6.0), (x_piv, side * 18.0, dz_wing + 6.0), 17.5, C_CARBON_DARK, n=12, alpha=1.0, stl=False)
    # Red 20° hardened 316 SS roller detent pin + Gold Wet IP68 75 kg·cm Servo & Over-Center Cam/Rocker module aft of gear mesh
    mb.add_rod((x_piv + 44.0, 0.0, dz_wing - 12.0), (x_piv + 44.0, 0.0, dz_wing + 14.0), 6.0, C_PUSHROD, n=10, alpha=1.0, stl=True)
    mb.add_box(x_piv + 52.0, x_piv + 106.0, -24.0, 24.0, dz_wing - 11.0, dz_wing + 13.0, C_KEVLAR, 1.0, stl=True)


# ---------------------------------------------------------------------------
# MODEL 7 (FULL LONG-RANGE MAX EFFICIENCY — SOLO 1-CHAIR MODE): 70-84 nm
# ---------------------------------------------------------------------------
def build_model_07_lr_max_range():
    mb = MeshBuilder()
    add_navigator_300_hull(mb, tube_alpha=0.35, stl_hull=True, deck_thick=60.0, with_bow_dodger=True, show_bench_seats=False, with_ltracks=True)
    # 1 Solo Ergonomic Low-Sit Pilot Chair slid right over midship CoG (X = +20 mm -> crew CoG dead-on foil CoL!)
    add_low_sit_chair(mb, x_hip=20.0, z_deck=63.0, y_track=195.0, with_armrest_helm=True)
    x_f, x_r = -540.0, 220.0
    z_top, z_bot = -22.0, -702.0
    add_2x_center_recessed_struts(mb, z_top=z_top, z_bot=z_bot, x_front=x_f, x_rear=x_r)
    add_flying_keel_pod(mb, dx=-160.0, dz=z_bot, pod_h=95.0, with_motors=False)
    add_single_centerline_prop_and_rudder(mb, dx=-160.0, dz=z_bot, show_internal=False)
    add_lower_wings(mb, dx=-160.0, dz=z_bot - 42.0, half_span=775.0, root_chord=102.0, x_le=-220.0)
    add_linked_fold_root_box(mb, dx=-160.0, dz_wing=z_bot - 42.0, x_le=-220.0)
    # Upper Fold Channel (13 mm roof recess): Switchblade blades recessed cleanly INSIDE pod roof behind front strut!
    for side in (-1, 1):
        mb.add_box(-470, 120, side * 44 - 38, side * 44 + 38, z_bot + 38, z_bot + 46, C_WING_UP, 0.72, stl=False)
    add_plane_grid(mb, -370.0, C_WATER, 0.16)

    write_binary_stl(mb, MODELS_DIR / "07_navigator300_lr_max_range.stl", "FoilSkiff 07 (Full LR Solo 1-Chair): Navigator 300 70-84 nm Build (mm)")
    callouts = [
        ((-1050, 0, 500), "left", 96, 235, "Swap #4: Aerodynamic Bow Dodger", "Pilot tucks low behind dodger (-8 Wh/nm aero!)"),
        ((-120, -225, 380), "left", 204, 240, "Solo Low-Sit Chair Slid Over CoG!", "5-sec L-Track slide balances foil CoL • Open aft bay"),
        ((-300, 720, -718), "left", 345, 235, "Swap #2: AR 14 (1.55 m) 90° Belly Foil", "Folds 90° flush in 220 mm pod (179 mm ahead of prop!)"),
        ((-795, 0, -702), "left", 478, 235, "95 mm Upper/Lower Fold-Channel Pod", "13 mm roof + 12 mm belly • 100% intact 26 L dry bay!"),
        ((720, -195, 65), "right", 96, 800, "Open Aft Flush L-Track Cargo Bay", "Clip 2nd chair, dry bag, or plug-in extender pack!"),
        ((220, 0, -330), "right", 225, 805, "Swap #3: 2× Hollow Center Struts", "Wide T-heads + IP68 Servo Strut Pin (0% Beach / ~140 kgf)"),
        ((380, 0, -565), "right", 370, 795, "Internal-Servo Tailfin Rudder", "Zero deck boxes, zero external steering rods"),
        ((575, 0, -702), "right", 495, 805, "Swap #1: Single 65161 + 10\" CNC 2-Blade", "70–84 nm (10.8 kWh LFP) • 55–67 nm (8.2 kWh NMC)"),
    ]
    render_3d_svg(
        mb, DIAG_DIR / "14-navigator300-lr-max-range-3d-cad.svg",
        "3D CAD Model 7 (Full LR Solo 1-Chair): True Kit Navigator 300 (70–84 nm)",
        "Solo chair on L-Tracks + Single 65161 (10\" prop), AR 14 90° Fold Channels, Dual IP68 Servo Pins & Dodger",
        callouts, az_deg=-138, el_deg=20, scale=0.285, z_center=245,
        footer="Interactive 3D STL: models/07_navigator300_lr_max_range.stl (Solo 1-Chair Full 4-Swap Max-Range Build)",
    )
    render_openscad_png(mb, RENDERS_DIR / "07-navigator300-lr-max-range-3d.png", "-40,0,-210,74,0,224,5200")


# ---------------------------------------------------------------------------
# MODEL 8 (CLOSE-UP CUTAWAY): Long-Range Single-Prop Pod & 2x Recessed Struts
# ---------------------------------------------------------------------------
def build_model_08_lr_pod_closeup():
    mb = MeshBuilder()
    # Bow-contoured 60 mm Battery-Floor Hard Deck (translucent front cut showing dry pack) + contoured under-plate
    deck_st = [
        (-1050, 220, 48, 86),
        (-900, 295, 18, 72),
        (-740, 320, 3, 63),
        (60, 320, 3, 63),
        (72, 320, 3, 63),
        (760, 320, 3, 63),
    ]
    under_st = [(-1040, 130, 38, 48), (-900, 148, 8, 18), (-740, 152, -16, -2), (760, 152, -16, -2)]
    add_contoured_deck_and_underplate(mb, deck_st, under_st, latch_x=66.0)
    for sy in (-125, 125):
        mb.add_box(-740, 760, sy - 22, sy + 22, -24, -12, C_ALU, 1.0, stl=True)

    # 2x Recessed Center Tandem Struts (100x18 mm, T-heads bolting across both 250 mm rails + Wet IP68 Servo Lock!)
    add_2x_center_recessed_struts(mb, z_top=-22.0, z_bot=-620.0, x_front=-420.0, x_rear=310.0)
    # Translucent 95 mm pod revealing swappable cartridges, 1x 75100 VESC, ESP32/IMU & internal aft rudder servo!
    add_flying_keel_pod(mb, dx=0.0, dz=-620.0, pod_h=95.0, with_motors=False, shell_alpha=0.38)
    add_single_centerline_prop_and_rudder(mb, dx=0.0, dz=-620.0, show_internal=True)
    # High-aspect AR 14 (1.55 m) lower wing in True 90° Lower Belly Fold Channel (12 mm) + Wet IP68 Servo Roller Lock!
    add_lower_wings(mb, dx=0.0, dz=-662.0, half_span=775.0, root_chord=102.0, x_le=-220.0)
    add_linked_fold_root_box(mb, dx=0.0, dz_wing=-662.0, x_le=-220.0)
    # Upper Fold Channel (13 mm roof recess): Switchblade blades recessed cleanly inside pod roof behind front center strut!
    for side in (-1, 1):
        mb.add_box(-330, 240, side * 44 - 38, side * 44 + 38, -582, -574, C_WING_UP, 0.48, stl=False)

    write_binary_stl(mb, MODELS_DIR / "08_lr_pod_closeup.stl", "FoilSkiff 08 (LR Cutaway): Single-Prop Pod, 2x Recessed Struts & 90-deg Fold Channels (mm)")
    callouts = [
        ((-940, 0, 62), "left", 104, 245, "60 mm Bow-Contoured Battery Deck", "Houses 5.38 kWh dry EVE LF105 (100% flush top!)"),
        ((-475, 0, -36), "left", 228, 245, "Strut Wet IP68 Servo Roller Lock", "0% Beach / ~140 kgf Shoal (0 W TDC) + 260 mm T-heads!"),
        ((-150, 0, -662), "left", 375, 245, "12 mm Belly Channel + IP68 Servo Pin", "y=±54 mm pivots + gears + 0%/50%/100% roller cam!"),
        ((-120, 680, -654), "left", 495, 245, "High-Aspect AR 14 Main Wing (1.55 m)", "Folds true 90° into 220 mm pod (Dyneema pulley loop!)"),
        ((310, 0, -280), "right", 118, 795, "Rear Strut Drafts in Front Wake", "Twin 6 mm G10 internal bulkheads take roll & yaw!"),
        ((500, 0, -605), "right", 252, 795, "Internal Aft Rudder Servo + 1× VESC", "100% intact 26 L dry bay between upper/lower channels"),
        ((540, 0, -490), "right", 375, 795, "Compact Tailfin & Hinged Rudder (+14°)", "Direct-drive shaft seal — zero deck boxes!"),
        ((725, 0, -620), "right", 498, 800, "Single 65161 + 10\"×11\" 2-Blade CNC Prop", "90° folded wing stops 179 mm ahead of prop!"),
    ]
    render_3d_svg(
        mb, DIAG_DIR / "15-lr-pod-closeup-3d-cad.svg",
        "3D CAD Model 8 (Long-Range Pod Cutaway): 90° Fold Channels & Dual IP68 Servo Pins",
        "Translucent 95 mm pod shows 100% intact 26 L bay, 12 mm belly channel (y=±54 mm pivots + servo cam) & upper strut servo lock",
        callouts, az_deg=-134, el_deg=22, scale=0.35, z_center=295,
        footer="Interactive 3D STL: models/08_lr_pod_closeup.stl (Long-Range Hydro Package internal cutaway)",
    )
    render_openscad_png(mb, RENDERS_DIR / "08-lr-pod-closeup-3d.png", "30,0,-305,67,0,224,3350")


# ---------------------------------------------------------------------------
# MODEL 9 (MODULAR DECK SEATING): Bow-Contoured Hard Deck + Flush L-Tracks + 2 Chairs
# ---------------------------------------------------------------------------
def build_model_09_modular_seating():
    mb = MeshBuilder()
    dt = 60.0
    deck_st = [
        (-1245, 95, 86, 86 + 32.0),
        (-1160, 185, 62, 62 + 38.0),
        (-1030, 268, 34, 34 + 48.0),
        (-880, 322, 12, 12 + dt),
        (-720, 340, 3, 3 + dt),
        (60, 340, 3, 3 + dt),
        (72, 340, 3, 3 + dt),
        (990, 340, 3, 3 + dt),
    ]
    under_st = [
        (-1175, 115, 52, 62),
        (-1030, 148, 22, 32),
        (-880, 154, -2, 10),
        (-720, 152, -16, -2),
        (1095, 152, -16, -2),
    ]
    add_contoured_deck_and_underplate(mb, deck_st, under_st, latch_x=66.0)
    add_flush_ltracks(mb, z_top=3.0 + dt, x0=-680.0, x1=890.0, y_track=195.0)
    # Transom C-clamp & bow Dyneema sling shown for hull context
    for sy in (-125, 125):
        mb.add_box(-740, 1095, sy - 22, sy + 22, -24, -12, C_ALU, 1.0, stl=True)
    mb.add_box(1065, 1095, -160, 160, -24, 160, C_ALU, 1.0, stl=True)
    mb.add_box(1005, 1095, -160, 160, 140, 168, C_ALU, 1.0, stl=True)
    # 2 Inline Tandem Low-Sit Ergonomic Chairs (slideable to 1-Chair Solo @ CoG or removed in 5 sec!)
    add_low_sit_chair(mb, x_hip=-320.0, z_deck=3.0 + dt, y_track=195.0, with_armrest_helm=False)
    add_low_sit_chair(mb, x_hip=420.0, z_deck=3.0 + dt, y_track=195.0, with_armrest_helm=True)

    write_binary_stl(mb, MODELS_DIR / "09_modular_hard_deck_seating.stl", "FoilSkiff 09 (Modular Seating): Contoured Deck, Flush L-Tracks & 2 Low-Sit Chairs (mm)")
    callouts = [
        ((-1130, 0, 95), "left", 104, 240, "Bow-Contoured Footrest & Ski-Plate", "Legs extend naturally onto upturned bow deck!"),
        ((-320, 210, 460), "left", 228, 245, "Front Low-Sit Chair (424 mm Wide)", "22° lumbar recline • Fits 600 mm tunnel cleanly"),
        ((-510, 195, 82), "left", 378, 240, "Spring-Loaded L-Track Quick-Release", "900 kgf double-stud pins • 5-sec slide/remove!"),
        ((-650, -195, 65), "left", 498, 240, "Flush Recessed Twin L-Tracks (390 mm)", "100% flush with deck — zero trip hazard when empty!"),
        ((690, 0, 495), "right", 104, 800, "Aft Pilot Chair (Slides to Solo CoG!)", "Slide 1 chair to X ≈ 0 mm for solo 70+ nm flights"),
        ((270, 225, 395), "right", 232, 800, "Integrated Armrest Wireless Helm Pod", "Right-hand thumb-throttle & joystick move with chair!"),
        ((820, -195, 65), "right", 368, 800, "2-Piece Midship Latch + 60 mm Deck", "Packs into 2 halves • Houses 5.38 kWh dry pack"),
        ((1080, 0, 120), "right", 492, 800, "Tru-Alu Transom Hybrid C-Clamp", "Zero deck boxes, zero hull holes!"),
    ]
    render_3d_svg(
        mb, DIAG_DIR / "17-modular-deck-seating-3d-cad.svg",
        "3D CAD Model 9: Modular Hard Deck Seating (Flush L-Tracks + 1 or 2 Low-Sit Chairs)",
        "5-sec quick-release slide between Solo (1 chair @ CoG), Tandem (2 chairs inline), and Open Deck (0 chairs, 100% flush!)",
        callouts, az_deg=-136, el_deg=24, scale=0.33, z_center=-180,
        footer="Interactive 3D STL: models/09_modular_hard_deck_seating.stl (Modular 1-or-2 Low-Sit Ergonomic Seating System)",
    )
    render_openscad_png(mb, RENDERS_DIR / "09-modular-deck-seating-3d.png", "-40,0,190,68,0,224,3850")


# ---------------------------------------------------------------------------
# MODEL 10 (UPGRADE): Dual-Mode Morphing STOL-to-Staggerwing Flaperon Pod
# ---------------------------------------------------------------------------
def build_model_10_morphing_stol_staggerwing():
    """
    100% Internal-Pod Wet-Slot / Dry-Bay Vertical Elevator Sled (ZERO external swing-arms, belts, or sliding dry seals!):
      - 90 mm tall Flying-Keel Pod (Z = dz - 45 to dz + 45) completely encloses the entire morphing mechanism!
      - Main Wing (1,000 cm², 100 mm chord) mounted in the LOWER THIRD (Z = dz - 22 mm).
      - Free-Flooding Internal Wing-Box (x = -142..-46 mm) bounded by twin watertight bulkheads:
          * Twin Ø10 mm stainless vertical guide rods + central self-locking Tr10×2 stainless leadscrew (0 W hold!)
          * 70 mm pure vertical travel: Mode 1 DOWN (Z = -35 mm, 6-8 mm optimal Venturi STOL slot, still 10 mm inside pod belly!)
            ↔ Mode 2 UP (Z = +35 mm, 57 mm / 4-5× wake clearance Protected Staggerwing cruise, still 10 mm inside pod roof!).
          * 2× individually waterproof IP68 billet pitch servos ride DIRECTLY ON the elevator sled, direct-driving the Ø8 mm
            flaperon shafts through flush silicone cheek wiper skirts (ZERO external arms, ZERO belts/gears, ZERO sliding dry-hull seals!).
      - Shown in split demonstration: Starboard (+Y, foreground) = Mode 2 UP (Z = +35 mm, Protected Staggerwing Cruise),
        Port (-Y) = Mode 1 DOWN (Z = -35 mm, +15° Junkers STOL Takeoff) so both extremes of the 70 mm internal stroke are unmistakable!
    """
    mb = MeshBuilder()
    # Flush Bow-Contoured Hard Deck (0 boxes!) + contoured under-hull plate
    deck_st = [
        (-1050, 220, 48, 72),
        (-900, 295, 18, 42),
        (-740, 320, 3, 28),
        (60, 320, 3, 28),
        (72, 320, 3, 28),
        (760, 320, 3, 28),
    ]
    under_st = [(-1040, 130, 38, 48), (-900, 148, 8, 18), (-740, 152, -16, -2), (760, 152, -16, -2)]
    add_contoured_deck_and_underplate(mb, deck_st, under_st, latch_x=66.0)
    add_flush_ltracks(mb, z_top=28.0, x0=-680.0, x1=720.0, y_track=195.0)
    for sy in (-125, 125):
        mb.add_box(-740, 760, sy - 22, sy + 22, -24, -12, C_ALU, 1.0, stl=True)

    dz = -620.0
    add_4x_blades(mb, z_top=-22.0, z_bot=dz, fold_deg=0.0, x_front=-450.0, x_rear=320.0, y_half=122.0)
    # 90 mm tall translucent Flying-Keel Pod (100% encloses the internal vertical elevator sled!)
    add_flying_keel_pod(mb, dx=0.0, dz=dz, pod_h=90.0, with_motors=False, shell_alpha=0.34)
    add_single_centerline_prop_and_rudder(mb, dx=0.0, dz=dz, show_internal=False)

    # 1. Fixed Main Wing (1,000 cm², 100 mm chord) in LOWER THIRD of 90 mm pod (Z = dz - 22 mm)
    add_lower_wings(mb, dx=0.0, dz=dz - 22.0, half_span=560.0, root_chord=100.0, x_le=-255.0)

    # 2. Free-Flooding Internal Wing-Box (x = -142..-46 mm) separated from Dry Bay by twin curved watertight bulkheads!
    x_sled = -94.0
    def add_pod_bulkhead(bx, ry=105.0, rz=42.0, half_t=3.5):
        n_ang = 20
        rings = []
        for xx in (bx - half_t, bx + half_t):
            ring = []
            for i in range(n_ang):
                a = 2 * math.pi * i / n_ang
                ca, sa = math.cos(a), math.sin(a)
                ring.append((xx, ry * math.copysign(abs(ca) ** 0.85, ca), dz + rz * math.copysign(abs(sa) ** 0.85, sa)))
            rings.append(ring)
        mb.add_loft(rings, C_WING_UP, 0.90, stl=False, cap_ends=True)

    add_pod_bulkhead(-145.0)
    add_pod_bulkhead(-43.0)
    # Twin Ø10 mm stainless vertical guide rods (at y = ±56 mm, 100% inside curved pod!) + central gold Tr10×2 leadscrew
    for ry in (-56.0, 56.0):
        mb.add_rod((x_sled, ry, dz - 36.0), (x_sled, ry, dz + 36.0), 4.5, C_ALU, n=10, alpha=1.0, stl=True)
    mb.add_rod((x_sled, 0.0, dz - 41.0), (x_sled, 0.0, dz + 41.0), 5.5, C_KEVLAR, n=10, alpha=1.0, stl=True)
    # Compact red top leadscrew drive cap tucked inside roof contour
    mb.add_box(x_sled - 18, x_sled + 18, -20, 20, dz + 28, dz + 41, C_PUSHROD, 1.0, stl=False)
    # Curved flush silicone cheek wiper skirts hugging the exact superellipse pod wall from z = -34 to +34 mm!
    for side in (-1, 1):
        wiper_pts = []
        for k in range(9):
            t = -1.0 + 2.0 * k / 8.0  # -1..+1
            sa = 0.76 * t
            ca = math.sqrt(max(0.0, 1.0 - sa * sa))
            wy = side * 110.5 * (ca ** 0.85)
            wz = dz + 45.0 * math.copysign(abs(sa) ** 0.85, sa)
            wiper_pts.append((x_sled, wy, wz, 5.0))
        mb.add_tube_along_path(wiper_pts, C_CARBON_DARK, n=8, alpha=0.95, stl=True, cap_ends=True)

    # Dry Bay behind aft watertight bulkhead: Static IP68 wire gland + ESP32/IMU + 75100 VESC (ZERO sliding dry seals!)
    mb.add_rod((-52, 20, dz), (-32, 20, dz), 6.5, C_PUSHROD, n=10, alpha=1.0, stl=False)      # Static bulkhead cable gland
    mb.add_box(-22, 62, -34, 34, dz - 16, dz + 16, C_WING_UP, 1.0, stl=False)                 # ESP32 + 6-DOF IMU
    mb.add_box(85, 220, -56, 56, dz - 32, dz - 2, C_ALU, 1.0, stl=False)                      # 75100 VESC

    # 3. Split Demonstration of the 70 mm Pure Vertical Internal Elevator Sled:
    #    - Starboard (+Y, foreground!): Mode 2 UP (Z = +32 mm, Protected Staggerwing Cruise — 54 mm / 4-5× above wake!)
    #    - Port (-Y): Mode 1 DOWN (Z = -32 mm, +15° Junkers STOL Takeoff — 6-8 mm optimal Venturi slot!)
    fl_sec = naca4_section(0.02, 0.4, 0.11, 60.0, n=10)
    for side, z_off, pitch_deg, col in [(1, 32.0, 1.5, C_FLAP_R), (-1, -32.0, 15.0, C_FLAP_L)]:
        fz = dz + z_off
        # Internal Aluminum Elevator Sled half-carriage riding inside pod curve on the Ø10 mm guide rod + Tr10×2 leadscrew
        y0, y1 = (0, 66) if side > 0 else (-66, 0)
        mb.add_box(x_sled - 18, x_sled + 18, y0, y1, fz - 8, fz + 8, C_ALU, 1.0, stl=True)
        # Individually waterproof IP68 billet pitch servo riding DIRECTLY ON the sled (0 belts/gears!)
        mb.add_box(x_sled - 15, x_sled + 15, side * 34 - 16, side * 34 + 16, fz - 9, fz + 9, C_KEVLAR, 1.0, stl=False)
        # Direct-drive Ø8 mm stainless shaft straight from IP68 servo through flush silicone wiper into flaperon 20%-chord root!
        mb.add_cylinder_y(x_sled, side * 48, side * 98, fz, 4.2, C_PUSHROD, n=10, alpha=1.0, stl=True)
        # Flaperon lofted blade starting cleanly flush at the curved pod shoulder (Y = ±84 mm -> ±560 mm)
        rad = math.radians(pitch_deg)
        rings = []
        for dist in (84, 320, 560):
            y = side * dist
            rings.append([(x_sled + (xl - 12.0) * math.cos(rad) + zl * math.sin(rad), y, fz - (xl - 12.0) * math.sin(rad) + zl * math.cos(rad)) for xl, zl in fl_sec])
        mb.add_loft(rings, col, 1.0, stl=True)

    # Translucent vertical stroke guide bar on foreground Starboard cheek showing pure vertical internal travel!
    mb.add_rod((x_sled, 126.0, dz - 32.0), (x_sled, 126.0, dz + 32.0), 3.6, C_WING_UP, n=8, alpha=0.75, stl=False)

    write_binary_stl(mb, MODELS_DIR / "10_morphing_stol_staggerwing_pod.stl", "FoilSkiff 10 (Upgrade): 100% Internal-Pod Morphing STOL-to-Staggerwing Sled (mm)")
    callouts = [
        ((-920, 0, 56), "left", 96, 245, "100% Flush Bow-Contoured Hard Deck", "ZERO deck boxes • Entire sled fits inside 90 mm pod!"),
        ((-94, 420, dz + 35), "left", 218, 245, "Mode 2 UP (Z = +35 mm): Staggerwing", "57 mm (4–5×) above wake • Still 10 mm inside pod roof!"),
        ((-94, 128, dz), "left", 355, 245, "70 mm Pure Vertical Internal Stroke", "ZERO external arms • Flush silicone cheek wiper skirts"),
        ((-220, 440, dz - 22), "left", 488, 245, "Fixed Main Wing (Lower Third, -22 mm)", "Shields UP flaperons from kelp/logs • 6–8 mm STOL slot"),
        ((320, -122, -290), "right", 104, 795, "Clean 4× Blades (0 External Pushrods!)", "Self-contained 90 mm pod • No fold binding"),
        ((-94, 0, dz + 35), "right", 232, 795, "Wet-Slot Sled: Tr10×2 + IP68 Servos", "Direct Ø8 mm drive ON sled • 0 belts, 0 sliding dry seals!"),
        ((-94, -420, dz - 35), "right", 372, 795, "Mode 1 DOWN (Z = -35 mm): STOL (+15°)", "Optimal 6–8 mm Venturi slot • Still 10 mm above pod belly!"),
        ((725, 0, dz), "right", 495, 800, "Dry IP68 Bay + Static Bulkhead Gland", "Only a stationary servo cable enters dry battery/VESC bay"),
    ]
    render_3d_svg(
        mb, DIAG_DIR / "19-morphing-stol-staggerwing-3d-cad.svg",
        "3D CAD Model 10 (Upgrade): 100% Internal-Pod Morphing STOL-to-Staggerwing Sled",
        "Split Demo: Foreground = Mode 2 UP (+35 mm Staggerwing) | Far = Mode 1 DOWN (-35 mm STOL) • ZERO External Arms or Belts!",
        callouts, az_deg=-134, el_deg=23, scale=0.37, z_center=295,
        footer="Interactive 3D STL: models/10_morphing_stol_staggerwing_pod.stl (100% Internal-Pod Wet-Slot Elevator Sled)",
    )
    render_openscad_png(mb, RENDERS_DIR / "10-morphing-stol-staggerwing-3d.png", "10,0,-305,66,0,226,3150")


if __name__ == "__main__":
    for old_f in [
        MODELS_DIR / "01_step_out_flying_keel_truekit.stl",
        MODELS_DIR / "04_retracted_beaching_truekit.stl",
        MODELS_DIR / "01_navigator300_step_out_flying_keel.stl",
        MODELS_DIR / "05_discovery330_oframe_step_out.stl",
        DIAG_DIR / "00-foil-skiff-3d-cad.svg",
        DIAG_DIR / "08-retracted-beaching-3d.svg",
        RENDERS_DIR / "01-step-out-truekit-3d.png",
        RENDERS_DIR / "04-retracted-beaching-3d.png",
        RENDERS_DIR / "01-navigator300-step-out-3d.png",
    ]:
        if old_f.exists():
            old_f.unlink()

    build_model_01_navigator300()
    build_model_02_switchblade()
    build_model_03_stol_flaperons()
    build_model_04_navigator300_retracted()
    build_model_05_discovery330()
    build_model_06_lr_8020()
    build_model_07_lr_max_range()
    build_model_08_lr_pod_closeup()
    build_model_09_modular_seating()
    build_model_10_morphing_stol_staggerwing()
    print("All 10 3D STL models, 10 annotated 3D SVGs, and 10 OpenSCAD PNG renders generated successfully.")
