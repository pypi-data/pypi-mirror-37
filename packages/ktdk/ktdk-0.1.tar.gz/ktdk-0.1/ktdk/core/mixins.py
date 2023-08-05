from ktdk.runtime.context import Context


class ContextMixin(object):
    @property
    def context(self) -> Context:
        return getattr(self, '_context', None)

    def inject_context(self, context):
        setattr(self, '_context', context)


class CheckersMixin:
    def check_that(self, task: 'Task', points_multiplier=0, after_tasks=False):
        """Adds the check task
        Args:
            after_tasks:
            points_multiplier: If this task fails, how much from the test points should be discarded
            task(Task): Task instance
        """
        from .tasks import TaskType
        setattr(task, '_type', TaskType.CHECKED)
        setattr(task, '_points_multiplier', points_multiplier)
        if after_tasks:
            self.add_after(task)
        else:
            self.add_task(task)

    def require_that(self, task: 'Task', points_multiplier=0, after_tasks=False):
        """Requires a subtask to pass
        Args:
            points_multiplier: If this task fails, how much from the test points should be discarded
            task(Task):
        """
        from .tasks import TaskType
        self.check_that(task, points_multiplier=points_multiplier, after_tasks=after_tasks)
        setattr(task, '_type', TaskType.REQUIRED)
