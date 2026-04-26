import pytest
from agent.task_queue import TaskQueue

def test_cancel_nonexistent_task():
    queue = TaskQueue()
    result = queue.cancel("nonexistent-task-id")
    assert result is False
