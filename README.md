# Minecraft Bedrock AI Attack Interval Fix (MCPE-231095)

A precision-engineered hotfix for the [**MCPE-231095**](https://bugs.mojang.com/browse/MCPE/issues/MCPE-231095) bug affecting Minecraft Bedrock Edition **1.21.130+**.

## 🛡️ The Issue (MCPE-231095)

Starting with version 1.21.130, many vanilla entities (notably **Wolves**, **Drowned**, and **Guardians**) began triggering massive console log spam. The error typically looks like this:
[Server] [Json] minecraft:wolf | ... | For entity wolf, "attack_interval" is disabled (max <= 0); goal will fall back to "scan_interval" (ticks).
This occurs because the engine now expects attack_interval to be a **Range Object** { "range_min": x, "range_max": y }, while vanilla files still contain integers or legacy underscore fields (\_min/\_max).

## ✨ Key Features

- **Fixes MCPE-231095**: Stops the INFO log spam that can bloat server log files to several GBs.
- **Full-Clone Safety**: Unlike standard "component-only" patches, this fix clones the **entire entity JSON**. This ensures that state-dependent logic (like Wolf anger/taming/variants) remains 100% intact.
- **Legacy Value Inheritance**: Automatically maps old attack_interval_min/max values to the new schema, preserving original game balance.
- **Minimal Impact**: No changes to entity behavior or loot tables; purely a schema-compliance patch.

## 🚀 Installation

1.  Download the latest .mcpack from the Releases page.
2.  Import it into your world or add it to your server's behavior_packs folder.
3.  **Important**: Place this pack at the top of your Behavior Pack stack to ensure it overrides the faulty vanilla definitions.
