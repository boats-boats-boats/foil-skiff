# FoilSkiff — Visual Design Atlas & 3D CAD Model Gallery

A complete visual companion to [`electric-foiling-dinghy-guide.md`](electric-foiling-dinghy-guide.md), [`BREAKAWAY_WING_SOCKET.md`](BREAKAWAY_WING_SOCKET.md), and [`DESIGN_TRADE_OFFS.md`](DESIGN_TRADE_OFFS.md), pairing **interactive millimeter-scale 3D `.stl` CAD models** (orbitable directly in GitHub's native 3D viewer), **multi-material OpenSCAD 3D renderings (`renders/`)**, and **25 mathematically-scaled engineering SVG drawings (`diagrams/`)**.

* **Primary Hull:** **`True Kit Navigator 300`** (`300 × 155 cm`, `60 cm` inside beam, `Ø460 mm` continuous closed-bow tubes, factory `Tru-Alu` rigid aluminum transom, `31 kg` bare weight, `500 kg` capacity).
* **Primary Wing & Actuation:** **Deep-Submerged Split STOL Flaperons (`1,000 + 2×250 cm²`, `400 mm` deep)** with **`2×` `IP67` brushless servos sealed INSIDE the Flying-Keel Pod** (`ZERO` boxes above the top Hard Deck, `ZERO` external strut pushrods, `ZERO` surface-piercing wave-slam wings!).
* **Secondary Wing:** **Flush-Nested Top-Deck Switchblade (`+1,300 cm²` roof-nested blades + `1,250 cm²` lower thin wing)** for maximum `22 kn` speed & `30.8 nm` range.
* **Secondary Open-Bow Hull Reference:** **`True Kit Discovery 330`** / **`Takacat LX`** (open square bow enabling a full rigid Bow-to-Transom O-Frame).

---

## Part I — Interactive 3D CAD Models & Renderings

| # | 3D CAD Model (Click on GitHub to Orbit in 3D) | Role | Key Highlight Shown |
| :---: | :--- | :---: | :--- |
| **1** | [`models/01_navigator300_stol_flaperons.stl`](models/01_navigator300_stol_flaperons.stl) | **`Navigator 300`** *(PRIMARY)* | **Bow-Contoured Hard Deck & Under-Hull Hybrid C-Frame** + **`6 mm` Dyneema Bow Sling** + **Deep-Submerged Split STOL Flaperons** (internal pod servos, `0` deck boxes, clean wave zone!) |
| **2** | [`models/02_switchblade_pod.stl`](models/02_switchblade_pod.stl) | *Secondary Wing Pod* | **Flush-Nested Top-Deck Switchblade Wing** (`+1,300 cm²` deployed + `70 mm` carbon overhang bridge + contoured bow-bent under-plate) |
| **3** | [`models/03_stol_flaperon_pod.stl`](models/03_stol_flaperon_pod.stl) | *Primary Pod Cutaway* | **Split STOL Flaperons (`+18°` / `-8°` differential bank)** with **translucent pod showing `2×` internal `IP67` servos, `Ø8 mm` sealed shafts & `ESP32`/IMU** (`ZERO` boxes above flush Hard Deck!) |
| **4** | [`models/04_navigator300_retracted_beaching.stl`](models/04_navigator300_retracted_beaching.stl) | **`Navigator 300`** *(PRIMARY)* | **Retracted `86.5°` Parallelogram Beaching Mode** tucked cleanly beneath the `Tru-Alu` transom (`~130–140 mm` / `5.1–5.5"` sand clearance; **True `90°` Upper/Lower Fold Channels** tuck wings inside **`220 mm` dart** right between the `250 mm` rails!) |
| **5** | [`models/05_discovery330_oframe_stol.stl`](models/05_discovery330_oframe_stol.stl) | `Discovery 330` *(Secondary Hull)* | Secondary open-bow reference showing **Bow-Contoured Hard Deck + Full Rigid O-Frame** + identical swappable **Split STOL Flaperon Pod** (also applies to `Takacat LX`) |
| **6** | [`models/06_navigator300_lr_8020_sweetspot.stl`](models/06_navigator300_lr_8020_sweetspot.stl) | **`Navigator 300`** *(LR 80/20 Tandem)* | **Long-Range 80/20 Tandem (`65–79 nm`):** **2 inline low-sit ergonomic chairs** on flush L-Tracks + `4×` easy blades + Split STOL + **Single `65161` (`10"` CNC prop)** + `AR 13.5` wing + `60 mm` Deck Pack & Bow Dodger |
| **7** | [`models/07_navigator300_lr_max_range.stl`](models/07_navigator300_lr_max_range.stl) | **`Navigator 300`** *(Full LR Solo)* | **Full 4-Swap Long-Range Solo (`70–84 nm`):** **1 low-sit pilot chair slid over CoG** (open aft gear/extender bay!) + `2×` Recessed Center Struts + `AR 14` Flush Switchblade + Single `65161` (`10"` prop) & Bow Dodger |
| **8** | [`models/08_lr_pod_closeup.stl`](models/08_lr_pod_closeup.stl) | *Long-Range Pod Cutaway* | **Internal Cutaway of Long-Range Single-Prop Pod:** translucent shell showing `2×` recessed center struts, swappable cartridges (`5.4 kWh` `LiFePO4` / `8.2 kWh` `NMC`), `1×` `75100` VESC, internal rudder servo & `10"` 2-blade CNC prop |
| **9** | [`models/09_modular_hard_deck_seating.stl`](models/09_modular_hard_deck_seating.stl) | **`Navigator 300`** *(Modular Deck)* | **Modular Hard Deck Seating System:** Bow-contoured 2-piece Hard Deck + **flush recessed twin L-Track rails (`390 mm` spacing)** + **2 quick-release low-sit ergonomic chairs** + right-hand armrest wireless helm pod (`0` trip edges when empty!) |
| **10** | [`models/10_morphing_stol_staggerwing_pod.stl`](models/10_morphing_stol_staggerwing_pod.stl) | *Dual-Mode Wing Upgrade* | **100% Internal-Pod Morphing STOL-to-Staggerwing Sled:** `90 mm` pod encloses a **Wet-Slot / Dry-Bay Vertical Elevator Sled (`70 mm` stroke, `0` external arms!)** switching between **DOWN STOL (`6–8 mm` slot)** & **UP Protected Staggerwing (`57 mm` / `4–5×` above wake!)** via `Tr10×2` leadscrew + `2×` direct-drive `IP68` servos ON sled |
| **11** | [`models/11_split_keel_jet_ccv_pod.stl`](models/11_split_keel_jet_ccv_pod.stl) | *Prop-Free Jet-CCV Pod* | **`70/30` Split Keel Jet-CCV Pod (`1,450 mm` LOA):** Rigid front/mid chassis (`1,120 mm`, `5.38 kWh` @ CoG, `Flipsky 65161` + `Ø140` BLI pump-jet, twin `Ø80 mm` zero-seal mag-drive CCV pumps + pop-up inboard roll-trim doors) + **330 mm 2-axis gimbaled hollow ring-nozzle** carrying a **spider-mounted sliding plug** (`~60%` η, `25–26 nm` — `3.4×` `BP100`!) |
| **12** | [`models/ccv_magdrive_pump_80mm.scad`](models/ccv_magdrive_pump_80mm.scad) | *Printable Bench-Test Pump* | **`Ø80 mm` Mag-Drive Centrifugal CCV Pump (`5.5 L/s @ 0.50 bar`):** `6`-blade backward-curved impeller (`N_q ≈ 52`), logarithmic volute, `608` ceramic wet bearing, and `6× N52` mag-coupling across a `1.5 mm` solid barrier (`0` shaft seals!) — includes 4 ready-to-print `1:1` STLs |
| **13** | [`models/gimbal_nozzle_150mm.scad`](models/gimbal_nozzle_150mm.scad) | *Close-Up Gimbal CAD* | **2-Axis Spherical Ring-Nozzle Gimbal & Spider-Mounted Plug:** Male/female spherical `UHMW-PE` seal (`R = 75 mm`), external `Ø179 mm` Cardan ring (`±15°` Y / `±6°` P, zero collision), heim-joint servo pushrods & `3`-vane spider-mounted sliding plug (`Tr8×2` leadscrew) — includes 4 printable `1:1` STLs |
| **14** | [`models/12_quad_swath_tandem_jet.stl`](models/12_quad_swath_tandem_jet.stl) | *Quad-SWATH Tandem Jet* | **4-Corner Twin-Torpedo Wide-Staggered Tandem SWATH (`ZERO` Moving Tail Parts!):** Over-tube cross-beams (bypasses `~3"` tunnel!), `4×` corner buoyant wing-struts (`820 mm` open middle + anti-ventilation fences), `2× Ø115×1,500 mm` battery torpedoes, `65/35` staggered tandem foils (`1.76 m`, `+140 mm` vertical stagger) & twin fixed `Ø108 mm` rear pump-jets (`~31 nm` @ `12 kn`) |
| **15** | [`models/13_center_keel_tip_float_ufoil.stl`](models/13_center_keel_tip_float_ufoil.stl) | *2-Wing 4-Float U-Foil* | **Central Keel + `2` Staggered U-Foils + `4` Corner Tip Floats + Above-Water Tie-Bars (`NO` Outer Torpedoes!):** `4 × 24 L` corner floats (top: torpedo; side: `620×400 mm` rounded rect) tied fore-to-aft by **dry above-water carbon rails** (`0 N` water drag!), `65/35` staggered `1.80 m` U-foils (`+130 mm` vertical stagger), all `4` floats wet @ `6–10 kn` and **`+30 mm` DRY @ `12–15.5 kn`** (`~33 nm` @ `12 kn`) |

---

### 1. PRIMARY: `True Kit Navigator 300` + Split STOL Flaperons (Internal Pod Servos)
*Exact `True Kit Navigator 300` geometry (`300 × 155 cm`, `60 cm` inside beam, `Ø460 mm` continuous closed curved bow tube, factory notched `Tru-Alu` aluminum transom) fitted with a **bow-contoured, upward-curved 2-piece Hard Deck** (`ZERO` boxes above deck!), **bow-contoured `Tru-Alu` Transom-Clamped Hybrid C-Frame Ski-Plate**, **`6 mm` Dyneema Bow-D-Ring Tieback Sling**, `4×` `60 × 9 mm` side-straddling blades (clean wave zone — zero surface-piercing wing!), and **Submerged `26 L` Flying-Keel Pod with `1,000 + 2×250 cm²` Split STOL Flaperons & internal `IP67` pod servos**.*

![OpenSCAD 3D Render: Primary True Kit Navigator 300 + Split STOL Flaperons](renders/01-navigator300-stol-3d.png)

<details>
<summary><strong>View Annotated 3D Isometric Engineering Callouts (SVG)</strong></summary>

![Annotated 3D Isometric CAD: Primary True Kit Navigator 300](diagrams/00-navigator300-3d-cad.svg)

</details>

---

### 2. Secondary Wing Track (Max Range/Speed): Flush-Nested Top-Deck Switchblade Pod
*Two `680 × 105 × 13 mm` solid UD carbon blades (`1.58 m` span, `AR ≈ 15`) sweep cleanly between the `x = 170 mm` and `x = 960 mm` side-straddling blades, locking beneath a `70 mm` carbon overhang bridge at takeoff (`6.7 kn`) and folding `100%` flush into the fuselage roof above `9 kn` (`0 cm²` extra wet area, `0` wave-crest wing slam, `30.8 nm` @ `15.5 kn`, `32.3 lbf` best pod drag @ `22 kn`).*

![OpenSCAD 3D Render: Flush-Nested Top-Deck Switchblade Wing Pod](renders/02-switchblade-pod-3d.png)

<details>
<summary><strong>View Annotated 3D Isometric Engineering Callouts (SVG)</strong></summary>

![Annotated 3D Isometric CAD: Flush-Nested Top-Deck Switchblade Wing Pod](diagrams/06-switchblade-3d-cad.svg)

</details>

---

### 3. PRIMARY Pod Close-Up: Split STOL Flaperons + Internal Pod Servos (`ZERO` Deck Boxes!)
*Compact `1,000 cm²` main wing paired with independent port (`+18°`) and starboard (`-8°`) `250 cm²` Junkers external slotted flaperons. Translucent pod shell reveals the **`2×` `IP67` `70–80 kg·cm` brushless servos, `Ø8 mm` double-O-ring direct-drive stainless shafts, `ESP32`/`BNO085` 6-DOF IMU, and seawater-cooled `75100` `VESC`s sealed inside the pod**—leaving the **bow-contoured Hard Deck `100%` flush** with zero protruding boxes and zero external strut pushrods!*

![OpenSCAD 3D Render: Primary Split STOL Flaperon Pod with Internal Servos](renders/03-stol-flaperon-pod-3d.png)

<details>
<summary><strong>View Annotated 3D Isometric Engineering Callouts (SVG)</strong></summary>

![Annotated 3D Isometric CAD: Primary Split STOL Flaperon Pod with Internal Servos](diagrams/07-stol-flaperons-3d-cad.svg)

</details>

---

### 4. PRIMARY Retracted Beaching Mode: `86.5°` Parallelogram Fold on `True Kit Navigator 300`
*Tunnel-level view of the **`True Kit Navigator 300`** resting on flat beach sand (`Z = -232 mm`). One press of **`BEACH MODE`** rotates both Foil & Strut `IP68` servo pins to `0%`, the closed-loop Dyneema pulley folds all wings **true `90°` flush inside the `13 mm` upper & `12 mm` lower pod channels (`220 mm` total width — zero overhang!)**, and all `4×` `60 × 9 mm` side-straddling blades fold `86.5°` aft beside the `95 mm` pod right **between the `250 mm` under-hull rails** beneath the factory `Tru-Alu` transom (**`~130–140 mm` / `5.1–5.5"` clear above flat sand** within the `300 cm` LOA).*

![OpenSCAD 3D Render: True Kit Navigator 300 Retracted 86.5-deg Beaching Mode](renders/04-navigator300-retracted-3d.png)

<details>
<summary><strong>View Annotated 3D Isometric Engineering Callouts (SVG)</strong></summary>

![Annotated 3D Isometric CAD: True Kit Navigator 300 Retracted Beaching Mode](diagrams/08-navigator300-retracted-3d.svg)

</details>

---

### 5. Secondary Open-Bow Hull Reference: `True Kit Discovery 330` + Contoured O-Frame
*For open-bow catamarans (`True Kit Discovery 280/330/400`, `Takacat LX`), the identical swappable Split STOL Flaperon Flying-Keel Pod mounts to a bow-contoured rigid **O-Frame** wrapping around both open ends.*

![OpenSCAD 3D Render: Secondary True Kit Discovery 330 + Contoured O-Frame](renders/05-discovery330-oframe-3d.png)

<details>
<summary><strong>View Annotated 3D Isometric Engineering Callouts (SVG)</strong></summary>

![Annotated 3D Isometric CAD: Secondary True Kit Discovery 330 + Contoured O-Frame](diagrams/11-discovery330-oframe-3d-cad.svg)

</details>

---

### 6. Long-Range 80/20 Sweet Spot (`65–79 nm`): `Navigator 300` + Single `65161` (`10"` Prop) + `AR 13.5` Split STOL + `60 mm` Dual-Pack Deck
*Hitting **`65 nm` @ `15.5 kn` / `79 nm` @ `12 kn`** on `100%` fire-safe **`10.76 kWh` `LiFePO4`** (`5.38 kWh` pod + `5.38 kWh` dry inside the `60 mm` bow-contoured Battery-Floor Hard Deck) while **keeping `4×` easy side-straddling blades (`5.5"` sand clearance) and Primary Split STOL Flaperon chop control**. Adds the **Single Centerline `65161` + `10"×11"` 2-blade CNC prop + internal-servo tail rudder** (nearly half the total range gain!), wider `AR 13.5` (`1.50 m`) main wing, and a low-profile curved bow spray dodger.*

![OpenSCAD 3D Render: Long-Range 80/20 Sweet Spot Navigator 300](renders/06-navigator300-lr-8020-3d.png)

<details>
<summary><strong>View Annotated 3D Isometric Engineering Callouts (SVG)</strong></summary>

![Annotated 3D Isometric CAD: Long-Range 80/20 Sweet Spot Navigator 300](diagrams/13-navigator300-lr-8020-3d-cad.svg)

</details>

---

### 7. Full 4-Swap Long-Range Max Efficiency (`70–84 nm` `LiFePO4` / `67 nm` Single-Pod `NMC`): `2×` Recessed Center Struts + `AR 14` Flush Switchblade
*All four Long-Range Hydro Package swaps combined on **`True Kit Navigator 300`**: **`2×` hollow `100 × 18 mm` recessed center struts** (`9.1 lbf`, rear drafts in front wake), **`AR 14` (`1.55 m`) wing + Flush-Nested Switchblade** (`0 cm²` extra wet area closed), **Single Centerline `65161` + `10"` 2-blade CNC prop + tail rudder**, and curved bow spray dodger — cutting energy burn to **`118 Wh/nm` @ `12 kn` (`84 nm`)** and **`142 Wh/nm` @ `15.5 kn` (`70 nm`)** on `10.8 kWh` `LiFePO4` (or **`67 nm` @ `12 kn`** from a single `8.2 kWh` `21700 NMC` pod keeping the slim `28 mm` Hard Deck!).*

![OpenSCAD 3D Render: Full 4-Swap Long-Range Max Efficiency Navigator 300](renders/07-navigator300-lr-max-range-3d.png)

<details>
<summary><strong>View Annotated 3D Isometric Engineering Callouts (SVG)</strong></summary>

![Annotated 3D Isometric CAD: Full 4-Swap Long-Range Max Efficiency Navigator 300](diagrams/14-navigator300-lr-max-range-3d-cad.svg)

</details>

---

### 8. Long-Range Single-Prop Pod Close-Up Cutaway (`2×` Recessed Struts, Internal Rudder Servo & `10"` 2-Blade CNC Prop)
*Close-up translucent cutaway showing the **`60 mm` bow-contoured Battery-Floor Hard Deck** (`100%` flush top, zero boxes!), **`2×` `100 × 18 mm` recessed center tandem struts** with `300 mm` T-heads and offset gold pivot pins, swappable `IP68` cartridges, **`1×` seawater-cooled `Flipsky 75100` `VESC`**, `ESP32`/`BNO085` IMU, **internal aft `IP67` rudder servo** driving the orange tailfin rudder flap, and the **Single `65161` + `10"×11"` 2-blade CNC prop**.*

![OpenSCAD 3D Render: Long-Range Single-Prop Pod Internal Cutaway](renders/08-lr-pod-closeup-3d.png)

<details>
<summary><strong>View Annotated 3D Isometric Engineering Callouts (SVG)</strong></summary>

![Annotated 3D Isometric CAD: Long-Range Single-Prop Pod Internal Cutaway](diagrams/15-lr-pod-closeup-3d-cad.svg)

</details>

---

### 9. Modular Hard Deck Seating System: Flush Recessed L-Tracks + 1 or 2 Ergonomic Low-Sit Chairs
*Close-up of the **Bow-Contoured 2-Piece Hard Deck** outfitted with **twin flush-recessed marine L-Track rails (`390 mm` spacing, `1,570 mm` long)** that sit `100%` flush with the top carbon skin (zero trip edges when chairs are unclipped!). Tool-free `900 kgf` spring-loaded double-stud quick-release fittings let you switch in `5 seconds` between **Solo Long-Range (`1 chair` slid right over midship CoG)**, **Tandem 2-Up (`2× 424 mm` inline chairs cleanly inside the `600 mm` tunnel)**, and **Open Cargo/Beaching Deck (`0 chairs`)**—with the wireless thumb-throttle & mini-joystick integrated right onto the pilot's right-hand armrest.*

![OpenSCAD 3D Render: Modular Hard Deck with Flush L-Tracks and 2 Low-Sit Chairs](renders/09-modular-deck-seating-3d.png)

<details>
<summary><strong>View Annotated 3D Isometric Engineering Callouts (SVG)</strong></summary>

![Annotated 3D Isometric CAD: Modular Hard Deck Seating System](diagrams/17-modular-deck-seating-3d-cad.svg)

</details>

---

### 10. Dual-Mode Upgrade: 100% Internal-Pod Morphing STOL-to-Staggerwing Elevator Sled
*Keeps `100%` of the morphing mechanism inside a **`90 mm` Flying-Keel Pod (`ZERO` external swing-arms, `ZERO` belts/gears, `ZERO` sliding dry-hull seals!)**. A dedicated `96 mm`-long **free-flooding internal wing-box** (bounded by twin curved green watertight bulkheads) houses twin `Ø10 mm` guide rods and a self-locking **`Tr10×2` stainless leadscrew (`0 W` hold)** moving the aluminum elevator sled `70 mm` straight vertically between **Mode 1 DOWN** (far port side: `Z = -35 mm`, optimal `6–8 mm` Venturi STOL slot, `CL_max ≈ 2.0`, still `10 mm` above pod belly) and **Mode 2 UP** (foreground starboard side: `Z = +35 mm`, `57 mm` / `4–5×` above the Main Wing's `~12 mm` turbulent wake, shielded behind the fixed lower Main Wing, still `10 mm` below pod roof!). Both individually waterproof **`IP68` billet pitch servos** ride **directly ON the sled** (direct-driving the `Ø8 mm` flaperon shafts through flush silicone cheek wiper skirts), while only a stationary cable passes through a **static bulkhead gland** into the dry battery/VESC/IMU bay (`ZERO` boxes above the Hard Deck!).*

![OpenSCAD 3D Render: 100% Internal-Pod Morphing STOL-to-Staggerwing Sled](renders/10-morphing-stol-staggerwing-3d.png)

<details>
<summary><strong>View Annotated 3D Isometric Engineering Callouts (SVG)</strong></summary>

![Annotated 3D Isometric CAD: 100% Internal-Pod Morphing STOL-to-Staggerwing Sled](diagrams/19-morphing-stol-staggerwing-3d-cad.svg)

</details>

---

### 11. Prop-Free Foiling Track: `70/30` Split Keel Jet-CCV Pod (Gimbaled Ring-Nozzle + Mag-Drive CCV)
*Full `1,450 mm` prop-free foiling pod documented in [`SPLIT_KEEL_JET_CCV_POD.md`](SPLIT_KEEL_JET_CCV_POD.md): **`1,120 mm` rigid front/mid chassis** houses `5.38 kWh` cartridges dead-on Wing CoL (`X_CoG = 545 mm`), all `4×` blades (`160 mm` ahead of the gimbal split), twin `Ø80 mm` zero-seal mag-drive CCV pumps feeding `2 × 250 mm` inboard wing-root plenums (foreground Starboard pop-up door OPEN for `88 N·m` differential roll + proverse yaw!), and an inline `Flipsky 65161` (`100 Kv`) driving a `Ø140 mm` BLI pump-jet. Behind the gold spherical gimbal (`±15°` Yaw / `±6°` Pitch), a **`330 mm` hollow converging ring-nozzle** (`Ø132 mm` bore) doubles as a power-off ring-tail stabilizer and carries a **spider-mounted sliding teardrop plug** concentrically (`~60%` η, **`~25–26 nm`** @ `15.5 kn` — `3.4×` the `BP100` hull jet!).*

![OpenSCAD 3D Render: 70/30 Split Keel Jet-CCV Pod](renders/11-split-keel-jet-ccv-pod-3d.png)

<details>
<summary><strong>View Annotated 3D Isometric Engineering Callouts (SVG)</strong></summary>

![Annotated 3D Isometric CAD: 70/30 Split Keel Jet-CCV Pod](diagrams/25-split-keel-jet-ccv-pod-3d-cad.svg)

</details>

---

### 12. Printable Bench-Test Unit: `Ø80 mm` Mag-Drive Centrifugal CCV Pump (`5.5 L/s @ 0.50 bar`)
*Parametric `1:1` OpenSCAD design ([`models/ccv_magdrive_pump_80mm.scad`](models/ccv_magdrive_pump_80mm.scad)) with 4 manifold printable STLs (`impeller`, `volute`, `bulkhead_lid`, `drive_hub`) for tub bench-testing. Fits in a `~56 mm` stack inside the `96 mm` keel pod with **zero rotary shaft seals** (`6× 15×10×5 mm N52` magnets across a solid `1.5 mm` waterproof barrier transmit `>4.5 N·m` vs. `1.42 N·m` running torque at `2,350 RPM`).*

![OpenSCAD 3D Cutaway: Ø80 mm Mag-Drive Centrifugal CCV Pump](renders/12-ccv-magdrive-pump-80mm-3d.png)

---

### 13. Close-Up Gimbal Mechanics: 2-Axis Spherical Ring-Nozzle & Spider-Mounted Sliding Plug
*Parametric `1:1` OpenSCAD mechanical assembly ([`models/gimbal_nozzle_150mm.scad`](models/gimbal_nozzle_150mm.scad)) with 4 manifold printable STLs (`stator_housing`, `cardan_ring`, `rear_nozzle`, `sliding_plug`). Shows live **`+12°` Yaw / `+4°` Pitch** deflection across the stationary `R = 75.0 mm` male spherical ball, white `UHMW-PE` spherical seal band, gold external `Ø179 mm` Cardan ring (Pitch on 3/9 o'clock stationary fork pins; Yaw on 12/6 o'clock inward nozzle pins — mathematically collision-free!), red spherical heim-joint servo pushrods, and the `Ø65 → Ø16 mm` teardrop plug sliding on `3` internal spider vanes + `Tr8×2` leadscrew concentrically inside the pivoting shroud.*

![OpenSCAD 3D Close-Up Cutaway: 2-Axis Spherical Ring-Nozzle Gimbal](renders/13-gimbal-nozzle-cutaway-3d.png)

<details>
<summary><strong>View Exploded Mechanical Assembly (All Gimbal Parts Separated)</strong></summary>

![OpenSCAD 3D Exploded View: 2-Axis Spherical Ring-Nozzle Gimbal](renders/14-gimbal-nozzle-exploded-3d.png)

</details>

---

### 14. Zero-Moving-Parts Prop-Free Track: 4-Corner Twin-Torpedo Wide-Staggered Tandem SWATH (`Model 12`)
*Full `1:1` assembly documented in [`QUAD_SWATH_TANDEM_JET.md`](QUAD_SWATH_TANDEM_JET.md): mounts via **two over-tube aluminum cross-beam saddles** across the `Navigator 300`'s `Ø460 mm` tubes (`0` hull holes, completely bypasses the real `~3"` tunnel!). Four slim `NACA 0013` corner wing-struts (`220 × 28 mm`, `820 mm` open middle gap, horizontal red anti-ventilation fences) join **two sleek `Ø115 × 1,500 mm` battery torpedoes** (`2 × 2.7 kWh`, no 3rd center pod!) carrying **twin fixed `Ø108 mm` rear differential pump-jets** (`1.76 m` yaw lever arm, `0` moving tail parts!) and **wide-staggered `65/35` tandem foils** (`900 cm²` front-low + `500 cm²` rear-high `+140 mm` above front wake $\rightarrow$ `~5.8 kn` passive takeoff, `±35 cm` CoG freedom, **`~31 nm` @ `12 kn`**). Vertical `220 mm` strut slide-up + stern `QuickLok` launching wheels handle rocky beaching cleanly.*

![OpenSCAD 3D Render: 4-Corner Twin-Torpedo Wide-Staggered Tandem SWATH](renders/15-quad-swath-tandem-jet-3d.png)

<details>
<summary><strong>View Annotated 3D Isometric Engineering Callouts (SVG)</strong></summary>

![Annotated 3D Isometric CAD: 4-Corner Twin-Torpedo Wide-Staggered Tandem SWATH](diagrams/26-quad-swath-tandem-jet-3d-cad.svg)

</details>

---

### 15. 3-Stage 4-Float Staggered U-Foil: Central Keel + `2` Staggered U-Foils + `4` Tip Floats + Above-Water Tie-Bars (`Model 13`)
*Combines the **`-50%` lower body drag of a single `28 L` central keel pod** (`5.38 kWh` pack + twin fixed `Ø108 mm` rear differential pump-jets, **NO outer torpedoes!**) with **two wide-staggered `1.80 m` U-foils** (Front Main `65%` lift at `Z = -830 mm`; Rear Staggered `35%` lift `+130 mm` higher above front wake) bending up into `18 mm` lower vertical blades (with red anti-ventilation fences) topped by **four `24 L` corner tip floats** (`620 × 400 × 135 mm` — torpedo from above, rounded-corner rectangle from the side). **Above-water longitudinal carbon tie-bars (`Z = -175 mm`)** rigidly connect front and rear floats on each side (`+330 mm` dry in air = `0 N` water drag!), eliminating blade torsion and acting as continuous outer dock rub-rails: **`0–5 kn`** (`~100 kgf` 4-corner pre-lift), **`6–10 kn`** (all `4` floats wet for full passive pitch + roll stabilization), **`12–15.5 kn`** (all `4` floats **`+30 mm` DRY IN AIR** $\rightarrow$ **`~33 nm` @ `12 kn` / `~20.5 nm` @ `15.5 kn`**).*

![OpenSCAD 3D Render: Central Keel + Stepped Torpedo-Planform Tip-Float U-Foil](renders/16-center-keel-tip-float-ufoil-3d.png)

<details>
<summary><strong>View Annotated 3D Isometric Engineering Callouts (SVG)</strong></summary>

![Annotated 3D Isometric CAD: Central Keel + Stepped Torpedo-Planform Tip-Float U-Foil](diagrams/27-center-keel-tip-float-ufoil-3d-cad.svg)

</details>

---

## Part II — Scaled 2D Engineering Drawings (`diagrams/`)

### 11. 100% Internal-Pod Morphing STOL-to-Staggerwing Sled (Wet-Slot / Dry-Bay Mechanics & Wake Clearance)
![100% Internal-Pod Morphing STOL-to-Staggerwing Wet-Slot Elevator Sled](diagrams/20-morphing-stol-staggerwing.svg)

### 12. `2×` Recessed Center Struts & True `90°` Upper/Lower Fold-Channel Protection (Dual Servo-Pin Smart Divider)
![2x Recessed Center Struts and True 90-deg Upper/Lower Channel Linked-Fold Protection](diagrams/21-center-strut-asymmetric-loads.svg)

### 13. True `90°` Upper (`13 mm`) & Lower (`12 mm`) Fold Channels, Closed-Loop Dyneema Pulleys & Rotating Foil-Base Servo
![True 90-deg Upper and Lower Fold Channels, Dyneema Pulley Loop and Rotating Foil-Base Servo](diagrams/22-breakaway-socket-options.svg)

### 14. True `90°` Upper & Lower Fold Channels: All 3 Wing Tracks & `220 mm` Beaching Dart (Fits Between `250 mm` Rails!)
![True 90-deg Upper and Lower Fold Channels: All 3 Wing Tracks and 220 mm Beaching Dart](diagrams/23-breakaway-deployed-flaperons.svg)

### 15. Wet `IP68` Servo-Controlled Variable-Preload Roller Pins for Foils & Upper Struts (`0%` Fold / `50%` Reef / `100%` `0 W` Cruise)
![Wet IP68 Servo-Controlled Variable-Preload Roller Pins for Foils and Struts](diagrams/24-servo-preload-pins-mechanics.svg)

### 16. Modular Hard Deck Seating Ergonomics & CoG Trim (Solo 1-Chair, Tandem 2-Chair & Flush L-Track Detail)
![Modular Hard Deck Seating Ergonomics and L-Track Detail](diagrams/18-modular-seating-ergonomics.svg)

### 17. Long-Range (`60–75+ nm`) Hydro Package Swaps & Battery Recipes Comparison
![Long-Range Hydro Package Swaps and Battery Recipes](diagrams/16-long-range-hydro-packages.svg)

### 18. PRIMARY Wing Cross-Section: Submerged Split STOL Flaperons & Internal Pod Servos
![Staggerwing vs. STOL External Slotted Flaperon Cross-Sections](diagrams/02-stol-flaperons-cross-section.svg)

### 19. Flying-Keel Pod Internal Cutaway (`26 L` Swappable Cartridges, Internal Servos, Seawater Cooling & Safety)
![Flying-Keel Pod Internal Cutaway](diagrams/09-swappable-cartridge-cutaway.svg)

### 20. Secondary Wing: Flush-Nested Top-Deck Switchblade Wing (Top-Down Closed vs. Deployed)
![Flush-Nested Switchblade Top-Down Geometry](diagrams/01-switchblade-wing-topdown.svg)

### 21. Contoured Bow-Bent Hard Deck & Under-Hull Coupling Options (`Navigator 300` Primary + Magnets + `Discovery 330` O-Frame + OEM Slot)
![Drop-In Rigid Spine Floor Coupling Options](diagrams/03-spine-floor-coupling-options.svg)

### 22. Grounding Kick-Up Kinematics: Why a Single Central Mast Fails vs. 4-Bar Parallelogram
![Single Central Mast Collision vs. 4-Bar Parallelogram Kick-Up](diagrams/04-grounding-kickup-geometry.svg)

### 23. Strut Architecture & Folded Stack-Up Clearance Inside the `Navigator 300` Tunnel (`600 mm` Wide × `230 mm` High)
![Strut Architecture & Folded Beaching Stack-Up](diagrams/05-strut-folded-stackup.svg)

### 24. Integrated Battery-Hull Architecture Comparison on `True Kit Navigator 300`
![Integrated Battery-Hull Architecture Comparison](diagrams/10-alt-architectures-comparison.svg)

### 25. Rejected Concept Physics: Why Surface-Piercing Step-Out Wings Fail in Chop (Forward & Deep-Aft)
![Rejected Concept Physics: Surface-Piercing Step-Out Wing Wave-Slam Hazards](diagrams/12-rejected-concepts-physics.svg)

---

## Part III — Regenerating or Modifying the Parametric CAD & Drawings

All `.stl` models, `.svg` technical drawings, and OpenSCAD `.png` renderings are generated deterministically with **zero Python third-party dependencies** (plus optional `openscad` CLI for shaded PNG renders):

```bash
# Regenerate all 15 scaled 2D engineering SVGs (pure Python 3)
python3 diagrams/generate_diagrams.py

# Regenerate all 10 binary 3D .stl CAD models, 10 annotated 3D SVGs, and 10 OpenSCAD PNGs
python3 models/generate_cad.py
```

* **OpenSCAD (macOS / Linux / Docker):** Install natively (`brew install --cask openscad`) or run headless via Docker (`docker run --rm -v "$PWD":/work openscad/openscad ...`).
* **3D Printing Tabletop Models:** Import any file in `models/*.stl` into PrusaSlicer / Bambu Studio / Cura and scale to **`1:15` (`6.7%`)** or **`1:10` (`10%`)** (all coordinates are native `1:1` millimeters).
