"""Internationalization support."""
import locale
import os

# Current language
_current_lang = None
_translations = {}


def detect_language() -> str:
    """Detect system language. Returns 'zh_CN' for Chinese (simplified/traditional), 'en_US' otherwise."""
    try:
        # Try environment variables first
        lang = os.environ.get('LANG', '') or os.environ.get('LANGUAGE', '')
        if not lang:
            # Try system locale
            lang, _ = locale.getdefaultlocale()
        
        if lang:
            lang = lang.lower()
            # Chinese (simplified or traditional) -> zh_CN
            if lang.startswith(('zh', 'chinese')):
                return 'zh_CN'
    except:
        pass
    
    # Default to English
    return 'en_US'


def load_language(lang: str = None):
    """Load language pack."""
    global _current_lang, _translations
    
    if lang is None:
        lang = detect_language()
    
    _current_lang = lang
    
    try:
        if lang == 'zh_CN':
            from .i18n_zh_CN import translations
        else:
            from .i18n_en_US import translations
        _translations = translations
    except ImportError:
        # Fallback to English
        from .i18n_en_US import translations
        _translations = translations


def t(key: str, **kwargs) -> str:
    """Get translated string. Supports format placeholders."""
    if _translations is None:
        load_language()
    
    text = _translations.get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text


# Auto-load on import
load_language()
