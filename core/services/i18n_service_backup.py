"""
i18n Service - Central translation management
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from core.services.user_override_service import get_override_service


class I18nService:
    """Central service for internationalization."""
    
    LANGUAGE_GROUPS = {}  # Will be populated below
    
    def __init__(self):
        pass
