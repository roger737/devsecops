import argparse
import json
from collections import Counter
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('report', type=Path)
    parser.add_argument('--require-juice-shop-findings', action='store_true')
    args = parser.parse_args()

    report = json.loads(args.report.read_text(encoding='utf-8'))
    results = report.get('results', [])
    counts = Counter(item['check_id'] for item in results)
    print(f'## Static analysis: {len(results)} High-severity finding(s)\n')
    for rule_id, count in sorted(counts.items()):
        print(f'- `{rule_id}`: {count}')
    if results:
        print('\n| Rule | File | Line |')
        print('| --- | --- | ---: |')
        for item in results[:20]:
            path = item['path'].replace('|', '\\|')
            print(f"| `{item['check_id']}` | `{path}` | {item['start']['line']} |")
        locations = ', '.join(f"{item['path']}:{item['start']['line']}" for item in results[:10])
        locations = locations.replace('%', '%25').replace('\r', '%0D').replace('\n', '%0A')
        print(f'::error title=High-severity static analysis::{len(results)} finding(s): {locations}')

    if args.require_juice_shop_findings:
        expected = {
            'acme.javascript.express.permissive-cors': 'juice-shop/server.ts',
            'acme.javascript.sequelize.unsafe-template-query': 'juice-shop/routes/login.ts',
        }
        actual = {(item['check_id'], item['path']) for item in results}
        missing = [f'{rule} in {path}' for (rule, path) in expected.items() if (rule, path) not in actual]
        if missing:
            raise SystemExit('Expected real Juice Shop detections missing: ' + '; '.join(missing))
        print('\nVerified both custom rules against their intended Juice Shop source locations.')


if __name__ == '__main__':
    main()
