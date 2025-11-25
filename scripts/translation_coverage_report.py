#!/usr/bin/env python3
"""
Translation Coverage Report Generator
Creates an interactive HTML dashboard showing translation coverage for all languages
"""
import json
from pathlib import Path
from datetime import datetime

class CoverageReportGenerator:
    def __init__(self, qa_report_file: str = "reports/qa_report.json"):
        self.qa_report_file = Path(qa_report_file)
        self.report_data = None
        
    def load_qa_report(self):
        """Load QA report"""
        if not self.qa_report_file.exists():
            print(f"❌ QA report not found: {self.qa_report_file}")
            print(f"   Please run translation_qa_checker.py first")
            return False
        
        with open(self.qa_report_file, 'r', encoding='utf-8') as f:
            self.report_data = json.load(f)
        
        print(f"✅ Loaded QA report from: {self.qa_report_file}")
        return True
    
    def generate_html(self) -> str:
        """Generate HTML coverage report"""
        languages = self.report_data['languages']
        summary = self.report_data['summary']
        
        # Sort languages by coverage (descending)
        sorted_langs = sorted(
            languages.items(),
            key=lambda x: x[1].get('coverage', 0),
            reverse=True
        )
        
        # Build table rows
        rows = []
        for lang_code, data in sorted_langs:
            if not data.get('functional'):
                status_class = "error"
                status_icon = "❗"
            elif data.get('coverage', 0) == 100:
                status_class = "complete"
                status_icon = "✅"
            elif data.get('coverage', 0) >= 50:
                status_class = "partial"
                status_icon = "⚠️"
            else:
                status_class = "minimal"
                status_icon = "❌"
            
            coverage = data.get('coverage', 0)
            translated = data.get('translated', 0)
            total = data.get('total_keys', 0)
            fallbacks = data.get('fallbacks', 0)
            
            rows.append(f"""
                <tr class="{status_class}">
                    <td>{status_icon}</td>
                    <td><code>{lang_code}</code></td>
                    <td><strong>{translated}</strong> / {total}</td>
                    <td>{fallbacks}</td>
                    <td>
                        <div class="progress-bar">
                            <div class="progress-fill {status_class}" style="width: {coverage}%">
                                <span class="progress-text">{coverage}%</span>
                            </div>
                        </div>
                    </td>
                </tr>
            """)
        
        table_html = "\n".join(rows)
        
        # Complete HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Translation Coverage Report - MacGyver Multi-Tool</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .subtitle {{
            opacity: 0.9;
            font-size: 1.1em;
        }}
        
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
            border-bottom: 2px solid #e9ecef;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .stat-label {{
            color: #6c757d;
            font-size: 0.9em;
            margin-top: 8px;
        }}
        
        .content {{
            padding: 30px;
        }}
        
        table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
        }}
        
        thead {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }}
        
        th {{
            padding: 16px;
            text-align: left;
            font-weight: 600;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        tbody tr {{
            border-bottom: 1px solid #e9ecef;
            transition: background-color 0.2s;
        }}
        
        tbody tr:hover {{
            background-color: #f8f9fa;
        }}
        
        td {{
            padding: 14px 16px;
        }}
        
        .progress-bar {{
            background: #e9ecef;
            border-radius: 8px;
            height: 30px;
            position: relative;
            overflow: hidden;
        }}
        
        .progress-fill {{
            height: 100%;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: width 0.3s ease;
        }}
        
        .progress-fill.complete {{
            background: linear-gradient(90deg, #10b981, #059669);
        }}
        
        .progress-fill.partial {{
            background: linear-gradient(90deg, #f59e0b, #d97706);
        }}
        
        .progress-fill.minimal {{
            background: linear-gradient(90deg, #dc2626, #b91c1c);
        }}
        
        .progress-fill.error {{
            background: linear-gradient(90deg, #6b7280, #4b5563);
        }}
        
        .progress-text {{
            color: white;
            font-weight: 600;
            font-size: 0.85em;
        }}
        
        code {{
            background: #f8f9fa;
            padding: 4px 8px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }}
        
        footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #6c757d;
            font-size: 0.9em;
            border-top: 2px solid #e9ecef;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🌍 Translation Coverage Report</h1>
            <p class="subtitle">MacGyver Multi-Tool - Quality Analysis Dashboard</p>
            <p style="margin-top: 10px; opacity: 0.8; font-size: 0.9em;">
                Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            </p>
        </header>
        
        <div class="summary">
            <div class="stat-card">
                <div class="stat-value">{summary['total_languages']}</div>
                <div class="stat-label">Total Languages</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{summary['total_keys']}</div>
                <div class="stat-label">Translation Keys</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{summary['fully_functional']}</div>
                <div class="stat-label">✅ Complete</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{summary['partially_functional']}</div>
                <div class="stat-label">⚠️ Partial</div>
            </div>
        </div>
        
        <div class="content">
            <h2 style="margin-bottom: 20px;">Language Coverage Details</h2>
            <table>
                <thead>
                    <tr>
                        <th>Status</th>
                        <th>Language</th>
                        <th>Translated</th>
                        <th>Fallbacks</th>
                        <th>Coverage</th>
                    </tr>
                </thead>
                <tbody>
                    {table_html}
                </tbody>
            </table>
        </div>
        
        <footer>
            <p>MacGyver Multi-Tool Translation System v1.0</p>
            <p style="margin-top: 5px;">© 2025 Jan Friske - All rights reserved</p>
        </footer>
    </div>
</body>
</html>"""
        
        return html
    
    def save_report(self, output_file: str = "reports/translation_coverage.html"):
        """Save HTML coverage report"""
        if not self.load_qa_report():
            return False
        
        html = self.generate_html()
        
        # Ensure directory exists
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ HTML coverage report generated: {Path(output_file).absolute()}")
        print(f"   Open in browser to view interactive report")
        return True

def main():
    generator = CoverageReportGenerator()
    
    if generator.save_report():
        print("\n🎉 Coverage report complete!")
        return 0
    else:
        print("\n❌ Failed to generate coverage report")
        return 1

if __name__ == "__main__":
    exit(main())
