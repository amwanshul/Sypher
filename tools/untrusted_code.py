from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Callable

from security.approval import require_untrusted_execution_approval


BASE_DIR = Path(__file__).resolve().parent.parent
API_CONFIG_PATH = BASE_DIR / "config" / "api_keys.json"


def _get_api_key() -> str:
    with open(API_CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["gemini_api_key"]


def _describe_system_paths() -> str:
    home = Path.home()
    desktop = home / "Desktop"
    downloads = home / "Downloads"
    documents = home / "Documents"
    return (
        f"Desktop   = r'{desktop}'\n"
        f"Downloads = r'{downloads}'\n"
        f"Documents = r'{documents}'\n"
        f"Home      = r'{home}'\n"
    )


def generate_and_run_python(
    parameters: dict,
    player=None,
    speak: Callable | None = None,
) -> str:
    import google.generativeai as genai

    description = (parameters or {}).get("description", "").strip()
    if not description:
        raise ValueError("generated_code requires a 'description' parameter.")

    genai.configure(api_key=_get_api_key())
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=(
            "You are an expert Python developer. "
            "Write clean, complete, working Python code. "
            "Do not install packages. Do not use subprocess, shell commands, or network calls. "
            "Do not delete files or modify locations outside temporary working directories. "
            "Return ONLY the Python code. No explanation, no markdown, no backticks.\n\n"
            f"SYSTEM PATHS:\n{_describe_system_paths()}"
        ),
    )

    response = model.generate_content(
        f"Write Python code to accomplish this task safely:\n\n{description}"
    )
    code = response.text.strip()
    code = re.sub(r"```(?:python)?", "", code).strip().rstrip("`").strip()

    approved, message = require_untrusted_execution_approval(
        player=player,
        source="generated_code",
        reason=description,
        code_preview=code,
    )
    if not approved:
        if speak:
            speak(message)
        return message

    if speak:
        speak("Approval received. Running the generated code now.")

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".py",
        delete=False,
        encoding="utf-8",
    ) as f:
        f.write(code)
        tmp_path = f.name

    try:
        result = subprocess.run(
            [sys.executable, tmp_path],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(Path.home()),
        )
    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass

    output = result.stdout.strip()
    error = result.stderr.strip()

    if result.returncode == 0 and output:
        return output
    if result.returncode == 0:
        return "Task completed successfully."
    if error:
        raise RuntimeError(f"Code error: {error[:400]}")
    return "Completed."
