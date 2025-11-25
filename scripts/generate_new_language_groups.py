"""
Generate new LANGUAGE_GROUPS with geographic structure
Based on UN countries (195 states) organized by 6 continents
"""

# This will be inserted into i18n_service.py

LANGUAGE_GROUPS = {
    # ===== GEOGRAFISCHE KATEGORIEN (6 Kontinente) =====
    
    "🌍 Afrika": {
        "Nordafrika": {
            "ar": "العربية (Arabisch)",
            "ar_DZ": "العربية (Algerien)",
            "ar_EG": "العربية (Ägypten)",
            "ar_LY": "العربية (Libyen)",
            "ar_MA": "العربية (Marokko)",
            "ar_TN": "العربية (Tunesien)",
            "ar_SD": "العربية (Sudan)",
        },
        "Subsahara West": {
            "fr": "Français (Französisch)",
            "en": "English",
            "ha": "Hausa",
            "ig": "Igbo",
            "yo": "Yoruba",
            "wo": "Wolof",
            "sg": "Sango",
        },
        "Subsahara Ost": {
            "sw": "Kiswahili (Swahili)",
            "so": "Somali",
            "am": "አማርኛ (Amharisch)",
            "ti": "ትግርኛ (Tigrinya)",
            "rw": "Kinyarwanda",
            "mg": "Malagasy",
        },
        "Subsahara Süd": {
            "af": "Afrikaans",
            "zu": "isiZulu",
            "xh": "isiXhosa",
            "tn": "Setswana",
            "nso": "Sepedi (Nord-Sotho)",
            "st": "Sesotho",
        },
        "Inseln": {
            "crs": "Seychellenkreol",
            "pt": "Português (Kap Verde, São Tomé)",
        },
    },
    
    "🌏 Asien": {
        "Westasien (Naher Osten)": {
            "ar": "العربية (Arabisch)",
            "he": "עברית (Hebräisch)",
            "fa": "فارسی (Persisch/Farsi)",
            "prs": "دری (Dari - Afghanistan)",
            "ps": "پښتو (Pashtu)",
            "ku": "Kurdî (Kurdisch)",
            "tr": "Türkçe (Türkisch)",
        },
        "Zentralasien": {
            "kk": "Қазақша (Kasachisch)",
            "ky": "Кыргызча (Kirgisisch)",
            "uz": "Oʻzbekcha (Usbekisch)",
            "tk": "Türkmençe (Turkmenisch)",
            "tg": "Тоҷикӣ (Tadschikisch)",
            "mn": "Монгол (Mongolisch)",
        },
        "Südasien": {
            "hi": "हिन्दी (Hindi)",
            "bn": "বাংলা (Bengalisch)",
            "ur": "اردو (Urdu)",
            "pa": "ਪੰਜਾਬੀ (Punjabi)",
            "mr": "मराठी (Marathi)",
            "gu": "ગુજરાતી (Gujarati)",
            "ta": "தமிழ் (Tamil)",
            "te": "తెలుగు (Telugu)",
            "kn": "ಕನ್ನಡ (Kannada)",
            "ml": "മലയാളം (Malayalam)",
            "si": "සිංහල (Singhalesisch)",
            "ne": "नेपाली (Nepali)",
            "dz": "རྫོང་ཁ (Dzongkha - Bhutan)",
        },
        "Südostasien": {
            "th": "ไทย (Thailändisch)",
            "vi": "Tiếng Việt (Vietnamesisch)",
            "id": "Bahasa Indonesia (Indonesisch)",
            "ms": "Bahasa Melayu (Malaiisch)",
            "fil": "Filipino/Tagalog",
            "my": "မြန်မာ (Birmanisch)",
            "km": "ខ្មែរ (Khmer)",
            "lo": "ລາວ (Laotisch)",
            "tet": "Tetum (Timor-Leste)",
        },
        "Ostasien": {
            "zh": "中文 (Chinesisch)",
            "zh_Hans": "简体中文 (Vereinfacht)",
            "zh_Hant": "繁體中文 (Traditionell)",
            "ja": "日本語 (Japanisch)",
            "ko": "한국어 (Koreanisch)",
        },
    },
    
    "🌍 Europa": {
        "Westeuropa": {
            "de": "Deutsch",
            "de_AT": "🇦🇹 Österreichisches Deutsch",
            "de_CH": "🇨🇭 Schweizer Hochdeutsch",
            "de_LI": "🇱🇮 Liechtenstein",
            "de_LU": "🇱🇺 Luxemburg",
            "fr": "Français (Französisch)",
            "fr_BE": "🇧🇪 Français (Belgien)",
            "fr_CH": "🇨🇭 Français (Schweiz)",
            "fr_LU": "🇱🇺 Français (Luxemburg)",
            "nl": "Nederlands (Niederländisch)",
            "nl_BE": "🇧🇪 Vlaams (Flämisch)",
            "lb": "Lëtzebuergesch (Luxemburgisch)",
            "rm": "Rumantsch (Rätoromanisch)",
        },
        "Nordeuropa": {
            "en_GB": "🇬🇧 English (UK)",
            "en": "English (US/International)",
            "sv": "Svenska (Schwedisch)",
            "da": "Dansk (Dänisch)",
            "no": "Norsk",
            "nb": "Norsk Bokmål",
            "nn": "Norsk Nynorsk",
            "fi": "Suomi (Finnisch)",
            "is": "Íslenska (Isländisch)",
        },
        "Osteuropa": {
            "ru": "Русский (Russisch)",
            "pl": "Polski (Polnisch)",
            "uk": "Українська (Ukrainisch)",
            "cs": "Čeština (Tschechisch)",
            "sk": "Slovenčina (Slowakisch)",
            "hu": "Magyar (Ungarisch)",
            "ro": "Română (Rumänisch)",
            "bg": "Български (Bulgarisch)",
            "be": "Беларуская (Belarussisch)",
            "lt": "Lietuvių (Litauisch)",
            "lv": "Latviešu (Lettisch)",
            "et": "Eesti (Estnisch)",
        },
        "Südeuropa": {
            "it": "Italiano (Italienisch)",
            "es": "Español (Spanisch)",
            "pt": "Português (Portugiesisch)",
            "el": "Ελληνικά (Griechisch)",
            "hr": "Hrvatski (Kroatisch)",
            "sr": "Српски (Serbisch)",
            "sl": "Slovenščina (Slowenisch)",
            "bs": "Bosanski (Bosnisch)",
            "mk": "Македонски (Mazedonisch)",
            "sq": "Shqip (Albanisch)",
            "mt": "Malti (Maltesisch)",
            "ca": "Català (Katalanisch)",
            "eu": "Euskara (Baskisch)",
            "gl": "Galego (Galicisch)",
        },
        "Keltische Sprachen": {
            "ga": "Gaeilge (Irisch)",
            "cy": "Cymraeg (Walisisch)",
            "gd": "Gàidhlig (Schottisch-Gälisch)",
        },
    },
    
    "🌎 Nordamerika": {
        "Nordamerika": {
            "en": "English (USA)",
            "en_CA": "🇨🇦 English (Kanada)",
            "fr_CA": "🇨🇦 Français (Québec)",
            "es_MX": "🇲🇽 Español (Mexiko)",
        },
        "Mittelamerika": {
            "es": "Español",
            "es_GT": "🇬🇹 Guatemala",
            "es_CR": "🇨🇷 Costa Rica",
            "es_PA": "🇵🇦 Panama",
        },
        "Karibik": {
            "ht": "Kreyòl Ayisyen (Haitianisch-Kreolisch)",
            "es_CU": "🇨🇺 Español (Kuba)",
            "es_DO": "🇩🇴 Español (Dominikanische Rep.)",
        },
    },
    
    "🌎 Südamerika": {
        "Spanisch-sprachig": {
            "es": "Español",
            "es_AR": "🇦🇷 Argentinien",
            "es_CL": "🇨🇱 Chile",
            "es_CO": "🇨🇴 Kolumbien",
            "es_PE": "🇵🇪 Peru",
            "es_VE": "🇻🇪 Venezuela",
            "es_UY": "🇺🇾 Uruguay",
        },
        "Portugiesisch-sprachig": {
            "pt_BR": "🇧🇷 Português (Brasilien)",
            "pt": "Português (Portugal)",
        },
        "Indigene Sprachen": {
            "gn": "Guaraní (Paraguay, Bolivien)",
            "qu": "Runasimi (Quechua)",
            "quz": "Qhichwa (Quechua - Varianten)",
            "ay": "Aymara (Bolivien, Peru)",
        },
        "Andere": {
            "nl": "Nederlands (Suriname)",
            "en": "English (Guyana)",
        },
    },
    
    "🌊 Ozeanien": {
        "Australien & Neuseeland": {
            "en": "English",
            "en_AU": "🇦🇺 English (Australien)",
            "en_NZ": "🇳🇿 English (Neuseeland)",
            "mi": "Te Reo Māori",
        },
        "Melanesien": {
            "fj": "Na Vosa Vakaviti (Fidschi)",
            "hif": "Fiji Hindi",
            "bi": "Bislama (Vanuatu)",
            "tpi": "Tok Pisin (Papua-Neuguinea)",
            "ho": "Hiri Motu (Papua-Neuguinea)",
        },
        "Mikronesien": {
            "gil": "Gilbertese (Kiribati)",
            "mh": "Kajin M̧ajeļ (Marshallisch)",
            "pau": "Tekoi ra Belau (Palauisch)",
        },
        "Polynesien": {
            "sm": "Gagana Sāmoa (Samoanisch)",
            "to": "Lea Fakatonga (Tongaisch)",
            "tvl": "Te Ggana Tuuvalu (Tuvaluisch)",
            "na": "Dorerin Naoero (Nauruisch)",
        },
    },
    
    # ===== SONDERKATEGORIEN =====
    
    "🏛️ Klassisch & Konstruiert": {
        "": {
            "la": "Latina (Latein)",
            "eo": "Esperanto",
            "ia": "Interlingua",
            "tlh": "tlhIngan Hol (Klingonisch)",  # MOVED from Historisch
        },
    },
    
    "📜 Historisch & Spezial": {
        "Historische Varianten": {
            "de_middlehigh": "🕰️ Mittelhochdeutsch (1050-1350)",
            "en_old": "🕰️ Altenglisch (450-1150)",
        },
        "☠️ Pirate-Varianten": {  # MOVED HERE
            "en_pirate": "☠️ Pirate English",
            "de_pirate": "☠️ Piraten-Deutsch",
            "fr_pirate": "☠️ Français Pirate",
            "es_pirate": "☠️ Español Pirata",
            "pt_pirate": "☠️ Português Pirata",
            "sco_pirate": "☠️ Scots Pirate",
            "tlh_pirate": "☠️ Klingon Pirate",
            "fr_CA_pirate": "☠️ Québécois Pirate",
            "it_pirate": "☠️ Italiano Pirata",
            "nl_pirate": "☠️ Nederlands Piraat",
            "ru_pirate": "☠️ Русский Пират",
            "pl_pirate": "☠️ Polski Pirat",
            "tr_pirate": "☠️ Türk Korsan",
            "ja_pirate": "☠️ 海賊日本語",
            "zh_pirate": "☠️ 海盜中文",
        },
    },
    
    "🇩🇪 Deutsche Dialekte": {
        "Bairisch & Österreichisch": {
            "de_bavarian": "Bairisch",
            "de_AT_vienna": "🇦🇹 Wienerisch",
            "de_AT_styria": "🇦🇹 Steirisch",
            "de_AT_tyrol": "🇦🇹 Tirolerisch",
        },
        "Alemannisch & Schwäbisch": {
            "de_swabian": "Schwäbisch",
            "de_alemannic": "Alemannisch",
            "de_badisch": "Badisch",
        },
        "Mitteldeutsch": {
            "de_saxon": "Sächsisch",
            "de_thuringian": "Thüringisch",
            "de_hessian": "Hessisch",
        },
        "Niederdeutsch": {
            "de_plattdeutsch": "Plattdeutsch/Niederdeutsch",
            "de_cologne": "Kölsch",
            "de_berlin": "Berlinerisch",
            "de_hamburg": "Hamburger Platt",
        },
        # ... weitere deutsche Dialekte
    },
}

print("✅ New LANGUAGE_GROUPS structure generated")
print(f"📊 Total categories: {len(LANGUAGE_GROUPS)}")
