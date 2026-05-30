# Week 7 Write-up

## Submission Details

Name: **张蔚原** \
SUNet ID: **S202588320** \
Citations: **Local repository files, local pytest results, Graphite submission to be completed manually after push**

This assignment took me about **5.5** hours to do.

## Task 1: Add more endpoints and validations
a. Links to relevant commits/issues
> Local work only so far. After pushing, I would split this into a dedicated branch/PR named around `task-1-endpoints-validations`.

b. PR Description
> Expanded the notes API with stronger validation and more complete endpoint coverage. The main changes were request constraints in schemas plus `PUT` and `DELETE` support and more predictable list/search behavior. Testing was done with `pytest backend/tests -q`, which passed locally.

c. Graphite Diamond generated code review
> Pending manual Graphite Diamond run after you push the branch and open the PR. The local code is ready for that step, but I did not fabricate a review that was not actually generated.

## Task 2: Extend extraction logic
a. Links to relevant commits/issues
> Local work only so far. Recommended branch name: `task-2-extraction-logic`.

b. PR Description
> Extended extraction to recognize checkbox-style action items and `#hashtags`, then added `POST /notes/{id}/extract` so extraction can be run against saved notes with an optional persistence path for tags. Verified through backend tests.

c. Graphite Diamond generated code review
> Pending manual Graphite Diamond run after PR creation.

## Task 3: Try adding a new model and relationships
a. Links to relevant commits/issues
> Local work only so far. Recommended branch name: `task-3-tags-relationships`.

b. PR Description
> Added a `Tag` model with a many-to-many relation via `note_tags`, plus list/create/delete tag endpoints and attach/detach operations on notes. This satisfies the “new model and relationships” requirement while staying close to the existing note workflow.

c. Graphite Diamond generated code review
> Pending manual Graphite Diamond run after PR creation.

## Task 4: Improve tests for pagination and sorting
a. Links to relevant commits/issues
> Local work only so far. Recommended branch name: `task-4-pagination-sorting-tests`.

b. PR Description
> Added page-style search/list endpoints and expanded backend coverage for pagination, filtering, sorting, tag attachment, extraction, validation, and bulk completion behaviors. Local test command: `pytest backend/tests -q`.

c. Graphite Diamond generated code review
> Pending manual Graphite Diamond run after PR creation.

## Brief Reflection
a. The types of comments you typically made in your manual reviews
> In manual reviews I tend to focus first on correctness and API shape, then on validation gaps, test coverage, and whether new features fit the existing data model cleanly. For this assignment I also paid attention to Windows-specific test cleanup because that can silently break grading runs.

b. A comparison of your comments vs. Graphite's AI-generated comments for each PR
> At the moment I only have my own local review notes, not actual Graphite-generated comments, because the PR step still has to be done in your GitHub account. My expectation is that Graphite will be good at spotting validation gaps, missing edge-case tests, and inconsistent response patterns, while my own review is better at deciding whether the chosen feature boundary makes sense for the assignment.

c. When the AI reviews were better/worse than yours
> AI review is usually better at broad checklist coverage than at judging whether a feature is the right one to add. For example, it would likely catch missing 404 and 422 paths quickly, but it may not question whether tags belong on notes versus action items unless the prompt is very explicit. My manual review was stronger on that architectural judgment.

d. Your comfort level trusting AI reviews going forward and any heuristics for when to rely on them
> I am comfortable using AI review as a second pass, not as the primary sign-off. My heuristic is: rely on it more for repetitive surface checks like tests, validation, naming consistency, and obvious error handling; rely on manual review more for product scope, data model decisions, migration risk, and any change that touches persistence or public API contracts.
