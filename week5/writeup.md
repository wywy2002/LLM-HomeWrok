# Week 5 Write-up

## Submission Details

Name: **张蔚原** \
SUNet ID: **S202588320** \
Citations: **Warp docs, local repository files, week5/docs/TASKS.md**

This assignment took me about **4.0** hours to do.

## Your Responses

### Automation A: Warp Drive saved prompts, rules, MCP servers

a. Design of each automation, including goals, inputs/outputs, steps
> Automation A is the playbook in `week5/docs/warp-drive-search-crud.md`. Its goal is to automate the common backend loop for note search, pagination, CRUD edits, and regression tests. Inputs are the selected task from `docs/TASKS.md` and an optional test path. Outputs are changed backend files, a pytest result, and an endpoint summary.

b. Before vs. after
> Before this automation, each iteration required manually restating the task, opening the same backend files, and deciding what to test. After packaging the flow as a Warp-oriented prompt, the work is repeatable and the verification step is built into the workflow.

c. Autonomy levels used for each completed task
> The intended autonomy level is repo-scoped code editing plus non-interactive test execution inside `week5/`. That is enough to implement and verify search/CRUD behavior while keeping changes bounded to the starter app. I supervised by re-running the shared backend suite after edits.

d. Multi-agent notes
> This automation is single-agent, so there were no concurrency concerns in its normal use.

e. How you used the automation
> I used it to implement notes search with pagination/sorting and full note CRUD. It mainly reduces the friction of repeated edit-test-summarize cycles on the same small FastAPI codebase.

### Automation B: Multi-agent workflows in Warp

a. Design of each automation, including goals, inputs/outputs, steps
> Automation B is the coordination guide in `week5/docs/warp-multi-agent-playbook.md`. It assigns note search/CRUD, action-item filters/bulk-complete, and frontend review to separate agents or Warp tabs. The outputs are isolated file changes and a final integration pass.

b. Before vs. after
> Before the playbook, concurrent work on the same repo would risk schema or payload drift. After writing it down, responsibilities are explicit enough that multiple tabs can work in parallel without guessing ownership.

c. Autonomy levels used for each completed task
> The autonomy level here is higher because each agent is allowed to edit code in its lane and run local tests. I would still keep commit, push, and PR creation manual, because coordination mistakes are more expensive than local code mistakes.

d. Multi-agent notes
> Roles: Agent 1 for notes routes, Agent 2 for action-item routes, Agent 3 for frontend checks. The main win is parallelism on independent files. The main risk is shared schema drift, so the playbook calls that out explicitly.

e. How you used the automation
> I used this structure while selecting week5 tasks to implement locally. Even in a single-session run, the role split helped keep the notes and action-item changes separate and easier to verify.

### Optional Automation C
a. Design of each automation, including goals, inputs/outputs, steps
> I did not add a third automation beyond the two required ones.

b. Before vs. after
> N/A

c. Autonomy levels used for each completed task
> N/A

d. Multi-agent notes
> N/A

e. How you used the automation
> N/A
