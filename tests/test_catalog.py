from tools.catalog import (
    _default_message,
    _invoke_action,
    _register_simple,
    TOOL_REGISTRY
)


def test_default_message_with_string():
    msg = "Test message"
    fallback = _default_message(msg)
    assert callable(fallback)
    assert fallback({"param": "value"}) == msg


def test_default_message_with_callable():
    def mock_message(parameters):
        return f"Message: {parameters.get('key')}"
    fallback = _default_message(mock_message)
    assert callable(fallback)
    assert fallback({"key": "value"}) == "Message: value"


def test_invoke_action_no_args():
    def mock_func():
        return "Success"
    result = _invoke_action(mock_func, {"test": "val"})
    assert result == "Success"


def test_invoke_action_all_args():
    def mock_func(parameters, player, speak, response, session_memory):
        assert parameters == {"test": "val"}
        assert player == "mock_player"
        assert speak == "mock_speak"
        assert response is None
        assert session_memory is None
        return "Success"
    result = _invoke_action(
        mock_func,
        {"test": "val"},
        player="mock_player",
        speak="mock_speak"
    )
    assert result == "Success"


def test_register_simple():
    name = "test_simple_action"

    def mock_func(parameters):
        if parameters.get("fail"):
            return None
        return "Action Result"

    _register_simple(name, mock_func, "Default Backup Message")

    # Verify it registered with registry
    assert name in TOOL_REGISTRY._sync_handlers

    # Test success path
    handler = TOOL_REGISTRY._sync_handlers[name]
    result1 = handler({"fail": False})
    assert result1 == "Action Result"

    # Test fallback path
    result2 = handler({"fail": True})
    assert result2 == "Default Backup Message"
