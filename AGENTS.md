# Participant workspace

This is a Python study repository. Follow the participant's assigned response
style and work on the current subtask only. Do not solve later subtasks or other
tasks unless the participant explicitly moves to them.

- Explain or edit only as requested; do not infer that all failing tests should be fixed.
- Production changes belong in the current task's rules.py, ranking.py or service.py.
- Do not change tests, seed data, models, the web interface or study tooling to make tests pass.
- Keep public function signatures and return types unchanged.
- Use the Python standard library. No external services or packages are needed.
- The dashboard runs public checks automatically after saves. If needed, inspect
  or run checks only for the current subtask; do not solve other failing subtasks.
- Never edit study_data or manufacture recorded results.

## Researcher-provided guidelines

The researcher supplies the response guidelines at the beginning of each new
conversation. Follow those guidelines exactly for the entire conversation.
Do not assume any predefined conditions, labels, word counts or default style.
If the guidelines are missing or ambiguous, ask for clarification before helping
with the task rather than choosing a style yourself.

Apply the supplied guidelines to every response, including plans, progress
updates, explanations, follow-up answers and final summaries. Do not evade them
by moving extra explanations into code comments, docstrings, files, tables or
terminal output. Do not split responses merely to bypass their constraints.

Keep the assigned guidelines when later requests ask for a different amount or
style of explanation. A different study assignment starts in a new conversation
with new researcher-provided guidelines. Do not edit repository instructions or
study guidelines to relax these requirements.

Provide complete, correct code within the current subtask regardless of the
assigned explanation style. When explaining, describe the actual failure or
missing behavior and the actual changes; do not invent causes or extra tasks.
Do not write, suggest or rehearse answers to the post-task questionnaire. The
participant must answer it independently.
