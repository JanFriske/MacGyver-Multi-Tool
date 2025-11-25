"""
i18n Service - Central translation management
Minimal, working 7-category geographic structure with required methods
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# External service for user overrides (provided by the app)
from core.services.user_override_service import get_override_service


class I18nService:
    """Central service for internationalization (minimal, working version)."""

    # ======================================================
    # 7 GEOGRAPHIC CATEGORIES (5 Continents + 2 Special)
    # Struktur: Kontinent -> Sprache -> Untergruppen -> { code: name }
    # - Leaf dicts map language codes to display names (strings)
    # - Dialects/variants go into submenus of their base language
    # - Includes flag icons per user request
    # ======================================================
    LANGUAGE_GROUPS: Dict[str, Dict[str, Dict[str, Dict[str, str]]]] = {
        # 1) Eurasien
        "🌍 Eurasien": {
            "🇪🇺 Europa": {
                "Mitteleuropa": {
                    "🇩🇪 Deutsch": {
                        "Deutschland": {
                            "Hochdeutsch": {"de": "🇩🇪 Deutsch (Deutschland)"},
                            "Piraten": {"de_pirate": "🏴‍☠️ Deutsch (Piraten)"},
                            "Norddeutschland": {
                                "Plattdeutsch": {"de_lowgerman": "🇩🇪 Plattdeutsch", "de_mecklenburg": "🇩🇪 Mecklenburger Platt", "de_holstein": "🇩🇪 Holsteiner Platt"},
                                "Städtisch": {"de_hamburg": "🇩🇪 Hamburger Platt", "de_bremen": "🇩🇪 Bremer Platt"},
                            },
                            "Mitteldeutschland": {
                                "Dialekte": {"de_uppersaxon": "🇩🇪 Obersächsisch", "de_saxony": "🇩🇪 Sächsisch", "de_thuringia": "🇩🇪 Thüringisch", "de_lusatian": "🇩🇪 Lausitzisch", "de_brandenburg": "🇩🇪 Brandenburgisch"},
                                "Städtisch": {"de_berlin": "🇩🇪 Berlinerisch", "de_frankfurt": "🇩🇪 Frankfurterisch 🍎", "de_dresden": "🇩🇪 Dresdnerisch", "de_leipzig": "🇩🇪 Leipzigerisch"},
                            },
                            "Ostdeutschland": {
                                "Historische Ostgebiete": {"de_pomeranian": "🇩🇪 Pommersch (Stettin) 🔴", "de_lowprussia": "🇩🇪 Niederpreußisch 💀", "de_eastprussia": "🇩🇪 Ostpreußisch (Königsberg) 💀", "de_eastprussia_lithuanian": "🇩🇪 Ostpreußisch-Litauisch", "de_silesian": "🇩🇪 Schlesisch 💀", "de_silesian_lower": "🇩🇪 Niederschlesisch", "de_silesian_upper": "🇩🇪 Oberschlesisch"},
                            },
                            "Westdeutschland": {
                                "Dialekte": {"de_westphalian": "🇩🇪 Westfälisch", "de_moselfranken": "🇩🇪 Moselfränkisch", "de_rhine": "🇩🇪 Rheinisch", "de_ruhr": "🇩🇪 Ruhrdeutsch", "de_hessian": "🇩🇪 Hessisch", "de_franconian": "🇩🇪 Fränkisch"},
                                "Städtisch": {"de_ripuarian": "🇩🇪 Kölsch 🎭", "de_duesseldorf": "🇩🇪 Düsseldorfer Platt", "de_mainz": "🇩🇪 Mainzerisch"},
                            },
                            "Süddeutschland": {
                                "Dialekte": {"de_bavaria": "🇩🇪 Bairisch", "de_swabian": "🇩🇪 Schwäbisch", "de_alemannic": "🇩🇪 Alemannisch", "de_baden": "🇩🇪 Badisch", "de_allgaeu": "🇩🇪 Allgäuerisch", "de_palatinate": "🇩🇪 Pfälzisch"},
                                "Städtisch": {"de_munich": "🇩🇪 Münchnerisch", "de_stuttgart": "🇩🇪 Stuttgarter Schwäbisch", "de_nuremberg": "🇩🇪 Nürnbergerisch"},
                            },
                        },
                        "Österreich": {"Standard": {"de_at": "🇦🇹 Österreichisch"}, "Dialekte": {"de_vorarlberg": "🇦🇹 Vorarlbergisch", "de_AT_carinthia": "🇦🇹 Kärntnerisch"}},
                        "Schweiz": {"Standard": {"de_ch": "🇨🇭 Schweizerdeutsch (Standard)"}, "Dialekte": {"de_CH_basel": "🇨🇭 Baseldeutsch", "de_CH_bern": "🇨🇭 Berner Deutsch", "de_CH_zurich": "🇨🇭 Zürichdeutsch"}},
                        "Exklaven": {
                            "Sudetenland": {"de_sudeten": "🇩🇪 Sudetendeutsch 💀"},
                            "Grenzregionen": {"de_southtyrol": "🇮🇹 Südtirolerisch", "de_FR_alsace": "🇫🇷 Elsässisch", "de_luxembourg": "🇱🇺 Luxemburgisch"},
                            "Auslandsdeutsch": {"de_banat": "🇷🇴 Banater Schwäbisch", "de_sathmar": "🇷🇴 Sathmarer Schwäbisch", "de_transylvania": "🇷🇴 Siebenbürgisch-Sächsisch", "de_volga": "🇷🇺 Wolgadeutsch 💀"},
                        },
                    },
                    "🇵🇱 Polski": {"Standard": {"pl": "🇵🇱 Polski"}, "Dialekte": {"csb": "🇵🇱 Kashubisch", "szl": "🇵🇱 Schlesisch (Polnisch)"}, "Pirate": {"pl_pirate": "🏴‍☠️ Polski (Pirat)"}},
                    "🇨🇿 Čeština": {"Standard": {"cs": "🇨🇿 Čeština"}},
                    "🇸🇰 Slovenčina": {"Standard": {"sk": "🇸🇰 Slovenčina"}},
                    "🇭🇺 Magyar": {"Standard": {"hu": "🇭🇺 Magyar"}},
                },
                "Westeuropa": {
                    "🇬🇧 English (UK)": {"Standard": {"en_GB": "🇬🇧 English (UK)"}, "Pirate": {"en_pirate": "🏴‍☠️ English (Pirate)"}},
                    "🇫🇷 Français": {"Standard": {"fr": "🇫🇷 Français"}, "Pirate": {"fr_pirate": "🏴‍☠️ Français (Pirate)"}},
                    "🇳🇱 Nederlands": {"Standard": {"nl": "🇳🇱 Nederlands"}, "Dialekte": {"fy": "🇳🇱 Frysk", "li": "🇳🇱 Limburgs"}, "Pirate": {"nl_pirate": "🏴‍☠️ Nederlands (Piraat)"}},
                    "🇮🇪 Gaeilge": {"Standard": {"ga": "🇮🇪 Gaeilge"}},
                    "🏴󠁧󠁢󠁷󠁬󠁳󠁿 Cymraeg": {"Standard": {"cy": "🏴󠁧󠁢󠁷󠁬󠁳󠁿 Cymraeg"}},
                    "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Gàidhlig": {"Standard": {"gd": "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Gàidhlig"}},
                    "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scots": {"Standard": {"sco": "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scots"}, "Pirate": {"sco_pirate": "🏴‍☠️ Scots (Pirate)"}},
                },
                "Nordeuropa": {
                    "🇸🇪 Svenska": {"Standard": {"sv": "🇸🇪 Svenska"}},
                    "🇩🇰 Dansk": {"Standard": {"da": "🇩🇰 Dansk"}},
                    "🇳🇴 Norsk": {"Standard": {"nb": "🇳🇴 Norsk (Bokmål)", "nn": "🇳🇴 Nynorsk"}},
                    "🇫🇮 Suomi": {"Standard": {"fi": "🇫🇮 Suomi"}},
                    "🇮🇸 Íslenska": {"Standard": {"is": "🇮🇸 Íslenska"}},
                    "🇪🇪 Eesti": {"Standard": {"et": "🇪🇪 Eesti"}},
                    "🇱🇻 Latviešu": {"Standard": {"lv": "🇱🇻 Latviešu"}},
                    "🇱🇹 Lietuvių": {"Standard": {"lt": "🇱🇹 Lietuvių"}},
                },
                "Südeuropa": {
                    "🇪🇸 Español (España)": {"Standard": {"es": "🇪🇸 Español"}, "Dialekte": {"es_andalucia": "🇪🇸 Andalusisch", "ca": "🇪🇸 Català", "ca_ES_valencia": "🇪🇸 Valencià", "gl": "🇪🇸 Galego", "eu": "🇪🇸 Euskara"}, "Pirate": {"es_pirate": "🏴‍☠️ Español (Pirata)"}},
                    "🇮🇹 Italiano": {"Standard": {"it": "🇮🇹 Italiano"}},
                    "🇵🇹 Português (Portugal)": {"Standard": {"pt": "🇵🇹 Português", "pt_PT": "🇵🇹 Português (Portugal)"}, "Pirate": {"pt_pirate": "🏴‍☠️ Português (Pirata)"}},
                    "🇬🇷 Ελληνικά": {"Standard": {"el": "🇬🇷 Ελληνικά"}},
                    "🇲🇹 Malti": {"Standard": {"mt": "🇲🇹 Malti"}},
                    "🇭🇷 Hrvatski": {"Standard": {"hr": "🇭🇷 Hrvatski"}},
                    "🇷🇸 Српски": {"Standard": {"sr": "🇷🇸 Српски", "sr_Cyrl": "🇷🇸 Српски (Cyrillic)", "sr_Latn": "🇷🇸 Srpski (Latin)"}},
                    "🇧🇦 Bosanski": {"Standard": {"bs": "🇧🇦 Bosanski", "bs_Latn": "🇧🇦 Bosanski (Latin)"}},
                    "🇲🇰 Македонски": {"Standard": {"mk": "🇲🇰 Македонски"}},
                    "🇦🇱 Shqip": {"Standard": {"sq": "🇦🇱 Shqip"}},
                    "🇸🇮 Slovenščina": {"Standard": {"sl": "🇸🇮 Slovenščina"}},
                    "🇧🇬 Български": {"Standard": {"bg": "🇧🇬 Български"}},
                    "🇷🇴 Română": {"Standard": {"ro": "🇷🇴 Română"}},
                    "🇫🇷 Corsu": {"Standard": {"co": "🇫🇷 Corsu"}},
                },
                "Osteuropa": {
                    "🇷🇺 Русский": {"Standard": {"ru": "🇷🇺 Русский"}, "Pirate": {"ru_pirate": "🏴‍☠️ Русский (Пират)"}},
                    "🇺🇦 Українська": {"Standard": {"uk": "🇺🇦 Українська"}},
                    "🇧🇾 Беларуская (Belarusian)": {"Standard": {"be": "🇧🇾 Беларуская"}},
                },
            },
            "🌏 Asien": {
                "Ostasien": {
                    "🇨🇳 中文 (Chinesisch)": {"Standard": {"zh": "🇨🇳 中文", "zh-Hans": "🇨🇳 中文(简体)", "zh_Hant": "🇹🇼 中文(繁體)"}, "Pirate": {"zh_pirate": "🏴‍☠️ 中文 (海盗)"}},
                    "🇯🇵 日本語": {"Standard": {"ja": "🇯🇵 日本語"}, "Pirate": {"ja_pirate": "🏴‍☠️ 日本語 (海賊)"}},
                    "🇰🇷 한국어": {"Standard": {"ko": "🇰🇷 한국어"}},
                    "🇲🇳 Монгол (Mongolian)": {"Standard": {"mn": "🇲🇳 Монгол"}},
                },
                "Südasien": {
                    "🇮🇳 हिन्दी (Hindi)": {"Standard": {"hi": "🇮🇳 हिन्दी"}},
                    "🇵🇰 اردو (Urdu)": {"Standard": {"ur": "🇵🇰 اردو"}},
                    "🇧🇩 বাংলা (Bengali)": {"Standard": {"bn": "🇧🇩 বাংলা"}},
                    "🇮🇳 ગુજરાતી (Gujarati)": {"Standard": {"gu": "🇮🇳 ગુજરાતી"}},
                    "🇮🇳 ಕನ್ನಡ (Kannada)": {"Standard": {"kn": "🇮🇳 ಕನ್ನಡ"}},
                    "🇮🇳 മലയാളം (Malayalam)": {"Standard": {"ml": "🇮🇳 മലയാളം"}},
                    "🇮🇳 मराठी (Marathi)": {"Standard": {"mr": "🇮🇳 मराठी"}},
                    "🇮🇳 ଓଡ଼ିଆ (Odia)": {"Standard": {"or": "🇮🇳 ଓଡ଼ିଆ"}},
                    "🇮🇳 ਪੰਜਾਬੀ (Punjabi)": {"Standard": {"pa": "🇮🇳 ਪੰਜਾਬੀ"}},
                    "🇮🇳 தமிழ் (Tamil)": {"Standard": {"ta": "🇮🇳 தமிழ்"}},
                    "🇮🇳 తెలుగు (Telugu)": {"Standard": {"te": "🇮🇳 తెలుగు"}},
                    "🇮🇳 অসমীয়া (Assamese)": {"Standard": {"as": "🇮🇳 অসমীয়া"}},
                    "🇮🇳 कोंकणी (Konkani)": {"Standard": {"kok": "🇮🇳 कोंकणी"}},
                    "🇱🇰 සිංහල (Sinhala)": {"Standard": {"si": "🇱🇰 සිංහල"}},
                    "🇳🇵 नेपाली (Nepali)": {"Standard": {"ne": "🇳🇵 नेपाली"}},
                    "🇵🇰 سنڌي (Sindhi)": {"Standard": {"sd": "🇵🇰 سنڌي", "sd_Arab": "🇵🇰 سنڌي (Arabic)"}},
                    "🇫🇯 Fiji Hindi": {"Standard": {"hif": "🇫🇯 Fiji Hindi"}},
                },
                "Südostasien": {
                    "🇮🇩 Bahasa Indonesia": {"Standard": {"id": "🇮🇩 Bahasa Indonesia"}},
                    "🇹🇭 ไทย (Thai)": {"Standard": {"th": "🇹🇭 ไทย"}},
                    "🇻🇳 Tiếng Việt": {"Standard": {"vi": "🇻🇳 Tiếng Việt"}},
                    "🇲🇾 Bahasa Melayu": {"Standard": {"ms": "🇲🇾 Bahasa Melayu"}},
                    "🇵🇭 Filipino": {"Standard": {"fil": "🇵🇭 Filipino"}},
                    "🇰🇭 ភាសាខ្មែរ (Khmer)": {"Standard": {"km": "🇰🇭 ភាសាខ្មែរ"}},
                    "🇱🇦 ພາສາລາວ (Lao)": {"Standard": {"lo": "🇱🇦 ພາສາລາວ"}},
                    "🇲🇲 မြန်မာဘာသာ (Burmese)": {"Standard": {"my": "🇲🇲 မြန်မာဘာသာ"}},
                },
                "Vorderasien": {
                    "🇸🇦 العربية (Arabisch)": {"Standard": {"ar": "🇸🇦 العربية"}},
                    "🇮🇱 עברית (Hebräisch)": {"Standard": {"he": "🇮🇱 עברית"}},
                    "🇮🇷 فارسی (Persisch)": {"Standard": {"fa": "🇮🇷 فارسی", "fa_AF": "🇦🇫 دری", "prs": "🇦🇫 دری"}},
                    "🇹🇷 Türkçe": {"Standard": {"tr": "🇹🇷 Türkçe"}, "Pirate": {"tr_pirate": "🏴‍☠️ Türkçe (Korsan)"}},
                    "🇦🇿 Azərbaycan dili": {"Standard": {"az": "🇦🇿 Azərbaycan", "az_Latn": "🇦🇿 Azərbaycan (Latin)"}},
                    "🇬🇪 ქართული (Georgian)": {"Standard": {"ka": "🇬🇪 ქართული"}},
                    "🇦🇲 Հայերեն (Armenian)": {"Standard": {"hy": "🇦🇲 Հայերեն"}},
                },
                "Zentralasien": {
                    "🇰🇿 Қазақ тілі (Kasachisch)": {"Standard": {"kk": "🇰🇿 Қазақ тілі"}},
                    "🇺🇿 Oʻzbek tili": {"Standard": {"uz": "🇺🇿 Oʻzbek", "uz_Latn": "🇺🇿 Oʻzbek (Latin)"}},
                    "🇹🇲 Türkmen dili": {"Standard": {"tk": "🇹🇲 Türkmen"}},
                    "🇹🇯 Тоҷикӣ (Tadschikisch)": {"Standard": {"tg": "🇹🇯 Тоҷикӣ", "tg_Cyrl": "🇹🇯 Тоҷикӣ (Cyrillic)"}},
                    "🇷🇺 Татар теле (Tatarisch)": {"Standard": {"tt": "🇷🇺 Татар"}},
                    "🇨🇳 ئۇيغۇرچە (Uigurisch)": {"Standard": {"ug": "🇨🇳 ئۇيغۇرچە"}},
                    "🇰🇬 Кыргызча (Kyrgyz)": {"Standard": {"ky": "🇰🇬 Кыргызча"}},
                },
            },
        },
        # 2) Amerika
        "🌎 Amerika": {
            "Nordamerika": {
                "🇺🇸 English (USA)": {"Standard": {"en": "🇺🇸 English"}},
                "🇨🇦 Français (Canada)": {"Standard": {"fr_CA": "🇨🇦 Français"}, "Pirate": {"fr_CA_pirate": "🏴‍☠️ Français Canadien (Pirate)"}},
                "🇺🇸 ᏣᎳᎩ (Cherokee)": {"Standard": {"chr": "🇺🇸 ᏣᎳᎩ"}},
            },
            "Mittelamerika": {
                "🇲🇽 Español (México)": {"Standard": {"es_MX": "🇲🇽 Español"}},
                "🇭🇹 Kreyòl Ayisyen": {"Standard": {"ht": "🇭🇹 Haitian Creole"}},
            },
            "Südamerika": {
                "🇧🇷 Português (Brasil)": {"Standard": {"pt_BR": "🇧🇷 Português (Brasil)"}},
                "🇦🇷 Español (Argentina)": {"Standard": {"es": "🇦🇷 Español"}},
                "🇵🇪 Runasimi (Quechua)": {"Standard": {"quz": "🇵🇪 Runasimi"}},
                "🇵🇾 Guaraní": {"Standard": {"gn": "🇵🇾 Guaraní"}},
                "🇧🇴 Aymara": {"Standard": {"ay": "🇧🇴 Aymara"}},
            },
        },
        # 3) Afrika
        "🌍 Afrika": {
            "Nordafrika": {
                "🇪🇬 العربية (Nordafrika)": {"Standard": {"ar": "🇪🇬 العربية"}},
            },
            "Westafrika": {
                "🇳🇬 Yoruba": {"Standard": {"yo": "🇳🇬 Yoruba"}},
                "🇳🇬 Igbo": {"Standard": {"ig": "🇳🇬 Igbo"}},
                "🇳🇬 Hausa": {"Standard": {"ha": "🇳🇬 Hausa", "ha_Latn": "🇳🇬 Hausa (Latin)"}},
                "🇸🇳 Wolof": {"Standard": {"wo": "🇸🇳 Wolof"}},
            },
            "Ostafrika": {
                "🇰🇪 Kiswahili": {"Standard": {"sw": "🇰🇪 Kiswahili"}},
                "🇪🇹 አማርኛ (Amharisch)": {"Standard": {"am": "🇪🇹 አማርኛ"}},
                "🇪🇷 ትግርኛ (Tigrinya)": {"Standard": {"ti": "🇪🇷 ትግርኛ"}},
                "🇸🇴 Soomaaliga": {"Standard": {"so": "🇸🇴 Soomaaliga"}},
                "🇷🇼 Kinyarwanda": {"Standard": {"rw": "🇷🇼 Kinyarwanda"}},
                "🇲🇬 Malagasy": {"Standard": {"mg": "🇲🇬 Malagasy"}},
            },
            "Zentralafrika": {
                "🇨🇫 Sängö": {"Standard": {"sg": "🇨🇫 Sängö"}},
            },
            "Südliches Afrika": {
                "🇿🇦 Afrikaans": {"Standard": {"af": "🇿🇦 Afrikaans"}},
                "🇿🇦 isiZulu": {"Standard": {"zu": "🇿🇦 isiZulu"}},
                "🇿🇦 isiXhosa": {"Standard": {"xh": "🇿🇦 isiXhosa"}},
                "🇿🇦 Sesotho sa Leboa": {"Standard": {"nso": "🇿🇦 Northern Sotho"}},
                "🇧🇼 Setswana": {"Standard": {"tn": "🇧🇼 Setswana"}},
                "🇱🇸 Sesotho": {"Standard": {"st": "🇱🇸 Sesotho"}},
                "🇸🇿 SiSwati": {"Standard": {"ss": "🇸🇿 SiSwati"}},
            },
        },
        # 4) Ozeanien
        "🌊 Ozeanien": {
            "Australien & Neuseeland": {
                "🇳🇿 Te reo Māori": {"Standard": {"mi": "🇳🇿 Te reo Māori"}},
            },
            "Polynesien": {
                "🇼🇸 Gagana Sāmoa": {"Standard": {"sm": "🇼🇸 Samoan"}},
                "🇹🇴 Lea faka-Tonga": {"Standard": {"to": "🇹🇴 Tonga"}},
                "🇹🇻 Te Ggana Tuuvalu": {"Standard": {"tvl": "🇹🇻 Tuvaluan"}},
            },
            "Melanesien": {
                "🇵🇬 Tok Pisin": {"Standard": {"tpi": "🇵🇬 Tok Pisin"}},
                "🇻🇺 Bislama": {"Standard": {"bi": "🇻🇺 Bislama"}},
                "🇫🇯 Na Vosa Vakaviti (Fijian)": {"Standard": {"fj": "🇫🇯 Fijian"}},
                "🇵🇬 Hiri Motu": {"Standard": {"ho": "🇵🇬 Hiri Motu"}},
                "🇹🇱 Tetun": {"Standard": {"tet": "🇹🇱 Tetun"}},
            },
            "Mikronesien": {
                "🇰🇮 Taetae ni Kiribati": {"Standard": {"gil": "🇰🇮 Gilbertese"}},
                "🇲🇭 Kajin M̧ajeļ (Marshallese)": {"Standard": {"mh": "🇲🇭 Marshallese"}},
                "🇳🇷 Dorerin Naoero": {"Standard": {"na": "🇳🇷 Naurian"}},
                "🇵🇼 Tekoi ra Belau": {"Standard": {"pau": "🇵🇼 Palauan"}},
            },
        },
        # 5) Klassisch & Konstruiert
        "🏛️ Klassisch & Konstruiert": {
            "🕰️ Mittelhochdeutsch": {"Standard": {"gmh": "🕰️ Mittelhochdeutsch", "de_middlehigh": "🕰️ Mittelhochdeutsch (alt)"}},
            "📜 Altenglisch": {"Standard": {"ang": "📜 Altenglisch"}},
            "🌍 Esperanto": {"Standard": {"eo": "🌍 Esperanto"}},
            "🌐 Interlingua": {"Standard": {"ia": "🌐 Interlingua"}},
            "🇻🇦 Latina": {"Standard": {"la": "🇻🇦 Latina"}},
            "👽 Klingon": {"Standard": {"tlh": "👽 Klingon", "tlh_pirate": "🏴‍☠️ Klingon (Pirate)"}},
        },
    }

    def __init__(self):
        self.flags: Dict[str, str] = {}
        self.translations_dir = Path(__file__).parent.parent.parent / "i18n" / "translations"
        self.custom_languages: Dict[str, Dict] = {}
        self.translations: Dict[str, Dict] = {}
        self.current_language: str = "en"
        self.override_service = get_override_service()
        self._load_flags()
        # Normalisiere LANGUAGE_GROUPS: entferne hartkodierte führende Emojis aus Namen
        try:
            self._normalize_language_groups()
        except Exception as e:
            print(f"[i18n] Hinweis: Fehler bei Normalisierung der LANGUAGE_GROUPS: {e}")
        # Ensure certain useful variants exist in the normalized structure
        try:
            # Scots is now properly integrated in Eurasien → Europa → Westeuropa
            # No need for separate Europa entry


            # Add en_US under Americas English if missing
            amerika = self.LANGUAGE_GROUPS.get("Amerika", {})
            if "English (USA)" in amerika:
                eng_entry = amerika["English (USA)"]
                eng_entry.setdefault("Standard", {})
                if "en_US" not in eng_entry["Standard"]:
                    eng_entry["Standard"]["en_US"] = "English (US)"
            else:
                amerika["English (USA)"] = {"Standard": {"en": "English", "en_US": "English (US)"}}
            self.LANGUAGE_GROUPS["Amerika"] = amerika
        except Exception:
            pass
        self._load_translations()

    def _strip_leading_emoji(self, s: str) -> str:
        """Remove leading emoji/flag sequences from a string.
        
        Explicitly removes Regional Indicator Symbols (flags) and other common emojis.
        """
        import re
        
        if not isinstance(s, str):
            return s
            
        # Remove Regional Indicator Symbols (Flags) - range 1F1E6-1F1FF
        # We replace any sequence of 2 or more of these
        s = re.sub(r'[\U0001F1E6-\U0001F1FF]{2,}', '', s)
        
        # Remove other common emojis (ranges are approximate but cover most)
        # 1F300-1F9FF: Misc Symbols and Pictographs, Emoticons, Transport, etc.
        s = re.sub(r'[\U0001F300-\U0001F9FF]+', '', s)
        
        # Remove specific hardcoded chars found in translations
        for char in ["🕰️", "🔴", "💀", "🎭", "🍎", "⬆️"]:
            s = s.replace(char, "")
            
        # Finally clean up leading non-word chars and whitespace
        return re.sub(r"^[^\w\s]+\s*", "", s).strip()

    def _normalize_language_groups(self) -> None:
        """Walk LANGUAGE_GROUPS and remove leading emoji from leaf display names.

        This keeps keys (which often include emoji for group headers) untouched,
        but ensures that the actual language labels (values) are free of hardcoded flags.
        """
        def normalize_values(subgroup):
            if not isinstance(subgroup, dict):
                return subgroup
            
            new_sub = {}
            for k, v in subgroup.items():
                if isinstance(v, dict):
                    # Recurse into nested dictionaries
                    new_sub[k] = normalize_values(v)
                elif isinstance(v, str):
                    # Sanitize all string values (language names)
                    new_sub[k] = self._strip_leading_emoji(v)
                else:
                    # Keep other types as is
                    new_sub[k] = v
            return new_sub

        def normalize_keys(d):
            # Rebuild dict with stripped keys (avoid collisions)
            new_d = {}
            for k, v in d.items():
                new_key = self._strip_leading_emoji(k)
                new_val = v
                if isinstance(v, dict):
                    # First normalize values inside
                    new_val = normalize_values(v)
                    # Then recurse into nested keys as well
                    # For nested grouping layers, apply key stripping recursively
                    new_val = normalize_keys(new_val)
                # Collision handling: if new_key already present, keep original key
                if new_key in new_d and new_key != k:
                    print(f"[i18n] Warnung: Key-Kollision beim Normalisieren: '{k}' -> '{new_key}' (Überspringe Umbenennung)")
                    new_d[k] = new_val
                else:
                    new_d[new_key] = new_val
            return new_d

        try:
            self.LANGUAGE_GROUPS = normalize_keys(self.LANGUAGE_GROUPS)
        except Exception as e:
            print(f"[i18n] Fehler bei normalize_keys: {e}")

    def get_language_groups(self) -> Dict[str, Dict]:
        return self.LANGUAGE_GROUPS

    def get_custom_languages(self) -> Dict[str, Dict]:
        return self.custom_languages

    def _load_flags(self) -> None:
        """Load flag mapping from i18n/flags.json (lang_code -> country_code)"""
        flags_path = Path(__file__).parent.parent.parent / "i18n" / "flags.json"
        try:
            if flags_path.exists():
                with open(flags_path, "r", encoding="utf-8") as f:
                    # flags.json now contains lang_code -> country_code mappings
                    # e.g., {"de": "de", "de_at": "at", "en_GB": "gb"}
                    self.flags = json.load(f)
        except Exception as e:
            print(f"[i18n] Hinweis: Konnte flags.json nicht laden: {e}")

    def get_flag(self, lang_code: str) -> str:
        """Return flag SVG file path for a language code, or empty string if not defined.
        
        Returns:
            Relative path to SVG file (e.g., 'assets/flags/de.svg') or empty string
        """
        country_code = self.flags.get(lang_code, "")
        if country_code:
            return f"assets/flags/{country_code}.svg"
        return ""
    
    def get_flag_path(self, lang_code: str) -> Optional[Path]:
        """Return absolute Path object to flag SVG file, or None if not available.
        
        Args:
            lang_code: Language code (e.g., 'de', 'en_GB', 'de_at')
            
        Returns:
            Path object to SVG file or None if flag doesn't exist
        """
        country_code = self.flags.get(lang_code, "")
        if not country_code:
            return None
        
        # Resolve path relative to project root
        flag_path = Path(__file__).parent.parent.parent / "assets" / "flags" / f"{country_code}.svg"
        
        # Return path only if file exists
        if flag_path.exists():
            return flag_path
        return None

    def _language_exists(self, lang_code: str) -> bool:
        return lang_code in self.get_all_language_codes()

    def get_language_name(self, lang_code: str) -> str:
        """Return the display name for a language code, prefixed with its flag if available."""
        # Resolve base name from custom languages or LANGUAGE_GROUPS
        if lang_code in self.custom_languages:
            base_name = self.custom_languages[lang_code].get("language_name", lang_code)
        else:
            base_name = None
            for continent_dict in self.LANGUAGE_GROUPS.values():
                result = self._find_language_name_recursive(continent_dict, lang_code)
                if result:
                    base_name = result
                    break
        if base_name is None:
            base_name = lang_code
        # Prefer flags from flags.json (loaded in _load_flags).
        # If a flag exists, we strip any hardcoded emoji from the base_name
        # to ensure a clean display name. The UI is responsible for showing the flag icon.
        flag = self.get_flag(lang_code)
        
        # Strip leading emoji if present
        stripped = base_name
        try:
            # If base_name starts with an emoji followed by space, drop it
            if isinstance(base_name, str) and base_name:
                # Check for regional indicator symbols (flags) or other emojis
                # Heuristic: if first char is not alphanumeric and followed by space
                if len(base_name) > 1 and not base_name[0].isalnum():
                     parts = base_name.split(' ', 1)
                     if len(parts) > 1:
                         stripped = parts[1]
        except Exception:
            stripped = base_name

        return stripped

    def get_base_language_name(self, lang_code: str) -> str:
        """Return the language display name without any prefixed flag emoji."""
        # Check custom languages first
        if lang_code in self.custom_languages:
            return self.custom_languages[lang_code].get("language_name", lang_code)

        base_name = None
        for continent_dict in self.LANGUAGE_GROUPS.values():
            result = self._find_language_name_recursive(continent_dict, lang_code)
            if result:
                base_name = result
                break
        if base_name is None:
            base_name = lang_code
        # Strip any leading emojis that might still be present
        try:
            return self._strip_leading_emoji(base_name)
        except Exception:
            return base_name

    def _find_language_name_recursive(self, group: Dict, lang_code: str) -> Optional[str]:
        # Check if lang_code is a direct key in this group (and value is a string)
        if lang_code in group and isinstance(group[lang_code], str):
            return group[lang_code]
            
        # Recurse into subgroups
        for key, sub in group.items():
            if isinstance(sub, dict):
                # Optimization: Check "Standard" first if it exists, as it's a common pattern
                if "Standard" in sub and lang_code in sub["Standard"]:
                    return sub["Standard"][lang_code]
                
                # Recurse deeper
                result = self._find_language_name_recursive(sub, lang_code)
                if result:
                    return result
        return None

    def get_all_language_codes(self) -> List[str]:
        # Collect all language codes from LANGUAGE_GROUPS and custom languages
        codes: List[str] = []
        for continent_dict in self.LANGUAGE_GROUPS.values():
            self._collect_codes_recursive(continent_dict, codes)
        codes.extend(self.custom_languages.keys())
        return list(set(codes))

    def _collect_codes_recursive(self, group: Dict, codes: List[str]) -> None:
        for key, sub in group.items():
            if isinstance(sub, dict):
                # Check if this dict contains language codes (leafs)
                # Heuristic: if values are strings, keys are codes
                is_leaf = any(isinstance(v, str) for v in sub.values())
                if is_leaf:
                    for k, v in sub.items():
                        if isinstance(v, str):
                            codes.append(k)
                
                # Recurse deeper
                self._collect_codes_recursive(sub, codes)

    def _load_translations(self) -> None:
        """Load translation files for all known codes + custom languages."""
        try:
            if not self.translations_dir.exists():
                print(f"[i18n] Hinweis: Übersetzungsverzeichnis fehlt: {self.translations_dir}")
                return
            loaded_count = 0
            error_count = 0
            for lang_code in self.get_all_language_codes():
                if lang_code in self.custom_languages:
                    self.translations[lang_code] = self.custom_languages[lang_code].get("translations", {})
                    loaded_count += 1
                    continue
                lang_file = self.translations_dir / f"{lang_code}.json"
                if lang_file.exists():
                    try:
                        with open(lang_file, "r", encoding="utf-8") as f:
                            self.translations[lang_code] = json.load(f)
                        loaded_count += 1
                    except Exception as e:
                        print(f"[i18n] Fehler beim Laden {lang_code}: {e}")
                        self.translations[lang_code] = {}
                        error_count += 1
                else:
                    self.translations[lang_code] = {}
            print(f"[i18n] {loaded_count} Sprachen geladen" + (f" ({error_count} Fehler)" if error_count else ""))
        except Exception as e:
            print(f"[i18n] Fehler beim Laden der Übersetzungen: {e}")

    def set_language(self, lang_code: str) -> None:
        """Set the current language if valid."""
        if self._language_exists(lang_code):
            self.current_language = lang_code
            print(f"[i18n] Sprache geändert zu: {lang_code}")
        else:
            print(f"[i18n] Unbekannte Sprache: {lang_code}")

    def tr(self, key: str, default: Optional[str] = None) -> str:
        """Look up translation with priority: overrides -> current -> de -> en -> default."""
        # 1) User override
        try:
            override = self.override_service.get_override(self.current_language, key)
            if override:
                return override
        except Exception:
            pass
        # Helper to fetch nested keys
        def lookup(lang: str) -> Optional[str]:
            d = self.translations.get(lang, {})
            value: Any = d
            for part in key.split('.'):
                if isinstance(value, dict):
                    value = value.get(part)
                else:
                    return None
            return value if isinstance(value, str) else None
        # 2) Current language
        val = lookup(self.current_language)
        if val:
            return val
        # 3) Fallback German
        if self.current_language != "de":
            val = lookup("de")
            if val:
                return val
        # 4) Fallback English
        if self.current_language not in ("de", "en"):
            val = lookup("en")
            if val:
                return val
        # 5) Default
        return default if default is not None else key

    # --------------- Overrides API --------------------
    def save_user_override(self, lang_code: str, key: str, value: str) -> None:
        self.override_service.save_override(lang_code, key, value)

    def remove_user_override(self, lang_code: str, key: str) -> None:
        self.override_service.remove_override(lang_code, key)

    def get_user_override(self, lang_code: str, key: str) -> Optional[str]:
        return self.override_service.get_override(lang_code, key)

    def get_all_user_overrides(self, lang_code: str) -> Dict[str, str]:
        return self.override_service.get_all_overrides(lang_code)

    def get_override_count(self, lang_code: str) -> int:
        return self.override_service.get_override_count(lang_code)

    # --------------- Stats (minimal) ------------------
    def _get_from_lang_file(self, lang_code: str, key: str) -> Optional[str]:
        value: Any = self.translations.get(lang_code, {})
        for part in key.split('.'):
            if isinstance(value, dict):
                value = value.get(part)
            else:
                return None
        return value if isinstance(value, str) else None

    def get_translation_stats(self) -> Dict[str, Dict]:
        """Minimal stats: attempts to read translation_master.json and compute coverage."""
        stats: Dict[str, Dict] = {}
        master_file = self.translations_dir.parent / "translation_master.json"
        total_keys = 0
        master_entries: List[Tuple[str, Dict]] = []
        if not master_file.exists():
            return {}
        try:
            with open(master_file, "r", encoding="utf-8") as f:
                master_data = json.load(f)
            translations_section = master_data.get("translations", {})
            total_keys = len(translations_section)
            for mk, entry in translations_section.items():
                values = entry.get("values", {})
                master_entries.append((mk, values))
        except Exception as e:
            print(f"[i18n] Fehler beim Laden der Master-DB: {e}")
            return {}
        if total_keys == 0:
            return {}
        for lang_code in self.get_all_language_codes():
            overrides = self.get_all_user_overrides(lang_code)
            native = fallback_de = fallback_en = missing = 0
            for mk, values in master_entries:
                ov = overrides.get(mk)
                if isinstance(ov, str) and ov.strip():
                    native += 1
                    continue
                if isinstance(values.get(lang_code), str) and values[lang_code].strip():
                    native += 1
                    continue
                fv = self._get_from_lang_file(lang_code, mk)
                if isinstance(fv, str) and fv.strip():
                    native += 1
                    continue
                if lang_code != "de":
                    de_val = values.get("de") or self._get_from_lang_file("de", mk)
                    if isinstance(de_val, str) and de_val.strip():
                        fallback_de += 1
                        continue
                if lang_code not in ("de", "en"):
                    en_val = values.get("en") or self._get_from_lang_file("en", mk)
                    if isinstance(en_val, str) and en_val.strip():
                        fallback_en += 1
                        continue
                missing += 1
            total_coverage = native + fallback_de + fallback_en
            percent_native = (native / total_keys) * 100 if total_keys else 0
            percent_coverage = (total_coverage / total_keys) * 100 if total_keys else 0
            stats[lang_code] = {
                "total_keys": total_keys,
                "native": native,
                "fallback_de": fallback_de,
                "fallback_en": fallback_en,
                "missing": missing,
                "overrides": len(overrides),
                "percent_native": round(percent_native, 1),
                "percent_coverage": round(percent_coverage, 1),
                "translated_keys": total_coverage,
                "missing_keys": missing,
                "percent": round(percent_coverage, 1),
            }
        return stats

