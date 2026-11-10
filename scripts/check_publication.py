"""Offline structural publication checks. PASS is not visual or factual approval."""
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r'(!?)\[([^\]\n]*)\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+"[^"]*")?\s*\)')


def targets(text):
    for image, label, target in LINK.findall(text):
        yield bool(image), label, target.strip('<>')
    for target in re.findall(r'(?:src|href)=[\"\']([^\"\']+)[\"\']', text):
        yield False, '', target


def check(root):
    root = root.resolve()
    errors = []
    pages = [root / 'README.md'] + sorted((root / 'experiments').rglob('*.md'))
    for page in pages:
        rel = page.relative_to(root).as_posix()
        if not page.is_file():
            errors.append(f'{rel}: missing page'); continue
        text = page.read_text(encoding='utf-8')
        if not re.search(r'^#\s+\S', text, re.M):
            errors.append(f'{rel}: missing primary heading')
        local = []
        for image, label, target in targets(text):
            if image and not label.strip():
                errors.append(f'{rel}: image requires descriptive alt text')
            url = urlsplit(target)
            if url.scheme or url.netloc or not url.path:
                continue
            dest = (root / unquote(url.path).lstrip('/') if url.path.startswith('/')
                    else page.parent / unquote(url.path)).resolve()
            if not dest.is_relative_to(root):
                errors.append(f'{rel}: target escapes repository: {target}')
            elif not dest.exists():
                errors.append(f'{rel}: missing local target: {target}')
            local.append(dest)
        # Top-level article pages must offer navigation to another local Markdown page.
        if page.parent.parent.name == 'experiments' and page.name != 'README.md':
            if not any(p != page and p.suffix == '.md' for p in local):
                errors.append(f'{rel}: missing article navigation')
    root_text = (root / 'README.md').read_text(encoding='utf-8') if (root / 'README.md').exists() else ''
    indexed = {(root / unquote(urlsplit(t).path)).resolve() for _, _, t in targets(root_text)
               if not urlsplit(t).scheme and urlsplit(t).path}
    for entry in sorted((root / 'experiments').glob('*/README.md')):
        if entry.resolve() not in indexed:
            errors.append(f'README.md: series missing from index: {entry.relative_to(root)}')
    return errors


if __name__ == '__main__':
    errors = check(ROOT)
    for error in errors:
        print('FAIL:', error)
    print('STRUCTURAL_CHECK=' + ('FAIL' if errors else 'PASS'))
    print('NOT_CHECKED: rendered layout, mobile readability, factual accuracy, external URLs, anchor fragments, reference-style Markdown links, published commit readback')
    sys.exit(bool(errors))
