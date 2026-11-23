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


# -------------------------------------------------------------------------
# DIAGRAM 20: Dual-Mode Morphing STOL-to-Staggerwing Flaperon Kinematics
# -------------------------------------------------------------------------
def gen_20_morphing_stol_staggerwing():
    W, H = 1040, 548
    s = svg_header(
        W, H,
        "20. 100% Internal-Pod Morphing STOL-to-Staggerwing Flaperon (Wet-Slot Elevator Sled)",
        "90 mm Pod Envelope (ZERO External Arms, Belts, or Sliding Dry-Hull Seals) • Mode 1 DOWN (-35 mm) ↔ Mode 2 UP (+35 mm)"
    )

    # --- PANEL A (LEFT): SIDE-PROFILE 90 mm POD & 70 mm PURE VERTICAL TRAVEL ---
    s += '  <rect x="24" y="68" width="530" height="456" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>\n'
    s += '  <text x="42" y="92" class="sec">A. Side Profile: 100% Inside 90 mm Pod (70 mm Stroke)</text>\n'
    s += '  <text x="42" y="109" class="ok">6–8 mm Venturi slot (DOWN) ↔ 57 mm / 4–5× wake clearance (UP)</text>\n'
    s += '  <rect x="34" y="118" width="510" height="316" rx="6" fill="url(#water)"/>\n'

    # Scale: 1 mm = 1.60 px -> 90 mm pod height = 144 px tall; cy = 266 -> top = 194, bot = 338
    cy = 266
    # 90 mm Flying-Keel Pod outline (100% encloses Main Wing + both UP & DOWN flaperon pivots!)
    s += f'  <rect x="44" y="{cy-72}" width="474" height="144" rx="36" fill="#334155" fill-opacity="0.16" stroke="#334155" stroke-width="2"/>\n'
    # Free-flooding internal wing-box bay (x = 304..404) bounded by twin green watertight bulkheads!
    s += f'  <rect x="304" y="{cy-70}" width="100" height="140" fill="#BAE6FD" fill-opacity="0.45" stroke="none"/>\n'
    s += f'  <rect x="294" y="{cy-71}" width="10" height="142" rx="2" fill="#0F766E" stroke="#134E4A" stroke-width="1.2"/>\n'
    s += f'  <rect x="404" y="{cy-71}" width="10" height="142" rx="2" fill="#0F766E" stroke="#134E4A" stroke-width="1.2"/>\n'
    s += f'  <text x="168" y="{cy-52}" text-anchor="middle" class="lbl-sm">Dry IP68 Bay (Battery + VESC + IMU)</text>\n'
    s += f'  <text x="354" y="{cy-80}" text-anchor="middle" style="font-size:8.8px;fill:#0F766E;font-weight:700;">Wet Wing-Box</text>\n'

    # Twin Ø10 mm vertical guide rods + central gold Tr10x2 leadscrew inside wet wing-box
    s += f'  <rect x="330" y="{cy-68}" width="5" height="136" fill="url(#alu)" stroke="#475569" stroke-width="0.9"/>\n'
    s += f'  <rect x="373" y="{cy-68}" width="5" height="136" fill="url(#alu)" stroke="#475569" stroke-width="0.9"/>\n'
    s += f'  <rect x="351" y="{cy-68}" width="6" height="136" fill="#FBBF24" stroke="#92400E" stroke-width="1"/>\n'
    # Vertical flush cheek slot outline (12 x 75 mm -> 19 x 120 px)
    s += f'  <rect x="345" y="{cy-60}" width="18" height="120" rx="4" fill="none" stroke="#0F172A" stroke-width="1.2" stroke-dasharray="3,2"/>\n'

    # Fixed Main Wing (100 mm chord = 160 px) mounted in LOWER THIRD (Z = -22 mm -> y = 266 + 35 = 301)
    y_mw = cy + 35
    mw_pts = transform_pts(naca4_points(0.02, 0.4, 0.10, 160), 118, y_mw, deg=2)
    s += f'  <polygon points="{pts_to_str(mw_pts)}" fill="url(#carbon)" stroke="#0F172A" stroke-width="1.8"/>\n'
    s += f'  <text x="195" y="{y_mw+26}" text-anchor="middle" class="lbl">Fixed Main Wing (Z = -22 mm)</text>\n'

    # Thin turbulent viscous wake trailing aft of Main Wing (~10-14 mm thick = ~18-22 px, ~1 deg downwash)
    s += f'  <path d="M 278 {y_mw-4} L 538 {y_mw+2} L 538 {y_mw+26} L 278 {y_mw+10} Z" fill="#94A3B8" fill-opacity="0.38"/>\n'
    s += f'  <text x="482" y="{y_mw+18}" text-anchor="middle" class="lbl-sm">~12 mm Wake</text>\n'

    # Mode 1 DOWN: Z = -35 mm -> y_dn = 266 + 56 = 322 (+15 deg STOL Takeoff, 6-8 mm slot gap!)
    xp = 354
    y_dn = cy + 56
    y_up = cy - 56
    fl_dn = transform_pts(naca4_points(0.02, 0.4, 0.11, 96), xp - 19, y_dn - 3, deg=15)
    s += f'  <polygon points="{pts_to_str(fl_dn)}" fill="url(#wingBlue)" fill-opacity="0.88" stroke="#0369A1" stroke-width="1.6"/>\n'
    s += f'  <circle cx="{xp}" cy="{y_dn}" r="4.5" fill="#FBBF24" stroke="#0F172A" stroke-width="1.2"/>\n'
    # Converging Venturi slot jet between Main Wing TE (278, 305) and Flap LE (335, 319)
    s += f'  <path d="M 225 {y_mw+16} Q 290 {y_mw+15} 348 {y_dn+2} Q 402 {y_dn+14} 448 {y_dn+32}" fill="none" stroke="#0284C7" stroke-width="2" marker-end="url(#arrBlue)"/>\n'

    # Mode 2 UP: Z = +35 mm -> y_up = 266 - 56 = 210 (0 deg / +/-3 deg Protected Staggerwing Cruise!)
    fl_up = transform_pts(naca4_points(0.02, 0.4, 0.11, 96), xp - 19, y_up - 1, deg=0)
    s += f'  <polygon points="{pts_to_str(fl_up)}" fill="#F97316" stroke="#9A3412" stroke-width="1.6"/>\n'
    s += f'  <circle cx="{xp}" cy="{y_up}" r="4.5" fill="#FBBF24" stroke="#0F172A" stroke-width="1.2"/>\n'
    # Clean laminar freestream streamline over UP wing (far above wake!)
    s += f'  <path d="M 195 {y_up-18} L 526 {y_up-18}" fill="none" stroke="#059669" stroke-width="1.8" stroke-dasharray="5,3" marker-end="url(#arrGreen)"/>\n'

    # Vertical travel arrow & clear non-overlapping callouts
    s += f'  <line x1="{xp}" y1="{y_dn-9}" x2="{xp}" y2="{y_up+10}" stroke="#0D9488" stroke-width="2.6" marker-end="url(#arrGreen)"/>\n'
    s += dim_line(456, y_up, 456, y_dn, "70 mm", dx=24, dy=4, cls="ok", marker="arrGreen", stroke="#059669")
    s += dim_line(284, y_up, 284, y_mw, "57 mm", dx=-24, dy=-4, cls="dim", marker="arrBlue", stroke="#0284C7")

    s += '  <text x="366" y="142" text-anchor="middle" class="ok">Mode 2 UP (Z = +35 mm): Protected Staggerwing</text>\n'
    s += '  <text x="366" y="156" text-anchor="middle" class="lbl-sm">100% laminar flow (4–5× above wake) • Still 10 mm inside pod roof!</text>\n'
    s += '  <text x="300" y="396" text-anchor="middle" class="dim">Mode 1 DOWN (Z = -35 mm): Junkers STOL (+15°)</text>\n'
    s += '  <text x="300" y="410" text-anchor="middle" class="lbl-sm">Optimal 6–8 mm Venturi slot (CL_max ≈ 2.0) • Still 10 mm inside pod belly!</text>\n'
    s += '  <text x="150" y="254" text-anchor="middle" class="ok">Dry Bay</text>\n'
    s += '  <text x="150" y="268" text-anchor="middle" class="lbl-sm">(Watertight Bulkhead at TE →)</text>\n'

    s += '  <text x="42" y="458" class="ok">Zero External Arms: Entire sled + 70 mm travel fits flush inside 90 mm pod!</text>\n'
    s += '  <text x="42" y="476" class="lbl-sm">Hydrodynamic Win: Narrower 6–8 mm STOL slot (DOWN) + 4–5× wake clearance (UP).</text>\n'
    s += '  <text x="42" y="496" class="lbl-sm">Debris Shield: Fixed lower Main Wing blocks kelp/rocks ahead of UP flaperons.</text>\n'

    # --- PANEL B (RIGHT): FRONT CROSS-SECTION (Y-Z CUTAWAY) OF WET-SLOT ELEVATOR SLED ---
    s += '  <rect x="574" y="68" width="442" height="456" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>\n'
    s += '  <text x="592" y="92" class="sec">B. Front Cutaway: Wet-Slot / Dry-Bay Elevator Sled</text>\n'
    s += '  <text x="592" y="109" class="dim">Direct-drive IP68 servos ride ON sled • ZERO belts, gears, or sliding dry seals</text>\n'

    cx_b, cy_b = 795, 266
    # 220 x 90 mm Flying-Keel Pod cross-section (220 px wide x 144 px tall -> x=685..905, y=194..338)
    s += f'  <rect x="{cx_b-110}" y="{cy_b-72}" width="220" height="144" rx="28" fill="#E0F2FE" stroke="#0F172A" stroke-width="2.4"/>\n'
    s += f'  <text x="{cx_b}" y="144" text-anchor="middle" class="lbl-sm">220 × 90 mm Free-Flooding Wing-Box (Front View)</text>\n'

    # Flush Silicone Cheek Wiper Skirts (centerboard-style gaskets at pod walls x = cx_b +/- 110)
    for sd in (-1, 1):
        wx = cx_b + sd * 110
        s += f'  <rect x="{wx-5}" y="{cy_b-60}" width="10" height="120" rx="2" fill="#0F766E" stroke="#134E4A" stroke-width="1.2"/>\n'

    # Twin Ø10 mm stainless vertical guide rods + central gold Tr10x2 self-locking leadscrew
    s += f'  <rect x="{cx_b-78}" y="{cy_b-68}" width="8" height="136" fill="url(#alu)" stroke="#334155" stroke-width="1.1"/>\n'
    s += f'  <rect x="{cx_b+70}" y="{cy_b-68}" width="8" height="136" fill="url(#alu)" stroke="#334155" stroke-width="1.1"/>\n'
    s += f'  <rect x="{cx_b-5}" y="{cy_b-68}" width="10" height="136" fill="#FBBF24" stroke="#92400E" stroke-width="1.2"/>\n'

    # Top worm-gear / motor drive cap (0 W self-locking Tr10x2 hold, >300 kgf vertical!)
    s += f'  <rect x="{cx_b-30}" y="{cy_b-98}" width="60" height="24" rx="4" fill="#DC2626" stroke="#7F1D1D" stroke-width="1.3"/>\n'
    s += f'  <text x="{cx_b}" y="{cy_b-83}" text-anchor="middle" style="font-size:8.2px;fill:#FFFFFF;font-weight:700;">Tr10×2 Drive</text>\n'

    # Dashed Ghost Elevator Sled at Mode 1 DOWN (Z = -35 mm -> y = cy_b + 48)
    y_sled_dn = cy_b + 44
    s += f'  <rect x="{cx_b-86}" y="{y_sled_dn-14}" width="172" height="28" rx="4" fill="#0284C7" fill-opacity="0.18" stroke="#0284C7" stroke-width="1.4" stroke-dasharray="4,3"/>\n'
    s += f'  <line x1="{cx_b-166}" y1="{y_sled_dn}" x2="{cx_b-86}" y2="{y_sled_dn}" stroke="#0284C7" stroke-width="5" stroke-dasharray="4,3"/>\n'
    s += f'  <line x1="{cx_b+86}" y1="{y_sled_dn}" x2="{cx_b+166}" y2="{y_sled_dn}" stroke="#0284C7" stroke-width="5" stroke-dasharray="4,3"/>\n'
    s += f'  <text x="{cx_b}" y="{y_sled_dn+4}" text-anchor="middle" style="font-size:8.5px;fill:#0369A1;font-weight:700;">Mode 1 DOWN Sled (Z = -35 mm)</text>\n'

    # Solid Aluminum/Delrin Elevator Sled at Mode 2 UP (Z = +35 mm -> y = cy_b - 42)
    y_sled_up = cy_b - 40
    s += f'  <rect x="{cx_b-88}" y="{y_sled_up-18}" width="176" height="36" rx="5" fill="#475569" stroke="#0F172A" stroke-width="1.6"/>\n'
    # 2x Gold IP68 CNC Billet Pitch Servos riding DIRECTLY on the sled!
    for sd, lbl_s in [(-1, "Port IP68"), (1, "Stbd IP68")]:
        sx = cx_b + sd * 44
        s += f'  <rect x="{sx-26}" y="{y_sled_up-14}" width="52" height="28" rx="4" fill="#FBBF24" stroke="#92400E" stroke-width="1.3"/>\n'
        s += f'  <text x="{sx}" y="{y_sled_up-2}" text-anchor="middle" style="font-size:7.6px;fill:#0F172A;font-weight:700;">{lbl_s}</text>\n'
        s += f'  <text x="{sx}" y="{y_sled_up+9}" text-anchor="middle" style="font-size:7.2px;fill:#451A03;">75 kg·cm</text>\n'
        # Direct-drive Ø8 mm stainless flaperon shaft exiting through cheek wiper!
        x_sh0 = sx + sd * 26
        x_sh1 = cx_b + sd * 130
        s += f'  <line x1="{x_sh0}" y1="{y_sled_up}" x2="{x_sh1}" y2="{y_sled_up}" stroke="#DC2626" stroke-width="4.2"/>\n'
        # Orange UP flaperon blade extending outboard
        fx0 = cx_b + sd * 124 if sd > 0 else cx_b - 196
        s += f'  <rect x="{fx0}" y="{y_sled_up-8}" width="72" height="16" rx="4" fill="#F97316" stroke="#9A3412" stroke-width="1.4"/>\n'

    # Central Tr10x2 bronze nut on sled
    s += f'  <rect x="{cx_b-10}" y="{y_sled_up-10}" width="20" height="20" rx="2" fill="#D97706" stroke="#78350F" stroke-width="1.2"/>\n'

    # Static IP68 Bulkhead Wire Gland + flexible 3-wire silicone pigtail loop (ZERO sliding dry seals!)
    s += f'  <circle cx="{cx_b-34}" cy="{cy_b+4}" r="6" fill="#0F766E" stroke="#134E4A" stroke-width="1.3"/>\n'
    s += f'  <path d="M {cx_b-44} {y_sled_up+14} C {cx_b-56} {cy_b-8} {cx_b-16} {cy_b-12} {cx_b-34} {cy_b+4}" fill="none" stroke="#DC2626" stroke-width="2" stroke-dasharray="3,2"/>\n'
    s += f'  <text x="{cx_b+32}" y="{cy_b+6}" text-anchor="middle" style="font-size:8.2px;fill:#0F766E;font-weight:700;">← Static Bulkhead Gland</text>\n'

    # Bottom Sand-Flush Drain Port
    s += f'  <rect x="{cx_b-16}" y="{cy_b+67}" width="32" height="10" rx="2" fill="#0284C7" stroke="#0369A1" stroke-width="1.1"/>\n'
    s += f'  <text x="{cx_b}" y="{cy_b+93}" text-anchor="middle" class="lbl-sm">Bottom Sand-Flush Drain Port (5 s freshwater hose rinse)</text>\n'

    # Side labels for silicone wipers & direct shafts
    s += f'  <text x="636" y="{y_sled_up-16}" text-anchor="middle" class="lbl">Ø8 mm Direct</text>\n'
    s += f'  <text x="954" y="{y_sled_up-16}" text-anchor="middle" class="lbl">UP Flaperon</text>\n'
    s += f'  <text x="636" y="{cy_b+16}" text-anchor="middle" class="ok">Silicone</text>\n'
    s += f'  <text x="636" y="{cy_b+28}" text-anchor="middle" class="lbl-sm">Wiper Skirt</text>\n'
    s += f'  <text x="956" y="{cy_b+16}" text-anchor="middle" class="ok">Silicone</text>\n'
    s += f'  <text x="956" y="{cy_b+28}" text-anchor="middle" class="lbl-sm">Wiper Skirt</text>\n'

    # Bottom numbered takeaways
    s += '  <text x="592" y="438" class="lbl-sm">1. Tr10×2 leadscrew self-locks UP/DOWN at 0 W (&gt;300 kgf vertical load).</text>\n'
    s += '  <text x="592" y="456" class="lbl-sm">2. IP68 servos ride ON sled: direct Ø8 mm drive (≤3.6 N·m, 0 belts/gears).</text>\n'
    s += '  <text x="592" y="474" class="ok">3. Dry bay stays 100% statically sealed (only a stationary cable gland).</text>\n'
    s += '  <text x="592" y="494" class="dim">Simpler Alt: Fixed Upper Staggerwing (Z = +35 mm) = +0.5 kn takeoff, 0 sled!</text>\n'

    s += "</svg>\n"
    (OUT_DIR / "20-morphing-stol-staggerwing.svg").write_text(s)


# -------------------------------------------------------------------------
# DIAGRAM 21: 2x Recessed Center Struts — Asymmetric Loads & One-Sided Impact
# -------------------------------------------------------------------------
def gen_21_center_strut_asymmetric_loads():
    W, H = 1080, 760
    s = svg_header(
        W, H,
        "21. 2× Recessed Center Struts & True 90° Upper/Lower Channel Linked-Fold Protection",
        "90° Flush Under/Above Channels (220 mm Dart!) + Wet IP68 Servo Variable-Preload Pins + Wide T-Head & Pod Saddle Trunnions"
    )

    # =========================================================================
    # PANEL A (TOP LEFT): (A1) ZOOMED 90° LOWER CHANNEL + (A2) 220 mm FOLDED DART
    # =========================================================================
    s += '  <rect x="24" y="68" width="508" height="346" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>\n'
    s += '  <text x="42" y="92" class="sec">A. Bottom-Up: True 90° Lower Fold Channel (220 mm Dart!)</text>\n'
    s += '  <text x="42" y="109" class="ok">Pivots @ y = ±54 mm + meshed gears → BOTH halves tuck 90° flush under belly!</text>\n'

    # --- SUB-BOX A1 (TOP HALF): ZOOMED ROOT PIVOTS + MESHED GEARS + SERVO CAM PIN ---
    s += '  <rect x="36" y="118" width="484" height="128" rx="6" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>\n'
    s += '  <text x="46" y="134" class="dim">A1. Close-Up Inside 12 mm Recessed Belly Channel (Bottom-Up View)</text>\n'
    s += '  <text x="46" y="238" class="lbl-sm">← BOW</text>\n'
    s += '  <text x="510" y="238" text-anchor="end" class="ok">90° STRAIGHT-AFT CHANNEL →</text>\n'

    gx, gy = 160, 184
    s += f'  <rect x="{gx-52}" y="{gy-40}" width="92" height="80" rx="6" fill="#FEF3C7" stroke="#D97706" stroke-width="1.6"/>\n'
    s += f'  <rect x="{gx-22}" y="{gy-46}" width="38" height="34" rx="4" fill="url(#wingBlue)" stroke="#0369A1" stroke-width="1.4"/>\n'
    s += f'  <rect x="{gx-22}" y="{gy+12}" width="38" height="34" rx="4" fill="url(#wingBlue)" stroke="#0369A1" stroke-width="1.4"/>\n'
    s += f'  <circle cx="{gx-3}" cy="{gy-12}" r="11" fill="url(#alu)" stroke="#334155" stroke-width="1.5" stroke-dasharray="3,2"/>\n'
    s += f'  <circle cx="{gx-3}" cy="{gy+12}" r="11" fill="url(#alu)" stroke="#334155" stroke-width="1.5" stroke-dasharray="3,2"/>\n'
    # 2x Gold Ø16 mm Vertical Root Pivot Pins at y = ±54 mm
    s += f'  <circle cx="{gx-3}" cy="{gy-28}" r="5.0" fill="#FBBF24" stroke="#0F172A" stroke-width="1.3"/>\n'
    s += f'  <circle cx="{gx-3}" cy="{gy+28}" r="5.0" fill="#FBBF24" stroke="#0F172A" stroke-width="1.3"/>\n'
    # Servo-controlled variable-preload roller pin on 110 mm slider lug (red dot + gold servo box!)
    s += f'  <rect x="{gx+8}" y="{gy-6}" width="36" height="12" rx="2" fill="#475569"/>\n'
    s += f'  <circle cx="{gx+34}" cy="{gy}" r="5.4" fill="#DC2626" stroke="#FFFFFF" stroke-width="1.3"/>\n'
    s += f'  <path d="M {gx+24} {gy-34} Q {gx+56} {gy-34} {gx+70} {gy-14}" fill="none" stroke="#059669" stroke-width="2.2" marker-end="url(#arrGreen)"/>\n'
    s += f'  <path d="M {gx+24} {gy+34} Q {gx+56} {gy+34} {gx+70} {gy+14}" fill="none" stroke="#059669" stroke-width="2.2" marker-end="url(#arrGreen)"/>\n'

    s += '  <text x="46" y="168" class="lbl-sm">40 mm Roots</text>\n'
    s += '  <text x="46" y="180" class="lbl-sm">under Bridge</text>\n'
    s += '  <text x="46" y="192" class="lbl-sm">(100% lift!)</text>\n'
    s += '  <text x="268" y="152" class="warn">1. Wet IP68 Servo Roller Pin (red)</text>\n'
    s += '  <text x="278" y="165" class="lbl-sm">dials 0% Fold / 50% Reef / 100% Cruise!</text>\n'
    s += '  <text x="268" y="184" class="ok">2. Meshed 90° stainless gears</text>\n'
    s += '  <text x="278" y="197" class="lbl-sm">tuck BOTH halves 90° inside 220 mm!</text>\n'
    s += '  <text x="268" y="213" class="dim">3. Dyneema pulley loop deploys/folds</text>\n'
    s += '  <text x="278" y="225" class="lbl-sm">5-sec pull-to-reset — ZERO broken pins!</text>\n'

    # --- SUB-BOX A2 (BOTTOM HALF): FULL-POD TOP-DOWN IN 90° FLUSH 220 mm DART MODE ---
    s += '  <rect x="36" y="254" width="484" height="148" rx="6" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>\n'
    s += '  <text x="46" y="270" class="dim">A2. Full-Pod 90° Folded Dart (204 mm Inside 220 mm Pod • 179 mm Clear of Prop!)</text>\n'

    px, py = 248, 330
    # Pod body (230 px long: x = 133..363, height 34 px = 220 mm!)
    s += f'  <rect x="{px-115}" y="{py-17}" width="230" height="34" rx="16" fill="url(#carbon)" stroke="#0F172A" stroke-width="1.5"/>\n'
    # Tail prop at x = 376
    s += f'  <line x1="{px+128}" y1="{py-22}" x2="{px+128}" y2="{py+22}" stroke="#0284C7" stroke-width="4" stroke-linecap="round"/>\n'
    s += f'  <text x="{px+136}" y="{py-2}" class="dim">Tail Prop</text>\n'
    s += f'  <text x="{px+136}" y="{py+10}" class="ok">(179 mm</text>\n'
    s += f'  <text x="{px+136}" y="{py+22}" class="ok">clear!)</text>\n'

    # Deployed 0° Wing ghost (dashed blue) at x = 180
    s += f'  <rect x="{px-74}" y="{py-56}" width="16" height="112" rx="4" fill="url(#wingBlue)" fill-opacity="0.22" stroke="#0369A1" stroke-width="1.2" stroke-dasharray="3,2"/>\n'
    # BOTH HALVES FOLDED TRUE 90° STRAIGHT-PARALLEL FLUSH INSIDE THE 220 mm POD FOOTPRINT! (orange solid)
    s += f'  <rect x="{px-68}" y="{py-14}" width="136" height="12" rx="3" fill="#F97316" fill-opacity="0.94" stroke="#9A3412" stroke-width="1.2"/>\n'
    s += f'  <rect x="{px-68}" y="{py+2}" width="136" height="12" rx="3" fill="#F97316" fill-opacity="0.94" stroke="#9A3412" stroke-width="1.2"/>\n'
    # Sweep arc arrows on both sides into 90° channel
    s += f'  <path d="M {px-54} {py-52} Q {px-10} {py-54} {px+14} {py-20}" fill="none" stroke="#059669" stroke-width="1.8" marker-end="url(#arrGreen)"/>\n'
    s += f'  <path d="M {px-54} {py+52} Q {px-10} {py+54} {px+14} {py+20}" fill="none" stroke="#059669" stroke-width="1.8" marker-end="url(#arrGreen)"/>\n'

    # Front & Rear Center Strut footprints (760 mm tandem spacing!)
    s += f'  <rect x="{px-82}" y="{py-4}" width="18" height="8" rx="2" fill="#FBBF24" stroke="#0F172A" stroke-width="1"/>\n'
    s += f'  <rect x="{px+52}" y="{py-4}" width="18" height="8" rx="2" fill="#FBBF24" stroke="#0F172A" stroke-width="1"/>\n'
    s += f'  <line x1="{px-73}" y1="{py-17}" x2="{px-73}" y2="{py-40}" stroke="#DC2626" stroke-width="2" marker-end="url(#arrRed)"/>\n'
    s += f'  <line x1="{px+61}" y1="{py+17}" x2="{px+61}" y2="{py+40}" stroke="#DC2626" stroke-width="2" marker-end="url(#arrRed)"/>\n'

    s += f'  <line x1="{px-116}" y1="{py+44}" x2="{px-80}" y2="{py+44}" stroke="#DC2626" stroke-width="2.4" marker-end="url(#arrRed)"/>\n'
    s += f'  <text x="{px-120}" y="{py+41}" text-anchor="end" class="warn">Tip Hit</text>\n'
    s += f'  <text x="{px-120}" y="{py+53}" text-anchor="end" class="lbl-sm">(~85 kgf)</text>\n'
    s += f'  <text x="{px-102}" y="{py-28}" text-anchor="end" class="warn">+F_lat</text>\n'
    s += f'  <text x="{px+70}" y="{py+44}" class="warn">-F_lat</text>\n'
    s += f'  <text x="{px+88}" y="{py-42}" text-anchor="middle" class="ok">TRUE 90° FLUSH FOLD!</text>\n'
    s += f'  <text x="{px+88}" y="{py-30}" text-anchor="middle" class="lbl-sm">204 mm inside 220 mm pod</text>\n'
    s += f'  <text x="150" y="{py+67}" text-anchor="middle" class="ok">220 mm Total Width!</text>\n'
    s += f'  <text x="378" y="{py+67}" text-anchor="middle" class="lbl-sm">760 mm Tandem Struts (yaw ≤545 N·m)</text>\n'

    # =========================================================================
    # PANEL B (TOP RIGHT): FULL SIDE PROFILE — DUAL SERVO-PIN SMART DIVIDER!
    # =========================================================================
    s += '  <rect x="548" y="68" width="508" height="346" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>\n'
    s += '  <text x="566" y="92" class="sec">B. Side Profile: Dual Servo-Pin Smart Divider (Struts + Foils)</text>\n'
    s += '  <text x="566" y="109" class="dim">Center shoal (~140 kgf) → Struts kick up • Tip hit (~85 kgf) → Wings fold 90° flush</text>\n'

    s += '  <rect x="560" y="118" width="484" height="236" rx="6" fill="url(#water)"/>\n'
    s += '  <text x="570" y="133" class="lbl-sm">← BOW (Water Flow →)</text>\n'
    s += '  <text x="1034" y="133" text-anchor="end" class="lbl-sm">STERN →</text>\n'

    s += '  <rect x="574" y="140" width="430" height="12" rx="3" fill="url(#alu)" stroke="#334155" stroke-width="1.3"/>\n'
    # Upper Strut Servo-Controlled Variable-Preload Lock Box (gold servo + red roller pin!)
    s += '  <rect x="614" y="152" width="54" height="18" rx="3" fill="#FBBF24" stroke="#92400E" stroke-width="1.2"/>\n'
    s += '  <circle cx="656" cy="161" r="4.6" fill="#DC2626" stroke="#7F1D1D" stroke-width="1.1"/>\n'
    for sx in (668, 890):
        s += f'  <rect x="{sx}" y="152" width="46" height="114" rx="5" fill="url(#carbon)" stroke="#0F172A" stroke-width="1.5"/>\n'
        s += f'  <circle cx="{sx+35}" cy="162" r="4.8" fill="#FBBF24" stroke="#0F172A" stroke-width="1.2"/>\n'
    s += '  <path d="M 718 198 Q 752 194 770 172" fill="none" stroke="#059669" stroke-width="2.2" stroke-dasharray="4,2" marker-end="url(#arrGreen)"/>\n'

    # Flying-Keel Pod with 13 mm Upper Fold Channel + 100% Intact Dry Bay + 12 mm Lower Fold Channel!
    s += '  <rect x="588" y="236" width="398" height="60" rx="24" fill="#334155" fill-opacity="0.22" stroke="#0F172A" stroke-width="1.6"/>\n'
    for sx in (668, 890):
        s += f'  <rect x="{sx-4}" y="236" width="54" height="32" rx="3" fill="#E2E8F0" stroke="#475569" stroke-width="1.1"/>\n'
        s += f'  <rect x="{sx}" y="236" width="46" height="30" rx="3" fill="url(#carbon)" fill-opacity="0.72"/>\n'
        s += f'  <circle cx="{sx+11}" cy="256" r="4.6" fill="#FBBF24" stroke="#0F172A" stroke-width="1.2"/>\n'
    s += '  <polygon points="668,236 652,236 668,218" fill="#F97316" stroke="#9A3412" stroke-width="1.2"/>\n'

    # Tail Propeller (x = 1004)
    s += '  <rect x="986" y="258" width="16" height="16" rx="3" fill="#334155"/>\n'
    s += '  <line x1="1004" y1="234" x2="1004" y2="298" stroke="#0284C7" stroke-width="4.5" stroke-linecap="round"/>\n'

    # UPPER FOLD CHANNEL (13 mm roof recess — Switchblade / Upper Staggerwing folded 90° flush!)
    s += '  <rect x="726" y="236" width="154" height="9" rx="2" fill="#0F766E" stroke="#134E4A" stroke-width="1.2"/>\n'
    # LOWER FOLD CHANNEL (12 mm belly recess — Main Wing folded 90° flush + wet IP68 servo lock!)
    s += '  <rect x="652" y="286" width="276" height="10" rx="3" fill="#F97316" fill-opacity="0.92" stroke="#9A3412" stroke-width="1.3"/>\n'
    s += '  <circle cx="716" cy="291" r="4.2" fill="#DC2626" stroke="#FFFFFF" stroke-width="1"/>\n'
    s += '  <line x1="734" y1="312" x2="882" y2="312" stroke="#059669" stroke-width="2.2" marker-end="url(#arrGreen)"/>\n'

    s += '  <text x="642" y="184" text-anchor="end" class="warn">Strut Servo Pin</text>\n'
    s += '  <text x="642" y="196" text-anchor="end" class="lbl-sm">(0% / ~140 kgf)</text>\n'
    s += '  <text x="776" y="170" class="ok">Top Pin @ TE (+24)</text>\n'
    s += '  <text x="748" y="206" class="ok">1. Shoal → Struts kick aft!</text>\n'
    s += '  <text x="648" y="224" text-anchor="end" class="warn">Line Cutter</text>\n'
    s += '  <text x="802" y="231" text-anchor="middle" class="ok">Upper Channel (13 mm roof)</text>\n'
    s += '  <text x="802" y="276" text-anchor="middle" class="dim">Bottom Pins @ LE (-24)</text>\n'
    s += '  <text x="626" y="324" text-anchor="middle" class="warn">Lower Channel</text>\n'
    s += '  <text x="626" y="336" text-anchor="middle" class="lbl-sm">(12 mm + Servo)</text>\n'
    s += '  <text x="860" y="334" text-anchor="middle" class="warn">2. Folded 90° Flush (220 mm • 179 mm Clear of Prop!)</text>\n'

    s += '  <text x="566" y="376" class="ok">1-Button BEACH MODE: Both Strut &amp; Foil servos drop preload to 0% simultaneously!</text>\n'
    s += '  <text x="566" y="394" class="lbl-sm">Resettable on water in 5 s (zero broken Delrin pins — see Diagram 24 for cam math!).</text>\n'

    # =========================================================================
    # PANEL C (BOTTOM FULL WIDTH): FRONT CROSS-SECTION OF WIDE UPPER & LOWER TRUNNIONS
    # =========================================================================
    s += '  <rect x="24" y="428" width="1032" height="308" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>\n'
    s += '  <text x="42" y="452" class="sec">C. Front Cross-Section: Upper 260 mm T-Head, Lower 180 mm Saddle &amp; 220 mm Fold Channels</text>\n'
    s += '  <text x="42" y="469" class="lbl-sm">Wide full-span axles cut pin bearing loads 8.3× • Upper (13 mm) &amp; Lower (12 mm) channels keep the 26 L dry bay 100% intact!</text>\n'

    cx_c = 345
    s += dim_line(cx_c - 125, 492, cx_c + 125, 492, "250 mm Bearing Span (8.3× Lower Pin Load!)", dy=-6, cls="ok", stroke="#059669", marker="arrGreen")

    s += f'  <rect x="{cx_c-190}" y="504" width="380" height="14" rx="3" fill="url(#carbon)" stroke="#0F172A" stroke-width="1.3"/>\n'
    s += f'  <rect x="{cx_c-148}" y="520" width="296" height="8" rx="2" fill="url(#alu)" stroke="#334155" stroke-width="1.2"/>\n'
    for sd in (-1, 1):
        rx = cx_c + sd * 125
        s += f'  <rect x="{rx-18}" y="528" width="36" height="30" rx="3" fill="url(#alu)" stroke="#334155" stroke-width="1.4"/>\n'
        wx = rx - sd * 21
        s += f'  <rect x="{wx-4}" y="530" width="8" height="26" rx="1.5" fill="#F97316" stroke="#9A3412" stroke-width="1"/>\n'
    s += f'  <path d="M {cx_c-100} 530 L {cx_c+100} 530 L {cx_c+100} 556 L {cx_c+22} 576 L {cx_c+14} 632 L {cx_c+76} 650 L {cx_c+76} 674 L {cx_c-76} 674 L {cx_c-76} 650 L {cx_c-14} 632 L {cx_c-22} 576 L {cx_c-100} 556 Z" fill="url(#carbon)" stroke="#0F172A" stroke-width="1.6"/>\n'
    s += f'  <rect x="{cx_c-146}" y="539" width="292" height="8" rx="3" fill="#FBBF24" stroke="#78350F" stroke-width="1.2"/>\n'

    # Pod cross-section showing Upper 13 mm Channel (teal) + Dry Bay + Lower 12 mm Channel (orange)
    s += f'  <rect x="{cx_c-116}" y="628" width="232" height="68" rx="20" fill="#334155" fill-opacity="0.22" stroke="#0F172A" stroke-width="1.8"/>\n'
    s += f'  <rect x="{cx_c-92}" y="628" width="184" height="9" rx="2" fill="#0F766E" stroke="#134E4A" stroke-width="1"/>\n'
    for sd in (-1, 1):
        bx = cx_c + sd * 88
        s += f'  <rect x="{bx-6}" y="636" width="12" height="54" rx="2" fill="#10B981" stroke="#065F46" stroke-width="1.2"/>\n'
        wx = bx - sd * 9
        s += f'  <rect x="{wx-3}" y="650" width="6" height="22" rx="1" fill="#F97316" stroke="#9A3412" stroke-width="0.9"/>\n'
    s += f'  <rect x="{cx_c-98}" y="656" width="196" height="8" rx="3" fill="#FBBF24" stroke="#78350F" stroke-width="1.2"/>\n'
    s += f'  <rect x="{cx_c-96}" y="688" width="192" height="10" rx="2" fill="#F97316" stroke="#9A3412" stroke-width="1.1"/>\n'

    s += f'  <line x1="{cx_c-148}" y1="594" x2="{cx_c-148}" y2="566" stroke="#0284C7" stroke-width="2.2" marker-end="url(#arrBlue)"/>\n'
    s += f'  <line x1="{cx_c+148}" y1="566" x2="{cx_c+148}" y2="594" stroke="#0284C7" stroke-width="2.2" marker-end="url(#arrBlue)"/>\n'
    s += f'  <text x="{cx_c-154}" y="586" text-anchor="end" class="dim">Push/Pull</text>\n'
    s += f'  <text x="{cx_c-154}" y="599" text-anchor="end" class="lbl-sm">132 kgf/rail</text>\n'
    s += f'  <line x1="{cx_c-180}" y1="660" x2="{cx_c-124}" y2="660" stroke="#DC2626" stroke-width="2.6" marker-end="url(#arrRed)"/>\n'
    s += f'  <text x="{cx_c-184}" y="664" text-anchor="end" class="warn">±F_lat Thrust</text>\n'

    s += dim_line(cx_c - 96, 718, cx_c + 96, 718, "220 mm Folded Width (Fits Between 250 mm Rails!)", dy=12, cls="ok", stroke="#059669", marker="arrGreen")

    s += '  <rect x="588" y="488" width="450" height="226" rx="6" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.2"/>\n'
    s += '  <text x="606" y="512" class="sec">3-Stage Resettable Impact &amp; Beaching System</text>\n'
    s += '  <text x="606" y="536" class="warn">1. True 90° Upper &amp; Lower Fold Channels (220 mm Wide!):</text>\n'
    s += '  <text x="616" y="552" class="lbl-sm">• Main Wing (2×102 mm) nests 90° flush in 12 mm belly channel; Switchblade</text>\n'
    s += '  <text x="616" y="566" class="lbl-sm">  or Upper Staggerwing nests 90° flush in 13 mm roof channel (0 drag!).</text>\n'
    s += '  <text x="606" y="592" class="ok">2. Dual Wet IP68 Servo Variable-Preload Roller Pins:</text>\n'
    s += '  <text x="616" y="608" class="lbl-sm">• Foil pin (~85 kgf tip) &amp; Strut pin (~140 kgf shoal) lock over-center at 0 W,</text>\n'
    s += '  <text x="616" y="622" class="lbl-sm">  drop to 0% for Dyneema fold/beaching, &amp; reset in 5 s (0 broken pins!).</text>\n'
    s += '  <text x="606" y="648" class="dim">3. Wide Full-Span Trunnions + Twin 6 mm Internal Bulkheads:</text>\n'
    s += '  <text x="616" y="664" class="lbl-sm">• Upper 250 mm Ø16 axle + UHMW thrust washers (μ≈0.08) + Lower 180 mm</text>\n'
    s += '  <text x="616" y="678" class="lbl-sm">  pod saddle into twin 6 mm G10 bulkheads carry all roll &amp; side thrust.</text>\n'
    s += '  <text x="616" y="698" class="ok">• Bolt-On Alt: External foil-base 90° knuckles (~350 mm) if pod untouched.</text>\n'

    s += "</svg>\n"
    (OUT_DIR / "21-center-strut-asymmetric-loads.svg").write_text(s)


# -------------------------------------------------------------------------
# DIAGRAM 22: True 90° Upper/Lower Fold Channels + Dyneema Pulley Loop & Dog-Clutch
# -------------------------------------------------------------------------
def gen_22_breakaway_socket_options():
    W, H = 1080, 720
    s = svg_header(
        W, H,
        "22. True 90° Upper & Lower Fold Channels, Dyneema Pulley Loop & Rotating Foil-Base Servo",
        "220 mm Total Folded Width (Fits Between 250 mm Rails!) • 100% Intact 26 L Dry Bay • Active 0.0° Pitch Control!"
    )

    # =========================================================================
    # PANEL A (TOP LEFT): FRONT CROSS-SECTION OF UPPER & LOWER FOLD CHANNELS
    # =========================================================================
    s += '  <rect x="24" y="68" width="510" height="332" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>\n'
    s += '  <text x="42" y="92" class="sec">A. Front Cross-Section: Upper (13 mm) &amp; Lower (12 mm) Channels</text>\n'
    s += '  <text x="42" y="109" class="ok">2×102 mm Main Wing + 2×105 mm Roof Blades nest 90° flush inside 220 mm!</text>\n'

    # Pod cross-section (x = 84..468 -> 384 px = 220 mm; cy = 228)
    cx_a, cy_a = 276, 224
    # Outer Pod Shell (rounded rectangle 360 x 154 px)
    s += f'  <rect x="{cx_a-180}" y="{cy_a-78}" width="360" height="156" rx="34" fill="#F1F5F9" stroke="#0F172A" stroke-width="2.4"/>\n'
    # 13 mm UPPER FOLD CHANNEL recessed flush in roof (Switchblade 2x105 mm OR Upper Staggerwing 2x55 mm!)
    s += f'  <rect x="{cx_a-156}" y="{cy_a-78}" width="312" height="22" rx="4" fill="#CCFBF1" stroke="#0F766E" stroke-width="1.4"/>\n'
    s += f'  <rect x="{cx_a-148}" y="{cy_a-74}" width="140" height="14" rx="3" fill="#0F766E" stroke="#134E4A" stroke-width="1.1"/>\n'
    s += f'  <rect x="{cx_a+8}" y="{cy_a-74}" width="140" height="14" rx="3" fill="#0F766E" stroke="#134E4A" stroke-width="1.1"/>\n'
    s += f'  <text x="{cx_a}" y="{cy_a-88}" text-anchor="middle" class="ok">Upper Fold Channel (13 mm): Switchblade OR Staggerwing (210 mm)</text>\n'

    # 100% INTACT 26 L DRY IP68 BATTERY BAY in center!
    s += f'  <rect x="{cx_a-136}" y="{cy_a-44}" width="272" height="86" rx="8" fill="#10B981" fill-opacity="0.22" stroke="#059669" stroke-width="1.6"/>\n'
    s += f'  <text x="{cx_a}" y="{cy_a-6}" text-anchor="middle" class="sec">100% Intact 26 L Dry IP68 Battery Bay</text>\n'
    s += f'  <text x="{cx_a}" y="{cy_a+12}" text-anchor="middle" class="lbl-sm">(2× Swappable 14 kg Cartridges + VESCs + IMU — ZERO intrusion!)</text>\n'

    # 12 mm LOWER FOLD CHANNEL recessed flush in belly (Main Wing 2x102 mm = 204 mm inside 220 mm!)
    s += f'  <rect x="{cx_a-156}" y="{cy_a+54}" width="312" height="24" rx="4" fill="#FEF3C7" stroke="#D97706" stroke-width="1.4"/>\n'
    # Top/bottom UHMW strips inside overhang bridge
    s += f'  <rect x="{cx_a-148}" y="{cy_a+54}" width="296" height="4" fill="#F97316"/>\n'
    s += f'  <rect x="{cx_a-148}" y="{cy_a+74}" width="296" height="4" fill="#F97316"/>\n'
    # Port & Stbd Main Wing halves nested 90° flush side-by-side + y = ±54 mm golden pivots + center gear mesh!
    s += f'  <rect x="{cx_a-146}" y="{cy_a+59}" width="136" height="14" rx="3" fill="url(#wingBlue)" stroke="#0369A1" stroke-width="1.2"/>\n'
    s += f'  <rect x="{cx_a+10}" y="{cy_a+59}" width="136" height="14" rx="3" fill="url(#wingBlue)" stroke="#0369A1" stroke-width="1.2"/>\n'
    s += f'  <rect x="{cx_a-92}" y="{cy_a+50}" width="10" height="32" rx="2" fill="#FBBF24" stroke="#78350F" stroke-width="1.2"/>\n'
    s += f'  <rect x="{cx_a+82}" y="{cy_a+50}" width="10" height="32" rx="2" fill="#FBBF24" stroke="#78350F" stroke-width="1.2"/>\n'
    s += f'  <rect x="{cx_a-12}" y="{cy_a+60}" width="24" height="12" rx="2" fill="url(#alu)" stroke="#334155" stroke-width="1.1"/>\n'
    s += f'  <text x="{cx_a}" y="{cy_a+98}" text-anchor="middle" class="warn">Lower Fold Channel (12 mm): Main Wing 2×102 mm (Pivots @ y = ±54 mm)</text>\n'

    # Dimension & bottom summary notes
    s += '  <text x="42" y="346" class="ok">40 mm Inboard Overhang Roots: Carry 100% lift/roll in compression (~35 MPa, &gt;10×!).</text>\n'
    s += '  <text x="42" y="366" class="lbl-sm">Zero Side-Wall Cutouts: Unlike hollowing the pod sides, top/bottom channels keep 100% dry bay!</text>\n'
    s += '  <text x="42" y="384" class="dim">Total Pod Height: ~95–105 mm (vs 80 mm fixed) • Zero external hubs = ~0 lbf extra drag!</text>\n'

    # =========================================================================
    # PANEL B (TOP RIGHT): CLOSED-LOOP DYNEEMA PULLEY DEPLOY/FOLD SYSTEM
    # =========================================================================
    s += '  <rect x="550" y="68" width="506" height="332" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>\n'
    s += '  <text x="568" y="92" class="sec">B. Closed-Loop Dyneema Pulley Deploy/Fold (Zero Sweep Motors!)</text>\n'
    s += '  <text x="568" y="109" class="dim">One Ø2.5 mm SK78 loop wraps a single belly drum — drives BOTH meshed wings 0° ↔ 90° (&lt;8 kgf)!</text>\n'

    # --- SUB-BOX B1 (LEFT): SIDE VIEW — COCKPIT TO POD COAXIAL ROUTING ---
    s += '  <rect x="562" y="118" width="222" height="202" rx="6" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>\n'
    s += '  <text x="572" y="133" class="ok">B1. Side View: Coaxial Strut Routing</text>\n'

    # Stacked dry-cockpit handles (zero line crossing over buttons!) above Hard Deck bar
    s += '  <rect x="572" y="139" width="54" height="13" rx="3" fill="#10B981" stroke="#065F46" stroke-width="1.1"/>\n'
    s += '  <text x="599" y="148" text-anchor="middle" style="font-size:7.6px;fill:#FFFFFF;font-weight:700;">← DEPLOY</text>\n'
    s += '  <rect x="572" y="155" width="54" height="13" rx="3" fill="#F97316" stroke="#9A3412" stroke-width="1.1"/>\n'
    s += '  <text x="599" y="164" text-anchor="middle" style="font-size:7.6px;fill:#FFFFFF;font-weight:700;">← FOLD</text>\n'
    # Cockpit Hard Deck bar (y = 171..177)
    s += '  <rect x="572" y="171" width="198" height="6" rx="2" fill="#475569" stroke="#0F172A" stroke-width="1"/>\n'

    # Ghosted 86.5° folded strut from exact same top hinge pin (showing constant length!)
    s += '  <line x1="714" y1="184" x2="774" y2="192" stroke="#94A3B8" stroke-width="9" stroke-linecap="round" stroke-dasharray="4,3"/>\n'
    s += '  <path d="M 728 224 A 34 34 0 0 0 750 198" fill="none" stroke="#64748B" stroke-width="1.3" stroke-dasharray="3,2"/>\n'
    s += '  <text x="764" y="216" text-anchor="middle" style="font-size:7.6px;fill:#475569;font-weight:700;">86.5°</text>\n'
    s += '  <text x="764" y="226" text-anchor="middle" style="font-size:7.2px;fill:#475569;">fold</text>\n'

    # Vertical Deployed Strut (x = 706..722, y = 184..278)
    s += '  <rect x="706" y="184" width="16" height="94" rx="3" fill="url(#carbon)" stroke="#0F172A" stroke-width="1.3"/>\n'
    # Pod Belly Channel strip at strut bottom
    s += '  <rect x="688" y="278" width="88" height="22" rx="4" fill="#FEF3C7" stroke="#D97706" stroke-width="1.2"/>\n'

    # Top & Bottom Coaxial Pulleys centered directly on strut hinge axles!
    s += '  <circle cx="714" cy="184" r="9" fill="#FBBF24" stroke="#78350F" stroke-width="1.3"/>\n'
    s += '  <circle cx="714" cy="184" r="2.6" fill="#0F172A"/>\n'
    s += '  <circle cx="714" cy="278" r="9" fill="#FBBF24" stroke="#78350F" stroke-width="1.3"/>\n'
    s += '  <circle cx="714" cy="278" r="2.6" fill="#0F172A"/>\n'

    # Continuous Green (DEPLOY) & Orange (FOLD) lines: handles -> top coaxial pulley -> strut TE groove -> bottom coaxial pulley -> right to B2!
    s += '  <path d="M 626 145 L 708 145 L 708 284 L 774 284" fill="none" stroke="#059669" stroke-width="2.1" marker-end="url(#arrGreen)"/>\n'
    s += '  <path d="M 626 161 L 720 161 L 720 294 L 774 294" fill="none" stroke="#F97316" stroke-width="2.1" stroke-dasharray="4,2" marker-end="url(#arrRed)"/>\n'

    # Clear callouts on left side of B1
    s += '  <text x="696" y="191" text-anchor="end" class="lbl-sm">Top Coaxial Pulley</text>\n'
    s += '  <text x="696" y="202" text-anchor="end" style="font-size:7.6px;fill:#64748B;">(on strut hinge pin)</text>\n'
    s += '  <text x="696" y="228" text-anchor="end" class="dim">2 lines inside</text>\n'
    s += '  <text x="696" y="239" text-anchor="end" class="lbl-sm">strut TE groove</text>\n'
    s += '  <text x="696" y="266" text-anchor="end" class="lbl-sm">Bottom Coaxial</text>\n'
    s += '  <text x="696" y="276" text-anchor="end" style="font-size:7.6px;fill:#64748B;">Pulley (constant L!)</text>\n'
    s += '  <text x="673" y="313" text-anchor="middle" class="warn">Lines enter Belly Drum → (B2)</text>\n'

    # --- SUB-BOX B2 (RIGHT): BOTTOM-UP VIEW — BELLY DRUM & MESHED GEARS ---
    s += '  <rect x="790" y="118" width="256" height="202" rx="6" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>\n'
    s += '  <text x="800" y="133" class="warn">B2. Bottom-Up: Belly Drum &amp; Wings</text>\n'

    # Pod Belly Channel outline (x = 810..1034, y = 178..258; centerline y = 218)
    s += '  <rect x="810" y="178" width="224" height="80" rx="22" fill="#FEF3C7" fill-opacity="0.72" stroke="#D97706" stroke-width="1.4"/>\n'
    s += '  <text x="816" y="173" style="font-size:7.4px;fill:#64748B;font-weight:700;">← BOW</text>\n'
    s += '  <text x="1030" y="173" text-anchor="end" style="font-size:7.4px;fill:#64748B;font-weight:700;">STERN (90° AFT) →</text>\n'

    # DEPLOYED 0° WINGS (Blue, sticking UP for Port & DOWN for Stbd!)
    s += '  <rect x="862" y="140" width="24" height="58" rx="4" fill="url(#wingBlue)" stroke="#0369A1" stroke-width="1.3"/>\n'
    s += '  <rect x="862" y="238" width="24" height="58" rx="4" fill="url(#wingBlue)" stroke="#0369A1" stroke-width="1.3"/>\n'
    # Cleanly placed labels on LEFT of top blue wing (zero overlap with green arc!)
    s += '  <text x="856" y="150" text-anchor="end" class="ok">0° Deployed</text>\n'
    s += '  <text x="856" y="160" text-anchor="end" style="font-size:7.6px;fill:#047857;">(Pull Green)</text>\n'

    # FOLDED 90° WINGS (Dashed Orange, lying straight right inside 220 mm belly channel!)
    s += '  <rect x="882" y="186" width="110" height="22" rx="4" fill="#F97316" fill-opacity="0.32" stroke="#EA580C" stroke-width="1.4" stroke-dasharray="4,2"/>\n'
    s += '  <rect x="882" y="228" width="110" height="22" rx="4" fill="#F97316" fill-opacity="0.32" stroke="#EA580C" stroke-width="1.4" stroke-dasharray="4,2"/>\n'
    s += '  <text x="944" y="200" text-anchor="middle" style="font-size:8px;fill:#9A3412;font-weight:700;">90° Folded</text>\n'
    s += '  <text x="944" y="242" text-anchor="middle" style="font-size:8px;fill:#9A3412;font-weight:700;">(Pull Orange)</text>\n'

    # Meshed 90° Stainless Root Gears (Port cy=198, Stbd cy=238, r=19 — meshing right at y=218!)
    s += '  <circle cx="874" cy="198" r="19" fill="url(#alu)" stroke="#0F172A" stroke-width="1.5" stroke-dasharray="4,2"/>\n'
    s += '  <circle cx="874" cy="238" r="19" fill="url(#alu)" stroke="#0F172A" stroke-width="1.5" stroke-dasharray="4,2"/>\n'
    # Grooved Pulley Drum mounted directly on Port gear hub (r = 11.5, gold!)
    s += '  <circle cx="874" cy="198" r="11.5" fill="#FBBF24" stroke="#78350F" stroke-width="1.5"/>\n'
    # Visible continuous loop wrapping right around the Port pulley drum!
    s += '  <path d="M 800 186.5 L 874 186.5 A 11.5 11.5 0 0 1 885.5 198" fill="none" stroke="#059669" stroke-width="2.3"/>\n'
    s += '  <path d="M 885.5 198 A 11.5 11.5 0 0 1 874 209.5 L 800 209.5" fill="none" stroke="#F97316" stroke-width="2.3" stroke-dasharray="4,2"/>\n'
    # Crisp pull arrowheads at left entry inside B2
    s += '  <line x1="824" y1="186.5" x2="800" y2="186.5" stroke="#059669" stroke-width="2.3" marker-end="url(#arrGreen)"/>\n'
    s += '  <line x1="824" y1="209.5" x2="800" y2="209.5" stroke="#F97316" stroke-width="2.3" marker-end="url(#arrRed)"/>\n'
    s += '  <circle cx="874" cy="198" r="4" fill="#0F172A"/>\n'
    s += '  <circle cx="874" cy="238" r="4.5" fill="#FBBF24" stroke="#0F172A" stroke-width="1.1"/>\n'

    # Curved motion arrows showing simultaneous symmetric wing swing (completely clear of all text!)
    s += '  <path d="M 964 176 A 72 72 0 0 0 894 146" fill="none" stroke="#059669" stroke-width="1.9" marker-end="url(#arrGreen)"/>\n'
    s += '  <text x="952" y="152" class="ok">DEPLOY</text>\n'
    s += '  <path d="M 894 288 A 72 72 0 0 0 964 260" fill="none" stroke="#F97316" stroke-width="1.9" marker-end="url(#arrRed)"/>\n'
    s += '  <text x="952" y="286" class="warn">FOLD</text>\n'

    # Red Servo Pin behind gear mesh + Rear 90° Ball Detent!
    s += '  <circle cx="902" cy="218" r="5.5" fill="#DC2626" stroke="#FFFFFF" stroke-width="1.1"/>\n'
    s += '  <text x="911" y="221" style="font-size:7.6px;fill:#B91C1C;font-weight:700;">Servo Pin</text>\n'
    s += '  <circle cx="998" cy="218" r="4.5" fill="#0F766E" stroke="#FFFFFF" stroke-width="1"/>\n'
    s += '  <text x="1005" y="221" style="font-size:7.4px;fill:#0F766E;font-weight:700;">Detent</text>\n'

    s += '  <text x="918" y="313" text-anchor="middle" class="dim">1 Drum + Meshed Gears = Symmetric Swing!</text>\n'

    # Crisp 3-step summary below Panel B sub-boxes
    s += '  <text x="568" y="338" class="ok">1. Pull Green (DEPLOY, &lt;8 kgf): Turns Port drum CCW + Stbd gear CW → wings lock at 0°!</text>\n'
    s += '  <text x="568" y="356" class="warn">2. Drop Servo Pin to 0% &amp; Pull Orange (FOLD): Reverses drum → wings click 90° flat!</text>\n'
    s += '  <text x="568" y="374" class="dim">3. Coaxial Hinge Pulleys: Line length stays constant as struts fold 0° ↔ 86.5° (0 slack!).</text>\n'
    s += '  <text x="568" y="391" class="lbl-sm">Sand/saltwater-proof Ø2.5 mm SK78 Dyneema (700 kg!) + open Delrin sheaves • Zero motors!</text>\n'

    # =========================================================================
    # PANEL C (BOTTOM FULL WIDTH): EMBEDDED ROTATING WET IP68 FOIL-BASE SERVO (PRECISE 0.0° CONTROL!)
    # =========================================================================
    s += '  <rect x="24" y="414" width="1032" height="284" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>\n'
    s += '  <text x="42" y="438" class="sec">C. Active Flaperon 90° Fold: Embedded Rotating Wet IP68 Foil-Base Servo (Direct-Drive or Leveraged)</text>\n'
    s += '  <text x="42" y="455" class="ok">Servo rides INSIDE the folding root carrier &amp; rotates 90° WITH the blade — exact 0.0° flat-lock before folding (never relies on water flow!)</text>\n'

    # Left Sub-Box (C1): DEPLOYED (0° ACTIVE FLIGHT — SERVO EMBEDDED IN ROOT CARRIER!)
    s += '  <rect x="38" y="468" width="484" height="214" rx="6" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>\n'
    s += '  <text x="50" y="486" class="ok">C1. Deployed (0° Flight): Embedded IP68 Servo Direct-Drives (or Levers) Pitch Spar</text>\n'

    y_c = 576
    # Stationary Dry Pod Wall + Static Bulkhead Cable Gland (ZERO moving rotary O-rings!)
    s += f'  <rect x="58" y="{y_c-66}" width="76" height="132" rx="8" fill="#E2E8F0" stroke="#475569" stroke-width="1.6"/>\n'
    s += f'  <text x="96" y="{y_c-46}" text-anchor="middle" class="lbl-sm">Dry Pod</text>\n'
    s += f'  <text x="96" y="{y_c-34}" text-anchor="middle" style="font-size:7.6px;fill:#475569;">(ESP32/IMU)</text>\n'
    # Static IP68 wire gland in pod wall
    s += f'  <rect x="128" y="{y_c-12}" width="14" height="24" rx="3" fill="#0F766E" stroke="#134E4A" stroke-width="1.2"/>\n'
    s += f'  <text x="104" y="{y_c+28}" text-anchor="middle" style="font-size:7.5px;fill:#0F766E;font-weight:700;">Static Gland</text>\n'
    s += f'  <text x="104" y="{y_c+38}" text-anchor="middle" style="font-size:7.2px;fill:#64748B;">(0 rotary seals!)</text>\n'

    # Rotating Root Carrier Block pivoted on Ø10 mm vertical sweep pin (houses Wet IP68 Servo!)
    s += f'  <rect x="166" y="{y_c-28}" width="114" height="62" rx="8" fill="#FEF3C7" stroke="#D97706" stroke-width="1.6"/>\n'
    # Vertical Ø10 mm Sweep Pivot Pin at inboard edge of carrier
    s += f'  <circle cx="182" cy="{y_c+18}" r="6.5" fill="#10B981" stroke="#065F46" stroke-width="1.4"/>\n'
    # Embedded Wet IP68 Low-Profile Servo (20 mm flat direct-drive OR 15 mm leveraged wing servo!)
    s += f'  <rect x="196" y="{y_c-21}" width="58" height="38" rx="4" fill="#FBBF24" stroke="#92400E" stroke-width="1.4"/>\n'
    s += f'  <text x="225" y="{y_c-4}" text-anchor="middle" style="font-size:8px;fill:#0F172A;font-weight:700;">Wet IP68</text>\n'
    s += f'  <text x="225" y="{y_c+8}" text-anchor="middle" style="font-size:7.6px;fill:#78350F;font-weight:700;">Servo</text>\n'
    # Direct-drive Ø8 mm splined shaft / leveraged horn straight into flaperon root spar!
    s += f'  <rect x="254" y="{y_c-6}" width="38" height="10" rx="2" fill="#DC2626"/>\n'
    # Flexible 3-wire silicone servo cable curving smoothly from static gland around pivot to rotating servo!
    s += f'  <path d="M 142 {y_c} Q 162 {y_c-26} 196 {y_c-8}" fill="none" stroke="#0284C7" stroke-width="2.4" stroke-dasharray="4,2"/>\n'
    s += f'  <text x="190" y="{y_c-36}" text-anchor="middle" class="dim">3-Wire Flex Loop</text>\n'

    # Active Flaperon Blade attached to Rotating Root Carrier
    s += f'  <rect x="280" y="{y_c-24}" width="218" height="54" rx="6" fill="url(#wingBlue)" stroke="#0369A1" stroke-width="1.5"/>\n'
    s += f'  <text x="389" y="{y_c}" text-anchor="middle" style="font-size:10px;fill:#FFFFFF;font-weight:700;">Active Flaperon (Exact Closed-Loop Pitch)</text>\n'
    s += f'  <text x="389" y="{y_c+15}" text-anchor="middle" style="font-size:8.4px;fill:#E0F2FE;">±15° STOL / ±3° roll • Direct or 1.5:1 horn!</text>\n'
    s += f'  <text x="228" y="{y_c+54}" text-anchor="middle" class="ok">Ø10 mm Vertical Sweep Pivot</text>\n'
    s += '  <text x="50" y="670" class="lbl-sm">Zero dog-clutch, zero dynamic O-rings — servo &amp; blade form 1 rigid watertight assembly!</text>\n'

    # Right Sub-Box (C2): FOLDED 90° STRAIGHT AFT (SERVO ROTATES 90° WITH BLADE AT EXACT 0.0°!)
    s += '  <rect x="546" y="468" width="494" height="214" rx="6" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>\n'
    s += '  <text x="558" y="486" class="warn">C2. Folded 90° Straight Aft: Commanded 0.0° Flat-Lock (Servo Swings WITH Blade!)</text>\n'

    # Dry Pod Wall + Static Gland
    s += f'  <rect x="566" y="{y_c-66}" width="64" height="132" rx="8" fill="#E2E8F0" stroke="#475569" stroke-width="1.6"/>\n'
    s += f'  <rect x="624" y="{y_c-12}" width="12" height="24" rx="3" fill="#0F766E" stroke="#134E4A" stroke-width="1.2"/>\n'

    # Entire Rotating Root Carrier + Embedded Servo + Flaperon pivoted 90° STRAIGHT AFT together!
    s += f'  <rect x="668" y="{y_c-22}" width="54" height="58" rx="7" fill="#FEF3C7" stroke="#D97706" stroke-width="1.5"/>\n'
    s += f'  <circle cx="680" cy="{y_c-10}" r="6" fill="#10B981" stroke="#065F46" stroke-width="1.4"/>\n'
    s += f'  <rect x="684" y="{y_c-2}" width="32" height="32" rx="4" fill="#FBBF24" stroke="#92400E" stroke-width="1.3"/>\n'
    s += f'  <text x="700" y="{y_c+17}" text-anchor="middle" style="font-size:7px;fill:#0F172A;font-weight:700;">IP68</text>\n'
    # Flexible 3-wire silicone cable flexing gently 90° around the vertical sweep pivot!
    s += f'  <path d="M 636 {y_c} Q 656 {y_c+14} 684 {y_c+14}" fill="none" stroke="#0284C7" stroke-width="2.4" stroke-dasharray="4,2"/>\n'
    # Folded Orange Blade locked at exact 0.0° flat inside the 220 mm roof channel!
    s += f'  <rect x="676" y="{y_c+34}" width="42" height="60" rx="5" fill="#F97316" stroke="#9A3412" stroke-width="1.5"/>\n'
    s += f'  <text x="697" y="{y_c+67}" text-anchor="middle" style="font-size:7.6px;fill:#FFFFFF;font-weight:700;">0.0°</text>\n'
    s += f'  <path d="M 730 {y_c-12} Q 758 {y_c+8} 736 {y_c+48}" fill="none" stroke="#059669" stroke-width="2.3" marker-end="url(#arrGreen)"/>\n'

    s += '  <text x="768" y="520" class="ok">1. Exact 0.0° Flat-Lock Before Folding:</text>\n'
    s += '  <text x="778" y="534" class="lbl-sm">Controller commands exact 0.0° flat —</text>\n'
    s += '  <text x="778" y="547" class="lbl-sm">cross-currents/waves NEVER jam the slot!</text>\n'
    s += '  <text x="768" y="569" class="dim">2. Zero Clutch Misalignment or Wear:</text>\n'
    s += '  <text x="778" y="583" class="lbl-sm">Servo stays splined/levered at all angles;</text>\n'
    s += '  <text x="778" y="596" class="lbl-sm">only a soft 3-wire pigtail flexes 90°!</text>\n'
    s += '  <text x="768" y="618" class="warn">3. Compact Packaging Inside 220 mm Pod:</text>\n'
    s += '  <text x="778" y="632" class="lbl-sm">20 mm direct-drive (or 15 mm levered)</text>\n'
    s += '  <text x="778" y="645" class="lbl-sm">fits inside 60 mm chord (2×60 = 120 mm!).</text>\n'
    s += '  <text x="778" y="666" class="ok">Impact safe: whole carrier sweeps aft!</text>\n'

    s += "</svg>\n"
    (OUT_DIR / "22-breakaway-socket-options.svg").write_text(s)


# -------------------------------------------------------------------------
# DIAGRAM 23: True 90° Upper/Lower Channels — All 3 Wing Tracks & 220 mm Folded Dart
# -------------------------------------------------------------------------
def gen_23_breakaway_deployed_flaperons():
    W, H = 1080, 580
    s = svg_header(
        W, H,
        "23. True 90° Upper & Lower Fold Channels: All 3 Wing Tracks & 220 mm Beaching Dart",
        "Zero Collision Across Switchblade / Upper Staggerwing (Roof) & Main Wing (Belly) — Fits Even Between 250 mm Rails!"
    )

    # =========================================================================
    # PANEL A (LEFT): SIDE PROFILE OF UPPER & LOWER 90° FOLD CHANNELS
    # =========================================================================
    s += '  <rect x="24" y="68" width="508" height="486" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>\n'
    s += '  <text x="42" y="92" class="sec">A. Side Profile: Upper (13 mm) &amp; Lower (12 mm) Fold Channels</text>\n'
    s += '  <text x="42" y="109" class="ok">Every wing folds 90° straight aft in its own dedicated channel — zero clash!</text>\n'
    s += '  <rect x="36" y="118" width="484" height="292" rx="6" fill="url(#water)"/>\n'
    s += '  <text x="46" y="134" class="lbl-sm">← BOW (95–105 mm Pod w/ 100% Intact 26 L Dry Bay)</text>\n'
    s += '  <text x="510" y="134" text-anchor="end" class="lbl-sm">STERN →</text>\n'

    cy = 248
    s += f'  <rect x="52" y="{cy-54}" width="404" height="108" rx="38" fill="#334155" fill-opacity="0.16" stroke="#0F172A" stroke-width="1.8"/>\n'
    # Tail prop at x = 474
    s += f'  <rect x="456" y="{cy-14}" width="16" height="28" rx="3" fill="#334155"/>\n'
    s += f'  <line x1="474" y1="{cy-60}" x2="474" y2="{cy+60}" stroke="#0284C7" stroke-width="4.5" stroke-linecap="round"/>\n'

    # UPPER CHANNEL (13 mm Roof Recess): Switchblade (2x105 mm) OR Upper Staggerwing Flaperons (2x55 mm)
    s += f'  <rect x="116" y="{cy-56}" width="246" height="12" rx="3" fill="#0F766E" stroke="#134E4A" stroke-width="1.4"/>\n'
    s += f'  <text x="242" y="{cy-66}" text-anchor="middle" class="ok">Upper Fold Channel (13 mm Roof): Switchblade OR Staggerwing</text>\n'

    # 100% INTACT 26 L DRY BATTERY BAY in center
    s += f'  <rect x="116" y="{cy-32}" width="270" height="62" rx="8" fill="#10B981" fill-opacity="0.22" stroke="#059669" stroke-width="1.4" stroke-dasharray="4,2"/>\n'
    s += f'  <text x="251" y="{cy+4}" text-anchor="middle" class="sec">100% Intact 26 L Dry Bay</text>\n'

    # LOWER CHANNEL (12 mm Belly Recess): Linked-Fold Main Wing (2x102 mm = 204 mm side-by-side!)
    s += f'  <rect x="128" y="{cy+42}" width="252" height="12" rx="3" fill="url(#wingBlue)" stroke="#0369A1" stroke-width="1.5"/>\n'
    s += f'  <text x="254" y="{cy+72}" text-anchor="middle" class="dim">Lower Fold Channel (12 mm Belly): Main Wing 90° Flush!</text>\n'
    s += f'  <text x="254" y="{cy+86}" text-anchor="middle" class="lbl-sm">1.55 m (AR 14) tips stop 179 mm ahead of tail prop</text>\n'

    # Vertical separation dimension callout
    s += dim_line(92, cy - 48, 92, cy + 48, "80 mm", dx=-24, dy=4, cls="ok", stroke="#059669", marker="arrGreen")

    s += '  <text x="42" y="436" class="ok">1. Primary Approach: Upper Channel (Roof) + Lower Channel (Belly):</text>\n'
    s += '  <text x="52" y="454" class="lbl-sm">• 80 mm vertical separation across the dry bay → zero collision at every angle!</text>\n'
    s += '  <text x="52" y="472" class="lbl-sm">• Works identically for Flush Switchblade OR Fixed Upper Staggerwing flaperons.</text>\n'
    s += '  <text x="42" y="496" class="dim">2. Optional Morphing STOL Mode (DOWN ~5 s Takeoff):</text>\n'
    s += '  <text x="52" y="514" class="lbl-sm">• Embedded rotating IP68 servo commands exact 0.0° flat to sweep cleanly below Main Wing.</text>\n'

    # =========================================================================
    # PANEL B (RIGHT): TOP-DOWN 220 mm FOLDED DART INSIDE 250 mm RAILS & 600 mm TUNNEL!
    # =========================================================================
    s += '  <rect x="548" y="68" width="508" height="486" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>\n'
    s += '  <text x="566" y="92" class="sec">B. Top-Down: True 90° 220 mm Dart (Fits Between 250 mm Rails!)</text>\n'
    s += '  <text x="566" y="109" class="ok">ZERO overhang outside pod — 190 mm clear per side inside 600 mm tunnel!</text>\n'
    s += '  <rect x="560" y="118" width="484" height="292" rx="6" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>\n'

    my = 264
    # Navigator 300 600 mm Inside Tunnel Walls
    s += '  <rect x="566" y="126" width="472" height="26" rx="12" fill="#CBD5E1" stroke="#64748B" stroke-width="1.3"/>\n'
    s += '  <rect x="566" y="376" width="472" height="26" rx="12" fill="#CBD5E1" stroke="#64748B" stroke-width="1.3"/>\n'
    s += '  <text x="802" y="143" text-anchor="middle" class="lbl-sm">Port Ø460 mm Inflatable Tube Edge</text>\n'
    s += '  <text x="802" y="393" text-anchor="middle" class="lbl-sm">Starboard Ø460 mm Inflatable Tube Edge</text>\n'

    # Dashed 250 mm Under-Hull Twin Rails showing the 220 mm folded dart fits INSIDE the rails!
    s += f'  <line x1="590" y1="{my-50}" x2="980" y2="{my-50}" stroke="#94A3B8" stroke-width="2" stroke-dasharray="6,3"/>\n'
    s += f'  <line x1="590" y1="{my+50}" x2="980" y2="{my+50}" stroke="#94A3B8" stroke-width="2" stroke-dasharray="6,3"/>\n'
    s += f'  <text x="720" y="{my-56}" text-anchor="middle" class="lbl-sm">250 mm Under-Hull Twin Rails (Pod tucks between!)</text>\n'

    # 220 mm Flying-Keel Pod (height 84 px = 220 mm!)
    s += f'  <rect x="604" y="{my-42}" width="350" height="84" rx="36" fill="url(#carbon)" stroke="#0F172A" stroke-width="1.6"/>\n'
    # BOTH Main Wing Halves (2x102 mm = 204 mm, orange) AND Roof Blades (teal) folded TRUE 90° FLUSH INSIDE the 220 mm pod!
    s += f'  <rect x="650" y="{my-36}" width="246" height="32" rx="4" fill="#F97316" fill-opacity="0.92" stroke="#9A3412" stroke-width="1.3"/>\n'
    s += f'  <rect x="650" y="{my+4}" width="246" height="32" rx="4" fill="#F97316" fill-opacity="0.92" stroke="#9A3412" stroke-width="1.3"/>\n'
    # Inner teal overlay showing Upper Channel Roof Blades nested right above!
    s += f'  <rect x="666" y="{my-28}" width="176" height="22" rx="3" fill="#0F766E" fill-opacity="0.88" stroke="#134E4A" stroke-width="1.1"/>\n'
    s += f'  <rect x="666" y="{my+6}" width="176" height="22" rx="3" fill="#0F766E" fill-opacity="0.88" stroke="#134E4A" stroke-width="1.1"/>\n'
    # Twin y = ±54 mm golden root pivots
    s += f'  <circle cx="662" cy="{my-20}" r="4.5" fill="#FBBF24" stroke="#0F172A" stroke-width="1"/>\n'
    s += f'  <circle cx="662" cy="{my+20}" r="4.5" fill="#FBBF24" stroke="#0F172A" stroke-width="1"/>\n'

    # Tail Prop at x = 974
    s += f'  <line x1="974" y1="{my-34}" x2="974" y2="{my+34}" stroke="#0284C7" stroke-width="4.5" stroke-linecap="round"/>\n'
    s += f'  <text x="1008" y="{my+4}" text-anchor="middle" class="dim">Prop</text>\n'

    # Crisp non-overlapping dimensions
    s += dim_line(586, 152, 586, 376, "600 mm", dx=26, dy=-82, cls="dim")
    s += dim_line(916, my - 42, 916, my + 42, "220 mm!", dx=30, dy=64, cls="ok", stroke="#059669", marker="arrGreen")
    s += dim_line(896, my - 72, 974, my - 72, "179 mm clear!", dy=-6, cls="ok", stroke="#059669", marker="arrGreen")

    s += '  <text x="566" y="436" class="ok">Why True 90° Upper &amp; Lower Fold Channels Win:</text>\n'
    s += '  <text x="576" y="454" class="lbl-sm">• Narrowest Possible Fold: 220 mm total width (zero wider than pod itself!).</text>\n'
    s += '  <text x="576" y="472" class="lbl-sm">• Fits cleanly BETWEEN the 250 mm rails on 86.5° retraction (+5.5" sand clear).</text>\n'
    s += '  <text x="576" y="490" class="lbl-sm">• Zero external hubs = ~0 lbf interference drag at 15.5–22 kn cruise!</text>\n'
    s += '  <text x="576" y="508" class="lbl-sm">• 5-Second Water Reset: Pull Dyneema Deploy line → servo roller clicks locked!</text>\n'

    s += "</svg>\n"
    (OUT_DIR / "23-breakaway-deployed-flaperons.svg").write_text(s)


# -------------------------------------------------------------------------
# DIAGRAM 24: Wet IP68 Servo-Controlled Variable-Preload Roller Pins (Foils & Struts)
# -------------------------------------------------------------------------
def gen_24_servo_preload_pins():
    W, H = 1080, 620
    s = svg_header(
        W, H,
        "24. Wet IP68 Servo-Controlled Variable-Preload Roller Pins (Foils & Struts)",
        "100% Resettable Ski-Binding Cam-and-Rocker Lock: 0% Fold/Deploy • 50% Reef Mode • 100% Over-Center Cruise (0 W Hold!)"
    )

    # =========================================================================
    # PANEL A (LEFT): FOIL LOCK MECHANISM (LOWER & UPPER CHANNELS — ~85 kgf TIP)
    # =========================================================================
    s += '  <rect x="24" y="68" width="508" height="528" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>\n'
    s += '  <text x="42" y="92" class="sec">A. Foil Channel Lock: Over-Center Cam + 3.5:1 Rocker + 20° Roller</text>\n'
    s += '  <text x="42" y="109" class="ok">18× lever reduction lets a 75 kg·cm IP68 servo hold ~85 kgf tip / ~170 kgf center!</text>\n'
    s += '  <rect x="36" y="118" width="484" height="252" rx="6" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>\n'

    # 1. Wet IP68 Billet Servo (gold) + 12 mm Eccentric Over-Center Cam at top-left (x = 96..176, y = 138..184)
    s += '  <rect x="74" y="138" width="92" height="44" rx="5" fill="#FBBF24" stroke="#92400E" stroke-width="1.5"/>\n'
    s += '  <text x="120" y="158" text-anchor="middle" style="font-size:8.8px;fill:#0F172A;font-weight:700;">Wet IP68 Servo</text>\n'
    s += '  <text x="120" y="170" text-anchor="middle" style="font-size:7.8px;fill:#451A03;">75 kg·cm (0 W TDC)</text>\n'
    # Eccentric Cam disc pushing DOWN onto Grease-Booted 316 SS Die Spring (x = 120, y = 196)
    s += '  <circle cx="120" cy="196" r="14" fill="#475569" stroke="#0F172A" stroke-width="1.4"/>\n'
    s += '  <circle cx="120" cy="191" r="4" fill="#FBBF24"/>\n'

    # 2. Grease-Booted 316 SS Die Spring (37 kgf @ 100%, sealed inside green silicone sand boot! y = 210..268)
    s += '  <rect x="104" y="210" width="32" height="54" rx="6" fill="#10B981" fill-opacity="0.28" stroke="#059669" stroke-width="1.6"/>\n'
    s += '  <path d="M 110 216 L 130 223 L 110 230 L 130 237 L 110 244 L 130 251 L 110 258" fill="none" stroke="#334155" stroke-width="2.2"/>\n'

    # 3. 3.5:1 Stainless Rocker Lever (70 mm spring arm left -> fulcrum @ x=298 -> 20 mm roller pin arm right @ x=356!)
    s += '  <rect x="108" y="264" width="262" height="12" rx="4" fill="url(#alu)" stroke="#0F172A" stroke-width="1.5"/>\n'
    # Fulcrum pivot pin at x = 296 (creating 3.5:1 leverage: 188 px left vs 54 px right!)
    s += '  <polygon points="296,276 284,296 308,296" fill="#334155" stroke="#0F172A" stroke-width="1.2"/>\n'
    s += '  <circle cx="296" cy="270" r="5" fill="#FBBF24" stroke="#0F172A" stroke-width="1.2"/>\n'

    # 4. Hardened 316 SS Roller Pin (y = 276..314) pressed DOWN into 20° Detent Notch on 110 mm Wing Slider Lug!
    s += '  <rect x="348" y="276" width="16" height="28" rx="3" fill="#475569" stroke="#0F172A" stroke-width="1.3"/>\n'
    s += '  <circle cx="356" cy="308" r="8" fill="#DC2626" stroke="#7F1D1D" stroke-width="1.4"/>\n'

    # 5. Wing Gear Slider Lug (110 mm arm, blue) with steep 20° hardened detent notch!
    s += '  <polygon points="184,316 336,316 346,326 366,326 376,316 462,316 462,344 184,344" fill="url(#wingBlue)" stroke="#0369A1" stroke-width="1.5"/>\n'
    s += '  <text x="270" y="334" text-anchor="middle" style="font-size:8.8px;fill:#FFFFFF;font-weight:700;">110 mm Wing Gear Slider Lug</text>\n'
    # Aft drag arrow on impact
    s += '  <line x1="466" y1="330" x2="508" y2="330" stroke="#DC2626" stroke-width="2.6" marker-end="url(#arrRed)"/>\n'
    # Upward cam-out force arrow at roller
    s += '  <line x1="382" y1="308" x2="382" y2="278" stroke="#059669" stroke-width="2.2" marker-end="url(#arrGreen)"/>\n'

    # Clean non-overlapping callouts inside Panel A
    s += '  <text x="182" y="156" class="ok">12 mm Eccentric Cam (62 kgf push)</text>\n'
    s += '  <text x="182" y="170" class="lbl-sm">Static 3-wire gland → 0 moving hull seals!</text>\n'
    s += '  <text x="148" y="226" class="ok">Grease-Booted 316 SS Spring</text>\n'
    s += '  <text x="148" y="239" class="lbl-sm">37 kgf @ 100% (sand-proof boot!)</text>\n'
    s += '  <text x="206" y="294" text-anchor="middle" class="dim">3.5:1 Rocker (70:20 mm)</text>\n'
    s += '  <text x="444" y="284" text-anchor="middle" class="warn">130 kgf Clamp</text>\n'
    s += '  <text x="444" y="297" text-anchor="middle" class="lbl-sm">20° Roller (μ≈0.08)</text>\n'
    s += '  <text x="456" y="358" text-anchor="middle" class="warn">4,605 N @ 85 kgf Tip!</text>\n'

    # 3-Mode Calibration Table below Panel A diagram (y = 386..580)
    s += '  <rect x="36" y="382" width="484" height="198" rx="6" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.2"/>\n'
    s += '  <text x="52" y="404" class="sec">3 Cockpit-Selectable Foil Modes (1× Servo Dial)</text>\n'
    modes_a = [
        ("0° Servo (0% Preload):", "Roller lifted clear → effortless Dyneema 0° ↔ 90° fold/deploy!", "ok"),
        ("90° Servo (50% Reef Mode):", "~45 kgf tip pop-out → soft resettable release in dense crab pots!", "dim"),
        ("180° Servo (100% TDC, 0 W):", "~85 kgf tip / ~170 kgf center → high-speed cruise lock!", "warn"),
    ]
    my_a = 428
    for mt, md, mc in modes_a:
        s += f'  <text x="52" y="{my_a}" class="{mc}">{mt}</text>\n'
        s += f'  <text x="218" y="{my_a}" class="lbl-sm">{md}</text>\n'
        my_a += 26
    s += '  <line x1="50" y1="504" x2="506" y2="504" stroke="#E2E8F0" stroke-width="1"/>\n'
    s += '  <text x="52" y="524" class="ok">5-Second On-Water Reset: Pull Deploy Dyneema → roller clicks back in!</text>\n'
    s += '  <text x="52" y="544" class="lbl-sm">Upper Switchblade Channel: Uses smaller 45 kg·cm IP68 servo (~45 kgf pop-out).</text>\n'
    s += '  <text x="52" y="564" class="dim">Emergency Backup: Manual M6 stainless lock-pin hole if 12 V power ever fails.</text>\n'

    # =========================================================================
    # PANEL B (RIGHT): UPPER STRUT KICK-UP SERVO LOCK (~140 kgf SHOAL)
    # =========================================================================
    s += '  <rect x="548" y="68" width="508" height="528" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>\n'
    s += '  <text x="566" y="92" class="sec">B. Upper Strut Lock: Front Rail Anti-Splay Bridge (0%–140 kgf)</text>\n'
    s += '  <text x="566" y="109" class="dim">Unloaded in cruise • Auto kicks up @ ~140 kgf shoal • 0% for 1-button beaching!</text>\n'
    s += '  <rect x="560" y="118" width="484" height="252" rx="6" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>\n'

    # Twin Under-Hull Rail + Anti-Splay Bridge ceiling (y = 136..152)
    s += '  <rect x="580" y="136" width="444" height="16" rx="3" fill="url(#alu)" stroke="#334155" stroke-width="1.4"/>\n'
    s += '  <text x="802" y="148" text-anchor="middle" style="font-size:8.4px;fill:#0F172A;font-weight:700;">Under-Hull Twin Rails &amp; Anti-Splay Bridge (Above Waterline!)</text>\n'

    # Front Strut (100x18 mm carbon) descending on right (x = 846..930, y = 152..354)
    s += '  <rect x="846" y="152" width="84" height="202" rx="6" fill="url(#carbon)" stroke="#0F172A" stroke-width="1.6"/>\n'
    # Top Ø16 mm Stainless Hinge Axle offset to TRAILING EDGE (+24 mm -> x = 910, y = 172)
    s += '  <circle cx="910" cy="172" r="8" fill="#FBBF24" stroke="#78350F" stroke-width="1.5"/>\n'
    # 100 mm Forward Leading-Edge Lock Tang extending left from strut (x = 768..846, y = 180..218)
    s += '  <polygon points="846,180 768,180 768,218 846,218" fill="url(#carbon)" stroke="#0F172A" stroke-width="1.4"/>\n'
    # Solid 70 mm Aluminum Forward Compression Stop Shoulder directly BELOW the LE tang (takes 100% cruise thrust!)
    s += '  <rect x="762" y="218" width="84" height="24" rx="3" fill="#334155" stroke="#0F172A" stroke-width="1.3"/>\n'
    s += '  <text x="804" y="233" text-anchor="middle" style="font-size:8px;fill:#FFFFFF;font-weight:700;">Solid Cruise Stop</text>\n'

    # Horizontal 20° Roller Pin engaging the TOP edge of the LE tang (resisting upward kick-up rotation!)
    s += '  <circle cx="764" cy="188" r="8" fill="#DC2626" stroke="#7F1D1D" stroke-width="1.4"/>\n'
    # 3.5:1 Vertical Rocker Lever + Grease-Booted Spring + IP68 Servo Cam mounted forward under bridge (x = 602..756)
    s += '  <rect x="720" y="176" width="38" height="16" rx="3" fill="url(#alu)" stroke="#0F172A" stroke-width="1.3"/>\n'
    s += '  <rect x="670" y="172" width="50" height="26" rx="5" fill="#10B981" fill-opacity="0.28" stroke="#059669" stroke-width="1.5"/>\n'
    s += '  <path d="M 676 185 L 683 177 L 690 193 L 697 177 L 704 193 L 711 185" fill="none" stroke="#334155" stroke-width="2"/>\n'
    # IP68 Servo + Over-Center Cam (gold box at x = 584..664, y = 164..206)
    s += '  <rect x="584" y="164" width="80" height="42" rx="5" fill="#FBBF24" stroke="#92400E" stroke-width="1.5"/>\n'
    s += '  <text x="624" y="183" text-anchor="middle" style="font-size:8.4px;fill:#0F172A;font-weight:700;">IP68 Servo</text>\n'
    s += '  <text x="624" y="195" text-anchor="middle" style="font-size:7.6px;fill:#451A03;">Cam + Rocker</text>\n'

    # Kick-up force arrows showing how shoal hit drives LE tang UP against roller pin while strut rotates aft!
    s += '  <path d="M 936 286 Q 974 276 994 236" fill="none" stroke="#059669" stroke-width="2.4" marker-end="url(#arrGreen)"/>\n'
    s += '  <line x1="802" y1="180" x2="802" y2="156" stroke="#DC2626" stroke-width="2.4" marker-end="url(#arrRed)"/>\n'

    # Clean non-overlapping callouts inside Panel B
    s += '  <text x="984" y="176" text-anchor="middle" class="ok">TE Pivot</text>\n'
    s += '  <text x="984" y="188" text-anchor="middle" class="lbl-sm">(Ø16 mm)</text>\n'
    s += '  <text x="984" y="298" text-anchor="middle" class="ok">Kicks Aft</text>\n'
    s += '  <text x="984" y="310" text-anchor="middle" class="lbl-sm">0° → 86.5°</text>\n'
    s += '  <text x="668" y="226" text-anchor="middle" class="ok">37 kgf Booted Spring</text>\n'
    s += '  <text x="668" y="239" text-anchor="middle" class="lbl-sm">(0% Unlock → 100% Cruise)</text>\n'
    s += '  <text x="720" y="274" text-anchor="middle" class="dim">Cruise Thrust pushes LE</text>\n'
    s += '  <text x="720" y="287" text-anchor="middle" class="lbl-sm">DOWN onto solid Alu stop</text>\n'
    s += '  <text x="720" y="300" text-anchor="middle" class="ok">(0 kgf on pin in flight!)</text>\n'
    s += '  <text x="720" y="328" text-anchor="middle" class="warn">Shoal Hit (~140 kgf) drives</text>\n'
    s += '  <text x="720" y="341" text-anchor="middle" class="lbl-sm">100 mm LE tang UP across roller!</text>\n'

    # 1-Button Beach Sequence & Smart Divider Box below Panel B (y = 382..580)
    s += '  <rect x="560" y="382" width="484" height="198" rx="6" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.2"/>\n'
    s += '  <text x="576" y="404" class="sec">1-Button Cockpit "BEACH MODE" &amp; Auto-Reset</text>\n'
    s += '  <text x="576" y="428" class="ok">Step 1 — Press BEACH MODE:</text>\n'
    s += '  <text x="586" y="443" class="lbl-sm">• Both Foil &amp; Strut IP68 servos rotate to 0% preload (pins retracted!).</text>\n'
    s += '  <text x="576" y="466" class="ok">Step 2 — Pull Fold Dyneema Handle (2 s):</text>\n'
    s += '  <text x="586" y="481" class="lbl-sm">• All wings fold true 90° flush inside 220 mm upper/lower pod channels!</text>\n'
    s += '  <text x="576" y="504" class="ok">Step 3 — Pull 3:1 Strut Tackle (3 s):</text>\n'
    s += '  <text x="586" y="519" class="lbl-sm">• 220 mm pod tucks 86.5° flat BETWEEN the 250 mm rails (5.5" sand clear!).</text>\n'
    s += '  <text x="576" y="544" class="dim">Auto-Reset After Sandbar Kick-Up:</text>\n'
    s += '  <text x="586" y="559" class="lbl-sm">• Lower struts back to 0° → roller pin snaps automatically into cruise notch!</text>\n'
    s += '  <text x="586" y="573" class="warn">• Smart Divider preserved: Shoal (~140 kgf) kicks struts before wings (~170 kgf)!</text>\n'

    s += "</svg>\n"
    (OUT_DIR / "24-servo-preload-pins-mechanics.svg").write_text(s)


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
    gen_20_morphing_stol_staggerwing()
    gen_21_center_strut_asymmetric_loads()
    gen_22_breakaway_socket_options()
    gen_23_breakaway_deployed_flaperons()
    gen_24_servo_preload_pins()
    print("Generated all 15 2D engineering SVGs in", OUT_DIR)
