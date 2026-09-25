from agent.task_queue import TaskPriority, TaskQueue, TaskRequest, TaskStatus


class _FakeExecutor:
    def execute(self, goal, speak=None, player=None, cancel_flag=None):
        assert goal == "run me"
        assert cancel_flag is not None
        return "finished"


class _FailingExecutor:
    def execute(self, goal, speak=None, player=None, cancel_flag=None):
        raise RuntimeError("executor failed")


def test_run_task_completes_and_invokes_callback():
    completed = []
    queue = TaskQueue()
    task_id = queue.submit(
        TaskRequest(
            goal="run me",
            priority=TaskPriority.NORMAL,
            on_complete=lambda task_id, result: completed.append((task_id, result)),
        )
    )
    task = queue._tasks[task_id]
    task.status = TaskStatus.RUNNING
    queue._active_count = 1
    queue._get_executor = lambda: _FakeExecutor()

    queue._run_task(task)

    assert task.status == TaskStatus.COMPLETED
    assert task.result == "finished"
    assert task.error == ""
    assert completed == [(task_id, "finished")]
    assert queue._active_count == 0


def test_run_task_records_failure_and_releases_active_slot():
    queue = TaskQueue()
    task_id = queue.submit(TaskRequest(goal="run me", priority=TaskPriority.NORMAL))
    task = queue._tasks[task_id]
    task.status = TaskStatus.RUNNING
    queue._active_count = 1
    queue._get_executor = lambda: _FailingExecutor()

    queue._run_task(task)

    assert task.status == TaskStatus.FAILED
    assert task.error == "executor failed"
    assert task.result is None
    assert queue._active_count == 0


def test_run_task_honors_cancellation_and_skips_callback():
    completed = []
    queue = TaskQueue()
    task_id = queue.submit(
        TaskRequest(
            goal="run me",
            priority=TaskPriority.NORMAL,
            on_complete=lambda task_id, result: completed.append((task_id, result)),
        )
    )
    task = queue._tasks[task_id]
    task.status = TaskStatus.RUNNING
    task.cancel_flag.set()
    queue._active_count = 1
    queue._get_executor = lambda: _FakeExecutor()

    queue._run_task(task)

    assert task.status == TaskStatus.CANCELLED
    assert task.result is None
    assert task.error == ""
    assert completed == []
    assert queue._active_count == 0
