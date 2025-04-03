import json
import re
from pathlib import Path
import spacy

nlp = spacy.load("en_core_web_sm")

# Input and output paths
input_path = Path("output.json")
output_path = Path("processed.json")

# Load original JSON
with input_path.open("r", encoding="utf-8") as f:
    raw_data = json.load(f)

# Map abbreviation to full part-of-speech
type_map = {
    "n.": "noun",
    "v.": "verb",
    "adj.": "adjective",
    "intrj.": "interjection",
    "adv.": "adverb",
    "prep.": "preposition",
    "conj.": "conjunction",
    "pl.": "plural",
    "pron.": "pronoun"
}

def extract_type_and_definition(entry):
    tagalog = entry["tagalog"].strip()
    raw = entry["english"].strip()

    # Remove the tagalog word from the start of the definition if it's duplicated
    if raw.lower().startswith(tagalog.lower()):
        raw = raw[len(tagalog):].strip()

    # Match the first known type abbreviation (e.g., adj., n., v., etc.)
    type_match = re.match(r'^([a-z]{1,6}\.)', raw)
    type_abbr = type_match.group(1) if type_match else None
    full_type = type_map.get(type_abbr, "unknown") if type_abbr else "unknown"

    # Remove type from definition
    definition = raw
    if type_abbr:
        definition = raw[len(type_abbr):].strip()

    # Clean punctuation from definition
    definition = definition.strip(" :;.")

    # Clean the tagalog word from embedded variations, like: abangan (inaabangan...)
    base_word = re.sub(r"\s*\(.+\)", "", tagalog)

    return {
        "tagalog": base_word,
        "type": full_type,
        "definition": definition,
        "raw_definition": entry["english"]
    }

# Process entries
processed = [extract_type_and_definition(entry) for entry in raw_data]

# Write to file
with output_path.open("w", encoding="utf-8") as f:
    json.dump(processed, f, ensure_ascii=False, indent=2)

print(f"Processed {len(processed)} entries → {output_path}")

