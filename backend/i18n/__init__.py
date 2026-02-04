"""i18n package initialization."""
from i18n.translations import TRANSLATIONS, get_translation, get_all_translations
from i18n.translator import Translator, translator

__all__ = ["TRANSLATIONS", "get_translation", "get_all_translations", "Translator", "translator"]
