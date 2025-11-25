# Mehrsprachigkeits-Implementierungsplan
## MacGyver Multi-Tool i18n System

### 1. Übersicht

**Ziel:** Vollständige Mehrsprachigkeits-Unterstützung mit 10 Sprachen/Dialekten

**Sprachen (alphabetisch sortiert):**
1. Deutsch (Standard)
2. Deutsch (Berliner Dialekt)
3. Deutsch (Bayrischer Dialekt)
4. Englisch (English)
5. Französisch (Français)
6. Italienisch (Italiano)
7. Niederländisch (Nederlands)
8. Portugiesisch (Português)
9. Russisch (Русский)
10. Spanisch (Español)

---

### 2. Architektur

#### 2.1 Komponenten

**A. i18n Service (`core/services/i18n_service.py`)**
- Zentraler Übersetzungsmanager
- Lädt Sprachdateien
- Verwaltet aktuelle Sprache
- Bietet `tr()` Funktion für Übersetzungen
- Signal für Sprachwechsel

**B. Sprachdateien (`i18n/translations/`)**
- JSON-Format für jede Sprache
- Struktur: `{key: "Übersetzung"}`
- Dateinamen: `de.json`, `de_berlin.json`, `de_bavaria.json`, `en.json`, etc.

**C. Sprach-Manager (`core/services/language_manager.py`)**
- Verwaltet Sprachauswahl
- Persistiert Spracheinstellung (QSettings)
- Lädt Standardsprache beim Start

**D. Signal-System**
- `language_changed` Signal in MainWindow
- Automatische UI-Aktualisierung bei Sprachwechsel

---

### 3. Dateistruktur

```
MacGyver Multi-Tool/
├── core/
│   └── services/
│       ├── i18n_service.py          # Übersetzungsservice
│       └── language_manager.py      # Sprachverwaltung
├── i18n/
│   ├── translations/
│   │   ├── de.json                  # Deutsch (Standard)
│   │   ├── de_berlin.json           # Berliner Dialekt
│   │   ├── de_bavaria.json          # Bayrischer Dialekt
│   │   ├── en.json                  # Englisch
│   │   ├── fr.json                  # Französisch
│   │   ├── it.json                  # Italienisch
│   │   ├── nl.json                  # Niederländisch
│   │   ├── pt.json                  # Portugiesisch
│   │   ├── ru.json                  # Russisch
│   │   └── es.json                  # Spanisch
│   └── __init__.py
└── ...
```

---

### 4. Implementierungsphasen

#### Phase 1: Grundstruktur (Foundation)
1. ✅ i18n Service erstellen
2. ✅ Language Manager erstellen
3. ✅ Sprachdateien-Struktur anlegen
4. ✅ Basis-Übersetzungen (Deutsch) erstellen

#### Phase 2: Menü-Integration
1. ✅ "Einstellungen"-Menü zwischen "Werkzeuge" und "Hilfe" einfügen
2. ✅ "Sprachen"-Untermenü erstellen
3. ✅ Alle 10 Sprachen als Menüpunkte hinzufügen (alphabetisch)
4. ✅ Signal für Sprachwechsel verbinden

#### Phase 3: Übersetzungen
1. ✅ Alle Menü-Texte übersetzen
2. ✅ Widget-Titel übersetzen
3. ✅ Dialog-Texte übersetzen
4. ✅ Status-Meldungen übersetzen
5. ✅ Fehlermeldungen übersetzen

#### Phase 4: Dynamische UI-Aktualisierung
1. ✅ Signal/Slot für Sprachwechsel implementieren
2. ✅ Alle UI-Elemente bei Sprachwechsel aktualisieren
3. ✅ Persistierung der Spracheinstellung

#### Phase 5: Dialekt-Unterstützung
1. ✅ Berliner Dialekt-Übersetzungen
2. ✅ Bayrischer Dialekt-Übersetzungen
3. ✅ Spezielle Dialekt-Ausdrücke

---

### 5. Technische Details

#### 5.1 Sprach-Codes
```python
LANGUAGES = {
    "de": "Deutsch",
    "de_berlin": "Deutsch (Berliner Dialekt)",
    "de_bavaria": "Deutsch (Bayrischer Dialekt)",
    "en": "English",
    "fr": "Français",
    "it": "Italiano",
    "nl": "Nederlands",
    "pt": "Português",
    "ru": "Русский",
    "es": "Español"
}
```

#### 5.2 Übersetzungsschlüssel-Struktur
```json
{
    "menu": {
        "file": "Datei",
        "edit": "Bearbeiten",
        "view": "Ansicht",
        "tools": "Werkzeuge",
        "settings": "Einstellungen",
        "help": "Hilfe"
    },
    "widgets": {
        "clock": "Weltzeituhr",
        "system_monitor": "System Monitor",
        ...
    },
    "dialogs": {
        "about": {
            "title": "Über MacGyver Multi-Tool",
            "version": "Version 1.0"
        }
    }
}
```

#### 5.3 Signal-Integration
```python
# In MainWindow
language_changed = Signal(str)  # Sprachcode

# In Controller
def change_language(self, lang_code):
    i18n_service.set_language(lang_code)
    # UI aktualisieren
    self.view.update_ui_language()
```

---

### 6. Ablaufplan

**Schritt 1:** i18n Service & Language Manager erstellen
**Schritt 2:** Sprachdateien-Struktur anlegen (alle 10 Sprachen)
**Schritt 3:** Menü "Einstellungen" mit "Sprachen"-Untermenü integrieren
**Schritt 4:** Basis-Übersetzungen (Deutsch) in alle Dateien eintragen
**Schritt 5:** Signal/Slot für Sprachwechsel implementieren
**Schritt 6:** Alle UI-Texte durch Übersetzungsfunktion ersetzen
**Schritt 7:** Übersetzungen für alle Sprachen erstellen
**Schritt 8:** Dialekt-Übersetzungen hinzufügen
**Schritt 9:** Persistierung der Spracheinstellung
**Schritt 10:** Testing & Fehlerbehebung

---

### 7. Besondere Anforderungen

#### 7.1 Dialekte
- **Berliner Dialekt:** "Weltzeituhr" → "Weltzeituhr" (aber andere Ausdrücke)
- **Bayrischer Dialekt:** "Weltzeituhr" → "Weltzeituhr" (aber andere Ausdrücke)
- Dialekt-spezifische Begriffe und Formulierungen

#### 7.2 Alphabetische Sortierung
- Menüpunkte müssen alphabetisch nach Anzeigename sortiert sein
- Sortierung: Deutsch, Deutsch (Berliner Dialekt), Deutsch (Bayrischer Dialekt), English, Français, Italiano, Nederlands, Português, Русский, Español

#### 7.3 Persistierung
- Spracheinstellung in QSettings speichern
- Beim Start letzte gewählte Sprache laden
- Fallback auf Systemsprache oder Deutsch

---

### 8. Testplan

1. ✅ Sprachwechsel über Menü testen
2. ✅ UI-Aktualisierung bei Sprachwechsel prüfen
3. ✅ Persistierung testen (Neustart)
4. ✅ Alle 10 Sprachen durchtesten
5. ✅ Dialekt-Übersetzungen prüfen
6. ✅ Fehlende Übersetzungen identifizieren

---

### 9. Erweiterbarkeit

- Einfaches Hinzufügen neuer Sprachen
- Übersetzungsdateien können extern bearbeitet werden
- Unterstützung für Rechts-nach-Links-Sprachen (später)
