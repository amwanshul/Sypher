import asyncio
import json
import pytest
from pathlib import Path
from tools.registry import ToolRegistry

def test_init_without_schema():
    registry = ToolRegistry()
    assert registry.declarations == []
    assert registry._sync_handlers == {}
    assert registry._live_handlers == {}

def test_init_with_schema(tmp_path):
    schema_path = tmp_path / "schema.json"
    schema_data = [{"name": "test_tool"}]
    schema_path.write_text(json.dumps(schema_data))

    registry = ToolRegistry(schema_path)
    assert registry.declarations == schema_data

def test_load_schemas_success(tmp_path):
    schema_path = tmp_path / "schema.json"
    schema_data = [{"name": "tool1"}, {"name": "tool2"}]
    schema_path.write_text(json.dumps(schema_data))

    registry = ToolRegistry()
    registry.load_schemas(schema_path)
    assert registry.declarations == schema_data

def test_load_schemas_invalid_json(tmp_path):
    schema_path = tmp_path / "schema.json"
    schema_path.write_text("invalid json")

    registry = ToolRegistry()
    with pytest.raises(json.JSONDecodeError):
        registry.load_schemas(schema_path)

def test_load_schemas_not_list(tmp_path):
    schema_path = tmp_path / "schema.json"
    schema_path.write_text(json.dumps({"name": "tool"}))

    registry = ToolRegistry()
    with pytest.raises(ValueError, match="Tool schema file must contain a list of declarations."):
        registry.load_schemas(schema_path)

def test_declarations_property():
    registry = ToolRegistry()
    registry._declarations = [{"name": "tool"}]

    decls = registry.declarations
    assert decls == [{"name": "tool"}]

    # modify copy, original shouldn't change
    decls.append({"name": "new_tool"})
    assert registry.declarations == [{"name": "tool"}]

def test_register_and_execute_sync():
    registry = ToolRegistry()

    def my_handler(params, player, speak):
        return f"Hello {params.get('name')}"

    registry.register_sync("greet", my_handler)

    result = registry.execute_sync("greet", {"name": "World"})
    assert result == "Hello World"

def test_execute_sync_not_found():
    registry = ToolRegistry()
    with pytest.raises(KeyError, match="'unknown_tool'"):
        registry.execute_sync("unknown_tool", {})

def test_register_and_execute_live():
    registry = ToolRegistry()

    async def my_live_handler(params, player, speak, loop):
        await asyncio.sleep(0) # Simulate async work
        return f"Async {params.get('val')}"

    registry.register_live("async_task", my_live_handler)

    result = asyncio.run(registry.execute_live("async_task", {"val": 42}))
    assert result == "Async 42"

def test_execute_live_fallback_to_sync():
    registry = ToolRegistry()

    def my_sync_handler(params, player, speak):
        return f"Sync {params.get('val')}"

    registry.register_sync("sync_task", my_sync_handler)

    result = asyncio.run(registry.execute_live("sync_task", {"val": 42}))
    assert result == "Sync 42"

def test_execute_live_not_found():
    registry = ToolRegistry()
    with pytest.raises(KeyError, match="'unknown_tool'"):
        asyncio.run(registry.execute_live("unknown_tool", {}))
