> **Archived.** This is plan v1, the original plan written with ChatGPT, kept verbatim for the decision record. It is superseded by [project-plan.md](../project-plan.md); the differences are explained in [plan-review.md](../plan-review.md).

Battery-Powered Cooling Vest — Project Plan

## 1. Objective and design targets

Build a wearable liquid-cooling vest connected to a backpack containing a sealed compressor chiller, circulation pump, battery, and temperature controls. The project should demonstrate mechanical design, thermal and fluid calculations, fabrication, and comparison between predictions and measurements.

**Confirmed requirements:** adjustable coolant temperature, operation near 30°C outdoors, compressor refrigeration, and construction using basic tools with outsourced fabrication.

| Requirement | Initial target |
|---|---|
| Coolant adjustment | 20–28°C in 1°C increments, initially evaluated on the bench |
| Temperature regulation | Vest inlet within ±1°C of its setting after stabilization |
| Cooling performance | Sustain a 75 W controlled water-side heat load at 30°C ambient and 20°C coolant |
| Battery runtime | At least 60 minutes at the specified test condition |
| Electrical efficiency | Target ≤60 W average total consumption; verify experimentally |
| Battery capacity | Start with approximately 120 Wh; finalize from measured consumption |
| Circulation | Approximately 0.5 L/min through the complete circuit |
| Water inventory | Approximately 0.3 L, including tubing and heat exchangers |
| Total wearable mass | Target ≤6 kg, including water and battery |
| Backpack volume | Target ≤15 L |
| Budget | US$1,500 planning allowance |
| Schedule | 12 working weeks at approximately 8 hours per week; allow additional procurement time |

Except for the confirmed requirements, these are provisional targets. **The 75 W refrigeration benchmark does not establish how much heat the vest removes from a person.** Garment performance will be measured separately.

## 2. System design and component strategy

**Water circuit**

Reservoir → pump → chiller → inlet temperature sensor → front/back vest circuits → return temperature sensor → reservoir.

Use two parallel tubing circuits, one serving the front and one the back. Start with equal-length branches and approximately 4 mm internal-diameter flexible tubing. Keep the tubing removable, secure it in sewn channels, and insulate the backpack supply and return hoses.

Select the pump to deliver the required flow **through the assembled circuit**, accounting for the chiller, tubing, and connectors.

**Refrigeration**

Purchase a complete, sealed DC water-chiller module containing the compressor, evaporator, condenser, expansion device, and driver. Keep the refrigerant circuit intact.

Use a 24 V module as the initial candidate. The RIGID DV1920E-P-S provides a useful reference: its listing shows a $470 price and 3 kg mass, while its linked specification gives 3.5 kg. Confirm the supplied configuration before using either value in the design. [Product listing](https://www.rigidhvac.com/store/products/mini-water-chiller-dv1920e-p-s-24v), [Specification](https://uploads.strikinglycdn.com/files/c9523143-a135-4a0a-bebd-788c411fe973/Mini%20Water%20Chiller%20Spec-DV1920E-P%28S%29%2024V.docx.pdf?id=3700598)

**First purchasing milestone:** obtain consistent documentation confirming cooling capacity and electrical input at 30°C ambient and 20°C water, minimum water flow, adjustment across 20–28°C, mounting orientation, restart behavior, and supplied components. Require approximately 100 W available cooling capacity at the design condition to provide margin above the 75 W test load.

**Backpack and garment**

- Use an existing backpack with a removable, bolted equipment frame.
- Place heavy components close to the wearer’s back and distribute their weight through the straps.
- Separate condenser intake and exhaust airflow; direct exhaust away from the wearer.
- Outsource printed brackets and ducts after checking component dimensions.
- Separate electronics from likely leak and condensation paths.
- Provide accessible filling, draining, battery removal, and vest connections.

**Controls and measurement**

Use a small microcontroller, local temperature selector, display, and data logging. Measure coolant inlet/outlet temperatures, ambient temperature, flow, and electrical power. Use matched, calibrated temperature sensors so small inlet/outlet differences can be measured reliably.

Control cooling from the vest inlet temperature. Establish flow before enabling refrigeration and respect the chiller’s restart restrictions. Provide a physical power switch and fault responses for loss of flow, sensor failure, abnormal coolant temperature, and battery undervoltage.

The coolant adjustment range is a hardware test specification. Establish wearer-use limits separately before powered wearer evaluation.

## 3. Work stages and deliverables

| Weeks | Work | Deliverable and milestone |
|---|---|---|
| **1** | Freeze requirements; verify chiller documentation, availability, and delivered cost | Requirements sheet, component shortlist, and purchasing decision |
| **2–3** | Calculate heat loads, tubing losses, battery demand, and mass; create preliminary CAD | Calculation workbook, system schematic, and packaging layout |
| **4–5** | Assemble the water loop and controlled heater fixture using a bench power supply | Measured cooling capacity, electrical consumption, and flow; finalize battery sizing |
| **6–7** | Build front/back garment circuits; compare tubing placement and attachment methods | Garment prototype and measured temperature distribution |
| **8–9** | Integrate temperature adjustment, logging, display, and fault handling | Working controls and fault-test record |
| **10** | Manufacture outsourced parts and assemble the backpack | Complete wearable assembly with measured mass and dimensions |
| **11** | Run integrated thermal and battery tests; evaluate fit and movement | Validation results and a prioritized improvement list |
| **12** | Complete one design revision and prepare portfolio materials | Engineering report, CAD/drawings, photographs, and demonstration video |

Proceed to final fabrication after the bench system establishes actual power, cooling, and component dimensions.

Keep a decision log throughout: alternatives considered, calculations used, measurements obtained, and reasons for each revision. This provides useful interview material.

## 4. Calculations, testing, and acceptance criteria

**Required calculations**

- Water-side heat removal: \(Q=\dot m c_p(T_\text{return}-T_\text{supply})\).
- Battery runtime from measured average total electrical consumption and usable battery energy.
- Pressure loss through tubing, branches, connectors, and the chiller.
- Refrigeration heat rejection: cooling load plus compressor input.
- Total mass and volume, including water, battery, supports, and ventilation space.

At 0.5 L/min, a 75 W water-side load produces approximately a **2.2°C temperature rise**. That makes sensor matching and calibration important.

**Bench tests**

- Calibrate temperature and flow measurements; establish measurement uncertainty.
- Test 25, 50, and 75 W heater loads at 20, 24, and 28°C coolant settings.
- At the main design condition, demonstrate 75 W operation with coolant regulation within ±1°C for at least 30 minutes after stabilization.
- Record ambient temperature at the condenser intake and document humidity.
- Perform leakage checks before adding electronics and repeat them after garment flexing.
- Test sensor disconnection, restricted flow, low battery, and the physical shutdown switch.

**Garment tests**

Use a temperature-controlled heated surface to compare front/back circuits, contact quality, and cooling uniformity under repeatable conditions. Thermal-manikin testing has been used to validate liquid-cooled garment models. [Research example](https://pubmed.ncbi.nlm.nih.gov/25774026/)

Separate measured heat extraction from the heated surface from heat gained through hoses and the surrounding environment.

**Integrated tests**

- Demonstrate at least 60 minutes of battery operation under the specified controlled load.
- Measure total mass, enclosure volume, noise, and condensation.
- Verify that backpack exhaust is not drawn directly back into its intake.
- Check fit, hose routing, and movement against the chiller’s permitted orientation.
- Complete bench and fault checks before any powered wearer evaluation.

Report every target as **met, missed, or not tested**. If power consumption exceeds 60 W, use the measured value to revise the battery budget and document the resulting mass/runtime tradeoff.

## 5. Budget and portfolio outcome

These amounts are spending allowances, not supplier quotations.

| Category | Allowance |
|---|---:|
| Sealed chiller and delivery | $550 |
| Protected battery and charger | $200 |
| Pump, tubing, reservoir, and fittings | $120 |
| Controls, sensors, and logging | $160 |
| Garment and sewing materials | $70 |
| Outsourced brackets, ducts, and frame parts | $100 |
| Bench testing equipment and fixture | $150 |
| Contingency | $150 |
| **Total** | **US$1,500** |

Assume outsourced printing and simple bolted construction. Keep custom refrigeration fabrication, medical claims, and strenuous heat-exposure testing outside the first prototype.

The completed portfolio should contain:

- A requirements-to-results table.
- CAD assembly, exploded view, manufacturing drawings, and bill of materials.
- Thermal, fluid, energy, and mass calculations.
- Measured-versus-predicted plots and one documented design improvement.
- A short video showing the assembled vest, temperature adjustment, and live measurements.

Your eventual resume entry should use actual results:

“Designed and built a battery-powered liquid-cooling vest with adjustable coolant temperature; validated **[measured cooling capacity]**, **[runtime]**, and **[total mass]** at **[ambient condition]**, improving **[performance metric]** through thermal testing and mechanical redesign.”
