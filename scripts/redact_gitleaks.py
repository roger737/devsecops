import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('report', type=Path)
    args = parser.parse_args()
    if not args.report.exists():
        print(f'No Gitleaks report found at {args.report}.')
        return

    findings = json.loads(args.report.read_text(encoding='utf-8'))
    for finding in findings:
        for field in ('Secret', 'Match', 'Line'):
            if field in finding:
                finding[field] = 'REDACTED'
        finding.pop('Author', None)
        finding.pop('Email', None)
    temporary = args.report.with_suffix(args.report.suffix + '.tmp')
    temporary.write_text(json.dumps(findings, indent=2) + '\n', encoding='utf-8')
    temporary.replace(args.report)
    print(f'Redacted sensitive and author fields in {len(findings)} finding(s).')


if __name__ == '__main__':
    main()
