# CLAUDE.md — Project Context & Engineering Guidelines for `foil-skiff`

## 1. Project Overview
`foil-skiff` (**FoilSkiff**) is an R&D, hydrodynamics, and fabrication repository for **lightweight, power-steered `48 V` electric, hydrofoiling, and integrated battery-floor inflatable catamaran tenders** (`10 ft` tunnel-catamaran class, e.g., `True Kit Navigator 300` / `Discovery 330`).

Primary reference document: [`electric-foiling-dinghy-guide.md`](electric-foiling-dinghy-guide.md).

---

## 2. Core Engineering Rules & Physical Constraints (Do Not Violate)

When generating hydrodynamic calculations, CAD/3D-print fairings, battery layouts, controller wiring, or BOMs in this repository, always adhere to these physical and electrical constraints:

1. **Prioritize Compact `4–13 kg` Low-`Kv` (`60–150 Kv`) Drives with Built-In or Differential Power Steering:**
   * Avoid heavy `15–26 kg` industrial outboard conversions (`Motenergy ME1304` + donor gas leg) on a `31 kg` inflatable catamaran transom unless heavy yacht hip-towing is the sole priority.
   * **Primary Pick:** Twin `IP68` submerged direct-drive e-foil pods (**`2 × Flipsky 65161`** or **`2 × Maytech MTO65162`**, `100 Kv`, `4–6 kg` total, `6–10 kW` cont., `200–240 lbf`) + **`2 × Flipsky 75100` `VESC`** mounted directly on foil struts—giving zero-hardware `360°` differential power steering via CAN-bus joystick at half the cost and `1/4` the weight of an industrial outboard.
   * **Zero-Fab Turnkey Pick:** Steerable CNC aluminum azimuth pods (**`2 × W-30`** `730 mm` tall shafts or **`1 × 5–6 kW`** USV azimuth pod) with built-in `±85°` electric steering and wireless remote.
   * **Low-Speed Bollard Pick:** **`2 × APISQUEEN U30`** (`4.0 kW`, `132 lbf` / `60 kgf`, `33 lbf/kW`, `5.3 kg`) for `4–11 kn` silent cruising and docking.
   * **Never specify high-`Kv` (`350–500 Kv`) RC boat motors** without a dedicated planetary reduction gearbox—they lack torque at marine propeller speeds (`2,500–5,500 RPM`).

2. **`14S` vs. `16S LiFePO4` ESC Voltage-Ceiling Rule:**
   * Many hobby/ROV marine ESCs (including stock `APISQUEEN U30` `12S LiPo` ESCs and some `36–48 V` white-label `W-30` azimuth pods) have a hard **`50.4 V` maximum input rating**.
   * A standard `16S LiFePO4` pack (`51.2 V` nominal) rests at `~53.2 V` and charges to **`55.2–58.4 V`** (`3.45–3.65 V/cell`)—exceeding `50.4 V` stock ESCs and leaving unsafe headroom on `60 V` MOSFETs.
   * **Mandatory Rule:** Either build a **`14S LiFePO4` pack (`44.8 V` nom. / `48.3–49.0 V` charge @ `3.45–3.50 V/cell`, strictly `<50.4 V` and under ISO `50 V`)** to retain stock `12S` ESCs, **OR** use a standard **`16S LiFePO4` pack (`51.2 V` nom.)** paired strictly with **`75 V`-rated `VESC` controllers (`Flipsky 75100` / `75200`)** with `VESC Tool` `Max Duty Cycle` (`~82%–85%`) and `Max Current` limits protecting the motor windings.

3. **Round Outboard Shaft Tube Fairing Requirement (`NACA 0024`):**
   * A bare round shaft tube (`Ø36 mm × 0.50 m` submerged, $C_D \approx 1.15$) generates **`63 lbf` (`281 N`) of drag and wastes `~2.4 kW` of shaft power at `10 knots`**, while shedding vortices that ventilate the propeller.
   * Any round-tube electric outboard (e.g., stripped `Hangkai M2200` test mule) used above `6 knots` or for foiling trials **must** be wrapped in a streamlined **`NACA 0020` / `NACA 0024` airfoil fairing (`~150 mm` chord)** (`3D`-printed PETG/CF-Nylon core skinned in glass/carbon epoxy), cutting strut drag by `~90%` (`~2.1 kW` saved at `10 kn`).

4. **Foiling Immersion Depth & Anti-Ventilation Geometry:**
   * Never attempt hydrofoiling with a fixed `15"` (`381 mm`) short-shaft transom outboard—the propeller ventilates immediately on lift-off.
   * Mount direct-drive pods (`65161` / `65162`) directly on the flip-up foil struts **`250–350 mm` below the tubes**, or mount tall-shaft transom drives (`730 mm` `W-30` or `20"`–`25"` donor leg) on a **vertical sliding/kick-up jack plate** to maintain `6"`–`9"` hull air gap in flight and `6"` beaching draft when raised.

5. **Pump-Jet (`APISQUEEN BP100`) Physics Constraints:**
   * A compact `100 mm` pump-jet (`BP100`, `10 kW`, `72–86 V`, `158 lbf` = `15.8 lbf/kW`) delivers `~60%` of propeller thrust efficiency and **cannot be paired with hydrofoils** (lifting the hull starves the flush bottom jet intake of water). Specify pump-jets strictly for prop-free, `3"`-draft rocky/sandy beaching or detachable jet-surfboard cassettes.

6. **Inflatable Catamaran Structural & Custom Battery-Floor Rules:**
   * Never transfer concentrated hydrofoil bending loads directly into glued PVC/Valmex inflatable seams. Always load hydrofoils through either (a) a **rigid `55–60 mm` 2-piece carbon/E-glass composite "Battery-Floor" skateboard chassis** replacing the `100 mm` drop-stitch air floor (recommended), or (b) a **clamp-on athwartships `6061-T6` / carbon saddle beam tied directly to the rigid transom via twin longitudinal torque bars**.
   * **Preserving the Catamaran Tunnel:** A `60 mm` rigid battery-floor (packing flat `36.7 mm` `EVE LF105` `LiFePO4` cells: `560 × 840 × 37 mm` for `16S 5.38 kWh` or `560 × 1,260 × 37 mm` for `24S 8.06 kWh`) sits **dry above the static waterline** and preserves factory tunnel clearance, avoiding the high saltwater-flood risk of permanently submerged `IP68` torpedo battery pods.
