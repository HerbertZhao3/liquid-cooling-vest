# CAD

Conventions for the CAD files in this folder. The design intent for each part is in [plan §3.2 and §4](../docs/project-plan.md).

## Layout

| Folder | Contents |
|---|---|
| `library/` | Purchased parts (PP-xxx), modelled from datasheets or downloaded from the manufacturer |
| `phase1/` | Native files for CV-1xx parts and assemblies |
| `phase2/` | Native files for CV-2xx parts and assemblies |
| `exports/` | STEP for every released part and assembly, plus STL for printed parts |
| `drawings/` | Released PDF drawings, one per part number and revision |
| `renders/` | PNG renders and exploded views for the portfolio |

## Part numbers

| Number | Part | Phase |
|---|---|---|
| CV-100 | Phase 1 top-level assembly | 1 |
| CV-101 | Manifold: supply split, returns, R/M tees, sensor ports | 1 |
| CV-102 | Wearable housing | 1 |
| CV-103 | Housing lid / UI panel | 1 |
| CV-104 | Pump isolator (TPU) | 1 |
| CV-106 | Tube clip (TPU) | 1 |
| CV-107 | Garment tube layout and sewing template | 1 |
| CV-110 | Heated-torso lid | 1 |
| CV-111 | Contact band clamp | 1 |
| CV-112 | Heater-block clamp | 1 |
| CV-200 | Phase 2 backpack top-level assembly | 2 |
| CV-201 | Frame (sheet metal) | 2 |
| CV-202 | Chiller mount | 2 |
| CV-203 | Shell, back panel | 2 |
| CV-204 | Shell, cover | 2 |
| CV-205 | Intake duct | 2 |
| CV-206 | Exhaust duct | 2 |
| CV-207 | Battery case | 2 |
| CV-208 | Heat shield | 2 |
| PP-xxx | Purchased parts (pumps, jar, quick disconnect, ESP32, chiller, isolators, …) | — |

## Rules

- **File names:** `CV-101_manifold_revA.<ext>`. The revision letter goes up when a released part changes form, fit, or function.
- **Release:** a part is released when its drawing PDF and STEP export are committed together with the native file, and the change is recorded in the [decision log](../docs/decision-log.md).
- **Mass properties:** assign real materials so assembly mass can be checked against the measured mass (target ±10%).
- **File size:** CAD files are binary and cannot be diffed. Commit them at meaningful checkpoints rather than after every save. If the folder grows past a few hundred MB, move native files to Git LFS.
