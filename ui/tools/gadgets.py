from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QHBoxLayout, QGridLayout
from PySide6.QtCore import QTimer, QTime, QDate, Qt, QDateTime, QTimeZone, QLocale
import psutil
import time
import locale
from ui.components.circular_gauge import CircularGauge
from ui.components.macgyver_widget import MacGyverWidget

# Deutsche Lokalisierung
DE_WEEKDAYS = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
DE_MONTHS = ["Januar", "Februar", "März", "April", "Mai", "Juni", 
             "Juli", "August", "September", "Oktober", "November", "Dezember"]

class ClockWidget(MacGyverWidget):
    def __init__(self):
        super().__init__("Weltzeituhr", size_span=(2, 1))
        
        # Weather Service
        try:
            from core.services.weather_service import WeatherService
            self.weather_service = WeatherService()
            self.weather_data = None
        except:
            self.weather_service = None
            self.weather_data = None
        
        self._init_ui()
        self._update_time()
        
        # Wetter sofort laden (nicht warten)
        QTimer.singleShot(100, self._load_weather)
        
        # Timer für Zeit-Updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_time)
        self.timer.start(1000)
        
        # Timer für Wetter-Updates (alle 10 Minuten)
        if self.weather_service:
            self.weather_timer = QTimer(self)
            self.weather_timer.timeout.connect(self._load_weather)
            self.weather_timer.start(600000)  # 10 Minuten

    def _init_ui(self):
        # Clear existing content if any
        if self.content_area.count():
            while self.content_area.count():
                item = self.content_area.takeAt(0)
                if item.widget(): item.widget().deleteLater()

        # Initialize all labels to None first
        self.time_label = None
        self.date_label = None
        self.gmt_label = None
        self.tz_label = None
        self.dst_label = None
        self.week_label = None
        self.region_label = None
        self.weather_container = None
        self.weather_icon_label = None
        self.weather_temp_label = None
        self.weather_desc_label = None
        self.weather_forecast_widgets = []

        if self.span_w == 1 and self.span_h == 1:
            # 1x1: Kompakt - Nur Zeit groß
            container = QWidget()
            l = QVBoxLayout(container)
            l.setContentsMargins(8, 8, 8, 8)
            l.setSpacing(4)
            
            self.time_label = QLabel()
            self.time_label.setAlignment(Qt.AlignCenter)
            self.time_label.setStyleSheet("""
                font-size: 24px; 
                font-weight: bold; 
                color: #007aff; 
                font-family: 'Segoe UI';
                padding: 4px;
            """)
            l.addWidget(self.time_label)
            self.add_bubble(container)
            
        elif self.span_w == 2 and self.span_h == 1:
            # 2x1: Kompakt mit Datum
            container = QWidget()
            l = QVBoxLayout(container)
            l.setContentsMargins(10, 10, 10, 10)
            l.setSpacing(6)
            
            self.time_label = QLabel()
            self.time_label.setAlignment(Qt.AlignCenter)
            self.time_label.setStyleSheet("""
                font-size: 28px; 
                font-weight: bold; 
                color: #007aff; 
                font-family: 'Segoe UI';
                padding: 2px;
            """)
            l.addWidget(self.time_label)
            
            self.date_label = QLabel()
            self.date_label.setAlignment(Qt.AlignCenter)
            self.date_label.setStyleSheet("""
                font-size: 14px; 
                color: rgba(255, 255, 255, 0.8); 
                font-family: 'Segoe UI'; 
                font-weight: 500;
            """)
            l.addWidget(self.date_label)
            
            self.add_bubble(container)
            
        elif self.span_w == 3 and self.span_h == 1:
            # 3x1: Breit mit GMT - verbesserte Abstände
            container = QWidget()
            l = QVBoxLayout(container)
            l.setContentsMargins(14, 14, 14, 14)
            l.setSpacing(10)
            
            self.time_label = QLabel()
            self.time_label.setAlignment(Qt.AlignCenter)
            self.time_label.setStyleSheet("""
                font-size: 34px; 
                font-weight: bold; 
                color: #007aff; 
                font-family: 'Segoe UI';
                padding: 4px 0px;
            """)
            l.addWidget(self.time_label)
            
            self.date_label = QLabel()
            self.date_label.setAlignment(Qt.AlignCenter)
            self.date_label.setWordWrap(True)
            self.date_label.setStyleSheet("""
                font-size: 15px; 
                color: rgba(255, 255, 255, 0.9); 
                font-family: 'Segoe UI'; 
                font-weight: 500;
                padding: 2px 4px;
            """)
            l.addWidget(self.date_label)
            
            self.gmt_label = QLabel()
            self.gmt_label.setAlignment(Qt.AlignCenter)
            self.gmt_label.setStyleSheet("""
                font-size: 12px; 
                color: rgba(255, 255, 255, 0.65); 
                font-family: 'Segoe UI';
                padding: 2px 0px;
            """)
            l.addWidget(self.gmt_label)
            
            self.add_bubble(container)
            
        elif self.span_w == 2 and self.span_h == 2:
            # 2x2: Mittelgroß mit erweiterten Infos - verbesserte Abstände
            # Zeit-Bubble
            time_container = QWidget()
            l = QVBoxLayout(time_container)
            l.setContentsMargins(10, 10, 10, 10)
            self.time_label = QLabel()
            self.time_label.setAlignment(Qt.AlignCenter)
            self.time_label.setStyleSheet("""
                font-size: 40px; 
                font-weight: bold; 
                color: #007aff; 
                font-family: 'Segoe UI';
                padding: 4px 0px;
            """)
            l.addWidget(self.time_label)
            self.add_bubble(time_container)
            
            # Info-Bubble
            info_container = QWidget()
            l2 = QVBoxLayout(info_container)
            l2.setContentsMargins(10, 10, 10, 10)
            l2.setSpacing(8)
            
            self.date_label = QLabel()
            self.date_label.setAlignment(Qt.AlignCenter)
            self.date_label.setWordWrap(True)
            self.date_label.setStyleSheet("font-size: 15px; color: rgba(255, 255, 255, 0.95); font-family: 'Segoe UI'; font-weight: 500; padding: 2px 4px;")
            l2.addWidget(self.date_label)
            
            self.gmt_label = QLabel()
            self.gmt_label.setAlignment(Qt.AlignCenter)
            self.gmt_label.setStyleSheet("font-size: 12px; color: rgba(255, 255, 255, 0.75); font-family: 'Segoe UI'; padding: 2px 0px;")
            l2.addWidget(self.gmt_label)
            
            self.tz_label = QLabel()
            self.tz_label.setAlignment(Qt.AlignCenter)
            self.tz_label.setWordWrap(True)
            self.tz_label.setStyleSheet("font-size: 11px; color: rgba(255, 255, 255, 0.6); font-family: 'Segoe UI'; padding: 2px 4px;")
            l2.addWidget(self.tz_label)
            
            self.week_label = QLabel()
            self.week_label.setAlignment(Qt.AlignCenter)
            self.week_label.setStyleSheet("font-size: 10px; color: rgba(255, 255, 255, 0.5); font-family: 'Segoe UI'; padding: 2px 0px;")
            l2.addWidget(self.week_label)
            
            self.add_bubble(info_container)
            
        elif self.span_w == 3 and self.span_h == 2:
            # 3x2: Groß mit Wetter-Vorschau - verbesserte Abstände
            # Zeit-Bubble (oben)
            time_container = QWidget()
            l = QVBoxLayout(time_container)
            l.setContentsMargins(12, 12, 12, 12)
            self.time_label = QLabel()
            self.time_label.setAlignment(Qt.AlignCenter)
            self.time_label.setStyleSheet("""
                font-size: 46px; 
                font-weight: bold; 
                color: #007aff; 
                font-family: 'Segoe UI';
                padding: 4px 0px;
            """)
            l.addWidget(self.time_label)
            self.add_bubble(time_container)
            
            # Datum & Info
            info_container = QWidget()
            l2 = QVBoxLayout(info_container)
            l2.setContentsMargins(12, 12, 12, 12)
            l2.setSpacing(10)
            
            self.date_label = QLabel()
            self.date_label.setAlignment(Qt.AlignCenter)
            self.date_label.setWordWrap(True)
            self.date_label.setStyleSheet("font-size: 17px; color: rgba(255, 255, 255, 0.95); font-family: 'Segoe UI'; font-weight: 500; padding: 2px 6px;")
            l2.addWidget(self.date_label)
            
            self.gmt_label = QLabel()
            self.gmt_label.setAlignment(Qt.AlignCenter)
            self.gmt_label.setStyleSheet("font-size: 13px; color: rgba(255, 255, 255, 0.75); font-family: 'Segoe UI'; padding: 2px 0px;")
            l2.addWidget(self.gmt_label)
            
            self.tz_label = QLabel()
            self.tz_label.setAlignment(Qt.AlignCenter)
            self.tz_label.setWordWrap(True)
            self.tz_label.setStyleSheet("font-size: 11px; color: rgba(255, 255, 255, 0.6); font-family: 'Segoe UI'; padding: 2px 6px;")
            l2.addWidget(self.tz_label)
            
            self.add_bubble(info_container)
            
            # Wetter-Vorschau (kompakt)
            if self.weather_service:
                weather_container = QWidget()
                weather_layout = QHBoxLayout(weather_container)
                weather_layout.setContentsMargins(8, 8, 8, 8)
                weather_layout.setSpacing(8)
                
                self.weather_icon_label = QLabel("🌤️")
                self.weather_icon_label.setAlignment(Qt.AlignCenter)
                self.weather_icon_label.setStyleSheet("font-size: 32px;")
                weather_layout.addWidget(self.weather_icon_label)
                
                weather_info = QWidget()
                weather_info_layout = QVBoxLayout(weather_info)
                weather_info_layout.setContentsMargins(0, 0, 0, 0)
                weather_info_layout.setSpacing(2)
                
                self.weather_temp_label = QLabel("--°C")
                self.weather_temp_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                self.weather_temp_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #ff9500; font-family: 'Segoe UI';")
                weather_info_layout.addWidget(self.weather_temp_label)
                
                self.weather_desc_label = QLabel("Wird geladen...")
                self.weather_desc_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                self.weather_desc_label.setStyleSheet("font-size: 12px; color: rgba(255, 255, 255, 0.7); font-family: 'Segoe UI';")
                weather_info_layout.addWidget(self.weather_desc_label)
                
                weather_layout.addWidget(weather_info)
                weather_layout.addStretch()
                
                self.weather_container = weather_container
                self.add_bubble(weather_container)
            
        elif self.span_w == 3 and self.span_h == 3:
            # 3x3: Maximum - Vollständige Ansicht mit Wetter - Premium Design
            # Zeit-Bubble (oben, groß)
            time_container = QWidget()
            l = QVBoxLayout(time_container)
            l.setContentsMargins(14, 14, 14, 14)
            self.time_label = QLabel()
            self.time_label.setAlignment(Qt.AlignCenter)
            self.time_label.setStyleSheet("""
                font-size: 54px; 
                font-weight: bold; 
                color: #007aff; 
                font-family: 'Segoe UI';
                padding: 6px 0px;
            """)
            l.addWidget(self.time_label)
            self.add_bubble(time_container)
            
            # Datum & Zeitzone Info
            info_container = QWidget()
            l2 = QVBoxLayout(info_container)
            l2.setContentsMargins(14, 14, 14, 14)
            l2.setSpacing(12)
            
            self.date_label = QLabel()
            self.date_label.setAlignment(Qt.AlignCenter)
            self.date_label.setWordWrap(True)
            self.date_label.setStyleSheet("font-size: 19px; color: rgba(255, 255, 255, 0.98); font-family: 'Segoe UI'; font-weight: 500; padding: 3px 8px;")
            l2.addWidget(self.date_label)
            
            self.gmt_label = QLabel()
            self.gmt_label.setAlignment(Qt.AlignCenter)
            self.gmt_label.setStyleSheet("font-size: 14px; color: rgba(255, 255, 255, 0.8); font-family: 'Segoe UI'; padding: 2px 0px;")
            l2.addWidget(self.gmt_label)
            
            self.tz_label = QLabel()
            self.tz_label.setAlignment(Qt.AlignCenter)
            self.tz_label.setWordWrap(True)
            self.tz_label.setStyleSheet("font-size: 12px; color: rgba(255, 255, 255, 0.65); font-family: 'Segoe UI'; padding: 2px 8px;")
            l2.addWidget(self.tz_label)
            
            self.dst_label = QLabel()
            self.dst_label.setAlignment(Qt.AlignCenter)
            self.dst_label.setStyleSheet("font-size: 11px; color: rgba(255, 255, 255, 0.55); font-family: 'Segoe UI'; font-style: italic; padding: 2px 0px;")
            l2.addWidget(self.dst_label)
            
            self.week_label = QLabel()
            self.week_label.setAlignment(Qt.AlignCenter)
            self.week_label.setWordWrap(True)
            self.week_label.setStyleSheet("font-size: 10px; color: rgba(255, 255, 255, 0.5); font-family: 'Segoe UI'; padding: 2px 4px;")
            l2.addWidget(self.week_label)
            
            self.add_bubble(info_container)
            
            # Wetter-Sektion (vollständig mit Vorhersage)
            if self.weather_service:
                weather_container = QWidget()
                weather_layout = QVBoxLayout(weather_container)
                weather_layout.setContentsMargins(12, 12, 12, 12)
                weather_layout.setSpacing(10)
                
                # Aktuelles Wetter
                current_weather = QWidget()
                current_layout = QHBoxLayout(current_weather)
                current_layout.setContentsMargins(0, 0, 0, 0)
                current_layout.setSpacing(12)
                
                self.weather_icon_label = QLabel("🌤️")
                self.weather_icon_label.setAlignment(Qt.AlignCenter)
                self.weather_icon_label.setStyleSheet("font-size: 48px;")
                current_layout.addWidget(self.weather_icon_label)
                
                weather_info = QWidget()
                weather_info_layout = QVBoxLayout(weather_info)
                weather_info_layout.setContentsMargins(0, 0, 0, 0)
                weather_info_layout.setSpacing(4)
                
                self.weather_temp_label = QLabel("--°C")
                self.weather_temp_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                self.weather_temp_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #ff9500; font-family: 'Segoe UI';")
                weather_info_layout.addWidget(self.weather_temp_label)
                
                self.weather_desc_label = QLabel("Wetterdaten werden geladen...")
                self.weather_desc_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                self.weather_desc_label.setStyleSheet("font-size: 14px; color: rgba(255, 255, 255, 0.8); font-family: 'Segoe UI';")
                weather_info_layout.addWidget(self.weather_desc_label)
                
                current_layout.addWidget(weather_info)
                current_layout.addStretch()
                
                weather_layout.addWidget(current_weather)
                
                # Vorhersage (3 Tage)
                forecast_label = QLabel("3-Tage-Vorhersage")
                forecast_label.setAlignment(Qt.AlignLeft)
                forecast_label.setStyleSheet("font-size: 12px; font-weight: bold; color: rgba(255, 255, 255, 0.65); font-family: 'Segoe UI'; padding-top: 4px;")
                weather_layout.addWidget(forecast_label)
                
                forecast_container = QWidget()
                forecast_layout = QHBoxLayout(forecast_container)
                forecast_layout.setContentsMargins(0, 0, 0, 0)
                forecast_layout.setSpacing(8)
                
                # Wird dynamisch gefüllt
                self.weather_forecast_container = forecast_container
                weather_layout.addWidget(forecast_container)
                
                self.weather_container = weather_container
                self.add_bubble(weather_container)

    def _format_german_date(self, date_time, format_type="full"):
        """Formatiert Datum auf Deutsch."""
        weekday = date_time.date().dayOfWeek() - 1  # Qt: 1=Montag, 7=Sonntag
        day = date_time.date().day()
        month = date_time.date().month() - 1  # 0-indexed
        year = date_time.date().year()
        
        weekday_name = DE_WEEKDAYS[weekday]
        month_name = DE_MONTHS[month]
        
        if format_type == "short":
            return f"{weekday_name}, {day:02d}.{month+1:02d}.{year}"
        elif format_type == "medium":
            return f"{weekday_name}, {day}. {month_name} {year}"
        else:  # full
            return f"{weekday_name}, {day}. {month_name} {year}"
    
    def _get_german_timezone_name(self):
        """Gibt deutschen Zeitzonennamen zurück."""
        try:
            is_dst = time.localtime().tm_isdst > 0
            tz_name = time.tzname[1] if is_dst else time.tzname[0]
            
            # Übersetze bekannte Zeitzonen
            tz_translations = {
                "CET": "Mitteleuropäische Zeit",
                "CEST": "Mitteleuropäische Sommerzeit",
                "MEZ": "Mitteleuropäische Zeit",
                "MESZ": "Mitteleuropäische Sommerzeit",
                "GMT": "Greenwich Mean Time",
                "UTC": "Koordinierte Weltzeit"
            }
            
            # Prüfe ob Übersetzung vorhanden
            for key, translation in tz_translations.items():
                if key in tz_name.upper():
                    return translation
            
            # Fallback: Originalname
            return tz_name
        except:
            return "Systemzeit"
    
    def _update_time(self):
        now = QDateTime.currentDateTime()
        current_time = now.toString("HH:mm:ss")
        
        # Calculate GMT offset string
        offset_seconds = now.offsetFromUtc()
        offset_hours = offset_seconds // 3600
        sign = "+" if offset_hours >= 0 else ""
        gmt_offset_str = f"GMT{sign}{offset_hours}"
        
        # Update time label (always present)
        if self.time_label:
            self.time_label.setText(current_time)
        
        # Update date and info based on widget size
        if self.span_w == 1 and self.span_h == 1:
            # 1x1: Only time
            pass
            
        elif self.span_w == 2 and self.span_h == 1:
            # 2x1: Time + Date (kompakt)
            if self.date_label:
                self.date_label.setText(self._format_german_date(now, "short"))
                
        elif self.span_w == 3 and self.span_h == 1:
            # 3x1: Time + Date + GMT
            if self.date_label:
                self.date_label.setText(self._format_german_date(now, "medium"))
            if self.gmt_label:
                utc_now = QDateTime.currentDateTimeUtc()
                gmt_time = utc_now.toString("HH:mm:ss")
                self.gmt_label.setText(f"GMT: {gmt_time} ({gmt_offset_str})")
                
        elif self.span_w == 2 and self.span_h == 2:
            # 2x2: Extended info
            if self.date_label:
                self.date_label.setText(self._format_german_date(now, "full"))
            if self.gmt_label:
                utc_now = QDateTime.currentDateTimeUtc()
                gmt_time = utc_now.toString("HH:mm:ss")
                self.gmt_label.setText(f"GMT: {gmt_time} ({gmt_offset_str})")
            if self.tz_label:
                tz_name = self._get_german_timezone_name()
                self.tz_label.setText(f"Zeitzone: {tz_name}")
            if self.week_label:
                week_num = now.date().weekNumber()[0]
                day_of_year = now.date().dayOfYear()
                self.week_label.setText(f"Kalenderwoche {week_num} • Tag {day_of_year}")
                
        elif self.span_w == 3 and self.span_h == 2:
            # 3x2: Full info + Weather preview
            if self.date_label:
                self.date_label.setText(self._format_german_date(now, "full"))
            if self.gmt_label:
                utc_now = QDateTime.currentDateTimeUtc()
                gmt_time = utc_now.toString("HH:mm:ss")
                self.gmt_label.setText(f"GMT: {gmt_time} ({gmt_offset_str})")
            if self.tz_label:
                tz_name = self._get_german_timezone_name()
                self.tz_label.setText(f"Zeitzone: {tz_name}")
                
        elif self.span_w == 3 and self.span_h == 3:
            # 3x3: Maximum with weather
            if self.date_label:
                self.date_label.setText(self._format_german_date(now, "full"))
            if self.gmt_label:
                utc_now = QDateTime.currentDateTimeUtc()
                gmt_time = utc_now.toString("HH:mm:ss")
                self.gmt_label.setText(f"GMT: {gmt_time} ({gmt_offset_str})")
            if self.tz_label:
                tz_name = self._get_german_timezone_name()
                self.tz_label.setText(f"Zeitzone: {tz_name}")
            if self.dst_label:
                is_dst = time.localtime().tm_isdst > 0
                dst_status = "Sommerzeit (MESZ)" if is_dst else "Winterzeit (MEZ)"
                self.dst_label.setText(dst_status)
            if self.week_label:
                week_num = now.date().weekNumber()[0]
                day_of_year = now.date().dayOfYear()
                self.week_label.setText(f"Kalenderwoche {week_num} • {day_of_year}. Tag des Jahres")
    
    def _load_weather(self):
        """Lädt Wetterdaten asynchron."""
        if not self.weather_service:
            return
        
        try:
            weather_data = self.weather_service.get_weather()
            if weather_data:
                self.weather_data = weather_data
                self._update_weather_display()
        except Exception as e:
            print(f"Weather load error: {e}")
    
    def _update_weather_display(self):
        """Aktualisiert die Wetteranzeige."""
        if not self.weather_data:
            return
        
        current = self.weather_data.get("current", {})
        
        # Update current weather
        if self.weather_icon_label:
            self.weather_icon_label.setText(current.get("icon", "🌤️"))
        
        if self.weather_temp_label:
            temp = current.get("temp", 0)
            self.weather_temp_label.setText(f"{int(temp)}°C")
        
        if self.weather_desc_label:
            desc = current.get("desc", "Unbekannt")
            feels_like = current.get("feels_like", temp)
            humidity = current.get("humidity", 0)
            wind = current.get("wind", 0)
            
            # Formatierung je nach Widget-Größe
            if self.span_w == 3 and self.span_h == 3:
                # 3x3: Vollständige Info
                self.weather_desc_label.setText(f"{desc} • Gefühlt: {int(feels_like)}°C • Luftfeuchtigkeit: {humidity}% • Wind: {wind} km/h")
            else:
                # 3x2: Kompakt
                self.weather_desc_label.setText(f"{desc} • Gefühlt: {int(feels_like)}°C")
        
        # Update forecast for 3x3 widget
        if self.span_w == 3 and self.span_h == 3 and hasattr(self, 'weather_forecast_container'):
            forecast = self.weather_data.get("forecast", [])
            
            # Clear existing forecast widgets
            while self.weather_forecast_container.layout().count():
                child = self.weather_forecast_container.layout().takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            
            # Add forecast widgets
            from datetime import datetime, timedelta
            for idx, day_data in enumerate(forecast[:3]):  # Max 3 days
                day_widget = QWidget()
                day_layout = QVBoxLayout(day_widget)
                day_layout.setContentsMargins(8, 8, 8, 8)
                day_layout.setSpacing(4)
                day_layout.setAlignment(Qt.AlignCenter)
                
                icon_label = QLabel(day_data.get("icon", "🌤️"))
                icon_label.setAlignment(Qt.AlignCenter)
                icon_label.setStyleSheet("font-size: 24px;")
                day_layout.addWidget(icon_label)
                
                temp_label = QLabel(f"{day_data.get('high', 0)}°/{day_data.get('low', 0)}°")
                temp_label.setAlignment(Qt.AlignCenter)
                temp_label.setStyleSheet("font-size: 11px; color: rgba(255, 255, 255, 0.8); font-family: 'Segoe UI';")
                day_layout.addWidget(temp_label)
                
                # Berechne Wochentag für Vorhersage
                forecast_date = datetime.now() + timedelta(days=idx + 1)
                weekday_idx = forecast_date.weekday()  # 0=Montag, 6=Sonntag
                weekday_short = DE_WEEKDAYS[weekday_idx][:2]  # Erste 2 Buchstaben
                
                day_label = QLabel(f"{weekday_short}, {day_data.get('day', '?')}.")
                day_label.setAlignment(Qt.AlignCenter)
                day_label.setStyleSheet("font-size: 9px; color: rgba(255, 255, 255, 0.5); font-family: 'Segoe UI';")
                day_layout.addWidget(day_label)
                
                day_widget.setStyleSheet("""
                    QWidget {
                        background-color: rgba(50, 50, 50, 0.3);
                        border-radius: 8px;
                        border: 1px solid rgba(255, 255, 255, 0.1);
                    }
                """)
                
                self.weather_forecast_container.layout().addWidget(day_widget)

    def rebuild_for_span(self, w, h):
        """Rebuild widget for new span size."""
        self.span_w = w
        self.span_h = h
        super().rebuild_for_span(w, h)
        self._init_ui()
        self._update_time()  # Refresh display

class SystemMonitorWidget(MacGyverWidget):
    def __init__(self):
        super().__init__("System Monitor", size_span=(2, 1))
        self._init_ui()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_stats)
        self.timer.start(1000)
    
    def rebuild_for_span(self, w, h):
        """Rebuild widget for new span size."""
        self.span_w = w
        self.span_h = h
        super().rebuild_for_span(w, h)
        # Clear content_area
        while self.content_area.count():
            item = self.content_area.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        self._init_ui()

    def _init_ui(self):
        container = QWidget()
        
        # Responsive sizing based on span
        if self.span_w == 1 and self.span_h == 1:
            # 1x1: Compact vertical stack with small gauges
            layout = QVBoxLayout(container)
            size = 50  # Reduced from 60px to fit better
        elif self.span_h == 2:
            # 2x2: Larger gauges, vertical or horizontal
            layout = QVBoxLayout(container) if self.span_w == 1 else QHBoxLayout(container)
            size = 100  # Increased from 90px for better visibility
        else:
            # 2x1: Standard horizontal
            layout = QHBoxLayout(container)
            size = 70  # Reduced from 80px for better fit
        
        layout.setSpacing(12)  # Increased spacing
        
        self.cpu_gauge = CircularGauge("CPU", unit="%", size=size)
        self.ram_gauge = CircularGauge("RAM", unit="%", size=size)
        
        layout.addWidget(self.cpu_gauge)
        layout.addWidget(self.ram_gauge)
        
        self.add_bubble(container)

    def _update_stats(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        if hasattr(self, 'cpu_gauge'): self.cpu_gauge.set_value(cpu)
        if hasattr(self, 'ram_gauge'): self.ram_gauge.set_value(ram)

class NetworkMonitorWidget(MacGyverWidget):
    def __init__(self):
        super().__init__("Netzwerk-Traffic", size_span=(2, 1))
        self._init_ui()
        
        self.last_net = psutil.net_io_counters()
        self.last_time = time.time()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_stats)
        self.timer.start(1000)

    def rebuild_for_span(self, w, h):
        """Rebuild widget for new span size."""
        self.span_w = w
        self.span_h = h
        super().rebuild_for_span(w, h)
        # Clear content_area
        while self.content_area.count():
            item = self.content_area.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        self._init_ui()

    def _init_ui(self):
        container = QWidget()
        
        # Calculate gauge size based on widget dimensions
        # Optimized for better space usage
        if self.span_w == 1:
            size = 50  # Reduced for compact fit
            layout = QVBoxLayout(container)
        elif self.span_w == 2:
            size = 60  # Reduced from 70px to prevent overlap
            layout = QHBoxLayout(container)
        else:  # 3x1 or larger
            size = 65  # Slightly reduced for optimal fit
            layout = QHBoxLayout(container)
        
        layout.setSpacing(12)  # Increased spacing
        
        self.up_gauge = CircularGauge("Upload", max_val=1000, unit=" KB/s", size=size)
        self.down_gauge = CircularGauge("Download", max_val=5000, unit=" KB/s", size=size)
        
        layout.addWidget(self.up_gauge)
        layout.addWidget(self.down_gauge)
        
        self.add_bubble(container)

    def _update_stats(self):
        current_net = psutil.net_io_counters()
        current_time = time.time()
        
        dt = current_time - self.last_time
        if dt > 0:
            sent = (current_net.bytes_sent - self.last_net.bytes_sent) / 1024 / dt
            recv = (current_net.bytes_recv - self.last_net.bytes_recv) / 1024 / dt
            
            self.up_gauge.set_value(sent)
            self.down_gauge.set_value(recv)
            
            if sent > self.up_gauge.max_val: self.up_gauge.max_val = sent * 1.2
            if recv > self.down_gauge.max_val: self.down_gauge.max_val = recv * 1.2

        self.last_net = current_net
        self.last_time = current_time

class GPUMonitorWidget(MacGyverWidget):
    def __init__(self):
        super().__init__("GPU-Monitor", size_span=(2, 1))
        self._init_ui()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_stats)
        self.timer.start(1000)

    def rebuild_for_span(self, w, h):
        """Rebuild widget for new span size."""
        self.span_w = w
        self.span_h = h
        super().rebuild_for_span(w, h)
        # Clear content_area
        while self.content_area.count():
            item = self.content_area.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        self._init_ui()

    def _init_ui(self):
        container = QWidget()
        
        # Responsive layout and sizing
        if self.span_w == 1:
            layout = QVBoxLayout(container)
            size = 50  # Reduced for compact fit
        elif self.span_h == 2:
            layout = QHBoxLayout(container) if self.span_w > 1 else QVBoxLayout(container)
            size = 95  # Optimized for tall widgets
        else:  # 2x1
            layout = QHBoxLayout(container)
            size = 70  # Optimized for 2x1
             
        self.add_bubble(container)
        
        self.gpu_gauges = []
        
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            self.has_real_gpus = len(gpus) > 0
        except ImportError:
            self.has_real_gpus = False
            gpus = []

        if self.has_real_gpus:
            for i, gpu in enumerate(gpus):
                gauge = CircularGauge(f"GPU {i}", unit="%", size=size)
                layout.addWidget(gauge)
                self.gpu_gauges.append(gauge)
        else:
            self.gpu0_gauge = CircularGauge("GPU 0", unit="%", size=size)
            self.gpu1_gauge = CircularGauge("GPU 1", unit="%", size=size)
            layout.addWidget(self.gpu0_gauge)
            layout.addWidget(self.gpu1_gauge)
            self.sim_val0 = 10
            self.sim_val1 = 5

    def _update_stats(self):
        if self.has_real_gpus:
            try:
                import GPUtil
                gpus = GPUtil.getGPUs()
                for i, gpu in enumerate(gpus):
                    if i < len(self.gpu_gauges):
                        self.gpu_gauges[i].set_value(gpu.load * 100)
            except Exception as e:
                print(f"GPU Error: {e}")
        else:
            import random
            self.sim_val0 = max(0, min(100, self.sim_val0 + random.randint(-10, 10)))
            self.sim_val1 = max(0, min(100, self.sim_val1 + random.randint(-5, 5)))
            self.gpu0_gauge.set_value(self.sim_val0)
            self.gpu1_gauge.set_value(self.sim_val1)

class TempMonitorWidget(MacGyverWidget):
    def __init__(self):
        super().__init__("Temperatur", size_span=(1, 1))
        
        container = QWidget()
        layout = QHBoxLayout(container)
        
        # Responsive sizing
        size = 75 if self.span_w > 1 else 55
        
        self.temp_gauge = CircularGauge("System", min_val=0, max_val=100, unit="°C", size=size)
        layout.addWidget(self.temp_gauge)
        self.add_bubble(container)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_stats)
        self.timer.start(2000)

    def rebuild_for_span(self, w, h):
        """Rebuild widget for new span size."""
        self.span_w = w
        self.span_h = h
        super().rebuild_for_span(w, h)
        # Clear content_area
        while self.content_area.count():
            item = self.content_area.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        # Rebuild UI
        container = QWidget()
        layout = QHBoxLayout(container)
        size = 75 if w > 1 else 55
        self.temp_gauge = CircularGauge("System", min_val=0, max_val=100, unit="°C", size=size)
        layout.addWidget(self.temp_gauge)
        self.add_bubble(container)

    def _update_stats(self):
        temp = 45
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                for name, entries in temps.items():
                    if entries:
                        temp = entries[0].current
                        break
        except:
            pass
        self.temp_gauge.set_value(temp)

class DiskIOMonitorWidget(MacGyverWidget):
    def __init__(self):
        super().__init__("Datenträger I/O", size_span=(2, 2)) # Large widget
        
        self.container = QWidget()
        self.layout_inner = QVBoxLayout(self.container)
        self.add_bubble(self.container)
        
        self.io_widgets = {}
        self.last_disk = psutil.disk_io_counters(perdisk=True)
        self.last_time = time.time()
        
        self._init_drives()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_stats)
        self.timer.start(1000)

    def rebuild_for_span(self, w, h):
        """Rebuild widget for new span size."""
        self.span_w = w
        self.span_h = h
        super().rebuild_for_span(w, h)
        # Clear content_area
        while self.content_area.count():
            item = self.content_area.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        # Rebuild container
        self.container = QWidget()
        self.layout_inner = QVBoxLayout(self.container)
        self.add_bubble(self.container)
        self._init_drives()

    def _init_drives(self):
        # Clear existing
        while self.layout_inner.count():
            child = self.layout_inner.takeAt(0)
            if child.widget(): child.widget().deleteLater()

        io_counters = psutil.disk_io_counters(perdisk=True)
        if io_counters:
            for key in io_counters:
                drive_layout = QVBoxLayout()
                label = QLabel(f"Disk: {key}")
                label.setStyleSheet("font-weight: bold; color: #ddd;")
                drive_layout.addWidget(label)
                
                r_layout = QHBoxLayout()
                r_bar = QProgressBar()
                r_bar.setRange(0, 100)
                r_bar.setStyleSheet("QProgressBar::chunk { background-color: #34c759; border-radius: 2px; } QProgressBar { background-color: #333; border: none; border-radius: 2px; }")
                r_bar.setFixedHeight(8)
                r_layout.addWidget(QLabel("R"))
                r_layout.addWidget(r_bar)
                
                w_layout = QHBoxLayout()
                w_bar = QProgressBar()
                w_bar.setRange(0, 100)
                w_bar.setStyleSheet("QProgressBar::chunk { background-color: #ff3b30; border-radius: 2px; } QProgressBar { background-color: #333; border: none; border-radius: 2px; }")
                w_bar.setFixedHeight(8)
                w_layout.addWidget(QLabel("W"))
                w_layout.addWidget(w_bar)
                
                drive_layout.addLayout(r_layout)
                drive_layout.addLayout(w_layout)
                
                # Wrapper for spacing
                wrapper = QWidget()
                wrapper.setLayout(drive_layout)
                self.layout_inner.addWidget(wrapper)
                
                self.io_widgets[key] = {'r': r_bar, 'w': w_bar}

    def _update_stats(self):
        current_disk = psutil.disk_io_counters(perdisk=True)
        current_time = time.time()
        dt = current_time - self.last_time
        
        if dt > 0 and current_disk:
            for key, stats in current_disk.items():
                if key in self.io_widgets:
                    prev = self.last_disk.get(key)
                    if prev:
                        read_mb = (stats.read_bytes - prev.read_bytes) / 1024 / 1024 / dt
                        write_mb = (stats.write_bytes - prev.write_bytes) / 1024 / 1024 / dt
                        
                        self.io_widgets[key]['r'].setValue(int(read_mb))
                        self.io_widgets[key]['w'].setValue(int(write_mb))

        self.last_disk = current_disk
        self.last_time = current_time
