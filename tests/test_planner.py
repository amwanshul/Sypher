import pytest
from agent.planner import _fallback_plan

def test_fallback_plan():
    goal = "sample goal"
    result = _fallback_plan(goal)

    assert isinstance(result, dict)
    assert "steps" in result
    assert isinstance(result["steps"], list)
    assert len(result["steps"]) == 1

    step = result["steps"][0]
    assert step.get("tool") == "web_search"
    assert step.get("parameters") == {"query": goal}

def test_fallback_plan_empty_string():
    goal = ""
    result = _fallback_plan(goal)

    assert isinstance(result, dict)
    assert "steps" in result
    assert isinstance(result["steps"], list)
    assert len(result["steps"]) == 1

    step = result["steps"][0]
    assert step.get("tool") == "web_search"
    assert step.get("parameters") == {"query": goal}
