# Decision log

Each entry records the decision, the alternatives considered, and the evidence. Add measurements and revisions as they come in, and when a measurement changes an ASSUMED input in `calcs/first_pass.py`, note it here.

## D-007 — Build in two phases: an ice-buffer prototype now, the compressor later

- **Date:** 2026-10-27 · **Status:** proposed in v3.
- **Context:** The goal is a strong resume on a student budget, and there is no budget for a US$550 chiller.
- **Options:**
  - (a) Full build with the chiller, about US$1,230.
  - (b) Design only, with no hardware.
  - (c) Build everything measurable with ice as the cold source, and design the compressor version on paper.
- **Decision:** (c), at about US$300.
  - (b) produces no measured results, and those are what make a hardware project credible.
  - (c) still delivers closed-loop control, a test rig, a validated model, and a measured design improvement.
- **Consequences:** The cold buffer is chiller-ready, so building Phase 2 later is a direct extension. The 75 W benchmark is measured through the garment instead of on the water side.

## D-010 — CAD-led scope

- **Date:** 2026-10-27 · **Status:** accepted in v3.
- **Context:** The user is a mechanical-engineering student and wants the project to showcase CAD.
- **Options:**
  - (a) A mechatronics-heavy build, with most hours on electronics and firmware.
  - (b) A CAD-led build: custom printed parts, simulations checked against measurements, and a full Phase 2 assembly with drawings.
  - (c) CAD only, with no hardware.
- **Decision:** (b).
  - (c) has no measurements, so its simulations would go unchecked.
  - (a) spends the hours on the wrong discipline for a mechanical resume.
- **Consequences:**
  - The electronics are capped at about 10 hours.
  - The off-the-shelf tees and bag are replaced by CV-101 and CV-102/103.
  - The CAD tool is whatever the university licenses, with SolidWorks preferred for job postings and CSWA practice; Fusion or Onshape are free alternatives.

## D-011 — Printed manifold instead of loose tees

- **Date:** 2026-10-27 · **Status:** proposed in v3.
- **Options:**
  - (a) Barbed tees and Y-pieces joined with hose.
  - (b) A printed manifold (CV-101) that integrates the supply split, returns, R/M tees, and sensor ports.
  - (c) A CNC-machined manifold.
- **Decision:** (b), in SLA resin if the makerspace has it, otherwise FDM PETG with solid walls around the ports.
  - It fixes the tee R/M spacing by design.
  - It puts the sensors where they are needed.
  - It is a real designed part with a drawing.
  - (c) costs more and needs shop access; keep its drawing as the production option.
- **Evidence to collect:** the 50 kPa leak test (Gate A), CFD against the measured front/back flow split, and the rev B changes.

## D-001 — Buy a sealed chiller module (Phase 2)

- **Date:** 2026-10-27 · **Status:** accepted for the Phase 2 design; buy only if Phase 2 is built.
- **Context:** Compressor refrigeration is the Phase 2 requirement, and the tools available are basic.
- **Options:**
  - (a) A sealed DC chiller module.
  - (b) A bare compressor plus a plate exchanger and condenser, charged in-house.
  - (c) Thermoelectric cooling.
- **Decision:** (a).
  - (b) needs brazing, vacuum and charging equipment, and refrigerant handling.
  - (c) needs roughly 2–4× the electrical power for the same cooling.
- **Candidates:** the RIGID DV1920E-P(S), at 3.5 kg and 100–400 W, and RIGID's personal-wear unit, at 2.75 kg and 260 W. RIGID's standard compressors are rated for indoor use, and only its "T" series is rated to 52 °C ambient.
- **Evidence to collect:** written answers to [the data request](vendor-rfq.md) from each supplier.

## D-002 — Two loops with a cold buffer and injection mixing

- **Date:** 2026-10-27 · **Status:** accepted for both phases.
- **Context:** The chiller's minimum capacity (≥ 100 W) exceeds the 75 W load, and it restarts only after its pressures equalize (~3 min). The target is ±1 °C at the vest inlet.
- **Options:**
  - (a) v1's single loop, cycling the compressor.
  - (b) A single loop with enough thermal mass to ride through the off periods.
  - (c) A cold buffer with an injection pump.
  - (d) A cold buffer with a proportional 3-way mixing valve.
- **Decision:** (c).
  - (a) produces swings of about +11 K.
  - (b) needs about 1.6 kg of water.
  - (d) is ruled out because small proportional valves cost US$50 or more, and printed ones tend to leak.
- **Consequences:**
  - In Phase 1 the buffer is ice water, so the vest loop and controller are built and tuned without the chiller.
  - In Phase 2 the chiller charges the same buffer, which also bridges about 3 minutes of tilt or fall shutdown.
  - Phase 1 uses pumps B and C; Phase 2 adds pump A.

## D-003 — 7S Li-ion battery (Phase 2)

- **Date:** 2026-10-27 · **Status:** accepted for the Phase 2 design.
- **Context:** The chiller accepts 20–32 V, with up to 8.5 A.
- **Options:**
  - **6S Li-ion (18–25.2 V):** drops below 20 V before it is empty.
  - **7S Li-ion (21–29.4 V):** stays inside the window over its whole capacity.
  - **8S LiFePO4:** about 1.5× heavier per Wh.
  - **USB-C PD 3.1 bank at 28 V:** its 140 W cap is below the compressor's peak current, and a PD renegotiation drop would trigger the restart lockout.
  - **18/20 V power-tool packs:** below 20 V.
- **Decision:** 7S Li-ion, a finished pack with a BMS, with its capacity verified by a discharge test.

## D-008 — Phase 1 power from a USB-C power bank

- **Date:** 2026-10-27 · **Status:** proposed in v3.
- **Context:** Phase 1 draws about 5 W (two pumps plus the ESP32).
- **Decision:** a USB-C power bank you already own, with a PD trigger board. It is certified, protected, and free. Ice, not electricity, limits the runtime.

## D-004 — Measurement approach

- **Date:** 2026-10-27 · **Status:** proposed in v3.
- **Decision:**
  - Bench capacity is measured from the heater's electrical power (INA226).
  - Water-side ṁ·c<sub>p</sub>·ΔT is the cross-check, and the closure between the two is reported.
  - Eight 10k NTC probes on ADS1115 ADCs are calibrated together in the stirred torso bath for relative matching.
  - The flow sensor is calibrated by timed collection on a scale.
- **Rejected:**
  - PT1000 RTDs with MAX31865 converters cost about 3× more per channel and match no better than co-calibrated NTCs over 5–35 °C.
  - Uncalibrated DS18B20 sensors are only good to ±0.5 °C.

## D-009 — Heated torso: a water-filled bucket

- **Date:** 2026-10-27 · **Status:** proposed in v3.
- **Options:**
  - (a) Silicone heater pads on a form tube, with front and back zones.
  - (b) A 19 L bucket of water held at 34 °C by a 12 V immersion heater.
  - (c) A commercial thermal manikin.
- **Decision:** (b), at about US$30.
  - Its large thermal mass gives a uniform, stable surface.
  - It has a single heater to control and measure.
  - It doubles as the calibration bath.
  - (c) is unaffordable.
- **Consequences:** Front and back are measured on the water side from separate branch return sensors rather than from heater zones. Removal above the heater's capacity is still measurable from the bucket's cooling rate.

## D-005 — Fabrication at the campus makerspace

- **Date:** 2026-10-27 · **Status:** proposed in v3.
- **Decision:** Print the CV-1xx parts (SLA resin for the manifold if available; PETG and TPU otherwise) and sew the garment at the campus makerspace, paying for material only (about US$20 for two revisions). A commercial print service is the fallback.

## D-006 — ESP32 controller

- **Date:** 2026-10-27 · **Status:** proposed in v3.
- **Options:**
  - **Arduino Uno/Nano:** no Wi-Fi and little RAM for logging.
  - **Raspberry Pi:** needs to boot Linux, draws more power, and risks SD-card corruption when power is cut.
  - **ESP32:** has Wi-Fi, generates PWM in hardware, and costs about US$7.
- **Decision:** ESP32, with external ADS1115 ADCs because the ESP32's built-in ADC is nonlinear.
