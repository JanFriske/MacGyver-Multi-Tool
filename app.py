"""
MacGyver Multi-Tool – Hauptprogramm
© 2025 Jan Friske
Freeware / Non-Commercial License (PySide6 unter LGPL)
"""

import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QTextStream, Qt
from PySide6.QtGui import QIcon

from ui.view import MainWindow
from presenter.controller import Controller


def load_stylesheet(file_path):
    """Helper function to load a stylesheet from a file."""
    file = QFile(file_path)
    if not file.exists():
        print(f"[Warnung] Stylesheet-Datei '{file_path}' nicht gefunden.")
        return ""
    
    if file.open(QFile.ReadOnly | QFile.Text):
        stream = QTextStream(file)
        stylesheet = stream.readAll()
        file.close()
        return stylesheet
    else:
        print(f"[Fehler] Konnte Stylesheet '{file_path}' nicht laden.")
        return ""


def apply_mac_theme(app, theme="light"):
    """
    Lädt das macOS-ähnliche Stylesheet und setzt es für die gesamte Anwendung.
    """
    if theme == "dark":
        qss = load_stylesheet("ui/styles/mac_dark.qss")
    elif theme == "klingon":
        qss = load_stylesheet("ui/styles/mac_klingon.qss")
    else:
        qss = load_stylesheet("ui/styles/mac_light.qss")
    
    if qss:
        app.setStyleSheet(qss)
        print(f"[Theme] macOS-Stil '{theme}' erfolgreich angewendet.")
        return True
    else:
        # Fallback to the main theme file
        qss = load_stylesheet("ui/styles/mac_theme.qss")
        if qss:
            app.setStyleSheet(qss)
            print(f"[Theme] macOS-Stil '{theme}' erfolgreich angewendet (Fallback zu mac_theme.qss).")
            return True
        else:
            print(f"[Fehler] Konnte kein Stylesheet für das Theme '{theme}' laden.")
            return False


def main():
    """
    Einstiegspunkt der Anwendung.
    Initialisiert die QApplication, lädt Theme, startet View und Presenter.
    """
    # Ensure icons are shown in menus (some platforms/styles hide them by default)
    attr = getattr(Qt, 'AA_DontShowIconsInMenus', None)
    if attr is not None:
        QApplication.setAttribute(attr, False)
    app = QApplication(sys.argv)
    
    # CRITICAL: Set Fusion style FIRST before anything else
    # This is required for QSS to work properly on Windows
    app.setStyle("Fusion")

    # Set application attributes to make it more macOS-like
    app.setApplicationName("MacGyver Multi-Tool")
    app.setApplicationDisplayName("MacGyver Multi-Tool")
    app.setOrganizationName("Jan Friske")
    app.setOrganizationDomain("janfriske.com")

    # Fix for Windows Taskbar Icon (AppUserModelID)
    try:
        from ctypes import windll
        myappid = 'janfriske.macgyver.multitool.1.0' # arbitrary string
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except ImportError:
        pass

    # Set application icon (Absolute Path)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_dir, "assets", "icons", "mgmt.ico")
    
    app_icon = None
    if os.path.exists(icon_path):
        app_icon = QIcon(icon_path)
        app.setWindowIcon(app_icon)
    else:
        print(f"[Warnung] Icon nicht gefunden unter: {icon_path}")

    # Anwenden des macOS-Themes (Standard: hell)
    theme_applied = apply_mac_theme(app, "light")

    # Hauptfenster + Controller initialisieren
    window = MainWindow()
    
    # Explicitly set icon on main window as well
    if app_icon:
        window.setWindowIcon(app_icon)
    
    controller = Controller(window)
    
    # Connect theme change signal to update application stylesheet
    def update_app_theme(theme):
        apply_mac_theme(app, theme)
    
    window.theme_changed.connect(update_app_theme)

    # Auto-switch to Klingon theme when language is Klingon
    def on_language_changed(lang_code):
        if lang_code == "tlh":
            apply_mac_theme(app, "klingon")
            window.current_theme = "klingon" # Update window state if needed
        elif window.current_theme == "klingon": 
             # Revert to default or user preference if we were in Klingon mode
             # For now, revert to light as safe default or maybe check system?
             # Let's revert to "light" as a safe bet or "dark" if preferred.
             # Since we don't track "previous theme" easily here without more state,
             # let's default to "light" (standard macOS).
             apply_mac_theme(app, "light")
             window.current_theme = "light"
             
    window.language_changed.connect(on_language_changed)

    # Fenster anzeigen
    window.show()

    # Event Loop starten
    sys.exit(app.exec())


def exception_hook(exctype, value, traceback):
    """Global exception handler to ensure errors are logged."""
    print(f"[CRITICAL] Unhandled exception: {value}")
    sys.__excepthook__(exctype, value, traceback)


if __name__ == "__main__":
    sys.excepthook = exception_hook
    main()