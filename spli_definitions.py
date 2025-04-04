import json
import re
from pathlib import Path

# Paths
input_path = Path("processed.json")   # Your cleaned entries from earlier
output_path = Path("split_definitions.json")

def split_definitions(entry):
    raw = entry["definition"]

    # Try to split on "1.", "2.", etc.
    numbered_parts = re.split(r"\b\d+\.\s*", raw)
    numbered_parts = [p.strip() for p in numbered_parts if p.strip()]

    if len(numbered_parts) > 1:
        # We successfully split by numbers, so treat each as its own group
        definition_groups = [re.split(r";\s*", part) for part in numbered_parts]
    else:
        # No numbering — just split on semicolons
        definition_groups = [re.split(r";\s*", raw.strip())]

    # Clean up whitespace
    definition_groups = [
        [defn.strip() for defn in group if defn.strip()]
        for group in definition_groups
    ]

    # Return updated entry
    new_entry = dict(entry)  # Copy original
    new_entry["definitions"] = definition_groups
    del new_entry["definition"]  # Remove flat string

    return new_entry

# Process file
with input_path.open("r", encoding="utf-8") as f:
    data = json.load(f)

split_data = [split_definitions(entry) for entry in data]

# Write to output
with output_path.open("w", encoding="utf-8") as f:
    json.dump(split_data, f, ensure_ascii=False, indent=2)

print(f"Split {len(split_data)} entries into grouped definitions → {output_path}")

