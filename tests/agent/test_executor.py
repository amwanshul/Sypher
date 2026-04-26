from agent.executor import _detect_language


def test_detect_language_english():
    assert _detect_language("This is a simple text in English.") == "en"


def test_detect_language_turkish():
    assert _detect_language("Bu basit bir Türkçe metindir. şğüöçı") == "tr"


def test_detect_language_mixed():
    assert _detect_language("This is mixed text. ç") == "tr"


def test_detect_language_empty():
    assert _detect_language("") == "en"


def test_detect_language_caps():
    assert _detect_language("TÜRKÇE KARAKTERLER ÇĞIÖŞÜ") == "tr"
