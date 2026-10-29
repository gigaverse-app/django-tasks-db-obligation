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

This fork is also a canary for pytest-obligation: the Python dependency and the report and
publish actions deliberately track its `main` branch, including unreleased changes.

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
- [RealOrangeOne/django-tasks-db#66](https://github.com/RealOrangeOne/django-tasks-db/issues/66)
  (open): `db_worker --queue-name '*'` exits on a task whose queue is no longer configured, and the
  tasks behind it are not run.
- [RealOrangeOne/django-tasks-db#67](https://github.com/RealOrangeOne/django-tasks-db/issues/67)
  (open): a `task_started` receiver that raises records the task as FAILED with the receiver's
  error, and the task never runs.

## What the contract finds in django-tasks-db's master

<!-- pytest-obligation:start -->
<a href="https://github.com/gigaverse-app/pytest-obligation"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/sticky-banner-dark.svg"><img alt="pytest-obligation: what passed, what is missing, what to fix" src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/sticky-banner-light.svg" width="640"></picture></a>

### Obligation contract checks

Other pytest tests and workflow steps are not included in these counts.

<p><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/neutral-2-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/neutral-2-light.svg" width="18" height="36" alt="2 applications" align="middle"></picture><picture><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/space.svg" width="69" height="36" alt="" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/good-4-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/good-4-light.svg" width="18" height="36" alt="42 contract checks passed" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/good-2-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/good-2-light.svg" width="18" height="36" alt="" align="middle"></picture><picture><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/space.svg" width="57" height="36" alt="" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/divider-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/divider-light.svg" width="1" height="36" alt="" align="middle"></picture><picture><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/space.svg" width="12" height="36" alt="" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/bad-1-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/bad-1-light.svg" width="18" height="36" alt="18 contract failures" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/bad-8-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/bad-8-light.svg" width="18" height="36" alt="" align="middle"></picture><picture><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/space.svg" width="50" height="36" alt="" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/good-0-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/good-0-light.svg" width="18" height="36" alt="0 blocked checks" align="middle"></picture><picture><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/space.svg" width="75" height="36" alt="" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/warning-4-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/warning-4-light.svg" width="18" height="36" alt="4 coverage gaps" align="middle"></picture><picture><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/space.svg" width="72" height="36" alt="" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/good-0-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/good-0-light.svg" width="18" height="36" alt="0 rejected bindings" align="middle"></picture><picture><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/space.svg" width="73" height="36" alt="" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/neutral-0-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/neutral-0-light.svg" width="18" height="36" alt="0 skipped tests" align="middle"></picture><picture><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/space.svg" width="69" height="36" alt="" align="middle"></picture><br><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/captions-with-skips-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/captions-with-skips-light.svg" width="640" height="34" alt="applications · contract checks passed · contract failures · blocked checks · coverage gaps · rejected bindings · skipped tests" align="middle"></picture></p>

**Failures: 0 unexpected + 18 known expected.** Expected failures are declared by the application and do not fail CI. Review their reasons and evidence below; counts are checks, not distinct product bugs.

**Test step succeeded with known expected failures.**

<details>
<summary>Application inventory and skipped tests</summary>

**2** applications with results · **0** applications not run
Checks skipped: **0**.


Static declarations only; dynamically generated suites may be absent. No application code was imported.
Application name unresolved: tests.obligation.test&#95;worker&#95;contract.TestWorkerContract; showing its suite name.

</details>


<details>
<summary><strong>django-tasks-db: the wor&#8203;ker&#x27;s ready rows</strong><div align="right"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/good-3-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/good-3-light.svg" width="8" height="16" alt="39 passed" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/good-9-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/good-9-light.svg" width="8" height="16" alt="" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/label-passed-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/label-passed-light.svg" width="37" height="18" alt="" align="middle"></picture><picture><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/space.svg" width="29" height="18" alt="" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/divider-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/divider-light.svg" width="1" height="22" alt="" align="middle"></picture><picture><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/space.svg" width="12" height="18" alt="" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/bad-1-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/bad-1-light.svg" width="8" height="16" alt="13 failed" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/bad-3-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/bad-3-light.svg" width="8" height="16" alt="" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/label-failed-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/label-failed-light.svg" width="33" height="18" alt="" align="middle"></picture><picture><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/space.svg" width="32" height="18" alt="" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/good-0-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/good-0-light.svg" width="8" height="16" alt="0 blocked" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/label-blocked-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/label-blocked-light.svg" width="44" height="18" alt="" align="middle"></picture><picture><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/space.svg" width="36" height="18" alt="" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/warning-1-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/warning-1-light.svg" width="8" height="16" alt="1 gaps" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/label-gaps-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/label-gaps-light.svg" width="27" height="18" alt="" align="middle"></picture><picture><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/space.svg" width="39" height="18" alt="" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/good-0-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/good-0-light.svg" width="8" height="16" alt="0 rejected" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/label-rejected-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/label-rejected-light.svg" width="48" height="18" alt="" align="middle"></picture><picture><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/space.svg" width="34" height="18" alt="" align="middle"></picture></div></summary>

Contract contract setup: <code>tests/obligation/test&#95;worker&#95;rows.py:108</code>

Scope: **Scheduled selection and loop**. Covers the declared query and loop checks; does not establish full automatic recovery (profile A).

<details>
<summary><strong>🔴 Known defects · application-declared expected failures</strong></summary>

Application reason: A task whose worker died remains RUNNING forever. The real task body can complete it, but ready() never selects it at any recovery horizon and the backend schedules no reclaim.

Ticket not reported.

<details>
<summary>1 affected checks · execution evidence</summary>

- <code>assert&#95;selection&#95;is&#95;complete&#91;status:RUNNING&#93;</code>: Known expected failure
- **call:** SelectionIncomplete: django-tasks-db: the worker&#x27;s ready rows: the production selection skips a row with status=&#x27;RUNNING&#x27; (states {&#x27;status&#x27;: &#x27;RUNNING&#x27;}), and the production worker, delivered it, moved its states from {&#x27;status&#x27;: &#x27;RUNNING&#x27;} to {&#x27;status&#x27;: &#x27;SUCCESSFUL&#x27;}. Nothing recovers that work after a lost message, so the selection is missing an owed branch. Select the row, or, when it owes nothing, make the worker leave it alone; if the combination is unreachable or another recovery owns it, declare it in excluded&#95;states with the reason

</details>

Application reason: The database permits this exact status edge, but ready() skips it forever. A delivered worker attempts to reconstruct the task and records FAILED instead.

Ticket not reported.

<details>
<summary>4 affected checks · execution evidence</summary>

- <code>assert&#95;selection&#95;is&#95;complete&#91;status:&#64;blank&#93;</code>: Known expected failure
- **call:** SelectionIncomplete: django-tasks-db: the worker&#x27;s ready rows: the production selection skips a row with status=&#x27;&#x27; (states {&#x27;status&#x27;: &#x27;&#x27;}), and the production worker, delivered it, moved its states from {&#x27;status&#x27;: &#x27;&#x27;} to {&#x27;status&#x27;: &#x27;FAILED&#x27;}. Nothing recovers that work after a lost message, so the selection is missing an owed branch. Select the row, or, when it owes nothing, make the worker leave it alone; if the combination is unreachable or another recovery owns it, declare it in excluded&#95;states with the reason
- <code>assert&#95;selection&#95;is&#95;complete&#91;status:&#64;whitespace&#93;</code>: Known expected failure
- **call:** SelectionIncomplete: django-tasks-db: the worker&#x27;s ready rows: the production selection skips a row with status=&#x27; &#x27; (states {&#x27;status&#x27;: &#x27; &#x27;}), and the production worker, delivered it, moved its states from {&#x27;status&#x27;: &#x27; &#x27;} to {&#x27;status&#x27;: &#x27;FAILED&#x27;}. Nothing recovers that work after a lost message, so the selection is missing an owed branch. Select the row, or, when it owes nothing, make the worker leave it alone; if the combination is unreachable or another recovery owns it, declare it in excluded&#95;states with the reason
- <code>assert&#95;selection&#95;is&#95;complete&#91;status:&#64;max&#95;length&#93;</code>: Known expected failure
- **call:** SelectionIncomplete: django-tasks-db: the worker&#x27;s ready rows: the production selection skips a row with status=&#x27;xxxxxxxxxx&#x27; (states {&#x27;status&#x27;: &#x27;xxxxxxxxxx&#x27;}), and the production worker, delivered it, moved its states from {&#x27;status&#x27;: &#x27;xxxxxxxxxx&#x27;} to {&#x27;status&#x27;: &#x27;FAILED&#x27;}. Nothing recovers that work after a lost message, so the selection is missing an owed branch. Select the row, or, when it owes nothing, make the worker leave it alone; if the combination is unreachable or another recovery owns it, declare it in excluded&#95;states with the reason
- <code>assert&#95;selection&#95;is&#95;complete&#91;status:&#64;unknown&#95;choice&#93;</code>: Known expected failure
- **call:** SelectionIncomplete: django-tasks-db: the worker&#x27;s ready rows: the production selection skips a row with status=&#x27;not-a-memb&#x27; (states {&#x27;status&#x27;: &#x27;not-a-memb&#x27;}), and the production worker, delivered it, moved its states from {&#x27;status&#x27;: &#x27;not-a-memb&#x27;} to {&#x27;status&#x27;: &#x27;FAILED&#x27;}. Nothing recovers that work after a lost message, so the selection is missing an owed branch. Select the row, or, when it owes nothing, make the worker leave it alone; if the combination is unreachable or another recovery owns it, declare it in excluded&#95;states with the reason

</details>

Application reason: Worker.run&#95;task catches the receiver failure and makes the task FAILED. The healthy tail completes, but ready() never selects the failed task again and no automatic retry restores it.

Ticket not reported.

<details>
<summary>1 affected checks · execution evidence</summary>

- <code>assert&#95;one&#95;poisoned&#95;identity&#95;does&#95;not&#95;stall&#95;the&#95;tick</code>: Known expected failure
- **call:** PoisonDropped: django-tasks-db: the worker&#x27;s ready rows: the poisoned identity is no longer owed after the tick. Isolation must leave a failing identity selectable (or held with backoff), not drop, settle or retire it

</details>

Application reason: The worker catches the injected cooperative stop as BaseException, makes the interrupted task FAILED, and continues to the healthy tail. This checks exception handling, not its OS signal handler.

Ticket not reported.

<details>
<summary>1 affected checks · execution evidence</summary>

- <code>assert&#95;a&#95;soft&#95;time&#95;limit&#95;ends&#95;the&#95;tick</code>: Known expected failure
- **call:** StopRequestDropped: django-tasks-db: the worker&#x27;s ready rows: the identity whose step hit the soft time limit is no longer owed after the tick (it raised None). An interrupted step must leave its identity for the next run

</details>

Application reason: The all-queues worker claims a row with an empty queue name before InvalidTask escapes. The row leaves ready() without this light contract proving a terminal state or retry budget.

Ticket not reported.

<details>
<summary>1 affected checks · execution evidence</summary>

- <code>assert&#95;database&#95;legal&#95;owed&#95;row&#95;is&#95;handled&#91;task-queue&#95;name-blank&#93;</code>: Known expected failure
- **call:** OwedRowNotHandled: django-tasks-db: the worker&#x27;s ready rows: the production worker and its handoffs raised InvalidTask(&quot;Queue &#x27;&#x27; is not valid for backend.&quot;) on a database-legal owed row with queue&#95;name-blank (&#x27;&#x27;) after moving it out of the selection, and nothing ends it there: the row is in no terminal state (this contract declares none) and the contract claims no profile J to bound a repeat. Either what moved it expires (a claim, a lease, a backoff) and recovery hands the same row to the same raise, or no selection looks at it again and it stays unfinished. Exclude the row in the selection, end it in a terminal state instead of raising, or bound the retry with profile J

</details>

Application reason: A whitespace-only queue name is database-legal and selected by the all-queues worker. InvalidTask escapes after the claim; leaving ready() proves neither completion nor bounded failure.

Ticket not reported.

<details>
<summary>1 affected checks · execution evidence</summary>

- <code>assert&#95;database&#95;legal&#95;owed&#95;row&#95;is&#95;handled&#91;task-queue&#95;name-whitespace&#93;</code>: Known expected failure
- **call:** OwedRowNotHandled: django-tasks-db: the worker&#x27;s ready rows: the production worker and its handoffs raised InvalidTask(&quot;Queue &#x27; &#x27; is not valid for backend.&quot;) on a database-legal owed row with queue&#95;name-whitespace (&#x27; &#x27;) after moving it out of the selection, and nothing ends it there: the row is in no terminal state (this contract declares none) and the contract claims no profile J to bound a repeat. Either what moved it expires (a claim, a lease, a backoff) and recovery hands the same row to the same raise, or no selection looks at it again and it stays unfinished. Exclude the row in the selection, end it in a terminal state instead of raising, or bound the retry with profile J

</details>

Application reason: An unconfigured queue name raises InvalidTask after the worker claims the row. Leaving ready() does not prove the obligation was handled or that a bounded retry ends it.

Ticket not reported.

<details>
<summary>1 affected checks · execution evidence</summary>

- <code>assert&#95;database&#95;legal&#95;owed&#95;row&#95;is&#95;handled&#91;task-queue&#95;name-max&#95;length&#93;</code>: Known expected failure
- **call:** OwedRowNotHandled: django-tasks-db: the worker&#x27;s ready rows: the production worker and its handoffs raised InvalidTask(&quot;Queue &#x27;xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&#x27; is not valid for backend.&quot;) on a database-legal owed row with queue&#95;name-max&#95;length (&#x27;xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&#x27;) after moving it out of the selection, and nothing ends it there: the row is in no terminal state (this contract declares none) and the contract claims no profile J to bound a repeat. Either what moved it expires (a claim, a lease, a backoff) and recovery hands the same row to the same raise, or no selection looks at it again and it stays unfinished. Exclude the row in the selection, end it in a terminal state inste…

</details>

Application reason: The all-queues worker selects an empty queue name. Its error handler reconstructs the invalid task and raises InvalidTask, abandoning the healthy task behind it: https://github.com/RealOrangeOne/django-tasks-db/issues/66

Ticket not reported.

<details>
<summary>1 affected checks · execution evidence</summary>

- <code>assert&#95;inadmissible&#95;owed&#95;row&#95;does&#95;not&#95;block&#95;the&#95;next&#91;task-queue&#95;name-blank&#93;</code>: Known expected failure
- **call:** OwedRowNotHandled: django-tasks-db: the worker&#x27;s ready rows: a database-legal owed row with queue&#95;name-blank (&#x27;&#x27;) first in selection order stopped the tick before the valid row behind it (the tick raised InvalidTask(&quot;Queue &#x27;&#x27; is not valid for backend.&quot;)). Selection is oldest-first, so that row leads every tick and blocks every later row of its kind

</details>

Application reason: The all-queues worker claims a whitespace queue name, then InvalidTask from error reporting aborts the tick before the healthy task behind it: https://github.com/RealOrangeOne/django-tasks-db/issues/66

Ticket not reported.

<details>
<summary>1 affected checks · execution evidence</summary>

- <code>assert&#95;inadmissible&#95;owed&#95;row&#95;does&#95;not&#95;block&#95;the&#95;next&#91;task-queue&#95;name-whitespace&#93;</code>: Known expected failure
- **call:** OwedRowNotHandled: django-tasks-db: the worker&#x27;s ready rows: a database-legal owed row with queue&#95;name-whitespace (&#x27; &#x27;) first in selection order stopped the tick before the valid row behind it (the tick raised InvalidTask(&quot;Queue &#x27; &#x27; is not valid for backend.&quot;)). Selection is oldest-first, so that row leads every tick and blocks every later row of its kind

</details>

Application reason: A database-legal but unconfigured 32-character queue name is selected by the all-queues worker. Error reporting raises InvalidTask and aborts before the healthy tail: https://github.com/RealOrangeOne/django-tasks-db/issues/66

Ticket not reported.

<details>
<summary>1 affected checks · execution evidence</summary>

- <code>assert&#95;inadmissible&#95;owed&#95;row&#95;does&#95;not&#95;block&#95;the&#95;next&#91;task-queue&#95;name-max&#95;length&#93;</code>: Known expected failure
- **call:** OwedRowNotHandled: django-tasks-db: the worker&#x27;s ready rows: a database-legal owed row with queue&#95;name-max&#95;length (&#x27;xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&#x27;) first in selection order stopped the tick before the valid row behind it (the tick raised InvalidTask(&quot;Queue &#x27;xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&#x27; is not valid for backend.&quot;)). Selection is oldest-first, so that row leads every tick and blocks every later row of its kind

</details>

These are application declarations. An expected failure can come from a declared gap or an unmet proof precondition; inspect its execution and diagnostics before treating it as a reproduced product defect.

</details>

<details>
<summary><strong>⚪ Deliberate exclusions</strong></summary>

- **Scheduled selection and loop (selection) / schedule evidence** · Not claimed by application. Application reason: db&#95;worker is a continuously polling process; this batch invocation uses its same query and loop.

These are scope decisions, not demonstrated defects. Review their reasons when the application changes.

</details>

---

<details>
<summary><strong>Hypothesis · Not reported</strong></summary>

This report has no generated exploration evidence.

</details>

---

<details>
<summary><strong>⚪ 0 supported guarantees</strong></summary>


Suite (application code): <code>tests.obligation.test&#95;worker&#95;rows.TestDatabaseWorkerRows</code>

</details>

</details>

<details>
<summary><strong>django-tasks-db: the wor&#8203;ker running a task</strong><div align="right"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/good-3-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/good-3-light.svg" width="8" height="16" alt="3 passed" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/label-passed-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/label-passed-light.svg" width="37" height="18" alt="" align="middle"></picture><picture><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/space.svg" width="37" height="18" alt="" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/divider-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/divider-light.svg" width="1" height="22" alt="" align="middle"></picture><picture><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/space.svg" width="12" height="18" alt="" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/bad-5-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/bad-5-light.svg" width="8" height="16" alt="5 failed" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/label-failed-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/label-failed-light.svg" width="33" height="18" alt="" align="middle"></picture><picture><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/space.svg" width="40" height="18" alt="" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/good-0-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/good-0-light.svg" width="8" height="16" alt="0 blocked" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/label-blocked-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/label-blocked-light.svg" width="44" height="18" alt="" align="middle"></picture><picture><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/space.svg" width="36" height="18" alt="" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/warning-3-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/warning-3-light.svg" width="8" height="16" alt="3 gaps" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/label-gaps-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/label-gaps-light.svg" width="27" height="18" alt="" align="middle"></picture><picture><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/space.svg" width="39" height="18" alt="" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/good-0-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/good-0-light.svg" width="8" height="16" alt="0 rejected" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/label-rejected-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/label-rejected-light.svg" width="48" height="18" alt="" align="middle"></picture><picture><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/space.svg" width="34" height="18" alt="" align="middle"></picture></div></summary>

Contract contract setup: <code>tests/obligation/test&#95;worker&#95;contract.py:85</code>

<details>
<summary><strong>🔴 Known defects · application-declared expected failures</strong></summary>

Application reason: the worker selects only READY tasks, so a task left RUNNING by a worker that died is never run again (django-tasks-db#5)

Ticket not reported.

<details>
<summary>2 affected checks · execution evidence</summary>

- <code>A-known&#95;gap</code>: Known expected failure
- **call:** Failed: the worker selects only READY tasks, so a task left RUNNING by a worker that died is never run again (django-tasks-db#5)
- <code>extra-a task whose worker died is run again by what django-tasks-db runs</code>: Known expected failure
- **call:** AssertionError: a stranded row (&#x27;0b240281-9784-435d-9552-df623205acf1&#x27;) was not re-dispatched by the recovery tick: nothing in production re-selects its state, so a dead owner strands it permanently<br>assert &#x27;0b240281-9784-435d-9552-df623205acf1&#x27; in &#91;&#93;

</details>

Application reason: a claim holds no lease and no heartbeat: nothing can tell a live worker&#x27;s task from a dead one&#x27;s

Ticket not reported.

<details>
<summary>1 affected checks · execution evidence</summary>

- <code>B-known&#95;gap</code>: Known expected failure
- **call:** Failed: a claim holds no lease and no heartbeat: nothing can tell a live worker&#x27;s task from a dead one&#x27;s

</details>

Application reason: a task is marked RUNNING before its effect and SUCCESSFUL after it, with nothing in between: after a death the row cannot tell whether the effect happened

Ticket not reported.

<details>
<summary>1 affected checks · execution evidence</summary>

- <code>C-known&#95;gap</code>: Known expected failure
- **call:** Failed: a task is marked RUNNING before its effect and SUCCESSFUL after it, with nothing in between: after a death the row cannot tell whether the effect happened

</details>

Application reason: a worker that dies after claiming the task, or after its external call, leaves it RUNNING forever (https://github.com/RealOrangeOne/django-tasks-db/issues/5); and a task&#95;started receiver that raises marks the task FAILED before it runs, and nothing retries it (https://github.com/RealOrangeOne/django-tasks-db/issues/67). WORKER&#95;FINDINGS pins each history

Ticket not reported.

<details>
<summary>1 affected checks · execution evidence</summary>

- <code>handoff-the worker runs a task-assert&#95;crash&#95;at&#95;every&#95;commit&#95;converges</code>: Known expected failure
- **call:** HistoriesDiverged: django-tasks-db: handoff &#x27;the worker runs a task&#x27;: normal operation reaches TaskOutcome(status=&#x27;SUCCESSFUL&#x27;, effect=1), but these histories reach something else: {&#x27;worker died after commit 1&#x27;: TaskOutcome(status=&#x27;RUNNING&#x27;, effect=0), &#x27;worker died after external call 1&#x27;: TaskOutcome(status=&#x27;RUNNING&#x27;, effect=1), &#x27;signal receiver 1 failed&#x27;: TaskOutcome(status=&#x27;FAILED&#x27;, effect=0)}. Work was lost or repeated. A loss is work handed off only by a message, a commit hook or code after a commit that a dead worker never runs: commit the handoff with the state that owes it, or make that state selectable by recovery. A repeat is recovery redoing an external call whose effect already ex…

</details>

These are application declarations. An expected failure can come from a declared gap or an unmet proof precondition; inspect its execution and diagnostics before treating it as a reproduced product defect.

</details>

<details>
<summary><strong>🔴 Known gaps declared by the application</strong></summary>

- **Unfinished work gets recovered (A)** · Known gap declared. Application reason: the worker selects only READY tasks, so a task left RUNNING by a worker that died is never run again (django-tasks-db#5)
- **Worker ownership is bounded (B)** · Known gap declared. Application reason: a claim holds no lease and no heartbeat: nothing can tell a live worker&#x27;s task from a dead one&#x27;s
- **Uncertain outcomes are handled (C)** · Known gap declared. Application reason: a task is marked RUNNING before its effect and SUCCESSFUL after it, with nothing in between: after a death the row cannot tell whether the effect happened

</details>

<details>
<summary><strong>⚪ Deliberate exclusions</strong></summary>

- **Results eventually settle correctly (E)** · Not applicable (application decision). Application reason: one worker settles each task; no two results race to write it
- **Owed work is discovered from stored facts (F)** · Not applicable (application decision). Application reason: the obligation is the task row itself, not a fact derived from product state
- **Execution respects its gate (G)** · Not claimed by application. Application reason: django-tasks-db&#x27;s worker contract has no application readiness predicate; dependencies and product gates need their own ExecutionGate binding, including release with its notification lost.
- **Repeating work is harmless (H)** · Not applicable (application decision). Application reason: django-tasks-db never replays a task
- **Intent and work are saved together (I)** · Not claimed by application. Application reason: django-tasks-db&#x27;s worker receives already admitted work; it cannot make an application&#x27;s product transaction atomic with enqueue. Bind Profile I on the application&#x27;s command contract.
- **Retries have a limit (J)** · Not applicable (application decision). Application reason: Django&#x27;s task framework runs a task once: it is never retried

These are scope decisions, not demonstrated defects. Review their reasons when the application changes.

</details>

---

<details>
<summary><strong>Hypothesis · No generated scenario bindings collected</strong></summary>

No optional schedule-exploration cases were collected for this suite. Other Hypothesis use inside application callbacks is not assessed here.

</details>

---

<details>
<summary><strong>🟢 1 supported guarantees</strong></summary>

- **Needed records are retained**

Suite (application code): <code>tests.obligation.test&#95;worker&#95;contract.TestWorkerContract</code>

</details>

</details>

---

<details>
<summary><strong>What do these numbers mean?</strong></summary>

- **Failures:** an executed assertion failed unexpectedly or was an application-declared expected failure. Expected failures still permit successful CI; the visible breakdown distinguishes them.
- **Rejected bindings:** repair the connection to production code; these checks provide no supporting evidence.
- **Blocked checks:** checks could not establish a result, including missing execution, setup/cleanup errors, binding-debt or unclassified expected failures, and unexpected passes requiring declaration review.
- **Coverage gaps:** guarantees not assessed, missing scenarios, or with declared gaps. Each affected guarantee counts once. Deliberate exclusions are shown separately.

Pass/fail/blocked/rejected counts partition unique checks. Gaps count guarantees, not extra tests. Declined and not-applicable declarations remain separate and do not establish passing coverage. Graphics color contract results: passing checks and zero issues are green, failures and rejected bindings are red, blocked checks and gaps are amber. Missing reports never show green zeroes. The workflow status above is separate from these contract counts.

Elapsed time covers the pytest session. Summed check time includes setup, execution and cleanup; parallel work overlaps.
Application totals include discovered declarations and reported suites. Skipped checks count known deselections and explicit pytest skips; incomplete selected checks are not skips. Uncollected applications have unknown check counts. Zero recorded outcomes do not certify passing coverage.

Application names, quoted reasons and diagnostic values come from application code. Guarantee labels come from pytest-obligation. Results cover collected suites only; passing checks do not rate every test's quality.

Test step (reported): **success**
Source: <code>nightly run of tests/obligation against django-tasks-db&#x27;s current master</code>

</details>

[Report guide](https://github.com/gigaverse-app/pytest-obligation/blob/main/package/docs/github-action-report.md)
<!-- pytest-obligation:end -->
