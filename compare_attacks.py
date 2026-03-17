import json
import os
import sys

def compare(baseline, attacked):
    changes = []
    b_features = baseline.get("features", {})
    a_features = attacked.get("features", {})
    for feature, data in a_features.items():
        b_props = b_features.get(feature, {}).get("properties", {})
        a_props = data.get("properties", {})
        for prop, val in a_props.items():
            if b_props.get(prop) != val:
                changes.append({
                    "feature": feature,
                    "property": prop,
                    "before": b_props.get(prop),
                    "after": val
                })
    return changes

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python compare_attacks.py <baseline_dir> <attack_dir>")
        exit(1)

    baseline_dir = sys.argv[1]
    attack_dir = sys.argv[2]

    baseline_files = os.listdir(baseline_dir)
    if not baseline_files:
        print("No baseline files found.")
        exit(1)

    with open(os.path.join(baseline_dir, baseline_files[0])) as f:
        baseline = json.load(f)

    print("\n" + "=" * 45)
    print("ATTACK COMPARISON REPORT")
    print("=" * 45)

    for filename in sorted(os.listdir(attack_dir)):
        filepath = os.path.join(attack_dir, filename)
        with open(filepath) as f:
            attacked = json.load(f)

        print(f"\nAttack : {filename}")
        changes = compare(baseline, attacked)

        if changes:
            for c in changes:
                print(f"  CHANGED  {c['feature']}.{c['property']}:")
                print(f"           {c['before']} → {c['after']}")
        else:
            print("  No changes detected")

    print("\n" + "=" * 45)
    print("END OF REPORT")
    print("=" * 45)
