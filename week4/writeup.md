# Week 4 Write-up

## Submission Details

Name: **张蔚原** \
SUNet ID: **S202588320** \
Citations: **Anthropic Claude Code best practices, Anthropic SubAgents overview, local repository files**

This assignment took me about **3.0** hours to do.

## Your Responses

### Automation #1
a. Design inspiration
> I used Anthropic's Claude Code best-practices article for two ideas: keep automations narrow and idempotent, and make verification a first-class step. I also used the SubAgents overview as the model for splitting testing and documentation responsibilities.

b. Design of each automation, including goals, inputs/outputs, steps
> Automation #1 is a repo-local guidance and verification workflow built from `week4/CLAUDE.md` and `.claude/commands/tests.md`. Its goal is to keep changes inside `week4/`, route the model to the correct entry points, and force a test or lint pass after edits. Inputs are a target file or optional pytest path; outputs are a short verification summary and the failing file if something breaks.

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> Run it in Claude Code by invoking `/tests` or by starting a chat inside `week4/` so `CLAUDE.md` loads automatically. Expected output is either a passing test/lint summary or a concise failure report. Rollback is simple because the automation only reads, runs checks, and reports; it does not apply destructive git commands.

d. Before vs. after
> Before this automation, the workflow was manual context rebuilding: re-open routers, remember where tests live, and decide on commands each time. After the automation, the repo layout and verification steps are explicit, so repeated edits cost less context and fewer missed checks.

e. How you used the automation to enhance the starter application
> I used it while stabilizing the week4 starter tests on Windows. The main improvement was reliability: the guidance file kept the work scoped to `week4/`, and the verification command made the database cleanup regression obvious immediately.

### Automation #2
a. Design inspiration
> The second automation was inspired by the docs-oriented examples in the best-practices write-up. I wanted a lightweight docs-sync workflow rather than a broad agent, because the repo is small and the main risk is API drift, not discovery.

b. Design of each automation, including goals, inputs/outputs, steps
> Automation #2 is `.claude/commands/docs-sync.md`. Its goal is to compare the notes and action-items routers against documentation and produce route deltas. Input is the current router code; output is an updated `docs/API.md` plan or a route-delta summary. The steps are: inspect routers, compare payload shapes, then summarize mismatches.

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> Run it with `/docs-sync`. The expected output is a short endpoint summary and a list of fields that need documentation updates. Safety is high because the command is scoped to `week4/` and does not touch unrelated files or shell state.

d. Before vs. after
> Before this automation, docs drift had to be caught manually after code changes. After adding it, the intended workflow is to treat documentation as a final diff pass instead of an afterthought.

e. How you used the automation to enhance the starter application
> I used this automation concept to justify keeping endpoint changes small and inspectable while I fixed the week4 test fixture. Even without a large feature addition, it improved the repo's developer workflow by making verification and docs parity explicit.

### Optional Automation #3
a. Design inspiration
> I did not build a third automation because the first two already covered the required workflow surfaces: code guidance and post-change verification/documentation.

b. Design of each automation, including goals, inputs/outputs, steps
> N/A

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> N/A

d. Before vs. after
> N/A

e. How you used the automation to enhance the starter application
> N/A
