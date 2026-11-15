import argparse
from collections import Counter
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('report', type=Path)
    parser.add_argument('--label', default='Trivy')
    args = parser.parse_args()

    report = json.loads(args.report.read_text(encoding='utf-8'))
    findings = [
        vulnerability
        for result in report.get('Results') or []
        for vulnerability in result.get('Vulnerabilities') or []
    ]
    counts = Counter(item.get('Severity', 'UNKNOWN') for item in findings)
    print(f"## {args.label}: {len(findings)} High/Critical finding(s)\n")
    for severity, count in sorted(counts.items()):
        print(f'- `{severity}`: {count}')
    if not findings:
        return

    print('\n| ID | Severity | Package | Installed | Fixed |')
    print('| --- | --- | --- | --- | --- |')
    for item in findings[:50]:
        values = [
            item.get('VulnerabilityID', 'unknown'),
            item.get('Severity', 'UNKNOWN'),
            item.get('PkgName', 'unknown'),
            item.get('InstalledVersion', 'unknown'),
            item.get('FixedVersion', '') or 'No fixed version listed',
        ]
        print('| ' + ' | '.join(str(value).replace('|', '\\|') for value in values) + ' |')

    locations = ', '.join(
        f"{item.get('VulnerabilityID', 'unknown')} ({item.get('PkgName', 'unknown')})"
        for item in findings[:10]
    ).replace('%', '%25').replace('\r', '%0D').replace('\n', '%0A')
    print(f'::error title={args.label} findings::{len(findings)} High/Critical finding(s): {locations}')


if __name__ == '__main__':
    main()
