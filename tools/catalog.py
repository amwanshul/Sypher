from __future__ import annotations

import inspect
import threading
from pathlib import Path

from actions.browser_control import browser_control
from actions.cmd_control import cmd_control
from actions.code_helper import code_helper
from actions.computer_control import computer_control
from actions.computer_settings import computer_settings
from actions.desktop import desktop_control
from actions.dev_agent import dev_agent
from actions.file_controller import file_controller
from actions.flight_finder import flight_finder
from actions.open_app import open_app
from actions.reminder import reminder
from actions.screen_processor import screen_process
from actions.send_message import send_message
from actions.weather_report import weather_action
from actions.web_search import web_search
from actions.youtube_video import youtube_video
from tools.registry import ToolRegistry
from tools.untrusted_code import generate_and_run_python


SCHEMA_PATH = Path(__file__).with_name("schemas.json")
TOOL_REGISTRY = ToolRegistry(SCHEMA_PATH)
TOOL_DECLARATIONS = TOOL_REGISTRY.declarations


def _invoke_action(func, parameters: dict, *, player=None, speak=None):
    kwargs = {}
    signature = inspect.signature(func).parameters
    if "parameters" in signature:
        kwargs["parameters"] = parameters
    if "response" in signature:
        kwargs["response"] = None
    if "player" in signature:
        kwargs["player"] = player
    if "session_memory" in signature:
        kwargs["session_memory"] = None
    if "speak" in signature:
        kwargs["speak"] = speak
    return func(**kwargs)


def _default_message(message):
    if callable(message):
        return message
    return lambda _parameters: message


def _register_simple(name: str, func, default_message) -> None:
    fallback = _default_message(default_message)

    def handler(parameters: dict, player=None, speak=None) -> str:
        result = _invoke_action(func, parameters, player=player, speak=speak)
        return result or fallback(parameters)

    TOOL_REGISTRY.register_sync(name, handler)


def _screen_process_sync(parameters: dict, player=None, speak=None) -> str:
    _invoke_action(screen_process, parameters, player=player, speak=speak)
    return "Vision module activated. Stay completely silent - vision module will speak directly."


async def _screen_process_live(parameters: dict, player=None, speak=None, loop=None) -> str:
    threading.Thread(
        target=screen_process,
        kwargs={
            "parameters": parameters,
            "response": None,
            "player": player,
            "session_memory": None,
        },
        daemon=True,
    ).start()
    return "Vision module activated. Stay completely silent - vision module will speak directly."


def _agent_task_sync(parameters: dict, player=None, speak=None) -> str:
    from agent.task_queue import TaskPriority, get_queue

    goal = parameters.get("goal", "")
    priority_str = str(parameters.get("priority", "normal")).lower()
    priority_map = {
        "low": TaskPriority.LOW,
        "normal": TaskPriority.NORMAL,
        "high": TaskPriority.HIGH,
    }
    task_id = get_queue().submit(
        goal=goal,
        priority=priority_map.get(priority_str, TaskPriority.NORMAL),
        speak=speak,
        player=player,
    )
    return f"Task started (ID: {task_id}). I'll update you as I make progress, sir."


async def _agent_task_live(parameters: dict, player=None, speak=None, loop=None) -> str:
    return _agent_task_sync(parameters, player=player, speak=speak)


def _generated_code_sync(parameters: dict, player=None, speak=None) -> str:
    return generate_and_run_python(parameters, player=player, speak=speak)


_register_simple("open_app", open_app, lambda p: f"Opened {p.get('app_name')} successfully.")
_register_simple("weather_report", weather_action, lambda p: f"Weather report for {p.get('city')} delivered.")
_register_simple("browser_control", browser_control, "Browser action completed.")
_register_simple("file_controller", file_controller, "File operation completed.")
_register_simple("send_message", send_message, lambda p: f"Message sent to {p.get('receiver')}.")
_register_simple("reminder", reminder, lambda p: f"Reminder set for {p.get('date')} at {p.get('time')}.")
_register_simple("youtube_video", youtube_video, "Done.")
_register_simple("computer_settings", computer_settings, "Done.")
_register_simple("cmd_control", cmd_control, "Command executed.")
_register_simple("desktop_control", desktop_control, "Desktop action completed.")
_register_simple("code_helper", code_helper, "Done.")
_register_simple("dev_agent", dev_agent, "Done.")
_register_simple("web_search", web_search, "Search completed.")
_register_simple("computer_control", computer_control, "Done.")
_register_simple("flight_finder", flight_finder, "Done.")
TOOL_REGISTRY.register_sync("screen_process", _screen_process_sync)
TOOL_REGISTRY.register_live("screen_process", _screen_process_live)
TOOL_REGISTRY.register_sync("agent_task", _agent_task_sync)
TOOL_REGISTRY.register_live("agent_task", _agent_task_live)
TOOL_REGISTRY.register_sync("generated_code", _generated_code_sync)
