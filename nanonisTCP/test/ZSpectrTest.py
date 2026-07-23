# -*- coding: utf-8 -*-
"""
Test script for the ZSpectr (Z Spectroscopy) module.
Tests each function one by one with print statements to verify correct operation.
"""

from nanonisTCP import nanonisTCP
from nanonisTCP.ZSpectr import ZSpectr


TCP_IP   = '127.0.0.1'                             # Local host
TCP_PORT = 6501                                    # Check available ports in NANONIS > File > Settings Options > TCP Programming Interface

NTCP = nanonisTCP(TCP_IP, TCP_PORT, version=15809)
zspectr = ZSpectr(NTCP)

print("=" * 60)
print("ZSpectr Module Test Script")
print("=" * 60)

# -----------------------------------------------------------------------------
print("\n--- ZSpectr.Open ---")
zspectr.Open()
print("ZSpectr module opened successfully.")

# -----------------------------------------------------------------------------
print("\n--- ZSpectr.StatusGet ---")
status = zspectr.StatusGet()
print(f"Status: {status} ({'Running' if status == 1 else 'Not running'})")

# -----------------------------------------------------------------------------
print("\n--- ZSpectr.ChsSet ---")
channel_indexes = [0, 1]
zspectr.ChsSet(channel_indexes, mode="set")
print(f"Channels set to: {channel_indexes}")

# -----------------------------------------------------------------------------
print("\n--- ZSpectr.ChsGet ---")
ch_indexes, ch_names = zspectr.ChsGet()
print(f"Channel indexes : {ch_indexes}")
print(f"Channel names   : {ch_names}")

# Test add mode
print("\n  Testing ChsSet add mode (adding channel 2)...")
zspectr.ChsSet([2], mode="add")
ch_indexes, ch_names = zspectr.ChsGet()
print(f"  After add  - indexes: {ch_indexes}, names: {ch_names}")

# Test remove mode
print("\n  Testing ChsSet remove mode (removing channel 2)...")
zspectr.ChsSet([2], mode="remove")
ch_indexes, ch_names = zspectr.ChsGet()
print(f"  After remove - indexes: {ch_indexes}, names: {ch_names}")

# -----------------------------------------------------------------------------
#print("\n--- ZSpectr.PropsSet ---")
#zspectr.PropsSet(
#    back_sweep  = 1,    # Acquire backward sweep
#    num_points  = 100,
#    num_sweeps  = 1,
#    autosave    = 2,    # Autosave off
#    save_dialog = 2,    # Don't show save dialog
#    save_all    = 2,    # Don't save individual sweeps
#)
#print("Properties set: back_sweep=1, num_points=100, num_sweeps=1, autosave=off, save_dialog=off, save_all=off")

# -----------------------------------------------------------------------------
print("\n--- ZSpectr.PropsGet ---")
props = zspectr.PropsGet()
print(f"back_sweep       : {props['back_sweep']}")
print(f"num_points       : {props['num_points']}")
print(f"num_sweeps       : {props['num_sweeps']}")
print(f"autosave         : {props['autosave']}")
print(f"save_dialog      : {props['save_dialog']}")
print(f"save_all         : {props['save_all']}")
print(f"parameters       : {props['parameters']}")
print(f"fixed_parameters : {props['fixed_parameters']}")

# -----------------------------------------------------------------------------
print("\n--- ZSpectr.AdvPropsSet ---")
zspectr.AdvPropsSet(
    time_bw_sweep  = 0.01,  # 10 ms between forward and backward sweep
    record_final_z = 1,     # On
    lockin_run     = 2,     # Off
    reset_z        = 1,     # On
)
print("Advanced properties set: time_bw_sweep=0.01s, record_final_z=on, lockin_run=off, reset_z=on")

# -----------------------------------------------------------------------------
print("\n--- ZSpectr.AdvPropsGet ---")
adv_props = zspectr.AdvPropsGet()
print(f"time_bw_sweep  : {adv_props['time_bw_sweep']} s")
print(f"record_final_z : {adv_props['record_final_z']} (0=Off, 1=On)")
print(f"lockin_run     : {adv_props['lockin_run']} (0=Off, 1=On)")
print(f"reset_z        : {adv_props['reset_z']} (0=Off, 1=On)")

# -----------------------------------------------------------------------------
print("\n--- ZSpectr.RangeSet ---")
z_offset         = 0.0      # No offset (m)
z_sweep_distance = 5e-9     # 5 nm sweep
zspectr.RangeSet(z_offset, z_sweep_distance)
print(f"Range set: z_offset={z_offset} m, z_sweep_distance={z_sweep_distance} m")

# -----------------------------------------------------------------------------
print("\n--- ZSpectr.RangeGet ---")
rng = zspectr.RangeGet()
print(f"z_offset         : {rng['z_offset']} m")
print(f"z_sweep_distance : {rng['z_sweep_distance']} m")

# -----------------------------------------------------------------------------
print("\n--- ZSpectr.TimingSet ---")
zspectr.TimingSet(
    z_averaging_time      = 0.05,   # s
    initial_settling_time = 0.01,   # s
    maximum_slew_rate     = 1.0,    # V/s
    settling_time         = 0.001,  # s
    integration_time      = 0.01,   # s
    end_settling_time     = 0.001,  # s
    z_control_time        = 0.05,   # s
)
print("Timing set successfully.")

# -----------------------------------------------------------------------------
print("\n--- ZSpectr.TimingGet ---")
timing = zspectr.TimingGet()
print(f"z_averaging_time      : {timing['z_averaging_time']} s")
print(f"initial_settling_time : {timing['initial_settling_time']} s")
print(f"maximum_slew_rate     : {timing['maximum_slew_rate']} V/s")
print(f"settling_time         : {timing['settling_time']} s")
print(f"integration_time      : {timing['integration_time']} s")
print(f"end_settling_time     : {timing['end_settling_time']} s")
print(f"z_control_time        : {timing['z_control_time']} s")

# -----------------------------------------------------------------------------
print("\n--- ZSpectr.RetractDelaySet ---")
retract_delay = 0.05    # 50 ms
zspectr.RetractDelaySet(retract_delay)
print(f"Retract delay set to: {retract_delay} s")

# -----------------------------------------------------------------------------
print("\n--- ZSpectr.RetractDelayGet ---")
retract_delay_get = zspectr.RetractDelayGet()
print(f"Retract delay: {retract_delay_get} s")

# -----------------------------------------------------------------------------
#print("\n--- ZSpectr.RetractSet ---")
#zspectr.RetractSet(
#    enable       = 2,       # Off
#    threshold    = 1e-9,    # 1 nA
#    signal_index = 1,       # Signal index 1 (Current)
#    comparison   = 0,       # >
#)
#print("Auto retract main condition set: enable=off, threshold=1e-9, signal_index=1, comparison='>'")

# -----------------------------------------------------------------------------
print("\n--- ZSpectr.RetractGet ---")
retract = zspectr.RetractGet()
print(f"enable       : {retract['enable']} (0=Off, 1=On)")
print(f"threshold    : {retract['threshold']}")
print(f"signal_index : {retract['signal_index']}")
print(f"comparison   : {retract['comparison']} (0='>', 1='<')")

# -----------------------------------------------------------------------------
#print("\n--- ZSpectr.Retract2ndSet ---")
#zspectr.Retract2ndSet(
#    condition_2nd = 1,      # -No- (disable 2nd condition)
#    threshold     = 0.0,
#    signal_index  = -1,     # Leave unchanged
#    comparison    = 2,      # No change
#)
#print("Auto retract 2nd condition set: condition=-No-, signal_index unchanged")

# -----------------------------------------------------------------------------
print("\n--- ZSpectr.Retract2ndGet ---")
retract2nd = zspectr.Retract2ndGet()
cond_labels = {0: '-No-', 1: 'OR', 2: 'AND', 3: 'THEN'}
print(f"condition_2nd : {retract2nd['condition_2nd']} ({cond_labels.get(retract2nd['condition_2nd'], '?')})")
print(f"threshold     : {retract2nd['threshold']}")
print(f"signal_index  : {retract2nd['signal_index']}")
print(f"comparison    : {retract2nd['comparison']} (0='>', 1='<')")

# -----------------------------------------------------------------------------
print("\n--- ZSpectr.DigSyncSet ---")
zspectr.DigSyncSet(1)   # Off
print("Digital sync set to: 1 (Off)")

# -----------------------------------------------------------------------------
print("\n--- ZSpectr.DigSyncGet ---")
dig_sync = zspectr.DigSyncGet()
dig_sync_labels = {0: 'Off', 1: 'TTL Sync', 2: 'Pulse Sequence'}
print(f"Digital sync: {dig_sync} ({dig_sync_labels.get(dig_sync, '?')})")

# -----------------------------------------------------------------------------
print("\n--- ZSpectr.TTLSyncSet ---")
zspectr.TTLSyncSet(
    ttl_line     = 1,       # HS Line 1
    ttl_polarity = 2,       # High Active
    time_to_on   = 0.001,   # 1 ms
    on_duration  = 0.005,   # 5 ms
)
print("TTL sync set: line=HS Line 1, polarity=High Active, time_to_on=1ms, on_duration=5ms")

# -----------------------------------------------------------------------------
print("\n--- ZSpectr.TTLSyncGet ---")
ttl = zspectr.TTLSyncGet()
ttl_line_labels     = {0: 'HS Line 1', 1: 'HS Line 2', 2: 'HS Line 3', 3: 'HS Line 4'}
ttl_polarity_labels = {0: 'Low Active', 1: 'High Active'}
print(f"ttl_line     : {ttl['ttl_line']} ({ttl_line_labels.get(ttl['ttl_line'], '?')})")
print(f"ttl_polarity : {ttl['ttl_polarity']} ({ttl_polarity_labels.get(ttl['ttl_polarity'], '?')})")
print(f"time_to_on   : {ttl['time_to_on']} s")
print(f"on_duration  : {ttl['on_duration']} s")

# -----------------------------------------------------------------------------
print("\n--- ZSpectr.PulseSeqSyncSet ---")
zspectr.PulseSeqSyncSet(pulse_seq_nr=1, nr_periods=10)
print("Pulse sequence sync set: pulse_seq_nr=1, nr_periods=10")

# -----------------------------------------------------------------------------
print("\n--- ZSpectr.PulseSeqSyncGet ---")
pulse = zspectr.PulseSeqSyncGet()
print(f"pulse_seq_nr : {pulse['pulse_seq_nr']}")
print(f"nr_periods   : {pulse['nr_periods']}")

# -----------------------------------------------------------------------------
print("\n--- ZSpectr.Start (without data) ---")
zspectr.Start(get_data=0)
print("Sweep started (not waiting for data).")

print("\n--- ZSpectr.Stop ---")
zspectr.Stop()
print("Sweep stopped.")

# -----------------------------------------------------------------------------
print("\n--- ZSpectr.Start (with data) ---")
print("Starting sweep and retrieving data...")
result = zspectr.Start(get_data=1, save_base_name="")
if result is not None:
    print(f"Channels returned : {list(result['data_dict'].keys())}")
    for ch_name, ch_data in result['data_dict'].items():
        print(f"  {ch_name}: {len(ch_data)} points, min={ch_data.min():.4e}, max={ch_data.max():.4e}")
    print(f"Parameters        : {result['parameters']}")
else:
    print("No data returned.")

# -----------------------------------------------------------------------------
print("\n" + "=" * 60)
print("All ZSpectr tests completed.")
print("=" * 60)

NTCP.close_connection()
