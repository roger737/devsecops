import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from scripts.gitleaks_summary import main as gitleaks_summary
from scripts.redact_gitleaks import main as redact_gitleaks
from scripts.semgrep_summary import main as semgrep_summary


class SecurityScriptTests(unittest.TestCase):
    def test_gitleaks_report_is_redacted_before_summary(self):
        finding = {
            'RuleID': 'example-rule',
            'File': 'example.txt',
            'StartLine': 3,
            'Secret': 'synthetic-value',
            'Match': 'KEY=synthetic-value',
            'Line': 'KEY=synthetic-value',
            'Author': 'Test Author',
            'Email': 'author@example.invalid',
        }
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / 'gitleaks.json'
            report.write_text(json.dumps([finding]), encoding='utf-8')
            with patch('sys.argv', ['redact_gitleaks.py', str(report)]):
                redact_gitleaks()
            redacted = json.loads(report.read_text(encoding='utf-8'))[0]
            self.assertEqual(redacted['Secret'], 'REDACTED')
            self.assertEqual(redacted['Match'], 'REDACTED')
            self.assertEqual(redacted['Line'], 'REDACTED')
            self.assertNotIn('Author', redacted)
            self.assertNotIn('Email', redacted)
            output = io.StringIO()
            with patch('sys.argv', ['gitleaks_summary.py', str(report)]), redirect_stdout(output):
                gitleaks_summary()
            self.assertNotIn('synthetic-value', output.getvalue())
            self.assertIn('example-rule', output.getvalue())

    def test_semgrep_summary_accepts_expected_real_findings(self):
        results = [
            {'check_id': 'acme.javascript.express.permissive-cors', 'path': 'juice-shop/server.ts', 'start': {'line': 185}},
            {'check_id': 'acme.javascript.sequelize.unsafe-template-query', 'path': 'juice-shop/routes/login.ts', 'start': {'line': 34}},
        ]
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / 'semgrep.json'
            report.write_text(json.dumps({'results': results}), encoding='utf-8')
            output = io.StringIO()
            with patch('sys.argv', ['semgrep_summary.py', str(report), '--require-juice-shop-findings']), redirect_stdout(output):
                semgrep_summary()
            self.assertIn('Verified both custom rules', output.getvalue())

    def test_semgrep_summary_rejects_missing_real_findings(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / 'semgrep.json'
            report.write_text('{"results": []}', encoding='utf-8')
            with patch('sys.argv', ['semgrep_summary.py', str(report), '--require-juice-shop-findings']), redirect_stdout(io.StringIO()):
                with self.assertRaises(SystemExit):
                    semgrep_summary()

    def test_suppression_expiry_is_enforced(self):
        import datetime as dt
        from scripts.check_exception_expiry import check_file

        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'example.ts'
            source.write_text('// nosemgrep: example.rule -- SEC-123; owner @owner; expires 2026-12-31\n', encoding='utf-8')
            self.assertEqual(check_file(source, dt.date(2026, 11, 15)), 1)
            with self.assertRaisesRegex(ValueError, 'expired'):
                check_file(source, dt.date(2027, 1, 1))
            source.write_text('// nosemgrep: example.rule\n', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'requires'):
                check_file(source, dt.date(2026, 11, 15))

    def test_trivy_summary_counts_and_redacts_layout(self):
        from scripts.trivy_summary import main as trivy_summary

        report_data = {
            'Results': [{
                'Vulnerabilities': [{
                    'VulnerabilityID': 'CVE-0000-0001',
                    'Severity': 'CRITICAL',
                    'PkgName': 'synthetic-package',
                    'InstalledVersion': '1.0.0',
                    'FixedVersion': '1.0.1',
                }],
            }],
        }
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / 'trivy.json'
            report.write_text(json.dumps(report_data), encoding='utf-8')
            output = io.StringIO()
            with patch('sys.argv', ['trivy_summary.py', str(report), '--label', 'Synthetic scan']), redirect_stdout(output):
                trivy_summary()
            self.assertIn('1 High/Critical finding', output.getvalue())
            self.assertIn('CVE-0000-0001', output.getvalue())
            self.assertIn('synthetic-package', output.getvalue())


if __name__ == '__main__':
    unittest.main()
