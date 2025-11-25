"""
Regenerate i18n/flags.json with a clean, complete, and valid mapping.
"""
import json
from pathlib import Path

flags_map = {
    # Europa
    "de": "de", "de_at": "at", "de_ch": "ch", "de_luxembourg": "lu",
    "de_transylvania": "ro", "de_banat": "ro", "de_sathmar": "ro",
    "de_southtyrol": "it", "de_FR_alsace": "fr", "de_volga": "ru",
    "de_middlehigh": "de", "gmh": "de", "ang": "gb", # Historical
    "en": "us", "en_GB": "gb", "en_US": "us",
    "fr": "fr", "fr_CA": "ca",
    "es": "es", "es_MX": "mx",
    "it": "it", "nl": "nl", "ru": "ru", "ro": "ro", "pl": "pl",
    "pt": "pt", "pt_BR": "br", "pt_PT": "pt",
    "sv": "se", "da": "dk", "no": "no", "nb": "no", "nn": "no",
    "fi": "fi", "cs": "cz", "hu": "hu", "sk": "sk", "sl": "si",
    "hr": "hr", "bg": "bg", "el": "gr", "tr": "tr",
    "uk": "ua", "be": "by", "sr": "rs", "sr_Cyrl": "rs", "sr_Latn": "rs",
    "bs": "ba", "bs_Latn": "ba", "mk": "mk", "sq": "al", "mt": "mt",
    "is": "is", "ca": "es", "ca_ES_valencia": "es", "eu": "es", "gl": "es",
    "fy": "nl", "lb": "lu", "co": "fr", "li": "nl", "csb": "pl",
    
    # Asien
    "ja": "jp", "zh": "cn", "zh-Hans": "cn", "zh_Hant": "tw", "ko": "kr",
    "ar": "sa", "he": "il", "yi": "il", "yi_latn": "il",
    "hi": "in", "bn": "bd", "pa": "in", "gu": "in", "ta": "in",
    "te": "in", "kn": "in", "ml": "in", "mr": "in", "ur": "pk",
    "fa": "ir", "fa_AF": "af", "prs": "af",
    "th": "th", "vi": "vn", "id": "id", "ms": "my", "fil": "ph",
    "km": "kh", "lo": "la", "my": "mm", "ka": "ge", "hy": "am",
    "az": "az", "az_Latn": "az", "kk": "kz", "uz": "uz", "uz_Latn": "uz",
    "tg": "tj", "tg_Cyrl": "tj", "tk": "tm", "ky": "kg", "mn": "mn",
    "ne": "np", "si": "lk", "as": "in", "kok": "in", "or": "in",
    "sd": "pk", "sd_Arab": "pk", "tt": "ru", "ug": "cn",
    
    # Afrika
    "sw": "ke", "am": "et", "ti": "er", "so": "so",
    "af": "za", "zu": "za", "xh": "za", "nso": "za", "tn": "bw",
    "st": "ls", "ss": "sz", "rw": "rw", "mg": "mg",
    "yo": "ng", "ig": "ng", "ha": "ng", "ha_Latn": "ng",
    "wo": "sn", "sg": "cf", "crs": "sc",
    
    # Amerika / Ozeanien / Sonstige
    "ht": "ht", "ay": "bo", "gn": "py", "quz": "pe", "chr": "us",
    "mi": "nz", "sm": "ws", "to": "to", "fj": "fj", "tpi": "pg",
    "bi": "vu", "gil": "ki", "ho": "pg", "mh": "mh", "na": "nr",
    "pau": "pw", "tet": "tl", "tvl": "tv", "hif": "fj",
    "eo": "un", "ia": "un", "la": "va", "tlh": "un",
    
    # UK Regional
    "gd": "gb-sct", "sco": "gb-sct", "cy": "gb-wls", "ga": "ie",
    "et": "ee", "lv": "lv", "lt": "lt",
    
    # Pirate / Fun
    "en_pirate": "gb", "ja_pirate": "jp", "zh_pirate": "cn",
    "tr_pirate": "tr", "fr_pirate": "fr", "es_pirate": "es",
    "pt_pirate": "pt", "pl_pirate": "pl", "ru_pirate": "ru",
    "nl_pirate": "nl", "sco_pirate": "gb-sct", "tlh_pirate": "un",
    "fr_CA_pirate": "ca"
}

output_path = Path("i18n/flags.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(flags_map, f, indent=4, sort_keys=True)

print(f"Regenerated {output_path} with {len(flags_map)} entries.")
