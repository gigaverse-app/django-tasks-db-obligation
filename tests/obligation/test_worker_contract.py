"""
django-tasks-db's contract with its worker, proven by pytest-obligation.

A task enqueued with the database backend is a row, committed or rolled back
with the transaction that enqueued it. The worker, ``manage.py db_worker``,
claims a READY row, marks it RUNNING, runs the task and records how it ended.
The obligation this contract states: a task that ran is recorded as it ended,
and a task that has not run is run.

``worker_contract`` from pytest-obligation's django-tasks integration generates
the proofs, bound here to ``tests.obligation.tasks.send_message``, whose effect
is a message sent outside the database. Retention is claimed and proven against
``prune_db_task_results``. What the worker lacks is declared as known gaps, each
a strict xfail that a fix flips to a failure. The worker's crash histories kill
it right after each commit and right after the task's external call, and fail
each ``task_started`` and ``task_finished`` receiver in turn; ``WORKER_FINDINGS``
pins what every one of those histories leaves, in the same run.
"""

from pytest_obligation import CallableDelivery, Findings, due_work_contract_suite
from pytest_obligation.crash_histories import ExternalCall
from pytest_obligation.integrations.django_tasks import (
    TaskOutcome,
    db_worker_once,
    worker_contract,
)

from .tasks import Outbox, outbox, send_message

MESSAGE = "your order has shipped"

# REAL PRODUCTION: one `manage.py db_worker --batch` pass, as a deployment runs the worker.
WORKER = CallableDelivery(name="django-tasks-db", recover=db_worker_once())


def a_message_owed() -> str:
    # ARRANGE: a task that sends one message, enqueued and ready for a worker.
    outbox.sent.clear()
    return str(send_message.enqueue(MESSAGE).id)


def messages_sent(_task_id: str) -> int:
    # OBSERVE: how many times the message left for the outside system.
    return outbox.sent[MESSAGE]


def _task(status: str, sent: int) -> TaskOutcome:
    return TaskOutcome(status=status, effect=sent)


# What each history leaves after the worker runs again, pinned in the same run as the
# verdict; a history not listed must reach normal operation. A change in the worker
# moves an entry, and the case names the one that moved. The receivers failed are the
# task framework's own logging receivers, standing in for any receiver that raises
# (a bug, an unreachable metrics backend).
WORKER_FINDINGS: dict[str, TaskOutcome] = {
    # FINDING (#5): the claim committed, the worker died, and the task stays RUNNING forever.
    "worker died after commit 1": _task("RUNNING", 0),
    # Benign: set_successful committed the outcome before the death (commit 3 is the next, empty, poll).
    "worker died after commit 2": _task("SUCCESSFUL", 1),
    "worker died after commit 3": _task("SUCCESSFUL", 1),
    # FINDING (#5): the message was sent and the task stays RUNNING forever.
    "worker died after external call 1": _task("RUNNING", 1),
    # FINDING: task_started's receiver raised, so the task is FAILED without running, and nothing retries it.
    "signal receiver 1 failed": _task("FAILED", 0),
}

WORKER_HISTORY_GAP = (
    "a worker that dies after claiming the task, or after its external call, leaves it RUNNING forever "
    "(https://github.com/RealOrangeOne/django-tasks-db/issues/5); and a task_started receiver that raises "
    "marks the task FAILED before it runs, and nothing retries it. WORKER_FINDINGS pins each history"
)

_CONTRACT = worker_contract(
    name="django-tasks-db: the worker running a task",
    enqueue=a_message_owed,
    effect=messages_sent,
    expected=_task("SUCCESSFUL", 1),
    # EXTERNAL SEAM: the outbox the task sends its message through.
    external_calls=(ExternalCall(owner=Outbox, attribute="send"),),
    delivery=WORKER,
    findings=Findings(_task("SUCCESSFUL", 1), WORKER_FINDINGS),
)
CONTRACT = _CONTRACT.model_copy(
    update={"handoff_gaps": dict.fromkeys(_CONTRACT.handoff_gaps, WORKER_HISTORY_GAP)}
)


# The class is empty on purpose: the decorator reads CONTRACT and generates its tests,
# bound to the real `db_worker`, `prune_db_task_results` and the send_message task.
@due_work_contract_suite(CONTRACT)
class TestWorkerContract:
    """Every case in this class is generated from CONTRACT."""
