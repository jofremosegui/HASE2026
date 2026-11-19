# Peer Review Board

Help a student find HASE projects to peer-review and accept assignments.

Use a new chat in the default Copilot panel and the response-style instruction we
gave you. Work on one subtask at a time; do not ask Copilot to solve the whole task.

## Scope

Under `hase_lab/reviews/`, change only `rules.py`, `ranking.py` and `service.py`.
Keep signatures and all other files unchanged. Inputs are valid: unique IDs,
nonnegative capacities and consistent records. Match text exactly, including case.

## 1. Show suitable options

A project is suitable only if it belongs to a different team from the reviewer, has a free review slot, and is not already assigned to that reviewer. Return all suitable options without changing input data.
Order does not matter yet.

## 2. Order the options

First show projects with fewer assigned reviewers. At equal reviewer counts, show projects matching the reviewer's expertise first. Resolve remaining ties by item ID in ascending order. Return a new list containing exactly the supplied candidates, without
filtering or changing the original list or records. Empty input gives an empty list.

## 3. Complete the action

A reviewer may hold at most two assignments; reaching two is allowed.
Reject unknown IDs, duplicates, unsuitable options and attempts beyond this limit.
Record the project in the reviewer's assignments and the reviewer in the project's reviewers. Return True on success. Return False on rejection and leave all
data unchanged. Use the current state to determine suitability.

## Progress and completion

Save your changes and watch the Peer Review Board web tab. The preview and subtask
checks update automatically. No commands are needed. Demo choices last until reset, reload or switching activities.

When finished, export the chat as `reviews_chat.json` into the repository folder.
Answer this task's questions in our form without Copilot before continuing.
See the introduction PDF or README for the JSON export steps.
