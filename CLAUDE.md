# CLAUDE.md — Project Context & Engineering Guidelines for `foil-skiff`

## 1. Project Overview
`foil-skiff` (**FoilSkiff**) is an R&D, hydrodynamics, and fabrication repository for a **Drop-In Rigid Spine Floor + Step-Out Flying-Keel Pod** (submerged lifting-body fuselage with swappable `IP68` battery cartridges + Upper "Step-Out" Booster Wing biplane hydrofoil) for `10 ft` inflatable tunnel-catamaran tenders (e.g., `True Kit Navigator 300` / `Discovery 330`, `Takacat LX`, `Saturn`, `Kaboat`).

Primary reference document: [`electric-foiling-dinghy-guide.md`](electric-foiling-dinghy-guide.md).

---

## 2. Core Engineering Rules & Physical Constraints (Do Not Violate)

When generating hydrodynamic calculations, CAD/molds, 3D-print fairings, battery layouts, controller wiring, or BOMs in this repository, always adhere to these physical and electrical constraints:

1. **Primary Architecture — Drop-In Rigid Spine Floor + Step-Out Flying-Keel Pod:**
   * **Drop-In Rigid Spine Floor (`25–35 mm` Thin 2-Piece Carbon/Aluminum) & Zero-Hole Coupling:** Both `True Kit` and `Takacat` have a continuous, permanently welded `~1.0–1.2 mm` PVC fabric tunnel ceiling underneath the stock air deck. Replace the drop-stitch air floor with a rigid 2-piece folding Spine Floor wedged directly onto that `1.2 mm` PVC web inside the tube pockets (`0` glue, `0` holes; universal `650 mm` Spine Core + swappable outer width strips). Connect top Spine Floor to the under-tunnel foil carriage without cutting the PVC web via:
     * **Full Bow-to-Transom Twin-Rail "O-Frame" Clamshell (`~2.5–3.5 kg`, Top Zero-Hole Pick for Open-Bow Cats):** For open-bow + open-transom hulls (`True Kit Discovery`, `Takacat LX`), wrap both ends with two `50 × 20 × 2.5 mm` `6061-T6` aluminum (or carbon) rails spaced `250–300 mm` apart (`3×–4×` lower bending moment, `220 mm` Flying-Keel Pod retracts *between* rails, splits at midship into `1.0 m` packable halves, Delrin breakaway shear pin).
     * **Open-Transom "C-Frame" Wrap-Around Spine (`~3.3–5.2 kg`):** For closed-bow + open-transom hulls (`True Kit Navigator 300`), a `180 × 30 × 3.5 mm` hollow box beam loops out the open transom `1.1 m` forward under the tunnel (upward lift compresses straight into Spine Floor).
     * **Through-Fabric Switchable Magnetic Clamp (`4 ×` `10 × 10 cm` `Magswitch`-style mechanical rotary `N52` or EPMs, `~800 kgf` total clamp across `~2.5 mm` gap):** Universal across open or closed transoms with built-in resettable reef-strike breakaway fuse; **mandatory rules:** sit Spine Floor directly on `1.2 mm` PVC (never through `100 mm` air deck), bond micro-ribbed rubber grip pads (`μ ≈ 0.65–0.80`), clip an aft transom Dyneema/stainless shear & safety bridle (never lose pod on breakaway), never use plain electromagnets, hermetically seal all `NdFeB`/steel keeper plates against saltwater, and run any `BNO085` IMU in 6-DOF (gyro+accel only) mode.
     * **Factory OEM Welded Centerboard Slot (`~1.0–1.5 kg`, OEM Only):** Single RF-welded `60 × 320 mm` slot + vertical PVC boot + split-neoprene spray gasket in the non-airtight tunnel web (airtight side tubes untouched); only for factory "Foil Edition" builds or dedicated modified hulls.
   * **Submerged Lifting Fuselage Bay + Swappable `IP68` Battery Cartridges:** Orient batteries **longitudinally (fore-and-aft)** inside a streamlined flattened lifting fuselage bay (`~1.3 m × 220 mm × 80 mm`, `~26 L` displacement = `~26.6 kg` Archimedes seawater buoyancy) as **two removable, factory-potted `IP68` `2.5–2.7 kWh` (`~14 kg` ea.) slide-in cartridges** (*Flitecell*-style, with blind-mate waterproof connectors + closed-cell foam dummy plug option for 1-cartridge solo hops) rather than a permanent monolithic sealed `30 kg` pack.
   * **Biplane Step-Out Wing Set + Optional `<$150` Auto-Trim:** Pair **sleek `10%`-thick high-aspect lower carbon wings (`1,300–1,400 cm²`)** with a fixed **Upper "Step-Out" Booster Wing (`+1,400 cm²` thick high-lift takeoff wing mounted `200–250 mm` higher on the `NACA 0024` strut)**. Both wings (`~2,750 cm²`) submerge for **`6.4 kn` lift-off** (`41%` lower takeoff power); above `9 kn`, the upper wing exits into dry air (`99.9%` drag elimination, `2.71 kW` / `30.8 nm` @ `15.5 kn`, passive mechanical ride-height stabilization). Optionally pair with a `<$150` `ESP32` + `BNO085` IMU + ToF auto-trim actuator (`±5°` on aft stabilizer) for effortless "push throttle and fly" cruising.
   * **Never use submerged longitudinal swing-wings** (persistent wetted area $S_{\text{wet}}$ & sideways blunt wingtip add `+33%–53%` cruise drag) and **never pack batteries spanwise inside a thick full-span wing (`3,400+ cm²`, `t/c ≥ 14%`)**.
   * House the battery cartridges, `Flipsky 75100` `VESC` controller(s) (heat-sunk directly to the seawater-cooled bottom skin), and tailcone **`Flipsky 65161`** pod(s) inside the same submerged fuselage so **zero high-current (`100–150 A`) DC cables run up the foil strut**.
   * **Mandatory Submerged-Pod & Step-Out Safety Package:**
     1. **Anti-ventilation strut fence collar (`~20 mm` horizontal carbon plate `50 mm` below the upper booster wing)** to prevent surface air from sucking down the strut onto the lower wing during the `8–9 kn` step-out breach.
     2. **`20 mm` sacrificial Kevlar/elastomer crush-nose bumper** ahead of a `5 mm` `G10` bulkhead for rock/debris impact protection.
     3. **CNC double-O-ring rear bay door** for swappable `IP68` cartridges, internal **optical/conductivity moisture leak sensor** wired to a cockpit alarm, and **`0.5 bar` pressure-relief burst valve**.
     4. **Dry deck-level charging umbilical** routed up inside the hollow `NACA 0024` strut for routine mothership charging without opening the bay door.
     5. **Assisted Hinged Retraction (`3:1` Dyneema tackle or marine gas strut)** in the Spine Floor's central trunk to lift the pod (`~37–43 kg` loaded / `~11–15 kg` empty) into the tunnel for beaching, plus **`350–450 mm` lower-pod cruise immersion depth** (placing the upper booster wing `100–150 mm` clear in dry air at cruise).

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
