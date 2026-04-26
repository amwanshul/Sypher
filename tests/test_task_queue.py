from agent.task_queue import TaskQueue

def test_cancel_non_existent_task():
    queue = TaskQueue()
    result = queue.cancel("non_existent_id")
    assert result is False, "Canceling a non-existent task should return False"
