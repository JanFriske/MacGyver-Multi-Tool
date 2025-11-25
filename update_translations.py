#!/usr/bin/env python3
"""
Script to add missing translation keys to all translation files
"""
import json
from pathlib import Path

# New keys to add with their English translations
NEW_KEYS = {
    "menu.german_dialects": {
        "de": "Deutsch",
        "en": "German",
        "es": "Alemán",
        "fr": "Allemand",
        "it": "Tedesco",
        "nl": "Duits",
        "pt": "Alemão",
        "ru": "Немецкий",
        "yi": "דײַטש",
        "yi_latn": "Daitsh",
        "he": "גרמנית",
        "ar": "الألمانية",
        "ja": "ドイツ語",
        "cs": "Němčina",
        "hu": "Német",
        "pl": "Niemiecki",
        "sk": "Nemčina",
        "tr": "Almanca",
        "de_berlin": "Deutsch",
        "de_bavaria": "Deutsch",
        "de_eastprussia": "Deutsch",
        "de_hessian": "Deutsch",
        "de_lowgerman": "Deutsch",
        "de_saxony": "Deutsch",
        "de_swabian": "Deutsch",
        "de_transylvania": "Deutsch"
    },
    "widgets.directory_browser_title": {
        "de": "Dateiverwaltung",
        "en": "File Manager",
        "es": "Administrador de archivos",
        "fr": "Gestionnaire de fichiers",
        "it": "Gestore file",
        "nl": "Bestandsbeheer",
        "pt": "Gerenciador de arquivos",
        "ru": "Файловый менеджер",
        "yi": "טעקע־פֿאַרוואַלטונג",
        "yi_latn": "Tek farmaltung",
        "he": "מנהל קבצים",
        "ar": "مدير الملفات",
        "ja": "ファイルマネージャー",
        "cs": "Správce souborů",
        "hu": "Fájlkezelő",
        "pl": "Menedżer plików",
        "sk": "Správca súborov",
        "tr": "Dosya Yöneticisi"
    },
    "widgets.quick_access_title": {
        "de": "Schnellzugriff",
        "en": "Quick Access",
        "es": "Acceso rápido",
        "fr": "Accès rapide",
        "it": "Accesso rapido",
        "nl": "Snelle toegang",
        "pt": "Acesso rápido",
        "ru": "Быстрый доступ",
        "yi": "גיכער צוטריט",
        "yi_latn": "Gikher tsutrit",
        "he": "גישה מהירה",
        "ar": "وصول سريع",
        "ja": "クイックアクセス",
        "cs": "Rychlý přístup",
        "hu": "Gyors hozzáférés",
        "pl": "Szybki dostęp",
        "sk": "Rýchly prístup",
        "tr": "Hızlı Erişim"
    },
    "widgets.file_stats_title": {
        "de": "Statistik",
        "en": "Statistics",
        "es": "Estadísticas",
        "fr": "Statistiques",
        "it": "Statistiche",
        "nl": "Statistieken",
        "pt": "Estatísticas",
        "ru": "Статистика",
        "yi": "סטאַטיסטיק",
        "yi_latn": "Statistik",
        "he": "סטטיסטיקה",
        "ar": "إحصائيات",
        "ja": "統計",
        "cs": "Statistiky",
        "hu": "Statisztikák",
        "pl": "Statystyki",
        "sk": "Štatistiky",
        "tr": "İstatistikler"
    },
    "widgets.file_stats_storage": {
        "de": "Speicher",
        "en": "Storage",
        "es": "Almacenamiento",
        "fr": "Stockage",
        "it": "Archiviazione",
        "nl": "Opslag",
        "pt": "Armazenamento",
        "ru": "Хранилище",
        "yi": "שפּײַכער",
        "yi_latn": "Shpaycher",
        "he": "אחסון",
        "ar": "تخزين",
        "ja": "ストレージ",
        "cs": "Úložiště",
        "hu": "Tárhely",
        "pl": "Przechowywanie",
        "sk": "Úložisko",
        "tr": "Depolama"
    },
    "widgets.recent_files_title": {
        "de": "Zuletzt verwendet",
        "en": "Recent Files",
        "es": "Archivos recientes",
        "fr": "Fichiers récents",
        "it": "File recenti",
        "nl": "Recente bestanden",
        "pt": "Arquivos recentes",
        "ru": "Недавние файлы",
        "yi": "לעצטע טעקעס",
        "yi_latn": "Letste tekes",
        "he": "קבצים אחרונים",
        "ar": "الملفات الأخيرة",
        "ja": "最近使用したファイル",
        "cs": "Poslední soubory",
        "hu": "Legutóbbi fájlok",
        "pl": "Ostatnie pliki",
        "sk": "Posledné súbory",
        "tr": "Son Dosyalar"
    },
    "file_manager.up_button": {
        "de": "⬆️ Hoch",
        "en": "⬆️ Up",
        "es": "⬆️ Arriba",
        "fr": "⬆️ Haut",
        "it": "⬆️ Su",
        "nl": "⬆️ Omhoog",
        "pt": "⬆️ Acima",
        "ru": "⬆️ Вверх",
        "yi": "⬆️ אַרויף",
        "yi_latn": "⬆️ AFreiden",
        "he": "⬆️ מעלה",
        "ar": "⬆️ أعلى",
        "ja": "⬆️ 上へ",
        "cs": "⬆️ Nahoru",
        "hu": "⬆️ Fel",
        "pl": "⬆️ Góra",
        "sk": "⬆️ Hore",
        "tr": "⬆️ Yukarı"
    },
    "media.open_button": {
        "de": "Öffnen",
        "en": "Open",
        "es": "Abrir",
        "fr": "Ouvrir",
        "it": "Apri",
        "nl": "Openen",
        "pt": "Abrir",
        "ru": "Открыть",
        "yi": "עפֿענען",
        "yi_latn": "Efenen",
        "he": "פתח",
        "ar": "فتح",
        "ja": "開く",
        "cs": "Otevřít",
        "hu": "Megnyitás",
        "pl": "Otwórz",
        "sk": "Otvoriť",
        "tr": "Aç"
    },
    "media.equalizer_preset_label": {
        "de": "Voreinstellung:",
        "en": "Preset:",
        "es": "Preajuste:",
        "fr": "Préréglage:",
        "it": "Preset:",
        "nl": "Voorinstelling:",
        "pt": "Predefinição:",
        "ru": "Пресет:",
        "yi": "פֿאָרײַנשטעלונג:",
        "yi_latn": "Foraynshteling:",
        "he": "קביעה מראש:",
        "ar": "الإعداد المسبق:",
        "ja": "プリセット:",
        "cs": "Předvolba:",
        "hu": "Előbeállítás:",
        "pl": "Ustawienie wstępne:",
        "sk": "Predvoľba:",
        "tr": "Önayar:"
    }
}

# Equalizer presets translations
EQUALIZER_PRESETS = {
    "media.equalizer_presets.flat": {
        "de": "Flach",
        "en": "Flat",
        "es": "Plano",
        "fr": "Plat",
        "it": "Piatto",
        "nl": "Vlak",
        "pt": "Plano",
        "ru": "Плоский",
        "yi": "פֿלאַך",
        "yi_latn": "Flach",
        "he": "שטוח",
        "ar": "مسطح",
        "ja": "フラット",
        "cs": "Ploché",
        "hu": "Sík",
        "pl": "Płaski",
        "sk": "Ploché",
        "tr": "Düz"
    },
    "media.equalizer_presets.rock": {
        "de": "Rock",
        "en": "Rock",
        "es": "Rock",
        "fr": "Rock",
        "it": "Rock",
        "nl": "Rock",
        "pt": "Rock",
        "ru": "Рок",
        "yi": "ראָק",
        "yi_latn": "Rok",
        "he": "רוק",
        "ar": "روك",
        "ja": "ロック",
        "cs": "Rock",
        "hu": "Rock",
        "pl": "Rock",
        "sk": "Rock",
        "tr": "Rock"
    },
    "media.equalizer_presets.pop": {
        "de": "Pop",
        "en": "Pop",
        "es": "Pop",
        "fr": "Pop",
        "it": "Pop",
        "nl": "Pop",
        "pt": "Pop",
        "ru": "Поп",
        "yi": "פּאָפּ",
        "yi_latn": "Pop",
        "he": "פופ",
        "ar": "بوب",
        "ja": "ポップ",
        "cs": "Pop",
        "hu": "Pop",
        "pl": "Pop",
        "sk": "Pop",
        "tr": "Pop"
    },
    "media.equalizer_presets.jazz": {
        "de": "Jazz",
        "en": "Jazz",
        "es": "Jazz",
        "fr": "Jazz",
        "it": "Jazz",
        "nl": "Jazz",
        "pt": "Jazz",
        "ru": "Джаз",
        "yi": "דזשאַז",
        "yi_latn": "Dzhaz",
        "he": "ג'אז",
        "ar": "جاز",
        "ja": "ジャズ",
        "cs": "Jazz",
        "hu": "Jazz",
        "pl": "Jazz",
        "sk": "Jazz",
        "tr": "Caz"
    },
    "media.equalizer_presets.classical": {
        "de": "Klassisch",
        "en": "Classical",
        "es": "Clásica",
        "fr": "Classique",
        "it": "Classica",
        "nl": "Klassiek",
        "pt": "Clássica",
        "ru": "Классика",
        "yi": "קלאַסיש",
        "yi_latn": "Klasish",
        "he": "קלאסי",
        "ar": "كلاسيكي",
        "ja": "クラシック",
        "cs": "Klasická",
        "hu": "Klasszikus",
        "pl": "Klasyczna",
        "sk": "Klasická",
        "tr": "Klasik"
    },
    "media.equalizer_presets.bass_boost": {
        "de": "Bass Verstärkung",
        "en": "Bass Boost",
        "es": "Refuerzo de graves",
        "fr": "Renforcement des basses",
        "it": "Potenziamento bassi",
        "nl": "Basversterking",
        "pt": "Reforço de graves",
        "ru": "Усиление басов",
        "yi": "באַס פֿאַרשטאַרקונג",
        "yi_latn": "Bas farshtarkung",
        "he": "חיזוק בס",
        "ar": "تعزيز الجهير",
        "ja": "低音ブースト",
        "cs": "Zvýraznění basů",
        "hu": "Basszus erősítés",
        "pl": "Wzmocnienie basów",
        "sk": "Zvýraznenie basov",
        "tr": "Bas Güçlendirme"
    }
}

# Combine all new keys
ALL_NEW_KEYS = {**NEW_KEYS, **EQUALIZER_PRESETS}

def add_nested_key(data, key_path, value):
    """Add a nested key to dictionary"""
    keys = key_path.split('.')
    current = data
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    current[keys[-1]] = value

def update_translation_file(filepath):
    """Update a single translation file"""
    lang_code = filepath.stem
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Add missing keys
        changes_made = False
        for key_path, translations in ALL_NEW_KEYS.items():
            if lang_code in translations:
                # Check if key exists
                keys = key_path.split('.')
                current = data
                exists = True
                for k in keys:
                    if isinstance(current, dict) and k in current:
                        current = current[k]
                    else:
                        exists = False
                        break
                
                if not exists:
                    add_nested_key(data, key_path, translations[lang_code])
                    changes_made = True
                    print(f"  Added {key_path} = {translations[lang_code]}")
        
        if changes_made:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"✅ Updated {filepath.name}")
        else:
            print(f"⏭️  {filepath.name} already has all keys")
            
    except Exception as e:
        print(f"❌ Error updating {filepath.name}: {e}")

def main():
    translations_dir = Path(__file__).parent / "i18n" / "translations"
    
    if not translations_dir.exists():
        print(f"Error: {translations_dir} not found")
        return
    
    print("Starting translation update...")
    print(f"Found {len(ALL_NEW_KEYS)} new keys to add")
    print()
    
    for json_file in sorted(translations_dir.glob("*.json")):
        if json_file.suffix == ".json" and not json_file.stem.endswith("corrupted"):
            print(f"\nProcessing {json_file.name}:")
            update_translation_file(json_file)
    
    print("\n✅ All translation files updated!")

if __name__ == "__main__":
    main()
