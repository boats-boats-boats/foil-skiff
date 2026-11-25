// ==========================================================================
// FoilSkiff PRIMARY — Close-Up: Parallel-Float Internal Blade-Tang Wing-Warp
// ==========================================================================
// Parametric 1:1 mm Close-Up Assembly (Starboard Pair: Front + Rear Floats)
//
// ZERO Telescoping Slip-Tube! Floats ALWAYS stay 100% rigid & parallel!
//   - Front & Rear 24 L Stepped Tip Floats (620 x 400 x 134 mm: NACA 0014
//     torpedo planform from above, R = 65 mm rounded rectangle from the side)
//     permanently joined by a SOLID FIXED-LENGTH Ø34 mm carbon tie-bar!
//   - Free-flooding vertical center slot/trunk inside each foam-filled float:
//       * Fixed Ø10 mm 316L stainless pivot pin at the lower float junction
//         (Z = +18 mm above float bottom — dry in 12-15.5 kn cruise!)
//       * Upper foil blade tang extends 320 mm straight UP inside the trunk
//       * Dry horizontal non-backdrivable IP67 Tr8 linear actuator at Z = +338 mm
//         pushes the upper tang ±17 mm fore-and-aft (~100 N peak force)
//         -> cleanly twists each submerged 0.90 m foil half by ±3.0° AoA!
//       * Fore & aft closed-cell foam float chambers stay 100% sealed & unsinkable!
//
// Exportable Printable 1:1 STLs:
//   "assembly_cutaway", "lower_pivot_saddle", "tang_clevis"
// ==========================================================================

/* [Render Mode & Live Kinematics] */
part_select   = "assembly_cutaway";
fwd_twist_deg = -2.5;    // Front foil tip twist (-3°..+3°)
aft_twist_deg =  2.5;    // Rear foil tip twist  (-3°..+3°)
vis_exag      =  2.4;    // Visual exaggeration for cutaway clarity

/* [Core Geometry (mm)] */
float_len     = 620.0;
float_h       = 400.0;
float_w       = 134.0;
corner_r      = 65.0;
x_fwd         = -450.0;  // Front float center
x_aft         =  450.0;  // Rear float center (900 mm rigid spacing)
z_pivot       =  18.0;   // Fixed Ø10 mm lower pivot height above float bottom (Z = 0)
z_act         = 338.0;   // Dry linear actuator height (320 mm internal lever arm!)
z_bar         = 315.0;   // Rigid fixed-length Ø34 mm tie-bar height
tiebar_od     =  34.0;   // Solid fixed carbon tie-bar OD
slot_w        =  28.0;   // Internal free-flooding vertical blade trunk width
slot_len      = 175.0;   // Fore-aft slot clearance for ±3° tang sweep
pin_dia       =  10.0;   // Fixed Ø10 mm 316L lower pivot pin

$fn = 64;

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

// Single 24 L Stepped Tip Float with Internal Vertical Blade-Tang Trunk
module tip_float_with_trunk() {
    difference() {
        intersection() {
            linear_extrude(height = float_h)
                polygon(naca_torp_pts(float_len, float_w / float_len, 22));
            translate([0, 0, float_h / 2])
                rotate([90, 0, 0])
                    linear_extrude(height = float_w + 20, center = true)
                        offset(r = corner_r)
                            square([float_len - 2*corner_r, float_h - 2*corner_r], center = true);
        }
        // Free-flooding vertical center blade trunk (fore & aft foam chambers stay 100% sealed!)
        translate([0, 0, float_h / 2 - 2])
            cube([slot_len, slot_w, float_h + 10], center = true);
        // Recessed top dry actuator pocket (Z = 285..405 mm)
        translate([-55, 0, 345])
            cube([290, 56, 125], center = true);
    }
}

// ==========================================================================
// PRINTABLE PART 1: Lower Fixed Pivot Saddle (Reinforces Float Bottom Trunk)
// ==========================================================================
module lower_pivot_saddle() {
    difference() {
        union() {
            // Twin side cheek plates bonding into the float lower trunk walls
            for (sy = [-1, 1]) {
                translate([0, sy * (slot_w / 2 + 5.0), z_pivot + 8.0])
                    cube([74.0, 10.0, 44.0], center = true);
            }
            // Fore & aft U-bridges keeping exact 28 mm trunk spacing
            for (sx = [-32.0, 32.0]) {
                translate([sx, 0, z_pivot + 8.0])
                    cube([10.0, slot_w + 20.0, 44.0], center = true);
            }
        }
        // Central trunk clearance for 18 mm blade
        translate([0, 0, z_pivot + 8.0])
            cube([54.0, slot_w, 50.0], center = true);
        // Horizontal Ø10 mm 316L fixed pivot pin bore (along Y) + flanged bronze bushing recess
        translate([0, 0, z_pivot])
            rotate([90, 0, 0]) cylinder(d = pin_dia + 0.15, h = slot_w + 30.0, center = true);
        // 4x M5 structural mounting bolts into carbon float floor
        for (sx = [-26.0, 26.0], sy = [-19.0, 19.0]) {
            translate([sx, sy, z_pivot + 24.0])
                rotate([90, 0, 0]) cylinder(d = 5.2, h = 14.0, center = true);
        }
    }
}

// ==========================================================================
// PRINTABLE PART 2: Upper Blade-Tang Actuator Clevis (Clamps Top of Tang)
// ==========================================================================
module tang_clevis() {
    difference() {
        union() {
            // Wrap-around clamp sleeve gripping the 18 mm carbon blade tang top
            cube([44.0, 30.0, 38.0], center = true);
            // Forward clevis fork ears for the IP67 linear actuator rod-end eye
            translate([-30.0, 0, 0]) cube([24.0, 24.0, 24.0], center = true);
        }
        // Blade tang pocket (18.4 mm wide)
        translate([4.0, 0, -2.0]) cube([38.0, 18.4, 42.0], center = true);
        // Fork slot for 10 mm actuator rod-end eye
        translate([-32.0, 0, 0]) cube([26.0, 10.6, 28.0], center = true);
        // Ø6 mm horizontal actuator clevis pin bore (along Y)
        translate([-33.0, 0, 0]) rotate([90, 0, 0]) cylinder(d = 6.2, h = 34.0, center = true);
        // 2x M5 blade-tang pinch bolts (along Y)
        for (bx = [-4.0, 12.0]) {
            translate([bx, 0, 0]) rotate([90, 0, 0]) cylinder(d = 5.2, h = 36.0, center = true);
        }
    }
}

// Full Vertical Blade (Lower Wet Leg + Upper Internal Tang) + Anti-Vent Fence + Submerged Foil Root
module rocking_blade_and_foil(lower_len, chord, foil_col) {
    // Continuous 18 mm vertical carbon blade from submerged foil (-lower_len) to tang top (+z_act + 16)!
    color(foil_col)
    translate([0, 0, -lower_len])
        linear_extrude(height = lower_len + z_act + 18)
            polygon(naca_torp_pts(chord * 1.15, 0.16, 16));

    // Red horizontal anti-ventilation fence (below cruise waterline)
    color([0.86, 0.20, 0.20])
        translate([-4, 0, -90])
            cube([chord * 1.25, 52, 6], center = true);

    // Submerged U-foil root stub extending inboard (-Y) with visible gold 25%-chord UD carbon spar!
    color(foil_col, 0.76)
    translate([0, -145, -lower_len])
        rotate([-90, 0, 0])
            linear_extrude(height = 150)
                polygon(naca_torp_pts(chord, 0.12, 16));

    // Gold 25%-chord UD Carbon Main Spar
    color([0.92, 0.70, 0.12])
        translate([-chord * 0.20, -160, -lower_len])
            rotate([-90, 0, 0])
                cylinder(d = chord * 0.09, h = 166);

    // Printable Upper Tang Clevis at Z = z_act
    color([0.74, 0.78, 0.84])
        translate([0, 0, z_act]) tang_clevis();
}

// Horizontal Dry IP67 Tr8 Linear Actuator mounted to the rigid float bulkhead
module horizontal_linear_actuator(x_rod_end, dir_sign = 1) {
    // Fixed actuator body on rigid float bulkhead (dir_sign=+1: body on -X pushing +X)
    body_x = -dir_sign * 138.0;
    color([0.16, 0.22, 0.28])
        translate([body_x, 0, z_act])
            rotate([0, 90, 0]) cylinder(d = 30.0, h = 110.0, center = true);
    // Motor gearbox pod under rear of actuator
    color([0.24, 0.30, 0.38])
        translate([body_x - dir_sign * 36.0, 0, z_act - 24.0])
            cylinder(d = 34.0, h = 42.0, center = true);
    // Extending stainless rod connecting body to moving tang clevis!
    rod_x0 = body_x + dir_sign * 52.0;
    rod_len = abs(x_rod_end - rod_x0);
    color([0.92, 0.72, 0.14])
        translate([(rod_x0 + x_rod_end) / 2, 0, z_act])
            rotate([0, 90, 0]) cylinder(d = 10.0, h = rod_len, center = true);
}

// ==========================================================================
// Assembly & Export Switch
// ==========================================================================
if (part_select == "lower_pivot_saddle") {
    translate([0, 0, -z_pivot + 14]) lower_pivot_saddle();
} else if (part_select == "tang_clevis") {
    tang_clevis();
} else {
    // "assembly_cutaway":
    //   - Front & Rear Floats stay 100% RIGID & PARALLEL, linked by ONE SOLID Ø34 mm carbon tie-bar!
    //   - Foreground (-Y) half of each orange float is cut away to reveal the internal vertical trunk,
    //     fixed red Ø10 mm lower pivot pin, rocking blade tang, and horizontal dry IP67 linear actuator!
    f_rot = fwd_twist_deg * vis_exag;
    a_rot = aft_twist_deg * vis_exag;

    // 1. RIGID FIXED-LENGTH CARBON TIE-BAR (Zero telescoping parts! Bonded straight into parallel floats!)
    color([0.16, 0.22, 0.28])
        translate([0, 0, z_bar])
            rotate([0, 90, 0]) cylinder(d = tiebar_od, h = (x_aft - x_fwd) - 340.0, center = true);
    // Non-marking dark rubber dock rub-strake along outer (+Y) face of tie-bar
    color([0.28, 0.34, 0.42])
        translate([0, tiebar_od * 0.5 + 4, z_bar])
            cube([(x_aft - x_fwd) - 420.0, 8.0, 22.0], center = true);

    // 2. FRONT FLOAT (100% PARALLEL!) + ROCKING FRONT BLADE TANG (Pivot fixed at Z = z_pivot!)
    translate([x_fwd, 0, 0]) {
        difference() {
            color([0.96, 0.46, 0.12, 0.94]) tip_float_with_trunk();
            translate([-240, -96, -2]) cube([480, 96, 410]);
        }
        color([0.65, 0.70, 0.76]) lower_pivot_saddle();
        // Red Fixed Ø10 mm 316L Lower Pivot Pin
        color([0.86, 0.20, 0.20])
            translate([0, 0, z_pivot]) rotate([90, 0, 0]) cylinder(d = pin_dia, h = 64.0, center = true);
        // Rocking Blade + Submerged Foil rotating around FIXED lower pivot (0, 0, z_pivot)!
        translate([0, 0, z_pivot])
            rotate([0, f_rot, 0])
                translate([0, 0, -z_pivot])
                    rocking_blade_and_foil(350, 95, [0.06, 0.52, 0.78]);
        // Horizontal Dry Linear Actuator driving tang top!
        x_clev_f = (z_act - z_pivot) * sin(f_rot) - 33.0 * cos(f_rot);
        horizontal_linear_actuator(x_clev_f, 1);
    }

    // 3. REAR FLOAT (100% PARALLEL!) + ROCKING REAR BLADE TANG (+130 mm higher staggered foil!)
    translate([x_aft, 0, 0]) {
        difference() {
            color([0.96, 0.46, 0.12, 0.94]) tip_float_with_trunk();
            translate([-240, -96, -2]) cube([480, 96, 410]);
        }
        color([0.65, 0.70, 0.76]) lower_pivot_saddle();
        color([0.86, 0.20, 0.20])
            translate([0, 0, z_pivot]) rotate([90, 0, 0]) cylinder(d = pin_dia, h = 64.0, center = true);
        translate([0, 0, z_pivot])
            rotate([0, a_rot, 0])
                translate([0, 0, -z_pivot])
                    rocking_blade_and_foil(220, 65, [0.05, 0.58, 0.53]);
        // Rear actuator mounted on aft bulkhead pushing forward onto tang!
        x_clev_a = (z_act - z_pivot) * sin(a_rot) - 33.0 * cos(a_rot);
        horizontal_linear_actuator(x_clev_a, 1);
    }

    // 4. Translucent 12-15.5 kn High-Speed Cruise Waterline (Z = -30 mm -> floats +30 mm DRY!)
    color([0.22, 0.74, 0.97, 0.16])
        translate([0, -40, -32])
            cube([1680, 420, 4], center = true);
}
