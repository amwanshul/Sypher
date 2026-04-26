import pytest
from agent.task_queue import TaskQueue, TaskPriority, TaskStatus

def test_task_queue_submit_basic():
    queue = TaskQueue()
    task_id = queue.submit(goal="Test goal")

    assert task_id is not None
    assert isinstance(task_id, str)
    assert len(task_id) == 8

    # Assert task in _tasks
    assert task_id in queue._tasks
    task = queue._tasks[task_id]
    assert task.goal == "Test goal"
    assert task.priority == TaskPriority.NORMAL.value
    assert task.status == TaskStatus.PENDING

    # Assert task in _queue
    assert len(queue._queue) == 1
    assert queue._queue[0].task_id == task_id

def test_task_queue_submit_priority_sorting():
    queue = TaskQueue()

    id_low = queue.submit(goal="Low priority", priority=TaskPriority.LOW)
    id_normal = queue.submit(goal="Normal priority", priority=TaskPriority.NORMAL)
    id_high = queue.submit(goal="High priority", priority=TaskPriority.HIGH)

    assert len(queue._queue) == 3

    # Queue is sorted by priority (lowest value first: HIGH=1, NORMAL=2, LOW=3)
    assert queue._queue[0].task_id == id_high
    assert queue._queue[1].task_id == id_normal
    assert queue._queue[2].task_id == id_low

def test_task_queue_submit_same_priority_sorting(monkeypatch):
    import time
    queue = TaskQueue()

    # We want to ensure created_at is strictly increasing
    def mock_time():
        mock_time.t += 1
        return mock_time.t
    mock_time.t = 1000
    monkeypatch.setattr(time, "time", mock_time)

    id1 = queue.submit(goal="Task 1", priority=TaskPriority.NORMAL)
    id2 = queue.submit(goal="Task 2", priority=TaskPriority.NORMAL)
    id3 = queue.submit(goal="Task 3", priority=TaskPriority.NORMAL)

    assert len(queue._queue) == 3

    # Same priority should sort by created_at (FIFO)
    assert queue._queue[0].task_id == id1
    assert queue._queue[1].task_id == id2
    assert queue._queue[2].task_id == id3

def test_task_queue_submit_with_callbacks():
    queue = TaskQueue()

    def dummy_speak():
        pass

    def dummy_on_complete(tid, res):
        pass

    task_id = queue.submit(
        goal="Test callbacks",
        speak=dummy_speak,
        player="dummy_player",
        on_complete=dummy_on_complete
    )

    task = queue._tasks[task_id]
    assert task.speak == dummy_speak
    assert task.player == "dummy_player"
    assert task.on_complete == dummy_on_complete
