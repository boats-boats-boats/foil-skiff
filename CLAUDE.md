# CLAUDE.md — Project Context & Engineering Guidelines for `foil-skiff`

## 1. Project Overview
`foil-skiff` (**FoilSkiff**) is an R&D, hydrodynamics, and fabrication repository for **`48 V` electric, hydrofoiling, and integrated battery-floor inflatable catamaran tenders** (`10 ft` tunnel-catamaran class, e.g., `True Kit Navigator 300` / `Discovery 330`).

Primary reference document: [`electric-foiling-dinghy-guide.md`](electric-foiling-dinghy-guide.md).

---

## 2. Core Engineering Rules & Physical Constraints (Do Not Violate)

When generating hydrodynamic calculations, CAD/3D-print fairings, battery layouts, controller wiring, or BOMs in this repository, always adhere to these physical and electrical constraints:

1. **`14S` vs. `16S LiFePO4` ESC Voltage-Ceiling Rule:**
   * Many hobby/ROV marine ESCs (including stock `APISQUEEN U30` `12S LiPo` ESCs and several `36–48 V` white-label azimuth pods) have a hard **`50.4 V` maximum input rating**.
   * A standard `16S LiFePO4` pack (`51.2 V` nominal) rests at `~53.2 V` and charges to **`55.2–58.4 V`** (`3.45–3.65 V/cell`)—which exceeds both `50.4 V` stock ESCs and leaves unsafe headroom on `60 V` MOSFETs.
   * **Mandatory Rule:** Either build a **`14S LiFePO4` pack (`44.8 V` nom. / `48.3–49.0 V` charge @ `3.45–3.50 V/cell`, strictly `<50.4 V` and under ISO `50 V`)** to retain stock `12S` ESCs, **OR** use a standard **`16S LiFePO4` pack (`51.2 V` nom.)** paired strictly with **`75 V`-rated controllers (`Flipsky 75100` / `75200` `VESC` or `Sevcon Gen4 48 V`)** with `VESC` max duty-cycle/current limiting to protect motor windings.

2. **Round Outboard Shaft Tube Fairing Requirement (`NACA 0024`):**
   * A bare round shaft tube (`Ø36 mm × 0.50 m` submerged, $C_D \approx 1.15$) generates **`63 lbf` (`281 N`) of drag and wastes `~2.4 kW` of shaft power at `10 knots`**, while shedding vortices that ventilate the propeller.
   * Any round-tube electric outboard (e.g., `Hangkai M2200`) used above `6 knots` or for foiling trials **must** be wrapped in a streamlined **`NACA 0020` / `NACA 0024` airfoil fairing (`~150 mm` chord)** (`3D`-printed PETG/CF-Nylon core skinned in glass/carbon epoxy), cutting strut drag by `~90%` (`~2.1 kW` saved at `10 kn`).

3. **Tall-Shaft Foiling Geometry & Anti-Ventilation Clearance:**
   * Never attempt hydrofoiling with a fixed `15"` (`381 mm`) short-shaft outboard—the propeller will ventilate as soon as the hull lifts.
   * Specify a **`20"` (`508 mm`) Long or `25"` (`635 mm`) Extra-Long donor lower leg** (or `730 mm` tall-shaft azimuth pod) mounted on a **vertical sliding/kick-up jack plate** so the propeller and aft stabilizer T-foil stay `220–300 mm` below the inflatable tubes in flight while preserving `6"` beaching draft when raised.

4. **Pump-Jet (`APISQUEEN BP100`) Physics Constraints:**
   * A compact `100 mm` pump-jet (`BP100`, `10 kW`, `72–86 V`, `158 lbf` = `15.8 lbf/kW`) delivers `~60%` of propeller thrust efficiency (`24–33 lbf/kW`) and **cannot be paired with hydrofoils** (lifting the hull starves the flush bottom jet intake of water). Specify pump-jets strictly for prop-free, `3"`-draft rocky/sandy beaching or detachable jet-surfboard cassettes.

5. **Inflatable Catamaran Structural & Custom Battery-Floor Rules:**
   * Never transfer concentrated hydrofoil bending loads directly into glued PVC/Valmex inflatable seams. Always load hydrofoils through either (a) a **clamp-on athwartships `6061-T6` / carbon saddle beam tied directly to the rigid transom via twin longitudinal torque bars**, or (b) a **rigid `55–60 mm` 2-piece carbon/E-glass composite "Battery-Floor" skateboard chassis** replacing the `100 mm` drop-stitch air floor.
   * **Preserving the Catamaran Tunnel:** A `60 mm` rigid battery-floor (packing flat `36.7 mm` `EVE LF105` `LiFePO4` cells: `560 × 840 × 37 mm` for `16S 5.38 kWh` or `560 × 1,260 × 37 mm` for `24S 8.06 kWh`) sits **dry above the static waterline** and preserves the factory tunnel clearance, avoiding the high saltwater-flood risk of permanently submerged `IP68` torpedo battery pods.
