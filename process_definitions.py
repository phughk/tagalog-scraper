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
    "pron.": "pronoun",
    "interrog.": "interrogative"
}

context_map = {
    "comp.": "computing",
    "math.": "mathematics",
    "mat.": "mathematics"
}

def extract_type_and_definition(entry):
    tagalog = entry["tagalog"].strip()
    raw = entry["english"].strip()
    base_word = re.sub(r"\s*\(.+\)", "", tagalog).strip()

    # Remove the tagalog word at the beginning, even with trailing punctuation
    cleaned = re.sub(rf"^{re.escape(base_word)}[!?.,]?\s*", "", raw, flags=re.IGNORECASE)

    # Remove parenthetical inflections
    cleaned = re.sub(r"^\([^)]*\)\s*", "", cleaned)

    # Remove prefix words not matching tagalog (like "sama", "ubos", etc.)
    # Only strip first word if it's not a tag
    maybe_first_word = cleaned.split(" ", 1)[0].lower()
    if maybe_first_word not in type_map and maybe_first_word not in context_map:
        cleaned = re.sub(rf"^{re.escape(maybe_first_word)}\s+", "", cleaned)


    # Extract all possible POS/type/context indicators
    all_tags = re.findall(r"\b([a-z]{2,10}\.)", cleaned.lower())

    # Try to find a main part of speech (noun, verb, adj, etc.)
    main_type = None
    context = None
    for tag in all_tags:
        if tag in type_map:
            main_type = type_map[tag]
            break
        elif tag in context_map:
            context = context_map[tag]

    # Remove the matched tag(s) from the start
    for tag in all_tags:
        cleaned = re.sub(rf"^{tag}\s*", "", cleaned, flags=re.IGNORECASE)

    # Final cleanup
    definition = cleaned.strip(" :;.")

    result = {
        "tagalog": base_word,
        "definition": definition,
        "raw_definition": entry["english"],
        "type": main_type or "unknown"
    }

    if context:
        result["context"] = context

    return result

# Process entries
processed = [extract_type_and_definition(entry) for entry in raw_data]

# Write to file
with output_path.open("w", encoding="utf-8") as f:
    json.dump(processed, f, ensure_ascii=False, indent=2)

print(f"Processed {len(processed)} entries → {output_path}")

