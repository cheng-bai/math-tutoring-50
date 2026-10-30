"""Validate public data, assets and obvious private-path leaks with Python 3."""
from pathlib import Path
from html.parser import HTMLParser
import re

root = Path(__file__).resolve().parents[1]
rows = (root / 'data/curriculum.tsv').read_text().splitlines()
assert len(rows) == 50
assert [int(row.split('\t')[0]) for row in rows] == list(range(1, 51))
for path in root.rglob('*'):
    if not path.is_file() or '.git' in path.parts:
        continue
    if path.suffix in ('.md', '.html', '.tsv', '.json'):
        text = path.read_text()
        assert not re.search(r'/Users/|\{\{PERSON_', text), str(path)
        if path.suffix == '.md':
            for link in re.findall(r'!\[[^\]]*\]\(([^)]+)\)', text):
                if not link.startswith(('http', 'data:')):
                    assert (path.parent / link).is_file(), (path, link)
print('PASS: 50 curriculum rows; public text scan; all Markdown images available.')
