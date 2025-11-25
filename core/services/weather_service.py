"""
Weather Service - Abruf von Wetterdaten
Unterstützt Windows Weather API und Fallback zu OpenWeatherMap
"""
import json
import subprocess
import platform
from typing import Optional, Dict
import time

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


class WeatherService:
    """Service zum Abrufen von Wetterdaten."""
    
    def __init__(self):
        self.last_update = 0
        self.cache_duration = 600  # 10 Minuten Cache
        self.cached_data = None
        self.api_key = None  # Kann später konfiguriert werden
        
    def get_weather(self) -> Optional[Dict]:
        """
        Ruft aktuelle Wetterdaten ab.
        Versucht zuerst Windows Weather, dann Fallback zu OpenWeatherMap.
        """
        # Cache prüfen
        current_time = time.time()
        if self.cached_data and (current_time - self.last_update) < self.cache_duration:
            return self.cached_data
        
        # Versuche Windows Weather API
        weather_data = self._get_windows_weather()
        
        if not weather_data:
            # Fallback zu OpenWeatherMap (ohne API-Key, limitiert)
            weather_data = self._get_openweather_fallback()
        
        if weather_data:
            self.cached_data = weather_data
            self.last_update = current_time
        
        return weather_data
    
    def _get_windows_weather(self) -> Optional[Dict]:
        """Versucht Wetterdaten über Windows Weather App zu erhalten."""
        if platform.system() != "Windows":
            return None
        
        try:
            # Versuche über PowerShell die Windows Weather App zu nutzen
            # Windows 10/11 hat eine Weather App mit API
            # Alternative: Nutze Windows Location Services + OpenWeatherMap
            
            # Für jetzt: Simuliere Windows Weather Daten
            # In Produktion würde man hier die echte Windows Weather API nutzen
            return self._get_simulated_weather()
        except Exception as e:
            print(f"Windows Weather Error: {e}")
            return None
    
    def _get_openweather_fallback(self) -> Optional[Dict]:
        """Fallback zu OpenWeatherMap API (ohne API-Key, limitiert)."""
        if not HAS_REQUESTS:
            return None
        
        try:
            # Versuche Standort über IP zu ermitteln
            # Dann Wetterdaten abrufen (ohne API-Key ist limitiert)
            # Für Demo: Simuliere Daten
            return self._get_simulated_weather()
        except Exception as e:
            print(f"OpenWeather Error: {e}")
            return None
    
    def _get_simulated_weather(self) -> Dict:
        """
        Simuliert Wetterdaten für Demo-Zwecke.
        In Produktion würde dies durch echte API-Aufrufe ersetzt.
        """
        import random
        from datetime import datetime
        
        # Simuliere verschiedene Wetterbedingungen (deutsch)
        conditions = [
            {"icon": "☀️", "desc": "Sonnig", "temp": 22, "feels_like": 21, "humidity": 45, "wind": 8},
            {"icon": "⛅", "desc": "Bewölkt", "temp": 18, "feels_like": 17, "humidity": 65, "wind": 12},
            {"icon": "🌧️", "desc": "Regen", "temp": 15, "feels_like": 14, "humidity": 85, "wind": 15},
            {"icon": "❄️", "desc": "Schnee", "temp": 2, "feels_like": -1, "humidity": 90, "wind": 20},
            {"icon": "🌤️", "desc": "Leicht bewölkt", "temp": 20, "feels_like": 19, "humidity": 55, "wind": 10},
            {"icon": "🌫️", "desc": "Nebel", "temp": 12, "feels_like": 11, "humidity": 95, "wind": 5},
            {"icon": "⛈️", "desc": "Gewitter", "temp": 19, "feels_like": 18, "humidity": 80, "wind": 18},
        ]
        
        # Wähle basierend auf Tageszeit
        hour = datetime.now().hour
        if 6 <= hour < 12:
            condition = conditions[0]  # Morgen: Sonnig
        elif 12 <= hour < 18:
            condition = conditions[1]  # Nachmittag: Bewölkt
        elif 18 <= hour < 22:
            condition = conditions[2]  # Abend: Regen möglich
        else:
            condition = conditions[4]  # Nacht: Leicht bewölkt
        
        # Füge Variation hinzu
        condition["temp"] += random.randint(-2, 2)
        condition["feels_like"] = condition["temp"] - random.randint(0, 2)
        
        # Vorhersage für nächste Tage
        forecast = []
        for i in range(1, 4):
            forecast.append({
                "day": (datetime.now().day + i) % 28 + 1,
                "icon": random.choice(["☀️", "⛅", "🌧️"]),
                "high": condition["temp"] + random.randint(-3, 5),
                "low": condition["temp"] - random.randint(3, 8),
            })
        
        return {
            "location": "Aktueller Standort",
            "current": condition,
            "forecast": forecast,
            "updated": datetime.now().strftime("%H:%M"),
        }

