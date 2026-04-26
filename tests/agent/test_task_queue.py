import pytest
from agent.task_queue import TaskQueue, TaskPriority, TaskStatus

def test_submit_adds_task():
    queue = TaskQueue()
    task_id = queue.submit(goal="test goal", priority=TaskPriority.NORMAL)

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
    id_low = queue.submit(goal="low priority", priority=TaskPriority.LOW)
    id_normal = queue.submit(goal="normal priority", priority=TaskPriority.NORMAL)
    id_high = queue.submit(goal="high priority", priority=TaskPriority.HIGH)

    assert len(queue._queue) == 3

    # Since queue._queue is a list that gets sorted by submit(), we can just check the IDs directly in order
    assert queue._queue[0].task_id == id_high
    assert queue._queue[0].priority == TaskPriority.HIGH.value

    # Normal priority second
    assert queue._queue[1].task_id == id_normal
    assert queue._queue[1].priority == TaskPriority.NORMAL.value

    # Low priority third
    assert queue._queue[2].task_id == id_low
    assert queue._queue[2].priority == TaskPriority.LOW.value
