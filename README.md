# HASE Lab

A fictional app for HASE course activities, with three independent Python tasks:
Workshop Planner, Peer Review Board and Study Buddy Finder.

## Open the app

1. Download the repository and open its folder in VS Code.
2. Choose **Terminal > Run Task... > Open HASE Lab**.
3. The browser opens automatically at a free local address. Leave the app running.
   If it does not open, click the address printed in the VS Code terminal.

Python 3.10+ is required. There are no packages to install. On macOS/Linux the
launcher uses `python3`; on Windows it uses `py`. Ask us if setup fails.
For setup troubleshooting only, Copilot can start `python3 serve.py --open`
(or `py serve.py --open` on Windows). The app selects a free port automatically, including when another instance is
running. It binds only to your own computer (`127.0.0.1`) and does not require
Wi-Fi or internet. Copilot itself still requires internet access.

## Participant sheets

Read the introduction together when instructed, then follow the task order we give you.

- [Introduction](output/pdf/HASE_Lab_Introduction.pdf)
- [Your role: Alex Morgan](output/pdf/HASE_Lab_Scenario.pdf)
- [Workshop Planner](output/pdf/HASE_Task_Workshops.pdf)
- [Peer Review Board](output/pdf/HASE_Task_Reviews.pdf)
- [Study Buddy Finder](output/pdf/HASE_Task_Buddies.pdf)

Each task has its own models, demo data and implementation under `hase_lab/`.
Only edit its `rules.py`, `ranking.py` and `service.py`. Each task's three
subtasks are sequential; completing one task is not required for another.

## Work with Copilot

Use a **new chat in the default Copilot panel for each task**, keep the default
model selection, and apply the response-style instruction we give you. Implement
one subtask at a time. Try to understand what was broken or missing and what
your changes do: you will explain this yourself in the form after each task.
Keep the assigned response style throughout the task chat. You may share the current subtask and relevant code or
errors; do not paste the whole sheet or ask Copilot to solve later subtasks.

**Save your changes.** The open web tab automatically checks saved Python files,
updates the preview and shows whether each subtask has passed. No manual test,
start, finish or submission commands are needed. The app checks for changes about
every two seconds while the tab is visible. Unsaved editor changes are not checked.

Only the selected task is checked. Results are cached until its source changes;
**Check again** retries without editing. The dashboard shows pass/fail summaries.
Accepted demo choices last until reset, reload or switching activities; they are not saved permanently.
The initial tasks are intentionally incomplete. Some checks already pass, but a
subtask only shows Passed when all four of its checks pass.

## After each task

When all three subtasks show Passed, or when we ask you to move on:

1. Stop editing and keep that task's Copilot conversation open.
2. Open the Command Palette: **Ctrl+Shift+P** (Windows/Linux) or **Cmd+Shift+P** (Mac).
3. Choose **Chat: Export Chat...** and save the JSON in the repository folder as
   `workshops_chat.json`, `reviews_chat.json` or `buddies_chat.json`.
4. Answer that task's questions in our form **without Copilot**.
5. Continue in your assigned order with a new chat.

[VS Code's chat export instructions](https://code.visualstudio.com/docs/agents/run/sessions/session-history#export-a-chat-session-as-a-json-file).

## Submit using the form

After all tasks, save all files and compress the repository folder into a ZIP.
Include your code changes, the three exported chat JSON files and `study_data/`.
Follow our form's instructions to send the files. Nothing is uploaded automatically.

The app saves automatic check results and passing source snapshots locally in
`study_data/`. It does not record keystrokes or capture your Copilot conversations.
Existing `study.py` commands remain available for researcher tooling and previous
pilots; they are not part of the participant workflow.
