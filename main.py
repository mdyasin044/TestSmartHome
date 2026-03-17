import subprocess
import sys
import os
import glob
from datetime import datetime

LOG_DIR = f"docker_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

# -----------------------------------------------
# HELPERS
# -----------------------------------------------

def run_script(script_name):
    print(f"\n>>> Running {script_name}...")
    print("-" * 40)
    result = subprocess.run(
        [sys.executable, script_name],
        capture_output=False
    )
    if result.returncode == 0:
        print(f">>> {script_name} completed ✓")
    else:
        print(f">>> {script_name} FAILED ✗")
    return result.returncode

def get_latest_dirs(prefix):
    dirs = sorted(glob.glob(f"{prefix}_*"), reverse=True)
    return dirs[0] if dirs else None

def run_compare(script_name, baseline_prefix, attack_prefix):
    baseline_dir = get_latest_dirs(baseline_prefix)
    attack_dir   = get_latest_dirs(attack_prefix)

    if not baseline_dir or not attack_dir:
        print(f"  Could not find dirs for {baseline_prefix} / {attack_prefix}")
        return

    print(f"\n>>> Comparing {baseline_dir} vs {attack_dir}")
    print("-" * 40)
    subprocess.run([sys.executable, script_name, baseline_dir, attack_dir])

def collect_docker_logs(label):
    os.makedirs(LOG_DIR, exist_ok=True)

    safe_label = label.replace("/", "_").replace("\\", "_")

    containers = [
        "docker-nginx-1",
        "docker-things-1",
        "docker-gateway-1",
        "docker-things-search-1",
        "docker-connectivity-1",
        "docker-swagger-ui-1",
        "docker-ditto-ui-1",
        "docker-mongodb-1",
        "docker-policies-1",
    ]

    COMPOSE_DIR = r"D:\LUCID\Docker\ditto\deployment\docker"

    print(f"\n[LOGS] Collecting Docker logs — {label}")

    # Per container logs
    for container in containers:
        filename = os.path.join(LOG_DIR, f"{safe_label}_{container}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            subprocess.run(
                ["docker", "logs", container],
                stdout=f,
                stderr=f
            )
        size = os.path.getsize(filename)
        print(f"  Saved: {filename} ({size} bytes)")

    # Combined log
    combined = os.path.join(LOG_DIR, f"{safe_label}_ALL.txt")
    with open(combined, "w", encoding="utf-8") as f:
        subprocess.run(
            ["docker", "compose", "logs", "--no-color"],
            stdout=f,
            stderr=f,
            cwd=COMPOSE_DIR
        )
    print(f"  Saved: {combined} ✓")

# -----------------------------------------------
# MAIN
# -----------------------------------------------

if __name__ == "__main__":
    print("=" * 50)
    print("  SMART HOME ATTACK SIMULATION — MAIN")
    print("=" * 50)

    # Collect logs BEFORE (baseline docker state)
    collect_docker_logs("01_before_setup")

    # STEP 1: Create devices
    print("\n[STEP 1] Creating all devices...")
    run_script("create_devices.py")
    collect_docker_logs("02_after_device_creation")

    # STEP 2: Run attacks
    print("\n[STEP 2] Running all attack simulations...")
    run_script("attack_bulb.py")
    collect_docker_logs("03_after_bulb_attacks")

    run_script("attack_ac.py")
    collect_docker_logs("04_after_ac_attacks")

    run_script("attack_alexa.py")
    collect_docker_logs("05_after_alexa_attacks")

    run_script("attack_router.py")
    collect_docker_logs("06_after_router_attacks")

    # STEP 3: Compare
    print("\n[STEP 3] Comparing baseline vs attack logs...")
    run_compare("compare_attacks.py", "all_attacks/bulb_baseline",   "all_attacks/bulb_attacks")
    run_compare("compare_attacks.py", "all_attacks/ac_baseline",     "all_attacks/ac_attacks")
    run_compare("compare_attacks.py", "all_attacks/alexa_baseline",  "all_attacks/alexa_attacks")
    run_compare("compare_attacks.py", "all_attacks/router_baseline", "all_attacks/router_attacks")

    # Final log collection
    collect_docker_logs("07_final")

    print("\n" + "=" * 50)
    print("  ALL DONE")
    print("=" * 50)
    print(f"\nDocker logs saved in: {LOG_DIR}/")
    print("Files collected:")
    for fname in sorted(os.listdir(LOG_DIR)):
        size = os.path.getsize(os.path.join(LOG_DIR, fname))
        print(f"  {fname} ({size} bytes)")
