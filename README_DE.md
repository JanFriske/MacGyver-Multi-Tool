# MacGyver Multi-Tool

![MacGyver Multi-Tool Logo](assets/images/logo.png)

[![Lizenz: LGPL v3](https://img.shields.io/badge/Lizenz-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![Plattform](https://img.shields.io/badge/Plattform-Windows-blue.svg)](https://www.microsoft.com/store)
[![PySide6](https://img.shields.io/badge/PySide6-Qt%20for%20Python-green.svg)](https://www.qt.io/qt-for-python)

**MacGyver Multi-Tool** ist eine leistungsstarke, vielseitige Desktop-Anwendung, die wichtige Systemüberwachungs-, Medienverwaltungs- und Produktivitätswerkzeuge in einer eleganten, macOS-inspirierten Benutzeroberfläche für Windows vereint.

[🇩🇪 Deutsche Version](README_DE.md) | [🌐 English Version](README.md)

---

## 🌟 Hauptfunktionen

### 🌍 Beispiellose Mehrsprachigkeit
- **260+ Sprachen & Dialekte** einschließlich:
  - Standardsprachen (Englisch, Deutsch, Französisch, Spanisch, Chinesisch, Japanisch, etc.)
  - Regionale deutsche Dialekte (Bairisch, Schwäbisch, Sächsisch, Kölsch, Plattdeutsch, etc.)
  - Historische Sprachen (Mittelhochdeutsch, Altenglisch, Latein)
  - Konstruierte Sprachen (Esperanto, Klingonisch)
  - Spaßvarianten (Piraten-Englisch, Piraten-Deutsch, etc.)
- **Dynamisches Übersetzungssystem** mit benutzerdefinierbaren Übersetzungen
- **Eigene Sprachen erstellen** mit dem integrierten Spracheditor
- **Hierarchisches Sprachmenü** organisiert nach Kontinenten und Regionen

### 🎛️ Dashboard & Widgets
- **Anpassbares Widget-Dashboard** mit Drag-and-Drop-Funktionalität
- **Systemüberwachungs-Widgets**:
  - CPU-, RAM- und GPU-Überwachung mit Echtzeit-Diagrammen
  - Netzwerkverkehr-Monitor
  - Temperatursensoren
  - Festplattennutzungsstatistiken
- **Weltzeituhr-Widget** mit Wetterintegration
- **Responsive Widget-Größenanpassung** - Widgets passen sich verschiedenen Rastergrößen an
- **Widget-Vorschauen** mit authentischer Verkleinerung

### 🎨 Premium macOS-Style Benutzeroberfläche
- **Rahmenloses Fensterdesign** mit benutzerdefinierter Titelleiste
- **Mehrere Themes**:
  - Light Mode (macOS-inspiriert)
  - Dark Mode (elegantes dunkles Theme)
  - Klingonisches Theme (aktiviert sich automatisch mit Klingonisch)
- **Flüssige Animationen** und Mikro-Interaktionen
- **Premium-Typografie** und Farbpaletten
- **Glassmorphismus-Effekte** für moderne Ästhetik

### 🎵 Medienverwaltung
- **Media Player** mit modernen Steuerelementen
- **Media Explorer** zum Durchsuchen von Mediendateien
- **Equalizer** mit anpassbaren Audio-Einstellungen
- **Video-Bildschirm**-Unterstützung

### 🔧 Entwickler-Tools & Gadgets
- **Dateiverwaltungs-Widgets**
- **Netzwerküberwachungs-Tools**
- **Systeminformationsanzeige**
- **Befehlspalette** (Strg+P) für schnellen Zugriff auf alle Funktionen

### ⚙️ Erweiterte Funktionen
- **Übersetzungseditor** - Übersetzungen für alle Sprachen bearbeiten
- **Benutzer-Override-System** - jede Übersetzung anpassen
- **Übersetzungsstatistiken** - Abdeckung über alle Sprachen hinweg verfolgen
- **Benutzerdefinierte Spracherstellung** - eigene Sprachpakete erstellen
- **Tooltip-System** mit detaillierter, kontextsensitiver Hilfe

---

## 🚀 Erste Schritte

### Voraussetzungen
- Windows 10/11
- Python 3.8 oder höher
- PySide6 (Qt für Python)

### Installation

1. **Repository klonen**
```bash
git clone https://github.com/JanFriske/MacGyver-Multi-Tool.git
cd MacGyver-Multi-Tool
```

2. **Abhängigkeiten installieren**
```bash
pip install -r requirements.txt
```

3. **Anwendung starten**
```bash
python app.py
```

---

## 📖 Verwendung

### Sprache wechseln
1. Navigieren Sie zu **Einstellungen → Sprachen**
2. Durchsuchen Sie das hierarchische Menü, organisiert nach Kontinenten
3. Wählen Sie Ihre bevorzugte Sprache oder Dialekt
4. Die gesamte Benutzeroberfläche wird sofort aktualisiert

### Widgets zum Dashboard hinzufügen
1. Öffnen Sie **Werkzeuge → Cockpit → Dashboard**
2. Klicken Sie auf **Widget hinzufügen**
3. Wählen Sie aus verfügbaren Widgets (Uhr, Systemmonitor, Netzwerk, GPU, Temperatur, etc.)
4. Ziehen und ablegen, um auf dem Raster anzuordnen
5. Größe der Widgets durch Ändern ihrer Spanne anpassen

### Benutzerdefinierte Übersetzungen erstellen
1. Gehen Sie zu **Einstellungen → Sprachen → Übersetzungen bearbeiten**
2. Wählen Sie die Sprache aus, die Sie anpassen möchten
3. Bearbeiten Sie jeden Übersetzungsschlüssel
4. Änderungen werden automatisch gespeichert und sofort angewendet

### Eine neue Sprache erstellen
1. Navigieren Sie zu **Einstellungen → Sprachen → Neue Sprache erstellen**
2. Geben Sie Sprachcode und Anzeigename ein
3. Optional: Übersetzungen aus einer vorhandenen Sprache importieren
4. Beginnen Sie mit der Anpassung der Übersetzungen

---

## 🏗️ Projektstruktur

```
MacGyver Multi-Tool/
├── app.py                      # Haupteinstiegspunkt der Anwendung
├── core/                       # Kern-Geschäftslogik
│   ├── model.py               # Datenmodelle
│   └── services/              # Service-Schicht
│       ├── i18n_service.py    # Internationalisierungsdienst (260+ Sprachen)
│       ├── weather_service.py # Wetterdatenintegration
│       └── user_override_service.py # Benutzer-Übersetzungsüberschreibungen
├── presenter/                  # Controller-Schicht (MVP-Muster)
│   └── controller.py          # Haupt-Anwendungscontroller
├── ui/                        # Benutzeroberflächen-Schicht
│   ├── view.py                # Hauptfenster und UI-Logik
│   ├── components/            # Wiederverwendbare UI-Komponenten
│   │   ├── command_palette.py # Schneller Befehlszugriff
│   │   └── title_bar.py       # Benutzerdefinierte Fenstertitelleiste
│   ├── dialogs/               # Dialogfenster
│   ├── tools/                 # Tool-Implementierungen
│   │   ├── dashboard.py       # Widget-Dashboard
│   │   ├── gadgets.py         # Systemüberwachungs-Widgets
│   │   ├── media_player.py    # Medienwiedergabe
│   │   ├── network_widgets.py # Netzwerküberwachung
│   │   └── widget_selector.py # Widget-Auswahldialog
│   └── styles/                # QSS-Stylesheets
│       ├── mac_light.qss      # Helles Theme
│       ├── mac_dark.qss       # Dunkles Theme
│       └── mac_klingon.qss    # Klingonisches Theme
├── i18n/                      # Internationalisierung
│   ├── translations/          # 260+ Sprach-JSON-Dateien
│   ├── flags.json             # Sprache-zu-Flagge-Zuordnungen
│   └── translation_master.json # Master-Übersetzungsdatenbank
├── assets/                    # Ressourcen
│   ├── icons/                 # Anwendungssymbole
│   ├── images/                # Bilder und Logos
│   └── flags/                 # Länder-/Sprachflaggen (SVG & PNG)
└── scripts/                   # Hilfsskripte für die Entwicklung
```

---

## 🎯 Roadmap

### Aktueller Status
✅ Kern-Anwendungsframework  
✅ 260+ Sprachunterstützung mit hierarchischem Menü  
✅ Dashboard mit anpassbaren Widgets  
✅ macOS-Style UI mit mehreren Themes  
✅ Übersetzungseditor und benutzerdefinierte Spracherstellung  
✅ Systemüberwachungs-Widgets  
✅ Media Player Integration  

### Geplante Funktionen
🔲 Zusätzliche Widget-Typen (Kalender, Notizen, Taschenrechner)  
🔲 Plugin-System für Drittanbieter-Erweiterungen  
🔲 Cloud-Synchronisation für Einstellungen  
🔲 Erweiterte Medienbibliotheksverwaltung  
🔲 Performance-Profiling-Tools  
🔲 Netzwerkanalyse-Tools  
🔲 Microsoft Store Veröffentlichung (Q4 2025 / Q1 2026)  

---

## 🤝 Mitwirken

Wir begrüßen Beiträge aus der Community! Ob Sie Fehler beheben, neue Funktionen hinzufügen oder die Dokumentation verbessern - Ihre Hilfe wird geschätzt.

Bitte lesen Sie unsere [Beitragsrichtlinien](CONTRIBUTING.md), um loszulegen.

### Wie Sie beitragen können
1. Repository forken
2. Feature-Branch erstellen (`git checkout -b feature/TollesFunktion`)
3. Änderungen committen (`git commit -m 'Füge tolle Funktion hinzu'`)
4. Zum Branch pushen (`git push origin feature/TollesFunktion`)
5. Pull Request öffnen

### Neue Sprachen hinzufügen
Wir sind immer auf der Suche nach Erweiterung unserer Sprachunterstützung! Wenn Sie eine neue Sprache oder einen Dialekt hinzufügen möchten:
1. Verwenden Sie die integrierte Funktion **Neue Sprache erstellen**
2. Exportieren Sie Ihre Übersetzungsdatei
3. Reichen Sie sie per Pull Request an `i18n/translations/` ein

---

## 📜 Lizenz

Dieses Projekt ist unter der **GNU Lesser General Public License v3.0 (LGPL-3.0)** lizenziert.

- ✅ **Kostenlos nutzbar** für private und kommerzielle Zwecke
- ✅ **Modifizieren und verteilen** mit Namensnennung
- ✅ **Dynamisch verlinken** ohne Copyleft-Anforderungen
- ⚠️ **Änderungen am LGPL-Code** müssen unter LGPL veröffentlicht werden

Siehe die [LICENSE](LICENSE)-Datei für vollständige Details.

### Lizenzen von Drittanbietern
- **PySide6**: Lizenziert unter LGPL v3
- **Qt Framework**: Lizenziert unter LGPL v3

---

## 🔒 Datenschutz

**MacGyver Multi-Tool respektiert Ihre Privatsphäre.**

- ❌ **Keine Datenerfassung** - Wir sammeln keine persönlichen Informationen
- ❌ **Kein Tracking** - Keine Analytik oder Telemetrie
- ❌ **Kein Internet erforderlich** - Funktioniert vollständig offline (außer Wetter-Widget)
- ✅ **Nur lokale Speicherung** - Alle Daten bleiben auf Ihrem Gerät

Lesen Sie unsere vollständige [Datenschutzerklärung](PRIVACY.md) für Details.

---

## 🏆 Danksagungen

- **Qt/PySide6** - Für das exzellente plattformübergreifende Framework
- **psutil** - Für Systemüberwachungsfunktionen
- **Die Open-Source-Community** - Für Inspiration und Unterstützung

---

## 📧 Kontakt

**Jan Friske**  
- GitHub: [@JanFriske](https://github.com/JanFriske)
- Projekt: [MacGyver Multi-Tool](https://github.com/JanFriske/MacGyver-Multi-Tool)

---

## 🌟 Star-Verlauf

Wenn Sie dieses Projekt nützlich finden, geben Sie ihm bitte einen ⭐ auf GitHub!

---

**Mit ❤️ erstellt von Jan Friske**  
*Ein Schweizer Taschenmesser für Ihren Windows-Desktop*
