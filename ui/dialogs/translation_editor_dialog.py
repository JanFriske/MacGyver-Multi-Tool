"""
Translation Editor Dialog
Allows users to customize translations for any language
Includes search, edit, import/export functionality
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QComboBox, QLineEdit, QLabel, QHeaderView, QMessageBox,
    QFileDialog, QGroupBox, QRadioButton, QButtonGroup
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from pathlib import Path
import json
from datetime import datetime
from core.services.translation_validator import get_validator
from core.services.custom_language_service import get_custom_language_service

class TranslationEditorDialog(QDialog):
    """Community Translation Editor"""
    
    translation_changed = Signal()  # Emit when translations are modified
    
    def __init__(self, i18n_service, parent=None):
        super().__init__(parent)
        self.i18n_service = i18n_service
        self.validator = get_validator()  # Import validator
        self.current_lang = "de"
        self.all_keys = []
        self.filtered_keys = []
        
        self.setWindowTitle(self.tr("Translation Editor"))
        self.setMinimumSize(1000, 700)
        
        self._init_ui()
        self._load_translation_keys()
        self._populate_table()
    
    def _init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout(self)
        
        # Top controls
        top_layout = QHBoxLayout()
        
        # Language selector
        lang_label = QLabel("Language:")
        self.lang_combo = QComboBox()
        self._populate_language_combo()
        self.lang_combo.currentTextChanged.connect(self._on_language_changed)
        
        # Search box
        search_label = QLabel("🔍 Search:")
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search by key or value...")
        self.search_edit.textChanged.connect(self._on_search_changed)
        
        top_layout.addWidget(lang_label)
        top_layout.addWidget(self.lang_combo, 1)
        top_layout.addSpacing(20)
        top_layout.addWidget(search_label)
        top_layout.addWidget(self.search_edit, 2)
        
        layout.addLayout(top_layout)
        
        # Main table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Key", 
            "🇩🇪 German (Reference)", 
            "🇬🇧 English (Reference)", 
            "Current Language", 
            "User Override", 
            "Actions"
        ])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setAlternatingRowColors(True)
        self.table.itemChanged.connect(self._on_item_changed)
        
        layout.addWidget(self.table)
        
        # Bottom controls
        bottom_layout = QHBoxLayout()
        
        # Save/Reset buttons
        self.save_btn = QPushButton("💾 Save All")
        self.save_btn.clicked.connect(self._save_all_changes)
        self.save_btn.setEnabled(False)
        
        self.reset_btn = QPushButton("🔄 Reset All")
        self.reset_btn.clicked.connect(self._reset_all_overrides)
        
        bottom_layout.addWidget(self.save_btn)
        bottom_layout.addWidget(self.reset_btn)
        bottom_layout.addStretch()
        
        layout.addLayout(bottom_layout)
        
        # Import/Export section
        ie_group = QGroupBox("Import/Export")
        ie_layout = QVBoxLayout()
        
        # Export options
        export_layout = QHBoxLayout()
        export_label = QLabel("📤 Export:")
        
        self.export_group = QButtonGroup()
        self.export_current = QRadioButton("Current Language")
        self.export_current.setChecked(True)
        self.export_all = QRadioButton("All Languages with Overrides")
        self.export_selected = QRadioButton("Selected Languages")
        
        self.export_group.addButton(self.export_current)
        self.export_group.addButton(self.export_all)
        self.export_group.addButton(self.export_selected)
        
        self.export_btn = QPushButton("Export as...")
        self.export_btn.clicked.connect(self._export_translations)
        
        export_layout.addWidget(export_label)
        export_layout.addWidget(self.export_current)
        export_layout.addWidget(self.export_all)
        export_layout.addWidget(self.export_selected)
        export_layout.addStretch()
        export_layout.addWidget(self.export_btn)
        
        ie_layout.addLayout(export_layout)
        
        # Import controls
        import_layout = QHBoxLayout()
        import_label = QLabel("📥 Import:")
        
        self.import_btn = QPushButton("Select File...")
        self.import_btn.clicked.connect(self._import_translations)
        
        import_layout.addWidget(import_label)
        import_layout.addWidget(self.import_btn)
        import_layout.addStretch()
        
        ie_layout.addLayout(import_layout)
        
        ie_layout.addLayout(import_layout)
        
        # Uplink Button
        uplink_layout = QHBoxLayout()
        self.uplink_btn = QPushButton("🚀 MacGyver Uplink (P2P Sync)")
        self.uplink_btn.setToolTip("Securely share translations via Magic Code")
        self.uplink_btn.clicked.connect(self._open_uplink_dialog)
        self.uplink_btn.setStyleSheet("font-weight: bold; color: #007aff;")
        uplink_layout.addWidget(self.uplink_btn)
        
        # Stats Button
        self.stats_btn = QPushButton("📊 Statistics")
        self.stats_btn.setToolTip("View translation coverage statistics")
        self.stats_btn.clicked.connect(self._open_stats_dialog)
        uplink_layout.addWidget(self.stats_btn)
        
        ie_layout.addLayout(uplink_layout)
        
        ie_group.setLayout(ie_layout)
        layout.addWidget(ie_group)
        
        # Close button
        close_layout = QHBoxLayout()
        close_layout.addStretch()
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        close_layout.addWidget(close_btn)
        
        layout.addLayout(close_layout)
    
    def _populate_language_combo(self):
        """Populate language combo box with all available languages, supporting nested groups and flags"""
        self.lang_combo.clear()
        lang_groups = self.i18n_service.get_language_groups()
        
        # Helper to recursively add items
        def add_items_recursive(data, prefix=""):
            for key, value in data.items():
                if isinstance(value, dict):
                    # Check if it's a leaf node (language definition)
                    # Heuristic: if it has "Standard" or "Dialekte" or "Pirate" keys, it's likely a language container
                    # BUT in our new structure, "Standard" is inside the language dict.
                    # Actually, the structure is: Group -> Subgroup -> Language -> Variant -> {code: name}
                    # OR Group -> Language -> Variant -> {code: name}
                    
                    # Let's look at the structure again:
                    # "Europa" -> "Mitteleuropa" -> "Deutsch" -> "Deutschland" -> "Hochdeutsch" -> {"de": "..."}
                    
                    # We can check if the values are strings (leafs)
                    is_leaf_dict = any(isinstance(v, str) for v in value.values())
                    
                    if is_leaf_dict:
                        # This is a dict of {code: name}, e.g. {"de": "Deutsch", "de_pirate": "..."}
                        for code, name in value.items():
                            self._add_language_item(code, name, prefix)
                    else:
                        # It's a group or subgroup
                        # Add a separator/header if it's a top-level group
                        if not prefix:
                            self.lang_combo.addItem(f"--- {key} ---", userData=None)
                            # Recurse
                            add_items_recursive(value, prefix=key)
                        else:
                            # Recurse with updated prefix (optional, maybe just indent?)
                            # For the combo box, we just want a flat list with headers or indentation
                            # Let's just recurse.
                            add_items_recursive(value, prefix=key)

        # Better approach: Flatten the list for the combo box, but keep groups visually distinct
        # We can use the same logic as the main menu, but flattened.
        
        # Let's use a simplified recursive traversal that just finds all codes and names
        # and adds them. To keep it organized, we can iterate the top-level groups.
        
        from PySide6.QtGui import QIcon
        
        def traverse_and_add(group_name, data, indent_level=0):
            # If it's a dict of languages (leaf node in the tree structure)
            # Check if values are strings -> {code: name}
            if all(isinstance(v, str) for v in data.values()):
                for code, name in data.items():
                    self._add_language_item(code, name)
                return

            # Otherwise it's a group
            # If indent_level == 0, add a header
            if indent_level == 0:
                 self.lang_combo.addItem(f"--- {group_name} ---", userData=None)
            
            for key, sub_data in data.items():
                if isinstance(sub_data, dict):
                    traverse_and_add(key, sub_data, indent_level + 1)

        # The structure is complex. Let's use get_all_language_codes to get a flat list,
        # but that loses the grouping.
        # The user wants "flags".
        
        # Let's try to replicate the menu structure but flattened into the combo.
        # Top level: Continents
        for continent, content in lang_groups.items():
            self.lang_combo.addItem(f"--- {continent} ---", userData=None)
            # We need to find all languages under this continent
            # We can reuse _collect_codes_recursive logic but we need names too.
            
            codes = []
            self.i18n_service._collect_codes_recursive(content, codes)
            # Sort codes by name for better UX
            code_name_pairs = []
            for code in codes:
                name = self.i18n_service.get_language_name(code)
                code_name_pairs.append((code, name))
            
            code_name_pairs.sort(key=lambda x: x[1])
            
            for code, name in code_name_pairs:
                self._add_language_item(code, name)

        # Add Custom Languages
        custom_langs = self.i18n_service.get_custom_languages()
        if custom_langs:
            self.lang_combo.addItem("--- Custom Languages ---", userData=None)
            for lang_code, lang_data in custom_langs.items():
                lang_name = lang_data.get("language_name", lang_code)
                self._add_language_item(lang_code, f"⭐ {lang_name}")
        
        # Set to current language
        for i in range(self.lang_combo.count()):
            if self.lang_combo.itemData(i) == self.i18n_service.current_language:
                self.lang_combo.setCurrentIndex(i)
                break

    def _add_language_item(self, code, name, prefix=""):
        from PySide6.QtGui import QIcon
        display_text = f"  {name} ({code})"
        
        # Load icon
        flag_path = self.i18n_service.get_flag_path(code)
        if flag_path:
            icon = QIcon(str(flag_path))
            self.lang_combo.addItem(icon, display_text, userData=code)
        else:
            self.lang_combo.addItem(display_text, userData=code)
    
    def _load_translation_keys(self):
        """Load all translation keys from master database or en.json"""
        master_file = Path("i18n/translation_master.json")
        
        if master_file.exists():
            with open(master_file, 'r', encoding='utf-8') as f:
                master_data = json.load(f)
                self.all_keys = list(master_data['translations'].keys())
        else:
            # Fallback to en.json if master DB doesn't exist
            en_file = Path("i18n/translations/en.json")
            with open(en_file, 'r', encoding='utf-8') as f:
                en_data = json.load(f)
                self.all_keys = self._flatten_keys(en_data)
        
        self.filtered_keys = self.all_keys.copy()
    
    def _flatten_keys(self, d, parent=''):
        """Flatten nested dictionary to dot notation keys"""
        keys = []
        for k, v in d.items():
            full_key = f"{parent}.{k}" if parent else k
            if isinstance(v, dict):
                keys.extend(self._flatten_keys(v, full_key))
            else:
                keys.append(full_key)
        return keys
    
    def _populate_table(self):
        """Populate table with translation keys"""
        self.table.setRowCount(0)
        self.table.blockSignals(True)
        
        for key in self.filtered_keys:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Column 0: Key (read-only)
            key_item = QTableWidgetItem(key)
            key_item.setFlags(key_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            key_item.setForeground(QColor("#666"))
            key_item.setToolTip(key)  # Add Tooltip
            self.table.setItem(row, 0, key_item)
            
            # Column 1: German Reference (read-only)
            german_value = self._get_translation_for_language(key, "de")
            german_item = QTableWidgetItem(german_value)
            german_item.setFlags(german_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            german_item.setForeground(QColor("#555"))
            german_item.setBackground(QColor("#f5f5f5"))
            german_item.setToolTip(german_value)  # Add Tooltip
            self.table.setItem(row, 1, german_item)
            
            # Column 2: English Reference (read-only)
            english_value = self._get_translation_for_language(key, "en")
            english_item = QTableWidgetItem(english_value)
            english_item.setFlags(english_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            english_item.setForeground(QColor("#555"))
            english_item.setBackground(QColor("#f5f5f5"))
            english_item.setToolTip(english_value)  # Add Tooltip
            self.table.setItem(row, 2, english_item)
            
            # Column 3: Current Language Value (read-only)
            if self.current_lang not in ["de", "en"]:
                current_value = self._get_translation_for_language(key, self.current_lang)
                current_item = QTableWidgetItem(current_value)
                current_item.setFlags(current_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                current_item.setForeground(QColor("#000"))
                current_item.setToolTip(current_value)  # Add Tooltip
                self.table.setItem(row, 3, current_item)
            else:
                # If current language is DE or EN, show it's the reference
                ref_item = QTableWidgetItem("(Reference language)")
                ref_item.setFlags(ref_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                ref_item.setForeground(QColor("#999"))
                ref_item.setFont(ref_item.font())
                ref_item.setToolTip("This is the reference language")  # Add Tooltip
                self.table.setItem(row, 3, ref_item)
            
            # Column 4: User Override (editable)
            override_value = self.i18n_service.get_user_override(self.current_lang, key)
            override_item = QTableWidgetItem(override_value or "")
            if override_value:
                override_item.setBackground(QColor("#e3f2fd"))  # Light blue for overrides
                override_item.setToolTip(f"Override: {override_value}")  # Add Tooltip
            else:
                override_item.setToolTip("Double-click to add override")  # Add Tooltip
            self.table.setItem(row, 4, override_item)
            
            # Column 5: Actions
            actions_item = QTableWidgetItem("")
            actions_item.setFlags(actions_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, 5, actions_item)
        
        self.table.blockSignals(False)
    
    def _get_translation_for_language(self, key: str, lang_code: str) -> str:
        """Get translation for specific language from file, with fallback"""
        # Try to load from language file
        lang_file = Path(f"i18n/translations/{lang_code}.json")
        
        if lang_file.exists():
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    lang_data = json.load(f)
                    value = self._get_nested_value(lang_data, key)
                    if value:
                        return value
            except Exception as e:
                print(f"Error loading {lang_code}.json: {e}")
        
        # Fallback to German
        if lang_code != "de":
            de_file = Path("i18n/translations/de.json")
            if de_file.exists():
                try:
                    with open(de_file, 'r', encoding='utf-8') as f:
                        de_data = json.load(f)
                        value = self._get_nested_value(de_data, key)
                        if value:
                            return value
                except Exception:
                    pass
        
        # Fallback to English
        en_file = Path("i18n/translations/en.json")
        if en_file.exists():
            try:
                with open(en_file, 'r', encoding='utf-8') as f:
                    en_data = json.load(f)
                    value = self._get_nested_value(en_data, key)
                    if value:
                        return value
            except Exception:
                pass
        
        # Last resort: return the key itself
        return key
    
    def _get_nested_value(self, data: dict, key: str):
        """Get value from nested dict using dot notation key"""
        parts = key.split('.')
        current = data
        
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
        
        return current if isinstance(current, str) else None
    
    def _on_language_changed(self):
        """Handle language selection change"""
        lang_code = self.lang_combo.currentData()
        if lang_code:
            self.current_lang = lang_code
            self._populate_table()
    
    def _on_search_changed(self, text):
        """Filter table based on search text"""
        if not text:
            self.filtered_keys = self.all_keys.copy()
        else:
            text_lower = text.lower()
            self.filtered_keys = [
                key for key in self.all_keys
                if text_lower in key.lower() or
                   text_lower in self.i18n_service.tr(key).lower()
            ]
        
        self._populate_table()
    
    def _on_item_changed(self, item):
        """Handle cell edit"""
        if item.column() == 4:  # User override column (now column 4)
            self.save_btn.setEnabled(True)
    
    def _save_all_changes(self):
        """Save all user overrides from table"""
        saved_count = 0
        
        # Check if custom language
        is_custom = self.current_lang.startswith("custom_")
        custom_service = None
        if is_custom:
            custom_service = get_custom_language_service()
        
        for row in range(self.table.rowCount()):
            key = self.table.item(row, 0).text()
            override_value = self.table.item(row, 4).text().strip()  # Column 4
            
            if override_value:
                if is_custom:
                    custom_service.update_custom_translation(self.current_lang, key, override_value)
                else:
                    self.i18n_service.save_user_override(self.current_lang, key, override_value)
                saved_count += 1
                # Highlight saved item
                self.table.item(row, 4).setBackground(QColor("#e3f2fd"))
            else:
                # Remove override if empty
                if is_custom:
                    custom_service.remove_custom_translation(self.current_lang, key)
                else:
                    self.i18n_service.remove_user_override(self.current_lang, key)
                self.table.item(row, 4).setBackground(QColor("#ffffff"))
        
        self.save_btn.setEnabled(False)
        self.translation_changed.emit()
        
        QMessageBox.information(
            self,
            "Saved",
            f"Saved {saved_count} translation overrides for {self.current_lang}"
        )
    
    def _reset_all_overrides(self):
        """Reset all overrides for current language"""
        reply = QMessageBox.question(
            self,
            "Reset Overrides",
            f"Are you sure you want to reset ALL overrides for {self.current_lang}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.i18n_service.override_service.clear_language_overrides(self.current_lang)
            self._populate_table()
            self.translation_changed.emit()
            
            QMessageBox.information(
                self,
                "Reset Complete",
                f"All overrides for {self.current_lang} have been reset"
            )
    
    def _export_translations(self):
        """Export translations to JSON file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Translations",
            f"translations_{self.current_lang}_{datetime.now().strftime('%Y%m%d')}.json",
            "JSON Files (*.json)"
        )
        
        if not file_path:
            return
        
        # Determine what to export based on radio button selection
        if self.export_current.isChecked():
            data = self._export_single_language(self.current_lang)
        elif self.export_all.isChecked():
            data = self._export_all_languages()
        else:
            # TODO: Implement multi-select dialog
            QMessageBox.information(self, "Not Implemented", "Multi-select export coming soon!")
            return
        
        # Save to file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        QMessageBox.information(
            self,
            "Export Complete",
            f"Translations exported to:\n{file_path}"
        )
    
    def _export_single_language(self, lang_code):
        """Export single language"""
        # Check if custom language
        if lang_code.startswith("custom_"):
            custom_service = get_custom_language_service()
            return custom_service.export_custom_language(lang_code)
            
        overrides = self.i18n_service.get_all_user_overrides(lang_code)
        
        return {
            "export_format": "macgyver_translation_single",
            "version": "1.0",
            "exported_at": datetime.now().isoformat(),
            "language": lang_code,
            "language_name": self.i18n_service.get_language_name(lang_code),
            "author": "User",  # TODO: Get from settings
            "translations": overrides,
            "metadata": {
                "total_overrides": len(overrides)
            }
        }
    
    def _export_all_languages(self):
        """Export all languages with overrides"""
        all_langs = {}
        total_count = 0
        
        for lang_code in self.i18n_service.get_all_language_codes():
            overrides = self.i18n_service.get_all_user_overrides(lang_code)
            if overrides:
                all_langs[lang_code] = {
                    "language_name": self.i18n_service.get_language_name(lang_code),
                    "translations": overrides
                }
                total_count += len(overrides)
        
        return {
            "export_format": "macgyver_translation_multi",
            "version": "1.0",
            "exported_at": datetime.now().isoformat(),
            "author": "User",
            "languages": all_langs,
            "metadata": {
                "total_languages": len(all_langs),
                "total_overrides": total_count
            }
        }
    
    def _import_translations(self):
        """Import translations from JSON file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Translations",
            "",
            "JSON Files (*.json)"
        )
        
        if not file_path:
            return
        
        # Validate file using validator
        file_path_obj = Path(file_path)
        valid, msg, sanitized_data = self.validator.validate_import_file(file_path_obj)
        
        if not valid:
            QMessageBox.critical(
                self,
                "Validation Failed",
                f"Import file validation failed:\n\n{msg}"
            )
            return
        
        # Proceed with import using sanitized data
        try:
            export_format = sanitized_data.get('export_format')
            
            if export_format == 'macgyver_translation_single':
                self._import_single_language(sanitized_data)
            elif export_format == 'macgyver_translation_multi':
                self._import_multi_language(sanitized_data)
            elif export_format == 'macgyver_translation_custom':
                try:
                    custom_service = get_custom_language_service()
                    lang_code = custom_service.import_custom_language(sanitized_data)
                    
                    QMessageBox.information(
                        self,
                        "Import Complete",
                        f"Imported custom language: {lang_code}"
                    )
                    
                    # Refresh language list
                    self._populate_language_combo()
                    
                    # Select the new language
                    index = self.lang_combo.findData(lang_code)
                    if index >= 0:
                        self.lang_combo.setCurrentIndex(index)
                        
                except Exception as e:
                    QMessageBox.critical(
                        self,
                        "Custom Language Import Error",
                        f"Failed to import custom language:\\n{str(e)}"
                    )
            else:
                QMessageBox.warning(
                    self,
                    "Invalid Format",
                    f"Unknown export format: {export_format}"
                )
                return
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Import Error",
                f"Failed to import translations:\n{str(e)}"
            )
    
    def _import_single_language(self, data):
        """Import single language translations"""
        lang_code = data.get('language')
        translations = data.get('translations', {})
        
        reply = QMessageBox.question(
            self,
            "Import Confirmation",
            f"Import {len(translations)} translations for {lang_code}?\n"
            f"This will merge with existing overrides.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            for key, value in translations.items():
                self.i18n_service.save_user_override(lang_code, key, value)
            
            self._populate_table()
            self.translation_changed.emit()
            
            QMessageBox.information(
                self,
                "Import Complete",
                f"Imported {len(translations)} translations for {lang_code}"
            )
    
    def _import_multi_language(self, data):
        """Import multiple language translations"""
        languages = data.get('languages', {})
        total_imported = 0
        
        reply = QMessageBox.question(
            self,
            "Import Confirmation",
            f"Import translations for {len(languages)} languages?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            for lang_code, lang_data in languages.items():
                translations = lang_data.get('translations', {})
                for key, value in translations.items():
                    self.i18n_service.save_user_override(lang_code, key, value)
                    total_imported += 1
            
            self._populate_table()
            self.translation_changed.emit()
            
            QMessageBox.information(
                self,
                "Import Complete",
                f"Imported {total_imported} translations for {len(languages)} languages"
            )
    
    def _open_uplink_dialog(self):
        """Open MacGyver Uplink Dialog"""
        from ui.dialogs.uplink_dialog import UplinkDialog
        dialog = UplinkDialog(self.i18n_service, self)
        if dialog.exec():
            # Refresh table if data was merged
            self._populate_table()
            self.translation_changed.emit()

    def _open_stats_dialog(self):
        """Open Translation Statistics Dialog"""
        from ui.dialogs.translation_stats_dialog import TranslationStatsDialog
        dialog = TranslationStatsDialog(self.i18n_service, self)
        dialog.exec()

    def tr(self, key: str) -> str:
        """Translate UI strings"""
        translations = {
            "Translation Editor": "Übersetzungs-Editor"
        }
        return translations.get(key, key)
