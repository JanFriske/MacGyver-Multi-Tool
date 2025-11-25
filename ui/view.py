from PySide6.QtCore import QEvent, Qt, Signal
from PySide6.QtGui import QAction, QIcon, QKeySequence, QShortcut, QPixmap, QPainter, QFont
from PySide6.QtSvg import QSvgRenderer
from pathlib import Path
from PySide6.QtWidgets import (
    QDockWidget,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenuBar,
    QMessageBox,
    QStackedWidget,
    QTabWidget,
    QToolTip,
    QVBoxLayout,
    QWidget,
    QWidgetAction,
    QApplication,
)

class LanguageMenuItem(QWidget):
    """Custom widget for language menu items to ensure consistent flag display."""
    triggered = Signal()

    def __init__(self, text, icon_path=None, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 4, 10, 4)
        layout.setSpacing(10)

        # Icon Label
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(24, 18)
        self.icon_label.setScaledContents(True)
        if icon_path and Path(icon_path).exists():
            self.icon_label.setPixmap(QPixmap(str(icon_path)))
        else:
            # Placeholder or empty
            self.icon_label.setText("")
        
        # Make icon label transparent to mouse events
        self.icon_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        
        # Text Label
        self.text_label = QLabel(text)
        self.text_label.setStyleSheet("QLabel { color: palette(text); }")
        
        # Make text label transparent to mouse events
        self.text_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        
        layout.addWidget(self.icon_label)
        layout.addWidget(self.text_label)
        layout.addStretch()
        
        # Hover handling
        self.setAttribute(Qt.WA_Hover)
        self.setStyleSheet("QWidget:hover { background-color: palette(highlight); } QWidget:hover QLabel { color: palette(highlighted-text); }")
        
        # Enable mouse tracking to ensure smooth hover behavior
        self.setMouseTracking(True)

    def mouseReleaseEvent(self, event):
        """Handle mouse release to trigger action."""
        self.triggered.emit()
        event.accept()  # Accept the event
        
    def mousePressEvent(self, event):
        """Accept mouse press to prevent it from closing the menu."""
        event.accept()
        
    def mouseMoveEvent(self, event):
        """Accept mouse move events to keep menu tracking working."""
        event.accept()


from ui.components.command_palette import CommandPalette
from ui.components.title_bar import TitleBar
from ui.tools.system_info import SystemInfoWidget


class MainWindow(QMainWindow):
    theme_changed = Signal(str)
    tool_opened = Signal(str)
    language_changed = Signal(str)  # Sprachcode
    delete_custom_language_requested = Signal(str)  # Signal to delete custom language

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        # Cache for rendered emoji icons
        self._emoji_icon_cache = {}
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(1200, 800)
        self.showMaximized()

        self.current_theme = "light"
        self.i18n_service = None  # Wird vom Controller gesetzt
        # Cache for SVG flag icons (lazy loading)
        self._flag_icon_cache = {}
        self._init_ui()

    def _init_ui(self):
        # Qt-Icon-Anzeige erzwingen vor der UI-Erstellung
        from PySide6.QtWidgets import QApplication
        app = QApplication.instance()
        if app:
            # Setze Qt-Style, der Icons unterstützt
            from PySide6.QtWidgets import QStyleFactory
            if 'Fusion' in QStyleFactory.keys():
                app.setStyle('Fusion')
        
        # Main Container (Rounded corners simulation)
        self.central_widget = QWidget()
        self.central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 1. Custom Title Bar
        self.title_bar = TitleBar(self)
        self.main_layout.addWidget(self.title_bar)

        # 2. Menu Bar
        self.menu_bar = self._create_menu_bar()
        self.main_layout.addWidget(self.menu_bar)

        # 3. Main Content Area (Top-Level Tabs)
        self.main_tab_widget = QTabWidget()
        self.main_tab_widget.setObjectName("MainTabs")
        self.main_tab_widget.setTabPosition(QTabWidget.North)
        self.main_tab_widget.setTabsClosable(True)
        self.main_tab_widget.tabCloseRequested.connect(self._close_main_tab)
        self.main_layout.addWidget(self.main_tab_widget)

        # Initialize Tools (Populate Menu)
        self._init_tools()

        # References to dynamic tabs
        self.cockpit_tab = None
        self.cockpit_dashboard = None
        self.dock_host_cockpit = None
        self.media_tab = None
        self.dock_host_media = None

        # Command Palette
        self.command_palette = CommandPalette(self)
        self.command_palette.action_triggered.connect(self._execute_command)

        # Global Shortcut Ctrl+P
        self.shortcut_palette = QShortcut(QKeySequence("Ctrl+P"), self)
        self.shortcut_palette.activated.connect(self.show_command_palette)

    def _create_menu_bar(self):
        menubar = QMenuBar(self)

        # Datei-Menü
        self.file_menu = menubar.addMenu(self.tr("menu.file", "Datei"))
        self.file_new = QAction(self.tr("menu_file.new", "Neu"), self)
        self.file_new.setToolTip(
            self.tr(
                "tooltips.file_new", "Erstellt eine neue Datei oder ein neues Projekt."
            )
        )
        self.file_open = QAction(self.tr("menu_file.open", "Öffnen..."), self)
        self.file_open.setToolTip(
            self.tr("tooltips.file_open", "Öffnet eine vorhandene Datei.")
        )
        self.file_save = QAction(self.tr("menu_file.save", "Speichern"), self)
        self.file_save.setToolTip(
            self.tr("tooltips.file_save", "Speichert die aktuellen Änderungen.")
        )
        self.file_exit = QAction(self.tr("menu_file.exit", "Beenden"), self)
        self.file_exit.setToolTip(
            self.tr("tooltips.file_exit", "Beendet die Anwendung.")
        )
        self.file_exit.triggered.connect(self.close)
        self.file_menu.addActions([self.file_new, self.file_open, self.file_save])
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.file_exit)
        self.file_menu.setToolTipsVisible(True)

        # Bearbeiten-Menü
        self.edit_menu = menubar.addMenu(self.tr("menu.edit", "Bearbeiten"))
        self.edit_undo = QAction(self.tr("menu_edit.undo", "Rückgängig"), self)
        self.edit_undo.setToolTip(
            self.tr("tooltips.edit_undo", "Macht die letzte Aktion rückgängig.")
        )
        self.edit_redo = QAction(self.tr("menu_edit.redo", "Wiederholen"), self)
        self.edit_redo.setToolTip(
            self.tr(
                "tooltips.edit_redo",
                "Wiederholt die letzte rückgängig gemachte Aktion.",
            )
        )
        self.edit_menu.addActions([self.edit_undo, self.edit_redo])
        self.edit_menu.setToolTipsVisible(True)

        # Werkzeuge-Menü
        self.tools_menu = menubar.addMenu(self.tr("menu.tools", "Werkzeuge"))
        self.tools_menu.setToolTipsVisible(True)

        # Einstellungen-Menü (NEU - zwischen Werkzeuge und Hilfe)
        self.settings_menu = menubar.addMenu(self.tr("menu.settings", "Einstellungen"))
        self.settings_menu.setToolTipsVisible(True)
        self._init_settings_menu()

        # Hilfe-Menü
        self.help_menu = menubar.addMenu(self.tr("menu.help", "Hilfe"))
        self.help_about = QAction(
            self.tr("dialogs.about.title", "Über MacGyver Multi-Tool"), self
        )
        self.help_about.setToolTip(
            self.tr("tooltips.help_about", "Zeigt Informationen über die Anwendung an.")
        )
        self.help_about.triggered.connect(self.show_about_dialog)
        self.help_menu.addAction(self.help_about)
        self.help_menu.setToolTipsVisible(True)

        self.help_menu.setToolTipsVisible(True)

        # Install Event Filter for reliable Tooltips on top-level items
        menubar.installEventFilter(self)
        menubar.setMouseTracking(True)

        return menubar

    def eventFilter(self, obj, event):
        """Custom event filter to handle tooltips reliably and smoothly."""
        if obj == self.menu_bar:
            # Handle ToolTip events
            if event.type() == QEvent.ToolTip:
                # Find the action at the mouse position
                action = self.menu_bar.actionAt(event.pos())
                if action and action.menu():
                    # It's a top-level menu (like File, Edit, Tools)
                    menu = action.menu()
                    tooltip_text = menu.toolTip()

                    if tooltip_text:
                        # Get the action's geometry for the bounding rectangle
                        # This prevents the tooltip from flickering as mouse moves within the same menu button
                        action_rect = self.menu_bar.actionGeometry(action)

                        # Show tooltip with bounding rectangle
                        # The tooltip will stay visible as long as mouse is within this rectangle
                        QToolTip.showText(
                            event.globalPos(), tooltip_text, self.menu_bar, action_rect
                        )
                        return True
                    else:
                        QToolTip.hideText()
                        return True

            # Handle HoverMove to update tooltips smoothly when moving between menu items
            elif event.type() in (QEvent.HoverMove, QEvent.HoverEnter):
                action = self.menu_bar.actionAt(event.pos())
                if action and action.menu():
                    menu = action.menu()
                    tooltip_text = menu.toolTip()

                    if tooltip_text:
                        action_rect = self.menu_bar.actionGeometry(action)
                        # Small delay before showing to avoid premature tooltips
                        # but we show immediately if already hovering over menu bar
                        QToolTip.showText(
                            self.menu_bar.mapToGlobal(event.pos()),
                            tooltip_text,
                            self.menu_bar,
                            action_rect,
                        )

        # Handle Right-Click on Custom Language Menu
        elif (
            event.type() == QEvent.MouseButtonPress and event.button() == Qt.RightButton
        ):
            if hasattr(self, "custom_menu") and obj == self.custom_menu:
                action = self.custom_menu.actionAt(event.pos())
                if action and action.data():
                    self._show_context_menu_for_language(
                        action, event.globalPosition().toPoint()
                    )
                    return True

        return super().eventFilter(obj, event)

    def _show_context_menu_for_language(self, action, pos):
        """Shows a context menu to delete a custom language."""
        from PySide6.QtWidgets import QMenu

        menu = QMenu(self)
        delete_action = QAction(
            "🗑️ " + self.tr("menu.delete_language", "Sprache löschen"), self
        )

        lang_code = action.data()

        def trigger_delete():
            self.delete_custom_language_requested.emit(lang_code)

        delete_action.triggered.connect(trigger_delete)
        menu.addAction(delete_action)
        menu.exec(pos)

    # Mapping for language group names to translation keys
    GROUP_NAME_MAPPING = {
        "🇩🇪 Deutsch": "menu_languages.german",
        "🌍 Hauptsprachen": "menu_languages.main",
        "Standard & Historisch": "menu_languages.standard",
        "Ostdeutsch (DDR-Erbe)": "menu_languages.east_legacy",
        "Historische Ostgebiete": "menu_languages.historical_east",
        "Diaspora & Auswanderer": "menu_languages.diaspora",
        "Süddeutsch/Alpin": "menu_languages.south_alpine",
        "Nord-/Westdeutsch": "menu_languages.north_west",
        "Städtisch": "menu_languages.urban",
        "Auslandsdeutsch": "menu_languages.abroad",
        "Europäisch": "menu_languages.european",
        "Asiatisch": "menu_languages.asian",
        "Naher Osten & Afrika": "menu_languages.middle_east",
        "Bonus": "menu_languages.bonus",
        "Sonstige": "menu_languages.other",
    }

    def _init_settings_menu(self):
        """Initialisiert das Einstellungen-Menü mit hierarchischer Sprachauswahl und Ansicht."""
        # Ansicht-Untermenü (Verschoben von Hauptmenü)
        self.view_menu = self.settings_menu.addMenu(self.tr("menu.view", "Ansicht"))
        self.theme_light = QAction(
            self.tr("menu_view.theme_light", "Helles Design"), self
        )
        self.theme_light.setToolTip(
            self.tr("tooltips.theme_light", "Wechselt zum hellen Erscheinungsbild.")
        )
        self.theme_dark = QAction(
            self.tr("menu_view.theme_dark", "Dunkles Design"), self
        )
        self.theme_dark.setToolTip(
            self.tr("tooltips.theme_dark", "Wechselt zum dunklen Erscheinungsbild.")
        )
        self.theme_light.triggered.connect(lambda: self.theme_changed.emit("light"))
        self.theme_dark.triggered.connect(lambda: self.theme_changed.emit("dark"))
        self.view_menu.addActions([self.theme_light, self.theme_dark])

        self.settings_menu.addSeparator()

        # Sprachen-Untermenü (HIERARCHISCH mit LANGUAGE_GROUPS)
        self.languages_menu = self.settings_menu.addMenu(
            self.tr("menu.languages", "Sprachen")
        )
        self.languages_menu.setToolTip(
            self.tr(
                "tooltips.menu_languages",
                "Sprache auswählen: Aus 147 Varianten wählen - Hauptsprachen, regionale Dialekte, Bonus-Sprachen.",
            )
        )
        
        self._populate_languages_menu()

    def _resolve_flag_path(self, lang_code: str, i18n_service=None) -> Path:
        """Ermittelt den Pfad zur Flaggen-Datei (SVG oder PNG)."""
        try:
            service = i18n_service or self.i18n_service
            if not service or not hasattr(service, "flags"):
                return None

            # Country-Code holen oder ableiten
            country_code = service.flags.get(lang_code, "")
            if not country_code:
                if "_" in lang_code:
                    country_code = lang_code.split("_")[-1]
                else:
                    country_code = lang_code

            country_code = (country_code or "").lower()

            # Kandidatenliste aufbauen
            candidates = []
            seen = set()

            def add_candidate(code):
                code = (code or "").strip().lower()
                if code and code not in seen:
                    seen.add(code)
                    candidates.append(code)

            add_candidate(country_code)
            
            # Spezielle Zuordnungen
            special_cases = {
                "ta": "sh", "bv": "no", "hm": "au", "tf": "fr", "gs": "gb",
                "um": "us", "io": "gb", "bl": "fr", "mf": "fr", "sx": "nl",
                "bq": "nl", "cw": "nl", "ax": "fi", "gg": "gb", "im": "gb",
                "je": "gb", "xk": "un"
            }
            if country_code in special_cases:
                add_candidate(special_cases[country_code])

            # Varianten wie es-vc
            if "-" in country_code:
                parts = country_code.split("-")
                add_candidate(parts[0])
                if len(parts[-1]) == 2:
                    add_candidate(parts[-1])
            if "_" in country_code:
                parts = country_code.split("_")
                add_candidate(parts[0])
                if len(parts[-1]) == 2:
                    add_candidate(parts[-1])

            # Basissprache
            if "_" in lang_code:
                add_candidate(lang_code.split("_")[0])

            # Kürzungs-Fallback
            if len(country_code) > 2:
                add_candidate(country_code[:2])

            # Versuche PNG/SVG zu finden
            assets_dir = Path(__file__).parent.parent / "assets" / "flags"
            for candidate in candidates:
                for ext in [".png", ".svg"]:
                    flag_path = assets_dir / f"{candidate}{ext}"
                    if flag_path.exists() and flag_path.is_file():
                        return flag_path
            
            return None

        except Exception as e:
            print(f"[FEHLER] Flaggen-Pfad {lang_code}: {e}")
            return None

    def _load_flag_icon(self, lang_code: str, i18n_service=None) -> QIcon:
        """Lädt das Flaggen-Icon für den angegebenen Sprachcode."""
        # Cache prüfen
        if lang_code in self._flag_icon_cache:
            return self._flag_icon_cache[lang_code]

        empty_icon = QIcon()
        
        flag_path = self._resolve_flag_path(lang_code, i18n_service)
        if flag_path:
            try:
                icon = QIcon(str(flag_path))
                if not icon.isNull():
                    pixmap = icon.pixmap(16, 16)
                    if not pixmap.isNull():
                        icon = QIcon(pixmap)
                        self._flag_icon_cache[lang_code] = icon
                        return icon
            except:
                pass

        self._flag_icon_cache[lang_code] = empty_icon
        return empty_icon

    def _populate_languages_menu(self):
        """Baut das Sprachmenü mit Standard- und benutzerdefinierten Sprachen auf."""
        self.languages_menu.clear()

        # Initialisiere Dictionaries für Aktionen und Untermenüs
        self.language_actions = {}
        self.language_submenus = {}

        # Importiere i18n Service für hierarchische Sprachstruktur
        i18n_temp = None
        try:
            from core.services.i18n_service import I18nService
            i18n_temp = I18nService()
            language_groups = i18n_temp.get_language_groups()
            print(f"[UI] {len(language_groups)} Sprachgruppen geladen")
        except Exception as e:
            print(f"[FEHLER] Kann Sprachgruppen nicht laden: {e}")
            # Fallback zu einfacher Sprachliste
            language_groups = {
                "🇩🇪 Deutsch": {"Standard": {"de": "Hochdeutsch"}},
                "🌍 Hauptsprachen": {"International": {"en": "English"}}
            }

        # Rekursive Funktion zum Erstellen der Menüstruktur
        def is_leaf_dict(d):
            """Überprüft, ob es sich um ein Blatt-Dictionary handelt (Sprachcodes → Namen)."""
            if not isinstance(d, dict):
                return False
            # A leaf dict has ALL string values (lang_code: lang_name)
            return all(isinstance(v, str) for v in d.values())
        
        def is_language_entry(d):
            """Überprüft, ob ein Dictionary ein Spracheintrag ist (enthält 'Standard', 'Dialekte', 'Pirate' etc.)."""
            if not isinstance(d, dict):
                return False
            # Check if this dict contains categories like 'Standard', 'Dialekte', 'Pirate'
            common_keys = {'Standard', 'Dialekte', 'Pirate', 'Regional', 'Städtisch', 'Historisch'}
            return any(key in d for key in common_keys)

        def build_menu(parent_menu, tree, parent_name=""):
            """Baut das Menü rekursiv auf."""
            import re
            
            for name, sub in tree.items():
                if is_leaf_dict(sub):
                    # Blattknoten: Erstelle Aktionen für Sprachcodes
                    for lang_code, lang_name in sub.items():
                        try:
                            # Basisname (native) ermitteln, ggf. Fallback
                            base_name = i18n_temp.get_base_language_name(lang_code) if i18n_temp else lang_name
                            
                            # Übersetzten Namen holen
                            tr_lang_name = self.i18n_service.tr(f"lang.{lang_code}", base_name) if self.i18n_service else base_name
                            
                            # Entferne evtl. Emojis aus dem übersetzten Namen
                            tr_lang_name = re.sub(r'[\U0001F1E6-\U0001F1FF]{2,}', '', tr_lang_name)
                            tr_lang_name = re.sub(r'[\U0001F300-\U0001F9FF]+', '', tr_lang_name)
                            tr_lang_name = tr_lang_name.strip()
                            
                            # Kombiniere übersetzten Namen mit dem nativen Namen
                            # Ausnahme: Wenn es die aktuell ausgewählte UI-Sprache ist, nur übersetzten Namen zeigen
                            if self.i18n_service and lang_code == self.i18n_service.current_language:
                                display_name = tr_lang_name
                            else:
                                display_name = f"{tr_lang_name} ({base_name})" if base_name else tr_lang_name
                            
                            # Flaggen-Pfad ermitteln
                            flag_path = self._resolve_flag_path(lang_code, i18n_service=i18n_temp)
                            
                            # QWidgetAction und LanguageMenuItem erstellen
                            action = QWidgetAction(self)
                            item_widget = LanguageMenuItem(display_name, flag_path)
                            action.setDefaultWidget(item_widget)
                            action.setToolTip(f"{display_name} ({lang_code})")
                            
                            def trigger_handler(checked=False, code=lang_code):
                                self._on_language_selected(code)
                            
                            item_widget.triggered.connect(trigger_handler)
                            parent_menu.addAction(action)
                            self.language_actions[lang_code] = action
                            
                        except Exception as e:
                            print(f"[FEHLER] Kann Sprache {lang_code} nicht hinzufügen: {e}")
                            continue
                
                elif is_language_entry(sub):
                    # This is a language entry containing categories (Standard, Dialekte, etc.)
                    # Create a submenu for this entry to avoid conflicts between categories
                    tr_sub_key = self.GROUP_NAME_MAPPING.get(name, name)
                    tr_sub_name = self.tr(tr_sub_key, name)
                    sub_menu = parent_menu.addMenu(tr_sub_name)
                    self.language_submenus[name] = sub_menu
                    # Add the categories to the submenu
                    build_menu(sub_menu, sub, name)
                            
                elif isinstance(sub, dict):
                    # Untermenü: Übersetze den Namen und rufe die Funktion rekursiv auf
                    tr_sub_key = self.GROUP_NAME_MAPPING.get(name, name)
                    tr_sub_name = self.tr(tr_sub_key, name)
                    
                    # Erstelle das Untermenü mit einem dezenten Icon
                    sub_menu = parent_menu.addMenu(tr_sub_name)
                    
                    # Optional: Füge ein passendes Icon für die Kategorie hinzu
                    if '🇩🇪' in name:
                        sub_menu.setIcon(QIcon(":/icons/languages/germany.png"))
                    elif '🌍' in name:
                        sub_menu.setIcon(QIcon(":/icons/languages/earth.png"))
                    
                    self.language_submenus[name] = sub_menu
                    build_menu(sub_menu, sub, name)

        # Hauptmenüstruktur aufbauen
        for group_name, group_content in language_groups.items():
            # Gruppennamen übersetzen
            tr_key = self.GROUP_NAME_MAPPING.get(group_name, group_name)
            tr_name = self.tr(tr_key, group_name)

            group_menu = self.languages_menu.addMenu(tr_name)
            self.language_submenus[group_name] = group_menu
            build_menu(group_menu, group_content, group_name)

        print(f"[UI] {len(self.language_actions)} Sprachoptionen geladen")

        # Benutzerdefinierte Sprachen hinzufügen, falls vorhanden
        if i18n_temp:
            try:
                custom_langs = i18n_temp.get_custom_languages()
                if custom_langs:
                    self.custom_menu = self.languages_menu.addMenu(
                        "🆕 " + self.tr("menu_languages.custom", "Hinzugefügte Sprachen")
                    )
                    # Event-Filter für Rechtsklick-Löschen
                    self.custom_menu.installEventFilter(self)

                    for lang_code, lang_data in custom_langs.items():
                        lang_name = lang_data.get("language_name", lang_code)
                        action = QAction(f"{lang_name} ⭐", self, checkable=True)
                        action.setData(lang_code)
                        action.triggered.connect(
                            lambda checked=False, code=lang_code: 
                                self._on_language_selected(code)
                        )
                        self.custom_menu.addAction(action)
                        self.language_actions[lang_code] = action
                    print(f"[UI] {len(custom_langs)} benutzerdefinierte Sprachen geladen")
            except Exception as e:
                print(f"[FEHLER] Kann benutzerdefinierte Sprachen nicht laden: {e}")

        # Trennlinie vor den Bearbeitungsoptionen
        self.languages_menu.addSeparator()

        # Übersetzungs-Editor
        self.edit_translations_action = QAction("✏️ " + self.tr("menu.translations_editor", "Übersetzungen bearbeiten..."), self)
        self.edit_translations_action.setToolTip(
            self.tr("tooltips.translations_editor", "Übersetzungen für alle Sprachen bearbeiten")
        )
        self.edit_translations_action.triggered.connect(self._open_translation_editor)
        self.languages_menu.addAction(self.edit_translations_action)

        # Neue Sprache erstellen
        self.create_language_action = QAction("➕ " + self.tr("menu.create_language", "Neue Sprache erstellen..."), self)
        self.create_language_action.setToolTip(
            self.tr("tooltips.create_language", "Erstellt eine neue benutzerdefinierte Sprache")
        )
        self.create_language_action.triggered.connect(self._open_create_language_dialog)
        self.languages_menu.addAction(self.create_language_action)

    def refresh_language_menu(self):
        """Refreshes the language menu."""
        self._populate_languages_menu()

    def _on_language_selected(self, lang_code: str):
        """Handler for language selection from menu."""
        print(f"[UI] Language selected: {lang_code}")
        self.language_changed.emit(lang_code)

    def set_current_language(self, lang_code: str):
        """Setzt die aktuelle Sprache und aktualisiert Checkmarks."""
        if hasattr(self, "language_actions") and lang_code in self.language_actions:
            for code, action in self.language_actions.items():
                action.setChecked(code == lang_code)

    def set_i18n_service(self, i18n_service):
        """Setzt den i18n Service für Übersetzungen."""
        self.i18n_service = i18n_service
        # Refresh all UI texts to reflect the newly set language
        self.update_ui_language()

    def tr(self, key: str, default: str = None) -> str:
        """Hilfsfunktion für Übersetzungen."""
        if self.i18n_service:
            return self.i18n_service.tr(key, default)
        return default if default else key

    def update_ui_language(self):
        """Aktualisiert alle UI-Texte bei Sprachwechsel."""
        print(
            f"[DEBUG] update_ui_language called. Current lang in service: {self.i18n_service.current_language if self.i18n_service else 'None'}"
        )
        if not self.i18n_service:
            return

        # Aktualisiere Checkmarks
        if hasattr(self.i18n_service, "current_language"):
            self.set_current_language(self.i18n_service.current_language)

        # Aktualisiere Menü-Texte
        self._update_menu_texts()

        # Aktualisiere Tab-Texte
        self._update_tab_texts()

    def _update_menu_texts(self):
        """Aktualisiert alle Menü-Texte."""
        if hasattr(self, "file_menu"):
            self.file_menu.setTitle(self.tr("menu.file", "Datei"))
            self.file_menu.setToolTip(
                self.tr("tooltips.menu_file", "Befehle zur Dateiverwaltung.")
            )
            self.file_new.setText(self.tr("menu_file.new", "Neu"))
            self.file_new.setToolTip(
                self.tr(
                    "tooltips.file_new",
                    "Erstellt eine neue Datei oder ein neues Projekt.",
                )
            )
            self.file_open.setText(self.tr("menu_file.open", "Öffnen..."))
            self.file_open.setToolTip(
                self.tr("tooltips.file_open", "Öffnet eine vorhandene Datei.")
            )
            self.file_save.setText(self.tr("menu_file.save", "Speichern"))
            self.file_save.setToolTip(
                self.tr("tooltips.file_save", "Speichert die aktuellen Änderungen.")
            )
            self.file_exit.setText(self.tr("menu_file.exit", "Beenden"))
            self.file_exit.setToolTip(
                self.tr("tooltips.file_exit", "Beendet die Anwendung.")
            )

        if hasattr(self, "edit_menu"):
            self.edit_menu.setTitle(self.tr("menu.edit", "Bearbeiten"))
            self.edit_menu.setToolTip(
                self.tr(
                    "tooltips.menu_edit",
                    "Inhalt bearbeiten und Aktionen rückgängig machen.",
                )
            )
            self.edit_undo.setText(self.tr("menu_edit.undo", "Rückgängig"))
            self.edit_undo.setToolTip(
                self.tr("tooltips.edit_undo", "Macht die letzte Aktion rückgängig.")
            )
            self.edit_redo.setText(self.tr("menu_edit.redo", "Wiederholen"))
            self.edit_redo.setToolTip(
                self.tr(
                    "tooltips.edit_redo",
                    "Wiederholt die letzte rückgängig gemachte Aktion.",
                )
            )

        if hasattr(self, "settings_menu"):
            self.settings_menu.setTitle(self.tr("menu.settings", "Einstellungen"))
            self.settings_menu.setToolTip(
                self.tr(
                    "tooltips.menu_settings", "Anwendungseinstellungen konfigurieren."
                )
            )

            # Ansicht-Untermenü aktualisieren
            if hasattr(self, "view_menu"):
                self.view_menu.setTitle(self.tr("menu.view", "Ansicht"))
                self.view_menu.setToolTip(
                    self.tr("tooltips.menu_view", "Erscheinungsbild und Design ändern.")
                )
                self.theme_light.setText(
                    self.tr("menu_view.theme_light", "Helles Design")
                )
                self.theme_light.setToolTip(
                    self.tr(
                        "tooltips.theme_light", "Wechselt zum hellen Erscheinungsbild."
                    )
                )

        if hasattr(self, "help_menu"):
            self.help_menu.setTitle(self.tr("menu.help", "Hilfe"))

        # Sprachen-Menü
        if hasattr(self, "languages_menu"):
            self.languages_menu.setTitle(self.tr("menu.languages", "Sprachen"))
            self.languages_menu.setToolTip(
                self.tr("tooltips.menu_languages", "Sprache auswählen.")
            )

            # Update Language Submenus (Categories)
            if hasattr(self, "language_submenus"):
                for group_name, menu in self.language_submenus.items():
                    # Translate group name using the mapping
                    tr_key = self.GROUP_NAME_MAPPING.get(group_name, group_name)
                    tr_name = self.tr(tr_key, group_name)
                    menu.setTitle(tr_name)

            # Update Language Actions (Names) — use base names without emoji so fonts don't show 'US'/'GB'
            if hasattr(self, "language_actions") and self.i18n_service:
                for lang_code, action in self.language_actions.items():
                        base_name = self.i18n_service.get_base_language_name(lang_code)
                        tr_name = self.tr(f"lang.{lang_code}", base_name)
                        action.setText(tr_name)
                        # Also update icon from the authoritative i18n service
                        try:
                            svg_path = Path(__file__).parent.parent / "assets" / "flags" / "svg" / f"{lang_code}.svg"
                            png_path = Path(__file__).parent.parent / "assets" / "flags" / f"{lang_code}.png"
                            if svg_path.exists():
                                action.setIcon(QIcon(str(svg_path)))
                            elif png_path.exists():
                                action.setIcon(QIcon(str(png_path)))
                            else:
                                flag = self.i18n_service.get_flag(lang_code)
                                if flag:
                                    icon = self._emoji_to_icon(flag, 18)
                                    if icon:
                                        action.setIcon(icon)
                                else:
                                    action.setIcon(QIcon())
                            try:
                                action.setIconVisibleInMenu(True)
                            except Exception:
                                pass
                        except Exception:
                            pass

        # Werkzeuge-Menü (Tools)
        if hasattr(self, "tools_menu"):
            self.tools_menu.setTitle(self.tr("menu.tools", "Werkzeuge"))
            self.tools_menu.setToolTip(
                self.tr("tooltips.menu_tools", "Zugriff auf verschiedene Werkzeuge.")
            )

        # Cockpit-Menü
        self.cockpit_menu.setTitle(self.tr("menu_tools.cockpit", "Cockpit"))
        self.cockpit_menu.setToolTip(
            self.tr("tooltips.menu_cockpit", "Dashboard- und Überwachungstools.")
        )
        if hasattr(self, "add_widget_action"):
            self.add_widget_action.setText(
                self.tr("menu_tools.add_widget", "➕ Widget hinzufügen...")
            )
            self.add_widget_action.setToolTip(
                self.tr(
                    "tooltips.add_widget", "Fügt ein neues Widget zum Dashboard hinzu."
                )
            )

        # Media-Menü
        self.media_menu.setTitle(self.tr("menu_tools.media", "Media"))
        self.media_menu.setToolTip(
            self.tr("tooltips.menu_media", "Medienplayer und Steuerung.")
        )

        # Tabs-Menü
        self.tab_menu.setTitle(self.tr("menu_tools.tabs", "Tabs"))
        self.tab_menu.setToolTip(
            self.tr("tooltips.menu_tabs", "Tabs und Fenster verwalten.")
        )

        # Aktualisiere Tool-Aktionen
        if hasattr(self, "tool_actions"):
            tool_translations = {
                "system_info": "menu_tools.system_monitor",
                "clock": "menu_tools.clock",
                "network_monitor": "menu_tools.network_traffic",
                "gpu_monitor": "menu_tools.gpu_monitor",
                "temp_monitor": "menu_tools.temperature",
                "disk_monitor": "menu_tools.disk_io",
                "media_controls": "menu_tools.media_controls",
                "video_screen": "menu_tools.video_screen",
                "media_explorer": "menu_tools.media_explorer",
                "stream_window": "menu_tools.stream",
                "equalizer": "menu_tools.equalizer",
                "file_manager": "menu_tools.file_manager",
                "network_diag": "menu_tools.network_diag",
            }

            for tool_id, (action, menu) in self.tool_actions.items():
                if tool_id in tool_translations:
                    # Update Text
                    action.setText(self.tr(tool_translations[tool_id], action.text()))
                    # Update Tooltip (Generic fallback for now, or specific keys if added later)
                    # For now, we use the translated name as tooltip or a generic "Open [Tool Name]"
                    action.setToolTip(
                        self.tr(
                            "tooltips.open_tool", "Öffnet das Werkzeug: {tool}"
                        ).format(tool=action.text())
                    )

    def _update_tab_texts(self):
        """Aktualisiert Tab-Texte."""
        if hasattr(self, "main_tab_widget"):
            # Cockpit Tab
            if self.cockpit_tab:
                idx = self.main_tab_widget.indexOf(self.cockpit_tab)
                if idx >= 0:
                    self.main_tab_widget.setTabText(
                        idx, self.tr("tabs.cockpit", "Cockpit")
                    )

            # Media Tab
            if self.media_tab:
                idx = self.main_tab_widget.indexOf(self.media_tab)
                if idx >= 0:
                    self.main_tab_widget.setTabText(
                        idx, self.tr("tabs.media_commander", "Media Commander")
                    )

    def _init_tools(self):
        # Submenus
        self.cockpit_menu = self.tools_menu.addMenu(
            self.tr("menu_tools.cockpit", "Cockpit")
        )
        self.media_menu = self.tools_menu.addMenu(self.tr("menu_tools.media", "Media"))
        self.tab_menu = self.tools_menu.addMenu(self.tr("menu_tools.tabs", "Tabs"))

        # Cockpit Tools
        # Add Widget Action
        self.add_widget_action = QAction(
            self.tr("menu_tools.add_widget", "➕ Widget hinzufügen..."), self
        )
        self.add_widget_action.triggered.connect(
            lambda: self.tool_opened.emit("add_widget")
        )
        self.cockpit_menu.addAction(self.add_widget_action)
        self.cockpit_menu.addSeparator()

        self.add_tool(
            self.tr("menu_tools.system_monitor", "System Monitor"),
            self.cockpit_menu,
            "system_info",
        )
        self.add_tool(
            self.tr("menu_tools.clock", "Weltzeituhr"), self.cockpit_menu, "clock"
        )
        self.add_tool(
            self.tr("menu_tools.network_traffic", "Netzwerk-Traffic"),
            self.cockpit_menu,
            "network_monitor",
        )
        self.add_tool(
            self.tr("menu_tools.gpu_monitor", "GPU-Monitor"),
            self.cockpit_menu,
            "gpu_monitor",
        )
        self.add_tool(
            self.tr("menu_tools.temperature", "Temperatur"),
            self.cockpit_menu,
            "temp_monitor",
        )
        self.add_tool(
            self.tr("menu_tools.disk_io", "Datenträger I/O"),
            self.cockpit_menu,
            "disk_monitor",
        )

        # Media Tools
        self.add_tool(
            self.tr("menu_tools.media_controls", "Medien-Steuerung"),
            self.media_menu,
            "media_controls",
        )
        self.add_tool(
            self.tr("menu_tools.video_screen", "Video-Screen"),
            self.media_menu,
            "video_screen",
        )
        self.add_tool(
            self.tr("menu_tools.media_explorer", "Medien-Explorer"),
            self.media_menu,
            "media_explorer",
        )
        self.add_tool(
            self.tr("menu_tools.stream", "Online Stream"),
            self.media_menu,
            "stream_window",
        )
        self.add_tool(
            self.tr("menu_tools.equalizer", "Equalizer"), self.media_menu, "equalizer"
        )

        # Tab Tools
        self.add_tool(
            self.tr("menu_tools.file_manager", "Dateiverwaltung"),
            self.tab_menu,
            "file_manager",
        )
        self.add_tool(
            self.tr("menu_tools.network_diag", "Netzwerkdiagnose"),
            self.tab_menu,
            "network_diag",
        )

    def add_tool(self, name, parent_menu, tool_id):
        action = QAction(name, self)
        action.triggered.connect(lambda: self.tool_opened.emit(tool_id))
        # Initial Tooltip
        action.setToolTip(
            self.tr("tooltips.open_tool", "Öffnet das Werkzeug: {tool}").format(
                tool=name
            )
        )
        parent_menu.addAction(action)
        # Speichere Referenz für spätere Aktualisierung
        if not hasattr(self, "tool_actions"):
            self.tool_actions = {}
        self.tool_actions[tool_id] = (action, parent_menu)

    def _emoji_to_icon(self, emoji: str, size: int = 16) -> QIcon:
        """Render a short emoji string to a QIcon using an emoji-capable font.

        This avoids relying on the system menu font supporting color emoji.
        """
        try:
            pix = QPixmap(size, size)
            pix.fill(Qt.transparent)
            painter = QPainter(pix)
            # Use a font likely to support emoji on Windows; fall back to default
            font = QFont("Segoe UI Emoji", max(10, int(size * 0.8)))
            painter.setFont(font)
            painter.setPen(Qt.black)
            # Center the emoji in the pixmap
            rect = pix.rect()
            painter.drawText(rect, Qt.AlignCenter, emoji)
            painter.end()
            return QIcon(pix)
        except Exception:
            return QIcon()

    def _ensure_cockpit_dashboard(self):
        if self.cockpit_tab is None:
            from ui.tools.dashboard import DashboardWidget

            self.cockpit_dashboard = DashboardWidget()
            self.cockpit_tab = self.cockpit_dashboard

            # Add to main tabs
            self.main_tab_widget.insertTab(
                0, self.cockpit_tab, self.tr("tabs.cockpit", "Cockpit")
            )

        # Ensure visible
        if self.main_tab_widget.indexOf(self.cockpit_tab) == -1:
            self.main_tab_widget.insertTab(0, self.cockpit_tab, "Cockpit")

    def _ensure_media_exists(self):
        if self.media_tab is None:
            self.media_tab = QWidget()
            layout = QVBoxLayout(self.media_tab)
            layout.setContentsMargins(0, 0, 0, 0)

            self.dock_host_media = QMainWindow()
            self.dock_host_media.setWindowFlags(Qt.Widget)
            self.dock_host_media.setDockOptions(
                QMainWindow.AllowTabbedDocks
                | QMainWindow.AnimatedDocks
                | QMainWindow.AllowNestedDocks
            )

            bg = QLabel("Media Commander\n(Player, Equalizer, Streams hier andocken)")
            bg.setAlignment(Qt.AlignCenter)
            bg.setObjectName("WorkspaceBackground")
            self.dock_host_media.setCentralWidget(bg)

            layout.addWidget(self.dock_host_media)
            # Insert after Cockpit if exists, else at 0, or just append?
            # Let's just append or insert at 1.
            index = (
                1
                if self.cockpit_tab
                and self.main_tab_widget.indexOf(self.cockpit_tab) != -1
                else 0
            )
            self.main_tab_widget.insertTab(
                index,
                self.media_tab,
                self.tr("tabs.media_commander", "Media Commander"),
            )

        if self.main_tab_widget.indexOf(self.media_tab) == -1:
            self.main_tab_widget.addTab(self.media_tab, "Media Commander")

    def add_tool_tab(self, title, widget, target="tab"):
        """
        Adds a tool to the specified target area.
        target: 'cockpit', 'media', or 'tab'
        """
        if target == "cockpit":
            self._ensure_cockpit_dashboard()
            # Add as dock widget to cockpit
            if hasattr(self, "cockpit_dashboard") and self.cockpit_dashboard:
                self.cockpit_dashboard.add_widget(widget)

        elif target == "media":
            self._ensure_media_exists()
            # Add as dock to media
            dock = QDockWidget(title, self.dock_host_media)
            dock.setWidget(widget)
            dock.setObjectName(f"MediaDock_{title}")
            self.dock_host_media.addDockWidget(Qt.RightDockWidgetArea, dock)

        else:  # target == "tab"
            # Add as top-level tab
            self.main_tab_widget.addTab(widget, title)

    def _close_main_tab(self, index):
        # Don't allow closing Cockpit or Media Commander tabs
        widget = self.main_tab_widget.widget(index)
        if widget == self.cockpit_tab or widget == self.media_tab:
            return

        self.main_tab_widget.removeTab(index)
        widget.deleteLater()

    def show_about_dialog(self):
        title = self.tr("dialogs.about.title", "Über MacGyver Multi-Tool")
        version = self.tr("dialogs.about.version", "Version 1.0 (MVP-Build)")
        description = self.tr(
            "dialogs.about.description", "Ein modulares Dienstprogramm im macOS-Design."
        )
        copyright_text = self.tr(
            "dialogs.about.copyright", "© 2025 Jan Friske – Alle Rechte vorbehalten."
        )
        license_text = self.tr(
            "dialogs.about.license", "Freeware-Lizenz (nicht kommerziell)."
        )

        message = f"{version}\n\n{description}\n\n{copyright_text}\n{license_text}"
        QMessageBox.about(self, title, message)

    def show_command_palette(self):
        """Collects all available actions and shows the palette."""
        actions = []

        # Menu Actions
        if hasattr(self, "file_new"):
            actions.append((f"Datei: {self.file_new.text()}", self.file_new))
        if hasattr(self, "file_open"):
            actions.append((f"Datei: {self.file_open.text()}", self.file_open))
        if hasattr(self, "file_save"):
            actions.append((f"Datei: {self.file_save.text()}", self.file_save))
        if hasattr(self, "file_exit"):
            actions.append((f"Datei: {self.file_exit.text()}", self.file_exit))

        if hasattr(self, "theme_light"):
            actions.append((f"Ansicht: {self.theme_light.text()}", self.theme_light))
        if hasattr(self, "theme_dark"):
            actions.append((f"Ansicht: {self.theme_dark.text()}", self.theme_dark))

        # Tools
        if hasattr(self, "tool_actions"):
            for tool_id, (action, _) in self.tool_actions.items():
                actions.append((f"Tool: {action.text()}", action))

        # Languages (Top 5 common or all?)
        # Let's add a generic "Switch Language" command or just a few major ones to avoid clutter
        # For now, let's add the current visible ones in the menu

        self.command_palette.set_actions(actions)
        self.command_palette.show_centered(self)

    def _execute_command(self, action):
        """Executes the action selected in the palette."""
        if isinstance(action, QAction):
            action.trigger()
        elif callable(action):
            action()

    def _open_translation_editor(self):
        """Opens the Translation Editor Dialog"""
        try:
            from ui.dialogs.translation_editor_dialog import TranslationEditorDialog

            dialog = TranslationEditorDialog(self.i18n_service, self)
            dialog.translation_changed.connect(self.update_ui_language)
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Failed to open Translation Editor:\n{str(e)}"
            )

    def _open_create_language_dialog(self):
        """Opens the Create Custom Language Dialog"""
        try:
            from core.services.custom_language_service import (
                get_custom_language_service,
            )
            from ui.dialogs.create_language_dialog import CreateLanguageDialog

            custom_lang_service = get_custom_language_service()

            dialog = CreateLanguageDialog(custom_lang_service, self.i18n_service, self)
            if dialog.exec():
                created_code = dialog.get_created_language_code()
                if created_code:
                    # Reload i18n service to include new custom language
                    self.i18n_service._load_custom_languages()
                    self.i18n_service._load_translations()

                    # Refresh UI
                    self.refresh_language_menu()

                    QMessageBox.information(
                        self,
                        "Language Created",
                        f"Custom language created: {created_code}\n\n"
                        "It now appears in '🆕 Hinzugefügte Sprachen'.\n"
                        "You can edit it in the Translation Editor.",
                    )
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Failed to open Create Language Dialog:\n{str(e)}"
            )
