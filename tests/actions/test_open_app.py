from unittest.mock import patch
from actions.open_app import _normalize

def test_normalize_exact_match_windows():
    with patch('platform.system', return_value='Windows'):
        assert _normalize("whatsapp") == "WhatsApp"
        assert _normalize("chrome") == "chrome"
        assert _normalize("google chrome") == "chrome"

def test_normalize_exact_match_darwin():
    with patch('platform.system', return_value='Darwin'):
        assert _normalize("whatsapp") == "WhatsApp"
        assert _normalize("chrome") == "Google Chrome"

def test_normalize_exact_match_linux():
    with patch('platform.system', return_value='Linux'):
        assert _normalize("whatsapp") == "whatsapp"
        assert _normalize("chrome") == "google-chrome"

def test_normalize_partial_match():
    with patch('platform.system', return_value='Windows'):
        # 'vscode' is an alias_key for 'code' in Windows
        assert _normalize("open vscode please") == "code"
        assert _normalize("visual studio code") == "code"

def test_normalize_unrecognized_app():
    with patch('platform.system', return_value='Windows'):
        assert _normalize("UnknownApp") == "UnknownApp"
        assert _normalize("  Some Weird App  ") == "  Some Weird App  "

def test_normalize_stripping_and_lowercasing():
    with patch('platform.system', return_value='Windows'):
        assert _normalize("  WHATSAPP  ") == "WhatsApp"
