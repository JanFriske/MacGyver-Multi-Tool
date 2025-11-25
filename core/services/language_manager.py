"""
Language Manager - Verwaltet Spracheinstellungen und Persistierung
"""
from PySide6.QtCore import QSettings, QObject, Signal
from core.services.i18n_service import I18nService

class LanguageManager(QObject):
    """Verwaltet Spracheinstellungen mit Persistierung."""
    
    language_changed = Signal(str)  # Sprachcode
    
    def __init__(self, i18n_service: I18nService):
        super().__init__()
        self.i18n_service = i18n_service
        self.settings = QSettings("Jan Fr iske", "MacGyver Multi-Tool")
        self._load_saved_language()
    
    def _load_saved_language(self):
        """Lädt die gespeicherte Spracheinstellung."""
        saved_lang = self.settings.value("language", "de")
        # Use get_all_language_codes() to include all language variants
        all_codes = self.i18n_service.get_all_language_codes()
        if saved_lang in all_codes:
            self.i18n_service.set_language(saved_lang)
            print(f"[LanguageManager] Gespeicherte Sprache geladen: {saved_lang}")
        else:
            # Fallback zu Deutsch
            self.i18n_service.set_language("de")
            print(f"[LanguageManager] Standardsprache: Deutsch")
    
    def set_language(self, lang_code: str):
        """Setzt die Sprache und speichert sie."""
        # Accept all language variants via get_all_language_codes()
        all_codes = self.i18n_service.get_all_language_codes()
        if lang_code in all_codes:
            self.i18n_service.set_language(lang_code)
            self.settings.setValue("language", lang_code)
            self.language_changed.emit(lang_code)
            print(f"[LanguageManager] Sprache geändert und gespeichert: {lang_code}")
        else:
            print(f"[LanguageManager] Unbekannte Sprache: {lang_code}")
    
    def get_current_language(self) -> str:
        """Gibt die aktuelle Sprache zurück."""
        return self.i18n_service.current_language
