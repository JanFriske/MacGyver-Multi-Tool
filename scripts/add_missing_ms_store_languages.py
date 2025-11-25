"""
Add Missing Microsoft Store Languages
Erstellt Platzhalter-JSON-Dateien für alle fehlenden Microsoft Store Sprachen
"""
import json
import sys
from pathlib import Path
from typing import Dict, List, Set

def load_microsoft_store_languages() -> Dict:
    """Lädt die Microsoft Store Sprachenliste."""
    ms_file = Path(__file__).parent.parent / "docs" / "microsoft_store_languages.json"
    with open(ms_file, "r", encoding="utf-8") as f:
        return json.load(f)

def get_existing_languages() -> Set[str]:
    """Ermittelt alle bereits vorhandenen Sprach-Dateien."""
    translations_dir = Path(__file__).parent.parent / "i18n" / "translations"
    existing = set()
    
    for file in translations_dir.glob("*.json"):
        if file.stem.endswith('.corrupted'):
            continue
        # Normalisiere den Code (entferne Unterstrich-Varianten)
        code = file.stem
        existing.add(code)
    
    return existing

def load_template() -> Dict:
    """Lädt die Vorlage für neue Sprachdateien (basierend auf en.json)."""
    template_file = Path(__file__).parent.parent / "i18n" / "translations" / "en.json"
    with open(template_file, "r", encoding="utf-8") as f:
        return json.load(f)

def create_placeholder_file(code: str, name: str, native_name: str, template: Dict):
    """Erstellt eine Platzhalter-Sprachdatei."""
    output_dir = Path(__file__).parent.parent / "i18n" / "translations"
    output_file = output_dir / f"{code}.json"
    
    # Verwende englische Vorlage als Basis
    placeholder_data = template.copy()
    
    # Schreibe die Datei
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(placeholder_data, f, ensure_ascii=False, indent=4)
    
    return output_file

def map_ms_code_to_macgyver_code(ms_code: str) -> str:
    """
    Mapped Microsoft Store BCP-47 Codes zu MacGyver Codes.
    Z.B.: zh-Hans -> zh, en-GB -> en_GB
    """
    # Spezielle Mappings
    mappings = {
        'zh-Hans': 'zh',
        'zh-Hant': 'zh',  # Wir nutzen bereits zh für vereinfacht
        'en-GB': 'en_GB',
        'fr-CA': 'fr_CA',
        'pt-BR': 'pt_BR',
        'pt-PT': 'pt_PT',
        'es-MX': 'es_MX',
        'sr-Cyrl': 'sr_Cyrl',
        'sr-Latn': 'sr_Latn',
        'ca-ES-valencia': 'ca_ES_valencia',
        'az': 'az_Latn',  # Aserbaidschanisch Lateinisch
        'bs': 'bs_Latn',  # Bosnisch Lateinisch
        'ha': 'ha_Latn',  # Hausa Lateinisch
        'ku': 'ku_Arab',  # Kurdisch Arabisch
        'mn': 'mn_Cyrl',  # Mongolisch Kyrillisch
        'sd': 'sd_Arab',  # Sindhi Arabisch
        'tg': 'tg_Cyrl',  # Tadschikisch Kyrillisch
        'uz': 'uz_Latn',  # Usbekisch Lateinisch
    }
    
    if ms_code in mappings:
        return mappings[ms_code]
    
    # Standard: Verwende den Code direkt
    return ms_code

def normalize_code_for_comparison(code: str) -> str:
    """Normalisiert Codes für Vergleich (entfernt Unterstriche/Bindestriche)."""
    return code.replace('_', '').replace('-', '').lower()

def main():
    print("=" * 80)
    print("MICROSOFT STORE SPRACHEN HINZUFÜGEN")
    print("=" * 80)
    print()
    
    # Lade Daten
    ms_data = load_microsoft_store_languages()
    existing = get_existing_languages()
    template = load_template()
    
    # Normalisiere existierende Codes für Vergleich
    existing_normalized = {normalize_code_for_comparison(code): code for code in existing}
    
    print(f"📊 Gefunden:")
    print(f"  Microsoft Store Sprachen: {len(ms_data['languages'])}")
    print(f"  Bereits vorhanden:        {len(existing)}")
    print()
    
    # Finde fehlende Sprachen
    missing = []
    for lang in ms_data['languages']:
        ms_code = lang['code']
        macgyver_code = map_ms_code_to_macgyver_code(ms_code)
        normalized = normalize_code_for_comparison(macgyver_code)
        
        if normalized not in existing_normalized:
            missing.append({
                'ms_code': ms_code,
                'macgyver_code': macgyver_code,
                'name': lang['name'],
                'native_name': lang['native_name']
            })
    
    if not missing:
        print("✅ Alle Microsoft Store Sprachen sind bereits vorhanden!")
        return
    
    print(f"⚠️  Fehlende Sprachen: {len(missing)}")
    print()
    
    # Frage nach Bestätigung
    print("Die folgenden Sprachen werden als Platzhalter hinzugefügt:")
    print()
    for i, lang in enumerate(missing, 1):
        print(f"  {i:3d}. {lang['macgyver_code']:15s} - {lang['name']:30s} ({lang['native_name']})")
    
    print()
    response = input("Fortfahren? (j/n): ")
    if response.lower() not in ['j', 'ja', 'y', 'yes']:
        print("❌ Abgebrochen.")
        return
    
    print()
    print("🚀 Erstelle Platzhalter-Dateien...")
    print()
    
    # Erstelle Platzhalter-Dateien
    created = []
    for lang in missing:
        try:
            output_file = create_placeholder_file(
                lang['macgyver_code'],
                lang['name'],
                lang['native_name'],
                template
            )
            created.append(lang['macgyver_code'])
            print(f"  ✅ {output_file.name}")
        except Exception as e:
            print(f"  ❌ Fehler bei {lang['macgyver_code']}: {e}")
    
    print()
    print("=" * 80)
    print("ZUSAMMENFASSUNG")
    print("=" * 80)
    print(f"✅ {len(created)} neue Sprachdateien erstellt")
    print(f"📁 Speicherort: i18n/translations/")
    print()
    print("NÄCHSTE SCHRITTE:")
    print("1. Erweitere LANGUAGE_GROUPS in core/services/i18n_service.py")
    print("2. Teste UI: Sprachwechsel für neue Sprachen")
    print("3. Führe scripts/compare_language_coverage.py aus")
    print()

if __name__ == "__main__":
    main()
