from collections import Counter

try:
    from django.tasks import task
except ImportError:
    from django_tasks import task  # type: ignore[no-redef]


class Outbox:
    """A system outside the database that a task reaches: it records each message instead of sending it."""

    def __init__(self) -> None:
        self.sent: Counter[str] = Counter()

    def send(self, message: str) -> None:
        self.sent[message] += 1


outbox = Outbox()


@task()
def send_message(message: str) -> None:
    outbox.send(message)
