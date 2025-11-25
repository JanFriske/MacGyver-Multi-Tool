# New LANGUAGE_GROUPS structure for i18n_service.py
# This will replace lines 19-300

LANGUAGE_GROUPS = {
    # ===== 6 GEOGRAFISCHE KATEGORIEN =====
    
    "🌍 Afrika": {
        "Nordafrika": {
            "ar": "🇪🇬 العربية (Arabisch)",
            "ar_DZ": "🇩🇿 العربية (Algerien)",
            "ar_EG": "🇪🇬 العربية (Ägypten)",
            "ar_LY": "🇱🇾 العربية (Libyen)",
            "ar_MA": "🇲🇦 العربية (Marokko)",
            "ar_TN": "🇹🇳 العربية (Tunesien)",
            "ar_SD": "🇸🇩 العربية (Sudan)",
        },
        "Subsahara West": {
            "fr": "🇫🇷 Français",
            "en": "🇬🇧 English",
            "ha": "🇳🇬 Hausa",
            "ig": "🇳🇬 Igbo",
            "yo": "🇳🇬 Yorùbá",
            "wo": "🇸🇳 Wolof",
            "sg": "🇨🇫 Sango",
        },
        "Subsahara Ost": {
            "sw": "🇹🇿 Kiswahili",
            "so": "🇸🇴 Somali",
            "am": "🇪🇹 አማርኛ (Amharisch)",
            "ti": "🇪🇷 ትግርኛ (Tigrinya)",
            "rw": "🇷🇼 Kinyarwanda",
            "mg": "🇲🇬 Malagasy",
        },
        "Subsahara Süd": {
            "af": "🇿🇦 Afrikaans",
            "zu": "🇿🇦 isiZulu",
            "xh": "🇿🇦 isiXhosa",
            "tn": "🇧🇼 Setswana",
            "nso": "🇿🇦 Sesotho sa Leboa",
            "st": "🇱🇸 Sesotho",
        },
        "Inseln": {
            "crs": "🇸🇨 Seychellenkreol",
            "pt": "🇵🇹 Português (Kap Verde, São Tomé)",
        },
    },
    
    "🌏 Asien": {
        "Westasien (Naher Osten)": {
            "he": "🇮🇱 עברית (Hebräisch)",
            "fa": "🇮🇷 فارسی (Persisch)",
            "prs": "🇦🇫 دری (Dari)",
            "ps": "🇦🇫 پښتو (Pashtu)",
            "ku": "🇮🇶 کوردی (Kurdisch)",
            "tr": "🇹🇷 Türkçe",
            "ur": "🇵🇰 اردو",
        },
        "Zentralasien": {
            "kk": "🇰🇿 Қазақша",
            "ky": "🇰🇬 Кыргызча (Kirgisisch)",
            "uz": "🇺🇿 O'zbek",
            "tk": "🇹🇲 Türkmençe",
            "tg": "🇹🇯 Тоҷикӣ (Tadschikisch)",
            "mn": "🇲🇳 Монгол",
        },
        "Südasien": {
            "hi": "🇮🇳 हिन्दी",
            "bn": "🇧🇩 বাংলা",
            "ur": "🇵🇰 اردو",
            "pa": "🇮🇳 ਪੰਜਾਬੀ (Punjabi)",
            "mr": "🇮🇳 मराठी (Marathi)",
            "gu": "🇮🇳 ગુજરાતી (Gujarati)",
            "ta": "🇮🇳 தமிழ் (Tamil)",
            "te": "🇮🇳 తెలుగు (Telugu)",
            "kn": "🇮🇳 ಕನ್ನಡ (Kannada)",
            "ml": "🇮🇳 മലയാളം (Malayalam)",
            "si": "🇱🇰 සිංහල (Singhalesisch)",
            "ne": "🇳🇵 नेपाली (Nepali)",
            "dz": "🇧🇹 རྫོང་ཁ (Dzongkha)",
            "as": "🇮🇳 অসমীয়া (Assamesisch)",
            "kok": "🇮🇳 कोंकणी (Konkani)",
            "or": "🇮🇳 ଓଡ଼ିଆ (Odia)",
        },
        "Südostasien": {
            "th": "🇹🇭 ไทย",
            "vi": "🇻🇳 Tiếng Việt",
            "id": "🇮🇩 Bahasa Indonesia",
            "ms": "🇲🇾 Bahasa Melayu",
            "fil": "🇵🇭 Filipino",
            "my": "🇲🇲 မြန်မာ (Birmanisch)",
            "km": "🇰🇭 ខ្មែរ (Khmer)",
            "lo": "🇱🇦 ລາວ (Laotisch)",
            "tet": "🇹🇱 Tetum",
        },
        "Ostasien": {
            "zh": "🇨🇳 中文",
            "zh-Hans": "🇨🇳 简体中文",
            "zh_Hant": "🇹🇼 繁體中文",
            "ja": "🇯🇵 日本語",
            "ko": "🇰🇷 한국어",
        },
    },
    
    "🌍 Europa": {
        "Deutsch-sprachig": {
            "de": "🇩🇪 Deutsch",
            "de_AT": "🇦🇹 Österreichisch",
            "de_CH": "🇨🇭 Schweizerdeutsch",
            "de_LI": "🇱🇮 Liechtenstein",
            "de_LU": "🇱🇺 Luxemburg",
            "lb": "🇱🇺 Lëtzebuergesch",
        },
        "Französisch-sprachig": {
            "fr": "🇫🇷 Français",
            "fr_BE": "🇧🇪 Français (Belgien)",
            "fr_CH": "🇨🇭 Français (Schweiz)",
            "fr_CA": "🇨🇦 Français (Québec)",
            "fr_LU": "🇱🇺 Français (Luxemburg)",
        },
        "Iberische Halbinsel": {
            "es": "🇪🇸 Español",
            "pt": "🇵🇹 Português",
            "ca": "🇪🇸 Català",
            "eu": "🇪🇸 Euskara",
            "gl": "🇪🇸 Galego",
            "ca_ES_valencia": "🇪🇸 Valencià",
        },
        "Italienisch": {
            "it": "🇮🇹 Italiano",
        },
        "Englisch-sprachig": {
            "en": "🇺🇸 English",
            "en_GB": "🇬🇧 English (UK)",
            "en_IE": "🇮🇪 English (Ireland)",
        },
        "Nordeuropa": {
            "sv": "🇸🇪 Svenska",
            "da": "🇩🇰 Dansk",
            "no": "🇳🇴 Norsk",
            "nb": "🇳🇴 Norsk Bokmål",
            "nn": "🇳🇴 Nynorsk",
            "fi": "🇫🇮 Suomi",
            "is": "🇮🇸 Íslenska",
        },
        "Osteuropa": {
            "ru": "🇷🇺 Русский",
            "pl": "🇵🇱 Polski",
            "uk": "🇺🇦 Українська",
            "cs": "🇨🇿 Čeština",
            "sk": "🇸🇰 Slovenčina",
            "hu": "🇭🇺 Magyar",
            "ro": "🇷🇴 Română",
            "bg": "🇧🇬 Български",
            "be": "🇧🇾 Беларуская",
            "lt": "🇱🇹 Lietuvių",
            "lv": "🇱🇻 Latviešu",
            "et": "🇪🇪 Eesti",
        },
        "Südeuropa / Balkan": {
            "hr": "🇭🇷 Hrvatski",
            "sr": "🇷🇸 Српски",
            "sl": "🇸🇮 Slovenščina",
            "bs": "🇧🇦 Bosanski",
            "mk": "🇲🇰 Македонски",
            "sq": "🇦🇱 Shqip",
            "el": "🇬🇷 Ελληνικά",
            "mt": "🇲🇹 Malti",
        },
        "Benelux": {
            "nl": "🇳🇱 Nederlands",
            "nl_BE": "🇧🇪 Vlaams",
        },
        "Keltische Sprachen": {
            "ga": "🇮🇪 Gaeilge",
            "cy": "🏴\u200d☠️ Cymraeg",
            "gd": "🏴\u200d☠️ Gàidhlig",
        },
        "Schweiz": {
            "de_CH": "🇨🇭 Schweizerdeutsch",
            "fr_CH": "🇨🇭 Français",
            "it": "🇨🇭 Italiano",
            "rm": "🇨🇭 Rumantsch",
        },
    },
    
    "🌎 Nordamerika": {
        "Nordamerika": {
            "en": "🇺🇸 English (USA)",
            "en_CA": "🇨🇦 English (Kanada)",
            "fr_CA": "🇨🇦 Français (Québec)",
            "es_MX": "🇲🇽 Español (Mexiko)",
        },
        "Mittelamerika": {
            "es": "🇪🇸 Español",
            "es_GT": "🇬🇹 Guatemala",
            "es_CR": "🇨🇷 Costa Rica",
            "es_PA": "🇵🇦 Panama",
        },
        "Karibik": {
            "ht": "🇭🇹 Kreyòl Ayisyen",
            "es_CU": "🇨🇺 Español (Kuba)",
            "es_DO": "🇩🇴 Español (Dom. Rep.)",
        },
    },
    
    "🌎 Südamerika": {
        "Spanisch-sprachig": {
            "es": "🇪🇸 Español",
            "es_AR": "🇦🇷 Argentinien",
            "es_CL": "🇨🇱 Chile",
            "es_CO": "🇨🇴 Kolumbien",
            "es_PE": "🇵🇪 Peru",
            "es_VE": "🇻🇪 Venezuela",
            "es_UY": "🇺🇾 Uruguay",
            "es_BO": "🇧🇴 Bolivien",
            "es_EC": "🇪🇨 Ecuador",
            "es_PY": "🇵🇾 Paraguay",
        },
        "Portugiesisch-sprachig": {
            "pt_BR": "🇧🇷 Português (Brasilien)",
        },
        "Indigene Sprachen": {
            "gn": "🇵🇾 Guaraní",
            "qu": "🇵🇪 Runasimi (Quechua)",
            "quz": "Qhichwa (Quechua Varianten)",
            "ay": "🇧🇴 Aymara",
        },
        "Andere": {
            "nl": "🇸🇷 Nederlands (Suriname)",
            "en": "🇬🇾 English (Guyana)",
        },
    },
    
    "🌊 Ozeanien": {
        "Australien & Neuseeland": {
            "en_AU": "🇦🇺 English (Australien)",
            "en_NZ": "🇳🇿 English (Neuseeland)",
            "mi": "🇳🇿 Te Reo Māori",
        },
        "Melanesien": {
            "fj": "🇫🇯 Na Vosa Vakaviti (Fidschi)",
            "hif": "🇫🇯 Fiji Hindi",
            "bi": "🇻🇺 Bislama",
            "tpi": "🇵🇬 Tok Pisin",
            "ho": "🇵🇬 Hiri Motu",
        },
        "Mikronesien": {
            "gil": "🇰🇮 Gilbertese (Kiribati)",
            "mh": "🇲🇭 Kajin M̧ajeļ (Marshallisch)",
            "pau": "🇵🇼 Tekoi ra Belau (Palauisch)",
        },
        "Polynesien": {
            "sm": "🇼🇸 Gagana Sāmoa",
            "to": "🇹🇴 Lea Fakatonga (Tongaisch)",
            "tvl": "🇹🇻 Te Ggana Tuuvalu",
            "na": "🇳🇷 Dorerin Naoero (Nauruisch)",
        },
    },
    
    # ===== SONDERKATEGORIEN =====
    
    "🏛️ Klassisch & Konstruiert": {
        "Klassisch": {
            "la": "🏛️ Latina (Latein)",
        },
        "Konstruiert": {
            "eo": "🏛️ Esperanto",
            "ia": "🏛️ Interlingua",
            "tlh": "🖖 tlhIngan Hol (Klingonisch)",  # MOVED HERE
        },
    },
    
    "📜 Historisch & Spezial": {
        "Historische Varianten": {
            "de_middlehigh": "🕰️ Mittelhochdeutsch",
            "en_old": "🕰️ Altenglisch",
        },
        "☠️ Pirate-Varianten": {  # MOVED HERE from various groups
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
        "Andere": {
            "yi": "🕍 ייִדיש (Jiddisch)",
            "sco": "🏴\u200d☠️ Scots",
        },
    },
    
    "🇩🇪 Deutsche Dialekte": {
        "Bairisch & Österreichisch": {
            "de_bavarian": "Bairisch",
            "de_AT_vienna": "Wienerisch",
            "de_AT_styria": "Steirisch",
            "de_AT_tyrol": "Tirolerisch",
        },
        "Alemannisch & Schwäbisch": {
            "de_swabian": "Schwäbisch",
            "de_alemannic": "Alemannisch",
            "de_badisch": "Badisch",
            "de_allgaeu": "Allgäuerisch",
        },
        "Mitteldeutsch": {
            "de_saxon": "Sächsisch",
            "de_thuringian": "Thüringisch",
            "de_hessian": "Hessisch",
            "de_franconian": "Fränkisch",
        },
        "Niederdeutsch": {
            "de_lowgerman": "Plattdeutsch",
            "de_cologne": "Kölsch",
            "de_berlin": "Berlinerisch",
            "de_ruhr": "Ruhrdeutsch",
        },
        "Historische & Diaspora": {
            "de_middlehigh": "🕰️ Mittelhochdeutsch",
            "de_volga": "Wolgadeutsch 🔴",
            "de_sudeten": "Sudetendeutsch 💀",
            "de_silesian": "Schlesisch 💀",
        },
    },
}
