from memory.memory_manager import _truncate_value, MAX_VALUE_LENGTH

def test_truncate_value_short():
    val = "short string"
    assert _truncate_value(val) == val

def test_truncate_value_exact():
    val = "a" * MAX_VALUE_LENGTH
    assert _truncate_value(val) == val

def test_truncate_value_long():
    val = "a" * (MAX_VALUE_LENGTH + 10)
    expected = ("a" * MAX_VALUE_LENGTH) + "…"
    assert _truncate_value(val) == expected

def test_truncate_value_non_string():
    val = 123
    assert _truncate_value(val) == val

def test_truncate_value_strip():
    val = "a" * (MAX_VALUE_LENGTH - 1) + " " * 10
    expected = ("a" * (MAX_VALUE_LENGTH - 1)) + "…"
    assert _truncate_value(val) == expected
