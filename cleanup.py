import requests
import time

BASE_URL = "http://localhost:8080/api/2"
HEADERS = {"Content-Type": "application/json"}
AUTH = ("ditto", "ditto")

THINGS = [
    "smarthome:bulb01",
    "smarthome:ac01",
    "smarthome:alexa01",
    "smarthome:router01"
]

POLICIES = [
    "smarthome:policy-bulb",
    "smarthome:policy-ac",
    "smarthome:policy-alexa",
    "smarthome:policy-router"
]

def delete_things():
    print("\n--- Deleting Things ---")
    for thing_id in THINGS:
        r = requests.delete(
            f"{BASE_URL}/things/{thing_id}",
            headers=HEADERS,
            auth=AUTH
        )
        if r.status_code in (200, 201, 204):
            print(f"  Deleted  [{thing_id}] ✓")
        elif r.status_code == 404:
            print(f"  Not found [{thing_id}] (skipped)")
        else:
            print(f"  Failed   [{thing_id}] {r.status_code} — {r.text}")

def delete_policies():
    print("\n--- Deleting Policies ---")
    for policy_id in POLICIES:
        r = requests.delete(
            f"{BASE_URL}/policies/{policy_id}",
            headers=HEADERS,
            auth=AUTH
        )
        if r.status_code in (200, 201, 204):
            print(f"  Deleted  [{policy_id}] ✓")
        elif r.status_code == 404:
            print(f"  Not found [{policy_id}] (skipped)")
        else:
            print(f"  Failed   [{policy_id}] {r.status_code} — {r.text}")

def verify_clean():
    print("\n--- Verifying Cleanup ---")
    all_clean = True
    for thing_id in THINGS:
        r = requests.get(
            f"{BASE_URL}/things/{thing_id}",
            headers=HEADERS,
            auth=AUTH
        )
        if r.status_code == 404:
            print(f"  Confirmed deleted [{thing_id}] ✓")
        else:
            print(f"  Still exists      [{thing_id}] ✗")
            all_clean = False

    for policy_id in POLICIES:
        r = requests.get(
            f"{BASE_URL}/policies/{policy_id}",
            headers=HEADERS,
            auth=AUTH
        )
        if r.status_code == 404:
            print(f"  Confirmed deleted [{policy_id}] ✓")
        else:
            print(f"  Still exists      [{policy_id}] ✗")
            all_clean = False

    return all_clean

if __name__ == "__main__":
    print("=" * 40)
    print("  CLEANUP — FRESH START")
    print("=" * 40)

    delete_things()
    time.sleep(1)
    delete_policies()
    time.sleep(1)

    all_clean = verify_clean()

    print("\n" + "=" * 40)
    if all_clean:
        print("  ALL CLEAN — Ready for fresh run ✓")
    else:
        print("  WARNING — Some items could not be deleted ✗")
    print("=" * 40)