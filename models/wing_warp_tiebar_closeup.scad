// ==========================================================================
// FoilSkiff PRIMARY — Close-Up: Dry 4-Float Wing-Warping & Passive Slip-Bar
// ==========================================================================
// Parametric 1:1 mm Close-Up Assembly (Starboard Pair: Front + Rear Floats)
//
// Shows the complete dry above-water wing-warping mechanism (Model 14):
//   - Front & Rear 24 L Stepped Tip Floats (620 x 400 x 135 mm: NACA 0014
//     torpedo planform from above, R = 65 mm rounded rectangle from the side)
//   - Dry recessed top actuator bays housing non-backdrivable worm-gear / Tr8
//     rotary drives (100% DRY +330 mm above 12-15.5 kn cruise waterline!)
//   - Passive Telescoping Carbon Slip-Tube Tie-Bar (Ø28 mm inner tube sliding
//     ±35 mm inside Ø32 mm outer tube across a 200 mm UHMW-PE bushing collar):
//       * Absorbs ΔL = ±34 mm freely when Front & Rear twist differently
//       * Transmits 100% of vertical shear F_z (~56 N) & bending reaction!
//   - Thin 18 mm lower vertical U-foil blades + red anti-ventilation fences
//   - Submerged Front Main & Rear Staggered U-Foil roots with 25%-chord UD
//     carbon main spars (aligns shear center -> >50 kn divergence safety!)
//
// Part Selection:
//   "assembly_cutaway" (default close-up view), "slip_collar", "actuator_clevis"
// ==========================================================================

/* [Render Mode & Live Kinematics] */
part_select   = "assembly_cutaway";
fwd_twist_deg = -2.0;    // Front foil tip twist (-3°..+3°; exaggerated 2x visually in cutaway)
aft_twist_deg =  2.0;    // Rear foil tip twist  (-3°..+3°)
vis_exag      =  2.2;    // Visual exaggeration multiplier for cutaway clarity

/* [Core Geometry (mm)] */
float_len     = 620.0;
float_h       = 400.0;
float_w       = 134.0;
corner_r      = 65.0;
x_fwd         = -450.0;  // Front float center
x_aft         =  450.0;  // Rear float center (L_bar = 900 mm)
z_bar         =  305.0;  // Tie-bar height above float bottom (Z=0 is float bottom!)
tube_out_od   =  34.0;   // Ø34 mm carbon outer tie-bar tube (ID 28.4 mm)
tube_in_od    =  28.0;   // Ø28 mm carbon inner sliding tube
uhmw_len      = 120.0;   // UHMW-PE bearing sleeve collar length

$fn = 64;

// NACA-style 2D symmetric torpedo planform polygon centered at x=0
function naca_torp_pts(L, thick_ratio, n=24) =
    let(
        up = [for (i = [0 : n])
            let(beta = 180 * i / n,
                xc = 0.5 * (1 - cos(beta)),
                yt = 5 * thick_ratio * (0.2969*sqrt(max(xc,0)) - 0.1260*xc - 0.3516*xc*xc + 0.2843*xc*xc*xc - 0.1036*xc*xc*xc*xc))
            [(xc - 0.45) * L, yt * L]
        ],
        lo = [for (i = [n-1 : -1 : 1])
            let(beta = 180 * i / n,
                xc = 0.5 * (1 - cos(beta)),
                yt = 5 * thick_ratio * (0.2969*sqrt(max(xc,0)) - 0.1260*xc - 0.3516*xc*xc + 0.2843*xc*xc*xc - 0.1036*xc*xc*xc*xc))
            [(xc - 0.45) * L, -yt * L]
        ]
    ) concat(up, lo);

// Single 24 L Stepped Tip Float (Torpedo from above x Rounded Rectangle from side)
module tip_float_solid() {
    intersection() {
        // Vertical extrusion of classical torpedo planform
        linear_extrude(height = float_h)
            polygon(naca_torp_pts(float_len, float_w / float_len, 22));
        // Side-view rounded-corner rectangle (620 x 400 mm, R = 65 mm)
        translate([0, 0, float_h / 2])
            rotate([90, 0, 0])
                linear_extrude(height = float_w + 20, center = true)
                    offset(r = corner_r)
                        square([float_len - 2*corner_r, float_h - 2*corner_r], center = true);
    }
}

// ==========================================================================
// PRINTABLE PART 1: Passive Telescoping UHMW Slip-Collar (Ø34 / Ø28 mm)
// ==========================================================================
module slip_collar() {
    difference() {
        union() {
            // Main collar sleeve
            rotate([0, 90, 0]) cylinder(d = tube_out_od + 10.0, h = uhmw_len, center = true);
            // Clamping rib ears for 4x M4 pinch bolts on outer carbon tube side (-X half)
            translate([-uhmw_len * 0.25, 0, tube_out_od * 0.5 + 5.0])
                cube([uhmw_len * 0.45, 16.0, 14.0], center = true);
        }
        // Left half (-X): clamps onto Ø34 mm outer carbon tube
        translate([-uhmw_len * 0.5 - 1, 0, 0])
            rotate([0, 90, 0]) cylinder(d = tube_out_od + 0.2, h = uhmw_len * 0.52 + 1);
        // Right half (+X): precision UHMW slip bore for Ø28 mm inner carbon tube (+0.25 mm)
        translate([-2, 0, 0])
            rotate([0, 90, 0]) cylinder(d = tube_in_od + 0.25, h = uhmw_len * 0.55 + 4);
        // Wiper O-ring groove at slip entry (+X end) to keep salt/spray out!
        translate([uhmw_len * 0.5 - 8.0, 0, 0])
            rotate([0, 90, 0])
                difference() {
                    cylinder(d = tube_in_od + 4.4, h = 3.2, center = true);
                    cylinder(d = tube_in_od - 1.0, h = 4.0, center = true);
                }
        // Pinch slot & 2x M4 clamp bolt holes on -X side
        translate([-uhmw_len * 0.25, 0, tube_out_od * 0.5 + 5.0])
            cube([uhmw_len * 0.5, 2.2, 22.0], center = true);
        for (bx = [-uhmw_len * 0.36, -uhmw_len * 0.14]) {
            translate([bx, 0, tube_out_od * 0.5 + 7.0])
                rotate([90, 0, 0]) cylinder(d = 4.3, h = 24.0, center = true);
        }
    }
}

// ==========================================================================
// PRINTABLE PART 2: Dry Rotary Worm-Actuator Clevis Hub (Bolts Inside Float)
// ==========================================================================
module actuator_clevis() {
    difference() {
        union() {
            // Cylindrical rotary hub driven by dry worm gearmotor shaft (along Y axis)
            rotate([90, 0, 0]) cylinder(d = 48.0, h = 46.0, center = true);
            // Tangential socket clamping onto the Ø34 mm (or Ø28 mm) tie-bar tube
            translate([34.0, 0, 0])
                rotate([0, 90, 0]) cylinder(d = tube_out_od + 9.0, h = 44.0, center = true);
            // Reinforcing web between hub & tube socket
            translate([18.0, 0, 0]) cube([36.0, 34.0, 36.0], center = true);
        }
        // Ø12 mm D-shaft worm-gear output bore (along Y)
        rotate([90, 0, 0]) cylinder(d = 12.1, h = 54.0, center = true);
        // Tie-bar tube bond/clamp socket
        translate([34.0, 0, 0])
            rotate([0, 90, 0]) cylinder(d = tube_out_od + 0.2, h = 48.0, center = true);
        // 2x M5 cross-pin lock bolts
        for (px = [26.0, 44.0]) {
            translate([px, 0, 0]) rotate([90, 0, 0]) cylinder(d = 5.2, h = 50.0, center = true);
        }
    }
}

// Lower 18 mm blade + anti-ventilation fence + submerged U-foil root w/ 25%-c UD spar
module lower_blade_and_foil(blade_len, chord, foil_col) {
    // Thin 18 mm vertical blade extending down from float bottom (Z=0 -> Z=-blade_len)
    color(foil_col)
    translate([0, 0, -blade_len])
        linear_extrude(height = blade_len + 20)
            polygon(naca_torp_pts(chord * 1.15, 0.16, 16));

    // Red horizontal anti-ventilation fence (Z = -90 mm)
    color([0.86, 0.20, 0.20])
        translate([-5, 0, -90])
            cube([chord * 1.25, 52, 6], center = true);

    // Curved U-foil root stub extending inboard (-Y) with visible gold 25%-chord UD carbon spar!
    color(foil_col, 0.72)
    translate([0, -140, -blade_len])
        rotate([-90, 0, 0])
            linear_extrude(height = 145)
                polygon(naca_torp_pts(chord, 0.12, 16));

    // Gold 25%-chord UD Carbon Main Spar (aligns shear center with center of pressure!)
    color([0.92, 0.70, 0.12])
        translate([-chord * 0.20, -155, -blade_len])
            rotate([-90, 0, 0])
                cylinder(d = chord * 0.09, h = 162);
}

// Dry non-backdrivable worm-gear rotary actuator unit inside top float pocket
module dry_worm_actuator() {
    // Aluminum worm-gear gearbox housing
    color([0.24, 0.30, 0.38])
        cube([64, 52, 58], center = true);
    // Brushless drive motor cylinder mounted vertically on gearbox
    color([0.14, 0.18, 0.24])
        translate([0, 0, -54]) cylinder(d = 36, h = 58, center = true);
    // Gold Ø12 mm output shaft
    color([0.92, 0.70, 0.12])
        rotate([90, 0, 0]) cylinder(d = 12, h = 68, center = true);
}

// ==========================================================================
// Assembly & Export Switch
// ==========================================================================
if (part_select == "slip_collar") {
    slip_collar();
} else if (part_select == "actuator_clevis") {
    actuator_clevis();
} else {
    // "assembly_cutaway": Starboard Front & Rear Floats (foreground cutaway!) +
    // Live Dry Worm Actuators + Passive Telescoping Carbon Tie-Bar + Submerged 25%-c Spars!
    f_rot = fwd_twist_deg * vis_exag;
    a_rot = aft_twist_deg * vis_exag;

    // 1. FRONT FLOAT + BLADE + MAIN U-FOIL ROOT (rotates around 25%-c spar @ Z = -350 mm!)
    translate([x_fwd, 0, -350])
        rotate([0, f_rot, 0])
            translate([0, 0, 350]) {
                // Cutaway camera-facing (-Y) half of orange float to reveal dry worm actuator & clevis!
                difference() {
                    color([0.96, 0.46, 0.12, 0.94]) tip_float_solid();
                    translate([-130, -96, 165]) cube([260, 96, 245]);
                }
                translate([0, 0, z_bar]) dry_worm_actuator();
                translate([0, 0, z_bar]) color([0.72, 0.76, 0.82]) actuator_clevis();
                lower_blade_and_foil(350, 95, [0.06, 0.52, 0.78]);
            }

    // 2. REAR FLOAT + BLADE + STAGGERED U-FOIL ROOT (+130 mm higher, rotates around Z = -220 mm!)
    translate([x_aft, 0, -220])
        rotate([0, a_rot, 0])
            translate([0, 0, 220]) {
                difference() {
                    color([0.96, 0.46, 0.12, 0.94]) tip_float_solid();
                    translate([-130, -96, 165]) cube([260, 96, 245]);
                }
                translate([0, 0, z_bar]) dry_worm_actuator();
                translate([0, 0, z_bar]) rotate([0, 0, 180]) color([0.72, 0.76, 0.82]) actuator_clevis();
                lower_blade_and_foil(220, 65, [0.05, 0.58, 0.53]);
            }

    // 3. ABOVE-WATER PASSIVE TELESCOPING CARBON SLIP-TUBE TIE-BAR (Z = z_bar = +305 mm!)
    //    Outer Ø34 mm carbon tube (left) + White/Cyan UHMW Slip-Collar (center) + Inner Ø28 mm tube (right)
    p_f = [x_fwd + 655 * sin(f_rot), 0, -350 + 655 * cos(f_rot)];
    p_a = [x_aft + 525 * sin(a_rot), 0, -220 + 525 * cos(a_rot)];
    p_m = (p_f + p_a) / 2;
    v_b = p_a - p_f;
    L_b = norm(v_b);
    ang_y = atan2(-v_b[2], v_b[0]);

    // Outer Ø34 mm carbon tube (front half)
    color([0.16, 0.22, 0.28])
        translate(p_f) rotate([0, ang_y, 0]) rotate([0, 90, 0])
            cylinder(d = tube_out_od, h = L_b * 0.52);

    // Inner Ø28 mm carbon tube (rear half, slides freely ±35 mm inside UHMW collar!)
    color([0.48, 0.55, 0.62])
        translate(p_m) rotate([0, ang_y, 0]) rotate([0, 90, 0])
            cylinder(d = tube_in_od, h = L_b * 0.50);

    // Printable UHMW-PE Passive Slip-Collar at center
    color([0.08, 0.74, 0.95])
        translate(p_m) rotate([0, ang_y, 0]) slip_collar();

    // 4. Translucent 12-15.5 kn High-Speed Cruise Waterline Plane (Z = -30 mm -> floats +30 mm DRY!)
    color([0.22, 0.74, 0.97, 0.16])
        translate([0, -40, -32])
            cube([1680, 420, 4], center = true);
}
