import os
import re

with open('media/generate_diagrams.py', 'r') as f:
    text = f.read()

# Just keep HEAD which has AGENTS.md
text = re.sub(r'<<<<<<< HEAD\n(.*?)\n=======\n.*?\n>>>>>>> origin/main', r'\1', text, flags=re.DOTALL)

with open('media/generate_diagrams.py', 'w') as f:
    f.write(text)
