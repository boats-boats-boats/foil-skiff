#!/usr/bin/env python3
"""
Generate mathematically-scaled 2D technical SVG engineering diagrams for FoilSkiff.
Zero external dependencies (pure Python 3 standard library).
"""

import html
import math
from pathlib import Path

OUT_DIR = Path(__file__).parent

FONT = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'


def svg_header(width: int, height: int, title: str, subtitle: str) -> str:
    title = html.escape(title)
    subtitle = html.escape(subtitle)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M 24 0 L 0 0 0 24" fill="none" stroke="#E2E8F0" stroke-width="0.6"/>
    </pattern>
    <linearGradient id="carbon" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#334155"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <linearGradient id="alu" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#CBD5E1"/>
      <stop offset="100%" stop-color="#64748B"/>
    </linearGradient>
    <linearGradient id="wingBlue" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#38BDF8"/>
      <stop offset="100%" stop-color="#0284C7"/>
    </linearGradient>
    <linearGradient id="wingTeal" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#2DD4BF"/>
      <stop offset="100%" stop-color="#0D9488"/>
    </linearGradient>
    <linearGradient id="water" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#BAE6FD" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#0284C7" stop-opacity="0.18"/>
    </linearGradient>
    <linearGradient id="kevlar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FBBF24"/>
      <stop offset="100%" stop-color="#D97706"/>
    </linearGradient>
    <linearGradient id="tubeGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#F1F5F9"/>
      <stop offset="55%" stop-color="#CBD5E1"/>
      <stop offset="100%" stop-color="#94A3B8"/>
    </linearGradient>
    <marker id="arrDark" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#334155"/>
    </marker>
    <marker id="arrBlue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284C7"/>
    </marker>
    <marker id="arrGreen" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669"/>
    </marker>
    <marker id="arrRed" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#DC2626"/>
    </marker>
    <style>
      text {{ font-family: {FONT}; }}
      .title {{ font-size: 18px; font-weight: 700; fill: #0F172A; }}
      .sub {{ font-size: 12px; fill: #475569; }}
      .sec {{ font-size: 13.5px; font-weight: 700; fill: #0F172A; }}
      .lbl {{ font-size: 11px; font-weight: 600; fill: #1E293B; }}
      .lbl-sm {{ font-size: 10px; fill: #475569; }}
      .lbl-w {{ font-size: 10.5px; font-weight: 700; fill: #FFFFFF; }}
      .dim {{ font-size: 10px; font-weight: 600; fill: #0284C7; }}
      .ok {{ font-size: 10.5px; font-weight: 700; fill: #059669; }}
      .warn {{ font-size: 10.5px; font-weight: 700; fill: #DC2626; }}
    </style>
  </defs>
  <rect x="1" y="1" width="{width-2}" height="{height-2}" rx="12" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5"/>
  <rect x="12" y="56" width="{width-24}" height="{height-68}" rx="8" fill="url(#grid)" stroke="#E2E8F0" stroke-width="1"/>
  <text x="24" y="28" class="title">{title}</text>
  <text x="24" y="46" class="sub">{subtitle}</text>
'''


def naca4_points(m: float, p: float, t: float, chord: float, n: int = 36):
    """Return closed (x, y) polygon points for a NACA 4-digit airfoil with LE at (0,0), TE at (chord,0), y-up."""
    upper, lower = [], []
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
        upper.append(((xc - yt * math.sin(th)) * chord, (yc + yt * math.cos(th)) * chord))
        lower.append(((xc + yt * math.sin(th)) * chord, (yc - yt * math.cos(th)) * chord))
    return upper + list(reversed(lower[1:-1]))


def transform_pts(pts, ox, oy, deg=0.0, flip_y=True):
    """Transform math coords (y-up) to SVG coords (y-down) rotated clockwise by deg."""
    rad = math.radians(deg)
    c, s = math.cos(rad), math.sin(rad)
    out = []
    for x, y in pts:
        # In math y-up, clockwise rotation by deg is: x' = x*cos + y*sin, y' = -x*sin + y*cos
        xr = x * c + y * s
        yr = -x * s + y * c
        sx = ox + xr
        sy = oy - yr if flip_y else oy + yr
        out.append((sx, sy))
    return out


def pts_to_str(pts) -> str:
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def dim_line(x1, y1, x2, y2, label, dx=0, dy=-6, cls="dim", marker="arrBlue", stroke="#0284C7"):
    mx, my = (x1 + x2) / 2 + dx, (y1 + y2) / 2 + dy
    return (
        f'  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{stroke}" stroke-width="1.2" marker-start="url(#{marker})" marker-end="url(#{marker})"/>\n'
        f'  <text x="{mx:.1f}" y="{my:.1f}" text-anchor="middle" class="{cls}">{label}</text>\n'
    )


# -------------------------------------------------------------------------
# DIAGRAM 1: Flush-Nested Top-Deck Switchblade Wing (Top-Down)
# -------------------------------------------------------------------------
def gen_01_switchblade():
    W, H = 1040, 560
    s = svg_header(
        W, H,
        "1. Flush-Nested Top-Deck Switchblade Wing (Top-Down Scale Geometry)",
        "1,300 x 220 mm Lifting Battery-Fuselage — 0 cm² Extra Wet Area Closed vs. +1,300 cm² (1.58 m Span, AR ≈ 15) Deployed"
    )
    # Scale: 1 mm = 0.30 px -> 1300 mm = 390 px, 220 mm = 66 px, 680 mm blade = 204 px, 105 mm chord = 31.5 px
    sc = 0.30

    def draw_fuselage_top(cx_nose, cy):
        # Streamlined 1300x220 mm fuselage top outline
        L = 1300 * sc  # 390 px
        hw = 110 * sc  # 33 px
        # Kevlar nose cone (0..180 mm)
        pts_body = []
        for i in range(41):
            u = i / 40.0
            x = cx_nose + u * L
            # Blunt elliptical nose, parallel midbody, tapered tailcone
            if u < 0.16:
                w = hw * math.sqrt(1 - ((0.16 - u) / 0.16) ** 2)
            elif u < 0.72:
                w = hw
            else:
                v = (u - 0.72) / 0.28
                w = hw * (1 - 0.72 * v**1.5)
            pts_body.append((x, cy - w))
        for i in range(40, -1, -1):
            u = i / 40.0
            x = cx_nose + u * L
            if u < 0.16:
                w = hw * math.sqrt(1 - ((0.16 - u) / 0.16) ** 2)
            elif u < 0.72:
                w = hw
            else:
                v = (u - 0.72) / 0.28
                w = hw * (1 - 0.72 * v**1.5)
            pts_body.append((x, cy + w))
        out = f'  <polygon points="{pts_to_str(pts_body)}" fill="url(#carbon)" stroke="#0F172A" stroke-width="1.8"/>\n'
        # Kevlar crush nose overlay (first 120 mm)
        nose_pts = []
        for i in range(15):
            u = 0.11 * i / 14.0
            x = cx_nose + u * L
            w = hw * math.sqrt(max(0, 1 - ((0.16 - u) / 0.16) ** 2))
            nose_pts.append((x, cy - w))
        for i in range(14, -1, -1):
            u = 0.11 * i / 14.0
            x = cx_nose + u * L
            w = hw * math.sqrt(max(0, 1 - ((0.16 - u) / 0.16) ** 2))
            nose_pts.append((x, cy + w))
        out += f'  <polygon points="{pts_to_str(nose_pts)}" fill="url(#kevlar)" stroke="#92400E" stroke-width="1.2"/>\n'
        # Lower fixed thin wings (1,250 cm² -> ~1.12 m span x 110 mm chord, centered at x=450 mm)
        wx = cx_nose + 420 * sc
        wc = 105 * sc
        wspan = 520 * sc  # each side from centerline (~1.04m total)
        out += (
            f'  <path d="M {wx:.1f} {cy-hw:.1f} L {wx+14:.1f} {cy-wspan:.1f} Q {wx+wc*0.6:.1f} {cy-wspan-6:.1f} {wx+wc:.1f} {cy-wspan+8:.1f} '
            f'L {wx+wc:.1f} {cy-hw:.1f} Z" fill="#475569" fill-opacity="0.38" stroke="#334155" stroke-width="1.2" stroke-dasharray="4,2"/>\n'
            f'  <path d="M {wx:.1f} {cy+hw:.1f} L {wx+14:.1f} {cy+wspan:.1f} Q {wx+wc*0.6:.1f} {cy+wspan+6:.1f} {wx+wc:.1f} {cy+wspan-8:.1f} '
            f'L {wx+wc:.1f} {cy+hw:.1f} Z" fill="#475569" fill-opacity="0.38" stroke="#334155" stroke-width="1.2" stroke-dasharray="4,2"/>\n'
        )
        # Twin 65161 tailcone motor pods
        tx = cx_nose + 1230 * sc
        for side in (-1, 1):
            my = cy + side * 24
            out += f'  <rect x="{tx:.1f}" y="{my-7:.1f}" width="32" height="14" rx="5" fill="#1E293B" stroke="#0F172A" stroke-width="1.2"/>\n'
            out += f'  <line x1="{tx+34:.1f}" y1="{my-12:.1f}" x2="{tx+34:.1f}" y2="{my+12:.1f}" stroke="#0284C7" stroke-width="2.5"/>\n'
        # 4x Side-Straddling Struts at x=200 mm & x=960 mm
        for sx_mm, tag in [(200, "x=200"), (960, "x=960")]:
            sx = cx_nose + sx_mm * sc
            for side in (-1, 1):
                sy = cy + side * (hw + 6)
                out += f'  <ellipse cx="{sx:.1f}" cy="{sy:.1f}" rx="9" ry="3.2" fill="#0F172A" stroke="#38BDF8" stroke-width="1.2"/>\n'
        # Recessed top pocket outline (x=220..905 mm, width=210 mm)
        px1 = cx_nose + 220 * sc
        pw = 685 * sc
        ph = 210 * sc
        out += f'  <rect x="{px1:.1f}" y="{cy-ph/2:.1f}" width="{pw:.1f}" height="{ph:.1f}" rx="4" fill="#0F172A" fill-opacity="0.45" stroke="#94A3B8" stroke-width="1" stroke-dasharray="3,2"/>\n'
        return out

    # --- LEFT PANEL: CLOSED (CRUISE 10-22 kn) ---
    s += '  <rect x="24" y="68" width="484" height="468" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>\n'
    s += '  <text x="42" y="94" class="sec">A. CLOSED — Cruise Mode (10–22 kn)</text>\n'
    s += '  <text x="42" y="112" class="ok">0 cm² extra wet area • 0 exposed tips • 30.8 nm @ 15.5 kn • 32.3 lbf @ 22 kn</text>\n'
    lx, ly = 68, 300
    s += draw_fuselage_top(lx, ly)
    # Closed switchblade blades nested side-by-side inside pocket
    bx1 = lx + 222 * sc
    blen = 680 * sc
    bch = 102 * sc
    s += f'  <rect x="{bx1:.1f}" y="{ly-bch-0.8:.1f}" width="{blen:.1f}" height="{bch:.1f}" rx="6" fill="url(#wingBlue)" stroke="#0369A1" stroke-width="1.4"/>\n'
    s += f'  <rect x="{bx1:.1f}" y="{ly+0.8:.1f}" width="{blen:.1f}" height="{bch:.1f}" rx="6" fill="url(#wingBlue)" stroke="#0369A1" stroke-width="1.4"/>\n'
    # Carbon overhang bridge across x=215..285 mm
    brx = lx + 212 * sc
    s += f'  <rect x="{brx:.1f}" y="{ly-34:.1f}" width="{70*sc:.1f}" height="68" rx="3" fill="#1E293B" fill-opacity="0.88" stroke="#F8FAFC" stroke-width="1.1"/>\n'
    # Pivot pins at x=245 mm
    for side in (-1, 1):
        s += f'  <circle cx="{lx+248*sc:.1f}" cy="{ly+side*15:.1f}" r="3.2" fill="#FBBF24" stroke="#0F172A" stroke-width="1"/>\n'
    # Labels Left Panel
    s += f'  <text x="{bx1+blen/2:.1f}" y="{ly-bch/2+3:.1f}" text-anchor="middle" class="lbl-w">Left Blade (680×105 mm)</text>\n'
    s += f'  <text x="{bx1+blen/2:.1f}" y="{ly+bch/2+4:.1f}" text-anchor="middle" class="lbl-w">Right Blade (680×105 mm)</text>\n'
    s += dim_line(lx, ly + 175, lx + 1300 * sc, ly + 175, "1,300 mm Fuselage Length (26 L Buoyancy)", dy=16)
    s += dim_line(lx + 200 * sc, ly - 62, lx + 960 * sc, ly - 62, "760 mm Clear Span Between Strut Pairs", dy=-8)
    s += f'  <text x="{lx+200*sc:.1f}" y="{ly-90:.1f}" text-anchor="middle" class="lbl-sm">Front Struts (x=200)</text>\n'
    s += f'  <text x="{lx+960*sc:.1f}" y="{ly-90:.1f}" text-anchor="middle" class="lbl-sm">Rear Struts (x=960)</text>\n'
    s += f'  <text x="{lx+420*sc+16:.1f}" y="{ly-170:.1f}" text-anchor="middle" class="lbl-sm">Fixed 1,250 cm² Lower Thin Wings (Dashed)</text>\n'
    s += f'  <text x="{lx+905*sc:.1f}" y="{ly+66:.1f}" text-anchor="middle" class="lbl-sm">2–3 mm Sand Flush Slots</text>\n'
    s += f'  <line x1="{lx+905*sc:.1f}" y1="{ly+54:.1f}" x2="{lx+902*sc:.1f}" y2="{ly+32:.1f}" stroke="#475569" stroke-width="1" marker-end="url(#arrDark)"/>\n'
    s += f'  <text x="{lx+245*sc:.1f}" y="{ly+94:.1f}" text-anchor="middle" class="lbl-sm">70 mm Carbon Overhang Bridge</text>\n'
    s += f'  <line x1="{lx+245*sc:.1f}" y1="{ly+82:.1f}" x2="{lx+245*sc:.1f}" y2="{ly+36:.1f}" stroke="#475569" stroke-width="1" marker-end="url(#arrDark)"/>\n'
    s += f'  <text x="{lx+18:.1f}" y="{ly+62:.1f}" text-anchor="middle" class="lbl-sm">Kevlar</text>\n'
    s += f'  <text x="{lx+18:.1f}" y="{ly+74:.1f}" text-anchor="middle" class="lbl-sm">Nose</text>\n'

    # --- RIGHT PANEL: DEPLOYED (TAKEOFF 0-9 kn) ---
    s += '  <rect x="532" y="68" width="484" height="468" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>\n'
    s += '  <text x="550" y="94" class="sec">B. DEPLOYED — Takeoff Mode (0–9 kn)</text>\n'
    s += '  <text x="550" y="112" class="dim">+1,300 cm² High-Aspect Switchblades • 1.58 m Span (AR ≈ 15) • 6.7 kn Takeoff</text>\n'
    rx, ry = 578, 300
    s += draw_fuselage_top(rx, ry)
    # Deployed blades swinging 90 deg out from pivot x=248 mm
    px = rx + 248 * sc
    # Left (top) blade: extends upward 680*sc = 204 px? Scale nicely (165 px so it fits comfortably inside card with labels)
    bvis = 158
    s += f'  <rect x="{px-14:.1f}" y="{ry-bvis-15:.1f}" width="{bch:.1f}" height="{bvis:.1f}" rx="8" fill="url(#wingBlue)" stroke="#0369A1" stroke-width="1.5"/>\n'
    s += f'  <rect x="{px-14:.1f}" y="{ry+15:.1f}" width="{bch:.1f}" height="{bvis:.1f}" rx="8" fill="url(#wingBlue)" stroke="#0369A1" stroke-width="1.5"/>\n'
    # Overhang bridge covering roots (x=212..282)
    s += f'  <rect x="{rx+212*sc:.1f}" y="{ry-34:.1f}" width="{70*sc:.1f}" height="68" rx="3" fill="#1E293B" fill-opacity="0.90" stroke="#FBBF24" stroke-width="1.3"/>\n'
    for side in (-1, 1):
        s += f'  <circle cx="{px:.1f}" cy="{ry+side*15:.1f}" r="3.2" fill="#FBBF24" stroke="#0F172A" stroke-width="1"/>\n'
    # Sweep arc arrows showing hydrodynamic self-closing!
    s += f'  <path d="M {px+24:.1f} {ry-125:.1f} A 115 115 0 0 1 {px+125:.1f} {ry-26:.1f}" fill="none" stroke="#059669" stroke-width="1.8" stroke-dasharray="5,3" marker-end="url(#arrGreen)"/>\n'
    s += f'  <path d="M {px+24:.1f} {ry+125:.1f} A 115 115 0 0 0 {px+125:.1f} {ry+26:.1f}" fill="none" stroke="#059669" stroke-width="1.8" stroke-dasharray="5,3" marker-end="url(#arrGreen)"/>\n'
    s += f'  <text x="{px+118:.1f}" y="{ry-100:.1f}" class="ok">Water drag</text>\n'
    s += f'  <text x="{px+118:.1f}" y="{ry-86:.1f}" class="ok">self-closes</text>\n'
    s += f'  <text x="{px+118:.1f}" y="{ry-72:.1f}" class="ok">flush @ 9–10 kn</text>\n'
    s += f'  <text x="{px+118:.1f}" y="{ry+95:.1f}" class="lbl-sm">Zero bending on pivot:</text>\n'
    s += f'  <text x="{px+118:.1f}" y="{ry+109:.1f}" class="lbl-sm">70 mm root slides under</text>\n'
    s += f'  <text x="{px+118:.1f}" y="{ry+123:.1f}" class="lbl-sm">carbon overhang bridge</text>\n'
    s += f'  <text x="{px+118:.1f}" y="{ry+137:.1f}" class="lbl-sm">(90 MPa takeoff / 181 MPa 2G)</text>\n'
    # Total span dimension on left edge of right panel
    s += dim_line(rx + 25, ry - bvis - 15, rx + 25, ry + bvis + 15, "", stroke="#0284C7")
    s += f'  <text x="{rx+18:.1f}" y="{ry:.1f}" text-anchor="middle" transform="rotate(-90 {rx+18:.1f} {ry:.1f})" class="dim">1.58 m Total Span (AR ≈ 15)</text>\n'
    # Flow arrow
    s += f'  <line x1="548" y1="300" x2="572" y2="300" stroke="#0284C7" stroke-width="2" marker-end="url(#arrBlue)"/>\n'
    s += '  <text x="556" y="290" text-anchor="middle" class="dim">Flow</text>\n'

    s += "</svg>\n"
    (OUT_DIR / "01-switchblade-wing-topdown.svg").write_text(s)


# -------------------------------------------------------------------------
# DIAGRAM 2: STOL External Slotted Flap vs. Negative-Stagger Biplane
# -------------------------------------------------------------------------
def gen_02_stol_flaperons():
    W, H = 1040, 500
    s = svg_header(
        W, H,
        "2. Submerged Variable-Angle Secondary Wing: Staggerwing vs. STOL Slotted Flaperon",
        "Exact NACA 4-Digit Airfoil Cross-Sections • 20% Chord Balanced Pivot (26–37 kg·cm Torque, Mechanical 0° Failsafe)"
    )

    # Panel A (Top): Above & Behind (Negative-Stagger Biplane / Staggerwing)
    s += '  <rect x="24" y="68" width="484" height="408" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>\n'
    s += '  <rect x="34" y="114" width="464" height="270" rx="6" fill="url(#water)"/>\n'
    s += '  <text x="42" y="92" class="sec">A. Above &amp; Behind (Negative-Stagger "Staggerwing")</text>\n'
    s += '  <text x="42" y="108" class="lbl-sm">Gentle stall • Higher rock clearance • Rear-strut mount (CL_max ≈ 1.65)</text>\n'

    # Main wing NACA 2410 (chord 210 px)
    main_a = transform_pts(naca4_points(0.02, 0.4, 0.10, 210), 100, 290, deg=2)
    s += f'  <polygon points="{pts_to_str(main_a)}" fill="url(#carbon)" stroke="#0F172A" stroke-width="1.6"/>\n'
    s += '  <text x="195" y="322" text-anchor="middle" class="lbl">Main Wing (1,000–1,350 cm², t/c = 10%)</text>\n'
    # Upper-aft secondary wing (chord 115 px, +12 deg takeoff)
    sec_a_cr = transform_pts(naca4_points(0.02, 0.4, 0.11, 115), 255, 215, deg=0)
    sec_a_to = transform_pts(naca4_points(0.02, 0.4, 0.11, 115), 255, 215, deg=14)
    s += f'  <polygon points="{pts_to_str(sec_a_cr)}" fill="none" stroke="#64748B" stroke-width="1.3" stroke-dasharray="4,3"/>\n'
    s += f'  <polygon points="{pts_to_str(sec_a_to)}" fill="url(#wingTeal)" stroke="#0F766E" stroke-width="1.5"/>\n'
    s += '  <circle cx="278" cy="218" r="4" fill="#FBBF24" stroke="#0F172A" stroke-width="1.2"/>\n'
    # Streamlines
    for sy in [245, 270, 305]:
        s += f'  <path d="M 48 {sy} Q 180 {sy-16} 310 {sy-10} T 470 {sy+14}" fill="none" stroke="#0284C7" stroke-width="1.2" stroke-opacity="0.55" marker-end="url(#arrBlue)"/>\n'
    s += '  <text x="355" y="185" text-anchor="middle" class="lbl">Secondary Wing (Pivots +12° TO → 0° Cruise)</text>\n'
    s += '  <text x="360" y="268" text-anchor="middle" class="lbl-sm">Dashed = 0° Cruise Position</text>\n'
    s += dim_line(232, 218, 232, 288, "50–100 mm Up", dx=-44, dy=4)
    s += '  <text x="42" y="408" class="lbl">Pros: Highest rock clearance, gentle stall, easy rear-strut mount.</text>\n'
    s += '  <text x="42" y="426" class="lbl-sm">Trade-off: Lower max lift (CL_max ≈ 1.65) than below-and-behind STOL slot.</text>\n'
    s += '  <text x="42" y="446" class="lbl-sm">4-in-1 Control: Takeoff lift, Direct-Lift elevation, roll leveling &amp; braking.</text>\n'

    # Panel B (Right): Slightly Below & Behind (True STOL Slotted Flap / Junkers Wing)
    s += '  <rect x="532" y="68" width="484" height="408" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>\n'
    s += '  <rect x="542" y="114" width="464" height="270" rx="6" fill="url(#water)"/>\n'
    s += '  <text x="550" y="92" class="sec">B. Slightly Below &amp; Behind (True STOL Slotted Flaperon)</text>\n'
    s += '  <text x="550" y="108" class="ok">Converging slot jet → CL_max ≈ 1.95–2.10 • 29.8 nm @ 15.5 kn</text>\n'

    # Main wing 1,000 cm2 (chord 190 px)
    main_b = transform_pts(naca4_points(0.02, 0.4, 0.10, 195), 590, 235, deg=2)
    s += f'  <polygon points="{pts_to_str(main_b)}" fill="url(#carbon)" stroke="#0F172A" stroke-width="1.6"/>\n'
    s += '  <text x="682" y="196" text-anchor="middle" class="lbl">Compact Main Wing (1,000 cm²)</text>\n'
    # Split 2x 250 cm2 flaperon (chord 105 px, pivot at 20% chord!)
    fl_cr = transform_pts(naca4_points(0.02, 0.4, 0.11, 105), 765, 268, deg=0)
    fl_to = transform_pts(naca4_points(0.02, 0.4, 0.11, 105), 765, 268, deg=18)
    s += f'  <polygon points="{pts_to_str(fl_cr)}" fill="none" stroke="#64748B" stroke-width="1.3" stroke-dasharray="4,3"/>\n'
    s += f'  <polygon points="{pts_to_str(fl_to)}" fill="url(#wingBlue)" stroke="#0369A1" stroke-width="1.6"/>\n'
    # Pivot pin at 20% chord — DIRECT-DRIVE internal pod servo + Ø8 mm double-O-ring sealed torque tube (ZERO deck boxes!)
    piv_x, piv_y = 786, 272
    # Translucent pod aft-bay outline showing internal IP67 servo right next to the flaperon root!
    s += f'  <rect x="{piv_x-18}" y="{piv_y-54}" width="64" height="40" rx="5" fill="#1E293B" fill-opacity="0.88" stroke="#FBBF24" stroke-width="1.4"/>\n'
    s += f'  <text x="{piv_x+14}" y="{piv_y-37}" text-anchor="middle" style="font-size:8.5px;fill:#FBBF24;font-weight:700;">IP67 Servo</text>\n'
    s += f'  <text x="{piv_x+14}" y="{piv_y-25}" text-anchor="middle" style="font-size:7.8px;fill:#E2E8F0;">INSIDE Pod!</text>\n'
    # Short internal linkage / Ø8 mm sealed stainless torque shaft directly to 20%-chord pivot
    s += f'  <line x1="{piv_x}" y1="{piv_y}" x2="{piv_x}" y2="{piv_y-16}" stroke="#FBBF24" stroke-width="4" stroke-linecap="round"/>\n'
    s += f'  <circle cx="{piv_x}" cy="{piv_y}" r="5.0" fill="#FBBF24" stroke="#0F172A" stroke-width="1.3"/>\n'
    s += f'  <text x="{piv_x+14}" y="145" text-anchor="middle" class="ok">Internal Pod Servos</text>\n'
    s += f'  <text x="{piv_x+14}" y="159" text-anchor="middle" class="lbl-sm">Ø8 mm double-O-ring shaft</text>\n'
    s += f'  <text x="{piv_x+14}" y="173" text-anchor="middle" class="ok">ZERO deck boxes / pushrods!</text>\n'
    s += f'  <line x1="{piv_x+14}" y1="178" x2="{piv_x+14}" y2="{piv_y-56}" stroke="#059669" stroke-width="1.2" marker-end="url(#arrGreen)"/>\n'
    # Converging high-pressure slot jet streamlines!
    s += '  <path d="M 555 268 Q 680 264 762 248 Q 815 244 895 292" fill="none" stroke="#059669" stroke-width="2.4" marker-end="url(#arrGreen)"/>\n'
    s += '  <path d="M 555 284 Q 685 278 760 258 Q 812 256 888 304" fill="none" stroke="#059669" stroke-width="1.8" stroke-opacity="0.8" marker-end="url(#arrGreen)"/>\n'
    s += '  <text x="688" y="302" text-anchor="middle" class="ok">High-pressure converging slot jet</text>\n'
    s += '  <text x="688" y="316" text-anchor="middle" class="ok">(prevents rear-wing stall @ +15°!)</text>\n'
    s += '  <text x="895" y="255" text-anchor="middle" class="lbl-sm">0° Cruise</text>\n'
    s += '  <text x="905" y="334" text-anchor="middle" class="dim">+15° Takeoff / ±3° Trim</text>\n'
    s += '  <text x="550" y="408" class="lbl">20%-Chord Direct-Drive: 26–37 kg·cm torque (8–22 kn), self-centers to 0°.</text>\n'
    s += '  <text x="550" y="426" class="lbl-sm">Split 2×250 cm²: Takeoff Flaps + Elevation + Roll + Banked Turns.</text>\n'
    s += '  <text x="550" y="446" class="ok">PRIMARY: 400 mm deep (0 wave slam) • Servos sealed inside pod (0 deck boxes!)</text>\n'

    s += "</svg>\n"
    (OUT_DIR / "02-stol-flaperons-cross-section.svg").write_text(s)


# -------------------------------------------------------------------------
# DIAGRAM 3: Spine-Floor Top-to-Bottom Coupling Options (O-Frame / C-Frame / OEM Slot)
# -------------------------------------------------------------------------
def gen_03_spine_coupling():
    W, H = 1040, 910
    s = svg_header(
        W, H,
        "3. Drop-In Rigid Spine Floor & Coupling Options (True Kit Navigator 300 Primary + Discovery 330)",
        "Bridging the Continuous 1.2 mm PVC Tunnel Web — Zero-Hole Navigator 300 Hybrid C-Frame, Switchable Magnets, Discovery O-Frame & OEM Slot"
    )

    def draw_hull_base(y0, open_bow=False, tru_alu_transom=True, show_deck_labels=True):
        # Inflatable catamaran silhouette with REAL upward bow rocker curve!
        out = f'  <path d="M 110 {y0-54} L 870 {y0-54} Q 920 {y0-54} 920 {y0+10} Q 920 {y0+66} 865 {y0+66} L 240 {y0+66} Q 150 {y0+62} 95 {y0+18} Q 76 {y0-28} 110 {y0-54} Z" fill="#E2E8F0" fill-opacity="0.35" stroke="#94A3B8" stroke-width="1.2" stroke-dasharray="6,4"/>\n'
        # Continuous 1.2 mm PVC tunnel web bending UPWARD in the bow (X = 270 -> 150 rises smoothly 24 px!)
        out += f'  <path d="M 830 {y0} L 285 {y0} Q 215 {y0-2} 152 {y0-24}" fill="none" stroke="#64748B" stroke-width="4" stroke-linecap="round"/>\n'
        if not open_bow:
            out += f'  <path d="M 152 {y0-24} Q 108 {y0-32} 96 {y0-50} Q 102 {y0-64} 148 {y0-58}" fill="#CBD5E1" fill-opacity="0.55" stroke="#475569" stroke-width="2.5"/>\n'
            out += f'  <rect x="96" y="{y0-24}" width="12" height="12" rx="2" fill="#FBBF24" stroke="#0F172A" stroke-width="1.2"/>\n'
            out += f'  <text x="122" y="{y0-56}" text-anchor="middle" class="lbl-sm">Closed Bow</text>\n'
        else:
            out += f'  <text x="124" y="{y0-42}" text-anchor="middle" class="ok">Open Bow</text>\n'
        if tru_alu_transom:
            out += f'  <rect x="828" y="{y0-56}" width="12" height="58" rx="2" fill="url(#alu)" stroke="#334155" stroke-width="1.4"/>\n'
            out += f'  <text x="892" y="{y0-36}" text-anchor="middle" class="lbl-sm">Tru-Alu</text>\n'
            out += f'  <text x="892" y="{y0-24}" text-anchor="middle" class="lbl-sm">Transom</text>\n'
        else:
            out += f'  <text x="880" y="{y0-28}" text-anchor="middle" class="ok">Open Transom</text>\n'
        # Contoured 2-Piece Hard Deck (Front half BENDS UP smoothly with bow rocker; zero protruding boxes above deck!)
        out += (
            f'  <path d="M 496 {y0-20} L 285 {y0-20} Q 222 {y0-22} 162 {y0-41} L 166 {y0-26} Q 224 {y0-7} 285 {y0-5} L 496 {y0-5} Z" '
            f'fill="url(#carbon)" stroke="#0F172A" stroke-width="1.4"/>\n'
        )
        out += f'  <rect x="501" y="{y0-20}" width="324" height="15" rx="3" fill="url(#carbon)" stroke="#0F172A" stroke-width="1.4"/>\n'
        out += f'  <rect x="492" y="{y0-22}" width="14" height="19" rx="2" fill="#FBBF24" stroke="#0F172A" stroke-width="1"/>\n'
        if show_deck_labels:
            out += f'  <text x="355" y="{y0-9}" text-anchor="middle" class="lbl-w">Bow-Contoured Hard Deck</text>\n'
            out += f'  <text x="663" y="{y0-9}" text-anchor="middle" class="lbl-w">Rear Hard Deck (100% Flush!)</text>\n'
        return out

    # --- SECTION 1 (PRIMARY): NAVIGATOR 300 HYBRID C-FRAME + BOW D-RING DYNEEMA SLING ---
    s += '  <rect x="24" y="68" width="992" height="196" rx="8" fill="#FFFFFF" stroke="#059669" stroke-width="1.8"/>\n'
    s += '  <text x="42" y="92" class="ok">1. PRIMARY (True Kit Navigator 300): Contoured Bow-Bent Hybrid C-Frame + 6 mm Dyneema Bow Sling</text>\n'
    s += '  <text x="42" y="109" class="lbl-sm">Both Hard Deck &amp; under-hull plate bend UP with bow contour • Clamps onto Tru-Alu transom • Zero boxes above deck!</text>\n'
    y1 = 186
    s += draw_hull_base(y1, open_bow=False, tru_alu_transom=True)
    # Contoured under-hull plate/rails hugging curved PVC web with upward bow ski-bend + over-transom clamp jaw!
    s += f'  <path d="M 185 {y1-4} Q 232 {y1+12} 290 {y1+13} L 848 {y1+13} L 848 {y1-34} L 822 {y1-34} L 822 {y1-14}" fill="none" stroke="#0284C7" stroke-width="8.5" stroke-linejoin="round" stroke-linecap="round"/>\n'
    # Red 6 mm Dyneema sling from upturned bow nose of under-hull plate (185, y1-4) to golden bow D-ring (106, y1-18)!
    s += f'  <line x1="185" y1="{y1-4}" x2="108" y2="{y1-18}" stroke="#DC2626" stroke-width="3.4" stroke-dasharray="6,2"/>\n'
    s += f'  <circle cx="385" cy="{y1+13}" r="4.5" fill="#FBBF24" stroke="#0F172A" stroke-width="1.2"/>\n'
    s += f'  <circle cx="595" cy="{y1+13}" r="4.5" fill="#FBBF24" stroke="#0F172A" stroke-width="1.2"/>\n'
    s += f'  <line x1="490" y1="{y1+47}" x2="490" y2="{y1+21}" stroke="#059669" stroke-width="2" marker-end="url(#arrGreen)"/>\n'
    s += f'  <text x="150" y="{y1+26}" text-anchor="middle" class="warn">Bow-Bent Ski Nose +</text>\n'
    s += f'  <text x="150" y="{y1+39}" text-anchor="middle" class="lbl-sm">6 mm Dyneema Sling</text>\n'
    s += f'  <text x="530" y="{y1+64}" text-anchor="middle" class="ok">Upward Lift Compresses Into Contoured Hard Deck • 250 mm Rails Let Pod Retract Flat!</text>\n'
    s += f'  <text x="898" y="{y1+22}" text-anchor="middle" class="dim">Transom Clamp</text>\n'
    s += f'  <text x="898" y="{y1+34}" text-anchor="middle" class="lbl-sm">(Like Outboard!)</text>\n'

    # --- SECTION 2: OPTION A — THROUGH-FABRIC SWITCHABLE MAGNETS (NAVIGATOR 300 UNIVERSAL ALT) ---
    s += '  <rect x="24" y="278" width="992" height="196" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>\n'
    s += '  <text x="42" y="302" class="sec">2. Option A (Navigator 300 / Universal Bolt-On): 4× Flush-Recessed Switchable Magnets + Transom Bridle</text>\n'
    s += '  <text x="42" y="319" class="dim">~800 kgf clamp across 2.5 mm gap (flush-recessed inside 28 mm Hard Deck) • 5-sec drop-on • Built-in breakaway fuse</text>\n'
    y2 = 396
    s += draw_hull_base(y2, open_bow=False, tru_alu_transom=True, show_deck_labels=False)
    # 4x flush-recessed rotary magnetic pucks (flush with top of Hard Deck — zero trip boxes!)
    for mx in [380, 610]:
        s += f'  <rect x="{mx-26}" y="{y2-21}" width="52" height="15" rx="2" fill="#DC2626" stroke="#7F1D1D" stroke-width="1.2"/>\n'
        s += f'  <text x="{mx}" y="{y2-10}" text-anchor="middle" style="font-size:8px;fill:#FFFFFF;font-weight:700;">Flush Mag</text>\n'
    s += f'  <rect x="335" y="{y2+4}" width="310" height="14" rx="3" fill="url(#alu)" stroke="#0F172A" stroke-width="1.4"/>\n'
    s += f'  <line x1="645" y1="{y2+11}" x2="834" y2="{y2-18}" stroke="#DC2626" stroke-width="3" stroke-dasharray="5,2"/>\n'
    s += f'  <text x="440" y="{y2+48}" text-anchor="middle" class="lbl">Rubber Grip Pads (μ ≈ 0.7) + Sealed Steel Keeper (~2.5 mm Gap)</text>\n'
    s += f'  <text x="800" y="{y2+32}" text-anchor="middle" class="warn">Transom Shear /</text>\n'
    s += f'  <text x="800" y="{y2+45}" text-anchor="middle" class="warn">Breakaway Bridle</text>\n'

    # --- SECTION 3: DISCOVERY 330 / TAKACAT LX FULL RIGID BOW-TO-TRANSOM O-FRAME ---
    s += '  <rect x="24" y="488" width="992" height="196" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>\n'
    s += '  <text x="42" y="512" class="sec">3. Option B2 (Open-Bow Secondary Ref — True Kit Discovery 330 / Takacat LX): Contoured Rigid "O-Frame"</text>\n'
    s += '  <text x="42" y="529" class="lbl-sm">Open square bow lets bow-bent 2× 50×20 mm Alu rails wrap BOTH ends rigidly (~3.5 kg, 3×–4× lower bending moment)</text>\n'
    y3 = 606
    s += draw_hull_base(y3, open_bow=True, tru_alu_transom=False)
    s += f'  <path d="M 164 {y3-34} L 146 {y3-34} L 146 {y3-10} Q 216 {y3+12} 288 {y3+13} L 846 {y3+13} L 846 {y3-12} L 825 {y3-12}" fill="none" stroke="#0284C7" stroke-width="9" stroke-linejoin="round"/>\n'
    s += f'  <circle cx="385" cy="{y3+13}" r="4.5" fill="#FBBF24" stroke="#0F172A" stroke-width="1.2"/>\n'
    s += f'  <circle cx="595" cy="{y3+13}" r="4.5" fill="#FBBF24" stroke="#0F172A" stroke-width="1.2"/>\n'
    s += f'  <text x="490" y="{y3+46}" text-anchor="middle" class="dim">Bow-Contoured Closed Rigid Loop Around Open Bow &amp; Open Transom (Splits to 1.0 m Halves)</text>\n'

    # --- SECTION 4: OPTION C (FACTORY OEM WELDED CENTERBOARD SLOT) ---
    s += '  <rect x="24" y="698" width="992" height="196" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>\n'
    s += '  <text x="42" y="722" class="sec">4. Option C (Official Factory OEM "Foil Edition"): RF-Welded Centerboard Slot in Non-Airtight Web</text>\n'
    s += '  <text x="42" y="739" class="lbl-sm">Lightest (~1.0–1.5 kg) &amp; cleanest tunnel • Zero airtight tubes touched • Tunnel ceiling sits ABOVE static waterline (no flooding!)</text>\n'
    y4 = 812
    s += f'  <rect x="80" y="{y4+30}" width="840" height="42" rx="4" fill="url(#water)"/>\n'
    s += f'  <line x1="80" y1="{y4+30}" x2="920" y2="{y4+30}" stroke="#0284C7" stroke-width="1.4" stroke-dasharray="6,3"/>\n'
    s += f'  <text x="145" y="{y4+46}" class="dim">Static Waterline (Below Web!)</text>\n'
    s += f'  <rect x="80" y="{y4-56}" width="840" height="122" rx="44" fill="#E2E8F0" fill-opacity="0.28" stroke="#94A3B8" stroke-width="1.2" stroke-dasharray="6,4"/>\n'
    s += f'  <line x1="170" y1="{y4}" x2="455" y2="{y4}" stroke="#64748B" stroke-width="4"/>\n'
    s += f'  <line x1="545" y1="{y4}" x2="830" y2="{y4}" stroke="#64748B" stroke-width="4"/>\n'
    s += f'  <path d="M 442 {y4} L 455 {y4} L 455 {y4-26} M 558 {y4} L 545 {y4} L 545 {y4-26}" fill="none" stroke="#0D9488" stroke-width="4"/>\n'
    s += f'  <rect x="175" y="{y4-20}" width="272" height="16" rx="3" fill="url(#carbon)" stroke="#0F172A" stroke-width="1.4"/>\n'
    s += f'  <rect x="553" y="{y4-20}" width="272" height="16" rx="3" fill="url(#carbon)" stroke="#0F172A" stroke-width="1.4"/>\n'
    s += f'  <rect x="447" y="{y4-26}" width="106" height="24" rx="3" fill="none" stroke="#0284C7" stroke-width="2.2"/>\n'
    s += f'  <rect x="486" y="{y4-34}" width="28" height="108" rx="4" fill="url(#carbon)" stroke="#0F172A" stroke-width="1.5"/>\n'
    s += f'  <line x1="456" y1="{y4+2}" x2="485" y2="{y4+2}" stroke="#F59E0B" stroke-width="3.5"/>\n'
    s += f'  <line x1="515" y1="{y4+2}" x2="544" y2="{y4+2}" stroke="#F59E0B" stroke-width="3.5"/>\n'
    s += f'  <text x="372" y="{y4-28}" text-anchor="end" class="dim">CNC Cassette Well (100% Load)</text>\n'
    s += f'  <line x1="378" y1="{y4-31}" x2="444" y2="{y4-18}" stroke="#0284C7" stroke-width="1.2" marker-end="url(#arrBlue)"/>\n'
    s += f'  <text x="615" y="{y4-26}" class="ok">RF-Welded PVC Collar Boot + Flush Neoprene Spray Gasket</text>\n'
    s += f'  <line x1="610" y1="{y4-29}" x2="548" y2="{y4-12}" stroke="#059669" stroke-width="1.2" marker-end="url(#arrGreen)"/>\n'
    s += f'  <text x="615" y="{y4+18}" class="lbl-sm">Snap-in HDPE blanking plug seals slot smoothly when sailing without foil</text>\n'

    s += "</svg>\n"
    (OUT_DIR / "03-spine-floor-coupling-options.svg").write_text(s)


# -------------------------------------------------------------------------
# DIAGRAM 4: Single Inverted-T Mast Grounding Collision vs. 4-Bar Parallelogram
# -------------------------------------------------------------------------
def gen_04_grounding_kickup():
    W, H = 1040, 560
    s = svg_header(
        W, H,
        "4. Grounding Kick-Up Kinematics: Why a Single Central Mast Fails vs. 4-Bar Parallelogram",
        "Exact-Scale Sweep (0.60 m Strut, 1.30 m Pod) — Single Mast Crashes Tail Into Floor @ 40° & Plows Nose 27 cm Deeper!"
    )
    # Scale: 1 cm = 2.6 px -> 60 cm mast = 156 px, 130 cm pod = 338 px (half = 169 px), 8 cm thick = 20.8 px
    sc = 2.5

    def pod_poly_single(ox, oy, deg):
        # Pod centered at (0, -60 cm) rotated counter-clockwise by deg (aft = +x, up = +y in math coords)
        L = 60.0
        half_l, half_t = 65.0, 4.0
        th = math.radians(deg)
        c, sn = math.cos(th), math.sin(th)
        corners = [(-half_l, -L - half_t), (half_l, -L - half_t), (half_l, -L + half_t), (-half_l, -L + half_t)]
        pts = []
        for x0, y0 in corners:
            x = x0 * c - y0 * sn
            y = x0 * sn + y0 * c
            pts.append((ox + x * sc, oy - y * sc))
        # Mast endpoints
        mx = 0 * c - (-L) * sn
        my = 0 * sn + (-L) * c
        return pts, (ox + mx * sc, oy - my * sc)

    # --- LEFT PANEL: SINGLE CENTRAL MAST (BROKEN!) ---
    s += '  <rect x="24" y="68" width="484" height="468" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>\n'
    s += '  <text x="42" y="92" class="warn">A. AVOID: Single Central "Inverted-T" Mast Kick-Up</text>\n'
    s += '  <text x="42" y="109" class="lbl-sm">At just 40° aft kick-up, tail smashes PVC ceiling (-1 cm) &amp; nose plows to -91 cm!</text>\n'
    ox1, oy1 = 230, 175
    # Tunnel ceiling (y=0) & original seabed line (-64 cm) & plow depth (-91 cm)
    s += f'  <rect x="38" y="{oy1-14}" width="456" height="14" rx="2" fill="#64748B"/>\n'
    s += f'  <text x="50" y="{oy1-3}" class="lbl-w">Tunnel Ceiling / PVC Web (y = 0 cm)</text>\n'
    s += f'  <line x1="38" y1="{oy1+64*sc:.1f}" x2="494" y2="{oy1+64*sc:.1f}" stroke="#94A3B8" stroke-width="1.2" stroke-dasharray="5,3"/>\n'
    s += f'  <text x="488" y="{oy1+64*sc-5:.1f}" text-anchor="end" class="lbl-sm">Deployed Bottom (-64 cm)</text>\n'
    s += f'  <line x1="38" y1="{oy1+91*sc:.1f}" x2="494" y2="{oy1+91*sc:.1f}" stroke="#DC2626" stroke-width="1.4" stroke-dasharray="5,3"/>\n'
    s += f'  <text x="488" y="{oy1+91*sc-5:.1f}" text-anchor="end" class="warn">Nose Plows 27 cm Deeper (-91 cm!)</text>\n'

    # 0 deg ghost
    pts0, m0 = pod_poly_single(ox1, oy1, 0)
    s += f'  <line x1="{ox1}" y1="{oy1}" x2="{m0[0]:.1f}" y2="{m0[1]:.1f}" stroke="#94A3B8" stroke-width="8" stroke-linecap="round"/>\n'
    s += f'  <polygon points="{pts_to_str(pts0)}" fill="#CBD5E1" fill-opacity="0.55" stroke="#64748B" stroke-width="1.2" stroke-dasharray="4,2"/>\n'
    # 40 deg COLLISION state!
    pts40, m40 = pod_poly_single(ox1, oy1, 40)
    s += f'  <line x1="{ox1}" y1="{oy1}" x2="{m40[0]:.1f}" y2="{m40[1]:.1f}" stroke="#DC2626" stroke-width="9" stroke-linecap="round"/>\n'
    s += f'  <polygon points="{pts_to_str(pts40)}" fill="#FEE2E2" stroke="#DC2626" stroke-width="2.2"/>\n'
    s += f'  <circle cx="{ox1}" cy="{oy1}" r="5.5" fill="#FBBF24" stroke="#0F172A" stroke-width="1.5"/>\n'
    # Crash burst at tailcone top (pts40[2])
    cx_hit, cy_hit = pts40[2]
    s += f'  <circle cx="{cx_hit:.1f}" cy="{cy_hit:.1f}" r="14" fill="#DC2626" fill-opacity="0.22" stroke="#DC2626" stroke-width="2"/>\n'
    s += f'  <text x="{cx_hit+4:.1f}" y="{cy_hit+30:.1f}" text-anchor="middle" class="warn">FLOOR CRASH @ 40°!</text>\n'
    # Nose plow callout (pts40[0])
    nx_hit, ny_hit = pts40[0]
    s += f'  <circle cx="{nx_hit:.1f}" cy="{ny_hit:.1f}" r="6" fill="#DC2626"/>\n'
    s += f'  <text x="{nx_hit+40:.1f}" y="{ny_hit+26:.1f}" text-anchor="middle" class="warn">Nose Dives to -91 cm!</text>\n'
    # Depth arrow -64 -> -91
    s += dim_line(72, oy1 + 64 * sc, 72, oy1 + 91 * sc, "-27 cm!", dx=32, dy=4, cls="warn", marker="arrRed", stroke="#DC2626")
    s += '  <text x="42" y="498" class="lbl">Verdict: Single central mast works ONLY for vertical daggerboard slide</text>\n'
    s += '  <text x="42" y="514" class="lbl-sm">(Option C OEM slot) or short dry-floor foils — NEVER pivot a 1.3 m pod!</text>\n'

    # --- RIGHT PANEL: 4-BAR PARALLELOGRAM (DEEP-SUBMERGED STOL / SWITCHBLADE POD) ---
    s += '  <rect x="532" y="68" width="484" height="468" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>\n'
    s += '  <text x="550" y="92" class="ok">B. MANDATORY: 4-Bar Parallelogram Struts (4× Blades)</text>\n'
    s += '  <text x="550" y="109" class="lbl-sm">Pod &amp; STOL flaperons stay 100% HORIZONTAL (0°→85°) — zero upper wing needed!</text>\n'
    ox2, oy2 = 678, 175
    # Contoured bow-bent under-hull plate at y = 0 cm
    s += f'  <path d="M 552 {oy2-26} Q 576 {oy2-12} 608 {oy2-12} L 1002 {oy2-12} L 1002 {oy2} L 608 {oy2} Q 572 {oy2} 546 {oy2-14} Z" fill="#0284C7"/>\n'
    s += f'  <text x="795" y="{oy2-3}" text-anchor="middle" class="lbl-w">Bow-Contoured Under-Hull Rails (y = 0 cm)</text>\n'
    s += f'  <line x1="546" y1="{oy2+64*sc:.1f}" x2="1002" y2="{oy2+64*sc:.1f}" stroke="#94A3B8" stroke-width="1.2" stroke-dasharray="5,3"/>\n'
    s += f'  <text x="996" y="{oy2+64*sc-5:.1f}" text-anchor="end" class="lbl-sm">Deployed (-64 cm)</text>\n'

    # Draw 0 deg (ghost), 40 deg (mid), 85 deg (flat tucked!)
    L_cm = 60.0
    p_front, p_rear = -36.0, 36.0
    for deg, fill_c, strk_c, dash, op in [
        (0, "#CBD5E1", "#64748B", "4,2", "0.50"),
        (40, "#BAE6FD", "#0284C7", "none", "0.75"),
        (85, "#A7F3D0", "#059669", "none", "0.95"),
    ]:
        th = math.radians(deg)
        dx = L_cm * math.sin(th)
        dy = L_cm * math.cos(th)
        for p_off in (p_front, p_rear):
            x1, y1 = ox2 + p_off * sc, oy2
            x2, y2 = ox2 + (p_off + dx) * sc, oy2 + dy * sc
            s += f'  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{strk_c}" stroke-width="5.2" stroke-dasharray="{dash}" stroke-linecap="round"/>\n'
        px = ox2 + (dx - 60.0) * sc
        py = oy2 + (dy - 4.0) * sc
        s += f'  <rect x="{px:.1f}" y="{py:.1f}" width="{120*sc:.1f}" height="{8*sc:.1f}" rx="8" fill="{fill_c}" fill-opacity="{op}" stroke="{strk_c}" stroke-width="1.8" stroke-dasharray="{dash}"/>\n'
        if deg in (0, 85):
            for p_off in (p_front, p_rear):
                s += f'  <circle cx="{ox2+(p_off+dx)*sc:.1f}" cy="{oy2+dy*sc:.1f}" r="3.6" fill="#FBBF24" stroke="#0F172A" stroke-width="1.1"/>\n'
        if deg == 85:
            s += f'  <text x="{px+120*sc/2:.1f}" y="{py+14:.1f}" text-anchor="middle" class="ok">85°: 100% FLAT &amp; TUCKED!</text>\n'
        elif deg == 40:
            s += f'  <text x="{px+120*sc/2:.1f}" y="{py+14:.1f}" text-anchor="middle" class="dim">40° Kick-Up: Flat (-50 cm)</text>\n'

    for p_off in (p_front, p_rear):
        s += f'  <circle cx="{ox2+p_off*sc:.1f}" cy="{oy2}" r="4.8" fill="#FBBF24" stroke="#0F172A" stroke-width="1.3"/>\n'

    s += '  <text x="550" y="498" class="ok">Verdict: Simple 4-pin/side parallelogram kicks pod flat UP &amp; AFT over reefs</text>\n'
    s += '  <text x="550" y="514" class="lbl-sm">with ZERO floor collision, ZERO nose plowing, and ZERO external pushrod binding!</text>\n'

    s += "</svg>\n"
    (OUT_DIR / "04-grounding-kickup-geometry.svg").write_text(s)


# -------------------------------------------------------------------------
# DIAGRAM 5: Folded Stack-Up Inside Ø460 mm Catamaran Tunnel (Front & Side)
# -------------------------------------------------------------------------
def gen_05_strut_stackup():
    W, H = 1040, 560
    s = svg_header(
        W, H,
        "5. Strut Architecture & Folded Beaching Stack-Up Inside a Ø460 mm Catamaran Tunnel",
        "Front View of 4× Side-Straddling Blades (Box-Portal Rigidity) + Exact Millimeter Sand Clearance (230 mm Tunnel Height)"
    )

    # --- LEFT PANEL: FRONT VIEW (DEPLOYED) ---
    s += '  <rect x="24" y="68" width="484" height="468" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>\n'
    s += '  <text x="42" y="92" class="sec">A. Front View — 4× Side-Straddling Blades (Deployed)</text>\n'
    s += '  <text x="42" y="109" class="ok">Direct rail-to-pod mount • Upper Wing box-portal tie (&lt;3 mm roll flex!)</text>\n'
    cx = 266
    # Scale: 1 mm = 0.24 px -> Ø460 tube = 110 px dia (r=55 px); tunnel width ~750 mm = 180 px; 250 mm rails = 60 px; 220 mm pod = 53 px
    # Waterline while foiling!
    y_web = 205
    y_tube_bot = y_web + 55  # 230 mm = 55.2 px
    y_water = y_tube_bot + 42  # 6-8" air gap below tubes!
    y_upper = y_water - 26     # Upper Step-Out Wing flying IN AIR >9 kn!
    y_pod = y_water + 98       # Lower pod 400 mm deep!
    s += f'  <rect x="34" y="{y_water}" width="464" height="{524-y_water}" rx="6" fill="url(#water)"/>\n'
    s += f'  <line x1="34" y1="{y_water}" x2="498" y2="{y_water}" stroke="#0284C7" stroke-width="1.8" stroke-dasharray="6,3"/>\n'
    s += f'  <text x="488" y="{y_water-6}" text-anchor="end" class="dim">Cruise Waterline (6"–8" Clear!)</text>\n'
    # Left & Right Ø460 mm inflatable pontoons
    s += f'  <circle cx="{cx-145}" cy="{y_web}" r="55" fill="url(#tubeGrad)" stroke="#475569" stroke-width="1.8"/>\n'
    s += f'  <circle cx="{cx+145}" cy="{y_web}" r="55" fill="url(#tubeGrad)" stroke="#475569" stroke-width="1.8"/>\n'
    s += f'  <text x="{cx-145}" y="{y_web+4}" text-anchor="middle" class="lbl-sm">Ø460 mm</text>\n'
    s += f'  <text x="{cx+145}" y="{y_web+4}" text-anchor="middle" class="lbl-sm">Ø460 mm</text>\n'
    # Continuous 1.2 mm PVC tunnel web + Drop-In Spine Floor
    s += f'  <line x1="{cx-90}" y1="{y_web}" x2="{cx+90}" y2="{y_web}" stroke="#64748B" stroke-width="3.5"/>\n'
    s += f'  <rect x="{cx-96}" y="{y_web-12}" width="192" height="10" rx="2" fill="url(#carbon)" stroke="#0F172A" stroke-width="1.2"/>\n'
    s += f'  <text x="{cx}" y="{y_web-18}" text-anchor="middle" class="lbl">100% Flush Contoured Hard Deck (0 Boxes!)</text>\n'
    # Twin Hybrid C-Frame rails (250 mm apart = 64 px)
    for side in (-1, 1):
        rx = cx + side * 32
        s += f'  <rect x="{rx-6}" y="{y_web+3}" width="12" height="7" rx="1.5" fill="url(#alu)" stroke="#334155" stroke-width="1.2"/>\n'
        # Vertical 60x9 mm carbon blade descending straight to pod side!
        s += f'  <rect x="{rx-3}" y="{y_web+10}" width="6" height="{y_pod-y_web-10}" fill="url(#carbon)" stroke="#0F172A" stroke-width="1"/>\n'
    # Slim above-water box-portal cross-brace ONLY (ZERO surface-piercing wing in wave zone!)
    s += f'  <rect x="{cx-32}" y="{y_upper-3}" width="64" height="5" rx="2" fill="url(#alu)" stroke="#334155" stroke-width="1"/>\n'
    s += f'  <text x="{cx+145}" y="{y_upper-4}" text-anchor="end" class="ok">Clean Wave Zone! (Only 9 mm blades)</text>\n'
    # Lower 220x80 mm Flying-Keel Pod + 1,000 cm2 Main + 2x250 cm2 Split STOL Flaperons (400 mm deep!)
    s += f'  <rect x="{cx-145}" y="{y_pod-3}" width="290" height="7" rx="3.5" fill="url(#wingBlue)" stroke="#0369A1" stroke-width="1.3"/>\n'
    s += f'  <rect x="{cx-130}" y="{y_pod+6}" width="92" height="5" rx="2.5" fill="url(#wingTeal)" stroke="#0F766E" stroke-width="1.1"/>\n'
    s += f'  <rect x="{cx+38}" y="{y_pod+6}" width="92" height="5" rx="2.5" fill="url(#wingTeal)" stroke="#0F766E" stroke-width="1.1"/>\n'
    s += f'  <rect x="{cx-30}" y="{y_pod-12}" width="60" height="24" rx="10" fill="url(#carbon)" stroke="#0F172A" stroke-width="1.6"/>\n'
    s += f'  <text x="{cx}" y="{y_pod+4}" text-anchor="middle" class="lbl-w">26 L</text>\n'
    s += f'  <text x="{cx}" y="{y_pod+32}" text-anchor="middle" class="lbl">220×80 mm Pod (Internal Servos) + Split STOL Flaperons</text>\n'
    s += dim_line(cx - 32, y_web + 24, cx + 32, y_web + 24, "250 mm", dy=-6)
    s += dim_line(cx - 190, y_water, cx - 190, y_pod, "400 mm", dx=24, dy=4)

    # --- RIGHT PANEL: SIDE-BY-SIDE FOLDED STACK-UP COMPARISON ---
    s += '  <rect x="532" y="68" width="484" height="468" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>\n'
    s += '  <text x="550" y="92" class="sec">B. Folded Stack-Up Comparison (85° Aft Fold vs. Flat Sand)</text>\n'
    s += '  <text x="550" y="109" class="lbl-sm">Navigator 300 (600 mm tunnel): ~230 mm web to Ø460 tube bottom</text>\n'

    # Scale for right panel: 1 mm = 0.45 px -> 230 mm = 103.5 px per sub-row!
    rsc = 0.44
    rows = [
        ("Primary A: 4× Side-Straddling Blades (60×9 mm)", 135, 90, "#059669", "ok", "90 mm deep → +140 mm (5.5\") CLEAR ABOVE SAND!", "Blades flank pod sides"),
        ("Primary B: 2× Recessed Center Struts (100×18 mm)", 280, 135, "#0284C7", "dim", "135 mm deep → +95 mm (3.7\") clear above sand", "55 mm top-slot overlap"),
        ("Avoid — Naive Stack: 120 mm Strut ON TOP of Pod", 425, 210, "#DC2626", "warn", "210 mm deep → ONLY +20 mm (0.8\") — hits pebbles!", "120+10+80 mm stack"),
    ]
    for title_r, y_top, depth_mm, col, tcls, badge, note in rows:
        s += f'  <text x="550" y="{y_top-4}" class="lbl">{title_r}</text>\n'
        # Tunnel ceiling (0 mm) & beach line (-230 mm)
        y_sand = y_top + 230 * rsc
        s += f'  <rect x="550" y="{y_top}" width="446" height="6" fill="#64748B"/>\n'
        s += f'  <rect x="550" y="{y_sand:.1f}" width="446" height="10" fill="#FDE68A" stroke="#D97706" stroke-width="1"/>\n'
        s += f'  <text x="990" y="{y_sand+8:.1f}" text-anchor="end" style="font-size:8.5px;fill:#92400E;font-weight:700;">Flat Beach / Bottom of Ø460 Tubes (-230 mm)</text>\n'
        # Draw folded pod & strut geometry
        pod_h = 80 * rsc
        pod_bot_y = y_top + depth_mm * rsc
        pod_top_y = pod_bot_y - pod_h
        if depth_mm == 90:
            # Side-straddling: 60 mm blade flanks 80 mm pod cleanly (ZERO upper wing in tunnel!)
            s += f'  <rect x="605" y="{pod_top_y:.1f}" width="210" height="{pod_h:.1f}" rx="8" fill="url(#carbon)" stroke="#0F172A" stroke-width="1.4"/>\n'
            s += f'  <rect x="585" y="{y_top+8:.1f}" width="185" height="{60*rsc:.1f}" rx="4" fill="url(#wingBlue)" fill-opacity="0.72" stroke="#0369A1" stroke-width="1.3"/>\n'
            s += f'  <text x="710" y="{pod_top_y+pod_h/2+4:.1f}" text-anchor="middle" class="lbl-w">80 mm Pod (60 mm Blades Beside)</text>\n'
        elif depth_mm == 135:
            # Recessed 55 mm into pod top slot
            s += f'  <rect x="605" y="{pod_top_y:.1f}" width="210" height="{pod_h:.1f}" rx="8" fill="url(#carbon)" stroke="#0F172A" stroke-width="1.4"/>\n'
            s += f'  <rect x="585" y="{y_top+8:.1f}" width="190" height="{100*rsc:.1f}" rx="4" fill="url(#wingBlue)" fill-opacity="0.62" stroke="#0369A1" stroke-width="1.3" stroke-dasharray="4,2"/>\n'
            s += f'  <text x="710" y="{pod_bot_y-8:.1f}" text-anchor="middle" class="lbl-w">80 mm Pod (55 mm Top Recess)</text>\n'
        else:
            # Naive stack: 120 mm strut sitting completely on top of 80 mm pod!
            s += f'  <rect x="585" y="{y_top+8:.1f}" width="190" height="{120*rsc:.1f}" rx="4" fill="#FCA5A5" stroke="#DC2626" stroke-width="1.3"/>\n'
            s += f'  <text x="680" y="{y_top+8+60*rsc+3:.1f}" text-anchor="middle" class="warn">120 mm Strut Chord Vertical</text>\n'
            s += f'  <rect x="605" y="{pod_top_y:.1f}" width="210" height="{pod_h:.1f}" rx="8" fill="url(#carbon)" stroke="#DC2626" stroke-width="1.6"/>\n'
            s += f'  <text x="710" y="{pod_top_y+pod_h/2+4:.1f}" text-anchor="middle" class="lbl-w">80 mm Pod Below Strut</text>\n'
        # Clearance dimension arrow on right (with label well clear of sand line!)
        lbl_dy = -6 if depth_mm == 210 else 4
        s += dim_line(855, pod_bot_y, 855, y_sand, f"+{230-depth_mm} mm", dx=34, dy=lbl_dy, cls=tcls, marker="arrGreen" if depth_mm == 90 else ("arrBlue" if depth_mm == 135 else "arrRed"), stroke=col)
        s += f'  <text x="556" y="{y_sand+23:.1f}" class="{tcls}">{badge}</text>\n'
        s += f'  <text x="992" y="{y_top+24:.1f}" text-anchor="end" class="lbl-sm">{note}</text>\n'

    s += "</svg>\n"
    (OUT_DIR / "05-strut-folded-stackup.svg").write_text(s)


# -------------------------------------------------------------------------
# DIAGRAM 9: Internal Longitudinal Cutaway of the 26 L Flying-Keel Pod
# -------------------------------------------------------------------------
def gen_09_cartridge_cutaway():
    W, H = 1040, 480
    s = svg_header(
        W, H,
        "9. Flying-Keel Pod Internal Cutaway (1,300 x 220 x 80 mm, 26 L Buoyancy)",
        "Swappable 2× 14 kg Potted IP68 Cartridges • Passive Seawater-Cooled 75100 VESCs • Kevlar Nose & Leak Safety"
    )
    s += '  <rect x="24" y="68" width="992" height="388" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>\n'
    s += '  <rect x="34" y="106" width="972" height="270" rx="6" fill="url(#water)"/>\n'

    # Fuselage outer shell (X: 90..930 = 840 px for 1300 mm -> 0.646 px/mm; Y center = 246, height = 112 px visual)
    cy = 248
    # Outer carbon fuselage profile
    s += (
        f'  <path d="M 88 {cy} Q 100 {cy-56} 200 {cy-56} L 735 {cy-56} Q 850 {cy-54} 920 {cy-18} '
        f'L 920 {cy+18} Q 850 {cy+54} 735 {cy+56} L 200 {cy+56} Q 100 {cy+56} 88 {cy} Z" '
        f'fill="url(#carbon)" stroke="#0F172A" stroke-width="2.2"/>\n'
    )
    # 20 mm Kevlar/elastomer crush nose cone (X: 88..178)
    s += (
        f'  <path d="M 88 {cy} Q 100 {cy-54} 178 {cy-54} L 178 {cy+54} Q 100 {cy+54} 88 {cy} Z" '
        f'fill="url(#kevlar)" stroke="#92400E" stroke-width="1.5"/>\n'
    )
    # 5 mm G10 structural impact bulkhead (X: 178..190)
    s += f'  <rect x="178" y="{cy-52}" width="11" height="104" fill="#10B981" stroke="#065F46" stroke-width="1.2"/>\n'

    # Internal dry IP68 bay cavity (X: 194..748)
    s += f'  <rect x="194" y="{cy-46}" width="554" height="92" rx="4" fill="#F1F5F9" stroke="#334155" stroke-width="1.2"/>\n'
    # Cartridge #1 (Front, 2.7 kWh, 14 kg potted IP68) & Cartridge #2 (Aft, 2.7 kWh or Foam Dummy Plug!)
    s += f'  <rect x="204" y="{cy-38}" width="185" height="62" rx="6" fill="url(#wingBlue)" stroke="#0369A1" stroke-width="1.6"/>\n'
    s += f'  <text x="296" y="{cy-11}" text-anchor="middle" class="lbl-w">IP68 Cartridge #1</text>\n'
    s += f'  <text x="296" y="{cy+4}" text-anchor="middle" class="lbl-w">2.7 kWh • 14 kg</text>\n'
    s += f'  <rect x="404" y="{cy-38}" width="185" height="62" rx="6" fill="url(#wingTeal)" stroke="#0F766E" stroke-width="1.6"/>\n'
    s += f'  <text x="496" y="{cy-11}" text-anchor="middle" class="lbl-w">IP68 Cartridge #2</text>\n'
    s += f'  <text x="496" y="{cy+4}" text-anchor="middle" class="lbl-w">(or Foam Plug Solo)</text>\n'
    # Blind-mate waterproof connectors between cartridges & VESC bay
    s += f'  <rect x="389" y="{cy-14}" width="15" height="16" rx="2" fill="#FBBF24" stroke="#0F172A" stroke-width="1"/>\n'
    s += f'  <rect x="589" y="{cy-14}" width="15" height="16" rx="2" fill="#FBBF24" stroke="#0F172A" stroke-width="1"/>\n'

    # 2x Internal IP67 Brushless Flaperon Servos + ESP32/BNO085 IMU inside pod bay (ZERO boxes above top deck!)
    s += f'  <rect x="608" y="{cy-38}" width="112" height="34" rx="4" fill="#0F766E" stroke="#134E4A" stroke-width="1.3"/>\n'
    s += f'  <text x="664" y="{cy-22}" text-anchor="middle" style="font-size:8.8px;fill:#FFFFFF;font-weight:700;">2× IP67 Servos + IMU</text>\n'
    s += f'  <text x="664" y="{cy-10}" text-anchor="middle" style="font-size:8px;fill:#CCFBF1;font-weight:700;">Ø8 mm Sealed Shafts</text>\n'
    # 2x Flipsky 75100 VESCs bolted directly to bottom aluminum/carbon seawater-cooled skin!
    s += f'  <rect x="608" y="{cy+6}" width="112" height="36" rx="4" fill="#334155" stroke="#0F172A" stroke-width="1.4"/>\n'
    s += f'  <text x="664" y="{cy+22}" text-anchor="middle" class="lbl-w">2× 75100 VESC</text>\n'
    s += f'  <text x="664" y="{cy+35}" text-anchor="middle" style="font-size:8.5px;fill:#BAE6FD;font-weight:700;">Bottom-Skin Cooled</text>\n'
    # Thermal conduction arrows into seawater
    for hx in [628, 664, 700]:
        s += f'  <line x1="{hx}" y1="{cy+44}" x2="{hx}" y2="{cy+72}" stroke="#DC2626" stroke-width="1.8" marker-end="url(#arrRed)"/>\n'
    # Optical leak sensor & 0.5 bar pressure relief burst valve
    s += f'  <circle cx="732" cy="{cy-26}" r="6.5" fill="#EF4444" stroke="#7F1D1D" stroke-width="1.2"/>\n'
    s += f'  <rect x="688" y="{cy-52}" width="24" height="10" rx="2" fill="#F59E0B" stroke="#78350F" stroke-width="1"/>\n'
    # CNC Double-O-Ring Rear Service Flange Door (X: 742..762)
    s += f'  <rect x="744" y="{cy-50}" width="18" height="100" rx="3" fill="url(#alu)" stroke="#0F172A" stroke-width="1.6"/>\n'
    for oy in [cy - 36, cy - 26, cy + 26, cy + 36]:
        s += f'  <circle cx="753" cy="{oy}" r="3" fill="#0F172A"/>\n'
    # Slide-out cartridge direction arrow
    s += f'  <line x1="768" y1="{cy}" x2="825" y2="{cy}" stroke="#059669" stroke-width="2.2" stroke-dasharray="4,2" marker-end="url(#arrGreen)"/>\n'

    # Twin Flipsky 65161 Tailcone Motor Pods
    s += f'  <rect x="850" y="{cy-16}" width="72" height="32" rx="10" fill="#1E293B" stroke="#0F172A" stroke-width="1.5"/>\n'
    s += f'  <line x1="928" y1="{cy-38}" x2="928" y2="{cy+38}" stroke="#0284C7" stroke-width="4" stroke-linecap="round"/>\n'
    s += f'  <text x="886" y="{cy+4}" text-anchor="middle" class="lbl-w">65161</text>\n'

    # Dry deck charging umbilical + 4-wire signal rising up strut channel (X: 595)
    s += f'  <line x1="650" y1="{cy-46}" x2="650" y2="112" stroke="#0284C7" stroke-width="3" stroke-dasharray="6,3" marker-end="url(#arrBlue)"/>\n'

    # Clean Callouts (Top & Bottom — zero overlaps!)
    s += f'  <text x="120" y="132" text-anchor="middle" class="lbl">20 mm Kevlar</text>\n'
    s += f'  <text x="120" y="145" text-anchor="middle" class="lbl-sm">Crush Nose</text>\n'
    s += f'  <line x1="120" y1="150" x2="125" y2="{cy-35}" stroke="#475569" stroke-width="1.1" marker-end="url(#arrDark)"/>\n'

    s += f'  <text x="235" y="132" text-anchor="middle" class="ok">5 mm G10 Bulkhead</text>\n'
    s += f'  <line x1="215" y1="138" x2="186" y2="{cy-52}" stroke="#059669" stroke-width="1.1" marker-end="url(#arrGreen)"/>\n'

    s += f'  <text x="415" y="132" text-anchor="middle" class="lbl">Blind-Mate IP68 Connectors</text>\n'
    s += f'  <text x="415" y="145" text-anchor="middle" class="lbl-sm">Carry-ashore 14 kg packs (zero high-amp strut cables!)</text>\n'

    s += f'  <text x="720" y="132" class="dim">Dry Deck Charge Umbilical + 4-Wire Alarm</text>\n'
    s += f'  <text x="720" y="145" class="lbl-sm">Routed up strut — charge without opening seal</text>\n'

    s += f'  <text x="785" y="176" class="warn">0.5 bar Relief Valve &amp; Leak Sensor</text>\n'
    s += f'  <line x1="780" y1="173" x2="714" y2="{cy-48}" stroke="#DC2626" stroke-width="1.1" marker-end="url(#arrRed)"/>\n'

    s += f'  <text x="585" y="344" text-anchor="middle" class="warn">Passive Seawater Cooling (&lt;45°C MOSFETs)</text>\n'
    s += f'  <text x="895" y="330" text-anchor="middle" class="ok">CNC Double-O-Ring Door</text>\n'
    s += f'  <text x="895" y="344" text-anchor="middle" class="lbl-sm">Slide cartridges out aft</text>\n'
    s += f'  <line x1="825" y1="322" x2="758" y2="{cy+44}" stroke="#059669" stroke-width="1.1" marker-end="url(#arrGreen)"/>\n'

    s += '  <text x="42" y="408" class="ok">Free Archimedes Lift (~26.6 kg Buoyancy): Cancels ~90% of 30 kg battery weight underwater with ZERO induced drag!</text>\n'
    s += '  <text x="42" y="428" class="lbl-sm">Serviceability: Run 1 cartridge + closed-cell foam dummy plug (~15 nm solo) or 2 cartridges (~31 nm 2-up); replace single pack if worn.</text>\n'
    s += '  <text x="42" y="446" class="lbl-sm">Impact Protection: 20 mm Kevlar/elastomer cone + 5 mm G10 bulkhead isolate cells from 15 kn debris/shoal strikes.</text>\n'

    s += "</svg>\n"
    (OUT_DIR / "09-swappable-cartridge-cutaway.svg").write_text(s)


# -------------------------------------------------------------------------
# DIAGRAM 10: 4-Panel Integrated Battery-Hull Architecture Comparison (+ Magnetic Clamp)
# -------------------------------------------------------------------------
def gen_10_alt_architectures():
    W, H = 1040, 620
    s = svg_header(
        W, H,
        "10. Integrated Battery-Hull Architectures & Through-Fabric Magnetic Clamp (Front Cross-Sections)",
        "Visual Comparison of All Four FoilSkiff Hull Foundations on a True Kit Navigator 300 (155 cm Beam, 60 cm Tunnel, Ø460 mm Tubes)"
    )

    panels = [
        (24, 68, "1. PRIMARY: Split STOL Flaperon Flying-Keel Pod", "7.2 kn TO • 29.8 nm @ 15.5 kn • Servos inside pod (0 wave slam)", "primary"),
        (532, 68, "2. ALT A: Dry 60 mm Rigid Battery-Floor", "9.5 kn TO • 31.8 nm @ 15.5 kn • Rocky-beach flip-up pick", "dry"),
        (24, 344, "3. ALT B: Twin Torpedo SWATH Floats", "2× Ø180 mm × 1.8 m tubes • Dual IP68 seals required", "swath"),
        (532, 344, "4. ALT C: Central BP100 10 kW Jet Board", "3\" draft • Detachable jet-surfboard • Cannot foil (7.4 nm)", "jet"),
    ]

    for px, py, ptitle, psub, mode in panels:
        s += f'  <rect x="{px}" y="{py}" width="484" height="260" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>\n'
        s += f'  <text x="{px+16}" y="{py+24}" class="sec">{html.escape(ptitle)}</text>\n'
        s += f'  <text x="{px+16}" y="{py+40}" class="{"ok" if mode=="primary" else "lbl-sm"}">{html.escape(psub)}</text>\n'
        cx = px + 242
        y_web = py + 106
        y_wat = py + 150 if mode in ("primary", "dry") else py + 132
        s += f'  <rect x="{px+12}" y="{y_wat}" width="460" height="{py+250-y_wat}" rx="4" fill="url(#water)"/>\n'
        s += f'  <line x1="{px+12}" y1="{y_wat}" x2="{px+472}" y2="{y_wat}" stroke="#0284C7" stroke-width="1.3" stroke-dasharray="5,3"/>\n'
        # Twin Ø460 mm inflatable pontoons
        s += f'  <circle cx="{cx-125}" cy="{y_web}" r="34" fill="url(#tubeGrad)" stroke="#475569" stroke-width="1.5"/>\n'
        s += f'  <circle cx="{cx+125}" cy="{y_web}" r="34" fill="url(#tubeGrad)" stroke="#475569" stroke-width="1.5"/>\n'
        s += f'  <line x1="{cx-91}" y1="{y_web}" x2="{cx+91}" y2="{y_web}" stroke="#64748B" stroke-width="3"/>\n'

        if mode == "primary":
            # Thin 28 mm Contoured Hard Deck + Hybrid C-Frame + 4x slim blades + Deep Split STOL Pod (ZERO surface wing!)
            s += f'  <rect x="{cx-95}" y="{y_web-9}" width="190" height="8" rx="2" fill="url(#carbon)"/>\n'
            for sd in (-1, 1):
                s += f'  <rect x="{cx+sd*24-3}" y="{y_web+2}" width="6" height="96" fill="url(#carbon)"/>\n'
            s += f'  <rect x="{cx-108}" y="{y_web+92}" width="216" height="6" rx="3" fill="url(#wingBlue)"/>\n'
            s += f'  <rect x="{cx-100}" y="{y_web+100}" width="70" height="4.5" rx="2" fill="url(#wingTeal)"/>\n'
            s += f'  <rect x="{cx+30}" y="{y_web+100}" width="70" height="4.5" rx="2" fill="url(#wingTeal)"/>\n'
            s += f'  <rect x="{cx-26}" y="{y_web+86}" width="52" height="20" rx="8" fill="url(#carbon)" stroke="#FBBF24" stroke-width="1.4"/>\n'
            s += f'  <text x="{cx}" y="{y_web+99}" text-anchor="middle" style="font-size:8.5px;fill:#FBBF24;font-weight:700;">5.4 kWh</text>\n'
            s += f'  <text x="{px+20}" y="{py+236}" class="ok">100% Flush Deck (0 Boxes) • Deep 400 mm Foil • Active Wave Control</text>\n'
        elif mode == "dry":
            # Thick 60 mm Dry Composite Battery-Floor housing flat 36.7 mm EVE LF105 cells ABOVE waterline!
            s += f'  <rect x="{cx-96}" y="{y_web-20}" width="192" height="18" rx="3" fill="url(#carbon)" stroke="#FBBF24" stroke-width="1.4"/>\n'
            s += f'  <text x="{cx}" y="{y_web-8}" text-anchor="middle" style="font-size:8.5px;fill:#FBBF24;font-weight:700;">Dry 5.4 kWh EVE LF105 (37 mm)</text>\n'
            # Lightweight 2-sec flip-up thin foil struts & 1,600 cm2 wing
            s += f'  <rect x="{cx-4}" y="{y_web+2}" width="8" height="96" fill="url(#carbon)"/>\n'
            s += f'  <rect x="{cx-125}" y="{y_web+94}" width="250" height="6" rx="3" fill="url(#wingBlue)"/>\n'
            s += f'  <text x="{px+20}" y="{py+236}" class="dim">Zero submerged lithium • 2-sec hand flip-up • Best >14 kn speed</text>\n'
        elif mode == "swath":
            # Twin Ø180 mm submerged torpedo battery floats under each pontoon + expanding wings
            s += f'  <rect x="{cx-95}" y="{y_web-8}" width="190" height="7" rx="2" fill="url(#alu)"/>\n'
            for sd in (-1, 1):
                tx = cx + sd * 105
                s += f'  <rect x="{tx-4}" y="{y_web+26}" width="8" height="62" fill="url(#carbon)"/>\n'
                s += f'  <circle cx="{tx}" cy="{y_web+92}" r="18" fill="url(#carbon)" stroke="#FBBF24" stroke-width="1.4"/>\n'
                s += f'  <text x="{tx}" y="{y_web+95}" text-anchor="middle" style="font-size:8px;fill:#FBBF24;font-weight:700;">2.7k</text>\n'
            s += f'  <rect x="{cx-145}" y="{y_web+90}" width="290" height="5" rx="2.5" fill="url(#wingBlue)"/>\n'
            s += f'  <text x="{px+20}" y="{py+236}" class="lbl-sm">Mini Foiling SWATH • High roll stability • Needs dual IP68 seals</text>\n'
        else:
            # Central under-tunnel BP100 10 kW jetboard cassette (blocks tunnel, 3" draft)
            s += f'  <rect x="{cx-95}" y="{y_web-8}" width="190" height="7" rx="2" fill="url(#alu)"/>\n'
            s += f'  <rect x="{cx-68}" y="{y_web+4}" width="136" height="24" rx="8" fill="url(#carbon)" stroke="#FBBF24" stroke-width="1.4"/>\n'
            s += f'  <text x="{cx}" y="{y_web+19}" text-anchor="middle" style="font-size:8.5px;fill:#FBBF24;font-weight:700;">BP100 10 kW Jet + 24S</text>\n'
            s += f'  <text x="{px+20}" y="{py+236}" class="warn">Prop-free rocky beaching (3\" draft) • Blocks tunnel, cannot foil</text>\n'

    s += "</svg>\n"
    (OUT_DIR / "10-alt-architectures-comparison.svg").write_text(s)


# -------------------------------------------------------------------------
# DIAGRAM 12: Why We Rejected Surface-Piercing Step-Out Wings (Wave-Slam Physics)
# -------------------------------------------------------------------------
def gen_12_rejected_step_out_physics():
    W, H = 1040, 540
    s = svg_header(
        W, H,
        "12. Rejected Concept Physics: Why Surface-Piercing Step-Out Wings Fail in Chop",
        "15.5 kn (q = 32.8 kPa, 850x Air-to-Water Density Shock) — Forward & Deep-Aft Step-Out Hazards vs. Deep-Submerged STOL Flaperons"
    )

    # --- LEFT PANEL: FORWARD STEP-OUT WING (WAVE SLAM & NOSE-DIVE SUCTION) ---
    s += '  <rect x="24" y="68" width="484" height="448" rx="8" fill="#FFFFFF" stroke="#FCA5A5" stroke-width="1.5"/>\n'
    s += '  <text x="42" y="92" class="warn">A. REJECTED: Forward Surface-Piercing Step-Out Wing</text>\n'
    s += '  <text x="42" y="109" class="lbl-sm">1,400 cm² horizontal slab hovering 50–100 mm above water hits a 1 ft wave crest</text>\n'
    # Wave profile rising right into the forward step-out wing!
    s += '  <path d="M 34 325 Q 110 265 185 268 Q 255 272 330 330 Q 410 355 498 315 L 498 440 L 34 440 Z" fill="url(#water)"/>\n'
    s += '  <path d="M 34 325 Q 110 265 185 268 Q 255 272 330 330 Q 410 355 498 315" fill="none" stroke="#0284C7" stroke-width="2.2"/>\n'
    # Boat pitching slightly nose-down (-6 deg) into wave crest
    s += '  <g transform="translate(265, 220) rotate(-6)">\n'
    s += '    <rect x="-145" y="-22" width="290" height="30" rx="14" fill="url(#tubeGrad)" stroke="#475569" stroke-width="1.6"/>\n'
    s += '    <line x1="-85" y1="8" x2="-85" y2="128" stroke="#334155" stroke-width="6"/>\n'
    s += '    <line x1="65" y1="8" x2="65" y2="128" stroke="#334155" stroke-width="6"/>\n'
    s += '    <rect x="-115" y="118" width="215" height="20" rx="8" fill="url(#carbon)" stroke="#0F172A" stroke-width="1.4"/>\n'
    # Forward Step-Out Wing SLAMMING into wave crest!
    s += '    <rect x="-126" y="42" width="60" height="10" rx="4" fill="#EF4444" stroke="#7F1D1D" stroke-width="1.6"/>\n'
    s += '    <circle cx="0" cy="-6" r="5" fill="#FBBF24" stroke="#0F172A" stroke-width="1.2"/>\n'
    s += '  </g>\n'
    # Impact ring & force vectors at forward step-out wing
    s += '  <circle cx="172" cy="274" r="18" fill="#DC2626" fill-opacity="0.22" stroke="#DC2626" stroke-width="1.8" stroke-dasharray="4,2"/>\n'
    s += '  <line x1="172" y1="286" x2="172" y2="352" stroke="#DC2626" stroke-width="3" marker-end="url(#arrRed)"/>\n'
    s += '  <line x1="184" y1="274" x2="246" y2="274" stroke="#DC2626" stroke-width="2.6" marker-end="url(#arrRed)"/>\n'
    s += '  <text x="172" y="370" text-anchor="middle" class="warn">-140 kgf Suction!</text>\n'
    s += '  <text x="172" y="383" text-anchor="middle" class="lbl-sm">(if pitch -5° to -8°)</text>\n'
    s += '  <text x="315" y="268" class="warn">+103 lbf Drag Trip</text>\n'
    s += '  <text x="275" y="176" text-anchor="middle" class="lbl-sm">CoG</text>\n'
    s += '  <text x="42" y="458" class="warn">1. Nose-Down Entry (-6°): -140 kgf suction + 103 lbf brake → pitchpole!</text>\n'
    s += '  <text x="42" y="476" class="warn">2. Level Wave Slam (0°): +210 kgf (+1G) bow launch → breach &amp; crash!</text>\n'
    s += '  <text x="42" y="496" class="lbl-sm">Also requires double-deck tie-bars, 6 pins/side &amp; anti-ventilation fence.</text>\n'

    # --- RIGHT PANEL: DEEP-AFT STEP-OUT WING (TAIL-UP NOSE-DIVE & 45 cm CoL JUMP) ---
    s += '  <rect x="532" y="68" width="484" height="448" rx="8" fill="#FFFFFF" stroke="#FCA5A5" stroke-width="1.5"/>\n'
    s += '  <text x="550" y="92" class="warn">B. REJECTED: Deep-Aft Step-Out Wing vs. Deep STOL</text>\n'
    s += '  <text x="550" y="109" class="lbl-sm">Moving the step-out wing aft still trips the bow on wave crests &amp; shifts CoL!</text>\n'
    # Wave crest slamming the AFT step-out wing upward!
    s += '  <path d="M 542 332 Q 635 352 725 322 Q 825 262 910 272 Q 960 280 1006 318 L 1006 440 L 542 440 Z" fill="url(#water)"/>\n'
    s += '  <path d="M 542 332 Q 635 352 725 322 Q 825 262 910 272 Q 960 280 1006 318" fill="none" stroke="#0284C7" stroke-width="2.2"/>\n'
    # Hull pitching nose-DOWN because wave slams aft wing UP!
    s += '  <g transform="translate(765, 224) rotate(-5)">\n'
    s += '    <rect x="-145" y="-22" width="290" height="30" rx="14" fill="url(#tubeGrad)" stroke="#475569" stroke-width="1.6"/>\n'
    s += '    <line x1="-75" y1="8" x2="-75" y2="128" stroke="#334155" stroke-width="6"/>\n'
    s += '    <line x1="75" y1="8" x2="75" y2="128" stroke="#334155" stroke-width="6"/>\n'
    s += '    <rect x="-110" y="118" width="215" height="20" rx="8" fill="url(#carbon)" stroke="#0F172A" stroke-width="1.4"/>\n'
    # Deep-Aft Step-Out Wing getting slammed UP by wave crest!
    s += '    <rect x="70" y="42" width="60" height="10" rx="4" fill="#EF4444" stroke="#7F1D1D" stroke-width="1.6"/>\n'
    s += '    <circle cx="0" cy="-6" r="5" fill="#FBBF24" stroke="#0F172A" stroke-width="1.2"/>\n'
    s += '  </g>\n'
    # Upward slam arrow at aft wing -> nose-down pitch arc at bow!
    s += '  <circle cx="866" cy="264" r="18" fill="#DC2626" fill-opacity="0.22" stroke="#DC2626" stroke-width="1.8" stroke-dasharray="4,2"/>\n'
    s += '  <line x1="866" y1="252" x2="866" y2="178" stroke="#DC2626" stroke-width="3" marker-end="url(#arrRed)"/>\n'
    s += '  <text x="866" y="166" text-anchor="middle" class="warn">+150 kgf Tail Slam!</text>\n'
    # Curved nose-down torque arrow at bow!
    s += '  <path d="M 616 205 A 65 65 0 0 0 600 268" fill="none" stroke="#DC2626" stroke-width="2.6" marker-end="url(#arrRed)"/>\n'
    s += '  <text x="588" y="288" text-anchor="middle" class="warn">-1,350 N·m</text>\n'
    s += '  <text x="588" y="301" text-anchor="middle" class="lbl-sm">Bow Driven Down!</text>\n'
    s += '  <text x="768" y="182" text-anchor="middle" class="lbl-sm">CoG</text>\n'
    s += '  <text x="550" y="458" class="warn">1. Wave Crest on Aft Wing: +150 kgf lifts tail → drives bow into trough!</text>\n'
    s += '  <text x="550" y="476" class="warn">2. Takeoff Balance: +1,400 cm² aft shifts CoL ~45 cm → bow wheelbarrows!</text>\n'
    s += '  <text x="550" y="496" class="ok">WINNER: Deep-Submerged Split STOL Flaperons (400 mm deep, ~4 lbf wave ripple!)</text>\n'

    s += "</svg>\n"
    (OUT_DIR / "12-rejected-concepts-physics.svg").write_text(s)


# -------------------------------------------------------------------------
# DIAGRAM 16: Long-Range (60-75+ nm) Hydro Package Swaps & Energy Recipes
# -------------------------------------------------------------------------
def gen_16_long_range_packages():
    W, H = 1040, 620
    s = svg_header(
        W, H,
        "16. Long-Range (60–75+ nm) Hydro Package Swaps & Battery Recipes (Navigator 300)",
        "4 Hardware Swaps Cutting Energy Burn 28% (195 → 142 Wh/nm @ 15.5 kn | 165 → 118 Wh/nm @ 12 kn) + 3 Pack Options"
    )

    # --- PANEL A (TOP LEFT): SWAP #1 PROPULSION (TWIN 7.5" vs SINGLE 10" 2-BLADE + RUDDER) ---
    s += '  <rect x="24" y="68" width="484" height="252" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>\n'
    s += '  <text x="42" y="92" class="sec">A. Swap #1 (~50% of Gain): Single 65161 + 10" CNC Prop</text>\n'
    s += '  <text x="42" y="109" class="ok">Saves -3.5 lbf drag &amp; boosts eff. 63% → 70% (-32 Wh/nm @ 15.5 kn!)</text>\n'
    # Top mini-schematic: Standard Twin 65161 (top-down tail)
    s += '  <text x="42" y="136" class="lbl-sm">Standard: Twin 65161 + 7.5" Props (63% eff., diff. steer)</text>\n'
    s += '  <path d="M 75 168 L 210 168 Q 250 168 270 160 L 270 176 Q 250 168 210 168 Z" fill="url(#carbon)" stroke="#0F172A" stroke-width="1.4"/>\n'
    s += '  <rect x="65" y="156" width="175" height="24" rx="10" fill="url(#carbon)" stroke="#0F172A" stroke-width="1.4"/>\n'
    s += '  <rect x="228" y="138" width="42" height="14" rx="5" fill="#334155"/>\n'
    s += '  <rect x="228" y="184" width="42" height="14" rx="5" fill="#334155"/>\n'
    s += '  <line x1="274" y1="135" x2="274" y2="155" stroke="#0284C7" stroke-width="3.2" stroke-linecap="round"/>\n'
    s += '  <line x1="274" y1="181" x2="274" y2="201" stroke="#0284C7" stroke-width="3.2" stroke-linecap="round"/>\n'
    s += '  <text x="305" y="166" class="lbl-sm">2× nacelles + 2× small props</text>\n'
    s += '  <text x="305" y="180" class="lbl-sm">(~9.5 lbf aft drag @ 15.5 kn)</text>\n'
    # Bottom mini-schematic: Long-Range Single Centerline 65161 + 10" 2-Blade + Rudder
    s += '  <text x="42" y="226" class="ok">Long-Range: Single Centerline 65161 + 10"×11" CNC 2-Blade</text>\n'
    s += '  <rect x="65" y="244" width="175" height="24" rx="10" fill="url(#carbon)" stroke="#0F172A" stroke-width="1.4"/>\n'
    s += '  <rect x="234" y="248" width="46" height="16" rx="6" fill="#0F766E" stroke="#134E4A" stroke-width="1.2"/>\n'
    s += '  <line x1="286" y1="230" x2="286" y2="282" stroke="#059669" stroke-width="4.2" stroke-linecap="round"/>\n'
    s += '  <polygon points="212,248 238,248 238,236 218,236" fill="#F97316" stroke="#9A3412" stroke-width="1"/>\n'
    s += '  <text x="305" y="252" class="ok">1× 65161 + 1× 75100 VESC (-$95)</text>\n'
    s += '  <text x="305" y="266" class="lbl-sm">Internal-servo tail rudder flap</text>\n'
    s += '  <text x="305" y="280" class="ok">78–80% prop eff. (-3.5 lbf drag!)</text>\n'

    # --- PANEL B (TOP RIGHT): SWAPS #2 & #3 WING AR 13.5-14 + 2x RECESSED STRUTS ---
    s += '  <rect x="532" y="68" width="484" height="252" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>\n'
    s += '  <text x="550" y="92" class="sec">B. Swaps #2 &amp; #3: AR 14 Wide Wing + 2× Center Struts</text>\n'
    s += '  <text x="550" y="109" class="dim">Induced drag drops ~30% (1.05 m → 1.55 m span) • Struts 11.4 → 9.1 lbf</text>\n'
    # Top-down span overlay comparison
    cx_b = 774
    s += f'  <rect x="{cx_b-95}" y="138" width="190" height="22" rx="8" fill="#CBD5E1" stroke="#64748B" stroke-width="1.2" stroke-dasharray="4,2"/>\n'
    s += f'  <text x="{cx_b}" y="153" text-anchor="middle" class="lbl-sm">Standard 1.05 m (AR ≈ 9)</text>\n'
    # Wide AR 14 wing with folding tip hinge markers at +/- 270 mm (inside 600 mm tunnel!)
    s += f'  <rect x="{cx_b-165}" y="172" width="330" height="18" rx="7" fill="url(#wingBlue)" stroke="#0369A1" stroke-width="1.5"/>\n'
    for sd in (-1, 1):
        s += f'  <circle cx="{cx_b+sd*72}" cy="181" r="4" fill="#FBBF24" stroke="#0F172A" stroke-width="1.1"/>\n'
    s += f'  <text x="{cx_b}" y="185" text-anchor="middle" class="lbl-w">Long-Range 1.50–1.55 m (AR 13.5–14)</text>\n'
    s += f'  <text x="{cx_b}" y="206" text-anchor="middle" class="lbl-sm">Gold tip hinges fold outer tips 90° aft cleanly inside 600 mm tunnel</text>\n'
    # Strut cross-section comparison: 4x Blades vs 2x Recessed Center Struts
    s += '  <text x="556" y="236" class="lbl">80/20 Sweet Spot (Model 6):</text>\n'
    s += '  <text x="556" y="250" class="lbl-sm">Keep 4× 60×9 mm blades + Split STOL</text>\n'
    s += '  <text x="556" y="264" class="ok">125 Wh/nm @ 12 kn • 5.5" sand clear!</text>\n'
    s += '  <line x1="774" y1="224" x2="774" y2="306" stroke="#CBD5E1" stroke-width="1.2"/>\n'
    s += '  <text x="790" y="236" class="dim">Max-Range Full 4-Swap (Model 7):</text>\n'
    s += '  <text x="790" y="250" class="lbl-sm">2× 100×18 mm center struts + Switchblade</text>\n'
    s += '  <text x="790" y="264" class="ok">118 Wh/nm @ 12 kn • 142 @ 15.5 kn!</text>\n'
    s += '  <text x="556" y="294" class="lbl-sm">Swap #4 (Both): Low bow spray dodger cuts wind drag ~1.6 lbf (~6 Wh/nm) + dry 5-hr runs.</text>\n'

    # --- PANEL C (BOTTOM FULL WIDTH): RANGE BAR CHART FOR ALL 3 BATTERY RECIPES ---
    s += '  <rect x="24" y="336" width="992" height="260" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>\n'
    s += '  <text x="42" y="360" class="sec">C. Real-World Navigator 300 Range Recipes: Reaching 60–75+ nm (With 15% Weather Reserve)</text>\n'
    s += '  <text x="42" y="377" class="lbl-sm">Bar length = theoretical range (nm); dashed green band marks target 60–75 nm mission envelope</text>\n'

    # Chart frame (x = 340..980 -> 640 px for 0..100 nm => 6.4 px/nm!)
    gx0, gx1 = 340, 980
    gsc = 6.4
    # Target 60..75 nm shaded band!
    s += f'  <rect x="{gx0 + 60*gsc:.1f}" y="390" width="{15*gsc:.1f}" height="172" fill="#D1FAE5" fill-opacity="0.55" stroke="#059669" stroke-width="1.2" stroke-dasharray="4,3"/>\n'
    s += f'  <text x="{gx0 + 67.5*gsc:.1f}" y="404" text-anchor="middle" class="ok">60–75 nm Target</text>\n'
    # Grid ticks
    for nm in (0, 20, 40, 60, 75, 90, 100):
        tx = gx0 + nm * gsc
        s += f'  <line x1="{tx:.1f}" y1="410" x2="{tx:.1f}" y2="562" stroke="#E2E8F0" stroke-width="1"/>\n'
        s += f'  <text x="{tx:.1f}" y="576" text-anchor="middle" class="lbl-sm">{nm} nm</text>\n'

    bars = [
        ("Baseline: 5.38 kWh LiFePO4 (Twin STOL)", 29.8, 34.7, "#94A3B8", "#64748B"),
        ("Recipe B: 8.2 kWh Single-Pod NMC (Full LR)", 54.7, 67.1, "#0284C7", "#0369A1"),
        ("Recipe A/C: 10.8 kWh LiFePO4 (80/20 STOL)", 65.4, 79.5, "#0D9488", "#0F766E"),
        ("Recipe A/C: 10.8 kWh LiFePO4 (Full LR)", 70.0, 84.2, "#059669", "#047857"),
        ("Max Hybrid: 13.6 kWh NMC+LFP (Full LR)", 85.0, 100.0, "#D97706", "#B45309"),
    ]
    for idx, (label, r15, r12, c15, c12) in enumerate(bars):
        by = 418 + idx * 29
        s += f'  <text x="330" y="{by+14}" text-anchor="end" class="lbl">{html.escape(label)}</text>\n'
        # 12 kn eco bar (lighter background extension)
        s += f'  <rect x="{gx0}" y="{by+2}" width="{min(100, r12)*gsc:.1f}" height="18" rx="4" fill="{c12}" fill-opacity="0.32" stroke="{c12}" stroke-width="1"/>\n'
        # 15.5 kn cruise bar (solid foreground)
        s += f'  <rect x="{gx0}" y="{by+2}" width="{min(100, r15)*gsc:.1f}" height="18" rx="4" fill="{c15}"/>\n'
        # Value tags cleanly positioned
        s += f'  <text x="{gx0 + min(100, r15)*gsc - 6:.1f}" y="{by+14}" text-anchor="end" style="font-size:9px;fill:#FFFFFF;font-weight:700;">{r15:.0f} nm @15.5</text>\n'
        if r12 < 96:
            s += f'  <text x="{gx0 + r12*gsc + 6:.1f}" y="{by+14}" class="lbl-sm">{r12:.0f} nm @12kn</text>\n'
        else:
            s += f'  <text x="{gx0 + 100*gsc - 6:.1f}" y="{by+14}" text-anchor="end" style="font-size:9px;fill:#78350F;font-weight:700;">100+ @12kn</text>\n'

    s += '  <text x="42" y="590" class="lbl-sm">Solid bar = 15.5 kn fast cruise • Shaded extension = 12.0 kn eco-foiling • Optional 400 W solar bimini adds +10–13 nm over 5 hrs.</text>\n'

    s += "</svg>\n"
    (OUT_DIR / "16-long-range-hydro-packages.svg").write_text(s)


# -------------------------------------------------------------------------
# DIAGRAM 18: Modular Hard Deck Seating (1 or 2 Ergonomic Low-Sit Chairs)
# -------------------------------------------------------------------------
def gen_18_modular_seating():
    W, H = 1040, 620
    s = svg_header(
        W, H,
        "18. Modular Hard Deck Seating: 1 or 2 Ergonomic Low-Sit Chairs on Flush L-Tracks",
        "True Kit Navigator 300 (600 mm Tunnel) • 5-Sec Slide Between Solo CoG, Tandem 2-Up & 100% Flush Open Cargo Deck"
    )

    def draw_side_hull_and_deck(px, py, mode_lbl, sub_lbl):
        out = f'  <rect x="{px}" y="{py}" width="484" height="252" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>\n'
        out += f'  <text x="{px+16}" y="{py+24}" class="sec">{html.escape(mode_lbl)}</text>\n'
        out += f'  <text x="{px+16}" y="{py+40}" class="ok">{html.escape(sub_lbl)}</text>\n'
        y0 = py + 178
        # Hull outline + upturned bow + bow spray dodger + Tru-Alu transom
        out += f'  <path d="M {px+46} {y0-42} L {px+425} {y0-42} Q {px+455} {y0-42} {px+455} {y0+6} Q {px+455} {y0+42} {px+420} {y0+42} L {px+125} {y0+42} Q {px+65} {y0+38} {px+38} {y0+6} Q {px+26} {y0-24} {px+46} {y0-42} Z" fill="#E2E8F0" fill-opacity="0.38" stroke="#94A3B8" stroke-width="1.2"/>\n'
        # Curved translucent bow spray dodger
        out += f'  <path d="M {px+42} {y0-36} Q {px+95} {y0-96} {px+175} {y0-94} L {px+175} {y0-38} Z" fill="#0D9488" fill-opacity="0.28" stroke="#0F766E" stroke-width="1.5"/>\n'
        # Tru-Alu transom
        out += f'  <rect x="{px+404}" y="{y0-48}" width="9" height="48" rx="2" fill="url(#alu)" stroke="#334155" stroke-width="1.2"/>\n'
        # Bow-contoured Hard Deck (upturned bow footrest + flat cockpit + flush L-Track top stripe!)
        out += f'  <path d="M {px+400} {y0-14} L {px+150} {y0-14} Q {px+105} {y0-15} {px+68} {y0-32} L {px+72} {y0-20} Q {px+108} {y0-3} {px+150} {y0-2} L {px+400} {y0-2} Z" fill="url(#carbon)" stroke="#0F172A" stroke-width="1.3"/>\n'
        out += f'  <line x1="{px+152}" y1="{y0-14}" x2="{px+394}" y2="{y0-14}" stroke="#FBBF24" stroke-width="2.4"/>\n'
        # Foil Center of Lift (CoL) marker under hull
        x_col = px + 228
        out += f'  <line x1="{x_col}" y1="{y0+44}" x2="{x_col}" y2="{y0+18}" stroke="#0284C7" stroke-width="2" marker-end="url(#arrBlue)"/>\n'
        out += f'  <text x="{x_col}" y="{y0+56}" text-anchor="middle" class="dim">Foil CoL</text>\n'
        return out, y0

    def draw_chair_side(cx, y_deck, helm=False):
        # Reclined 22-deg low-sit ergonomic chair silhouette (~125 mm pan height = 16 px)
        out = f'  <line x1="{cx-26}" y1="{y_deck}" x2="{cx+16}" y2="{y_deck}" stroke="#FBBF24" stroke-width="3.2"/>\n'
        out += f'  <line x1="{cx-20}" y1="{y_deck}" x2="{cx-28}" y2="{y_deck-18}" stroke="#475569" stroke-width="2.2"/>\n'
        out += f'  <line x1="{cx+10}" y1="{y_deck}" x2="{cx+12}" y2="{y_deck-14}" stroke="#475569" stroke-width="2.2"/>\n'
        out += f'  <path d="M {cx-32} {y_deck-20} L {cx+14} {y_deck-14} L {cx+34} {y_deck-66}" fill="none" stroke="#0F172A" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>\n'
        if helm:
            out += f'  <line x1="{cx-14}" y1="{y_deck-34}" x2="{cx+16}" y2="{y_deck-34}" stroke="#334155" stroke-width="3.2" stroke-linecap="round"/>\n'
            out += f'  <circle cx="{cx-16}" cy="{y_deck-38}" r="4.2" fill="#F97316" stroke="#9A3412" stroke-width="1"/>\n'
        return out

    # --- PANEL A (TOP LEFT): SOLO 1-CHAIR LONG-RANGE MODE ---
    s_a, y0_a = draw_side_hull_and_deck(24, 68, "A. Mode 1: Solo Long-Range (1 Chair @ CoG)", "Chair slides to X ≈ 0 mm • Head low behind dodger • Aft gear/extender bay")
    s += s_a
    s += draw_chair_side(24 + 258, y0_a - 14, helm=True)
    # Reclined pilot torso + legs forward onto upturned bow footrest!
    s += f'  <circle cx="{24+274}" cy="{y0_a-84}" r="10" fill="#38BDF8" stroke="#0369A1" stroke-width="1.3"/>\n'
    s += f'  <path d="M {24+272} {y0_a-74} L {24+258} {y0_a-34} L {24+185} {y0_a-38} L {24+120} {y0_a-32}" fill="none" stroke="#0369A1" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" stroke-opacity="0.55"/>\n'
    # Aft expedition dry bag / plug-in 5.4 kWh extender pack on rear L-Track
    s += f'  <rect x="{24+322}" y="{y0_a-42}" width="66" height="27" rx="4" fill="#FEF3C7" stroke="#D97706" stroke-width="1.3" stroke-dasharray="4,2"/>\n'
    s += f'  <text x="{24+355}" y="{y0_a-25}" text-anchor="middle" style="font-size:8.5px;fill:#92400E;font-weight:700;">Extender / Gear</text>\n'
    s += f'  <text x="42" y="{y0_a+66}" class="lbl-sm">Pilot CoG lands dead-on Foil CoL • -250 mm lower CoG &amp; -8 Wh/nm wind drag!</text>\n'

    # --- PANEL B (TOP RIGHT): TANDEM 2-CHAIR LONG-RANGE MODE ---
    s_b, y0_b = draw_side_hull_and_deck(532, 68, "B. Mode 2: Tandem 2-Up Long-Range (2 Chairs Inline)", "424 mm chairs fit 600 mm tunnel • Zero roll bias • Armrest helm on aft chair")
    s += s_b
    s += draw_chair_side(532 + 205, y0_b - 14, helm=False)
    s += draw_chair_side(532 + 322, y0_b - 14, helm=True)
    # Front passenger + aft pilot silhouettes
    s += f'  <circle cx="{532+222}" cy="{y0_b-84}" r="9.5" fill="#14B8A6" stroke="#0F766E" stroke-width="1.2"/>\n'
    s += f'  <path d="M {532+220} {y0_b-74} L {532+205} {y0_b-34} L {532+142} {y0_b-36} L {532+96} {y0_b-34}" fill="none" stroke="#0F766E" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round" stroke-opacity="0.55"/>\n'
    s += f'  <circle cx="{532+338}" cy="{y0_b-84}" r="9.5" fill="#38BDF8" stroke="#0369A1" stroke-width="1.2"/>\n'
    s += f'  <path d="M {532+336} {y0_b-74} L {532+322} {y0_b-34} L {532+262} {y0_b-36}" fill="none" stroke="#0369A1" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round" stroke-opacity="0.55"/>\n'
    s += f'  <text x="{532+286}" y="{y0_b-102}" text-anchor="middle" class="warn">Armrest Helm Pod</text>\n'
    s += f'  <line x1="{532+290}" y1="{y0_b-96}" x2="{532+305}" y2="{y0_b-56}" stroke="#DC2626" stroke-width="1.1" marker-end="url(#arrRed)"/>\n'
    s += f'  <text x="550" y="{y0_b+66}" class="lbl-sm">Slide ±150 mm on L-Tracks in 5 sec to trim perfectly for any crew weight!</text>\n'

    # --- PANEL C (BOTTOM FULL WIDTH): TOP-DOWN FITMENT & FLUSH L-TRACK CROSS-SECTION ---
    s += '  <rect x="24" y="336" width="992" height="260" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>\n'
    s += '  <text x="42" y="360" class="sec">C. Top-Down Navigator 300 Fitment (600 mm Inside Beam) &amp; Flush L-Track Detail</text>\n'
    s += '  <text x="42" y="377" class="lbl-sm">Zero protrusions when chairs unclip (Mode 3: Open Cargo / Beaching Deck) • Same twin rails hold chairs, batteries, or dry bags</text>\n'

    # Left half of Panel C: Top-Down schematic of Navigator 300 + Bow-Contoured Deck + Twin L-Tracks + 2 Tandem Chairs!
    tx0, ty_c = 70, 480
    # Outer U-shaped Ø460 inflatable tubes (visualized top-down!)
    s += f'  <path d="M {tx0+490} {ty_c-86} L {tx0+155} {ty_c-86} Q {tx0+32} {ty_c-86} {tx0+18} {ty_c} Q {tx0+32} {ty_c+86} {tx0+155} {ty_c+86} L {tx0+490} {ty_c+86}" fill="none" stroke="#94A3B8" stroke-width="32" stroke-linecap="round"/>\n'
    # Bow-contoured Hard Deck inside tubes
    s += f'  <path d="M {tx0+460} {ty_c-54} L {tx0+160} {ty_c-54} Q {tx0+92} {ty_c-48} {tx0+66} {ty_c} Q {tx0+92} {ty_c+48} {tx0+160} {ty_c+54} L {tx0+460} {ty_c+54} Z" fill="url(#carbon)" stroke="#0F172A" stroke-width="1.4"/>\n'
    # Flush Twin L-Track rails (390 mm spacing -> +/- 31 px!)
    for sd in (-1, 1):
        s += f'  <line x1="{tx0+145}" y1="{ty_c+sd*31}" x2="{tx0+445}" y2="{ty_c+sd*31}" stroke="#FBBF24" stroke-width="4"/>\n'
    # Front & Aft Low-Sit Chairs (424 mm wide -> 68 px height)
    s += f'  <rect x="{tx0+190}" y="{ty_c-34}" width="88" height="68" rx="7" fill="url(#wingTeal)" fill-opacity="0.88" stroke="#0F766E" stroke-width="1.5"/>\n'
    s += f'  <text x="{tx0+234}" y="{ty_c+4}" text-anchor="middle" class="lbl-w">Front Chair</text>\n'
    s += f'  <rect x="{tx0+315}" y="{ty_c-34}" width="88" height="68" rx="7" fill="url(#wingBlue)" fill-opacity="0.88" stroke="#0369A1" stroke-width="1.5"/>\n'
    s += f'  <text x="{tx0+359}" y="{ty_c+4}" text-anchor="middle" class="lbl-w">Pilot Chair</text>\n'
    # Armrest helm pod on starboard (-Y = top side) of aft pilot chair
    s += f'  <rect x="{tx0+322}" y="{ty_c-43}" width="32" height="9" rx="3" fill="#F97316" stroke="#9A3412" stroke-width="1"/>\n'
    # Dimension markers
    s += dim_line(tx0 + 508, ty_c - 54, tx0 + 508, ty_c + 54, "600 mm", dx=28, dy=4)
    s += f'  <text x="{tx0+280}" y="{ty_c+92}" text-anchor="middle" class="lbl-sm">424 mm Chairs Inside 600 mm Tunnel (~85 mm Clear/Side to Ø460 Tubes)</text>\n'

    # Right half of Panel C: Flush Recessed L-Track Cross-Section Detail!
    rx0, ry0 = 655, 425
    s += f'  <rect x="{rx0}" y="{ry0}" width="340" height="150" rx="6" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.2"/>\n'
    s += f'  <text x="{rx0+14}" y="{ry0+20}" class="lbl">Flush L-Track Cross-Section (Zero Trip Edge!)</text>\n'
    # 28/60 mm Carbon Hard Deck slab with routed recess pocket for L-Track
    s += f'  <path d="M {rx0+24} {ry0+68} L {rx0+125} {ry0+68} L {rx0+125} {ry0+94} L {rx0+215} {ry0+94} L {rx0+215} {ry0+68} L {rx0+316} {ry0+68} L {rx0+316} {ry0+128} L {rx0+24} {ry0+128} Z" fill="url(#carbon)" stroke="#0F172A" stroke-width="1.4"/>\n'
    # Recessed anodized aluminum L-Track profile sitting 100% FLUSH with top deck!
    s += f'  <path d="M {rx0+127} {ry0+68} L {rx0+154} {ry0+68} L {rx0+154} {ry0+77} L {rx0+144} {ry0+77} L {rx0+144} {ry0+87} L {rx0+196} {ry0+87} L {rx0+196} {ry0+77} L {rx0+186} {ry0+77} L {rx0+186} {ry0+68} L {rx0+213} {ry0+68} L {rx0+213} {ry0+92} L {rx0+127} {ry0+92} Z" fill="url(#alu)" stroke="#334155" stroke-width="1.2"/>\n'
    # Gold spring-loaded double-stud quick-release fitting clicking in from above!
    s += f'  <path d="M {rx0+162} {ry0+40} L {rx0+178} {ry0+40} L {rx0+178} {ry0+78} L {rx0+190} {ry0+78} L {rx0+190} {ry0+85} L {rx0+150} {ry0+85} L {rx0+150} {ry0+78} L {rx0+162} {ry0+78} Z" fill="#FBBF24" stroke="#78350F" stroke-width="1.2"/>\n'
    s += f'  <text x="{rx0+170}" y="{ry0+34}" text-anchor="middle" class="ok">5-Sec Quick-Release Stud (900 kgf)</text>\n'
    s += f'  <text x="{rx0+75}" y="{ry0+60}" text-anchor="middle" class="lbl-sm">100% Flush Deck</text>\n'
    s += f'  <text x="{rx0+268}" y="{ry0+60}" text-anchor="middle" class="lbl-sm">Recessed L-Track</text>\n'
    s += f'  <text x="{rx0+170}" y="{ry0+114}" text-anchor="middle" class="lbl-w">28 mm or 60 mm Hard Deck Core</text>\n'
    s += f'  <text x="{rx0+170}" y="{ry0+143}" text-anchor="middle" class="ok">Cost: ~$55 rails + ~$110–$180/chair (~2.5 kg ea.)</text>\n'

    s += "</svg>\n"
    (OUT_DIR / "18-modular-seating-ergonomics.svg").write_text(s)


if __name__ == "__main__":
    gen_01_switchblade()
    gen_02_stol_flaperons()
    gen_03_spine_coupling()
    gen_04_grounding_kickup()
    gen_05_strut_stackup()
    gen_09_cartridge_cutaway()
    gen_10_alt_architectures()
    gen_12_rejected_step_out_physics()
    gen_16_long_range_packages()
    gen_18_modular_seating()
    print("Generated all 10 2D engineering SVGs in", OUT_DIR)
