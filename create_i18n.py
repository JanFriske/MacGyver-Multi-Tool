"""
Script to create i18n_service.py with geographic categories
"""

content = '''"""
i18n Service - Central translation management
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from core.services.user_override_service import get_override_service


class I18nService:
    """Central service for internationalization."""

    # ========================================
    # 7 GEOGRAFISCHE KATEGORIEN (200+ Sprachen)
    # Struktur: Kontinent -> Sprache -> Dialekte/Varianten
    # ========================================
    LANGUAGE_GROUPS = {
        # ================================================
        # 🌍 AFRIKA
        # ================================================
        "🌍 Afrika": {
            "🇿🇦 Afrikaans": {
                "Standard": {"af": "🇿🇦 Afrikaans"},
            },
            "🇪🇹 አማርኛ (Amharisch)": {
                "Standard": {"am": "🇪🇹 አማርኛ"},
            },
            "🇳🇬 Hausa": {
                "Standard": {"ha_Latn": "🇳🇬 Hausa", "ha": "🇳🇬 Hausa (Latin)"},
            },
            "🇳🇬 Igbo": {
                "Standard": {"ig": "🇳🇬 Igbo"},
            },
            "🇷🇼 Kinyarwanda": {
                "Standard": {"rw": "🇷🇼 Kinyarwanda"},
            },
            "🇰🇪 Kiswahili": {
                "Standard": {"sw": "🇰🇪 Kiswahili"},
            },
            "🇿🇦 Sesotho sa Leboa": {
                "Standard": {"nso": "🇿🇦 Sesotho sa Leboa"},
            },
            "🇧🇼 Setswana": {
                "Standard": {"tn": "🇧🇼 Setswana"},
            },
            "🇸🇴 Somali": {
                "Standard": {"so": "🇸🇴 Somali"},
            },
            "🇪🇹 ትግርኛ (Tigrinya)": {
                "Standard": {"ti": "🇪🇹 ትግርኛ"},
            },
            "🇸🇳 Wolof": {
                "Standard": {"wo": "🇸🇳 Wolof"},
            },
            "🇿🇦 isiXhosa": {
                "Standard": {"xh": "🇿🇦 isiXhosa"},
            },
            "🇳🇬 Yorùbá": {
                "Standard": {"yo": "🇳🇬 Yorùbá"},
            },
            "🇿🇦 isiZulu": {
                "Standard": {"zu": "🇿🇦 isiZulu"},
            },
        },

        # ================================================
        # 🌏 ASIEN
        # ================================================
        "🌏 Asien": {
            "🇸🇦 العربية (Arabisch)": {
                "Standard": {"ar": "🇸🇦 العربية"},
            },
            "🇮🇳 অসমীয়া (Assamesisch)": {
                "Standard": {"as": "🇮🇳 অসমীয়া"},
            },
            "🇦🇿 Azərbaycan": {
                "Standard": {"az_Latn": "🇦🇿 Azərbaycan", "az": "🇦🇿 Azərbaycan (Latin)"},
            },
            "🇮🇳 বাংলা (Bengali)": {
                "Standard": {"bn": "🇮🇳 বাংলা"},
            },
            "🇨🇳 中文 (Chinesisch)": {
                "Standard": {
                    "zh": "🇨🇳 中文",
                    "zh-Hans": "🇨🇳 中文(简体)",
                    "zh_Hant": "🇹🇼 中文(繁體)",
                },
                "🏴‍☠️ Pirate": {"zh_pirate": "🏴‍☠️ Chinese Pirate"},
            },
            "🇧🇹 Dzongkha": {
                "Standard": {"dz": "🇧🇹 Dzongkha"},
            },
            "🇵🇭 Filipino": {
                "Standard": {"fil": "🇵🇭 Filipino"},
            },
            "🇮🇳 ગુજરાતી (Gujarati)": {
                "Standard": {"gu": "🇮🇳 ગુજરાતી"},
            },
            "🇮🇱 עברית (Hebräisch)": {
                "Standard": {"he": "🇮🇱 עברית"},
            },
            "🇮🇳 हिन्दी (Hindi)": {
                "Standard": {"hi": "🇮🇳 हिन्दी"},
            },
            "🇦🇲 Հայերեն (Armenisch)": {
                "Standard": {"hy": "🇦🇲 Հայերեն"},
            },
            "🇮🇩 Bahasa Indonesia": {
                "Standard": {"id": "🇮🇩 Bahasa Indonesia"},
            },
            "🇯🇵 日本語 (Japanisch)": {
                "Standard": {"ja": "🇯🇵 日本語"},
                "🏴‍☠️ Pirate": {"ja_pirate": "🏴‍☠️ Japanese Pirate"},
            },
            "🇬🇪 ქართული (Georgisch)": {
                "Standard": {"ka": "🇬🇪 ქართული"},
            },
            "🇰🇿 Қазақ тілі (Kasachisch)": {
                "Standard": {"kk": "🇰🇿 Қазақ тілі"},
            },
            "🇰🇭 ខ្មែរ (Khmer)": {
                "Standard": {"km": "🇰🇭 ខ្មែរ"},
            },
            "🇮🇳 ಕನ್ನಡ (Kannada)": {
                "Standard": {"kn": "🇮🇳 ಕನ್ನಡ"},
            },
            "🇮🇳 कोंकणी (Konkani)": {
                "Standard": {"kok": "🇮🇳 कोंकणी"},
            },
            "🇰🇷 한국어 (Koreanisch)": {
                "Standard": {"ko": "🇰🇷 한국어"},
            },
            "🇮🇶 کوردی (Kurdisch)": {
                "Standard": {"ku_Arab": "🇮🇶 کوردی", "ku": "🇮🇶 کوردی (Arabic)"},
            },
            "🇱🇦 ລາວ (Laotisch)": {
                "Standard": {"lo": "🇱🇦 ລາວ"},
            },
            "🇮🇳 മലയാളം (Malayalam)": {
                "Standard": {"ml": "🇮🇳 മലയാളം"},
            },
            "🇲🇳 Монгол (Mongolisch)": {
                "Standard": {"mn_Cyrl": "🇲🇳 Монгол", "mn": "🇲🇳 Монгол (Cyrillic)"},
            },
            "🇮🇳 मराठी (Marathi)": {
                "Standard": {"mr": "🇮🇳 मराठी"},
            },
            "🇲🇾 Bahasa Melayu": {
                "Standard": {"ms": "🇲🇾 Bahasa Melayu"},
            },
            "🇳🇵 नेपाली (Nepali)": {
                "Standard": {"ne": "🇳🇵 नेपाली"},
            },
            "🇮🇳 ଓଡ଼ିଆ (Odia)": {
                "Standard": {"or": "🇮🇳 ଓଡ଼ିଆ"},
            },
            "🇮🇳 ਪੰਜਾਬੀ (Punjabi)": {
                "Standard": {"pa": "🇮🇳 ਪੰਜਾਬੀ"},
            },
            "🇮🇷 فارسی (Persisch)": {
                "Standard": {"fa": "🇮🇷 فارسی", "fa_AF": "🇦🇫 دری", "prs": "🇦🇫 دری"},
            },
            "🇦🇫 پښتو (Paschtu)": {
                "Standard": {"ps": "🇦🇫 پښتو"},
            },
            "🇵🇰 سنڌي (Sindhi)": {
                "Standard": {"sd_Arab": "🇵🇰 سنڌي", "sd": "🇵🇰 سنڌي (Arabic)"},
            },
            "🇱🇰 සිංහල (Singhalesisch)": {
                "Standard": {"si": "🇱🇰 සිංහල"},
            },
            "🇮🇳 தமிழ் (Tamil)": {
                "Standard": {"ta": "🇮🇳 தமிழ்"},
            },
            "🇮🇳 తెలుగు (Telugu)": {
                "Standard": {"te": "🇮🇳 తెలుగు"},
            },
            "🇹🇯 Тоҷикӣ (Tadschikisch)": {
                "Standard": {"tg_Cyrl": "🇹🇯 Тоҷикӣ", "tg": "🇹🇯 Тоҷикӣ (Cyrillic)"},
            },
            "🇹🇭 ภาษาไทย (Thai)": {
                "Standard": {"th": "🇹🇭 ภาษาไทย"},
            },
            "🇹🇲 Türkmen": {
                "Standard": {"tk": "🇹🇲 Türkmen dili"},
            },
            "🇹🇷 Türkçe": {
                "Standard": {"tr": "🇹🇷 Türkçe"},
                "🏴‍☠️ Pirate": {"tr_pirate": "🏴‍☠️ Turkish Pirate"},
            },
            "🇨🇳 ئۇيغۇرچە (Uigurisch)": {
                "Standard": {"ug": "🇨🇳 ئۇيغۇرچە"},
            },
            "🇵🇰 اردو (Urdu)": {
                "Standard": {"ur": "🇵🇰 اردو"},
            },
            "🇺🇿 O'zbek (Usbekisch)": {
                "Standard": {"uz_Latn": "🇺🇿 O'zbek", "uz": "🇺🇿 O'zbek (Latin)"},
            },
            "🇻🇳 Tiếng Việt": {
                "Standard": {"vi": "🇻🇳 Tiếng Việt"},
            },
        },

        # ================================================
        # 🌎 EUROPA
        # ================================================
        "🌎 Europa": {
            "🇦🇱 Shqip (Albanisch)": {
                "Standard": {"sq": "🇦🇱 Shqip"},
            },
            "🇧🇾 Беларуская (Weißrussisch)": {
                "Standard": {"be": "🇧🇾 Беларуская"},
            },
            "🇧🇦 Bosanski": {
                "Standard": {"bs": "🇧🇦 Bosanski", "bs_Latn": "🇧🇦 Bosanski (Latin)"},
            },
            "🇧🇬 Български (Bulgarisch)": {
                "Standard": {"bg": "🇧🇬 Български"},
            },
            "🇪🇸 Català (Katalanisch)": {
                "Standard": {"ca": "🇪🇸 Català", "ca_ES_valencia": "🇪🇸 Valencià"},
            },
            "🇨🇿 Čeština (Tschechisch)": {
                "Standard": {"cs": "🇨🇿 Čeština"},
            },
            "🇩🇰 Dansk (Dänisch)": {
                "Standard": {"da": "🇩🇰 Dansk"},
            },
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
            "🇬🇷 Ελληνικά (Griechisch)": {
                "Standard": {"el": "🇬🇷 Ελληνικά"},
            },
            "🇬🇧 English": {
                "Standard": {"en": "🇬🇧 English", "en_GB": "🇬🇧 English (UK)"},
                "🏴‍☠️ Pirate": {"en_pirate": "🏴‍☠️ Pirate English"},
            },
            "🇪🇪 Eesti (Estnisch)": {
                "Standard": {"et": "🇪🇪 Eesti"},
            },
            "🇪🇸 Euskara (Baskisch)": {
                "Standard": {"eu": "🇪🇸 Euskara"},
            },
            "🇫🇮 Suomi (Finnisch)": {
                "Standard": {"fi": "🇫🇮 Suomi"},
            },
            "🇫🇷 Français": {
                "Standard": {"fr": "🇫🇷 Français", "fr_CA": "🇨🇦 Français (Canada)"},
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
            "🇳🇱 Frysk (Friesisch)": {
                "Standard": {"fy": "🇳🇱 Frysk"},
            },
            "🇮🇪 Gaeilge (Irisch)": {
                "Standard": {"ga": "🇮🇪 Gaeilge"},
            },
            "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Gàidhlig (Schottisch-Gälisch)": {
                "Standard": {"gd": "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Gàidhlig"},
            },
            "🇪🇸 Galego (Galizisch)": {
                "Standard": {"gl": "🇪🇸 Galego"},
            },
            "🇭🇷 Hrvatski (Kroatisch)": {
                "Standard": {"hr": "🇭🇷 Hrvatski"},
            },
            "🇭🇺 Magyar (Ungarisch)": {
                "Standard": {"hu": "🇭🇺 Magyar"},
            },
            "🇮🇸 Íslenska (Isländisch)": {
                "Standard": {"is": "🇮🇸 Íslenska"},
            },
            "🇮🇹 Italiano": {
                "Standard": {"it": "🇮🇹 Italiano", "vec": "🇮🇹 Venetian"},
                "🏴‍☠️ Pirate": {"it_pirate": "🏴‍☠️ Italiano Pirate"},
            },
            "🇱🇻 Latviešu (Lettisch)": {
                "Standard": {"lv": "🇱🇻 Latviešu"},
            },
            "🇱🇹 Lietuvių (Litauisch)": {
                "Standard": {"lt": "🇱🇹 Lietuvių"},
            },
            "🇱🇺 Lëtzebuergesch": {
                "Standard": {"lb": "🇱🇺 Lëtzebuergesch"},
            },
            "🇳🇱 Limburgs": {
                "Standard": {"li": "🇳🇱 Limburgs"},
            },
            "🇲🇰 Македонски (Mazedonisch)": {
                "Standard": {"mk": "🇲🇰 Македонски"},
            },
            "🇲🇹 Malti (Maltesisch)": {
                "Standard": {"mt": "🇲🇹 Malti"},
            },
            "🇳🇱 Nederlands": {
                "Standard": {"nl": "🇳🇱 Nederlands"},
                "🏴‍☠️ Pirate": {"nl_pirate": "🏴‍☠️ Nederlands Pirate"},
            },
            "🇳🇴 Norsk": {
                "Standard": {"nb": "🇳🇴 Norsk (Bokmål)", "nn": "🇳🇴 Nynorsk"},
            },
            "🇵🇱 Polski (Polnisch)": {
                "Standard": {"pl": "🇵🇱 Polski"},
                "Dialekte": {
                    "csb": "🇵🇱 Kashubisch",
                    "szl": "🇵🇱 Schlesisch (Polnisch)",
                },
                "🏴‍☠️ Pirate": {"pl_pirate": "🏴‍☠️ Polish Pirate"},
            },
            "🇵🇹 Português": {
                "Standard": {
                    "pt": "🇵🇹 Português",
                    "pt_PT": "🇵🇹 Português (Portugal)",
                    "pt_BR": "🇧🇷 Português (Brasil)",
                },
                "🏴‍☠️ Pirate": {"pt_pirate": "🏴‍☠️ Português Pirate"},
            },
            "🇷🇴 Română (Rumänisch)": {
                "Standard": {"ro": "🇷🇴 Română"},
            },
            "🇷🇺 Русский (Russisch)": {
                "Standard": {"ru": "🇷🇺 Русский"},
                "🏴‍☠️ Pirate": {"ru_pirate": "🏴‍☠️ Russian Pirate"},
            },
            "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scots": {
                "Standard": {"sco": "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scots"},
                "🏴‍☠️ Pirate": {"sco_pirate": "🏴‍☠️ Scots Pirate"},
            },
            "🇷🇸 Српски (Serbisch)": {
                "Standard": {
                    "sr": "🇷🇸 Српски",
                    "sr_Cyrl": "🇷🇸 Српски (Ћирилица)",
                    "sr_Latn": "🇷🇸 Srpski (Latinica)",
                },
            },
            "🇸🇰 Slovenčina (Slowakisch)": {
                "Standard": {"sk": "🇸🇰 Slovenčina"},
            },
            "🇸🇮 Slovenščina (Slowenisch)": {
                "Standard": {"sl": "🇸🇮 Slovenščina"},
            },
            "🇪🇸 Español": {
                "Standard": {"es": "🇪🇸 Español", "es_MX": "🇲🇽 Español (México)"},
                "Dialekte": {"es_andalucia": "🇪🇸 Andalusisch"},
                "🏴‍☠️ Pirate": {"es_pirate": "🏴‍☠️ Español Pirate"},
            },
            "🇸🇪 Svenska (Schwedisch)": {
                "Standard": {"sv": "🇸🇪 Svenska"},
            },
            "🇷🇺 Татар (Tatarisch)": {
                "Standard": {"tt": "🇷🇺 Татар"},
            },
            "🇺🇦 Українська (Ukrainisch)": {
                "Standard": {"uk": "🇺🇦 Українська"},
            },
            "🏴󠁧󠁢󠁷󠁬󠁳󠁿 Cymraeg (Walisisch)": {
                "Standard": {"cy": "🏴󠁧󠁢󠁷󠁬󠁳󠁿 Cymraeg"},
            },
        },

        # ================================================
        # 🌎 NORDAMERIKA
        # ================================================
        "🌎 Nordamerika": {
            "🇺🇸 English (USA)": {
                "Standard": {"en": "🇺🇸 English"},
                "🏴‍☠️ Pirate": {"en_pirate": "🏴‍☠️ Pirate English"},
            },
            "🇨🇦 Français (Canada)": {
                "Standard": {"fr_CA": "🇨🇦 Français"},
                "🏴‍☠️ Pirate": {"fr_CA_pirate": "🏴‍☠️ Québécois Pirate"},
            },
            "🇲🇽 Español (México)": {
                "Standard": {"es_MX": "🇲🇽 Español"},
            },
            "🇺🇸 ᏣᎳᎩ (Cherokee)": {
                "Standard": {"chr": "🇺🇸 ᏣᎳᎩ"},
            },
            "🇭🇹 Kreyòl Ayisyen": {
                "Standard": {"ht": "🇭🇹 Haitian Creole"},
            },
        },

        # ================================================
        # 🌎 SÜDAMERIKA
        # ================================================
        "🌎 Südamerika": {
            "🇧🇷 Português (Brasil)": {
                "Standard": {"pt_BR": "🇧🇷 Português"},
                "🏴‍☠️ Pirate": {"pt_pirate": "🏴‍☠️ Português Pirate"},
            },
            "🇦🇷 Español": {
                "Standard": {"es": "🇦🇷 Español"},
            },
            "🇧🇴 Aymara": {
                "Standard": {"ay": "🇧🇴 Aymara"},
            },
            "🇵🇾 Guaraní": {
                "Standard": {"gn": "🇵🇾 Guaraní"},
            },
            "🇵🇪 Runasimi (Quechua)": {
                "Standard": {"quz": "🇵🇪 Runasimi"},
            },
        },

        # ================================================
        # 🌊 OZEANIEN
        # ================================================
        "🌊 Ozeanien": {
            "🇻🇺 Bislama": {
                "Standard": {"bi": "🇻🇺 Bislama"},
            },
            "🇫🇯 Fijian": {
                "Standard": {"fj": "🇫🇯 Fijian"},
            },
            "🇫🇯 Fiji Hindi": {
                "Standard": {"hif": "🇫🇯 Fiji Hindi"},
            },
            "🇰🇮 Gilbertese": {
                "Standard": {"gil": "🇰🇮 Gilbertese"},
            },
            "🇵🇬 Hiri Motu": {
                "Standard": {"ho": "🇵🇬 Hiri Motu"},
            },
            "🇲🇬 Malagasy": {
                "Standard": {"mg": "🇲🇬 Malagasy"},
            },
            "🇳🇿 Te reo Māori": {
                "Standard": {"mi": "🇳🇿 Te reo Māori"},
            },
            "🇲🇭 Marshallese": {
                "Standard": {"mh": "🇲🇭 Marshallese"},
            },
            "🇳🇷 Nauru": {
                "Standard": {"na": "🇳🇷 Nauru"},
            },
            "🇵🇼 Palauan": {
                "Standard": {"pau": "
