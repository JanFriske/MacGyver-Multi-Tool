import json
import os
import re

# Klingon Cipher Mapping (Glagolitic Unicode)
# Converts Latin characters to "alien" script for tlhIngan Hol (Klingon)
CIPHER_MAP = {
    'a': 'Ⰰ', 'b': 'Ⰱ', 'c': 'Ⱌ', 'd': 'Ⰴ', 'e': 'Ⰵ', 'f': 'Ⱉ', 'g': 'Ⰳ', 'h': 'Ⱒ',
    'i': 'Ⰻ', 'j': 'Ⰼ', 'k': 'Ⰽ', 'l': 'Ⰾ', 'm': 'Ⰿ', 'n': 'Ⱀ', 'o': 'Ⱁ', 'p': 'Ⱂ',
    'q': 'Ⱋ', 'r': 'Ⱃ', 's': 'Ⱄ', 't': 'Ⱅ', 'u': 'Ⱆ', 'v': 'Ⱇ', 'w': 'Ⱈ', 'x': 'Ⱎ',
    'y': 'Ⱏ', 'z': 'Ⱘ',
    'A': 'Ⰰ', 'B': 'Ⰱ', 'C': 'Ⱌ', 'D': 'Ⰴ', 'E': 'Ⰵ', 'F': 'Ⱉ', 'G': 'Ⰳ', 'H': 'Ⱒ',
    'I': 'Ⰻ', 'J': 'Ⰼ', 'K': 'Ⰽ', 'L': 'Ⰾ', 'M': 'Ⰿ', 'N': 'Ⱀ', 'O': 'Ⱁ', 'P': 'Ⱂ',
    'Q': 'Ⱋ', 'R': 'Ⱃ', 'S': 'Ⱄ', 'T': 'Ⱅ', 'U': 'Ⱆ', 'V': 'Ⱇ', 'W': 'Ⱈ', 'X': 'Ⱎ',
    'Y': 'Ⱏ', 'Z': 'Ⱘ',
    ' ': ' ', '.': '⵰', ',': 'ⵯ', '!': 'ⵧ', '?': '⵨', '-': 'ⵤ',
    '0': '↊', '1': '↋', '2': '↌', '3': '↍', '4': '↎', '5': '↏', '6': '←', '7': '↑', '8': '→', '9': '↓'
}

def to_alien(text):
    """Convert text to Klingon cipher (Glagolitic), preserving placeholders like {tool}."""
    parts = []
    last_pos = 0
    # Regex to find {placeholders}
    for match in re.finditer(r'\{[^}]+\}', text):
        # Translate text before placeholder
        parts.append("".join(CIPHER_MAP.get(c, c) for c in text[last_pos:match.start()]))
        # Keep placeholder as is
        parts.append(match.group(0))
        last_pos = match.end()
    # Translate remaining text
    parts.append("".join(CIPHER_MAP.get(c, c) for c in text[last_pos:]))
    return "".join(parts)

# Define the master list of tooltips and their translations
# Now with MORE SPECIFIC and HELPFUL descriptions
TOOLTIPS_MASTER = {
    "tooltips.menu_file": {
        "en": "Create, open, save, and manage your files and projects.",
        "de": "Dateiverwaltung: Neue Projekte erstellen, bestehende öffnen, Änderungen speichern, Dateien schließen.",
        "nl": "Maak, open, bewaar en beheer uw bestanden en projecten.",
        "fr": "Créer, ouvrir, enregistrer et gérer vos fichiers et projets.",
        "es": "Crear, abrir, guardar y administrar sus archivos y proyectos.",
        "it": "Crea, apri, salva e gestisci i tuoi file e progetti.",
        "ro": "Creați, deschideți, salvați și gestionați fișierele și proiectele dvs.",
        "ru": "Создание, открытие, сохранение и управление файлами и проектами.",
        "zh": "创建、打开、保存和管理您的文件和项目。"
    },
    "tooltips.menu_edit": {
        "en": "Edit content, undo and redo recent changes.",
        "de": "Bearbeiten: Text/Inhalte ändern, Rückgängig machen (Strg+Z), Wiederholen (Strg+Y), Kopieren, Einfügen.",
        "nl": "Bewerk inhoud, maak ongedaan en voer recente wijzigingen opnieuw uit.",
        "fr": "Modifier le contenu, annuler et rétablir les modifications récentes.",
        "es": "Editar contenido, deshacer y rehacer cambios recientes.",
        "it": "Modifica contenuto, annulla e ripristina le modifiche recenti.",
        "ro": "Editați conținut, anulați și refaceți modificările recente.",
        "ru": "Редактирование содержимого, отмена и повтор последних изменений.",
        "zh": "编辑内容，撤销和重做最近的更改。"
    },
    "tooltips.menu_tools": {
        "en": "Access powerful utility tools including dashboard, media player, and more.",
        "de": "Werkzeuge öffnen: Cockpit-Dashboard, Mediaplayer, System-Tools, Dienstprogramme und Module.",
        "nl": "Toegang tot krachtige hulpmiddelen inclusief dashboard, mediaspeler en meer.",
        "fr": "Accédez à de puissants outils utilitaires comprenant tableau de bord, lecteur multimédia, etc.",
        "es": "Acceda a potentes herramientas de utilidad incluyendo panel, reproductor multimedia y más.",
        "it": "Accedi a potenti strumenti di utilità tra cui dashboard, lettore multimediale e altro.",
        "ro": "Accesați instrumente utilitare puternice, inclusiv tablou de bord, player media și multe altele.",
        "ru": "Доступ к мощным утилитам, включая панель управления, медиаплеер и многое другое.",
        "zh": "访问强大的实用工具，包括仪表板、媒体播放器等。"
    },
    "tooltips.menu_settings": {
        "en": "Configure application preferences, language, and appearance.",
        "de": "Einstellungen anpassen: Sprache wählen, Theme ändern (Hell/Dunkel), Präferenzen festlegen.",
        "nl": "Configureer applicatievoorkeuren, taal en uiterlijk.",
        "fr": "Configurez les préférences, la langue et l'apparence de l'application.",
        "es": "Configure las preferencias, el idioma y la apariencia de la aplicación.",
        "it": "Configura le preferenze, la lingua e l'aspetto dell'applicazione.",
        "ro": "Configurați preferințele aplicației, limba și aspectul.",
        "ru": "Настройка параметров приложения, языка и внешнего вида.",
        "zh": "配置应用程序首选项、语言和外观。"
    },
    "tooltips.menu_help": {
        "en": "Get help, view documentation, and learn about this application.",
        "de": "Hilfe & Infos: Bedienungsanleitung öffnen, Tipps anzeigen, Über-Dialog mit Versionsnummer.",
        "nl": "Krijg hulp, bekijk documentatie en leer meer over deze applicatie.",
        "fr": "Obtenez de l'aide, consultez la documentation et découvrez cette application.",
        "es": "Obtenga ayuda, vea la documentación y aprenda sobre esta aplicación.",
        "it": "Ottieni aiuto, visualizza la documentazione e scopri questa applicazione.",
        "ro": "Obțineți ajutor, vizualizați documentația și aflați despre această aplicație.",
        "ru": "Получить помощь, просмотреть документацию и узнать об этом приложении.",
        "zh": "获取帮助、查看文档并了解此应用程序。"
    },
    "tooltips.menu_view": {
        "en": "Change the visual appearance and theme of the application.",
        "de": "Ansicht ändern: Zwischen hellem und dunklem Theme wechseln, Farbschema anpassen.",
        "nl": "Wijzig het visuele uiterlijk en thema van de applicatie.",
        "fr": "Modifiez l'apparence visuelle et le thème de l'application.",
        "es": "Cambie la apariencia visual y el tema de la aplicación.",
        "it": "Modifica l'aspetto visivo e il tema dell'applicazione.",
        "ro": "Schimbați aspectul vizual și tema aplicației.",
        "ru": "Изменение визуального оформления и темы приложения.",
        "zh": "更改应用程序的视觉外观和主题。"
    },
    "tooltips.menu_languages": {
        "en": "Choose your preferred language from numerous options.",
        "de": "Sprache auswählen: Aus 147 Varianten wählen - Hauptsprachen, regionale Dialekte, Bonus-Sprachen.",
        "nl": "Kies uw voorkeurstaal uit talrijke opties.",
        "fr": "Choisissez votre langue préférée parmi de nombreuses options.",
        "es": "Elija su idioma preferido entre numerosas opciones.",
        "it": "Scegli la tua lingua preferita tra numerose opzioni.",
        "ro": "Alegeți limba preferată din numeroase opțiuni.",
        "ru": "Выберите предпочитаемый язык из множества вариантов.",
        "zh": "从众多选项中选择您的首选语言。"
    },
    "tooltips.menu_german_dialects": {
        "en": "Select a regional German dialect variant.",
        "de": "Deutsche Dialekte: 38 Varianten von Bairisch über Kölsch bis Mittelhochdeutsch auswählen.",
        "nl": "Selecteer een regionale Duitse dialectvariant.",
        "fr": "Sélectionnez une variante dialectale allemande régionale.",
        "es": "Seleccione una variante de dialecto alemán regional.",
        "it": "Seleziona una variante dialettale tedesca regionale.",
        "ro": "Selectați o variantă dialectală germană regională.",
        "ru": "Выберите региональный вариант немецкого диалекта.",
        "zh": "选择一个地区性德语方言变体。"
    },
    "tooltips.menu_cockpit": {
        "en": "System monitoring dashboard with customizable widgets and real-time data.",
        "de": "Cockpit öffnen: Dashboard mit Widgets (CPU, RAM, Festplatte), Echtzeit-Monitoring, anpassbar.",
        "nl": "Systeemmonitoringdashboard met aanpasbare widgets en realtime gegevens.",
        "fr": "Tableau de bord de surveillance système avec widgets personnalisables et données en temps réel.",
        "es": "Panel de monitoreo del sistema con widgets personalizables y datos en tiempo real.",
        "it": "Dashboard di monitoraggio del sistema con widget personalizzabili e dati in tempo reale.",
        "ro": "Tablou de bord de monitorizare a sistemului cu widget-uri personalizabile și date în timp real.",
        "ru": "Панель мониторинга системы с настраиваемыми виджетами и данными в реальном времени.",
        "zh": "系统监控仪表板，具有可定制的小部件和实时数据。"
    },
    "tooltips.menu_media": {
        "en": "Media player with advanced controls, equalizer, and streaming support.",
        "de": "Media Player öffnen: Audio/Video abspielen, Equalizer nutzen, Playlists verwalten, Streaming.",
        "nl": "Mediaspeler met geavanceerde bedieningselementen, equalizer en streamingondersteuning.",
        "fr": "Lecteur multimédia avec contrôles avancés, égaliseur et prise en charge du streaming.",
        "es": "Reproductor multimedia con controles avanzados, ecualizador y soporte de transmisión.",
        "it": "Lettore multimediale con controlli avanzati, equalizzatore e supporto streaming.",
        "ro": "Player media cu controale avansate, egalizator și suport pentru streaming.",
        "ru": "Медиаплеер с расширенными элементами управления, эквалайзером и поддержкой потокового вещания.",
        "zh": "媒体播放器，具有高级控制、均衡器和流媒体支持。"
    },
    "tooltips.menu_tabs": {
        "en": "Manage open tabs and organize your workspace efficiently.",
        "de": "Tabs verwalten: Zwischen geöffneten Modulen wechseln, schließen, neue hinzufügen, sortieren.",
        "nl": "Beheer open tabbladen en organiseer uw werkruimte efficiënt.",
        "fr": "Gérez les onglets ouverts et organisez votre espace de travail efficacement.",
        "es": "Administre las pestañas abiertas y organice su espacio de trabajo eficientemente.",
        "it": "Gestisci le schede aperte e organizza il tuo spazio di lavoro in modo efficiente.",
        "ro": "Gestionați filele deschise și organizați-vă spațiul de lucru eficient.",
        "ru": "Управление открытыми вкладками и эффективная организация рабочего пространства.",
        "zh": "管理打开的选项卡并高效地组织您的工作空间。"
    },
    "tooltips.file_new": {
        "en": "Create a new file or start a fresh project from scratch.",
        "de": "Neu erstellen: Leeres Projekt starten, neue Datei anlegen, frisch beginnen (Strg+N).",
        "nl": "Maak een nieuw bestand of start een nieuw project vanaf nul.",
        "fr": "Créez un nouveau fichier ou démarrez un nouveau projet à partir de zéro.",
        "es": "Cree un nuevo archivo o inicie un proyecto nuevo desde cero.",
        "it": "Crea un nuovo file o avvia un nuovo progetto da zero.",
        "ro": "Creați un fișier nou sau începeți un proiect nou de la zero.",
        "ru": "Создать новый файл или начать новый проект с нуля.",
        "zh": "创建新文件或从头开始新项目。"
    },
    "tooltips.file_open": {
        "en": "Open and load an existing file from your filesystem.",
        "de": "Datei öffnen: Bestehende Projekte/Dateien von Festplatte laden, durchsuchen (Strg+O).",
        "nl": "Open en laad een bestaand bestand uit uw bestandssysteem.",
        "fr": "Ouvrez et chargez un fichier existant depuis votre système de fichiers.",
        "es": "Abra y cargue un archivo existente de su sistema de archivos.",
        "it": "Apri e carica un file esistente dal tuo filesystem.",
        "ro": "Deschideți și încărcați un fișier existent din sistemul dvs. de fișiere.",
        "ru": "Открыть и загрузить существующий файл из вашей файловой системы.",
        "zh": "从文件系统中打开并加载现有文件。"
    },
    "tooltips.file_save": {
        "en": "Save all current changes to the active file.",
        "de": "Speichern: Aktuelle Änderungen sichern, Datei auf Festplatte schreiben (Strg+S).",
        "nl": "Bewaar alle huidige wijzigingen in het actieve bestand.",
        "fr": "Enregistrez toutes les modifications actuelles dans le fichier actif.",
        "es": "Guarde todos los cambios actuales en el archivo activo.",
        "it": "Salva tutte le modifiche correnti nel file attivo.",
        "ro": "Salvați toate modificările curente în fișierul activ.",
        "ru": "Сохранить все текущие изменения в активном файле.",
        "zh": "将所有当前更改保存到活动文件。"
    },
    "tooltips.file_exit": {
        "en": "Close the application and exit completely.",
        "de": "Beenden: Anwendung komplett schließen, alle Fenster beenden, Programm verlassen (Alt+F4).",
        "nl": "Sluit de applicatie af en verlaat volledig.",
        "fr": "Fermez l'application et quittez complètement.",
        "es": "Cierre la aplicación y salga completamente.",
        "it": "Chiudi l'applicazione ed esci completamente.",
        "ro": "Închideți aplicația și ieșiți complet.",
        "ru": "Закрыть приложение и полностью выйти.",
        "zh": "关闭应用程序并完全退出。"
    },
    "tooltips.edit_undo": {
        "en": "Undo the most recent action or change.",
        "de": "Rückgängig: Letzte Aktion widerrufen, Schritt zurück, Fehler korrigieren (Strg+Z).",
        "nl": "Maak de meest recente actie of wijziging ongedaan.",
        "fr": "Annulez l'action ou la modification la plus récente.",
        "es": "Deshaga la acción o cambio más reciente.",
        "it": "Annulla l'azione o la modifica più recente.",
        "ro": "Anulați cea mai recentă acțiune sau modificare.",
        "ru": "Отменить последнее действие или изменение.",
        "zh": "撤销最近的操作或更改。"
    },
    "tooltips.edit_redo": {
        "en": "Redo the last action that was undone.",
        "de": "Wiederholen: Rückgängig gemachte Aktion erneut ausführen, Schritt vorwärts (Strg+Y).",
        "nl": "Voer de laatste ongedaan gemaakte actie opnieuw uit.",
        "fr": "Rétablissez la dernière action annulée.",
        "es": "Rehaga la última acción deshecha.",
        "it": "Ripristina l'ultima azione annullata.",
        "ro": "Refaceți ultima acțiune anulată.",
        "ru": "Повторить последнее отмененное действие.",
        "zh": "重做上次撤销的操作。"
    },
    "tooltips.help_about": {
        "en": "Display version information and credits for this application.",
        "de": "Über MacGyver: Versionsnummer, Entwickler-Info, Lizenz, Credits und Copyright anzeigen.",
        "nl": "Toon versieinformatie en credits voor deze applicatie.",
        "fr": "Affichez les informations de version et les crédits de cette application.",
        "es": "Muestre información de versión y créditos de esta aplicación.",
        "it": "Visualizza informazioni sulla versione e crediti per questa applicazione.",
        "ro": "Afișați informații despre versiune și credite pentru această aplicație.",
        "ru": "Отобразить информацию о версии и благодарности для этого приложения.",
        "zh": "显示此应用程序的版本信息和版权信息。"
    },
    "tooltips.theme_light": {
        "en": "Switch to the bright, light-colored theme for daytime use.",
        "de": "Helles Theme: Helle Farben für Tageslicht, bessere Lesbarkeit, weniger Kontrast, augenfreundlich.",
        "nl": "Schakel over naar het heldere, lichtgekleurde thema voor daglicht.",
        "fr": "Passez au thème lumineux et clair pour une utilisation de jour.",
        "es": "Cambie al tema brillante y claro para uso diurno.",
        "it": "Passa al tema luminoso e chiaro per l'uso diurno.",
        "ro": "Comutați la tema luminoasă și deschisă pentru utilizarea în timpul zilei.",
        "ru": "Переключиться на яркую светлую тему для дневного использования.",
        "zh": "切换到明亮的浅色主题以供白天使用。"
    },
    "tooltips.theme_dark": {
        "en": "Switch to the dark theme for reduced eye strain in low-light conditions.",
        "de": "Dunkles Theme: Dunkle Farben für Abend/Nacht, weniger Augenbelastung, schont Akku, modern.",
        "nl": "Schakel over naar het donkere thema voor verminderde oogbelasting bij weinig licht.",
        "fr": "Passez au thème sombre pour réduire la fatigue oculaire en faible luminosité.",
        "es": "Cambie al tema oscuro para reducir la fatiga visual en condiciones de poca luz.",
        "it": "Passa al tema scuro per ridurre l'affaticamento degli occhi in condizioni di scarsa illuminazione.",
        "ro": "Comutați la tema întunecată pentru a reduce oboseala ochilor în condiții de lumină scăzută.",
        "ru": "Переключиться на темную тему для уменьшения нагрузки на глаза при слабом освещении.",
        "zh": "切换到深色主题以在低光条件下减少眼睛疲劳。"
    },
    "tooltips.open_tool": {
        "en": "Open and activate the {tool} utility tool.",
        "de": "{tool} öffnen: Dieses Werkzeug starten und in neuem Tab/Fenster aktivieren.",
        "nl": "Open en activeer het hulpmiddel {tool}.",
        "fr": "Ouvrez et activez l'outil utilitaire {tool}.",
        "es": "Abra y active la herramienta de utilidad {tool}.",
        "it": "Apri e attiva lo strumento di utilità {tool}.",
        "ro": "Deschideți și activați instrumentul utilitar {tool}.",
        "ru": "Открыть и активировать утилиту {tool}.",
        "zh": "打开并激活 {tool} 实用工具。"
    },
    "tooltips.add_widget": {
        "en": "Add a new customizable widget to your dashboard.",
        "de": "Widget hinzufügen: Neues Element zum Dashboard hinzufügen, konfigurieren, positionieren, anpassen.",
        "nl": "Voeg een nieuwe aanpasbare widget toe aan uw dashboard.",
        "fr": "Ajoutez un nouveau widget personnalisable à votre tableau de bord.",
        "es": "Agregue un nuevo widget personalizable a su panel.",
        "it": "Aggiungi un nuovo widget personalizzabile alla tua dashboard.",
        "ro": "Adăugați un widget nou personalizabil la tabloul dvs. de bord.",
        "ru": "Добавить новый настраиваемый виджет на панель управления.",
        "zh": "向您的仪表板添加新的可定制小部件。"
    }
}

TRANSLATIONS_DIR = "i18n/translations"

def update_translations():
    if not os.path.exists(TRANSLATIONS_DIR):
        print(f"Error: Directory {TRANSLATIONS_DIR} not found.")
        return

    for filename in os.listdir(TRANSLATIONS_DIR):
        if not filename.endswith(".json"):
            continue
        
        filepath = os.path.join(TRANSLATIONS_DIR, filename)
        lang_code = filename.split(".")[0]
        
        # Determine base language for fallback
        # Dialects fallback to 'de', others to 'en'
        if lang_code.startswith("de_"):
            base_lang = "de"
        else:
            base_lang = "en"
            
        # Special case for Klingon (tlh) - use cipher for authentic alien look
        if lang_code == "tlh":
            base_lang = "en"  # Still use English as source, but will cipher it

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            if "tooltips" not in data:
                data["tooltips"] = {}
            
            # Update tooltips - FORCE OVERWRITE to propagate new, better text
            for key, translations in TOOLTIPS_MASTER.items():
                target_text = ""
                
                # 1. Try specific language match
                if lang_code in translations:
                    target_text = translations[lang_code]
                # 2. Try base language (de for dialects)
                elif base_lang in translations:
                    target_text = translations[base_lang]
                # 3. Fallback to English
                else:
                    target_text = translations["en"]
                
                # Special: Apply Klingon cipher for tlh (tlhIngan Hol)
                if lang_code == "tlh":
                    target_text = to_alien(target_text)
                
                # ALWAYS update to enforce new, improved translations
                data["tooltips"][key] = target_text
                print(f"[{lang_code}] Updated {key}")

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                
        except Exception as e:
            print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    update_translations()
