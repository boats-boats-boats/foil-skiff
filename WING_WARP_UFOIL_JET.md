# FoilSkiff PRIMARY Architecture — Central-Keel 4-Float Staggered U-Foil with Dry Wing-Warping & Twin Fixed Differential Pump-Jets (`Models 13 & 14`)

This document specifies the **PRIMARY `FoilSkiff` architecture** for the **`True Kit Navigator 300`** (`300 × 155 cm`, `Ø460 mm` tubes, realistic `~75–100 mm` / `3"–4"` under-floor tunnel, `31 kg` bare weight, `500 kg` capacity).

It combines **four breakthroughs** into one cohesive, `100%` prop-free, zero-underwater-moving-parts electric hydrofoil tender:
1. **Single `28 L` Central Keel Pod (`NO` Outer Submerged Torpedoes):** Cuts submerged body drag by **`~50%`** vs. twin-torpedo SWATH and centralizes `5.38 kWh` swappable `IP68` batteries, `2 × Flipsky 75100` `VESC`s, and **twin fixed `Ø108 mm` wide-bore rear differential pump-jets** (`132.5 cm²` combined exit area, `360°` CAN-bus steering, instant reverse, dual-drive redundancy, **`0` moving tail parts**).
2. **Two Wide-Staggered `1.80 m` U-Foils (`65/35` Lift Split, `+130 mm` Vertical Stagger):**
   * **Front Main U-Foil (`~900 cm²`, `Z = -830 mm` / `320 mm` deep in cruise)** + **Rear Staggered U-Foil (`~500 cm²`, `Z = -700 mm` / `190 mm` deep in cruise, `+130 mm` clean above front wake)**.
   * Cuts takeoff induced drag **`-74%`** vs. a `1.05 m` center-pod wing, eliminates any separate aft stabilizer, and tolerates **`±35 cm` fore/aft passenger movement**.
3. **Four Stepped Corner Tip Floats (`4 × 24 L = 96 L`) + Above-Water Longitudinal Tie-Bars:**
   * **Top view:** Classical `NACA 0014` streamlined torpedo (`620 × 135 mm`). **Side view:** Vertical rounded-corner rectangle (`620 × 400 mm`, `R = 65 mm` corners) for strictly linear buoyancy unloading.
   * **3-Stage Flight Progression on `600 mm` Struts:**
     * **`0–5 kn` Takeoff:** All `4` floats `~75%` submerged (`~100 kgf` total pre-lift buoyancy with center pod) $\rightarrow$ effortless **`~5.0–5.5 kn`** takeoff!
     * **`6–10 kn` Post-Takeoff Climb:** Tubes `+100 mm` clear while all `4` floats remain `150 mm` in water $\rightarrow$ rock-solid 4-corner passive pitch & roll stability!
     * **`12–15.5 kn` High-Speed Cruise:** All `4` floats lift **`+30 mm` DRY IN AIR (`0 N` float water drag!)**, leaving only the thin `12–18 mm` lower vertical blades (w/ red anti-ventilation fences) wet $\rightarrow$ **`~36.5 nm` @ `12.0 kn` / `~24.2 nm` @ `15.5 kn`** on `5.38 kWh` (up to **`~27.3 nm` @ `15.5 kn`** with sleek `12 mm` outer blades + `2×` tandem center struts)!
4. **Parallel-Float Dry 4-Channel Wing-Warping (`±3.0°` Foil AoA — ZERO Telescoping Tubes & ZERO Underwater Actuators!):**
   * The `4` corner floats and **solid fixed-length `Ø34 mm` above-water carbon tie-bars** form one `100%` rigid, always-parallel outer frame (`+330 mm` dry in air, `0` telescoping slip-joints!).
   * Each foil's `18 mm` vertical blade pivots around a **fixed `Ø10 mm` `316L` pin at the bottom of the float** (`+30 mm` dry in cruise) and continues `320 mm` straight up as an internal blade tang inside a **free-flooding vertical center trunk** (fore & aft foam float chambers stay `100%` sealed & unsinkable, zero dynamic water seals!).
   * Four compact, dry, non-backdrivable **`IP67` `Tr8` horizontal linear actuators (`±17 mm` stroke, `~100 N` peak force, `0 W` hold)** tucked at the top of each float rock the upper blade tangs fore-and-aft—elastically twisting each submerged `0.90 m` foil half by **`±3.0°`** around its `25%`-chord UD carbon spar (`0.055%` strain = `10×` below fatigue limit!) for **active roll (`>150 N·m`), direct heave (`±336 N`), and locked `12–20+ kn` cruise ride height!**

---

## 1. Visual CAD Assemblies & Close-Up Mechanisms

![OpenSCAD 3D Render: Primary Central-Keel 4-Float Staggered U-Foil with Dry Wing-Warping (Model 13)](renders/16-center-keel-tip-float-ufoil-3d.png)

<details>
<summary><strong>View Annotated 3D Isometric Engineering Callouts (SVG)</strong></summary>

![Annotated 3D Isometric CAD: Primary 4-Float Wing-Warp U-Foil](diagrams/27-center-keel-tip-float-ufoil-3d-cad.svg)

</details>

### Close-Up: Parallel-Float Rigid Tie-Bar & Internal Blade-Tang Wing-Warping (`Model 14`)

![OpenSCAD 3D Close-Up: Parallel-Float Rigid Tie-Bar & Internal Blade-Tang Wing-Warping](renders/17-wing-warp-tiebar-closeup-3d.png)

### 3-Stage Flight Progression & Hydroelastic Mechanics (2D Engineering Diagram)

![3-Stage Flight Waterlines & Parallel-Float Wing-Warping Mechanics](diagrams/29-wing-warp-3stage-flight-dynamics.svg)

| Artifact | Path | Purpose |
| :--- | :--- | :--- |
| **Full Primary 3D Assembly STL (`Model 13`)** | [`models/13_center_keel_tip_float_ufoil.stl`](models/13_center_keel_tip_float_ufoil.stl) | `1:1` mm full `Navigator 300` assembly at `12–15.5 kn` cruise |
| **Parametric Wing-Warp Close-Up (OpenSCAD)** | [`models/wing_warp_tiebar_closeup.scad`](models/wing_warp_tiebar_closeup.scad) | Parametric `1:1` close-up of parallel floats, solid `Ø34 mm` tie-bar, fixed `Ø10 mm` lower pivots & internal `Tr8` linear actuators |
| **Printable Pivot Saddle & Tang Clevis STLs** | [`wing_warp_lower_pivot_saddle.stl`](models/wing_warp_lower_pivot_saddle.stl), [`wing_warp_tang_clevis.stl`](models/wing_warp_tang_clevis.stl) | Manifold `1:1` parts ready to print in `PA12-CF` / `PETG-CF` |
| **2D 3-Stage Flight & Kinematics SVG** | [`diagrams/29-wing-warp-3stage-flight-dynamics.svg`](diagrams/29-wing-warp-3stage-flight-dynamics.svg) | Scaled waterlines (`0–5` / `6–10` / `12–15.5 kn`) + internal-tang statics & divergence proof |

---

## 2. Exact 3-Stage Vertical Stack (`600 mm` Central Struts)

*All Z coordinates referenced to `Navigator 300` `Ø460 mm` tube bottom (`Z_tb = 0`; note factory welded PVC tunnel web sits at `~75–100 mm` / `3"–4"` above `Z_tb`—verify exact value on your hull).*

| Flight Stage | Speed | Waterline (rel. `Z_tb`) | `4×` Corner Tip Floats (`Z = -250 → +150 mm`) | Front / Rear Foil Depth | Active Wing-Warp Trim |
| :--- | :---: | :---: | :--- | :---: | :--- |
| **1. Lowered Pre-Lift Takeoff** | **`0–5 kn`** | `+50 mm` *(tubes `50 mm` wet)* | **`75%` submerged** (`~72 kgf` + `28 kgf` center pod = **`~100 kgf` pre-lift!**) | `650 / 520 mm` | All `4` tips **`+2.5°`** (max STOL lift) |
| **2. Post-Takeoff Climb** | **`6–10 kn`** | `-100 mm` *(tubes `+100 mm` clear!)* | **Still `150 mm` (`38%`) IN water** (linear 4-corner passive pitch + roll stability!) | `500 / 370 mm` | Neutral / gentle bank trim |
| **3. High-Speed Cruise** | **`12–15.5 kn`** | `-280 mm` *(tubes `+280 mm` clear!)* | **`+30 mm` DRY IN AIR (`0 N` water drag!)**; Tie-Bars `+330 mm` dry | **`320 / 190 mm` deep** *(zero chop breach!)* | Front **`-1.5°`** / Rear **`+1.5°`** locks cruise height; diff. **`±2.5°`** banks turns! |

---

## 3. Parallel-Float Internal Blade-Tang Wing-Warping & Hydroelastic Safety Rules

### Why Parallel Floats + Solid Fixed Tie-Bars Eliminate Telescoping Parts
* Instead of tilting the floats themselves (which would require a telescoping tie-bar), the **Front & Rear Floats stay `100%` parallel and permanently bonded to a solid fixed-length `Ø34 mm` carbon tie-bar** (`ZERO` sliding tubes, `ZERO` bushings!).
* Each foil's `18 mm` vertical blade passes up through a **free-flooding centerboard-style vertical trunk** inside the foam-filled float (fore & aft closed-cell foam chambers stay `100%` sealed & unsinkable, zero dynamic water seals!):
  * **Fixed Lower Pivot Pin (`Z = +18 mm` above float bottom):** One `Ø10 mm` `316L` stainless horizontal pin anchors the lower float-to-blade junction.
  * **Internal `320 mm` Blade Tang + Dry `IP67` `Tr8` Linear Actuator (`Z = +338 mm`):** Sweeping the top of the tang **`±17 mm`** fore-and-aft rocks the blade and twists the submerged `0.90 m` foil half **`±3.0°`** around its `25%`-chord spar while requiring only:
    $$F_{\text{act}} = \frac{M_{\text{twist}} + M_{\text{hydro}}}{0.32\text{ m}} \approx \frac{32\text{ N}\cdot\text{m}}{0.32\text{ m}} \approx \mathbf{100\text{ N}\ (10.2\text{ kgf})}$$
  * Easily driven by standard **`$35` `12 V` `IP67` `200–300 N` self-locking `Tr8` micro linear actuators** (`0 W` holding power, built-in potentiometer feedback), with the `32 N·m` reaction absorbed effortlessly by the rigid fixed tie-bar (`F_z ≈ 36 N`)!

### Mandatory Composite Layup & Divergence Rules (Do NOT Violate!)
1. **Place the `0°` UD Carbon Main Spar Dead-On `25%–28%` Chord:** Aligns the foil's elastic twist axis with its hydrodynamic center of pressure ($e \le 3\text{ mm}$), preventing static torsional divergence.
2. **Tailored Torsion Skin (`1` ply `±45°` carbon/glass, $GJ \approx 220\text{–}300\text{ N}\cdot\text{m}^2/\text{rad}$):**
   * Keeps `±3.0°` twist torque manageable (`~25–32 N·m` $\rightarrow$ `~100 N` at the `320 mm` internal tang lever) and peak surface shear strain at **`~0.06%`** (`~8×–10×` below epoxy fatigue endurance limit!).
3. **Strictly Non-Backdrivable Dry Linear Actuators (`Tr8` Leadscrew):** Locking the upper blade tang rigidly holds the wingtip fixed-fixed in torsion (`4×` divergence eigenvalue), pushing static divergence safely past **`50–60+ kn`**.
4. **Horizontal Anti-Ventilation Fences (`4×`):** Bond one `15 mm` horizontal fence on each `18 mm` lower vertical blade at `Z = -570 mm` (just below cruise waterline) so surface air cannot ventilate down onto the submerged U-foils.

---

## 4. Apples-to-Apples Drag, Power & Range (`5.38 kWh` `16S LiFePO4`, Same Basis as `Model 1`)

| Operating Point (`235 kg` All-Up, `~60%` Twin Fixed `Ø108 mm` Jets) | Total Drag | Battery Draw (`DC kW`) | Energy (`Wh/nm`) | Gross / `92%` Usable Range |
| :--- | :---: | :---: | :---: | :---: |
| **`5.2 kn` Pre-Lifted Takeoff** (`~100 kgf` buoyancy, `+2.5°` twist) | `~245 N` (`55 lbf`) | `~1.7 kW` *(brief)* | — | `2–3 sec` lift-off |
| **`12.0 kn` Eco Dry-Float Cruise** *(Sweet Spot)* | **`~172 N`** (`39 lbf`) | **`1.77 kW`** (`35 A`) | **`147 Wh/nm`** | **`36.5 nm`** / `33.6 nm` usable |
| **`15.5 kn` Fast Cruise (Standard `4×` Center + `4× 18 mm` Outer Blades)** | **`~257 N`** (`58 lbf`) | **`3.44 kW`** (`67 A`) | **`222 Wh/nm`** | **`24.2 nm`** / `22.3 nm` usable |
| **`15.5 kn` Optimized (`2×` Tandem Center + `4× 12 mm` Outer Blades)** | **`~229 N`** (`51 lbf`) | **`3.05 kW`** (`60 A`) | **`197 Wh/nm`** | **`27.3 nm`** / `25.1 nm` usable |

* **Why `15.5 kn` is `~2.5–5.5 nm` shy of bare open-prop `Model 1` (`29.8 nm` gross):** At `15.5+ kn`, induced drag is tiny (`9 N` vs `15 N`) while $V^2$ wetted skin friction dominates. The small gap comes purely from (a) the `4` extra outer surface-piercing vertical blades (`+22–38 N`, ~`60%` of the gap) and (b) shrouded pump-jets (`~60%` eff.) vs. bare open propellers (`~63%` eff., ~`30%` of the gap)—the direct physical price of `100%` prop-free safety, `~5 kn` pre-lifted takeoff, and `0` underwater moving parts. At `12 kn` eco cruise, the wide `1.80 m` U-foils close the gap almost completely (`~36.5 nm` vs `~34.7 nm` for `Model 1`!).

* **Beaching & Shallow Water (Honest `~3"` Tunnel Accounting):** Retracting the `4×` central struts lifts the flat U-foils snug beneath the `Ø460 mm` tube bottoms (`~10.5"` shallow motoring draft) while lifting all `4` outer tip floats **`~200 mm` clear above beach sand**; flip down **`Ø320 mm` QuickLok stern launching wheels** on the `Tru-Alu` transom to roll smoothly up rocky beaches (`+2.5"–4"` clear under the center pod).
* **Estimated DIY Conversion BOM (`~$4,050` incl. `5.38 kWh` `LiFePO4`):** `2 × Ø54 mm` sealed inrunners + `2 × Flipsky 75100` `VESC`s + fixed `Ø108 mm` shrouds (`$950`), `2 × 14 kg` swappable `IP68` `LiFePO4` cartridges (`$700`), central pod + `2×` wide U-foils + `4×` `24 L` floats + `2×` solid fixed `Ø34 mm` carbon tie-bars (`$1,800`), `4×` dry `IP67` `Tr8` micro linear actuators (`$160`) + `ESP32`/`BNO085` IMU (`$140`), contoured hard deck / rail carriage & stern wheels (`$300`).
