import os

with open('.github/prompts/refresh-claude-code-deck.prompt.md', 'r') as f:
    text = f.read()

import re
text = re.sub(r'Read `AGENTS\.md` and\n<<<<<<< HEAD\n`AGENTS\.md` first — they hold.*?\n=======\n`CLAUDE\.md` first — they hold.*?\n>>>>>>> origin/main', r'Read `AGENTS.md` first — it holds the layout rules, colour constants, and diagram', text, flags=re.DOTALL)

text = re.sub(r'<<<<<<< HEAD\n\s*worktrees, AGENTS\.md loading, and auto memory.*?=======\n\s*worktrees, CLAUDE\.md loading, and auto memory.*?\n>>>>>>> origin/main', r'  worktrees, AGENTS.md loading, and auto memory. Primary source:', text, flags=re.DOTALL)

text = re.sub(r'<<<<<<< HEAD\nprinciple in `AGENTS\.md` that diagrams and text must not restate each other.\n=======\nprinciple in `CLAUDE\.md` that diagrams and text must not restate each other.\n>>>>>>> origin/main', r'principle in `AGENTS.md` that diagrams and text must not restate each other.', text, flags=re.DOTALL)

with open('.github/prompts/refresh-claude-code-deck.prompt.md', 'w') as f:
    f.write(text)
