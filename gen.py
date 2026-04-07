"""This script was mainly written by Gemini"""

import os
import json
import re

# --- Configuration ---
VANILLA_PATH = "./behavior_packs/vanilla/entities"
OUTPUT_PATH = "./Fix_Attack_Interval/entities"

if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH, exist_ok=True)


def clean_json(text):
    """Clean comments and illegal commas from JSON to ensure robust parsing."""
    text = re.sub(r"//.*", "", text)
    text = re.sub(r"/\*[\s\S]*?\*/", "", text)
    text = re.sub(r",\s*([\]}])", r"\1", text)
    return text


def fix_ai_logic(comp_data):
    """
    Adapt only within the AI component:
    1. Extract old values.
    2. Wrap into a Range object (required by 1.21.130).
    3. Clean up old fields that cause errors.
    """
    new_data = comp_data.copy()

    # Extract values
    old_min = new_data.get("attack_interval_min")
    old_max = new_data.get("attack_interval_max")
    old_val = new_data.get("attack_interval")

    # Determine baseline value: use the number if specified in vanilla, otherwise default to 1.0
    fallback = old_val if isinstance(old_val, (int, float)) else 1.0
    fallback = old_val if isinstance(old_val, (int, float)) else 1.0

    final_min = float(old_min if old_min is not None else fallback)
    final_max = float(old_max if old_max is not None else fallback)

    # Format rewrite: Key step to satisfy 1.21.130 requirements
    new_data["attack_interval"] = {"range_min": final_min, "range_max": final_max}

    # Force cleanup: Remove old keys that cause 'child not valid here' errors
    for k in ["attack_interval_min", "attack_interval_max"]:
        if k in new_data:
            del new_data[k]

    return new_data


def run_safe_fix():
    print(
        "🚀 Starting safe fix procedure (keeping original version numbers, cloning all components)..."
    )
    count = 0
    target_key = "minecraft:behavior.nearest_attackable_target"

    for filename in os.listdir(VANILLA_PATH):
        if not filename.endswith(".json"):
            continue

        try:
            with open(os.path.join(VANILLA_PATH, filename), "r", encoding="utf-8") as f:
                raw = f.read()
                if raw.startswith("\ufeff"):
                    raw = raw[1:]
                data = json.loads(clean_json(raw))

            has_fix = False

            # We do not modify data["format_version"], keeping it as is (e.g., 1.13.0)
            entity_root = data.get("minecraft:entity", {})
            components = entity_root.get("components", {})
            groups = entity_root.get("component_groups", {})

            # 1. Scan base components
            if target_key in components:
                components[target_key] = fix_ai_logic(components[target_key])
                has_fix = True

            # 2. Scan component_groups (preserve all original components within groups)
            if groups:
                for group_name in groups:
                    group_content = groups[group_name]
                    if target_key in group_content:
                        group_content[target_key] = fix_ai_logic(
                            group_content[target_key]
                        )
                        has_fix = True

            if has_fix:
                with open(
                    os.path.join(OUTPUT_PATH, filename), "w", encoding="utf-8"
                ) as out_f:
                    # Write back fully; only the small part of the AI component is changed, rest remains untouched
                    json.dump(data, out_f, indent=2, ensure_ascii=False)
                count += 1
                print(f"Patched: {filename}")

        except Exception as e:
            print(f"❌ Parsing failed for {filename}: {e}")

    print(f"\n✨ Fix task completed! Generated {count} safe patches.")


if __name__ == "__main__":
    run_safe_fix()
