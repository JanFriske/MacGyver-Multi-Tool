#!/usr/bin/env python3
"""
Translation Quality Assurance Checker
Validates all translation filesen, identifies missing translations,
and calculates coverage percentages
"""
import json
import os
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

class TranslationQAChecker:
    def __init__(self):
        self.base_dir = Path("i18n/translations")
        self.master_file = Path("i18n/translation_master.json")
        self.master_data = None
        self.results = {}
        
    def load_master_db(self):
        """Load master translation database"""
        if not self.master_file.exists():
            print(f"❌ Master database not found: {self.master_file}")
            return False
        
        with open(self.master_file, 'r', encoding='utf-8') as f:
            self.master_data = json.load(f)
        
        print(f"✅ Loaded master database: {self.master_data['metadata']['total_keys']} keys")
        return True
    
    def get_all_language_files(self) -> List[Path]:
        """Get all JSON language files"""
        return sorted(self.base_dir.glob("*.json"))
    
    def validate_json_structure(self, file_path: Path) -> Tuple[bool, str]:
        """Validate if JSON file is valid and loadable"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
            return True, "Valid JSON"
        except json.JSONDecodeError as e:
            return False, f"JSON Error: {str(e)}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def flatten_dict(self, d, parent_key='', sep='.'):
        """Flatten nested dictionary"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self.flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
    
    def analyze_language_file(self, file_path: Path, en_ref: Dict) -> Dict:
        """Analyze single language file"""
        lang_code = file_path.stem
        
        # Validate JSON structure
        is_valid, error_msg = self.validate_json_structure(file_path)
        if not is_valid:
            return {
                "status": "error",
                "error": error_msg,
                "functional": False
            }
        
        # Load and flatten
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        flat_data = self.flatten_dict(data)
        total_keys = len(en_ref)
        present_keys = set(flat_data.keys())
        expected_keys = set(en_ref.keys())
        
        # Calculate metrics
        missing_keys = expected_keys - present_keys
        extra_keys = present_keys - expected_keys
        
        # Count how many values are identical to English (likely fallbacks)
        fallback_count = 0
        if lang_code != "en":
            for key in present_keys & expected_keys:
                if flat_data.get(key)== en_ref.get(key):
                    fallback_count += 1
        
        translated = len(present_keys & expected_keys) - fallback_count
        coverage = (translated / total_keys * 100) if total_keys > 0 else 0
        
        return {
            "status": "complete" if coverage == 100 else "partial" if coverage > 50 else "minimal",
            "total_keys": total_keys,
            "present_keys": len(present_keys),
            "translated": translated,
            "fallbacks": fallback_count,
            "missing": len(missing_keys),
            "extra": len(extra_keys),
            "coverage": round(coverage, 2),
            "functional": is_valid,
            "missing_keys": sorted(list(missing_keys))[:10],  # First 10 for report
            "extra_keys": sorted(list(extra_keys))[:10]
        }
    
    def run_full_check(self):
        """Run complete QA check on all language files"""
        if not self.load_master_db():
            return False
        
        # Get reference English
        en_file = self.base_dir / "en.json"
        with open(en_file, 'r', encoding='utf-8') as f:
            en_data = json.load(f)
        en_flat = self.flatten_dict(en_data)
        
        # Check all files
        lang_files = self.get_all_language_files()
        print(f"\n🔍 Checking {len(lang_files)} language files...\n")
        
        for file_path in lang_files:
            lang_code = file_path.stem
            print(f"   [{lang_code}] ", end="")
            
            result = self.analyze_language_file(file_path, en_flat)
            self.results[lang_code] = result
            
            # Print status
            if result["functional"]:
                coverage = result["coverage"]
                if coverage == 100:
                    print(f"✅ {coverage}% (Complete)")
                elif coverage >= 50:
                    print(f"⚠️  {coverage}% ({result['translated']}/{result['total_keys']})")
                else:
                    print(f"❌ {coverage}% (Mostly fallbacks)")
            else:
                print(f"❗ Error: {result.get('error', 'Unknown')}")
        
        return True
    
    def generate_summary(self):
        """Generate summary statistics"""
        total_langs = len(self.results)
        fully_functional = sum(1 for r in self.results.values() if r['functional'] and r['coverage'] == 100)
        partial = sum(1 for r in self.results.values() if r['functional'] and 0 < r['coverage'] < 100)
        fallback_only = sum(1 for r in self.results.values() if r['functional'] and r['coverage'] == 0)
        broken = sum(1 for r in self.results.values() if not r['functional'])
        
        print("\n" + "="*60)
        print("📊 SUMMARY")
        print("="*60)
        print(f"Total languages: {total_langs}")
        print(f"  ✅ Fully translated: {fully_functional}")
        print(f"  ⚠️  Partially translated: {partial}")
        print(f"  ❌ Fallback only: {fallback_only}")
        print(f"  ❗ Broken/Invalid: {broken}")
        print("="*60)
    
    def save_report(self, output_file: str = "reports/qa_report.json"):
        """Save detailed QA report to JSON"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_languages": len(self.results),
                "total_keys": self.master_data['metadata']['total_keys'] if self.master_data else 0,
                "fully_functional": sum(1 for r in self.results.values() if r.get('functional') and r.get('coverage') == 100),
                "partially_functional": sum(1 for r in self.results.values() if r.get('functional') and 0 < r.get('coverage', 0) < 100),
                "fallback_only": sum(1 for r in self.results.values() if r.get('functional') and r.get('coverage', 0) == 0)
            },
            "languages": self.results
        }
        
        # Ensure reports directory exists
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Report saved: {output_file}")

def main():
    checker = TranslationQAChecker()
    
    if checker.run_full_check():
        checker.generate_summary()
        checker.save_report()
        print("\n✅ Quality check complete!")
    else:
        print("\n❌ Quality check failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
