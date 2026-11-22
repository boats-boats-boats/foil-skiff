# FoilSkiff — Visual Design Atlas & 3D CAD Model Gallery

A complete visual companion to [`electric-foiling-dinghy-guide.md`](electric-foiling-dinghy-guide.md) and [`DESIGN_TRADE_OFFS.md`](DESIGN_TRADE_OFFS.md), pairing **interactive millimeter-scale 3D `.stl` CAD models** (orbitable directly in GitHub's native 3D viewer), **multi-material OpenSCAD 3D renderings (`renders/`)**, and **mathematically-scaled 2D engineering SVG drawings (`diagrams/`)**.

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
| **4** | [`models/04_navigator300_retracted_beaching.stl`](models/04_navigator300_retracted_beaching.stl) | **`Navigator 300`** *(PRIMARY)* | **Retracted `86.5°` Parallelogram Beaching Mode** tucked cleanly beneath the `Tru-Alu` transom (`~135–140 mm` / `5.5"` sand clearance; outer wingtips folded aft inside `600 mm` tunnel!) |
| **5** | [`models/05_discovery330_oframe_stol.stl`](models/05_discovery330_oframe_stol.stl) | `Discovery 330` *(Secondary Hull)* | Secondary open-bow reference showing **Bow-Contoured Hard Deck + Full Rigid O-Frame** + identical swappable **Split STOL Flaperon Pod** (also applies to `Takacat LX`) |

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
*Tunnel-level view of the **`True Kit Navigator 300`** resting on flat beach sand (`Z = -232 mm`). All `4×` `60 × 9 mm` side-straddling blades fold `86.5°` aft **beside** the `80 mm`-thick pod (zero vertical chord stack-up, zero upper wing, zero external pushrod binding!), sliding smoothly beneath the factory `Tru-Alu` transom with outer wingtips folded `90°` aft cleanly inside the `600 mm` tunnel (**`~130–140 mm` / `5.1–5.5"` clear above flat sand** within the `300 cm` LOA).*

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

## Part II — Scaled 2D Engineering Drawings (`diagrams/`)

### 6. PRIMARY Wing Cross-Section: Submerged Split STOL Flaperons & Internal Pod Servos
![Staggerwing vs. STOL External Slotted Flaperon Cross-Sections](diagrams/02-stol-flaperons-cross-section.svg)

### 7. Flying-Keel Pod Internal Cutaway (`26 L` Swappable Cartridges, Internal Servos, Seawater Cooling & Safety)
![Flying-Keel Pod Internal Cutaway](diagrams/09-swappable-cartridge-cutaway.svg)

### 8. Secondary Wing: Flush-Nested Top-Deck Switchblade Wing (Top-Down Closed vs. Deployed)
![Flush-Nested Switchblade Top-Down Geometry](diagrams/01-switchblade-wing-topdown.svg)

### 9. Contoured Bow-Bent Hard Deck & Under-Hull Coupling Options (`Navigator 300` Primary + Magnets + `Discovery 330` O-Frame + OEM Slot)
![Drop-In Rigid Spine Floor Coupling Options](diagrams/03-spine-floor-coupling-options.svg)

### 10. Grounding Kick-Up Kinematics: Why a Single Central Mast Fails vs. 4-Bar Parallelogram
![Single Central Mast Collision vs. 4-Bar Parallelogram Kick-Up](diagrams/04-grounding-kickup-geometry.svg)

### 11. Strut Architecture & Folded Stack-Up Clearance Inside the `Navigator 300` Tunnel (`600 mm` Wide × `230 mm` High)
![Strut Architecture & Folded Beaching Stack-Up](diagrams/05-strut-folded-stackup.svg)

### 12. Integrated Battery-Hull Architecture Comparison on `True Kit Navigator 300`
![Integrated Battery-Hull Architecture Comparison](diagrams/10-alt-architectures-comparison.svg)

### 13. Rejected Concept Physics: Why Surface-Piercing Step-Out Wings Fail in Chop (Forward & Deep-Aft)
![Rejected Concept Physics: Surface-Piercing Step-Out Wing Wave-Slam Hazards](diagrams/12-rejected-concepts-physics.svg)

---

## Part III — Regenerating or Modifying the Parametric CAD & Drawings

All `.stl` models, `.svg` technical drawings, and OpenSCAD `.png` renderings are generated deterministically with **zero Python third-party dependencies** (plus optional `openscad` CLI for shaded PNG renders):

```bash
# Regenerate all 8 scaled 2D engineering SVGs (pure Python 3)
python3 diagrams/generate_diagrams.py

# Regenerate all 5 binary 3D .stl CAD models, 5 annotated 3D SVGs, and 5 OpenSCAD PNGs
python3 models/generate_cad.py
```

* **OpenSCAD (macOS / Linux / Docker):** Install natively (`brew install --cask openscad`) or run headless via Docker (`docker run --rm -v "$PWD":/work openscad/openscad ...`).
* **3D Printing Tabletop Models:** Import any file in `models/*.stl` into PrusaSlicer / Bambu Studio / Cura and scale to **`1:15` (`6.7%`)** or **`1:10` (`10%`)** (all coordinates are native `1:1` millimeters).
