import json
import os

# Complete list of 38 German dialects with their codes
GERMAN_DIALECTS = [
    # Standard & Historical (2)
    ("de", "Hochdeutsch (Standard)", "exists"),  # Already main language
    ("de_middlehigh", "Mittelhochdeutsch (1050-1350)", "new"),
    
    # East German - DDR Heritage (5)
    ("de_brandenburg", "Brandenburgisch/Märkisch", "new"),
    ("de_thuringia", "Thüringisch", "new"),
    ("de_uppersaxon", "Obersächsisch", "new"),
    ("de_lusatian", "Lausitzisch", "new"),
    ("de_pomeranian", "Pommersch", "new"),
    
    # Historical Eastern Territories (4)
    ("de_sudeten", "Sudetendeutsch", "new"),
    ("de_silesian", "Schlesisch", "new"),
    ("de_lowprussia", "Niederpreußisch", "new"),
    ("de_eastprussia", "Hochpreußisch", "exists"),
    
    # Diaspora & Emigrants (3)
    ("de_volga", "Wolgadeutsch", "new"),
    ("de_banat", "Banater Schwäbisch", "new"),
    ("de_sathmar", "Sathmarisch-Schwäbisch", "new"),
    
    # South German/Alpine (9)
    ("de_bavaria", "Bairisch", "exists"),
    ("de_swabian", "Schwäbisch", "exists"),
    ("de_allgaeu", "Allgäuerisch", "new"),
    ("de_southtyrol", "Südtirolerisch", "new"),
    ("de_alemannic", "Alemannisch", "new"),
    ("de_baden", "Badisch", "new"),
    ("de_franconian", "Fränkisch", "new"),
    ("de_vorarlberg", "Vorarlbergisch", "new"),
    ("de_palatinate", "Pfälzisch", "exists"),
    
    # North/West German (8)
    ("de_lowgerman", "Plattdeutsch", "exists"),
    ("de_mecklenburg", "Mecklenburger Platt", "exists"),
    ("de_holstein", "Holsteiner Platt", "exists"),
    ("de_westphalian", "Westfälisch", "new"),
    ("de_ripuarian", "Ripuarisch/Kölsch", "new"),
    ("de_moselfranken", "Moselfränkisch", "new"),
    ("de_ruhr", "Ruhrdeutsch/Ruhrpott", "new"),
    
    # Urban/City Dialects (4)
    ("de_berlin", "Berlinerisch", "exists"),
    ("de_saxony", "Sächsisch", "exists"),
    ("de_frankfurt", "Frankfurterisch", "new"),
    ("de_rhine", "Rheinisch", "new"),
    
    # Foreign German (4)
    ("de_at", "Österreichisch", "exists"),
    ("de_ch", "Schwitzerdütsch", "exists"),
    ("de_luxembourg", "Luxemburgisch", "new"),
    ("de_transylvania", "Siebenbürgisch-Sächsisch", "exists"),
]

def create_german_dialect_files():
    """Create JSON files for missing German dialects."""
    
    base_path = "i18n/translations"
    de_file = os.path.join(base_path, "de.json")
    
    # Load German template
    with open(de_file, 'r', encoding='utf-8') as f:
        de_data = json.load(f)
    
    created_count = 0
    skipped_count = 0
    exists_count = 0
    
    print(f"{'='*70}")
    print(f"Creating German Dialect Files (38 Total)")
    print(f"{'='*70}\n")
    
    for lang_code, dialect_name, status in GERMAN_DIALECTS:
        filename = lang_code + '.json'
        target_file = os.path.join(base_path, filename)
        
        if status == "exists":
            if os.path.exists(target_file):
                print(f"✅ {lang_code:20s} - {dialect_name:35s} [ALREADY EXISTS]")
                exists_count += 1
            else:
                print(f"⚠️  {lang_code:20s} - {dialect_name:35s} [MARKED EXISTS BUT MISSING!]")
            continue
        
        # status == "new"
        if os.path.exists(target_file):
            print(f"⏭️  {lang_code:20s} - {dialect_name:35s} [SKIPPED - already created]")
            skipped_count += 1
            continue
        
        # Create new dialect file with German content
        with open(target_file, 'w', encoding='utf-8') as f:
            json.dump(de_data, f, indent=4, ensure_ascii=False)
        
        print(f"🆕 {lang_code:20s} - {dialect_name:35s} [CREATED]")
        created_count += 1
    
    print(f"\n{'='*70}")
    print(f"Summary:")
    print(f"  Already Existed: {exists_count}")
    print(f"  Newly Created:   {created_count}")
    print(f"  Skipped:         {skipped_count}")
    print(f"  Total Dialects:  {len(GERMAN_DIALECTS)}")
    print(f"{'='*70}")
    print(f"\n✅ Next step: Run 'update_tooltips.py' to propagate improved tooltips!")

if __name__ == "__main__":
    create_german_dialect_files()
