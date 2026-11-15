import argparse
import re
from pathlib import Path
from zipfile import ZipFile

import yaml
from pptx import Presentation

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def word_count(path: Path) -> int:
    return len(re.findall(r"\b[\w’/-]+\b", path.read_text(encoding='utf-8')))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--require-live', action='store_true')
    args = parser.parse_args()

    required = [
        'Dockerfile', 'README.md', 'docs/risk-brief.md', 'docs/rollout-plan.md',
        'docs/reflection.md', 'docs/dockerfile-comparison.md', 'docs/demo-runbook.md',
        'docs/evidence.md', 'security/semgrep/rules.yml', 'security/exceptions.md',
        'presentation/devsecops-presentation.pptx', 'presentation/devsecops-presentation.pdf',
        'presentation/speaker-notes.md', '.github/workflows/security.yml',
        '.github/workflows/secret-history.yml', '.github/CODEOWNERS',
    ]
    for name in required:
        require((ROOT / name).is_file(), f'Missing {name}')

    workflow = yaml.safe_load((ROOT / '.github/workflows/security.yml').read_text(encoding='utf-8'))
    require(set(workflow['jobs']) == {'sast', 'secrets', 'dependencies', 'container', 'verify'}, 'Unexpected security jobs')
    require(set(workflow['jobs']['verify']['needs']) == {'sast', 'secrets', 'dependencies', 'container'}, 'Aggregate gate dependencies incomplete')
    workflow_text = (ROOT / '.github/workflows/security.yml').read_text(encoding='utf-8')
    for tool in ('semgrep', 'gitleaks', 'trivy', 'sbom-action'):
        require(tool in workflow_text.lower(), f'Missing {tool}')
    require(workflow_text.count("severity: HIGH,CRITICAL") == 2, 'Dependency and image severity gates required')
    require(workflow_text.count("exit-code: '1'") + workflow_text.count('--exit-code 1') >= 3, 'Blocking scanner exit codes required')
    require('--require-juice-shop-findings' in workflow_text, 'Real-finding assertion missing')
    require('curl --fail' in workflow_text, 'Container HTTP smoke test missing')
    require("test \"$runtime_user\" = '65532:0'" in workflow_text, 'Runtime-user assertion missing')
    for match in re.finditer(r'uses:\s*([^\s]+)@([^\s]+)', workflow_text):
        require(re.fullmatch(r'[0-9a-f]{40}', match.group(2)) is not None, f'Unpinned action {match.group(1)}')

    rules = yaml.safe_load((ROOT / 'security/semgrep/rules.yml').read_text(encoding='utf-8'))['rules']
    require(len(rules) >= 2, 'At least two custom rules required')
    for rule in rules:
        require(rule['severity'] == 'ERROR', f"{rule['id']} must be High/ERROR")
        require(rule['metadata']['severity'] == 'HIGH', f"{rule['id']} metadata severity missing")
    cors_tests = (ROOT / 'security/semgrep/tests/permissive-cors.ts').read_text(encoding='utf-8')
    query_tests = (ROOT / 'security/semgrep/tests/unsafe-template-query.ts').read_text(encoding='utf-8')
    require('ruleid: acme.javascript.express.permissive-cors' in cors_tests and 'ok: acme.javascript.express.permissive-cors' in cors_tests, 'CORS safe/unsafe tests missing')
    require('ruleid: acme.javascript.sequelize.unsafe-template-query' in query_tests and 'ok: acme.javascript.sequelize.unsafe-template-query' in query_tests, 'Query safe/unsafe tests missing')

    dockerfile = (ROOT / 'Dockerfile').read_text(encoding='utf-8')
    require(dockerfile.count('@sha256:') == 2, 'Both base images must be digest-pinned')
    require('USER 65532:0' in dockerfile, 'Numeric non-root runtime identity missing')
    require('gcr.io/distroless/' in dockerfile, 'Distroless runtime missing')

    risk = (ROOT / 'docs/risk-brief.md').read_text(encoding='utf-8')
    require(len(re.findall(r'^## \d\.', risk, re.MULTILINE)) == 5, 'Risk brief must contain five numbered risks')
    require(risk.count('**Attack scenario:**') == 5, 'Each risk needs an attack scenario')
    require(word_count(ROOT / 'docs/risk-brief.md') <= 650, 'Risk brief exceeds one-page budget')
    require(400 <= word_count(ROOT / 'docs/reflection.md') <= 1200, 'Reflection must fit 1–2 pages')
    rollout = (ROOT / 'docs/rollout-plan.md').read_text(encoding='utf-8')
    require(len(re.findall(r'^### Phase \d', rollout, re.MULTILINE)) >= 3, 'At least three rollout phases required')
    for phrase in ('What “critical service” means', 'When a developer pushes back', 'Metrics and operating review'):
        require(phrase in rollout, f'Rollout section missing: {phrase}')

    presentation_path = ROOT / 'presentation/devsecops-presentation.pptx'
    with ZipFile(presentation_path) as archive:
        require(archive.testzip() is None, 'Invalid PowerPoint package')
    presentation = Presentation(presentation_path)
    require(len(presentation.slides) == 21, 'Unexpected slide count')
    require(all(slide.has_notes_slide for slide in presentation.slides), 'Speaker notes missing')
    require((ROOT / 'presentation/devsecops-presentation.pdf').stat().st_size > 10_000, 'PDF output missing or empty')

    if args.require_live:
        evidence = (ROOT / 'docs/evidence.md').read_text(encoding='utf-8')
        require('Pending' not in evidence and 'pending' not in evidence, 'Live evidence still pending')
        require(evidence.count('https://github.com/') >= 5, 'At least five real GitHub evidence links required')
        codeowners = (ROOT / '.github/CODEOWNERS').read_text(encoding='utf-8')
        require('REPOSITORY_OWNER' not in codeowners, 'CODEOWNERS placeholder remains')
        require((ROOT / 'docs/evidence/branch-protection-verified.json').is_file(), 'Verified branch protection missing')

    print('Repository deliverables validated.')
    if not args.require_live:
        print('Local/static validation only; use --require-live after real GitHub evidence is recorded.')


if __name__ == '__main__':
    main()
