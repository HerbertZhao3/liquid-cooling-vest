# Liquid-Cooling Vest

A CAD-led mechanical design project: a wearable liquid-cooling vest with closed-loop coolant temperature control. Two tubing circuits (front and back) carry water whose inlet temperature an ESP32 holds between 20 and 28 °C. It does this by injecting cold water from an insulated buffer through a custom 3D-printed manifold.

- **Phase 1 (built):** ice charges the buffer. The manifold, wearable housing, garment tube layout, and test fixtures are designed in CAD, printed, and tested on a heated-torso rig. The measurements validate the simulations.
- **Phase 2 (CAD design study):** a battery-powered compressor-chiller backpack, with a sheet-metal frame, shock-mounted chiller, shell and ducting, FEA, CFD, and drawings.

**Status:** planning complete. [Plan v3](docs/project-plan.md) week 1 is next: set up the CAD conventions, order parts, and model the purchased parts.

## Requirements and results (Phase 1)

| Requirement | Target | Result |
|---|---|---|
| Coolant adjustment | 20–28 °C in 1 °C steps | not tested |
| Regulation | Vest inlet ±1 °C, including 25 ↔ 75 W load steps | not tested |
| Garment heat removal | ≥ 75 W from the 34 °C heated torso at 20 °C inlet, 0.5 L/min | not tested |
| Thermal model validation | Simulation within ±20% of measurement | not tested |
| Flow balance | Front and back branches within ±10% | not tested |
| Leak-tightness | Printed parts hold 50 kPa for 10 min | not tested |
| CAD fidelity | CAD mass within ±10% of measured | not tested |
| Measurement quality | Energy balance within ±10% | not tested |
| Wearable runtime | ≥ 45 min at 75 W per ice charge | not tested |
| Wearable mass | ≤ 3.5 kg | not tested |
| Budget | ≤ US$300 | US$0 spent |

## Repository

| Path | Contents |
|---|---|
| [`docs/project-plan.md`](docs/project-plan.md) | The plan (v3), including the 12-week timeline |
| [`docs/plan-review.md`](docs/plan-review.md) | What changed from v1 and why |
| [`docs/decision-log.md`](docs/decision-log.md) | Decisions, alternatives, and evidence |
| [`docs/vendor-rfq.md`](docs/vendor-rfq.md) | Chiller data request for Phase 2 |
| [`docs/archive/plan-v1.md`](docs/archive/plan-v1.md) | The original plan |
| [`cad/`](cad/README.md) | CAD conventions and part numbers; models, drawings, and exports as they are released |
| [`calcs/first_pass.py`](calcs/first_pass.py) | Sizing calculations for both phases |
| [`bom/budget.csv`](bom/budget.csv) | Line-item budget by phase, with an `actual_usd` column |

`firmware/`, `data/`, and `report/` will be added as the work produces them.

## Calculations

```sh
python3 calcs/first_pass.py
```

The script uses only the Python standard library. Inputs marked `ASSUMED` are placeholders until measurements replace them.
