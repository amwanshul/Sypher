import pytest
from memory.memory_manager import _empty_memory

def test_empty_memory():
    """Test that _empty_memory returns the expected default dictionary structure."""
    expected = {
        "identity":      {},
        "preferences":   {},
        "relationships": {},
        "notes":         {}
    }
    result = _empty_memory()

    assert isinstance(result, dict)
    assert result == expected

    # Also verify that a fresh dictionary is created each time
    result2 = _empty_memory()
    assert result is not result2
