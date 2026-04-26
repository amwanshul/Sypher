import pytest
from tools.registry import ToolRegistry


def test_execute_sync_missing_handler():
    registry = ToolRegistry()
    with pytest.raises(KeyError) as exc_info:
        registry.execute_sync("dummy_tool", {})
    assert "dummy_tool" in str(exc_info.value)
