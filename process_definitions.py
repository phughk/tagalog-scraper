import json
import re
from pathlib import Path
import spacy

nlp = spacy.load("en_core_web_sm")

# Input and output paths
input_path = Path("output.json")
output_path = Path("processed.json")

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


def detect_type_with_spacy(def_text: str) -> str:
    doc = nlp(def_text)
    for token in doc:
        if token.pos_ in {"NOUN", "VERB", "ADJ", "ADV", "INTJ"}:
            return token.pos_.lower()
    return "unknown"

def extract_type_and_definition(entry):
    tagalog = entry["tagalog"].strip()
    raw = entry["english"].strip()

    # Remove variant info from tagalog (e.g., abain (inaaba, ...))
    base_word = re.sub(r"\s*\(.+\)", "", tagalog).strip()

    # Remove tagalog word at start of definition
    cleaned = re.sub(rf"^{re.escape(base_word)}[!?.,]?\s*", "", raw, flags=re.IGNORECASE)

    # Remove parenthetical inflections like (inaaba, inaba, ...)
    cleaned = re.sub(r"^\([^)]*\)\s*", "", cleaned)

    # Extract all tags like n., v., adj., etc.
    tag_matches = re.findall(r"\b([a-z]{1,10})\.", cleaned.lower())

    main_type = None
    context = None
    for tag in tag_matches:
        if f"{tag}." in type_map:
            main_type = type_map[f"{tag}."]
        elif f"{tag}." in context_map:
            context = context_map[f"{tag}."]

    # Remove all tag tokens (e.g., "v.,", "n.", "adj.,", etc.) and ", inf." or ", pl."
    cleaned = re.sub(r"^((\([^)]*\)\s*)?([a-z]{1,10}\.\s*,?\s*)+)", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"^,\s*(inf\.|pl\.|mat\.|comp\.)\s*", "", cleaned, flags=re.IGNORECASE)

    definition = cleaned.strip(" ,:;.")

    # Use spaCy to guess type if none found
    if not main_type:
        main_type = detect_type_with_spacy(definition)

    result = {
        "tagalog": base_word,
        "definition": definition,
        "raw_definition": raw,
        "type": main_type
    }

    if context:
        result["context"] = context

    return result

# Process entries
with input_path.open("r", encoding="utf-8") as f:
    raw_data = json.load(f)

processed = [extract_type_and_definition(entry) for entry in raw_data]

with output_path.open("w", encoding="utf-8") as f:
    json.dump(processed, f, ensure_ascii=False, indent=2)

print(f"Processed {len(processed)} entries → {output_path}")

