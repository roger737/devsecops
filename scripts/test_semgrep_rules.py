from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    fixtures = ROOT / 'security/semgrep/tests'
    work = ROOT / 'security-reports/rule-tests'
    work.mkdir(parents=True, exist_ok=True)
    for fixture in sorted(fixtures.glob('*.ts')):
        config = work / f'{fixture.stem}.yml'
        target = work / fixture.name
        shutil.copyfile(ROOT / 'security/semgrep/rules.yml', config)
        shutil.copyfile(fixture, target)
        result = subprocess.run(
            ['semgrep', 'scan', '--test', '--config', str(config), str(target)],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        print(result.stdout)
        if result.returncode:
            details = result.stdout[-6000:].replace('%', '%25').replace('\r', '%0D').replace('\n', '%0A')
            print(f'::error title=Custom rule tests failed::{details}')
            raise SystemExit(result.returncode)


if __name__ == '__main__':
    main()
