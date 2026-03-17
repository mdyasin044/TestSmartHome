import requests
import json
import os
import time
from datetime import datetime

BASE_URL = "http://localhost:8080/api/2"
HEADERS = {"Content-Type": "application/json"}
AUTH = ("ditto", "ditto")
THING_ID = "smarthome:router01"

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
BASELINE_DIR = f"all_attacks/router_baseline_{timestamp}"
ATTACK_DIR = f"all_attacks/router_attacks_{timestamp}"

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

def reset_router():
    set_property("network", "ssid", "HomeNetwork")
    set_property("network", "dns_primary", "8.8.8.8")
    set_property("network", "dns_secondary", "8.8.4.4")
    set_property("network", "wan_ip", "203.0.113.1")
    set_property("wifi", "is_enabled", True)
    set_property("wifi", "encryption", "WPA2")
    set_property("wifi", "channel", 6)
    set_property("firewall", "is_enabled", True)
    set_property("firewall", "blocked_ips", [])
    set_property("firewall", "intrusion_detection", True)
    set_property("connected_devices", "count", 3)
    set_property("connected_devices", "devices", ["bulb01", "alexa01", "ac01"])
    set_property("traffic", "current_usage_percent", 10)
    set_property("status", "is_online", True)

print("=" * 40)
print("ROUTER ATTACK SIMULATION")
print("MITRE ATT&CK Framework")
print("=" * 40)

# Pre-check
r = requests.get(f"{BASE_URL}/things/{THING_ID}", headers=HEADERS, auth=AUTH)
if r.status_code != 200:
    print("ERROR: router01 not found. Run create_devices.py first.")
    exit(1)

print("\n[RESET] Resetting Router to default state...")
reset_router()
time.sleep(1)

# Baseline
print("\n[BASELINE] Saving normal state...")
os.makedirs(BASELINE_DIR, exist_ok=True)
save_state(BASELINE_DIR, "router01_baseline.json")
time.sleep(2)

os.makedirs(ATTACK_DIR, exist_ok=True)

# --- ATTACK 1: T1565 - Data Manipulation ---
print("\nATTACK 1: T1565 - Data Manipulation")
print("  Action: Change DNS to malicious servers")
set_property("network", "dns_primary", "1.3.3.7")
set_property("network", "dns_secondary", "6.6.6.6")
set_property("network", "ssid", "FreePublicWiFi")
save_state(ATTACK_DIR, "T1565_data_manipulation.json")
time.sleep(2)
reset_router()

# --- ATTACK 2: T1499 - Denial of Service ---
print("\nATTACK 2: T1499 - Denial of Service")
print("  Action: Flood bandwidth usage to 100%")
set_property("traffic", "current_usage_percent", 100)
set_property("traffic", "bytes_sent", 999999999)
set_property("traffic", "bytes_received", 999999999)
for i in range(15):
    set_property("wifi", "channel", i % 13 + 1)
save_state(ATTACK_DIR, "T1499_denial_of_service.json")
time.sleep(2)
reset_router()

# --- ATTACK 3: T1557 - Man in the Middle ---
print("\nATTACK 3: T1557 - Man in the Middle")
print("  Action: Disable firewall, disable intrusion detection")
set_property("firewall", "is_enabled", False)
set_property("firewall", "intrusion_detection", False)
set_property("wifi", "encryption", "NONE")
set_property("network", "wan_ip", "10.0.0.1")
save_state(ATTACK_DIR, "T1557_man_in_the_middle.json")
time.sleep(2)
reset_router()

# --- ATTACK 4: T1071 - Command and Control ---
print("\nATTACK 4: T1071 - Command and Control")
print("  Action: Hijack connected devices, block legitimate IPs")
set_property("connected_devices", "devices", ["attacker_device"])
set_property("connected_devices", "count", 1)
set_property("firewall", "blocked_ips", ["192.168.1.101", "192.168.1.102"])
save_state(ATTACK_DIR, "T1071_command_and_control.json")
time.sleep(2)
reset_router()

# --- ATTACK 5: T1489 - Service Stop ---
print("\nATTACK 5: T1489 - Service Stop")
print("  Action: Disable WiFi and take router offline")
set_property("wifi", "is_enabled", False)
set_property("status", "is_online", False)
set_property("connected_devices", "count", 0)
set_property("connected_devices", "devices", [])
save_state(ATTACK_DIR, "T1489_service_stop.json")
reset_router()

print("\n" + "=" * 40)
print("ROUTER SIMULATION COMPLETE")
print("=" * 40)
print(f"Baseline : {BASELINE_DIR}")
print(f"Attacks  : {ATTACK_DIR}")
print(f"\nNext: python compare_attacks.py {BASELINE_DIR} {ATTACK_DIR}")
