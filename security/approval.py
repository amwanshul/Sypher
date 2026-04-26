
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
SETTINGS_PATH = BASE_DIR / "config" / "safety_settings.json"

DEFAULT_SETTINGS = {
    "allow_untrusted_code_execution": False,
    "require_confirmation_for_untrusted_code": True,
    "require_confirmation_for_file_delete": True,
}


def _ensure_settings_file() -> None:
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    if SETTINGS_PATH.exists():
        return
    SETTINGS_PATH.write_text(
        json.dumps(DEFAULT_SETTINGS, indent=2),
        encoding="utf-8",
    )


def load_safety_settings() -> dict:
    _ensure_settings_file()
    try:
        raw = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
    except Exception:
        raw = {}
    settings = dict(DEFAULT_SETTINGS)
    settings.update({k: raw.get(k, v) for k, v in DEFAULT_SETTINGS.items()})
    return settings


def _shorten(text: str, limit: int = 900) -> str:
    cleaned = (text or "").strip()
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 3].rstrip() + "..."


def require_untrusted_execution_approval(
    *,
    player=None,
    source: str,
    reason: str,
    code_preview: str = "",
) -> tuple[bool, str]:
    settings = load_safety_settings()

    if not settings["allow_untrusted_code_execution"]:
        return (
            False,
            "Untrusted code execution is disabled. "
            "Enable it in config/safety_settings.json to allow this action.",
        )

    if not settings["require_confirmation_for_untrusted_code"]:
        return True, ""

    if player is None or not hasattr(player, "confirm_action"):
        return (
            False,
            "Execution requires a confirmation-capable UI, but no confirmation channel is available.",
        )

    message = (
        f"Source: {source}\n\n"
        f"Reason:\n{_shorten(reason, 350) or 'No reason provided.'}\n\n"
        f"Code preview:\n{_shorten(code_preview, 1200) or 'No preview available.'}\n\n"
        "Approve running this untrusted code on the host machine?"
    )
    approved = player.confirm_action(
        "Approve Untrusted Code",
        message,
        default=False,
    )
    if approved:
        return True, ""
    return False, "Execution cancelled. Untrusted code was not run."


def require_file_delete_approval(*, player=None, target: str) -> tuple[bool, str]:
    settings = load_safety_settings()

    if not settings["require_confirmation_for_file_delete"]:
        return True, ""

    if player is None or not hasattr(player, "confirm_action"):
        return (
            False,
            "Delete actions require a visible confirmation dialog, but no UI is available.",
        )

    approved = player.confirm_action(
        "Confirm Delete",
        (
            "A delete action was requested for:\n"
            f"{target}\n\n"
            "Approve moving this item to the Recycle Bin or deleting it?"
        ),
        default=False,
    )
    if approved:
        return True, ""
    return False, "Delete cancelled. No files were removed."
