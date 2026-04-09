from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Awaitable, Callable


SyncToolHandler = Callable[[dict, object | None, Callable | None], str]
LiveToolHandler = Callable[
    [dict, object | None, Callable | None, asyncio.AbstractEventLoop | None],
    Awaitable[str],
]


class ToolRegistry:
    def __init__(self, schema_path: Path | None = None):
        self._declarations: list[dict] = []
        self._sync_handlers: dict[str, SyncToolHandler] = {}
        self._live_handlers: dict[str, LiveToolHandler] = {}
        if schema_path is not None:
            self.load_schemas(schema_path)

    def load_schemas(self, schema_path: Path) -> None:
        declarations = json.loads(schema_path.read_text(encoding="utf-8"))
        if not isinstance(declarations, list):
            raise ValueError("Tool schema file must contain a list of declarations.")
        self._declarations = declarations

    @property
    def declarations(self) -> list[dict]:
        return list(self._declarations)

    def register_sync(self, name: str, handler: SyncToolHandler) -> None:
        self._sync_handlers[name] = handler

    def register_live(self, name: str, handler: LiveToolHandler) -> None:
        self._live_handlers[name] = handler

    def execute_sync(
        self,
        name: str,
        parameters: dict,
        *,
        player=None,
        speak=None,
    ) -> str:
        if name not in self._sync_handlers:
            raise KeyError(name)
        return self._sync_handlers[name](parameters, player, speak)

    async def execute_live(
        self,
        name: str,
        parameters: dict,
        *,
        player=None,
        speak=None,
        loop: asyncio.AbstractEventLoop | None = None,
    ) -> str:
        if name in self._live_handlers:
            return await self._live_handlers[name](parameters, player, speak, loop)
        if name not in self._sync_handlers:
            raise KeyError(name)
        if loop is None:
            loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None,
            lambda: self._sync_handlers[name](parameters, player, speak),
        )
