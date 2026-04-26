import pytest
from agent.planner import _fallback_plan

def test_fallback_plan():
    goal = "find information about Python testing"
    expected_result = {
        "steps": [
            {
                "tool": "web_search",
                "parameters": {"query": goal},
                "description": "Information search"
            }
        ]
    }

    result = _fallback_plan(goal)
    assert result == expected_result
