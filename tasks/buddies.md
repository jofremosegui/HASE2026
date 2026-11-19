# Study Buddy Finder

Help a student find a suitable HASE study group and join it.

Use a new chat in the default Copilot panel and the response-style instruction we
gave you. Work on one subtask at a time; do not ask Copilot to solve the whole task.

## Scope

Under `hase_lab/buddies/`, change only `rules.py`, `ranking.py` and `service.py`.
Keep signatures and all other files unchanged. Inputs are valid: unique IDs,
nonnegative capacities and consistent records. Match text exactly, including case.

## 1. Show suitable options

A group is suitable only if its language is one the learner speaks, it has a free place, and the learner is not already a member. Return all suitable options without changing input data.
Order does not matter yet.

## 2. Order the options

First show groups matching the learner's goals. Within each preference group, show groups with more free places first. Resolve remaining ties by item ID in ascending order. Return a new list containing exactly the supplied candidates, without
filtering or changing the original list or records. Empty input gives an empty list.

## 3. Complete the action

A learner may hold at most two memberships; reaching two is allowed.
Reject unknown IDs, duplicates, unsuitable options and attempts beyond this limit.
Record the group in the learner's memberships and the learner in the group's members. Return True on success. Return False on rejection and leave all
data unchanged. Use the current state to determine suitability.

## Progress and completion

Save your changes and watch the Study Buddy Finder web tab. The preview and subtask
checks update automatically. No commands are needed. Demo choices last until reset, reload or switching activities.

When finished, export the chat as `buddies_chat.json` into the repository folder.
Answer this task's questions in our form without Copilot before continuing.
See the introduction PDF or README for the JSON export steps.
