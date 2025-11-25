import json
import os

# Define the Alien Cipher Mapping
# Mapping standard Latin characters to "Alien" Unicode characters
# Using a mix of Glagolitic, Coptic, and other obscure symbols to look "Klingon-esque"
CIPHER_MAP = {
    'a': '⍙', 'b': '⍝', 'c': '⍫', 'd': '⍮', 'e': '⍒', 'f': '⍂', 'g': '⍆', 'h': '⍊',
    'i': '⍘', 'j': '⍎', 'k': '⍖', 'l': '⍇', 'm': '⍈', 'n': '⍉', 'o': '⍛', 'p': '⍱',
    'q': '⍬', 'r': '⍇', 's': '⍕', 't': 'Tk', 'u': '⍶', 'v': '⍡', 'w': '⍢', 'x': '⍣',
    'y': '⍤', 'z': '⍥',
    'A': '⍙', 'B': '⍝', 'C': '⍫', 'D': '⍮', 'E': '⍒', 'F': '⍂', 'G': '⍆', 'H': '⍊',
    'I': '⍘', 'J': '⍎', 'K': '⍖', 'L': '⍇', 'M': '⍈', 'N': '⍉', 'O': '⍛', 'P': '⍱',
    'Q': '⍬', 'R': '⍇', 'S': '⍕', 'T': 'Tk', 'U': '⍶', 'V': '⍡', 'W': '⍢', 'X': '⍣',
    'Y': '⍤', 'Z': '⍥',
    ' ': ' ', '.': '⵰', ',': 'ⵯ', '!': 'ⵧ', '?': '⵨', '-': 'ⵤ',
    '0': '↊', '1': '↋', '2': '↌', '3': '↍', '4': '↎', '5': '↏', '6': '←', '7': '↑', '8': '→', '9': '↓'
}

# Improved mapping with more consistent "Alien" look (Glagolitic + Runes)
CIPHER_MAP = {
    'a': 'Ⰰ', 'b': 'Ⰱ', 'c': 'Ⱌ', 'd': 'Ⰴ', 'e': 'Ⰵ', 'f': 'Ⱉ', 'g': 'Ⰳ', 'h': 'Ⱒ',
    'i': 'Ⰻ', 'j': 'Ⰼ', 'k': 'Ⰽ', 'l': 'Ⰾ', 'm': 'Ⰿ', 'n': 'Ⱀ', 'o': 'Ⱁ', 'p': 'Ⱂ',
    'q': 'Ⱋ', 'r': 'Ⱃ', 's': 'Ⱄ', 't': 'Ⱅ', 'u': 'Ⱆ', 'v': 'Ⱇ', 'w': 'Ⱈ', 'x': 'Ⱎ',
    'y': 'Ⱏ', 'z': 'Ⱘ',
    'A': 'Ⰰ', 'B': 'Ⰱ', 'C': 'Ⱌ', 'D': 'Ⰴ', 'E': 'Ⰵ', 'F': 'Ⱉ', 'G': 'Ⰳ', 'H': 'Ⱒ',
    'I': 'Ⰻ', 'J': 'Ⰼ', 'K': 'Ⰽ', 'L': 'Ⰾ', 'M': 'Ⰿ', 'N': 'Ⱀ', 'O': 'Ⱁ', 'P': 'Ⱂ',
    'Q': 'Ⱋ', 'R': 'Ⱃ', 'S': 'Ⱄ', 'T': 'Ⱅ', 'U': 'Ⱆ', 'V': 'Ⱇ', 'W': 'Ⱈ', 'X': 'Ⱎ',
    'Y': 'Ⱏ', 'Z': 'Ⱘ',
    ' ': ' ', '.': '⵰', ',': 'ⵯ', '!': 'ⵧ', '?': '⵨', '-': 'ⵤ',
    '0': '↊', '1': '↋', '2': '↌', '3': '↍', '4': '↎', '5': '↏', '6': '←', '7': '↑', '8': '→', '9': '↓'
}

def to_alien(text):
    return "".join(CIPHER_MAP.get(c, c) for c in text)

def process_dict(data):
    new_data = {}
    for key, value in data.items():
        if isinstance(value, dict):
            new_data[key] = process_dict(value)
        elif isinstance(value, str):
            # Keep formatting placeholders like {name} intact
            parts = []
            last_pos = 0
            import re
            # Regex to find {placeholders}
            for match in re.finditer(r'\{[^}]+\}', value):
                # Translate text before placeholder
                parts.append(to_alien(value[last_pos:match.start()]))
                # Keep placeholder as is
                parts.append(match.group(0))
                last_pos = match.end()
            # Translate remaining text
            parts.append(to_alien(value[last_pos:]))
            new_data[key] = "".join(parts)
        else:
            new_data[key] = value
    return new_data

def main():
    base_path = "c:/Dev/Repos/JanFriske/MacGyver Multi-Tool/i18n/translations"
    en_path = os.path.join(base_path, "en.json")
    tlh_path = os.path.join(base_path, "tlh.json")

    with open(en_path, 'r', encoding='utf-8') as f:
        en_data = json.load(f)

    tlh_data = process_dict(en_data)

    # Overwrite specific keys to be more "Klingon" if needed, but the cipher does the job for the "unknown charset" look.
    # Maybe add a prefix to the window title?
    if "dialogs" in tlh_data and "about" in tlh_data["dialogs"]:
        tlh_data["dialogs"]["about"]["title"] = "tlhIngan wo' " + tlh_data["dialogs"]["about"]["title"]

    with open(tlh_path, 'w', encoding='utf-8') as f:
        json.dump(tlh_data, f, indent=4, ensure_ascii=False)
    
    print(f"Generated {tlh_path}")

if __name__ == "__main__":
    main()
