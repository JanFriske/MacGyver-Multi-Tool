"""
Script to rebuild i18n_service.py with 7-category structure
"""

content = '''"""
i18n Service - Central translation management
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Import user override service
from core.services.user_override_service import get_override_service


class I18nService:
    """Central service for internationalization."""

    # ========================================
    # 7 HAUPTKATEGORIEN - HIERARCHISCHE SPRACHGRUPPEN (200+ Varianten)
    # Struktur: Kategorie -> Sprache -> Dialekte/Varianten
    # ========================================
    LANGUAGE_GROUPS = {
        # ================================================
        # 1️⃣ GERMANISCHE SPRACHEN
        # ================================================
        "1️⃣ Germanische Sprachen": {
            "🇩🇪 Deutsch": {
                "Standard": {
                    "de": "🇩🇪 Deutsch",
                    "de_at": "🇦🇹 Österreichisch",
                    "de_ch": "🇨🇭 Schweizerdeutsch",
                },
                "Norddeutsch": {
                    "de_lowgerman": "Plattdeutsch",
                    "de_mecklenburg": "Mecklenburger Platt",
                    "de_holstein": "Holsteiner Platt",
                    "de_pomeranian": "Pommersch 🔴",
                },
                "Mitteldeutsch": {
                    "de_silesian": "Schlesisch 💀",
                    "de_silesian_lower": "Niederschlesisch",
                    "de_silesian_upper": "Oberschlesisch",
                    "de_sudeten": "Sudetendeutsch 💀",
                    "de_eastprussia_lithuanian": "Ostpreußisch-Litauisch",
                    "de_uppersaxon": "Obersächsisch",
                },
                "Westdeutsch": {
                    "de_westphalian": "Westfälisch",
                    "de_ripuarian": "Ripuarisch",
                    "de_cologne": "Kölsch 🎭",
                    "de_moselfranken": "Moselfränkisch",
                    "de_rhine": "Rheinisch",
                    "de_ruhr": "Ruhrdeutsch",
                },
                "Süddeutsch": {
                    "de_bavaria": "Bairisch",
                    "de_swabian": "Schwäbisch",
                    "de_alemannic": "Alemannisch",
                    "de_baden": "Badisch",
                    "de_allgaeu": "Allgäuerisch",
                    "de_palatinate": "Pfälzisch",
                    "de_frankfurt": "Frankfurterisch 🍎",
                },
                "Städtisch": {
                    "de_berlin": "Berlinerisch",
                },
                "Österreich": {
                    "de_AT_carinthia": "🇦🇹 Kärntnerisch",
                    "de_AT_vienna": "🇦🇹 Wienerisch",
                    "de_AT_styria": "🇦🇹 Steirisch",
                    "de_AT_tyrol": "🇦🇹 Tirolerisch",
                },
                "Schweiz": {
                    "de_CH_zurich": "🇨🇭 Zürichdeutsch",
                    "de_CH_bern": "🇨🇭 Berndeutsch",
                    "de_CH_basel": "🇨🇭 Baseldeutsch",
                },
                "Grenzregionen": {
                    "de_southtyrol": "🇮🇹 Südtirolerisch",
                    "de_vorarlberg": "🇦🇹🇨🇭 Vorarlbergisch",
                    "de_FR_alsace": "🇫🇷 Elsässisch",
                    "de_luxembourg": "🇱🇺 Luxemburgisch",
                },
                "Historische Diaspora": {
                    "de_volga": "Wolgadeutsch 🔴",
                    "de_banat": "Banat-Schwäbisch",
                    "de_sathmar": "Sathmarisch 💀",
                    "de_transylvania": "Siebenbürgisch-Sächsisch",
                },
            },
            "🇬🇧 English": {
                "Standard": {
                    "en": "🇬🇧 English",
                    "en_GB": "🇬🇧 English (UK)",
                },
                "🏴‍☠️ Pirate": {
                    "en_pirate": "🏴‍☠️ Pirate English",
                },
            },
            "🇳🇱 Nederlands": {
                "Standard": {
                    "nl": "🇳🇱 Nederlands",
                    "fy": "🇳🇱 Friesisch",
                    "li": "🇳🇱 Limburgisch",
                },
                "🏴‍☠️ Pirate": {
                    "nl_pirate": "🏴‍☠️ Nederlands Pirate",
                },
            },
            "🇩🇰 Dansk": {
                "Standard": {
                    "da": "🇩🇰 Dansk",
                },
            },
            "🇸🇪 Svenska": {
                "Standard": {
                    "sv": "🇸🇪 Svenska",
                },
            },
            "🇳🇴 Norsk": {
                "Standard": {
                    "nb": "🇳🇴 Norsk (Bokmål)",
                    "nn": "🇳🇴 Nynorsk",
                },
            },
            "🇮🇸 Íslenska": {
                "Standard": {
                    "is": "🇮🇸 Íslenska",
                },
            },
            "🇫🇮 Suomi": {
                "Standard": {
                    "fi": "🇫🇮 Suomi",
                },
            },
            "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scots": {
                "Standard": {
                    "sco": "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scots",
                },
                "🏴‍☠️ Pirate": {
                    "sco_pirate": "🏴‍☠️ Scots Pirate",
                },
            },
        },
        # ================================================
        # 2️⃣ ROMANISCHE SPRACHEN
        # ================================================
        "2️⃣ Romanische Sprachen": {
            "🇫🇷 Français": {
                "Standard": {
                    "fr": "🇫🇷 Français",
                    "fr_CA": "🇨🇦 Français (Canada)",
                },
                "Regional": {
                    "br": "🇫🇷 Bretonisch",
                    "co": "🇫🇷 Korsisch",
                    "oc": "🇫🇷 Okzitanisch",
                },
                "🏴‍☠️ Pirate": {
                    "fr_pirate": "🏴‍☠️ Français Pirate",
                    "fr_CA_pirate": "🏴‍☠️ Québécois Pirate",
                },
            },
            "🇪🇸 Español": {
                "Standard": {
                    "es": "🇪🇸 Español",
                    "es_MX": "🇲🇽 Español (México)",
                },
                "Dialekte": {
                    "es_andalucia": "🇪🇸 Andalusisch",
                },
                "🏴‍☠️ Pirate": {
                    "es_pirate": "🏴‍☠️ Español Pirate",
                },
            },
            "🇵🇹 Português": {
                "Standard": {
                    "pt": "🇵🇹 Português",
                    "pt_PT": "🇵🇹 Português (Portugal)",
                    "pt_BR": "🇧🇷 Português (Brasil)",
                },
                "🏴‍☠️ Pirate": {
                    "pt_pirate": "🏴‍☠️ Português Pirate",
                },
            },
            "🇮🇹 Italiano": {
                "Standard": {
                    "it": "🇮🇹 Italiano",
                    "vec": "🇮🇹 Venetian",
                },
                "🏴‍☠️ Pirate": {
                    "it_pirate": "🏴‍☠️ Italiano Pirate",
                },
            },
            "🇷🇴 Română": {
                "Standard": {
                    "ro": "🇷🇴 Română",
                },
            },
            "🇪🇸 Català": {
                "Standard": {
                    "ca": "🇪🇸 Català",
                    "ca_ES_valencia": "🇪🇸 Valencià",
                },
            },
            "🇪🇸 Galego": {
                "Standard": {
                    "gl": "🇪🇸 Galego",
                },
            },
        },
        # ================================================
        # 3️⃣ SLAWISCHE & OSTEUROPÄISCHE SPRACHEN
        # ================================================
        "3️⃣ Slawische & Osteuropäische Sprachen": {
            "🇷🇺 Русский": {
                "Standard": {
                    "ru": "🇷🇺 Русский",
                },
                "🏴‍☠️ Pirate": {
                    "ru_pirate": "🏴‍☠️ Russian Pirate",
                },
            },
            "🇵🇱 Polski": {
                "Standard": {
                    "pl": "🇵🇱 Polski",
                },
                "Dialekte": {
                    "csb": "🇵🇱 Kashubisch",
                    "szl": "🇵🇱 Schlesisch (Polnisch)",
                },
                "🏴‍☠️ Pirate": {
                    "pl_pirate": "🏴‍☠️ Polish Pirate",
                },
            },
            "🇨🇿 Čeština": {
                "Standard": {
                    "cs": "🇨🇿 Čeština",
                },
            },
            "🇸🇰 Slovenčina": {
                "Standard": {
                    "sk": "🇸🇰 Slovenčina",
                },
            },
            "🇺🇦 Українська": {
                "Standard": {
                    "uk": "🇺🇦 Українська",
                },
            },
            "🇧🇾 Беларуская": {
                "Standard": {
                    "be": "🇧🇾 Беларуская",
                },
            },
            "🇧🇬 Български": {
                "Standard": {
                    "bg": "🇧🇬 Български",
                },
            },
            "🇲🇰 Македонски": {
                "Standard": {
                    "mk": "🇲🇰 Македонски",
                },
            },
            "🇷🇸 Српски": {
                "Standard": {
                    "sr": "🇷🇸 Српски",
                    "sr_Cyrl": "🇷🇸 Српски (Ћирилица)",
                    "sr_Latn": "🇷🇸 Srpski (Latinica)",
                },
            },
            "🇭🇷 Hrvatski": {
                "Standard": {
                    "hr": "🇭🇷 Hrvatski",
                },
            },
            "🇧🇦 Bosanski": {
                "Standard": {
                    "bs": "🇧🇦 Bosanski",
                    "bs_Latn": "🇧🇦 Bosanski (Latin)",
                },
            },
            "🇸🇮 Slovenščina": {
                "Standard": {
                    "sl": "🇸🇮 Slovenščina",
                },
            },
            "🇪🇪 Eesti": {
                "Standard": {
                    "et": "🇪🇪 Eesti",
                },
            },
            "🇱🇻 Latviešu": {
                "Standard": {
                    "lv": "🇱🇻 Latviešu",
                },
            },
            "🇱🇹 Lietuvių": {
                "Standard": {
                    "lt": "🇱🇹 Lietuvių",
                },
            },
            "🇭🇺 Magyar": {
                "Standard": {
                    "hu": "🇭🇺 Magyar",
                },
            },
            "🇦🇱 Shqip": {
                "Standard": {
                    "sq": "🇦🇱 Shqip",
                },
            },
        },
        # ================================================
        # 4️⃣ ASIATISCHE SPRACHEN
        # ================================================
        "4️⃣ Asiatische Sprachen": {
            "🇨🇳 中文": {
                "Standard": {
                    "zh": "🇨🇳 中文",
                    "zh-Hans": "🇨🇳 中文(简体)",
                    "zh_Hant": "🇹🇼 中文(繁體)",
                },
                "🏴‍☠️ Pirate": {
                    "zh_pirate": "🏴‍☠️ Chinese Pirate",
                },
            },
            "🇯🇵 日本語": {
                "Standard": {
                    "ja": "🇯🇵 日本語",
                },
                "🏴‍☠️ Pirate": {
                    "ja_pirate": "🏴‍☠️ Japanese Pirate",
                },
            },
            "🇰🇷 한국어": {
                "Standard": {
                    "ko": "🇰🇷 한국어",
                },
            },
            "🇮🇳 हिन्दी": {"Standard": {"hi": "🇮🇳 हिन्दी"}},
            "🇮🇳 বাংলা": {"Standard": {"bn": "🇮🇳 বাংলা"}},
            "🇮🇳 தமிழ்": {"Standard": {"ta": "🇮🇳 தமிழ்"}},
            "🇮🇳 తెలుగు": {"Standard": {"te": "🇮🇳 తెలుగు"}},
            "🇮🇳 मराठी": {"Standard": {"mr": "🇮🇳 मराठी"}},
            "🇮🇳 ગુજરાતી": {"Standard": {"gu": "🇮🇳 ગુજરાતી"}},
            "🇮🇳 ಕನ್ನಡ": {"Standard": {"kn": "🇮🇳 ಕನ್ನಡ"}},
            "🇮🇳 മലയാളം": {"Standard": {"ml": "🇮🇳 മലയാളം"}},
            "🇮🇳 ਪੰਜਾਬੀ": {"Standard": {"pa": "🇮🇳 ਪੰਜਾਬੀ"}},
            "🇮🇳 অসমীয়া": {"Standard": {"as": "🇮🇳 অসমীয়া"}},
            "🇮🇳 कोंकणी": {"Standard": {"kok": "🇮🇳 कोंकणी"}},
            "🇮🇳 ଓଡ଼ିଆ": {"Standard": {"or": "🇮🇳 ଓଡ଼ିଆ"}},
            "🇳🇵 नेपाली": {"Standard": {"ne": "🇳🇵 नेपाली"}},
            "🇱🇰 සිංහල": {"Standard": {"si": "🇱🇰 සිංහල"}},
            "🇹🇭 ภาษาไทย": {"Standard": {"th": "🇹🇭 ภาษาไทย"}},
            "🇻🇳 Tiếng Việt": {"Standard": {"vi": "🇻🇳 Tiếng Việt"}},
            "🇮🇩 Bahasa Indonesia": {"Standard": {"id": "🇮🇩 Bahasa Indonesia"}},
            "🇲🇾 Bahasa Melayu": {"Standard": {"ms": "🇲🇾 Bahasa Melayu"}},
            "🇵🇭 Filipino": {"Standard": {"fil": "🇵🇭 Filipino"}},
            "🇰🇭 ខ្មែរ": {"Standard": {"km": "🇰🇭 ខ្មែរ"}},
            "🇱🇦 ລາວ": {"Standard": {"lo": "🇱🇦 ລາວ"}},
            "🇲🇳 Монгол": {"Standard": {"mn_Cyrl": "🇲🇳 Монгол", "mn": "🇲🇳 Монгол (Cyrillic)"}},
            "🇰🇿 Қазақ тілі": {"Standard": {"kk": "🇰🇿 Қазақ тілі"}},
            "🇺🇿 O'zbek": {"Standard": {"uz_Latn": "🇺🇿 O'zbek", "uz": "🇺🇿 O'zbek (Latin)"}},
            "🇹🇲 Türkmen": {"Standard": {"tk": "🇹🇲 Türkmen dili"}},
            "🇹🇯 Тоҷикӣ": {"Standard": {"tg_Cyrl": "🇹🇯 Тоҷикӣ", "tg": "🇹🇯 Тоҷикӣ (Cyrillic)"}},
            "🇨🇳 ئۇيغۇرچە": {"Standard": {"ug": "🇨🇳 ئۇيغۇرچە"}},
            "🇦🇲 Հայերեն": {"Standard": {"hy": "🇦🇲 Հայերեն"}},
            "🇬🇪 ქართული": {"Standard": {"ka": "🇬🇪 ქართული"}},
            "🇦🇿 Azərbaycan": {"Standard": {"az_Latn": "🇦🇿 Azərbaycan", "az": "🇦🇿 Azərbaycan (Latin)"}},
        },
        # ================================================
        # 5️⃣ NAHER OSTEN & AFRIKA
        # ================================================
        "5️⃣ Naher Osten & Afrika": {
            "🇸🇦 العربية": {"Standard": {"ar": "🇸🇦 العربية"}},
            "🇮🇱 עברית": {"Standard": {"he": "🇮🇱 עברית"}},
            "🇮🇷 فارسی": {"Standard": {"fa": "🇮🇷 فارسی", "fa_AF": "🇦🇫 دری", "prs": "🇦🇫 دری"}},
            "🇹🇷 Türkçe": {
                "Standard": {"tr": "🇹🇷 Türkçe"},
                "🏴‍☠️ Pirate": {"tr_pirate": "🏴‍☠️ Turkish Pirate"},
            },
            "🇵🇰 اردو": {"Standard": {"ur": "🇵🇰 اردو"}},
            "🇮🇶 کوردی": {"Standard": {"ku_Arab": "🇮🇶 کوردی", "ku": "🇮🇶 کوردی (Arabic)"}},
            "🇵🇰 سنڌي": {"Standard": {"sd_Arab": "🇵🇰 سنڌي", "sd": "🇵🇰 سنڌي (Arabic)"}},
            "🇰🇪 Kiswahili": {"Standard": {"sw": "🇰🇪 Kiswahili"}},
            "🇿🇦 Afrikaans": {"Standard": {"af": "🇿🇦 Afrikaans"}},
            "🇳🇬 Hausa": {"Standard": {"ha_Latn": "🇳🇬 Hausa", "ha": "🇳🇬 Hausa (Latin)"}},
            "🇳🇬 Igbo": {"Standard": {"ig": "🇳🇬 Igbo"}},
            "🇳🇬 Yorùbá": {"Standard": {"yo": "🇳🇬 Yorùbá"}},
            "🇸🇳 Wolof": {"Standard": {"wo": "🇸🇳 Wolof"}},
            "🇷🇼 Kinyarwanda": {"Standard": {"rw": "🇷🇼 Kinyarwanda"}},
            "🇿🇦 Sesotho sa Leboa": {"Standard": {"nso": "🇿🇦 Sesotho sa Leboa"}},
            "🇧🇼 Setswana": {"Standard": {"tn": "🇧🇼 Setswana"}},
            "🇿🇦 isiXhosa": {"Standard": {"xh": "🇿🇦 isiXhosa"}},
            "🇿🇦 isiZulu": {"Standard": {"zu": "🇿🇦 isiZulu"}},
            "🇪🇹 ትግርኛ": {"Standard": {"ti": "🇪🇹 ትግርኛ"}},
            "🇪🇹 አማርኛ": {"Standard": {"am": "🇪🇹 አማርኛ"}},
            "🇸🇴 Somali": {"Standard": {"so": "🇸🇴 Somali"}},
        },
        # ================================================
        # 6️⃣ KELTISCHE, KONSTRUIERTE & HISTORISCHE SPRACHEN
        # ================================================
        "6️⃣ Keltische, Konstruierte & Historische Sprachen": {
            "🏴󠁧󠁢󠁷󠁬󠁳󠁿 Cymraeg": {"Standard": {"cy": "🏴󠁧󠁢󠁷󠁬󠁳󠁿 Cymraeg"}},
            "🇮🇪 Gaeilge": {"Standard": {"ga": "🇮🇪 Gaeilge"}},
            "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Gàidhlig": {"Standard": {"gd": "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Gàidhlig"}},
            "🇪🇸 Euskara": {"Standard": {"eu": "🇪🇸 Euskara"}},
            "🌍 Esperanto": {"Standard": {"eo": "🌍 Esperanto"}},
            "🌍 Interlingua": {"Standard": {"ia": "🌍 Interlingua"}},
            "🖖 tlhIngan Hol": {
                "Standard": {"tlh": "🖖 tlhIngan Hol"},
                "🏴‍☠️ Pirate": {"tlh_pirate": "🏴‍☠️ Klingon Pirate"},
            },
            "🇻🇦 Latina": {"Standard": {"la": "🇻🇦 Latina"}},
            "🇮🇱 ייִדיש": {"Standard": {"yi": "🇮🇱 ייִדיש", "yi_latn": "🇮🇱 Yiddish (Latin)"}},
            "🇵🇪 Runasimi": {"Standard": {"quz": "🇵🇪 Runasimi"}},
            "🇺🇸 ᏣᎳᎩ": {"Standard": {"chr": "🇺🇸 ᏣᎳᎩ"}},
            "🇳🇿 Te reo Māori": {"Standard": {"mi": "🇳🇿 Te reo Māori"}},
        },
        # ================================================
        # 7️⃣ WEITERE SPRACHEN & SPEZIAL
        # ================================================
        "7️⃣ Weitere Sprachen & Spezial": {
            "🇬🇷 Ελληνικά": {"Standard": {"el": "🇬🇷 Ελληνικά"}},
            "🇲🇹 Malti": {"Standard": {"mt": "🇲🇹 Malti"}},
            "🇱🇺 Lëtzebuergesch": {"Standard": {"lb": "🇱🇺 Lëtzebuergesch"}},
            "🇦🇫 پښتو": {"Standard": {"ps": "🇦🇫 پښتو"}},
            "🇷🇺 Татар": {"Standard": {"tt": "🇷🇺 Татар"}},
            "🌴 Pazifik & Kreol": {
                "Standard": {
                    "ay": "🇧🇴 Aymara",
                    "bi": "🇻🇺 Bislama",
                    "crs": "🇸🇨 Seselwa Creole",
                    "dz": "🇧🇹 Dzongkha",
                    "fj": "🇫🇯 Fidschi",
                    "gil": "🇰🇮 Gilbertese",
                    "gn": "🇵🇾 Guaraní",
                    "hif": "🇫🇯 Fiji Hindi",
                    "ho": "🇵🇬 Hiri Motu",
                    "ht": "🇭🇹 Haitian Creole",
                    "mg": "🇲🇬 Malagasy",
                    "mh": "🇲🇭 Marshallese",
                    "na": "🇳🇷 Nauru",
                    "pau": "🇵🇼 Palau",
                    "sg": "🇨🇫 Sango",
                    "sm": "🇼🇸 Samoan",
                    "tet": "🇹🇱 Tetum",
                    "to": "🇹🇴 Tonga",
                    "tpi": "🇵🇬 Tok Pisin",
                    "tvl": "🇹🇻 Tuvalu",
                },
            },
        },
    }

    def __init__(self):
        self.current_language = "de"
        self.translations: Dict[str, Optional[Dict]] = {}
        self.translations_dir = Path(__file__).parent.parent.parent / "i18n" / "translations"
        self.override_service = get_override_service()
        self.custom_languages: Dict[str, Dict] = {}
        self._load_custom_languages()
        self._load_translations()

    def _load_custom_languages(self):
        """Loads custom languages from AppData."""
        from core.services.custom_language_service import get_custom_language_service
        custom_service = get_custom_language_service()
        for lang_code, lang_data in custom_service.get_all_custom_languages().items():
            self.custom_languages[lang_code] = lang_data
        if self.custom_languages:
            print(f"[i18n] ✅ {len(self.custom_languages)} Custom Languages geladen")

    def delete_custom_language(self, lang_code: str) -> bool:
        """Deletes a custom language and reloads."""
        from core.services.custom_language_service import get_custom_language_service
        custom_service = get_custom_language_service()
        if custom_service.delete_custom_language(lang_code):
            if lang_code in self.custom_languages:
                del self.custom_languages[lang_code]
            return True
        return False

    def get_custom_languages(self) -> Dict[str, Dict]:
        """Returns all custom languages."""
        return self.custom_languages.copy()

    def _get_all_language_codes(self) -> List[str]:
        """Extract all language codes from groups and custom languages."""
        codes = []
