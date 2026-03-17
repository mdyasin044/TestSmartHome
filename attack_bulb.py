import requests
import json
import os
import time
from datetime import datetime

BASE_URL = "http://localhost:8080/api/2"
HEADERS = {"Content-Type": "application/json"}
AUTH = ("ditto", "ditto")
THING_ID = "smarthome:bulb01"

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
BASELINE_DIR = f"all_attacks/bulb_baseline_{timestamp}"
ATTACK_DIR = f"all_attacks/bulb_attacks_{timestamp}"

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

def reset_bulb():
    set_property("power", "is_on", False)
    set_property("brightness", "level", 100)
    set_property("color", "rgb", "255,255,255")
    set_property("temperature", "celsius", 25.0)

print("=" * 40)
print("BULB ATTACK SIMULATION")
print("MITRE ATT&CK Framework")
print("=" * 40)

# Pre-check
r = requests.get(f"{BASE_URL}/things/{THING_ID}", headers=HEADERS, auth=AUTH)
if r.status_code != 200:
    print("ERROR: bulb01 not found. Run create_devices.py first.")
    exit(1)

print("\n[RESET] Resetting bulb to default state...")
reset_bulb()
time.sleep(1)

# Baseline
print("\n[BASELINE] Saving normal state...")
os.makedirs(BASELINE_DIR, exist_ok=True)
save_state(BASELINE_DIR, "bulb01_baseline.json")
time.sleep(2)

# Attacks
os.makedirs(ATTACK_DIR, exist_ok=True)

# --- ATTACK 1: T1565 - Data Manipulation ---
print("\nATTACK 1: T1565 - Data Manipulation")
print("  Action: Force ON at max brightness with red color")
set_property("power", "is_on", True)
set_property("brightness", "level", 255)
set_property("color", "rgb", "255,0,0")
save_state(ATTACK_DIR, "T1565_data_manipulation.json")
time.sleep(2)
reset_bulb()

# --- ATTACK 2: T1499 - Denial of Service ---
print("\nATTACK 2: T1499 - Denial of Service")
print("  Action: Rapidly flipping power 20 times")
for i in range(20):
    set_property("power", "is_on", i % 2 == 0)
save_state(ATTACK_DIR, "T1499_denial_of_service.json")
time.sleep(2)
reset_bulb()

# --- ATTACK 3: T1557 - Sensor Data Spoofing ---
print("\nATTACK 3: T1557 - Sensor Spoofing")
print("  Action: Inject false dangerous temperature")
set_property("temperature", "celsius", 999.9)
save_state(ATTACK_DIR, "T1557_sensor_spoofing.json")
time.sleep(2)
reset_bulb()

# --- ATTACK 4: T1071 - Command and Control ---
print("\nATTACK 4: T1071 - Command and Control")
print("  Action: Blackout — turn off, set color black")
set_property("color", "rgb", "0,0,0")
set_property("brightness", "level", 0)
set_property("power", "is_on", False)
save_state(ATTACK_DIR, "T1071_command_and_control.json")
time.sleep(2)
reset_bulb()

# --- ATTACK 5: T1496 - Resource Hijacking ---
print("\nATTACK 5: T1496 - Resource Hijacking")
print("  Action: Max brightness strobe simulation")
for i in range(10):
    set_property("brightness", "level", 255 if i % 2 == 0 else 0)
save_state(ATTACK_DIR, "T1496_resource_hijacking.json")
reset_bulb()

print("\n" + "=" * 40)
print("BULB SIMULATION COMPLETE")
print("=" * 40)
print(f"Baseline : {BASELINE_DIR}")
print(f"Attacks  : {ATTACK_DIR}")
print(f"\nNext: python compare_attacks.py {BASELINE_DIR} {ATTACK_DIR}")
