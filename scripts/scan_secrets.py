#!/usr/bin/env python3
# Scan repository for common secret patterns. Prints findings and exits with code 1 if any found.
import re
from pathlib import Path
import sys

ROOT = Path('.').resolve()
IGNORE_DIRS = {'.git','.venv','node_modules','.next','frontend/node_modules','backend/__pycache__'}
PATTERNS = [
    re.compile(r'GOOGLE_API_KEY', re.I),
    re.compile(r'API_KEY', re.I),
    re.compile(r'SECRET_KEY', re.I),
    re.compile(r'AWS_ACCESS_KEY_ID', re.I),
    re.compile(r'AKIA[A-Z0-9]{16}'),
    re.compile(r'-----BEGIN PRIVATE KEY-----'),
]

found = []
for p in ROOT.rglob('*'):
    if any(part in IGNORE_DIRS for part in p.parts):
        continue
    if p.is_file():
        try:
            text = p.read_text(encoding='utf-8')
        except Exception:
            continue
        for pat in PATTERNS:
            for m in pat.finditer(text):
                # capture a little context
                start = max(m.start() - 30, 0)
                end = min(m.end() + 30, len(text))
                context = text[start:end].replace('\n','\\n')
                found.append((str(p.relative_to(ROOT)), pat.pattern, m.group(0), context))

if found:
    print('Potential secrets found:')
    for f,patt,match,ctx in found:
        print(f"- {f}: pattern={patt} match={match} context={ctx}")
    sys.exit(1)
else:
    print('No obvious secrets found.')
    sys.exit(0)
