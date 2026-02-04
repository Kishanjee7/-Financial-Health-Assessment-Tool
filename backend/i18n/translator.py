"""
Translation service for multilingual support.
"""
from typing import Dict, List, Optional
from i18n.translations import TRANSLATIONS, get_translation, get_all_translations
from config import settings


class Translator:
    """Provides translation services for the platform."""
    
    def __init__(self, default_language: str = None):
        self.default_language = default_language or settings.DEFAULT_LANGUAGE
        self.supported_languages = settings.SUPPORTED_LANGUAGES
    
    def translate(self, key: str, language: str = None) -> str:
        """Translate a single key."""
        lang = language or self.default_language
        return get_translation(key, lang)
    
    def translate_dict(self, data: Dict, language: str = None) -> Dict:
        """Translate translatable keys in a dictionary."""
        lang = language or self.default_language
        translated = {}
        
        for key, value in data.items():
            if isinstance(value, str) and value.startswith('$'):
                # Keys starting with $ are translation keys
                translated[key] = get_translation(value[1:], lang)
            elif isinstance(value, dict):
                translated[key] = self.translate_dict(value, lang)
            elif isinstance(value, list):
                translated[key] = self.translate_list(value, lang)
            else:
                translated[key] = value
        
        return translated
    
    def translate_list(self, items: List, language: str = None) -> List:
        """Translate items in a list."""
        lang = language or self.default_language
        translated = []
        
        for item in items:
            if isinstance(item, str) and item.startswith('$'):
                translated.append(get_translation(item[1:], lang))
            elif isinstance(item, dict):
                translated.append(self.translate_dict(item, lang))
            else:
                translated.append(item)
        
        return translated
    
    def get_ui_labels(self, language: str = None) -> Dict:
        """Get all UI labels for a language."""
        lang = language or self.default_language
        return get_all_translations(lang)
    
    def format_currency(self, amount: float, language: str = None) -> str:
        """Format currency based on language."""
        lang = language or self.default_language
        
        if lang == 'hi':
            # Indian numbering system (lakhs, crores)
            if amount >= 10000000:
                return f"₹{amount/10000000:.2f} करोड़"
            elif amount >= 100000:
                return f"₹{amount/100000:.2f} लाख"
            else:
                return f"₹{amount:,.2f}"
        else:
            # Standard formatting
            if amount >= 10000000:
                return f"₹{amount/10000000:.2f} Cr"
            elif amount >= 100000:
                return f"₹{amount/100000:.2f} L"
            else:
                return f"₹{amount:,.2f}"
    
    def format_percentage(self, value: float, language: str = None) -> str:
        """Format percentage."""
        return f"{value * 100:.1f}%"
    
    def get_rating_text(self, rating: str, language: str = None) -> str:
        """Get localized rating text."""
        rating_keys = {
            'excellent': 'excellent',
            'good': 'good',
            'fair': 'fair',
            'poor': 'needs_attention',
            'critical': 'critical'
        }
        key = rating_keys.get(rating.lower(), rating)
        return self.translate(key, language)
    
    def get_risk_text(self, risk_level: str, language: str = None) -> str:
        """Get localized risk level text."""
        risk_keys = {
            'low': 'low_risk',
            'medium': 'medium_risk',
            'high': 'high_risk',
            'critical': 'critical_risk'
        }
        key = risk_keys.get(risk_level.lower(), risk_level)
        return self.translate(key, language)


translator = Translator()
