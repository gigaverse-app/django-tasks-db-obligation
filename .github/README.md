# django-tasks-db, checked by pytest-obligation

[![pytest-obligation](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/gigaverse-app/django-tasks-db-obligation/master/.github/obligation-badge.json)](#what-the-contract-finds-in-django-tasks-dbs-master)

This is [django-tasks-db](https://github.com/RealOrangeOne/django-tasks-db) with one addition: a
[pytest-obligation](https://github.com/gigaverse-app/pytest-obligation) contract for its worker,
in [`tests/obligation`](../tests/obligation). django-tasks-db's own README is
[`README.md`](../README.md); nothing outside `tests/obligation` and this fork's workflows is changed.

The contract enqueues a task that sends one message and runs it through the real
`manage.py db_worker`. It runs the worker once per thing that can go wrong: the worker dies right
after each of its commits or right after the message is sent, or a `task_started` or
`task_finished` receiver raises. Then it runs the worker again and compares what each run leaves
with a normal run: the task's status and how many messages were sent. A second contract hands
the worker's polling query every row the database allows (each status, blank and unconfigured
queue names, a task whose receiver fails, a task stopped mid-run) and checks that each is either
run or ends in a recorded state, without holding up the tasks behind it.
`prune_db_task_results` is checked to keep every task that has not run.

Every night the fork merges django-tasks-db's `master` and runs the contract against it, and the
report below is updated whenever what it finds changes. A change in what any history leaves
turns the run red; that is the signal to report it upstream, as a plain issue with a standalone
reproduction.

To run it locally (Python 3.11 or later, PostgreSQL):

```bash
pip install -e . --group dev --group postgres -r tests/obligation/requirements.txt
DATABASE_URL=postgres://postgres:postgres@localhost:5432/postgres python -m pytest tests/obligation
```

## Found by the contract

- [RealOrangeOne/django-tasks-db#62](https://github.com/RealOrangeOne/django-tasks-db/issues/62):
  a `task_finished` receiver that raised rewrote a task that had run as FAILED. Fixed on `master`
  by [#64](https://github.com/RealOrangeOne/django-tasks-db/pull/64); the contract's findings
  table records the fixed behaviour (the task stays SUCCESSFUL).
- [RealOrangeOne/django-tasks-db#5](https://github.com/RealOrangeOne/django-tasks-db/issues/5)
  (open, reported before this fork): a task whose worker died stays RUNNING forever.

## What the contract finds in django-tasks-db's master

<!-- pytest-obligation:start -->
<!-- pytest-obligation:end -->
