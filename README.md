# MacGyver Multi-Tool

![MacGyver Multi-Tool Logo](assets/images/logo.png)

[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)](https://www.microsoft.com/store)
[![PySide6](https://img.shields.io/badge/PySide6-Qt%20for%20Python-green.svg)](https://www.qt.io/qt-for-python)

**MacGyver Multi-Tool** is a powerful, versatile desktop application that brings together essential system monitoring, media management, and productivity tools in one elegant, macOS-inspired interface for Windows.

[🇩🇪 Deutsche Version](README_DE.md) | [🌐 English Version](README.md)

---

## 🌟 Key Features

### 🌍 Unprecedented Multilingual Support
- **260+ Languages & Dialects** including:
  - Standard languages (English, German, French, Spanish, Chinese, Japanese, etc.)
  - Regional German dialects (Bavarian, Swabian, Saxon, Kölsch, Plattdeutsch, etc.)
  - Historical languages (Middle High German, Old English, Latin)
  - Constructed languages (Esperanto, Klingon)
  - Fun variants (Pirate English, Pirate German, etc.)
- **Dynamic Translation System** with user-customizable translations
- **Create Your Own Languages** with the built-in language editor
- **Hierarchical Language Menu** organized by continents and regions

### 🎛️ Dashboard & Widgets
- **Customizable Widget Dashboard** with drag-and-drop functionality
- **System Monitor Widgets**:
  - CPU, RAM, and GPU monitoring with real-time graphs
  - Network traffic monitor
  - Temperature sensors
  - Disk usage statistics
- **World Clock Widget** with weather integration
- **Responsive Widget Sizing** - widgets adapt to different grid sizes
- **Widget Previews** with authentic downscaling

### 🎨 Premium macOS-Style Interface
- **Frameless Window Design** with custom title bar
- **Multiple Themes**:
  - Light Mode (macOS-inspired)
  - Dark Mode (elegant dark theme)
  - Klingon Theme (automatically activates with Klingon language)
- **Smooth Animations** and micro-interactions
- **Premium Typography** and color palettes
- **Glassmorphism Effects** for modern aesthetics

### 🎵 Media Management
- **Media Player** with modern controls
- **Media Explorer** for browsing media files
- **Equalizer** with customizable audio settings
- **Video Screen** support

### 🔧 Developer Tools & Gadgets
- **File Management Widgets**
- **Network Monitoring Tools**
- **System Information Display**
- **Command Palette** (Ctrl+P) for quick access to all features

### ⚙️ Advanced Features
- **Translation Editor** - edit translations for all languages
- **User Override System** - customize any translation
- **Translation Statistics** - track coverage across languages
- **Custom Language Creation** - build your own language packs
- **Tooltip System** with detailed, context-sensitive help

---

## 🚀 Getting Started

### Prerequisites
- Windows 10/11
- Python 3.8 or higher
- PySide6 (Qt for Python)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/JanFriske/MacGyver-Multi-Tool.git
cd MacGyver-Multi-Tool
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python app.py
```

---

## 📖 Usage

### Changing Language
1. Navigate to **Settings → Languages**
2. Browse through the hierarchical menu organized by continents
3. Select your preferred language or dialect
4. The entire UI updates instantly

### Adding Widgets to Dashboard
1. Open **Tools → Cockpit → Dashboard**
2. Click **Add Widget**
3. Select from available widgets (Clock, System Monitor, Network, GPU, Temperature, etc.)
4. Drag and drop to arrange on the grid
5. Resize widgets by changing their span

### Creating Custom Translations
1. Go to **Settings → Languages → Edit Translations**
2. Select the language you want to customize
3. Edit any translation key
4. Changes are saved automatically and applied immediately

### Creating a New Language
1. Navigate to **Settings → Languages → Create New Language**
2. Enter language code and display name
3. Optionally import translations from an existing language
4. Start customizing translations

---

## 🏗️ Project Structure

```
MacGyver Multi-Tool/
├── app.py                      # Main application entry point
├── core/                       # Core business logic
│   ├── model.py               # Data models
│   └── services/              # Service layer
│       ├── i18n_service.py    # Internationalization service (260+ languages)
│       ├── weather_service.py # Weather data integration
│       └── user_override_service.py # User translation overrides
├── presenter/                  # Controller layer (MVP pattern)
│   └── controller.py          # Main application controller
├── ui/                        # User interface layer
│   ├── view.py                # Main window and UI logic
│   ├── components/            # Reusable UI components
│   │   ├── command_palette.py # Quick command access
│   │   └── title_bar.py       # Custom window title bar
│   ├── dialogs/               # Dialog windows
│   ├── tools/                 # Tool implementations
│   │   ├── dashboard.py       # Widget dashboard
│   │   ├── gadgets.py         # System monitoring widgets
│   │   ├── media_player.py    # Media playback
│   │   ├── network_widgets.py # Network monitoring
│   │   └── widget_selector.py # Widget selection dialog
│   └── styles/                # QSS stylesheets
│       ├── mac_light.qss      # Light theme
│       ├── mac_dark.qss       # Dark theme
│       └── mac_klingon.qss    # Klingon theme
├── i18n/                      # Internationalization
│   ├── translations/          # 260+ language JSON files
│   ├── flags.json             # Language-to-flag mappings
│   └── translation_master.json # Master translation database
├── assets/                    # Resources
│   ├── icons/                 # Application icons
│   ├── images/                # Images and logos
│   └── flags/                 # Country/language flags (SVG & PNG)
└── scripts/                   # Utility scripts for development
```

---

## 🎯 Roadmap

### Current Status
✅ Core application framework  
✅ 260+ language support with hierarchical menu  
✅ Dashboard with customizable widgets  
✅ macOS-style UI with multiple themes  
✅ Translation editor and custom language creation  
✅ System monitoring widgets  
✅ Media player integration  

### Planned Features
🔲 Additional widget types (calendar, notes, calculator)  
🔲 Plugin system for third-party extensions  
🔲 Cloud synchronization for settings  
🔲 Advanced media library management  
🔲 Performance profiling tools  
🔲 Network analysis tools  
🔲 Microsoft Store release (Q4 2025 / Q1 2026)  

---

## 🤝 Contributing

We welcome contributions from the community! Whether you're fixing bugs, adding new features, or improving documentation, your help is appreciated.

Please read our [Contributing Guidelines](CONTRIBUTING.md) to get started.

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Adding New Languages
We're always looking to expand our language support! If you'd like to add a new language or dialect:
1. Use the built-in **Create New Language** feature
2. Export your translation file
3. Submit it via Pull Request to `i18n/translations/`

---

## 📜 License

This project is licensed under the **GNU Lesser General Public License v3.0 (LGPL-3.0)**.

- ✅ **Free to use** for personal and commercial purposes
- ✅ **Modify and distribute** with attribution
- ✅ **Link dynamically** without copyleft requirements
- ⚠️ **Modifications to LGPL code** must be released under LGPL

See the [LICENSE](LICENSE) file for full details.

### Third-Party Licenses
- **PySide6**: Licensed under LGPL v3
- **Qt Framework**: Licensed under LGPL v3

---

## 🔒 Privacy

**MacGyver Multi-Tool respects your privacy.**

- ❌ **No data collection** - We don't collect any personal information
- ❌ **No tracking** - No analytics or telemetry
- ❌ **No internet required** - Works completely offline (except weather widget)
- ✅ **Local storage only** - All data stays on your device

Read our full [Privacy Policy](PRIVACY.md) for details.

---

## 🏆 Acknowledgments

- **Qt/PySide6** - For the excellent cross-platform framework
- **psutil** - For system monitoring capabilities
- **The Open Source Community** - For inspiration and support

---

## 📧 Contact

**Jan Friske**  
- GitHub: [@JanFriske](https://github.com/JanFriske)
- Project: [MacGyver Multi-Tool](https://github.com/JanFriske/MacGyver-Multi-Tool)

---

## 🌟 Star History

If you find this project useful, please consider giving it a ⭐ on GitHub!

---

**Made with ❤️ by Jan Friske**  
*A Swiss Army knife for your Windows desktop*
