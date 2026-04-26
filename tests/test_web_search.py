from unittest.mock import patch
from actions.web_search import _compare


def test_compare_success():
    with patch("actions.web_search._gemini_search") as mock_gemini:
        mock_gemini.return_value = "Gemini comparison result"
        result = _compare(["Apple", "Orange"], "taste")
        assert result == "Gemini comparison result"
        msg = (
            "Compare Apple, Orange in terms of taste. "
            "Give specific facts and data."
        )
        mock_gemini.assert_called_once_with(msg)


def test_compare_fallback():
    with patch("actions.web_search._gemini_search") as mock_gemini, \
         patch("actions.web_search._ddg_search") as mock_ddg:

        mock_gemini.side_effect = Exception("API Error")

        def ddg_side_effect(query, max_results):
            if "Apple" in query:
                return [{"snippet": "Apple is sweet."}]
            elif "Orange" in query:
                return [{"snippet": "Orange is citrusy."}]
            return []

        mock_ddg.side_effect = ddg_side_effect

        result = _compare(["Apple", "Orange"], "taste")

        assert "Comparison — TASTE" in result
        assert "▸ Apple" in result
        assert "• Apple is sweet." in result
        assert "▸ Orange" in result
        assert "• Orange is citrusy." in result


def test_compare_fallback_ddg_error():
    with patch("actions.web_search._gemini_search") as mock_gemini, \
         patch("actions.web_search._ddg_search") as mock_ddg:

        mock_gemini.side_effect = Exception("API Error")
        mock_ddg.side_effect = Exception("DDG Error")

        result = _compare(["Apple"], "taste")

        assert "Comparison — TASTE" in result
        assert "▸ Apple" in result
