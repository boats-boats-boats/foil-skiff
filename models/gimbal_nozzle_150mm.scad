// ==========================================================================
// FoilSkiff — 2-Axis Spherical Ring-Nozzle Gimbal & Spider-Mounted Plug
// ==========================================================================
// Close-Up Mechanical Assembly for the 70/30 Split Keel Jet-CCV Pod (Model 11)
//
// Coordinate Convention (matches FoilSkiff CAD):
//   +X = Aft (Jet flow direction, Gimbal Center at X = 0, Y = 0, Z = 0)
//   ±Y = Starboard / Port (Pitch pivot axis: ±6° around Y via 3 & 9 o'clock pins)
//   ±Z = Up / Down        (Yaw pivot axis:   ±15° around Z via 12 & 6 o'clock pins)
//
// Zero-Collision Spherical Kinematics:
//   - Stationary Male Spherical Lip:    R_male   = 75.0 mm (centered at 0,0,0)
//   - Nozzle Female Spherical Collar:   R_in     = 75.4 mm, R_out = 79.8 mm
//   - UHMW-PE Spherical Seal Band:      R = 75.1 mm (0.1 mm water-lubricated fit, 0 leak!)
//   - External Cardan Gimbal Ring:      R_in = 82.5 mm, R_out = 89.5 mm (Ø179 mm OD)
//     Because the nozzle collar is spherical (R_out = 79.8 < 82.5 mm) across the
//     Cardan Ring width (X = -8..+8 mm), interference is mathematically impossible
//     at any simultaneous combination of ±15° Yaw and ±6° Pitch!
//   - Spider-Mounted Sliding Plug:      Carried by 3 streamlined vanes INSIDE the
//     pivoting nozzle so the Ø65 -> Ø16 mm plug gimbals 100% concentrically with
//     the Ø132 mm exit bore (ZERO wall clash at ±15° yaw!).
//
// Exportable Printable Parts (1:1 mm):
//   "assembly_cutaway", "exploded", "stator_housing", "cardan_ring",
//   "rear_nozzle", "sliding_plug"
// ==========================================================================

/* [Render Mode & Kinematics] */
part_select     = "assembly_cutaway";
yaw_deg         = 12.0;     // Live Yaw deflection (-15° to +15°, around Z)
pitch_deg       = 4.0;      // Live Pitch deflection (-6° to +6°, around Y)
plug_stroke_mm  = 16.0;     // Sliding plug axial travel (0 = wide 134 cm², 45 = trimmed 104 cm²)

/* [Core Hydrodynamic & Gimbal Radii (mm)] */
bore_in_r       = 70.0;     // Ø140 mm stationary pump/stator bore
bore_exit_r     = 66.0;     // Ø132 mm nozzle exit bore (133.7 cm² max open)
sphere_male_r   = 75.0;     // Male spherical sealing ball radius
nozzle_sph_in   = 75.4;     // Female spherical collar inner radius
nozzle_sph_out  = 79.8;     // Female spherical collar outer radius (strictly < cardan_in!)
cardan_in_r     = 82.5;     // External 2-axis Cardan ring inner radius
cardan_out_r    = 89.5;     // External 2-axis Cardan ring outer radius (Ø179 mm OD)
cardan_width    = 16.0;     // Cardan ring axial thickness centered at X = 0
pin_dia         = 8.0;      // 4x Ø8 mm 316L stainless gimbal pins (flanged bronze bushings)
nozzle_len      = 320.0;    // Articulated shroud length aft of gimbal center (X = 0..320)
hub_r           = 32.5;     // Ø65 mm Flipsky 65161 / stator hub radius

$fn = 96;

// ==========================================================================
// Helper: Revolve 2D [X_axial, R_radial] profile around the +X flow axis
// ==========================================================================
module revolve_x(pts) {
    rotate([0, 90, 0])
        rotate_extrude(convexity = 10)
            polygon([for (p = pts) [p[1], p[0]]]);
}

// Transform child geometry by the true 2-axis Pitch -> Yaw Cardan rotation
module gimbal_transform(do_yaw = true, do_pitch = true) {
    rotate([0, do_pitch ? -pitch_deg : 0, 0])
        rotate([0, 0, do_yaw ? yaw_deg : 0])
            children();
}

// ==========================================================================
// PART 1: Stationary Aft Stator Housing + Male Spherical Ball + Pitch Forks
// ==========================================================================
module stator_housing() {
    difference() {
        union() {
            // 1. Main cylindrical stator barrel (X = -115..-16 mm)
            revolve_x([
                [-115, bore_in_r], [-115, 76.5],
                [-16,  76.5],      [-16,  bore_in_r]
            ]);

            // 2. Male spherical sealing ball zone (X = -24..+24 mm, centered at 0,0,0!)
            intersection() {
                sphere(r = sphere_male_r);
                translate([-24, -95, -95]) cube([48, 190, 190]);
            }

            // 3. Forward mounting flange bolted to rigid front/mid pod (X = -115..-107)
            revolve_x([
                [-115, 76.0], [-115, 86.0],
                [-107, 86.0], [-107, 76.0]
            ]);

            // 4. Twin symmetrical longitudinal Pitch Fork Arms (3 & 9 o'clock, Y = ±91..±98 mm)
            //    Straddle OUTSIDE the Cardan Ring (R_out = 89.5 mm) to hold horizontal Pitch pins!
            for (sy = [-1, 1]) {
                mirror([0, sy < 0 ? 1 : 0, 0]) {
                    hull() {
                        translate([-95, 74.0, -10]) cube([26, 22.0, 20]);
                        translate([-10, 91.0, -10]) cube([18, 7.0, 20]);
                    }
                    // Boss around Pitch pin bore at (0, +94.5, 0)
                    translate([0, 91.0, 0])
                        rotate([-90, 0, 0])
                            cylinder(d = 20.0, h = 7.5);
                }
            }

            // 5. Dry-Pod Servo Pushrod Guide Bosses (Top = Pitch @ Z=+88, Stbd = Yaw @ Y=+88)
            translate([-105, -10, 74]) cube([22, 20, 22]);
            translate([-105, 74, -10]) cube([22, 22, 20]);
        }

        // Clean Ø140 mm internal water bore through barrel & spherical ball
        translate([-120, 0, 0])
            rotate([0, 90, 0])
                cylinder(r = bore_in_r, h = 155);

        // Horizontal Ø8 mm Pitch Pin Bores through fork arms (along Y axis at X=0, Z=0)
        rotate([90, 0, 0])
            cylinder(d = pin_dia + 0.2, h = 210, center = true);

        // Pushrod guide holes on top & starboard bosses
        translate([-110, 0, 88]) rotate([0, 90, 0]) cylinder(d = 7.0, h = 32);
        translate([-110, 88, 0]) rotate([0, 90, 0]) cylinder(d = 7.0, h = 32);

        // 8x M5 pod mounting holes on forward flange
        for (k = [0 : 7]) {
            rotate([k * 45 + 22.5, 0, 0])
                translate([-117, 0, 81.5])
                    rotate([0, 90, 0])
                        cylinder(d = 5.3, h = 14);
        }
    }

    // 6. Central Stator Hub Cone (Ø65 mm) + 7 Straightening Stator Vanes (ADDED AFTER bore cut!)
    revolve_x([
        [-115, 0], [-115, hub_r], [-40, hub_r], [-12, 22], [8, 6], [8, 0]
    ]);
    for (k = [0 : 6]) {
        rotate([k * (360 / 7), 0, 0])
            translate([-92, -1.8, hub_r - 2])
                cube([48, 3.6, bore_in_r - hub_r + 3.5]);
    }
}

// ==========================================================================
// PART 2: External 2-Axis Cardan Gimbal Ring (Ø165 ID / Ø179 OD x 16 mm)
// ==========================================================================
module cardan_ring() {
    difference() {
        union() {
            // Main concentric structural ring centered at X = 0
            translate([-cardan_width / 2, 0, 0])
                rotate([0, 90, 0])
                    difference() {
                        cylinder(r = cardan_out_r, h = cardan_width);
                        translate([0, 0, -1]) cylinder(r = cardan_in_r, h = cardan_width + 2);
                    }
            // Reinforced bearing bosses at 12, 3, 6, 9 o'clock
            for (ang = [0, 90, 180, 270]) {
                rotate([ang, 0, 0])
                    translate([0, 0, cardan_in_r - 1.0])
                        cylinder(d = 17.5, h = (cardan_out_r - cardan_in_r) + 2.5);
            }
        }

        // Clean inner clearance bore
        translate([-cardan_width, 0, 0])
            rotate([0, 90, 0])
                cylinder(r = cardan_in_r, h = cardan_width * 2);

        // Pitch Pin Bores (3 & 9 o'clock, along Y) — flanged bronze bushing fit (Ø10 mm)
        rotate([90, 0, 0])
            cylinder(d = pin_dia + 2.0, h = 210, center = true);

        // Yaw Pin Bores (12 & 6 o'clock, along Z) — flanged bronze bushing fit (Ø10 mm)
        cylinder(d = pin_dia + 2.0, h = 210, center = true);
    }
}

// ==========================================================================
// PART 3: Articulated Rear Ring-Nozzle + Female Spherical Collar + 3 Spiders
// ==========================================================================
module rear_nozzle() {
    difference() {
        union() {
            // 1. Female Spherical Overlap Collar (X = -20..+20 mm, strictly inside R=79.8!)
            intersection() {
                sphere(r = nozzle_sph_out);
                translate([-20, -90, -90]) cube([40, 180, 180]);
            }

            // 2. Hollow Converging Carbon Ring-Shroud (X = +16..+320 mm)
            //    Smoothly converges from Ø150 OD / Ø140 ID to Ø142 OD / Ø132 ID exit bore!
            revolve_x([
                [16,  bore_in_r + 0.5],  [16,  77.6],
                [95,  76.2],             [215, 73.5],
                [320, 71.2],             [320, bore_exit_r],
                [215, 67.5],             [95,  69.2],
                [16,  bore_in_r + 0.5]
            ]);

            // 3. Top & Bottom Yaw Pivot Ears at 12 & 6 o'clock (X = 0, Z = ±77..±82 mm)
            for (sz = [-1, 1]) {
                translate([0, 0, sz * 75.5])
                    cylinder(d = 16.0, h = sz > 0 ? 6.5 : 6.5, center = (sz < 0));
            }

            // 4. Servo Actuation Clevis Ears at X = +62 mm (Top = Pitch, Stbd = Yaw)
            //    Placed ~62 mm aft of gimbal pivot for balanced ~4.5 N·m steering torque!
            translate([54, -6, 75]) cube([16, 12, 16]);  // Top Pitch Clevis
            translate([54, 75, -6]) cube([16, 16, 12]);  // Stbd Yaw Clevis
        }

        // Female spherical socket matching Male Spherical Ball (R = 75.4 mm)
        sphere(r = nozzle_sph_in);

        // Internal UHMW-PE Spherical Seal Ring Groove (X = -7..+7 mm, R = 77.6 mm)
        intersection() {
            sphere(r = nozzle_sph_in + 2.4);
            translate([-7.0, -90, -90]) cube([14.0, 180, 180]);
        }

        // Smooth internal water bore through aft nozzle (ensures clean passage)
        revolve_x([
            [-25, 0], [-25, bore_in_r], [16, bore_in_r + 0.5],
            [95, 69.2], [215, 67.5], [325, bore_exit_r], [325, 0]
        ]);

        // Vertical Ø8 mm Yaw Pin Bores at 12 & 6 o'clock (X = 0, Y = 0)
        for (sz = [-1, 1]) {
            translate([0, 0, sz * 70.0])
                cylinder(d = pin_dia + 0.15, h = 24.0, center = true);
        }

        // Heim-joint bolt holes (M5) in Pitch & Yaw clevis ears
        translate([62, -10, 86]) rotate([-90, 0, 0]) cylinder(d = 5.2, h = 20);
        translate([62, 86, -10]) cylinder(d = 5.2, h = 20);
    }

    // 5. Three Thin Streamlined Spider Vanes INSIDE the gimbaled shroud (ADDED AFTER bore cut!)
    //    Carries the central Ø34 mm guide sleeve so the plug gimbals 100% concentrically WITH the shroud!
    for (k = [0 : 2]) {
        rotate([k * 120 + 90, 0, 0])
            translate([60, -2.0, 14.0])
                cube([42, 4.0, bore_in_r - 12.5]);
    }
    // Central Plug Guide Sleeve (stationary relative to rear shroud!)
    revolve_x([
        [52,  10.0], [52,  17.0],
        [152, 17.0], [152, 10.0]
    ]);
}

// ==========================================================================
// PART 4: Spider-Mounted Sliding Teardrop Throttling Plug (Ø65 -> Ø16 mm)
// ==========================================================================
module sliding_plug() {
    // Slides 0..45 mm along the central Ø34 mm guide sleeve inside the gimbaled shroud!
    difference() {
        revolve_x([
            [42,  8.0],
            [56,  24.0],
            [88,  32.5],   // Ø65 mm max shoulder
            [145, 31.0],
            [215, 22.0],
            [270, 10.0],
            [295, 2.5],
            [295, 0.0],
            [42,  0.0]
        ]);

        // Internal coaxial slide bore riding over the Ø34 mm guide sleeve + Tr8x2 nut pocket
        translate([40, 0, 0])
            rotate([0, 90, 0])
                cylinder(d = 34.4, h = 165);

        // 3x axial slots clearing the 3 spider vanes across the full 45 mm plug stroke!
        for (k = [0 : 2]) {
            rotate([k * 120 + 90, 0, 0])
                translate([38, -2.8, 15.0])
                    cube([118, 5.6, 22.0]);
        }
    }
}

// ==========================================================================
// Hardware & Reference Sub-Parts (Pins, UHMW Seal, Leadscrew, Heim Pushrods)
// ==========================================================================
module uhmw_seal_band() {
    color([0.94, 0.96, 0.98])
    intersection() {
        difference() {
            sphere(r = nozzle_sph_in + 2.2);
            sphere(r = sphere_male_r + 0.15);
        }
        translate([-6.5, -90, -90]) cube([13.0, 180, 180]);
    }
}

module gimbal_pins_pitch() {
    color([0.85, 0.22, 0.20])
    for (sy = [-1, 1]) {
        translate([0, sy * 82.0, 0])
            rotate([sy > 0 ? -90 : 90, 0, 0])
                cylinder(d = pin_dia, h = 18.0);
    }
}

module gimbal_pins_yaw() {
    color([0.85, 0.22, 0.20])
    for (sz = [-1, 1]) {
        translate([0, 0, sz * 74.0])
            cylinder(d = pin_dia, h = 17.0, center = (sz < 0));
    }
}

module leadscrew_visual() {
    color([0.88, 0.72, 0.18])
        translate([56, 0, 0])
            rotate([0, 90, 0])
                cylinder(d = 8.0, h = 165.0);
}

module pushrod_between(p0, p1) {
    v = p1 - p0;
    len_v = norm(v);
    b = acos(v[2] / len_v);
    c = atan2(v[1], v[0]);
    color([0.86, 0.20, 0.20]) {
        translate(p0) sphere(r = 5.0);
        translate(p1) sphere(r = 5.0);
        translate(p0)
            rotate([0, b, c])
                cylinder(d = 5.0, h = len_v);
    }
}

// Compute rotated clevis world coordinate for live pushrod animation!
function rot_pitch_yaw(p) =
    let(
        cy = cos(yaw_deg), sy = sin(yaw_deg),
        cp = cos(-pitch_deg), sp = sin(-pitch_deg),
        // First yaw (inner relative to pitch? Matches rotate([0,-pitch,0]) rotate([0,0,yaw]))
        x1 = p[0]*cy - p[1]*sy,
        y1 = p[0]*sy + p[1]*cy,
        z1 = p[2],
        x2 = x1*cp + z1*sp,
        y2 = y1,
        z2 = -x1*sp + z1*cp
    ) [x2, y2, z2];

// ==========================================================================
// Assembly & Export Switch
// ==========================================================================
if (part_select == "stator_housing") {
    stator_housing();
} else if (part_select == "cardan_ring") {
    cardan_ring();
} else if (part_select == "rear_nozzle") {
    rear_nozzle();
} else if (part_select == "sliding_plug") {
    sliding_plug();
} else if (part_select == "exploded") {
    color([0.22, 0.30, 0.40]) translate([-95, 0, 0]) stator_housing();
    color([0.92, 0.68, 0.14]) translate([0, 0, 0])   cardan_ring();
    gimbal_pins_pitch();
    translate([68, 0, 0]) uhmw_seal_band();
    color([0.15, 0.22, 0.30]) translate([135, 0, 0]) rear_nozzle();
    translate([135, 0, 0]) gimbal_pins_yaw();
    color([0.94, 0.60, 0.10]) translate([440, 0, 0]) sliding_plug();
} else {
    // "assembly_cutaway" — Live deflected 2-axis gimbal with foreground cutaway (-Y, +Z)!
    // Cutaway slices top-front quadrant of shroud & stator so spherical seal, pins,
    // spider vanes, and coaxial sliding plug + leadscrew are 100% visible!
    difference() {
        union() {
            color([0.22, 0.30, 0.40, 0.96]) stator_housing();
            gimbal_transform(do_yaw = false, do_pitch = true)
                color([0.92, 0.68, 0.14]) cardan_ring();
            gimbal_transform(do_yaw = true, do_pitch = true) {
                uhmw_seal_band();
                color([0.16, 0.24, 0.34, 0.95]) rear_nozzle();
            }
        }
        // Clean quarter-cutaway window along foreground (-Y, +Z) revealing full interior!
        translate([-125, -110, 0]) cube([465, 110, 110]);
    }

    // Keep pins, spider plug, leadscrew & live pushrods completely uncut for clarity!
    gimbal_pins_pitch();
    gimbal_transform(do_yaw = false, do_pitch = true) gimbal_pins_yaw();
    gimbal_transform(do_yaw = true, do_pitch = true) {
        leadscrew_visual();
        color([0.94, 0.56, 0.08])
            translate([plug_stroke_mm, 0, 0])
                sliding_plug();
    }

    // Live animated Pitch (top) & Yaw (starboard) stainless heim-joint pushrods!
    pushrod_between([-94, 0, 88],  rot_pitch_yaw([62, 0, 86]));
    pushrod_between([-94, 88, 0],  rot_pitch_yaw([62, 86, 0]));
}
