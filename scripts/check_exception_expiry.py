import argparse
import datetime as dt
import re
from pathlib import Path

PATTERN = re.compile(r'nosemgrep:\s*(?P<rule>[^\s]+).*?expires\s+(?P<expiry>\d{4}-\d{2}-\d{2})')


def check_file(path: Path, today: dt.date) -> int:
    text = path.read_text(encoding='utf-8')
    count = 0
    for line_number, line in enumerate(text.splitlines(), 1):
        if 'nosemgrep:' not in line:
            continue
        match = PATTERN.search(line)
        if not match or '--' not in line or not re.search(r'\b[A-Z]+-\d+\b', line) or not re.search(r'\bowner\s+@[\w-]+', line):
            raise ValueError(f'{path}:{line_number}: suppression requires rule, ticket, owner, and YYYY-MM-DD expiry')
        expiry = dt.date.fromisoformat(match.group('expiry'))
        if expiry < today:
            raise ValueError(f'{path}:{line_number}: {match.group("rule")} suppression expired {expiry}')
        count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('paths', nargs='+', type=Path)
    parser.add_argument('--today', type=dt.date.fromisoformat, default=dt.date.today())
    args = parser.parse_args()

    count = 0
    for source in args.paths:
        files = [source] if source.is_file() else [
            path for path in source.rglob('*')
            if path.is_file() and path.suffix in {'.js', '.jsx', '.ts', '.tsx'}
            and not any(part in {'.git', 'node_modules', 'dist', 'build'} for part in path.parts)
        ]
        for path in files:
            count += check_file(path, args.today)
    print(f'Validated {count} inline suppression(s); none are expired.')


if __name__ == '__main__':
    main()
