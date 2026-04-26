from actions.web_search import _compare


def test_compare_empty_list():
    assert _compare([], "speed") == ""


def test_compare_single_item():
    assert _compare(["Apple"], "speed") == "Sadece bir sonuç var: Apple"


def test_compare_multiple_items_mocked(monkeypatch):
    def mock_gemini_search(query):
        return f"Mocked comparison for {query}"

    monkeypatch.setattr(
        "actions.web_search._gemini_search", mock_gemini_search
    )
    result = _compare(["Apple", "Banana"], "taste")

    expected = (
        "Mocked comparison for Compare Apple, Banana in terms of taste. "
        "Give specific facts and data."
    )
    assert result == expected


def test_compare_multiple_items_fallback(monkeypatch, capsys):
    def mock_gemini_search(query):
        raise Exception("API Error")

    def mock_ddg_search(query, max_results):
        return [{"snippet": f"Mock DDG result for {query}"}]

    monkeypatch.setattr(
        "actions.web_search._gemini_search", mock_gemini_search
    )
    monkeypatch.setattr("actions.web_search._ddg_search", mock_ddg_search)

    result = _compare(["Apple", "Banana"], "taste")

    # Check the printed output
    captured = capsys.readouterr()
    assert "[WebSearch] ⚠️ Gemini compare failed: API Error" in captured.out

    # Check the actual result format
    assert "Comparison — TASTE" in result
    assert "▸ Apple" in result
    assert "• Mock DDG result for Apple taste" in result
    assert "▸ Banana" in result
    assert "• Mock DDG result for Banana taste" in result
