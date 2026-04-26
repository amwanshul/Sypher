from unittest.mock import patch, MagicMock

from actions.send_message import (
    _open_app,
    _search_contact,
    _type_and_send,
    _send_whatsapp,
    _send_instagram,
    _send_telegram,
    _send_generic,
    send_message
)

# Helpers

@patch("actions.send_message.pyautogui")
@patch("actions.send_message.time.sleep")
def test_open_app_success(mock_sleep, mock_pyautogui):
    # Test _open_app happy path
    result = _open_app("WhatsApp")
    assert result is True
    mock_pyautogui.press.assert_any_call("win")
    mock_pyautogui.write.assert_called_with("WhatsApp", interval=0.04)
    mock_pyautogui.press.assert_any_call("enter")

@patch("actions.send_message.pyautogui")
@patch("actions.send_message.time.sleep")
def test_open_app_exception(mock_sleep, mock_pyautogui):
    # Test _open_app exception handling
    mock_pyautogui.press.side_effect = Exception("Test Error")
    result = _open_app("WhatsApp")
    assert result is False

@patch("actions.send_message.pyautogui")
@patch("actions.send_message.time.sleep")
def test_search_contact(mock_sleep, mock_pyautogui):
    _search_contact("John Doe", "Platform")
    mock_pyautogui.hotkey.assert_any_call("ctrl", "f")
    mock_pyautogui.hotkey.assert_any_call("ctrl", "a")
    mock_pyautogui.write.assert_called_with("John Doe", interval=0.04)
    mock_pyautogui.press.assert_called_with("enter")

@patch("actions.send_message.pyautogui")
@patch("actions.send_message.time.sleep")
def test_type_and_send(mock_sleep, mock_pyautogui):
    _type_and_send("Hello World")
    mock_pyautogui.press.assert_any_call("tab")
    mock_pyautogui.hotkey.assert_any_call("ctrl", "a")
    mock_pyautogui.write.assert_called_with("Hello World", interval=0.03)
    mock_pyautogui.press.assert_any_call("enter")

# Specific Senders

@patch("actions.send_message._open_app")
@patch("actions.send_message.pyautogui")
@patch("actions.send_message.time.sleep")
def test_send_whatsapp_success(mock_sleep, mock_pyautogui, mock_open_app):
    mock_open_app.return_value = True
    result = _send_whatsapp("John Doe", "Hello")
    assert "Message sent to John Doe via WhatsApp" in result
    mock_open_app.assert_called_with("WhatsApp")
    mock_pyautogui.write.assert_any_call("John Doe", interval=0.04)
    mock_pyautogui.write.assert_any_call("Hello", interval=0.03)

@patch("actions.send_message._open_app")
def test_send_whatsapp_open_fail(mock_open_app):
    mock_open_app.return_value = False
    result = _send_whatsapp("John Doe", "Hello")
    assert result == "Could not open WhatsApp."

@patch("actions.send_message._open_app")
def test_send_whatsapp_exception(mock_open_app):
    mock_open_app.side_effect = Exception("Test Error")
    result = _send_whatsapp("John Doe", "Hello")
    assert "WhatsApp error: Test Error" in result

@patch("webbrowser.open")
@patch("actions.send_message.pyautogui")
@patch("actions.send_message.time.sleep")
def test_send_instagram_success(mock_sleep, mock_pyautogui, mock_webbrowser_open):
    result = _send_instagram("John Doe", "Hello")
    assert "Message sent to John Doe via Instagram" in result
    mock_webbrowser_open.assert_called_with("https://www.instagram.com/direct/new/")
    mock_pyautogui.write.assert_any_call("John Doe", interval=0.05)
    mock_pyautogui.write.assert_any_call("Hello", interval=0.04)

@patch("webbrowser.open")
def test_send_instagram_exception(mock_webbrowser_open):
    mock_webbrowser_open.side_effect = Exception("Test Error")
    result = _send_instagram("John Doe", "Hello")
    assert "Instagram error: Test Error" in result

@patch("actions.send_message._open_app")
@patch("actions.send_message.pyautogui")
@patch("actions.send_message.time.sleep")
def test_send_telegram_success(mock_sleep, mock_pyautogui, mock_open_app):
    mock_open_app.return_value = True
    result = _send_telegram("John Doe", "Hello")
    assert "Message sent to John Doe via Telegram" in result
    mock_open_app.assert_called_with("Telegram")

@patch("actions.send_message._open_app")
def test_send_telegram_open_fail(mock_open_app):
    mock_open_app.return_value = False
    result = _send_telegram("John Doe", "Hello")
    assert result == "Could not open Telegram."

@patch("actions.send_message._open_app")
def test_send_telegram_exception(mock_open_app):
    mock_open_app.side_effect = Exception("Test Error")
    result = _send_telegram("John Doe", "Hello")
    assert "Telegram error: Test Error" in result

@patch("actions.send_message._open_app")
@patch("actions.send_message.pyautogui")
@patch("actions.send_message.time.sleep")
def test_send_generic_success(mock_sleep, mock_pyautogui, mock_open_app):
    mock_open_app.return_value = True
    result = _send_generic("Signal", "John Doe", "Hello")
    assert "Message sent to John Doe via Signal" in result
    mock_open_app.assert_called_with("Signal")

@patch("actions.send_message._open_app")
def test_send_generic_open_fail(mock_open_app):
    mock_open_app.return_value = False
    result = _send_generic("Signal", "John Doe", "Hello")
    assert result == "Could not open Signal."

@patch("actions.send_message._open_app")
def test_send_generic_exception(mock_open_app):
    mock_open_app.side_effect = Exception("Test Error")
    result = _send_generic("Signal", "John Doe", "Hello")
    assert "Signal error: Test Error" in result

# Main send_message tests

def test_send_message_missing_receiver():
    result = send_message({"message_text": "Hello"})
    assert result == "Please specify who to send the message to, sir."

def test_send_message_missing_message():
    result = send_message({"receiver": "John Doe"})
    assert result == "Please specify what message to send, sir."

@patch("actions.send_message._send_whatsapp")
def test_send_message_routes_whatsapp(mock_send_whatsapp):
    mock_send_whatsapp.return_value = "Success"

    # Test different aliases
    for platform in ["whatsapp", "wp", "wapp"]:
        mock_player = MagicMock()
        result = send_message({"receiver": "John", "message_text": "Hi", "platform": platform}, player=mock_player)
        assert result == "Success"
        mock_send_whatsapp.assert_called_with("John", "Hi")
        mock_player.write_log.assert_called()

@patch("actions.send_message._send_instagram")
def test_send_message_routes_instagram(mock_send_instagram):
    mock_send_instagram.return_value = "Success"

    for platform in ["instagram", "ig", "insta"]:
        mock_player = MagicMock()
        result = send_message({"receiver": "John", "message_text": "Hi", "platform": platform}, player=mock_player)
        assert result == "Success"
        mock_send_instagram.assert_called_with("John", "Hi")

@patch("actions.send_message._send_telegram")
def test_send_message_routes_telegram(mock_send_telegram):
    mock_send_telegram.return_value = "Success"

    for platform in ["telegram", "tg"]:
        mock_player = MagicMock()
        result = send_message({"receiver": "John", "message_text": "Hi", "platform": platform}, player=mock_player)
        assert result == "Success"
        mock_send_telegram.assert_called_with("John", "Hi")

@patch("actions.send_message._send_generic")
def test_send_message_routes_generic(mock_send_generic):
    mock_send_generic.return_value = "Success"

    mock_player = MagicMock()
    result = send_message({"receiver": "John", "message_text": "Hi", "platform": "discord"}, player=mock_player)
    assert result == "Success"
    mock_send_generic.assert_called_with("discord", "John", "Hi")
