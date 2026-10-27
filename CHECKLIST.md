# Liquid Cooling Vest — Checklist

Tick items off as you go. On GitHub, open this file and click the boxes; locally, change `[ ]` to `[x]`. Part numbers (CV-xxx) are listed in [`cad/README.md`](cad/README.md). Week numbers are a guide, not a deadline.

---

## 0. Setup (week 1)

- [ ] Choose a CAD tool: SolidWorks through the university, or Fusion or Onshape (free for students)
- [ ] Check which simulation tools the licence includes (static FEA, thermal FEA, flow/CFD)
- [ ] Create the CAD folders: `library/`, `phase1/`, `phase2/`, `exports/`, `drawings/`, `renders/`
- [ ] Visit the makerspace and note the printers (FDM, SLA), TPU filament, sewing machine, and booking rules
- [ ] Arrange to borrow a bench power supply, a reference thermometer, a kitchen scale, and a bike pump with a gauge

## 1. Buy Phase 1 parts (week 1, ~US$300)

Full list with prices: [`bom/budget.csv`](bom/budget.csv). Record what you actually pay in the `actual_usd` column.

- [ ] 2 × small 12 V brushless pumps (same model)
- [ ] 25 m of 4 × 6 mm PU tubing, 2 m of 6 mm ID silicone hose, foam pipe insulation
- [ ] 1 pair of dry-break quick disconnects, plus barbs and hose clamps
- [ ] Vacuum food jar (~1.2 L) and 2 bulkhead fittings
- [ ] Compression shirt and stretch fabric strips (skip the shirt if you own one that fits snugly)
- [ ] ESP32, 2 × ADS1115, 8 × 10k NTC probes, flow sensor, INA226, OLED display and encoder, MOSFET modules, USB-C PD trigger board
- [ ] 12 V 20 A power supply (only if you can't borrow one)
- [ ] Heater-block parts: PC water block and 2 × 3.3 Ω 50 W resistors
- [ ] Heated-torso parts: 19 L bucket, 12 V immersion heater, small stirring pump

## 2. CAD the purchased parts (weeks 1–2)

Measure each part with calipers, or download the manufacturer's model. Model the mounting holes and ports accurately; the rest can be simplified.

- [ ] Pumps (body, inlet and outlet ports, mounting holes)
- [ ] Vacuum jar and lid
- [ ] Quick disconnect
- [ ] ESP32 board, OLED display, encoder, power bank
- [ ] Flow sensor and NTC probe
- [ ] 19 L bucket and PC water block
- [ ] Give every part a real material so mass properties work

## 3. Design and CAD the Phase 1 parts (weeks 2–3)

### CV-107 Garment tube layout and sewing template
- [ ] Measure the torso: chest, waist, and the front and back panel areas
- [ ] Sketch the front and back tube routing, about 9 m each, with **equal lengths** so the flow splits evenly
- [ ] Set the baseline spacing to ~25 mm (≈0.45 m² of vest ÷ 18 m of tubing)
- [ ] Check that every bend is at least the tubing's minimum bend radius (from the listing)
- [ ] Mark where the inlet and outlet leave the garment
- [ ] Export a full-size template PDF, print it, and tile the sheets together

### CV-101 Manifold
- [ ] Define the ports:
  - [ ] pump in
  - [ ] front supply and back supply
  - [ ] front return and back return
  - [ ] injection in
  - [ ] return to buffer
  - [ ] 3 sensor ports (inlet, front return, back return)
- [ ] Route the internal channels so the front and back paths are identical
- [ ] Put the return-to-buffer tee **upstream** of, and close to, the injection tee
- [ ] Design the barbs to suit the 4 × 6 mm tubing and 6 mm hose
- [ ] Add O-ring glands on the sensor ports
- [ ] Make the walls solid around the ports, and choose the print orientation (SLA preferred)
- [ ] Draw rev A, then print it

### CV-102 / 103 Wearable housing and lid
- [ ] Lay out the jar, both pumps, the ESP32, the power bank, and the wiring
- [ ] Put the electronics bay above the water, with a drip path away from it
- [ ] Add pump mounts that take the CV-104 isolators
- [ ] Plan the hose routing and the bulkhead positions
- [ ] Add cutouts in the lid for the OLED display, encoder, and power switch
- [ ] Choose the fastening: snap fits or heat-set inserts
- [ ] Add a strap or belt mount
- [ ] Check the mass and CG in CAD
- [ ] Print it

### Small parts
- [ ] CV-104 pump isolators (TPU)
- [ ] CV-106 tube clips (TPU), in two spacing variants for the redesign
- [ ] CV-110 torso lid (holds the heater, stirrer, and sensors)
- [ ] CV-111 contact band clamp (repeatable pressure between the vest and the torso)
- [ ] CV-112 heater-block clamp

### CV-100 Phase 1 assembly
- [ ] Assemble everything and run an interference check
- [ ] Create an exploded view
- [ ] Generate the BOM from CAD
- [ ] Record the CAD mass, to compare with the measured mass later

## 4. Build (weeks 3–4)

- [ ] Sew the tubing into the shirt using the template and clips
- [ ] Build the heater block and the heated torso
- [ ] Plumb the loop: manifold, pumps, jar, vest
- [ ] **Gate A:** pressurise the loop to 50 kPa (7 psi) with the bike pump, hold for 10 minutes, and fix any leaks before wiring
- [ ] Wire the electronics on perfboard (keep it minimal)
- [ ] Write the firmware: read sensors, run a PI controller on the injection pump, interlocks, logging

## 5. Test (weeks 4–5 and 7)

- [ ] Calibrate all the NTC probes together in the bucket against the reference thermometer
- [ ] Calibrate the flow sensor by timing how long it takes to fill a container on the scale
- [ ] Measure the front and back branch flows the same way (target: within 10% of each other)
- [ ] Check the energy balance: heater power against water-side heat (target ±10%)
- [ ] Step the setpoint between 20, 24, and 28 °C, and the load between 25 and 75 W (target ±1 °C)
- [ ] Run the torso tests: inlet at 20, 24, and 28 °C × flow at 0.3, 0.5, and 0.7 L/min (target ≥75 W at 20 °C)
- [ ] **Gate B:** test every interlock before wearing the vest
- [ ] Wearable: measure the mass (target ≤3.5 kg), the ice runtime at 75 W (target ≥45 min), and do a short seated test

## 6. Simulate and compare (week 6)

- [ ] Run a thermal FEA of one tube on the skin (2D cross-section) to get the contact conductance
- [ ] Run a CFD of the manifold to predict the front/back flow split
- [ ] Compare both with the measurements (targets: heat removal within 20%, flow split within 10%)
- [ ] Write the results in [`docs/decision-log.md`](docs/decision-log.md)

## 7. Redesign one part (week 7)

- [ ] Pick the weakest result: manifold rev B, or the tube spacing and clips
- [ ] Re-CAD it, reprint it, and re-measure
- [ ] Record the before-and-after numbers (these go on your resume)

## 8. Phase 2 — compressor backpack, CAD only (weeks 8–10)

- [ ] Send the chiller data request ([`docs/vendor-rfq.md`](docs/vendor-rfq.md)); do this in week 2 so the answers arrive in time
- [ ] Model the chiller from its datasheet outline (230 × 200 × 145 mm, 3.5 kg)
- [ ] CV-201 sheet-metal frame, with flat patterns
- [ ] CV-202 chiller mounts on rubber isolators, pre-tilted ~10°
- [ ] CV-203 / 204 shell back panel and cover
- [ ] CV-205 / 206 intake and exhaust ducts, kept separate
- [ ] CV-207 battery case
- [ ] CV-208 heat shield between the chiller and your back
- [ ] Hip-belt and harness interface
- [ ] Place the cold buffer, pumps, hoses, and IMU
- [ ] Check mass and CG in CAD (target ≤6 kg)
- [ ] Run FEA on the frame and mounts under a 10 g drop-equivalent load (target safety factor ≥2)
- [ ] Run CFD to check that exhaust doesn't reach the intake (target ≤1 K rise)
- [ ] Make the ice-vs-compressor chart (`python3 calcs/first_pass.py`, section 13)

## 9. Drawings and portfolio (weeks 11–12)

- [ ] Make GD&T drawings: CV-101, CV-102/103, the CV-201 flat pattern, and the other fabricated parts
- [ ] Commit STEP and STL exports alongside the native files
- [ ] Render CV-100 and CV-200, plus exploded views
- [ ] Fill in the results table in the [README](README.md)
- [ ] Write the report or portfolio page
- [ ] Record a short video of the vest on the torso rig and being worn
- [ ] Write your resume bullets with the real numbers
