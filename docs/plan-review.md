# Plan history and review

Review of [plan v1](archive/plan-v1.md), 2026-10-27. The resulting plan is [project-plan.md](project-plan.md) (v3). Figures come from [`calcs/first_pass.py`](../calcs/first_pass.py) and the RIGID DV1920E-P(S) datasheet.

## Why v3 is phased

The goal is a strong resume on a student budget. v1 needed US$1,500, and a cost-cut version (v2, never published) still needed US$1,230, because the sealed chiller alone costs about US$550.

v3 builds everything that can be measured without the chiller for about US$300, using ice as the cold source. The compressor backpack becomes a full design study, and building it stays possible later for about US$850 more.

v3 is also **CAD-led**, because this is a mechanical-engineering portfolio:
- The off-the-shelf tees and bag are replaced by designed parts: a printed manifold, a wearable housing, a garment tube layout, and test fixtures.
- Simulations (tube-contact thermal FEA and manifold CFD) are checked against measurements.
- Phase 2 becomes a full CAD assembly with FEA, CFD, and GD&T drawings.
- Electronics are kept to about 10 hours.
- The timeline is 12 weeks × 8 h, the same as v1.

**What carries over from v1:**
- The 20–28 °C adjustment, ±1 °C regulation, 0.5 L/min flow, and front/back garment concept are built and measured in Phase 1.
- The 75 W benchmark is now measured through the garment rather than as a water-side load.
- The compressor targets (75 W at 30 °C ambient, 60 minutes, ≤ 60 W, ≤ 6 kg, ≤ 15 L) are verified by calculation in Phase 2.

## Findings

| # | v1 | Finding | Where v3 handles it |
|---|---|---|---|
| 1 | One loop, with the chiller controlled from the vest inlet | The chiller's minimum capacity (≥ 100 W) exceeds the 75 W load, and it restarts only after its pressures equalize (~3 min). With 0.3 L of water, one off period adds +10.8 K at the vest inlet | Cold buffer plus injection mixing, built in Phase 1 with ice; Phase 2 charges the same buffer from the chiller |
| 2 | Water inventory ~0.3 L | 18 m of 4 mm tubing alone holds 0.23 L, which leaves no room for a reservoir | Phase 2 inventory corrected to ~0.85 L |
| 3 | Mass ≤ 6 kg, with no mass budget | Estimate is 7.3 kg with the 3.5 kg chiller and ~5.9 kg with every lever applied, which is too heavy for all-day wear | Phase 2 mass budget; Phase 1 wearable is ~3.30 kg; ice-vs-compressor mass/runtime chart (ice is lighter below ~6–7 h) |
| 4 | "Confirm the configuration" | The datasheet gives a 30 °C upper temperature (possibly ambient), a 40° tilt limit, 8.2/17 V fault thresholds that contradict its 20–32 V range, and 3.5 kg against the listing's 3.0 kg. RIGID's standard compressors are rated for indoor use, and only its "T" series is rated to 52 °C | Phase 2 RFQ, including the lighter 2.75 kg personal-wear unit |
| 5 | Orientation "checked" | A fall or a bend past 40° while running risks the compressor; impact can crack a refrigerant line, which cannot be repaired; a crushed battery is a fire risk | Phase 2 design: IMU cutoff, upright wait before restart, ~3 min of buffer cooling while stopped, shock-mounted shell, protected battery case, mount pre-tilted ~10° |
| 6 | "Protected battery ~120 Wh", US$200 | The chiller's 20–32 V window is not addressed | Phase 2: 7S Li-ion. Phase 1: a USB-C power bank (~5 W load) |
| 7 | Matched sensors for a 2.2 K ΔT | At 25 W the ΔT is 0.72 K, so ±0.05 K sensors give ±10% on Q | Heater electrical power is the reference; energy-balance closure is a reported result |
| 8 | Bench work depends on the chiller arriving | The chiller is the critical path | Removed from Phase 1 entirely |
| 9 | US$1,500 | — | Phase 1 is US$298 (~US$260 with a borrowed supply and your own shirt); the Phase 2 build is optional |
| 10 | "Document humidity" | The dew point at 30 °C and 70% RH is 23.9 °C, so 20 °C tubing sweats and wastes cooling on the air | Insulated cold lines (Phase 1); outer insulating vest layer and wicking base layer (Phase 2 design) |
| 11 | "Temperature-controlled heated surface" | The surface is not specified, and a thermal manikin is unaffordable | A water-filled heated torso at 34 °C; front and back measured from separate branch return sensors |
| 12 | Faults: flow, sensor, temperature, under-voltage | The cold-inlet hazard from the ice buffer is missing, as are freeze, tilt, and the compressor fault output for Phase 2 | Phase 1 interlocks (§2.2); Phase 2 design list |
| 13 | 75 W water-side benchmark | Does not measure what the garment removes | Phase 1 target: ≥ 75 W through the garment on the heated torso, plus a model validated against it |
| 14 | — | A heavy sweater in humid 30 °C heat: liquid cooling works without evaporation, but 75 W covers a resting person (~100 W of body heat), not a walking one (~250–350 W) | Phase 1 measures heat removal against inlet temperature and flow; Phase 2 sizing states the activity level it covers |
