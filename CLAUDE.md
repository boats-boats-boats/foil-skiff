# CLAUDE.md — Project Context & Engineering Guidelines for `foil-skiff`

## 1. Project Overview
`foil-skiff` (**FoilSkiff**) is an R&D, hydrodynamics, and fabrication repository for a **submerged lifting-body battery-fuselage ("Flying-Keel Pod") electric hydrofoiling catamaran tender** (`10 ft` inflatable tunnel-catamaran class, e.g., `True Kit Navigator 300` / `Discovery 330`).

Primary reference document: [`electric-foiling-dinghy-guide.md`](electric-foiling-dinghy-guide.md).

---

## 2. Core Engineering Rules & Physical Constraints (Do Not Violate)

When generating hydrodynamic calculations, CAD/molds, 3D-print fairings, battery layouts, controller wiring, or BOMs in this repository, always adhere to these physical and electrical constraints:

1. **Primary Architecture — Longitudinal Flattened Lifting Battery-Fuselage ("Flying-Keel Pod"):**
   * Orient submerged battery cells **longitudinally (fore-and-aft)** inside a streamlined flattened lifting fuselage (`~1.3 m × 220 mm × 80 mm`, `~26 L` displacement = `~26.6 kg` Archimedes seawater buoyancy) paired with **thin `10%`-thick high-aspect carbon outer wings** (`~2,200 cm²` effective area).
   * **Never pack batteries spanwise inside a thick full-span wing (`3,400+ cm²`, `t/c ≥ 14%`):** excessive wetted area doubles profile drag above `12 knots`.
   * House the battery, BMS, `Flipsky 75100` `VESC` controller(s) (heat-sunk directly to the seawater-cooled shell), and tailcone **`Flipsky 65161`** pod(s) inside the same submerged fuselage so **zero high-current (`100–150 A`) DC cables run up the foil strut**.
   * **Mandatory Submerged-Pod Safety Package:**
     1. **`20 mm` sacrificial Kevlar/elastomer crush-nose bumper** ahead of a `5 mm` `G10` bulkhead for rock/debris impact protection.
     2. **CNC double-O-ring anodized endcap/flange**, internal **optical/conductivity moisture leak sensor** wired to a cockpit alarm, and **`0.5 bar` pressure-relief burst valve**.
     3. **Dry deck-level charging umbilical** routed up inside the hollow `NACA 0024` strut so the `IP68` fuselage seal is never opened for routine charging.
     4. **Assisted Hinged Retraction (`3:1` Dyneema tackle or marine gas strut)** to lift the `~36–42 kg` pod into the central catamaran tunnel for beaching, plus **`350–450 mm` cruise immersion depth** to prevent sudden buoyancy loss from wave-trough surface breaching.

2. **Compact `4–13 kg` Low-`Kv` Drives & `100 Kv` vs. `120 Kv` Selection (`Flipsky 65161`):**
   * **Primary Pick:** Twin `IP68` sealed pods (**`2 × Flipsky 65161`** or **`2 × Maytech MTO65162`**, `4–6 kg` total, `6–10 kW` cont., `200–240 lbf`) + **`2 × Flipsky 75100` `VESC`** for zero-hardware `360°` CAN-bus differential power steering.
   * **Winding Selection Rule:**
     * On **`16S LiFePO4` (`49.5 V` loaded):** Pick **`100 Kv`** (`~4,160 RPM` loaded—matching `12S` `120 Kv`!) for `+20%` torque per phase amp (`14.3` vs `11.9 N·m` @ `150 A`), `~30%` less copper heat, and `16–19.5 kn` foiling (`21+ kn` w/ field weakening). Pick **`120 Kv`** on `16S` only if targeting `20–23 kn` on small `6"`-pitch props (prefer `75200` ESC for heavy 2-up takeoffs).
     * On **`14S LiFePO4` (`43.5 V` loaded, strictly `<50 V`):** Pick **`120 Kv`** (`~4,385 RPM`, `17–20 kn`).
     * **Never use `195 Kv`** for direct-drive propellers (jet pumps only), and **never use `350–500 Kv` RC boat motors** without a planetary reduction gearbox.
   * **Zero-Fab Turnkey Alternative:** Twin steerable CNC aluminum azimuth pods (**`2 × W-30`** on `730 mm` tall shafts, `13.2 kg`, `6.4 kW` peak, `110 lbf`, built-in `±85°` electric steering).
   * **Ultra-Budget Open-Can Alternative (`2 × T63100`, `120–140 Kv`):** Must verify epoxy-potted stator + sealed magnets, upgrade to full/hybrid ceramic bearings, keep out of beach sand, and fresh-water flush after every saltwater run.

3. **`14S` vs. `16S LiFePO4` ESC Voltage-Ceiling Rule:**
   * Stock `12S LiPo` ESCs (e.g., `APISQUEEN U30` and some `W-30` pods) max out at **`50.4 V`**, whereas `16S LiFePO4` rests at `~53.2 V` and charges to **`55.2–58.4 V`**.
   * Either build **`14S LiFePO4` (`44.8 V` nom. / `48.3–49.0 V` charge, strictly `<50 V`)** to retain stock `12S` ESCs, **OR** run **`16S LiFePO4`** strictly with **`75 V`-rated `VESC` controllers (`Flipsky 75100` / `75200`)** with `VESC Tool` `Max Duty Cycle` (`~82%–85%`) protecting motor windings.

4. **Round Outboard Shaft Tube Fairing Requirement (`NACA 0024`):**
   * A bare round shaft tube (`Ø36 mm × 0.50 m` submerged, $C_D \approx 1.15$) generates **`63 lbf` (`281 N`) drag and wastes `~2.4 kW` at `10 knots`**, while ventilating the prop. Any round-tube test mule (e.g., stripped `Hangkai M2200`) above `6 knots` **must** be wrapped in a `150 mm` chord **`NACA 0024` airfoil fairing** (`~90%` drag reduction, `2,135 W` saved at `10 kn`).

5. **Dry Alternative & Pump-Jet Constraints:**
   * For rocky-beach simplicity or `16–22 kn` max speed, use the **dry `60 mm` 2-piece carbon/E-glass composite "Battery-Floor"** (`16S EVE LF105` `36.7 mm` flat cells = `560 × 840 × 37 mm`) preserving the catamaran air tunnel.
   * **Pump-Jet (`APISQUEEN BP100`, `10 kW`, `72–86 V`, `158 lbf`):** Cannot be paired with hydrofoils (flush intake sucks air when the hull lifts); specify strictly for prop-free `3"`-draft beaching or detachable jet-surfboard cassettes.
