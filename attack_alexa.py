import requests
import json
import os
import time
from datetime import datetime

BASE_URL = "http://localhost:8080/api/2"
HEADERS = {"Content-Type": "application/json"}
AUTH = ("ditto", "ditto")
THING_ID = "smarthome:alexa01"

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
BASELINE_DIR = f"all_attacks/alexa_baseline_{timestamp}"
ATTACK_DIR = f"all_attacks/alexa_attacks_{timestamp}"

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

def reset_alexa():
    set_property("power", "is_on", True)
    set_property("audio", "volume", 5)
    set_property("audio", "is_muted", False)
    set_property("audio", "is_playing", False)
    set_property("voice_assistant", "is_listening", False)
    set_property("voice_assistant", "last_command", None)
    set_property("smart_home_control", "last_device_controlled", None)
    set_property("status", "do_not_disturb", False)
    set_property("status", "night_mode", False)
    set_property("network", "is_connected", True)

print("=" * 40)
print("ALEXA ATTACK SIMULATION")
print("MITRE ATT&CK Framework")
print("=" * 40)

# Pre-check
r = requests.get(f"{BASE_URL}/things/{THING_ID}", headers=HEADERS, auth=AUTH)
if r.status_code != 200:
    print("ERROR: alexa01 not found. Run create_devices.py first.")
    exit(1)

print("\n[RESET] Resetting Alexa to default state...")
reset_alexa()
time.sleep(1)

# Baseline
print("\n[BASELINE] Saving normal state...")
os.makedirs(BASELINE_DIR, exist_ok=True)
save_state(BASELINE_DIR, "alexa01_baseline.json")
time.sleep(2)

os.makedirs(ATTACK_DIR, exist_ok=True)

# --- ATTACK 1: T1565 - Data Manipulation ---
print("\nATTACK 1: T1565 - Data Manipulation")
print("  Action: Inject fake voice commands and responses")
set_property("voice_assistant", "last_command", "unlock front door")
set_property("voice_assistant", "last_response", "Unlocking front door")
set_property("smart_home_control", "last_device_controlled", "front_door_lock")
save_state(ATTACK_DIR, "T1565_data_manipulation.json")
time.sleep(2)
reset_alexa()

# --- ATTACK 2: T1499 - Denial of Service ---
print("\nATTACK 2: T1499 - Denial of Service")
print("  Action: Spam volume changes and mute toggling")
for i in range(20):
    set_property("audio", "volume", i % 11)
    set_property("audio", "is_muted", i % 2 == 0)
save_state(ATTACK_DIR, "T1499_denial_of_service.json")
time.sleep(2)
reset_alexa()

# --- ATTACK 3: T1557 - Man in the Middle ---
print("\nATTACK 3: T1557 - Man in the Middle")
print("  Action: Spoof network details and disconnect")
set_property("network", "is_connected", False)
set_property("network", "ip_address", "10.0.0.99")
set_property("network", "signal_strength_dbm", -999)
save_state(ATTACK_DIR, "T1557_man_in_the_middle.json")
time.sleep(2)
reset_alexa()

# --- ATTACK 4: T1071 - Command and Control ---
print("\nATTACK 4: T1071 - Command and Control")
print("  Action: Hijack connected devices list and routines")
set_property("smart_home_control", "connected_devices", ["attacker_device"])
set_property("smart_home_control", "active_routines", ["malicious_routine"])
set_property("voice_assistant", "wake_word", "Hey Attacker")
save_state(ATTACK_DIR, "T1071_command_and_control.json")
time.sleep(2)
reset_alexa()

# --- ATTACK 5: T1489 - Service Stop ---
print("\nATTACK 5: T1489 - Service Stop")
print("  Action: Shut down Alexa, enable DND, disable listening")
set_property("power", "is_on", False)
set_property("status", "do_not_disturb", True)
set_property("status", "is_online", False)
set_property("voice_assistant", "is_listening", False)
set_property("network", "is_connected", False)
save_state(ATTACK_DIR, "T1489_service_stop.json")
reset_alexa()

print("\n" + "=" * 40)
print("ALEXA SIMULATION COMPLETE")
print("=" * 40)
print(f"Baseline : {BASELINE_DIR}")
print(f"Attacks  : {ATTACK_DIR}")
print(f"\nNext: python compare_attacks.py {BASELINE_DIR} {ATTACK_DIR}")
