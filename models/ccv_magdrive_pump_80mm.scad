// ==========================================================================
// FoilSkiff — Ø80 mm Mag-Drive Centrifugal CCV Pump (Bench-Test & Pod Unit)
// ==========================================================================
// Duty Point (per wing side):
//   Flow Rate:       5.5 L/s (330 L/min / 87 GPM)
//   Pressure Head:   0.50 bar (50 kPa / 5.1 m water head)
//   Speed:           ~2,350 RPM (Specific Speed N_q ≈ 52 — peak centrifugal eff.)
//   Power / Torque:  ~250 W hyd. / ~380 W elec. | 1.42 N·m shaft torque
//   Drive:           5065 Dry Brushless Outrunner (~140-200 Kv on 48 V / 16S)
//   Coupling:        6x 15x10x5 mm N52 Magnets across 1.5 mm solid barrier (0 shaft seals!)
//   Discharge:       60 x 8 mm (4.8 cm²) tangential wing-root plenum port
//   Total Stack:     ~56 mm tall (fits cleanly inside 80-96 mm FoilSkiff keel pod!)
//
// Print Material:    PA12-CF (Carbon Nylon) or PETG-CF, 0.16-0.20 mm layers,
//                    4 perimeters, 40% gyroid infill (100% solid on bulkhead_lid barrier)
// Hardware Required:
//   - 12x N52 Neodymium block magnets (15 x 10 x 5 mm), alternating N-S poles
//   - 1x  608 full-ceramic (Si3N4 / ZrO2) 8x22x7 mm bearing (wet impeller)
//   - 1x  Ø8 x 24 mm 316L stainless dowel pin (stationary wet stub shaft)
//   - 8x  M4 x 16 mm 316L SHCS + locknuts (perimeter volute flange)
//   - 1x  Ø106 x 2.5 mm Viton/EPDM O-ring (volute-to-bulkhead face seal)
//   - 4x  M4 x 10 mm SHCS (5065 motor mount) + 2x M4 grub screws (drive hub)
// ==========================================================================

/* [Part Selection] */
// Options: "assembly_cutaway", "impeller", "volute_lower", "bulkhead_lid", "drive_hub", "exploded"
part_select = "assembly_cutaway";

/* [Hydraulic & Impeller Parameters (mm)] */
impeller_od       = 80.0;    // Outer tip diameter (r2 = 40 mm)
impeller_eye_dia  = 44.0;    // Axial suction eye diameter (r1 = 22 mm)
blade_height      = 10.0;    // Axial channel height b2
num_blades        = 6;       // Backward-curved logarithmic vanes
blade_thick       = 2.4;     // Printable vane wall thickness
blade_sweep_deg   = 74.0;    // Backward wrap angle from eye to tip
front_shroud_t    = 2.0;     // Bottom impeller shroud ring thickness
backplate_t       = 6.8;     // Top impeller hub thickness (houses 5 mm magnets + cap)

/* [Volute & Wing-Root Discharge Parameters (mm)] */
volute_r_start    = 43.0;    // Cutwater / tongue radius (3 mm tip clearance)
volute_r_end      = 56.5;    // Max spiral radius before tangential outlet
volute_wall       = 3.2;     // Outer casing wall thickness
volute_clearance  = 1.2;     // Axial clearance above/below impeller
flange_od         = 128.0;   // Perimeter bolt flange OD
flange_bolt_bc    = 118.0;   // 8x M4 bolt circle
plenum_w          = 60.0;    // Wing-root internal duct width (tangential)
plenum_h          = 8.0;     // Wing-root internal duct height (4.8 cm^2)
plenum_len        = 34.0;    // Tangential outlet transition stub length

/* [Magnetic Coupling & Bulkhead Parameters (mm)] */
barrier_thick     = 1.5;     // Solid waterproof wall (ZERO shaft seals!)
mag_airgap        = 1.0;     // Running clearance on each side of barrier
mag_count         = 6;       // Alternating N-S poles
mag_pcd           = 52.0;    // Magnet pitch circle diameter
mag_l             = 15.2;    // Pocket length (15 mm magnet + 0.2 clearance)
mag_w             = 10.2;    // Pocket width  (10 mm magnet + 0.2 clearance)
mag_h             = 5.2;     // Pocket depth  (5 mm magnet + 0.2 clearance)

/* [Bearing & 5065 Dry Motor Parameters (mm)] */
bearing_od        = 22.15;   // 608 full-ceramic bearing press/slip fit
bearing_h         = 7.2;
stub_shaft_dia    = 8.0;     // Stationary 316L stainless pin in bulkhead
motor_shaft_dia   = 8.1;     // 5065 motor shaft bore
motor_mount_bc    = 30.0;    // Standard 5065 4x M4 mounting circle

$fn = 96;

// Derived Z-stack datums (Z = 0 is the flush pod belly face!)
z_belly        = 0.0;
z_vol_floor    = 3.0;                                       // Bottom wall thickness
z_imp_bot      = z_vol_floor + volute_clearance;            // 4.2 mm
z_imp_blade_b  = z_imp_bot + front_shroud_t;                // 6.2 mm
z_imp_blade_t  = z_imp_blade_b + blade_height;              // 16.2 mm
z_imp_top      = z_imp_blade_t + backplate_t;               // 23.0 mm
z_barrier_bot  = z_imp_top + mag_airgap;                    // 24.0 mm
z_barrier_top  = z_barrier_bot + barrier_thick;             // 25.5 mm
z_hub_bot      = z_barrier_top + mag_airgap;                // 26.5 mm
z_hub_top      = z_hub_bot + 11.0;                          // 37.5 mm
z_motor_base   = z_hub_top + 4.5;                           // 42.0 mm (motor can ~50 mm dia x 18-30 mm pancake)

// ==========================================================================
// Helper: 2D Logarithmic Spiral Volute Profile & Backward-Curved Vane
// ==========================================================================
function volute_r(deg) = volute_r_start + (volute_r_end - volute_r_start) * pow(deg / 360.0, 0.92);

module volute_cavity_2d(extra_r = 0) {
    steps = 72;
    pts = [for (i = [0 : steps - 1])
        let(a = i * 360.0 / steps,
            r = volute_r(a) + extra_r)
        [r * cos(a), r * sin(a)]
    ];
    polygon(pts);
    // Clean tangential discharge channel leaving smoothly at angle 0 toward +Y
    // Inner wall tangent to r_start (43 mm), outer wall at r_end (56.5 mm) -> 13.5 mm wide x 20 mm tall passage
    translate([volute_r_start - extra_r, -2.0])
        square([(volute_r_end - volute_r_start) + 2.0 * extra_r, plenum_len + 26.0], center = false);
}

module backward_blade_2d() {
    r1 = impeller_eye_dia / 2.0 + 0.5;
    r2 = impeller_od / 2.0 - 0.2;
    n  = 24;
    // Spiral centerline curving backward (negative angle for CCW rotation)
    top_pts = [for (i = [0 : n])
        let(t = i / n,
            r = r1 + (r2 - r1) * t,
            ang = -blade_sweep_deg * pow(t, 1.15),
            // approximate normal offset
            nx = -sin(ang),
            ny =  cos(ang))
        [r * cos(ang) + (blade_thick/2) * nx, r * sin(ang) + (blade_thick/2) * ny]
    ];
    bot_pts = [for (i = [n : -1 : 0])
        let(t = i / n,
            r = r1 + (r2 - r1) * t,
            ang = -blade_sweep_deg * pow(t, 1.15),
            nx = -sin(ang),
            ny =  cos(ang))
        [r * cos(ang) - (blade_thick/2) * nx, r * sin(ang) - (blade_thick/2) * ny]
    ];
    polygon(concat(top_pts, bot_pts));
}

module magnet_pockets(z_base, h_pocket) {
    for (k = [0 : mag_count - 1]) {
        rotate([0, 0, k * 360 / mag_count])
            translate([mag_pcd / 2.0, 0, z_base + h_pocket / 2.0])
                cube([mag_w, mag_l, h_pocket], center = true);
    }
}

module magnets_visual(z_base) {
    for (k = [0 : mag_count - 1]) {
        col = (k % 2 == 0) ? [0.86, 0.22, 0.22] : [0.16, 0.48, 0.88];
        color(col)
        rotate([0, 0, k * 360 / mag_count])
            translate([mag_pcd / 2.0, 0, z_base + 2.5])
                cube([10.0, 15.0, 5.0], center = true);
    }
}

// ==========================================================================
// PART 1: Ø80 mm Backward-Curved Wet Centrifugal Impeller (Printable 1:1)
// ==========================================================================
module ccv_impeller(show_magnets = false) {
    difference() {
        union() {
            // 1. Lower front shroud ring (leaves Ø44 mm suction eye open)
            translate([0, 0, z_imp_bot])
                linear_extrude(front_shroud_t)
                    difference() {
                        circle(d = impeller_od);
                        circle(d = impeller_eye_dia);
                    }

            // 2. Six backward-curved logarithmic vanes
            translate([0, 0, z_imp_blade_b - 0.1])
                linear_extrude(blade_height + 0.2)
                    for (k = [0 : num_blades - 1])
                        rotate([0, 0, k * 360 / num_blades])
                            backward_blade_2d();

            // 3. Upper solid backplate & magnet carrier disk
            translate([0, 0, z_imp_blade_t])
                cylinder(d = impeller_od, h = backplate_t);

            // 4. Hydrodynamic intake nose cone guiding axial eye flow radially
            translate([0, 0, z_imp_blade_b])
                cylinder(d1 = 14.0, d2 = 28.0, h = blade_height);
        }

        // 608 Full-Ceramic Bearing Bore (top-loaded into backplate/cone)
        translate([0, 0, z_imp_top - bearing_h - 3.0])
            cylinder(d = bearing_od, h = bearing_h + 3.5);
        // Stub shaft clearance hole
        translate([0, 0, z_imp_blade_b - 1.0])
            cylinder(d = stub_shaft_dia + 2.5, h = blade_height + backplate_t + 2.0);

        // 6x N52 Magnet Pockets (recessed 1.0 mm below top face; pot with marine epoxy!)
        magnet_pockets(z_imp_top - mag_h - 0.8, mag_h + 1.0);
    }
    if (show_magnets) {
        magnets_visual(z_imp_top - mag_h - 0.4);
    }
}

// ==========================================================================
// PART 2: Logarithmic Spiral Volute Casing + Flush Belly Intake + Wing Plenum
// ==========================================================================
module volute_lower() {
    h_tot = z_barrier_bot;
    chan_w = volute_r_end - volute_r_start; // 13.5 mm tangential discharge width
    difference() {
        union() {
            // Outer spiral casing wall + integral tangential diffuser wall
            translate([0, 0, z_belly])
                linear_extrude(h_tot)
                    volute_cavity_2d(extra_r = volute_wall);

            // Top perimeter bolt flange ring (8x M4)
            translate([0, 0, h_tot - 6.0])
                cylinder(d = flange_od, h = 6.0);

            // Clean wing-root mating flange collar at end of tangential outlet
            translate([volute_r_start - 8.0, plenum_len + 18.0, z_belly])
                cube([chan_w + 16.0, 6.0, h_tot]);
        }

        // Main internal spiral wet cavity + smooth tangential discharge duct (all walls >= 3.2 mm!)
        translate([0, 0, z_vol_floor])
            linear_extrude(h_tot - z_vol_floor + 0.5)
                volute_cavity_2d(extra_r = 0);

        // Open discharge exit face through the mating collar
        translate([volute_r_start, plenum_len + 14.0, z_vol_floor])
            cube([chan_w, 14.0, h_tot - z_vol_floor - 2.0]);

        // 2x M4 wing-root plenum flange mounting holes
        for (ox = [volute_r_start - 4.0, volute_r_end + 4.0]) {
            translate([ox, plenum_len + 16.0, h_tot * 0.5])
                rotate([-90, 0, 0])
                    cylinder(d = 4.3, h = 10.0);
        }

        // Flush Belly Suction Eye (Ø44 mm)
        translate([0, 0, -1.0])
            cylinder(d = impeller_eye_dia, h = z_vol_floor + 2.0);

        // Viton O-ring groove on top mating flange (Ø106 x 2.5 mm)
        translate([0, 0, h_tot - 1.9])
            difference() {
                cylinder(d = 109.0, h = 2.2);
                cylinder(d = 103.5, h = 2.4);
            }

        // 8x M4 perimeter flange bolt holes
        for (k = [0 : 7]) {
            rotate([0, 0, k * 45 + 22.5])
                translate([flange_bolt_bc / 2.0, 0, h_tot - 7.0])
                    cylinder(d = 4.3, h = 8.5);
        }
    }

    // Integrated Flush Belly Debris Screen (5 streamlined ribs)
    intersection() {
        translate([0, 0, z_belly])
            cylinder(d = impeller_eye_dia + 2, h = z_vol_floor);
        union() {
            cylinder(d = 11.0, h = z_vol_floor);
            for (k = [0 : 4]) {
                rotate([0, 0, k * 72])
                    translate([0, -1.2, z_belly])
                        cube([impeller_eye_dia / 2.0 + 1, 2.4, z_vol_floor]);
            }
        }
    }
}

// ==========================================================================
// PART 3: Solid 1.5 mm Waterproof Containment Bulkhead Lid (ZERO Shaft Seals!)
// ==========================================================================
module bulkhead_lid() {
    flange_h = 6.0;
    difference() {
        union() {
            // Outer structural flange matching volute
            translate([0, 0, z_barrier_bot])
                cylinder(d = flange_od, h = flange_h);

            // Dry-side motor mounting bridge standoffs (clear the rotating dry magnet hub!)
            for (k = [0 : 3]) {
                rotate([0, 0, k * 90 + 45])
                    translate([44.0, 0, z_barrier_top])
                        cylinder(d = 10.0, h = z_motor_base - z_barrier_top);
            }
            // Top 5065 motor mounting ring plate
            translate([0, 0, z_motor_base - 4.0])
                cylinder(d = 98.0, h = 4.0);

            // Wet-side stationary stub-shaft boss (holds 316L Ø8 mm pin for ceramic 608 bearing!)
            translate([0, 0, z_imp_top - bearing_h - 1.5])
                cylinder(d = 14.0, h = z_barrier_bot - (z_imp_top - bearing_h - 1.5) + 0.5);
        }

        // Recess dry-side containment pocket down to exact 1.5 mm waterproof barrier thickness!
        translate([0, 0, z_barrier_top])
            cylinder(d = impeller_od + 6.0, h = flange_h + 2.0);

        // Central open window in top motor ring for 5065 shaft & dry hub ventilation
        translate([0, 0, z_motor_base - 5.0])
            cylinder(d = 20.0, h = 6.0);

        // Wet-side Ø8.0 mm blind press-fit socket for 316L stub shaft (does NOT pierce barrier!)
        translate([0, 0, z_imp_top - bearing_h - 2.0])
            cylinder(d = stub_shaft_dia, h = z_barrier_bot - (z_imp_top - bearing_h - 2.0) - 0.5);

        // 8x M4 perimeter bolt holes
        for (k = [0 : 7]) {
            rotate([0, 0, k * 45 + 22.5])
                translate([flange_bolt_bc / 2.0, 0, z_barrier_bot - 1.0])
                    cylinder(d = 4.3, h = flange_h + 2.0);
        }

        // 4x M4 5065 motor mounting holes on top plate
        for (k = [0 : 3]) {
            rotate([0, 0, k * 90])
                translate([motor_mount_bc / 2.0, 0, z_motor_base - 5.0])
                    cylinder(d = 4.3, h = 6.0);
        }
    }
}

// ==========================================================================
// PART 4: Dry-Side N52 Magnet Drive Hub (Clamps to Ø8 mm 5065 Motor Shaft)
// ==========================================================================
module drive_hub(show_magnets = false) {
    hub_h = z_hub_top - z_hub_bot;
    difference() {
        union() {
            translate([0, 0, z_hub_bot])
                cylinder(d = 74.0, h = hub_h - 3.0);
            // Central shaft clamping boss
            translate([0, 0, z_hub_bot])
                cylinder(d = 24.0, h = hub_h + 3.0);
        }

        // Ø8 mm motor shaft bore
        translate([0, 0, z_hub_bot - 1.0])
            cylinder(d = motor_shaft_dia, h = hub_h + 5.0);

        // 2x M4 grub-screw cross holes
        for (ang = [0, 90]) {
            rotate([0, 0, ang])
                translate([0, 0, z_hub_top - 1.0])
                    rotate([0, 90, 0])
                        cylinder(d = 3.4, h = 15.0);
        }

        // 6x N52 Magnet Pockets facing DOWN toward the 1.5 mm waterproof barrier
        magnet_pockets(z_hub_bot - 0.2, mag_h + 0.4);
    }
    if (show_magnets) {
        magnets_visual(z_hub_bot + 0.2);
    }
}

// ==========================================================================
// Phantom Reference Parts (Dry 5065 Brushless Motor + Ceramic Bearing)
// ==========================================================================
module phantom_5065_motor() {
    color([0.22, 0.28, 0.36, 0.72])
        translate([0, 0, z_motor_base])
            cylinder(d = 50.0, h = 24.0); // Compact pancake 5065/5045 outrunner
    color([0.75, 0.78, 0.82])
        translate([0, 0, z_hub_bot + 1.0])
            cylinder(d = 8.0, h = z_motor_base - z_hub_bot + 10.0);
}

module ceramic_bearing_ref() {
    color([0.92, 0.92, 0.95])
        translate([0, 0, z_imp_top - bearing_h - 2.5])
            difference() {
                cylinder(d = 22.0, h = 7.0);
                cylinder(d = 8.0, h = 7.2);
            }
}

// ==========================================================================
// Assembly & Export Switch
// ==========================================================================
if (part_select == "impeller") {
    translate([0, 0, -z_imp_bot]) ccv_impeller(false);
} else if (part_select == "volute_lower") {
    volute_lower();
} else if (part_select == "bulkhead_lid") {
    translate([0, 0, -z_barrier_bot]) bulkhead_lid();
} else if (part_select == "drive_hub") {
    translate([0, 0, -z_hub_bot]) drive_hub(false);
} else if (part_select == "exploded") {
    color([0.16, 0.24, 0.34]) volute_lower();
    translate([0, 0, 26]) color([0.06, 0.56, 0.78]) ccv_impeller(true);
    translate([0, 0, 52]) color([0.62, 0.68, 0.74]) bulkhead_lid();
    translate([0, 0, 80]) color([0.92, 0.62, 0.12]) drive_hub(true);
    translate([0, 0, 108]) phantom_5065_motor();
} else {
    // "assembly_cutaway" — clean 90-deg foreground cutaway (-X, -Y) leaving tangential outlet 100% intact!
    difference() {
        union() {
            color([0.16, 0.24, 0.34, 0.96]) volute_lower();
            color([0.68, 0.74, 0.80, 0.92]) bulkhead_lid();
        }
        translate([-95, -95, -2]) cube([95, 95, 75]);
    }
    difference() {
        color([0.06, 0.56, 0.78]) ccv_impeller(true);
        translate([-80, -80, z_imp_blade_t + 1.2]) cube([80, 80, 12]);
    }
    ceramic_bearing_ref();
    difference() {
        color([0.92, 0.62, 0.12]) drive_hub(true);
        translate([-80, -80, z_hub_bot - 1]) cube([80, 80, 20]);
    }
    phantom_5065_motor();
}
