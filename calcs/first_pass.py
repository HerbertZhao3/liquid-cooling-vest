"""First-pass sizing calculations for the liquid-cooling vest (plan v3).

Phase 1 sections size the ice-buffer prototype that gets built. Phase 2
sections size the compressor-chiller backpack design study.

Inputs marked ASSUMED are placeholders. Replace each one with a measured or
vendor-confirmed value as tests produce it, and note the change in
docs/decision-log.md.

Run:  python3 calcs/first_pass.py      (standard library only)
"""

import math

# Water near 22 °C
RHO = 997.8  # kg/m^3
CP = 4181.0  # J/(kg K)
MU = 0.955e-3  # Pa s
K_WATER = 0.60  # W/(m K)
ICE_LATENT = 334e3  # J/kg

# Air near 35 °C (condenser exhaust side)
RHO_AIR = 1.15  # kg/m^3
CP_AIR = 1007.0  # J/(kg K)

# Design point
FLOW_LPM = 0.5  # vest loop flow
LOAD_W = 75.0  # design heat load
SETPOINT_C = 20.0  # vest inlet
SURFACE_C = 34.0  # heated-torso water temperature, standing in for skin
AMBIENT_C = 30.0  # Phase 2 outdoor design ambient
RUNTIME_H = 1.0

# Garment
TUBE_ID = 0.004  # m
TUBE_OD = 0.006  # m
VEST_TUBE_M = 18.0  # two parallel branches of ~9 m, ASSUMED
K_TUBE = 0.25  # W/(m K), polyurethane, ASSUMED
G_CONTACT = 1.0  # W/(m K) per metre of tube, torso water → container wall → fabric → tube; ASSUMED, fit on the torso rig

# Phase 1 ice buffer (vacuum-insulated food jar)
ICE_KG = 0.6  # ASSUMED charge
ICE_WATER_KG = 0.4
BUFFER_MAX_C = 15.0  # ASSUMED: above this, injection can no longer hold a 20 °C setpoint with margin
BUFFER_GAIN_W = 5.0  # ASSUMED: heat leaking into the jar and the injection line

# Phase 2 chiller: RIGID DV1920E-P(S) datasheet values
CHILLER_MASS_KG = 3.5  # datasheet; the store listing says 3.0 — confirm
LIGHT_CHILLER_MASS_KG = 2.75  # RIGID personal-wear unit (260 W), listed on its website
CHILLER_DIMS_MM = (230, 200, 145)
CHILLER_Q_MIN_W = 120.0  # ASSUMED: datasheet floor is 100 W at 2,000 rpm, rating conditions not stated
RESTART_DELAY_S = 180.0  # ASSUMED: fault recovery in the datasheet is 3 min; confirm pressure-equalisation time
MIN_ON_TIME_S = 120.0  # ASSUMED: conservative minimum run time for oil return
COMPRESSOR_COP = 2.0  # ASSUMED, buffer at ~12 °C, 30 °C ambient
COLD_BUFFER_KG = 0.45  # from section 8
BATTERY_WH = 126.0  # 7S1P 21700 5 Ah
BATTERY_WH_PER_KG = 200.0  # ASSUMED pack level, including BMS and wrap
BATTERY_USABLE = 0.85 * 0.90  # BMS cut-off/temperature × ageing margin


def lpm_to_m3s(lpm):
    return lpm / 60000.0


def mass_flow(lpm):
    return RHO * lpm_to_m3s(lpm)


def temp_rise(q_w, lpm):
    return q_w / (mass_flow(lpm) * CP)


def laminar_pipe(length_m, id_m, lpm):
    """Hagen-Poiseuille pressure drop; returns (dp_pa, velocity_m_s, reynolds)."""
    q = lpm_to_m3s(lpm)
    area = math.pi * id_m**2 / 4
    v = q / area
    re = RHO * v * id_m / MU
    dp = 128 * MU * length_m * q / (math.pi * id_m**4)
    return dp, v, re


def tube_volume_l(length_m, id_m):
    return math.pi * id_m**2 / 4 * length_m * 1000


def dew_point_c(t_c, rh_pct):
    """Magnus approximation (Sonntag constants)."""
    a, b = 17.62, 243.12
    g = math.log(rh_pct / 100) + a * t_c / (b + t_c)
    return b * g / (a - g)


def rh_at_dew_point(t_c, dew_c):
    """Relative humidity (%) at which air at t_c has dew point dew_c."""
    a, b = 17.62, 243.12
    return 100 * math.exp(a * dew_c / (b + dew_c) - a * t_c / (b + t_c))


def tube_conductance_per_m(g_contact=G_CONTACT):
    """Surface-to-coolant conductance per metre of tube, W/(m K)."""
    g_inside = 3.66 * K_WATER * math.pi  # fully developed laminar flow, Nu = 3.66
    g_wall = 2 * math.pi * K_TUBE / math.log(TUBE_OD / TUBE_ID)
    return 1 / (1 / g_inside + 1 / g_wall + 1 / g_contact)


def garment_heat(t_in, lpm, g_contact=G_CONTACT):
    """Effectiveness-NTU: heat the vest takes from an isothermal surface.

    Two equal branches at half flow have the same NTU as one branch of the
    full length at full flow, so the vest is modelled as a single tube.
    """
    c = mass_flow(lpm) * CP
    ua = tube_conductance_per_m(g_contact) * VEST_TUBE_M
    return c * (SURFACE_C - t_in) * (1 - math.exp(-ua / c))


def ice_charge_kj(ice_kg, water_kg):
    return (ice_kg * ICE_LATENT + (ice_kg + water_kg) * CP * BUFFER_MAX_C) / 1000


def heading(title):
    print(f"\n== {title} ==")


# ---------------------------------------------------------------- Phase 1

def water_side_rise():
    heading("1. Water-side temperature rise at 0.5 L/min")
    # Per-sensor uncertainty after matched calibration in a stirred bath
    sensor_u = 0.05  # K, ASSUMED target
    dt_u = math.sqrt(2) * sensor_u
    print(f"{'Load (W)':>9} {'dT (K)':>8} {'dT uncertainty':>16}")
    for q in (25, 50, 75, 100):
        dt = temp_rise(q, FLOW_LPM)
        print(f"{q:>9} {dt:>8.2f} {dt_u / dt * 100:>15.1f}%")
    print(f"(matched sensors at ±{sensor_u} K each → ±{dt_u:.3f} K on dT; "
          "heater electrical power is the better reference at low loads)")


def hydraulics():
    heading("2. Vest-loop pressure drop (laminar, straight tube only)")
    branch_len = VEST_TUBE_M / 2
    hose_len = 2 * 1.2  # m, supply + return to the backpack
    hose_id = 0.006
    for tube_id in (TUBE_ID, 0.003):
        dp_b, v_b, re_b = laminar_pipe(branch_len, tube_id, FLOW_LPM / 2)
        dp_h, _, re_h = laminar_pipe(hose_len, hose_id, FLOW_LPM)
        total = dp_b + dp_h
        print(f"{tube_id * 1000:.0f} mm ID: branch {dp_b / 1000:.1f} kPa "
              f"(v={v_b:.2f} m/s, Re={re_b:.0f}), hoses {dp_h / 1000:.2f} kPa "
              f"(Re={re_h:.0f}) → {total / 1000:.1f} kPa before fittings")
    print("Quick disconnects, manifolds and barbs are not modelled: "
          "measure them; budget 10–20 kPa extra until measured.")
    hydraulic_w = 25e3 * lpm_to_m3s(FLOW_LPM)
    print(f"Hydraulic power at 25 kPa and 0.5 L/min: {hydraulic_w:.2f} W "
          "(pump electrical draw is set by pump efficiency, not by this)")


def garment_model():
    heading("3. Garment heat removal on the heated torso (effectiveness-NTU)")
    g = tube_conductance_per_m()
    print(f"Conductance per metre: {g:.2f} W/(m K) with contact term {G_CONTACT} (ASSUMED); "
          f"UA = {g * VEST_TUBE_M:.1f} W/K over {VEST_TUBE_M:.0f} m")
    flows = (0.3, 0.5, 0.7)
    print(f"{'Inlet (°C)':>11}" + "".join(f"{f'{f} L/min':>12}" for f in flows))
    for t_in in (20.0, 24.0, 28.0):
        print(f"{t_in:>11.0f}" + "".join(f"{garment_heat(t_in, f):>10.0f} W" for f in flows))
    print("Contact term sensitivity at 20 °C inlet, 0.5 L/min:")
    for gc in (0.5, 1.0, 2.0):
        print(f"  {gc} W/(m K) → {garment_heat(SETPOINT_C, FLOW_LPM, gc):.0f} W")
    print("The contact term dominates: fit it from one torso-rig run, then predict the others.")


def ice_buffer():
    heading("4. Ice buffer: injection flow and runtime")
    t_return = SETPOINT_C + temp_rise(LOAD_W, FLOW_LPM)
    for t_buf in (0.0, 8.0, BUFFER_MAX_C):
        m_inj = LOAD_W / (CP * (t_return - t_buf))
        print(f"  buffer at {t_buf:4.1f} °C → {m_inj / RHO * 60000:.3f} L/min injected to hold "
              f"{SETPOINT_C:.0f} °C at {LOAD_W:.0f} W")
    stored = ice_charge_kj(ICE_KG, ICE_WATER_KG)
    print(f"Charge: {ICE_KG} kg ice + {ICE_WATER_KG} kg water, usable to {BUFFER_MAX_C:.0f} °C "
          f"→ {stored:.0f} kJ")
    for q in (50.0, 75.0, 100.0):
        print(f"  {q:.0f} W load → {stored * 1000 / (q + BUFFER_GAIN_W) / 60:.0f} min")


def phase1_mass():
    heading("5. Phase 1 wearable mass (estimates)")
    vest_water = tube_volume_l(VEST_TUBE_M, TUBE_ID) + tube_volume_l(2.4, 0.006)
    items = {
        "vacuum food jar, 1.2 L": 0.45,
        "ice + water charge": ICE_KG + ICE_WATER_KG,
        f"vest tubing, PU 4x6 mm, {VEST_TUBE_M:.0f} m": 0.36,
        "compression shirt + channels": 0.25,
        "manifolds + quick disconnect": 0.10,
        "water in vest and hoses": vest_water * RHO / 1000,
        "pumps x2": 0.12,
        "ESP32, display, board": 0.10,
        "hoses + insulation": 0.08,
        "USB-C power bank": 0.20,
        "printed housing + strap (CV-102/103)": 0.35,
    }
    for name, kg in items.items():
        print(f"  {name:<36} {kg:5.2f} kg")
    total = sum(items.values())
    print(f"  {'total':<36} {total:5.2f} kg   (target ≤ 3.5 kg)")
    return total


def dew_points():
    heading("6. Condensation: dew point at 30 °C")
    for rh in (40, 50, 60, 70):
        print(f"  {rh}% RH → dew point {dew_point_c(AMBIENT_C, rh):.1f} °C")
    for surface_c, what in ((SETPOINT_C, "vest tubing at the 20 °C setpoint"),
                            (16.0, "buffer at 16 °C"), (8.0, "buffer at 8 °C")):
        print(f"  {what} sweats above {rh_at_dew_point(AMBIENT_C, surface_c):.0f}% RH")


# ---------------------------------------------------------------- Phase 2

def water_inventory():
    heading("7. Phase 2 water inventory")
    vest = tube_volume_l(VEST_TUBE_M, TUBE_ID)
    hoses = tube_volume_l(2.4, 0.006)
    evaporator = 0.05  # L, ASSUMED
    plumbing = 0.05  # L, ASSUMED: pump heads, tees, sensors, QDs
    parts = {f"vest tubing ({VEST_TUBE_M:.0f} m, 4 mm ID)": vest, "hoses (2.4 m, 6 mm ID)": hoses,
             "evaporator": evaporator, "pumps/fittings": plumbing, "cold buffer": COLD_BUFFER_KG}
    for name, vol in parts.items():
        print(f"  {name:<30} {vol:5.2f} L")
    total = sum(parts.values())
    print(f"  {'total':<30} {total:5.2f} L   (v1 target was 0.30 L)")
    return total


def cycling():
    heading("8. Phase 2 compressor cycling and cold-buffer sizing")
    # v1: single loop, the whole 0.3 L inventory is the only thermal mass
    c_v1 = 0.30 * CP
    rise = LOAD_W * RESTART_DELAY_S / c_v1
    print(f"v1 single loop, 0.30 L: one forced {RESTART_DELAY_S:.0f} s off-period "
          f"at {LOAD_W:.0f} W raises the vest inlet by {rise:.1f} K (target ±1 K)")
    print(f"Datasheet floor capacity (≥100 W) exceeds the {LOAD_W:.0f} W load, "
          "so the compressor must cycle.")

    print("\nCold buffer swinging between band limits below the setpoint:")
    print(f"{'Band (K)':>9} {'Load (W)':>9} {'kg for off-time':>16} {'kg for on-time':>15}")
    for band in (6.0, 8.0):
        for q in (25.0, 50.0, 75.0):
            m_off = q * RESTART_DELAY_S / (CP * band)
            m_on = (CHILLER_Q_MIN_W - q) * MIN_ON_TIME_S / (CP * band)
            print(f"{band:>9.0f} {q:>9.0f} {m_off:>16.2f} {m_on:>15.2f}")
    print(f"Largest entry sets the buffer: ≈{COLD_BUFFER_KG} kg for an 8 K band (e.g. 8–16 °C).")
    print("Colder/wider band = less buffer mass but lower compressor COP.")
    stored = COLD_BUFFER_KG * CP * 8.0
    print(f"The buffer also bridges a tilt or fall shutdown: {stored / LOAD_W / 60:.1f} min "
          f"of cooling at {LOAD_W:.0f} W.")


def power_and_battery():
    heading("9. Phase 2 electrical power and battery (all ASSUMED until measured)")
    buffer_leak_w = 4.0  # ASSUMED, insulated buffer in a warm pack
    loads = {
        "compressor": (LOAD_W + buffer_leak_w) / COMPRESSOR_COP,
        "condenser fan": 4.8,
        "vest pump": 3.0,
        "chiller-loop pump (60 % duty)": 3.0 * 0.6,
        "injection pump": 1.0,
        "electronics + converter losses": 2.5,
    }
    for name, w in loads.items():
        print(f"  {name:<32} {w:5.1f} W")
    total = sum(loads.values())
    print(f"  {'total':<32} {total:5.1f} W   (target ≤ 60 W)")
    need = total * RUNTIME_H / BATTERY_USABLE
    print(f"Nominal battery for {RUNTIME_H * 60:.0f} min: {need:.0f} Wh "
          f"(usable fraction {BATTERY_USABLE:.2f}); 7S1P 21700 5 Ah ≈ {BATTERY_WH:.0f} Wh")
    return total


def heat_rejection(electrical_w):
    heading("10. Phase 2 condenser heat rejection")
    q_rej = LOAD_W + 4.0 + electrical_w * 0.85  # most electrical input ends up as heat in the pack
    for cfm in (10, 15, 25):
        m_air = RHO_AIR * cfm * 0.000471947
        print(f"  {q_rej:.0f} W into {cfm} CFM → exhaust {AMBIENT_C + q_rej / (m_air * CP_AIR):.0f} °C "
              f"at {AMBIENT_C:.0f} °C intake")
    print("Any exhaust recirculation raises the intake above 30 °C — the chiller's "
          "listed upper temperature limit (confirm whether that is ambient).")


def phase2_mass(water_l):
    heading("11. Phase 2 wearable mass budget (estimates)")
    items = {
        "chiller module": CHILLER_MASS_KG,
        f"battery, 7S {BATTERY_WH:.0f} Wh": BATTERY_WH / BATTERY_WH_PER_KG,
        "water": water_l * RHO / 1000,
        f"vest tubing, PU 4x6 mm, {VEST_TUBE_M:.0f} m": 0.36,
        "base garment + channels": 0.25,
        "manifolds + quick disconnects": 0.12,
        "pumps x3": 0.20,
        "buffer reservoir + insulation": 0.15,
        "insulated hoses": 0.12,
        "electronics, wiring, fuse, switch": 0.20,
        "frame, brackets, ducts": 0.40,
        "backpack": 0.50,
    }
    for name, kg in items.items():
        print(f"  {name:<36} {kg:5.2f} kg")
    total = sum(items.values())
    print(f"  {'total':<36} {total:5.2f} kg   (target ≤ 6.0 kg)")
    print(f"  with the 3.0 kg chiller configuration: {total - CHILLER_MASS_KG + 3.0:.2f} kg")
    print(f"  with RIGID's 2.75 kg personal-wear unit: "
          f"{total - CHILLER_MASS_KG + LIGHT_CHILLER_MASS_KG:.2f} kg")
    return total - items[f"battery, 7S {BATTERY_WH:.0f} Wh"]


def volume_budget():
    heading("12. Phase 2 backpack volume (estimates)")
    chiller_l = math.prod(CHILLER_DIMS_MM) / 1e6
    items = {"chiller": chiller_l, "battery": 0.3, "pumps, buffer, plumbing": 1.2,
             "electronics": 0.3, "intake/exhaust plenums": 2.5, "frame + clearances": 1.5}
    for name, vol in items.items():
        print(f"  {name:<26} {vol:5.2f} L")
    print(f"  {'total':<26} {sum(items.values()):5.2f} L   (target ≤ 15 L)")


def ice_vs_compressor(phase1_kg, phase2_dry_kg, electrical_w):
    heading("13. Ice vs compressor: wearable mass against runtime at 75 W")
    container_ratio = 0.45  # ASSUMED: vacuum-jar mass per kg of ice it holds
    ice_kg_per_h = (LOAD_W + BUFFER_GAIN_W) * 3600 / (ICE_LATENT + CP * BUFFER_MAX_C)
    ice_fixed = phase1_kg - (ICE_KG + ICE_WATER_KG) - 0.45
    ice_slope = ice_kg_per_h * (1 + container_ratio)
    batt_slope = electrical_w / BATTERY_USABLE / BATTERY_WH_PER_KG
    comp_fixed = {"3.5 kg chiller": phase2_dry_kg,
                  "2.75 kg chiller": phase2_dry_kg - CHILLER_MASS_KG + LIGHT_CHILLER_MASS_KG}
    print(f"Ice: {ice_fixed:.2f} kg + {ice_slope:.2f} kg/h (pure-ice charge plus jar); "
          f"compressor: fixed + {batt_slope:.2f} kg/h of battery")
    print(f"{'Hours':>6} {'Ice (kg)':>10}" + "".join(f"{name:>17}" for name in comp_fixed))
    for h in (1, 2, 4, 6, 8):
        row = f"{h:>6} {ice_fixed + ice_slope * h:>10.1f}"
        row += "".join(f"{fixed + batt_slope * h:>17.1f}" for fixed in comp_fixed.values())
        print(row)
    for name, fixed in comp_fixed.items():
        print(f"  break-even with the {name}: {(fixed - ice_fixed) / (ice_slope - batt_slope):.1f} h")
    print("Ice needs a freezer and a refill each charge; the compressor runs as long as the battery.")


def main():
    print("PHASE 1 — ice-buffer prototype (built)")
    water_side_rise()
    hydraulics()
    garment_model()
    ice_buffer()
    phase1_kg = phase1_mass()
    dew_points()

    print("\n\nPHASE 2 — compressor backpack (design study)")
    water_l = water_inventory()
    cycling()
    electrical_w = power_and_battery()
    heat_rejection(electrical_w)
    phase2_dry_kg = phase2_mass(water_l)
    volume_budget()
    ice_vs_compressor(phase1_kg, phase2_dry_kg, electrical_w)


if __name__ == "__main__":
    main()
