"""
Language Coverage Comparison Tool
Vergleicht MacGyver Multi-Tool Sprachen mit Microsoft Store unterstützten Sprachen
"""
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple

def load_microsoft_store_languages() -> Dict:
    """Lädt die Microsoft Store Sprachenliste."""
    ms_file = Path(__file__).parent.parent / "docs" / "microsoft_store_languages.json"
    with open(ms_file, "r", encoding="utf-8") as f:
        return json.load(f)

def get_macgyver_languages() -> Dict[str, str]:
    """Extrahiert alle in MacGyver Multi-Tool definierten Sprachen."""
    # Importiere I18nService
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from core.services.i18n_service import I18nService
    
    service = I18nService()
    all_codes = service.get_all_language_codes()
    
    # Extrahiere Namen
    languages = {}
    for code in all_codes:
        name = service.get_language_name(code)
        languages[code] = name
    
    return languages

def normalize_language_code(code: str) -> str:
    """Normalisiert Sprachcodes für Vergleich."""
    # Entferne Regionalangaben für Basis-Vergleich
    base_code = code.split('-')[0].split('_')[0].lower()
    return base_code

def compare_languages() -> Tuple[Set[str], Set[str], Set[str]]:
    """Vergleicht MacGyver Sprachen mit Microsoft Store Sprachen."""
    ms_data = load_microsoft_store_languages()
    macgyver_langs = get_macgyver_languages()
    
    # Erstelle Sets von Basis-Sprachcodes
    ms_codes = {normalize_language_code(lang['code']) for lang in ms_data['languages']}
    mg_codes = {normalize_language_code(code) for code in macgyver_langs.keys()}
    
    # Berechne Unterschiede
    in_both = ms_codes & mg_codes
    only_ms = ms_codes - mg_codes
    only_mg = mg_codes - ms_codes
    
    return in_both, only_ms, only_mg

def generate_report():
    """Generiert einen detaillierten Vergleichsbericht."""
    print("=" * 80)
    print("SPRACHVERGLEICH: MacGyver Multi-Tool vs. Microsoft Store")
    print("=" * 80)
    print()
    
    ms_data = load_microsoft_store_languages()
    macgyver_langs = get_macgyver_languages()
    in_both, only_ms, only_mg = compare_languages()
    
    print(f"📊 STATISTIK")
    print(f"  Microsoft Store Sprachen:    {len(ms_data['languages'])}")
    print(f"  MacGyver Multi-Tool Sprachen: {len(macgyver_langs)}")
    print(f"  Gemeinsame Sprachen:          {len(in_both)}")
    print(f"  Nur im Microsoft Store:       {len(only_ms)}")
    print(f"  Nur in MacGyver:              {len(only_mg)}")
    print()
    
    coverage = (len(in_both) / len(ms_data['languages'])) * 100
    print(f"✅ ABDECKUNG: {coverage:.1f}% der Microsoft Store Sprachen")
    print()
    
    # Details: Nur im Microsoft Store
    if only_ms:
        print("⚠️  FEHLENDE SPRACHEN (im Microsoft Store, aber nicht in MacGyver):")
        ms_lookup = {normalize_language_code(l['code']): l for l in ms_data['languages']}
        sorted_missing = sorted(only_ms)
        for i, code in enumerate(sorted_missing, 1):
            lang = ms_lookup.get(code, {})
            name = lang.get('name', code)
            native = lang.get('native_name', '')
            print(f"  {i:3d}. {code:6s} - {name:30s} ({native})")
        print()
    
    # Details: Nur in MacGyver (z.B. deutsche Dialekte)
    if only_mg:
        print("ℹ️  ZUSÄTZLICHE SPRACHEN (in MacGyver, aber nicht im MS Store):")
        mg_sorted = sorted(only_mg)
        for i, code in enumerate(mg_sorted, 1):
            # Finde originalen Code
            orig_code = next((k for k in macgyver_langs.keys() if normalize_language_code(k) == code), code)
            name = macgyver_langs.get(orig_code, code)
            print(f"  {i:3d}. {code:6s} - {name}")
        print()
    
    # Gemeinsame Sprachen
    print(f"✓  GEMEINSAME SPRACHEN ({len(in_both)}):")
    common_sorted = sorted(in_both)
    for i, code in enumerate(common_sorted, 1):
        print(f"  {i:3d}. {code}", end="")
        if (i % 10) == 0:
            print()
    if len(common_sorted) % 10 != 0:
        print()
    print()
    
    print("=" * 80)
    print("EMPFEHLUNG:")
    print("=" * 80)
    if coverage < 90:
        print("⚡ Niedrige Abdeckung! Erwäge, fehlende Sprachen hinzuzufügen.")
    elif coverage < 100:
        print("👍 Gute Abdeckung! Einige Sprachen fehlen noch.")
    else:
        print("🎉 Perfekt! Alle Microsoft Store Sprachen werden unterstützt!")
    print()

if __name__ == "__main__":
    generate_report()
