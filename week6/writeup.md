# Week 6 Write-up

## Submission Details

Name: **张蔚原** \
SUNet ID: **S202588320** \
Citations: **Semgrep CLI output, local repository files**

This assignment took me about **2.5** hours to do.

## Brief Findings Overview
> Semgrep initially reported five blocking findings in `week6/`: one insecure wildcard CORS policy, one SQL construction issue using `sqlalchemy.text()`, and three dangerous debug endpoints built around `eval`, `subprocess.run(..., shell=True)`, and dynamic `urllib`. I kept the scan scoped to local code, fixed the root causes, re-ran the backend tests, and then re-ran Semgrep until the scan returned zero findings. I did not treat FastAPI or Pydantic deprecation warnings as security findings.

## Fix #1
a. File and line(s)
> `week6/backend/app/main.py:22-28`

b. Rule/category Semgrep flagged
> `python.fastapi.security.wildcard-cors.wildcard-cors`

c. Brief risk description
> Allowing any origin with credentials or broad methods/headers increases the chance that an unintended site can interact with the API from a browser context.

d. Your change
> I replaced `allow_origins=["*"]` with an explicit local allowlist and narrowed methods/headers to the ones the starter app actually uses. I made this change directly in the FastAPI app setup after reading the Semgrep finding and re-testing the app locally.

e. Why this mitigates the issue
> Restricting origins and methods cuts off accidental cross-origin access and matches the development surface actually needed by the app.

## Fix #2
a. File and line(s)
> `week6/backend/app/routers/notes.py:69-78`

b. Rule/category Semgrep flagged
> `python.sqlalchemy.security.audit.avoid-sqlalchemy-text.avoid-sqlalchemy-text`

c. Brief risk description
> The original endpoint interpolated `q` into raw SQL text. That bypasses SQLAlchemy's normal query construction protections and risks SQL injection if the parameter is attacker-controlled.

d. Your change
> I replaced the raw SQL string with a normal ORM `select(Note)` query that uses `contains()` filters, ordering, and `limit(50)`. This preserved the endpoint behavior while removing string-built SQL.

e. Why this mitigates the issue
> Using SQLAlchemy expressions instead of raw text keeps user input in bound parameters and restores the framework's intended safety properties.

## Fix #3
a. File and line(s)
> `week6/backend/app/routers/notes.py` debug endpoints removed after line 78

b. Rule/category Semgrep flagged
> `python.lang.security.audit.eval-detected.eval-detected`, `python.lang.security.audit.subprocess-shell-true.subprocess-shell-true`, and `python.lang.security.audit.dynamic-urllib-use-detected.dynamic-urllib-use-detected`

c. Brief risk description
> Those endpoints exposed highly dangerous primitives: arbitrary expression execution, shell command execution, and attacker-controlled URL fetching. They were not required for the product flow.

d. Your change
> I deleted the unsafe debug endpoints rather than trying to harden them. This was the smallest correct fix because the endpoints existed only for debugging and were not part of the real feature set.

e. Why this mitigates the issue
> Removing unused dangerous entry points is stronger than attempting partial sanitization, because it eliminates the attack surface entirely instead of trying to filter risky inputs.
