import pytest
from django.db import connection
from pytest_obligation import configure
from pytest_obligation.integrations.django import django_host
from pytest_obligation.integrations.django.receivers import django_receiver_breaker
from pytest_obligation.integrations.django.selection import DjangoSelectionInspector

from django_tasks_db.compat import task_finished, task_started

# The contract counts a worker's commits by asking PostgreSQL whether a statement
# wrote, so it runs only there.
if connection.vendor != "postgresql":
    raise pytest.UsageError(
        "the contract needs PostgreSQL: set DATABASE_URL=postgres://..."
    )

# The system under test is django-tasks-db, running tasks for Django's task
# framework: bindings must reach one of them. Crash histories fail each receiver
# of the signals db_worker sends in turn.
configure(
    django_host(
        production_packages={"django_tasks_db", "django_tasks", "django"},
        lifecycle_proofs=False,
        receiver_breaker=django_receiver_breaker(task_started, task_finished),
    ).model_copy(
        update={
            # PostgreSQL verifies the index's actual predicate; a name alone is not evidence.
            "selection_inspectors": (
                DjangoSelectionInspector(
                    partial_indexes=("tasks_db_new_ordering_idx",)
                ),
            ),
        }
    )
)
