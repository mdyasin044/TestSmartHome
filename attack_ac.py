import requests
import json
import os
import time
from datetime import datetime

BASE_URL = "http://localhost:8080/api/2"
HEADERS = {"Content-Type": "application/json"}
AUTH = ("ditto", "ditto")
THING_ID = "smarthome:ac01"

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
BASELINE_DIR = f"all_attacks/ac_baseline_{timestamp}"
ATTACK_DIR = f"all_attacks/ac_attacks_{timestamp}"

def get_thing():
    r = requests.get(f"{BASE_URL}/things/{THING_ID}", headers=HEADERS, auth=AUTH)
    if r.status_code != 200:
        print(f"  ERROR: {r.status_code} - {r.text}")
        return None
    return r.json()

def set_property(feature, prop, value):
    url = f"{BASE_URL}/things/{THING_ID}/features/{feature}/properties/{prop}"
    r = requests.put(url, headers=HEADERS, auth=AUTH, json=value)
    print(f"  SET {feature}.{prop} = {value} → {r.status_code}")

def save_state(directory, filename):
    state = get_thing()
    if state is None:
        return False
    with open(os.path.join(directory, filename), "w") as f:
        json.dump(state, f, indent=2)
    print(f"  Saved: {filename} ✓")
    return True

def reset_ac():
    set_property("power", "is_on", False)
    set_property("temperature", "target_celsius", 24.0)
    set_property("temperature", "current_celsius", 30.0)
    set_property("mode", "current_mode", "cool")
    set_property("fan", "speed", "medium")
    set_property("timer", "is_set", False)
    set_property("status", "error_code", None)
    set_property("status", "filter_clean_needed", False)

print("=" * 40)
print("AC ATTACK SIMULATION")
print("MITRE ATT&CK Framework")
print("=" * 40)

# Pre-check
r = requests.get(f"{BASE_URL}/things/{THING_ID}", headers=HEADERS, auth=AUTH)
if r.status_code != 200:
    print("ERROR: ac01 not found. Run create_devices.py first.")
    exit(1)

print("\n[RESET] Resetting AC to default state...")
reset_ac()
time.sleep(1)

# Baseline
print("\n[BASELINE] Saving normal state...")
os.makedirs(BASELINE_DIR, exist_ok=True)
save_state(BASELINE_DIR, "ac01_baseline.json")
time.sleep(2)

os.makedirs(ATTACK_DIR, exist_ok=True)

# --- ATTACK 1: T1565 - Data Manipulation ---
print("\nATTACK 1: T1565 - Data Manipulation")
print("  Action: Set temperature to dangerous max (30°C target)")
set_property("power", "is_on", True)
set_property("temperature", "target_celsius", 30.0)
set_property("mode", "current_mode", "heat")
save_state(ATTACK_DIR, "T1565_data_manipulation.json")
time.sleep(2)
reset_ac()

# --- ATTACK 2: T1499 - Denial of Service ---
print("\nATTACK 2: T1499 - Denial of Service")
print("  Action: Rapidly cycling power and modes")
modes = ["cool", "heat", "fan", "dry", "auto"]
for i in range(15):
    set_property("power", "is_on", i % 2 == 0)
    set_property("mode", "current_mode", modes[i % len(modes)])
save_state(ATTACK_DIR, "T1499_denial_of_service.json")
time.sleep(2)
reset_ac()

# --- ATTACK 3: T1557 - Sensor Spoofing ---
print("\nATTACK 3: T1557 - Sensor Spoofing")
print("  Action: Inject false current temperature reading")
set_property("temperature", "current_celsius", -10.0)
set_property("status", "error_code", "E404")
save_state(ATTACK_DIR, "T1557_sensor_spoofing.json")
time.sleep(2)
reset_ac()

# --- ATTACK 4: T1071 - Command and Control ---
print("\nATTACK 4: T1071 - Command and Control")
print("  Action: Hijack AC — max heat, max fan, disable timer")
set_property("power", "is_on", True)
set_property("temperature", "target_celsius", 30.0)
set_property("mode", "current_mode", "heat")
set_property("fan", "speed", "high")
set_property("timer", "is_set", False)
save_state(ATTACK_DIR, "T1071_command_and_control.json")
time.sleep(2)
reset_ac()

# --- ATTACK 5: T1485 - Data Destruction ---
print("\nATTACK 5: T1485 - Data Destruction")
print("  Action: Corrupt AC state — trigger false filter alert and error")
set_property("status", "filter_clean_needed", True)
set_property("status", "error_code", "CRITICAL_FAILURE")
set_property("temperature", "min_celsius", 999.0)
set_property("temperature", "max_celsius", -999.0)
save_state(ATTACK_DIR, "T1485_data_destruction.json")
reset_ac()

print("\n" + "=" * 40)
print("AC SIMULATION COMPLETE")
print("=" * 40)
print(f"Baseline : {BASELINE_DIR}")
print(f"Attacks  : {ATTACK_DIR}")
print(f"\nNext: python compare_attacks.py {BASELINE_DIR} {ATTACK_DIR}")
