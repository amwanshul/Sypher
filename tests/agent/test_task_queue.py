import pytest
from agent.task_queue import TaskQueue, TaskPriority, TaskRequest, TaskStatus


def test_submit_adds_task():
    queue = TaskQueue()
    task_id = queue.submit(TaskRequest(goal="test goal", priority=TaskPriority.NORMAL))

    assert task_id is not None
    assert isinstance(task_id, str)

    assert task_id in queue._tasks
    task = queue._tasks[task_id]
    assert task.goal == "test goal"
    assert task.priority == TaskPriority.NORMAL.value
    assert task.status == TaskStatus.PENDING

    assert len(queue._queue) == 1


def test_submit_sorts_by_priority():
    queue = TaskQueue()

    # Lower priority value means higher priority execution (1=HIGH, 2=NORMAL, 3=LOW)
    # They should be sorted ascending by priority value, then by creation time
    id_low = queue.submit(TaskRequest(goal="low priority", priority=TaskPriority.LOW))
    id_normal = queue.submit(TaskRequest(goal="normal priority", priority=TaskPriority.NORMAL))
    id_high = queue.submit(TaskRequest(goal="high priority", priority=TaskPriority.HIGH))

    assert len(queue._queue) == 3

    assert queue._queue[0].task_id == id_high
    assert queue._queue[0].priority == TaskPriority.HIGH.value

    assert queue._queue[1].task_id == id_normal
    assert queue._queue[1].priority == TaskPriority.NORMAL.value

    assert queue._queue[2].task_id == id_low
    assert queue._queue[2].priority == TaskPriority.LOW.value


def test_get_status_returns_snapshot_and_none_for_unknown_task():
    queue = TaskQueue()
    task_id = queue.submit(TaskRequest(goal="inspect me", priority=TaskPriority.HIGH))

    status = queue.get_status(task_id)

    assert status == {
        "task_id": task_id,
        "goal": "inspect me",
        "status": TaskStatus.PENDING.value,
        "result": None,
        "error": "",
    }
    assert queue.get_status("missing") is None
