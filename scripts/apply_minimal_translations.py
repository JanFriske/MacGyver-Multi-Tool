"""
Minimal Translation Script - Tier 1 Languages (7)
Translates only the 10 most critical UI keys for basic functionality
"""
import json
import os
from pathlib import Path

# Tier 1 Languages
TIER_1_LANGS = ["ko", "id", "th", "bn", "ur", "ps", "fa_AF"]

# Critical translations for minimal functional UI
# Based on standard software terminology in each language
TRANSLATIONS = {
    # Korean (한국어)
    "ko": {
        "menu.file": "파일",
        "menu.edit": "편집",
        "menu.view": "보기",
        "dialogs.about.title": "MacGyver Multi-Tool 정보",
        "dialogs.about.description": "macOS 디자인의 모듈식 유틸리티 도구",
        "dialogs.about.copyright": "© 2025 Jan Friske – 모든 권리 보유",
        "dialogs.about.license": "프리웨어 라이선스 (비상업적)",
        "tabs.cockpit": "콕핏",
        "tabs.media_commander": "미디어 커맨더"
    },
    
    # Indonesian (Bahasa Indonesia)
    "id": {
        "menu.file": "Berkas",
        "menu.edit": "Edit",
        "menu.view": "Tampilan",
        "dialogs.about.title": "Tentang MacGyver Multi-Tool",
        "dialogs.about.description": "Alat utilitas modular dengan desain macOS",
        "dialogs.about.copyright": "© 2025 Jan Friske – Hak cipta dilindungi",
        "dialogs.about.license": "Lisensi Freeware (non-komersial)",
        "tabs.cockpit": "Kokpit",
        "tabs.media_commander": "Media Commander"
    },
    
    # Thai (ภาษาไทย)
    "th": {
        "menu.file": "ไฟล์",
        "menu.edit": "แก้ไข",
        "menu.view": "มุมมอง",
        "dialogs.about.title": "เกี่ยวกับ MacGyver Multi-Tool",
        "dialogs.about.description": "เครื่องมือยูทิลิตี้แบบโมดูลาร์ด้วยการออกแบบ macOS",
        "dialogs.about.copyright": "© 2025 Jan Friske – สงวนลิขสิทธิ์",
        "dialogs.about.license": "สัญญาอนุญาตฟรีแวร์ (ไม่ใช่เชิงพาณิชย์)",
        "tabs.cockpit": "ค็อกพิท",
        "tabs.media_commander": "Media Commander"
    },
    
    # Bengali (বাংলা)
    "bn": {
        "menu.file": "ফাইল",
        "menu.edit": "সম্পাদনা",
        "menu.view": "দেখুন",
        "dialogs.about.title": "MacGyver Multi-Tool সম্পর্কে",
        "dialogs.about.description": "macOS ডিজাইনের সাথে একটি মডুলার ইউটিলিটি টুল",
        "dialogs.about.copyright": "© 2025 Jan Friske – সর্বস্বত্ব সংরক্ষিত",
        "dialogs.about.license": "ফ্রিওয়্যার লাইসেন্স (অ-বাণিজ্যিক)",
        "tabs.cockpit": "ককপিট",
        "tabs.media_commander": "মিডিয়া কমান্ডার"
    },
    
    # Urdu (اردو) - RTL
    "ur": {
        "menu.file": "فائل",
        "menu.edit": "ترمیم",
        "menu.view": "منظر",
        "dialogs.about.title": "MacGyver Multi-Tool کے بارے میں",
        "dialogs.about.description": "macOS ڈیزائن کے ساتھ ایک ماڈیولر یوٹیلٹی ٹول",
        "dialogs.about.copyright": "© 2025 Jan Friske – تمام حقوق محفوظ ہیں",
        "dialogs.about.license": "فری ویئر لائسنس (غیر تجارتی)",
        "tabs.cockpit": "کاک پٹ",
        "tabs.media_commander": "میڈیا کمانڈر"
    },
    
    # Pashto (پښتو) - RTL
    "ps": {
        "menu.file": "فایل",
        "menu.edit": "سمون",
        "menu.view": "کتل",
        "dialogs.about.title": "د MacGyver Multi-Tool په اړه",
        "dialogs.about.description": "د macOS ډیزاین سره یو ماډلر وسیله",
        "dialogs.about.copyright": "© 2025 Jan Friske – ټول حقونه خوندي دي",
        "dialogs.about.license": "د وړیا نرم افزار جواز (غیر تجارتي)",
        "tabs.cockpit": "کاکپټ",
        "tabs.media_commander": "میډیا کمانډر"
    },
    
    # Dari (دری) - Afghan Persian, RTL
    "fa_AF": {
        "menu.file": "فایل",
        "menu.edit": "ویرایش",
        "menu.view": "نمایش",
        "dialogs.about.title": "درباره MacGyver Multi-Tool",
        "dialogs.about.description": "یک ابزار کاربردی ماژولار با طراحی macOS",
        "dialogs.about.copyright": "© 2025 Jan Friske – تمام حقوق محفوظ است",
        "dialogs.about.license": "مجوز نرم‌افزار رایگان (غیرتجاری)",
        "tabs.cockpit": "کاکپیت",
        "tabs.media_commander": "فرمانده رسانه"
    }
}

def apply_translations():
    """Apply minimal translations to Tier 1 language files."""
    base_path = Path("i18n/translations")
    
    updated_count = 0
    total_translations = 0
    
    for lang_code in TIER_1_LANGS:
        lang_file = base_path / f"{lang_code}.json"
        
        if not lang_file.exists():
            print(f"⚠️  {lang_code}.json not found, skipping...")
            continue
        
        # Load existing file
        with open(lang_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Apply translations
        translations = TRANSLATIONS.get(lang_code, {})
        lang_updated = 0
        
        for key_path, translation in translations.items():
            keys = key_path.split(".")
            
            # Navigate to the right location and set value
            current = data
            for i, key in enumerate(keys[:-1]):
                if key not in current:
                    current[key] = {}
                current = current[key]
            
            # Set the final value
            final_key = keys[-1]
            current[final_key] = translation
            lang_updated += 1
            total_translations += 1
        
        # Save updated file
        with open(lang_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"✅ {lang_code}: {lang_updated} translations applied")
        updated_count += 1
    
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Languages updated: {updated_count}")
    print(f"  Total translations: {total_translations}")
    print(f"  Expected: {len(TIER_1_LANGS)} × ~9 = ~{len(TIER_1_LANGS) * 9}")
    print(f"{'='*60}")
    print(f"\n✅ Phase 5 (Reduced) Complete!")
    print(f"   Tier-1 languages now have basic UI translations.")
    print(f"   Rest of UI will use English fallback.")

if __name__ == "__main__":
    os.chdir("c:/Dev/Repos/JanFriske/MacGyver Multi-Tool")
    apply_translations()
