import pytest

from agent.task_queue import TaskPriority, TaskQueue, TaskRequest, TaskStatus


def test_cancel_pending_task_marks_it_cancelled_and_excludes_it_from_dispatch():
    queue = TaskQueue()
    task_id = queue.submit(TaskRequest(goal="cancel me", priority=TaskPriority.NORMAL))

    assert queue.pending_count() == 1
    assert queue.cancel(task_id) is True

    status = queue.get_status(task_id)
    assert status is not None
    assert status["status"] == TaskStatus.CANCELLED.value
    assert queue.pending_count() == 0
    assert queue._next_task() is None
    assert queue.cancel(task_id) is False
