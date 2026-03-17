import requests

BASE_URL = "http://localhost:8080/api/2"
HEADERS = {"Content-Type": "application/json"}
AUTH = ("ditto", "ditto")

def create_policy(policy_id):
    policy = {
        "entries": {
            "owner": {
                "subjects": {
                    "nginx:ditto": {"type": "nginx-authenticated"}
                },
                "resources": {
                    "thing:/": {"grant": ["READ", "WRITE"], "revoke": []},
                    "policy:/": {"grant": ["READ", "WRITE"], "revoke": []},
                    "message:/": {"grant": ["READ", "WRITE"], "revoke": []}
                }
            }
        }
    }
    response = requests.put(
        f"{BASE_URL}/policies/{policy_id}",
        headers=HEADERS, auth=AUTH, json=policy
    )
    status = "✓" if response.status_code in (200, 201, 204) else f"✗ {response.text}"
    print(f"  Policy [{policy_id}]: {response.status_code} {status}")

def create_bulb():
    bulb = {
        "policyId": "smarthome:policy-bulb",
        "attributes": {
            "name": "Living Room Bulb",
            "type": "smart-bulb",
            "location": "living_room"
        },
        "features": {
            "power": {"properties": {"is_on": False}},
            "brightness": {"properties": {"level": 100}},
            "color": {"properties": {"rgb": "255,255,255"}},
            "temperature": {"properties": {"celsius": 25.0}}
        }
    }
    r = requests.put(f"{BASE_URL}/things/smarthome:bulb01",
                     headers=HEADERS, auth=AUTH, json=bulb)
    status = "✓" if r.status_code in (200, 201, 204) else f"✗ {r.text}"
    print(f"  Bulb [smarthome:bulb01]: {r.status_code} {status}")

def create_ac():
    ac = {
        "policyId": "smarthome:policy-ac",
        "attributes": {
            "name": "Living Room AC",
            "type": "smart-ac",
            "location": "living_room",
            "manufacturer": "Generic",
            "model": "SmartCool-01"
        },
        "features": {
            "power": {"properties": {"is_on": False}},
            "temperature": {
                "properties": {
                    "target_celsius": 24.0,
                    "current_celsius": 30.0,
                    "min_celsius": 16.0,
                    "max_celsius": 30.0
                }
            },
            "mode": {
                "properties": {
                    "current_mode": "cool",
                    "available_modes": ["cool", "heat", "fan", "dry", "auto"]
                }
            },
            "fan": {
                "properties": {
                    "speed": "medium",
                    "available_speeds": ["low", "medium", "high", "auto"]
                }
            },
            "timer": {
                "properties": {
                    "is_set": False,
                    "turn_off_after_minutes": 0
                }
            },
            "status": {
                "properties": {
                    "is_online": True,
                    "error_code": None,
                    "filter_clean_needed": False
                }
            }
        }
    }
    r = requests.put(f"{BASE_URL}/things/smarthome:ac01",
                     headers=HEADERS, auth=AUTH, json=ac)
    status = "✓" if r.status_code in (200, 201, 204) else f"✗ {r.text}"
    print(f"  AC [smarthome:ac01]: {r.status_code} {status}")

def create_alexa():
    alexa = {
        "policyId": "smarthome:policy-alexa",
        "attributes": {
            "name": "Alexa Echo Dot",
            "type": "smart-speaker",
            "location": "living_room",
            "manufacturer": "Amazon",
            "model": "Echo Dot Gen 4"
        },
        "features": {
            "power": {
                "properties": {
                    "is_on": True,
                    "power_consumption_watts": 15
                }
            },
            "audio": {
                "properties": {
                    "volume": 5,
                    "is_muted": False,
                    "is_playing": False,
                    "current_track": None
                }
            },
            "voice_assistant": {
                "properties": {
                    "is_listening": False,
                    "wake_word": "Alexa",
                    "last_command": None,
                    "last_response": None
                }
            },
            "smart_home_control": {
                "properties": {
                    "connected_devices": ["bulb01", "ac01", "router01"],
                    "active_routines": ["morning", "night"],
                    "last_device_controlled": None
                }
            },
            "network": {
                "properties": {
                    "is_connected": True,
                    "ip_address": "192.168.1.101",
                    "mac_address": "AA:BB:CC:DD:EE:FF",
                    "signal_strength_dbm": -60
                }
            },
            "status": {
                "properties": {
                    "firmware_version": "1.0.0",
                    "is_online": True,
                    "do_not_disturb": False,
                    "night_mode": False
                }
            }
        }
    }
    r = requests.put(f"{BASE_URL}/things/smarthome:alexa01",
                     headers=HEADERS, auth=AUTH, json=alexa)
    status = "✓" if r.status_code in (200, 201, 204) else f"✗ {r.text}"
    print(f"  Alexa [smarthome:alexa01]: {r.status_code} {status}")

def create_router():
    router = {
        "policyId": "smarthome:policy-router",
        "attributes": {
            "name": "Home Router",
            "type": "wifi-router",
            "location": "living_room",
            "manufacturer": "Generic",
            "model": "HomeRouter-01"
        },
        "features": {
            "network": {
                "properties": {
                    "ssid": "HomeNetwork",
                    "ip_address": "192.168.1.1",
                    "subnet_mask": "255.255.255.0",
                    "dns_primary": "8.8.8.8",
                    "dns_secondary": "8.8.4.4",
                    "wan_ip": "203.0.113.1",
                    "connection_type": "fiber"
                }
            },
            "wifi": {
                "properties": {
                    "is_enabled": True,
                    "frequency_band": "2.4GHz",
                    "channel": 6,
                    "signal_strength_dbm": -55,
                    "encryption": "WPA2"
                }
            },
            "connected_devices": {
                "properties": {
                    "count": 3,
                    "devices": ["bulb01", "alexa01", "ac01"]
                }
            },
            "firewall": {
                "properties": {
                    "is_enabled": True,
                    "blocked_ips": [],
                    "intrusion_detection": True
                }
            },
            "traffic": {
                "properties": {
                    "bytes_sent": 0,
                    "bytes_received": 0,
                    "bandwidth_mbps": 100,
                    "current_usage_percent": 10
                }
            },
            "status": {
                "properties": {
                    "is_online": True,
                    "uptime_seconds": 86400,
                    "last_reboot": "2026-01-01T00:00:00Z"
                }
            }
        }
    }
    r = requests.put(f"{BASE_URL}/things/smarthome:router01",
                     headers=HEADERS, auth=AUTH, json=router)
    status = "✓" if r.status_code in (200, 201, 204) else f"✗ {r.text}"
    print(f"  Router [smarthome:router01]: {r.status_code} {status}")

def verify_all():
    things = [
        "smarthome:bulb01",
        "smarthome:ac01",
        "smarthome:alexa01",
        "smarthome:router01"
    ]
    print("\n--- Verification ---")
    for thing_id in things:
        r = requests.get(f"{BASE_URL}/things/{thing_id}",
                         headers=HEADERS, auth=AUTH)
        if r.status_code == 200:
            print(f"  {thing_id} → OK ✓")
        else:
            print(f"  {thing_id} → FAILED ✗ ({r.status_code})")

if __name__ == "__main__":
    print("=" * 40)
    print("CREATING ALL SMART HOME DEVICES")
    print("=" * 40)

    print("\n--- Policies ---")
    create_policy("smarthome:policy-bulb")
    create_policy("smarthome:policy-ac")
    create_policy("smarthome:policy-alexa")
    create_policy("smarthome:policy-router")

    print("\n--- Devices ---")
    create_bulb()
    create_ac()
    create_alexa()
    create_router()

    verify_all()

    print("\n" + "=" * 40)
    print("ALL DEVICES READY")
    print("=" * 40)
    print("  smarthome:bulb01   - Smart Bulb")
    print("  smarthome:ac01     - Smart AC")
    print("  smarthome:alexa01  - Alexa Echo Dot")
    print("  smarthome:router01 - Home Router")
