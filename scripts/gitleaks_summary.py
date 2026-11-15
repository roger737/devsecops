import argparse
import json
from collections import Counter
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('report', type=Path)
    args = parser.parse_args()

    findings = json.loads(args.report.read_text(encoding='utf-8'))
    counts = Counter(item.get('RuleID', 'unknown') for item in findings)
    print(f'## Secret detection: {len(findings)} finding(s)\n')
    for rule_id, count in sorted(counts.items()):
        print(f'- `{rule_id}`: {count}')
    if findings:
        print('\n| Rule | File | Line | Secret |')
        print('| --- | --- | ---: | --- |')
        for item in findings[:20]:
            path = item.get('File', '').replace('|', '\\|')
            print(f"| {item.get('RuleID', 'unknown')} | `{path}` | {item.get('StartLine', '')} | REDACTED |")
        print('\nReports are redacted. Revoke and rotate any real credential; deleting its latest file is not sufficient.')


if __name__ == '__main__':
    main()
