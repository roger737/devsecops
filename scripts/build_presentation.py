from pathlib import Path
from typing import Any

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt
from reportlab.lib.colors import HexColor as reportlab_hex_color
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


def HexColor(value: str):
    return reportlab_hex_color(f'#{value}')


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'presentation'
OUT.mkdir(exist_ok=True)

NAVY = '102A43'
TEAL = '007C83'
TEAL_LIGHT = 'DDF3F1'
ORANGE = 'D97706'
RED = 'B42318'
RED_LIGHT = 'FDECEA'
GREEN = '257A4E'
GREEN_LIGHT = 'E7F5EC'
INK = '243B53'
MUTED = '627D98'
LINE = 'D9E2EC'
PALE = 'F5F8FA'
WHITE = 'FFFFFF'

slides: list[dict[str, Any]] = [
    {
        'kind': 'title', 'section': 'ACME FINANCIAL SERVICES', 'duration': 1,
        'title': 'Security that ships\nwith the code',
        'subtitle': 'DevSecOps pipeline implementation',
        'tag': 'Security Consultant  /  45-minute interview presentation',
        'notes': 'Introduce the objective: reduce delivery risk for a fintech team without creating an unworkable delivery tax. State that the demonstration uses an intentionally vulnerable, unmodified Juice Shop commit and that real scan outcomes are reported honestly.'
    },
    {
        'kind': 'statement', 'section': 'EXECUTIVE OUTCOME', 'duration': 2,
        'title': 'The pipeline becomes a control point',
        'headline': 'Prevent new high-risk changes. Make existing exposure visible. Give teams a workable path to fix it.',
        'bullets': ['Four independent security gates with usable artifacts', 'One reviewed merge decision backed by branch protection', 'A 90-day rollout measured by risk reduction and delivery impact'],
        'notes': 'Frame the result in business terms. The solution is not four scanners; it is a repeatable decision about what may merge. Independent jobs preserve evidence when one gate fails. The aggregate check simplifies enforcement, and the rollout acknowledges that legacy findings need managed remediation rather than an immediate portfolio-wide shutdown.'
    },
    {
        'kind': 'table', 'section': 'DAY 1 RISK BRIEF', 'duration': 3,
        'title': 'Five risks, ordered by business consequence',
        'headers': ['Priority', 'Risk', 'Why it matters'], 'widths': [0.8, 3.4, 7.8],
        'rows': [
            ['Critical', 'Credentials in Git', 'Repository access can become cloud or customer-data access.'],
            ['Critical', 'Administrator cloud roles', 'One compromised role can affect the entire cloud account.'],
            ['High', 'Unreviewed main branch', 'One account can introduce a production backdoor or payment change.'],
            ['High', 'No vulnerability inventory', 'Known weaknesses persist; disclosure response lacks component visibility.'],
            ['High', 'Unprotected public services', 'Abuse and floods threaten revenue, data, and availability.'],
        ],
        'notes': 'Use one realistic attack sentence per item. Credentials are searched in current files and history and then reused. Administrator access turns a single compromise into account-wide confidentiality, integrity, and availability loss. Direct merges let one identity alter production. Missing scanning and inventory leave known flaws and slow response. Missing edge protection and unrestricted browser-origin policy expose public services to abuse. Refer the panel to the one-page brief for full scenarios.'
    },
    {
        'kind': 'flow', 'section': 'ATTACK PATHS', 'duration': 2,
        'title': 'Small control gaps combine into major incidents',
        'steps': ['Compromised developer', 'Direct main-branch change', 'Automatic deployment', 'Fraud or data loss'],
        'bullets': ['A second chain starts with a committed credential and ends with administrator-level cloud control.', 'A third starts with a known component flaw; no inventory delays identification across 40 services.'],
        'notes': 'Emphasize chained risk. A scanner alone does not remove stolen credentials or excessive cloud privilege. Review, least privilege, inventory, and edge controls interrupt different parts of these paths. This is why the first-fix order is based on blast radius and immediacy rather than scanner convenience.'
    },
    {
        'kind': 'timeline', 'section': 'PRIORITIZATION', 'duration': 2,
        'title': 'Contain immediate exposure first',
        'cards': [
            ['TODAY', 'Revoke exposed credentials; move replacements to managed storage. Remove administrator policies and preserve incident evidence.'],
            ['THIS WEEK', 'Protect main; add required review. Establish secret, code, dependency, image, and inventory controls in warning mode.'],
            ['NEXT', 'Enforce new findings, restrict browser origins, add managed edge protection, and track remediation and coverage.'],
        ],
        'notes': 'Explain why credentials and cloud privilege precede scanner rollout: they may already enable compromise. Branch protection then prevents unreviewed delivery. Scanning begins this week but transitions from warning to enforcement after teams validate it. Edge and browser-origin changes follow because they require deployment-specific knowledge.'
    },
    {
        'kind': 'bullets', 'section': 'SCOPE', 'duration': 1,
        'title': 'A pinned target; no modified Juice Shop source',
        'bullets': ['Juice Shop submodule: commit 266448aba68cd8ba5915f526a128da4fa7bc3f9f', 'GitHub Actions around the application, not application remediation', 'Local loopback and isolated CI only; no public deployment'],
        'right_title': 'Not claimed',
        'right': ['No real Acme cloud or firewall was configured', 'No scan proves complete application security', 'No genuine finding is hidden for a green demo'],
        'notes': 'Set boundaries early. A submodule gives reproducibility and clear ownership. This submission demonstrates delivery controls around the target. It does not claim to have changed Acme infrastructure or fixed the intentionally vulnerable application.'
    },
    {
        'kind': 'flow', 'section': 'PIPELINE ARCHITECTURE', 'duration': 2,
        'title': 'Parallel evidence; one merge decision',
        'steps': ['Push / pull request', 'Semgrep + Gitleaks\nTrivy + SBOM\nBuild + smoke + Trivy', 'Security gates / verify', 'Review + protected main'],
        'bullets': ['Least-privilege tokens; pinned actions, tools, and container images', 'JSON, SARIF, readable summaries, CycloneDX inventory, and smoke logs', 'Independent jobs ensure one failed scanner does not hide the other results'],
        'notes': 'Walk left to right. Static analysis, secret detection, dependency analysis, and the container job run independently. Each produces concise and machine-readable output. The verify job fails if any required job fails or is cancelled. Branch protection requires that check and a reviewer. Scheduled runs address new vulnerability disclosures and old Git history.'
    },
    {
        'kind': 'table', 'section': 'PREVENTION AND SUPPLY CHAIN', 'duration': 2,
        'title': 'Controls beyond scanning',
        'headers': ['Control', 'Implementation', 'Purpose'], 'widths': [2.5, 4.7, 4.8],
        'rows': [
            ['Review', 'One approval; code owners; stale reviews dismissed', 'Independent decision before merge'],
            ['Required check', 'Security gates / verify; up-to-date branch', 'High/Critical findings block merge'],
            ['History safety', 'No force push or deletion; conversations resolved', 'Preserve accountability and review context'],
            ['Pipeline hardening', 'Pinned actions/tools; minimal token permissions', 'Reduce CI supply-chain and token blast radius'],
        ],
        'notes': 'This is a preventive control, not just detection. A required reviewer and required aggregate check stop direct unreviewed merges. CODEOWNERS assigns accountability. Pinning and token permissions address the CI attack surface. Note that branch protection must be demonstrated through the actual repository API response, not just a script.'
    },
    {
        'kind': 'cards', 'section': 'LIVE DEMONSTRATION', 'duration': 1,
        'title': 'Three proofs, twelve minutes',
        'cards': [
            ['01  SOURCE', 'Custom rules catch SQL injection and unrestricted cross-origin middleware; High-severity gate blocks.'],
            ['02  SECRET', 'A synthetic credential is blocked, removed, and distinguished from rotation and history cleanup.'],
            ['03  IMAGE', 'Exact dependency inventory, hardened image build, non-root identity, HTTP response, and image scan.'],
        ],
        'notes': 'Orient the audience before changing screens. The live blocks use pre-recorded run evidence where necessary to avoid waiting on runners. The backup is the evidence ledger, downloaded artifacts, and screenshots. If infrastructure fails, disclose it and continue with evidence rather than disabling a gate.'
    },
    {
        'kind': 'code', 'section': 'DEMO 1 / STATIC ANALYSIS', 'duration': 4,
        'title': 'A real login SQL injection blocks the change',
        'code': "models.sequelize.query(\n  `SELECT * FROM Users\n   WHERE email = '${req.body.email || ''}' ...`,\n  { model: UserModel, plain: true })",
        'bullets': ['Custom rule: unsafe template literal in raw Sequelize query', 'Actual target: juice-shop/routes/login.ts', 'Safe tests use replacements or bind parameters', 'Second rule detects unrestricted cors() in server.ts'],
        'image': 'docs/evidence/sast.png',
        'notes': 'Follow demo-runbook Demo 1. Show the custom rule tests, then the actual login finding and CORS finding. Explain that interpolated request data can alter the query; replacements or bind parameters preserve the statement structure. Show the High-severity failure and aggregate result. CORS is a dangerous policy, not proof of universal account compromise. Use the evidence image if embedded; otherwise open the linked run.'
    },
    {
        'kind': 'flow', 'section': 'DEMO 2 / SECRET DETECTION', 'duration': 4,
        'title': 'Block the leak; do not confuse deletion with rotation',
        'steps': ['Add synthetic AWS-style value', 'Gitleaks current-tree gate fails', 'Remove demonstration file', 'Current-tree gate passes'],
        'bullets': ['Failed and later runs are linked in the evidence ledger', 'Reports redact values; no real credential is used', 'A real leak still requires revoke/rotate, containment, and history review'],
        'image': 'docs/evidence/secrets-blocked.png',
        'notes': 'Follow Demo 2 and use the recorded failed and later runs. Open the redacted report and pull-request result. Explain why the current-tree gate can pass after removal while the scheduled history audit remains necessary. For a real credential, removal is cosmetic: revoke it first, investigate use, replace it through managed secrets, and assess history.'
    },
    {
        'kind': 'cards', 'section': 'DEMO 3 / DEPENDENCIES AND IMAGE', 'duration': 4,
        'title': 'Inventory and runtime proof answer different questions',
        'cards': [
            ['DEPENDENCIES', 'CI resolves exact versions without package scripts. Trivy reports High/Critical results as observed.'],
            ['INVENTORY', 'Syft generates CycloneDX JSON. The software bill of materials is an artifact, not a vulnerability fix.'],
            ['CONTAINER', 'Build the pinned image; assert 65532:0; drop capabilities; require an HTTP response; scan OS and libraries.'],
        ],
        'image': 'docs/evidence/container.png',
        'notes': 'Follow Demo 3. Call out the missing upstream lockfile and the ephemeral lockfile solution. Open the CycloneDX artifact. Then show the exact image build, runtime-user assertion, HTTP smoke log, and Trivy result. Do not invent dependency or image vulnerabilities if current upstream versions have none; the real static-analysis findings already satisfy the real-vulnerability criterion.'
    },
    {
        'kind': 'statement', 'section': 'DECISION', 'duration': 2,
        'title': 'A red gate is a controlled business decision',
        'headline': 'The vulnerable target should not merge through a High-severity gate without explicit review.',
        'bullets': ['Fix the finding, prove it false, or request a time-bounded exception', 'Do not convert scanner errors into success', 'In a real rollout, baseline legacy issues and block new findings first'],
        'notes': 'Address the apparent paradox of a red main workflow. The demonstration intentionally retains real findings. Success is accurate detection and enforcement, not green cosmetics. In production, new findings block while legacy issues receive risk-based deadlines. An unavailable scanner is distinct from a vulnerability result and follows an explicit outage policy.'
    },
    {
        'kind': 'table', 'section': 'CONTAINER HARDENING', 'duration': 2,
        'title': 'Build on upstream strengths; add repeatability and proof',
        'headers': ['Area', 'Upstream baseline', 'This submission'], 'widths': [2.2, 4.2, 5.6],
        'rows': [
            ['Base images', 'Multi-stage distroless; mutable tags', 'Slim builder + distroless runtime, both digest-pinned'],
            ['Identity', 'Numeric non-root user', '65532:0 plus dropped capabilities and no privilege escalation'],
            ['Files', 'Application copied as runtime-owned', 'Root-owned code; limited group-writable runtime paths'],
            ['Assurance', 'Application SBOM', 'Independent SBOM, vulnerability gate, and HTTP smoke proof'],
        ],
        'notes': 'Be honest: upstream already uses distroless and non-root. The added value is pinning, a smaller builder, exact tool versions, reduced application-file ownership, runtime restrictions, and verified execution. Digest pinning adds maintenance. Distroless complicates debugging, so use CI logs and separate debug images.'
    },
    {
        'kind': 'bullets', 'section': 'FALSE POSITIVES AND EXCEPTIONS', 'duration': 2,
        'title': 'Narrow decisions with ownership and expiry',
        'bullets': ['Reproduce with actual data flow and deployment context', 'Add safe regression tests and the narrowest inline suppression', 'Code-owner review; never exclude a directory for one match'],
        'right_title': 'Genuine but accepted risk',
        'right': ['Business justification and compensating controls', 'Accountable owner + Engineering Manager/security approval', 'Critical: 30-day maximum; High: 90 days; expiry blocks again'],
        'notes': 'Differentiate false positives from accepted genuine risk. A false positive has technical evidence and a narrow suppression. A genuine issue needs remediation or an approved exception. Release pressure alone is not a technical justification. Expiry automatically restores the blocking decision. Escalation is visible, not an administrator quietly disabling a check.'
    },
    {
        'kind': 'bullets', 'section': 'ROLLOUT / SERVICE PRIORITY', 'duration': 2,
        'title': '“Critical” is an evidence-based classification',
        'bullets': ['Moves, approves, settles, or reconciles money', 'Handles customer identity, payment, authentication, or regulated data', 'Internet-facing with a path to those systems, or provides identity', 'Can modify production, networking, secrets, or audit controls'],
        'right_title': 'Availability test',
        'right': ['Outage stops customer transactions or regulatory reporting', 'No tested manual workaround for more than one hour', 'Uncertain classification defaults to critical until resolved'],
        'notes': 'This definition avoids a vague critical label. Use the service catalog and deployment evidence, not team preference. Any of the listed criteria qualifies a service. Record the business owner, data, exposure, privileges, dependencies, and recovery objective. Reassess after architecture changes.'
    },
    {
        'kind': 'table', 'section': 'ROLLOUT / 90 DAYS', 'duration': 2,
        'title': 'Warn, prove, enforce, then scale',
        'headers': ['Phase', 'Coverage', 'Controls and exit condition'], 'widths': [2.2, 2.0, 7.8],
        'rows': [
            ['Days 1–15', '5 critical', 'Secrets/review first; warning scans; owned baseline; reliable pilot evidence'],
            ['Days 16–45', '+15 services', 'Block new High/Critical findings; harden images and cloud roles; weekly scorecard'],
            ['Days 46–90', '+20 services', 'Five-day warning per team; all 40 covered; edge design and scheduled scans'],
            ['After day 90', 'Continuous', 'Dynamic tests, signed provenance, policy as code, quarterly rule review'],
        ],
        'notes': 'The counts sum to 40. Start with payment, authentication, customer data, public interfaces, and privileged deployment services. Warning mode has a deadline and owner. Enforce new findings while existing ones follow Critical seven-day and High 30-day targets, faster if exploited. Rollout pauses are narrow exceptions, not global scanner shutdowns.'
    },
    {
        'kind': 'cards', 'section': 'ADOPTION AND METRICS', 'duration': 2,
        'title': 'Measure risk reduction and delivery friction',
        'cards': [
            ['COVERAGE', '5 → 20 → 40 protected services'],
            ['EXPOSURE', 'Zero active leaked credentials'],
            ['REMEDIATION', 'Critical ≤ 7 days; High ≤ 30 days'],
            ['QUALITY', '≥ 90% confirmed findings; ≥ 95% scan reliability'],
            ['DELIVERY', 'Median and 95th-percentile added pull-request time'],
            ['EXCEPTIONS', 'Zero expired; bypasses and repeat exceptions reviewed'],
        ],
        'notes': 'Raw finding counts are not a success metric. Track protected coverage, live-secret elimination, remediation age, escaped findings, precision, reliability, delivery delay, and exception health. Developer pushback receives a two-day evidence review. Disagreement goes to the security lead and Engineering Manager; nobody self-approves. Repeated friction drives rule tuning or training.'
    },
    {
        'kind': 'table', 'section': 'TRADE-OFFS', 'duration': 2,
        'title': 'Deliberate choices and their costs',
        'headers': ['Decision', 'Benefit', 'Cost / limitation'], 'widths': [3.0, 4.2, 4.8],
        'rows': [
            ['Pinned submodule', 'Reproducible, unmodified target', 'Recursive clone and explicit updates'],
            ['Narrow Semgrep patterns', 'Explainable, testable detections', 'Not full data-flow analysis'],
            ['Digest-pinned distroless', 'Small, repeatable runtime', 'Updates and debugging require discipline'],
            ['Current-tree + history secrets', 'Actionable gate plus old-commit visibility', 'Two outcomes to explain; rotation still required'],
            ['Strict gates / phased rollout', 'Prevention without portfolio shock', 'Baseline and exception governance required'],
        ],
        'notes': 'Show that the design reasons about limitations. No tool is sufficient by itself. Narrow rules are easier to trust but can miss obfuscation. Pinning improves repeatability but needs updates. Strict enforcement in the demo is paired with a realistic adoption plan. A running container is not a vulnerability-free application.'
    },
    {
        'kind': 'bullets', 'section': 'WITH MORE TIME', 'duration': 2,
        'title': 'From delivery controls to verified production assurance',
        'bullets': ['Baseline-aware pull-request comparisons with full scheduled scans', 'Committed lockfiles and read-only container filesystem testing', 'Signed images, attestations, and deployment-time verification', 'Dynamic application tests in ephemeral environments'],
        'right_title': 'Client production work',
        'right': ['Managed secrets and least-privilege cloud roles', 'Managed web firewall, rate limits, and denial-of-service exercises', 'Service inventory integration and escaped-defect trend analysis'],
        'notes': 'Prioritize improvements that close current assurance gaps. Baseline-aware comparisons reduce legacy noise without hiding scheduled full-scan findings. Signing and deployment verification extend trust beyond the runner. Dynamic tests add runtime evidence. Real client work includes cloud privilege, managed secrets, and edge controls that could not be configured without the environment.'
    },
    {
        'kind': 'statement', 'section': 'CLOSE', 'duration': 1,
        'title': 'Reduce risk without losing delivery',
        'headline': 'Contain credentials and privilege. Prevent unreviewed high-risk merges. Scale through evidence, ownership, and measured adoption.',
        'bullets': ['Working controls with real, reproducible evidence', 'Honest limitations and explicit business decisions', 'A 90-day path for all 40 services'],
        'notes': 'Close on the three outcomes: immediate exposure containment, preventive delivery controls, and a measured adoption path. Point to the repository for the one-page brief, working pipeline, evidence, rollout, and reflection. Transition to Q&A after the 45-minute presentation.'
    },
]

assert len(slides) == 21
assert sum(slide['duration'] for slide in slides) == 45


def rgb(hex_value: str) -> RGBColor:
    return RGBColor.from_string(hex_value)


def add_text(slide, x, y, w, h, text, size=18, color=INK, bold=False, font='Aptos', align=PP_ALIGN.LEFT):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = shape.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = frame.margin_right = Inches(0.02)
    frame.margin_top = frame.margin_bottom = Inches(0.02)
    paragraph = frame.paragraphs[0]
    paragraph.text = text
    paragraph.alignment = align
    paragraph.font.name = font
    paragraph.font.size = Pt(size)
    paragraph.font.bold = bold
    paragraph.font.color.rgb = rgb(color)
    return shape


def add_box(slide, x, y, w, h, fill=PALE, line=LINE, radius=True):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb(fill)
    shape.line.color.rgb = rgb(line)
    return shape


def add_bullets(slide, items, x, y, w, h, size=17, color=INK):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = shape.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = Inches(0.04)
    for index, item in enumerate(items):
        paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        paragraph.text = f'•  {item}'
        paragraph.font.name = 'Aptos'
        paragraph.font.size = Pt(size)
        paragraph.font.color.rgb = rgb(color)
        paragraph.space_after = Pt(12)
        paragraph.line_spacing = 1.08
    return shape


def add_slide_chrome(slide, data, number):
    background = slide.background.fill
    background.solid()
    background.fore_color.rgb = rgb(WHITE)
    add_text(slide, 0.65, 0.28, 10.5, 0.25, data['section'], 10, TEAL, True)
    add_text(slide, 0.65, 0.65, 12.0, 0.65, data['title'], 28, NAVY, True)
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.65), Inches(7.13), Inches(12.0), Inches(0.012))
    line.fill.solid(); line.fill.fore_color.rgb = rgb(LINE); line.line.fill.background()
    add_text(slide, 0.65, 7.18, 6.5, 0.2, 'ACME  /  DEVSECOPS', 8, MUTED, True)
    add_text(slide, 10.8, 7.18, 1.85, 0.2, f"{data['duration']} MIN   ·   {number:02d}", 8, MUTED, True, align=PP_ALIGN.RIGHT)


def render_pptx() -> None:
    presentation = Presentation()
    presentation.slide_width = Inches(13.333333)
    presentation.slide_height = Inches(7.5)
    presentation.core_properties.title = 'Acme Financial Services — DevSecOps Pipeline Implementation'
    presentation.core_properties.author = 'Security Consultant'
    presentation.core_properties.subject = '45-minute interview presentation'

    for number, data in enumerate(slides, 1):
        slide = presentation.slides.add_slide(presentation.slide_layouts[6])
        if data['kind'] == 'title':
            slide.background.fill.solid(); slide.background.fill.fore_color.rgb = rgb(NAVY)
            accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.72), Inches(0.7), Inches(0.12), Inches(5.85))
            accent.fill.solid(); accent.fill.fore_color.rgb = rgb(TEAL); accent.line.fill.background()
            add_text(slide, 1.15, 0.82, 10.5, 0.3, data['section'], 12, '74D3CF', True)
            add_text(slide, 1.15, 1.55, 10.8, 1.8, data['title'], 40, WHITE, True)
            add_text(slide, 1.15, 3.65, 10.5, 0.55, data['subtitle'], 24, 'D9E2EC')
            add_text(slide, 1.15, 5.95, 10.5, 0.35, data['tag'], 13, '9FB3C8')
        else:
            add_slide_chrome(slide, data, number)
            kind = data['kind']
            if kind == 'statement':
                add_box(slide, 0.65, 1.55, 12.0, 1.35, TEAL_LIGHT, TEAL_LIGHT)
                add_text(slide, 0.95, 1.82, 11.4, 0.9, data['headline'], 22, NAVY, True)
                add_bullets(slide, data['bullets'], 0.9, 3.25, 11.4, 2.7, 18)
            elif kind == 'bullets':
                if data.get('right'):
                    add_bullets(slide, data['bullets'], 0.75, 1.6, 6.0, 4.9, 17)
                    add_box(slide, 7.05, 1.55, 5.55, 4.95, TEAL_LIGHT, TEAL_LIGHT)
                    add_text(slide, 7.4, 1.9, 4.85, 0.4, data['right_title'], 16, TEAL, True)
                    add_bullets(slide, data['right'], 7.35, 2.55, 4.75, 3.55, 16)
                else:
                    add_bullets(slide, data['bullets'], 0.8, 1.65, 11.7, 4.9, 19)
            elif kind == 'table':
                x, y, w, h = 0.65, 1.5, 12.0, 5.25
                table = slide.shapes.add_table(len(data['rows']) + 1, len(data['headers']), Inches(x), Inches(y), Inches(w), Inches(h)).table
                for index, width in enumerate(data['widths']):
                    table.columns[index].width = Inches(width)
                for col, header in enumerate(data['headers']):
                    cell = table.cell(0, col); cell.text = header
                    cell.fill.solid(); cell.fill.fore_color.rgb = rgb(NAVY)
                for row_index, row in enumerate(data['rows'], 1):
                    for col, value in enumerate(row):
                        cell = table.cell(row_index, col); cell.text = value
                        cell.fill.solid(); cell.fill.fore_color.rgb = rgb(WHITE if row_index % 2 else PALE)
                for row_index in range(len(data['rows']) + 1):
                    table.rows[row_index].height = Inches(0.58 if row_index == 0 else (4.67 / len(data['rows'])))
                    for cell in table.rows[row_index].cells:
                        cell.margin_left = cell.margin_right = Inches(0.12)
                        cell.margin_top = cell.margin_bottom = Inches(0.06)
                        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                        for paragraph in cell.text_frame.paragraphs:
                            paragraph.font.name = 'Aptos'
                            paragraph.font.size = Pt(12 if len(data['rows']) >= 5 else 13)
                            paragraph.font.bold = row_index == 0 or (cell == table.cell(row_index, 0))
                            paragraph.font.color.rgb = rgb(WHITE if row_index == 0 else (RED if cell.text == 'Critical' else INK))
            elif kind == 'flow':
                count = len(data['steps']); gap = 0.18; total = 12.0; box_w = (total - gap * (count - 1)) / count
                for index, step in enumerate(data['steps']):
                    x = 0.65 + index * (box_w + gap)
                    add_box(slide, x, 1.7, box_w, 1.55, TEAL_LIGHT if index < count - 1 else NAVY, TEAL_LIGHT if index < count - 1 else NAVY)
                    add_text(slide, x + 0.15, 1.96, box_w - 0.3, 1.0, step, 15, NAVY if index < count - 1 else WHITE, True, align=PP_ALIGN.CENTER)
                add_bullets(slide, data['bullets'], 0.85, 3.75, 11.4, 2.35, 17)
            elif kind in ('timeline', 'cards'):
                cards = data['cards']; columns = len(cards) if len(cards) <= 3 else 3
                rows = (len(cards) + columns - 1) // columns
                gap = 0.22; box_w = (12.0 - gap * (columns - 1)) / columns
                box_h = 2.15 if rows == 2 else 3.65
                for index, (heading, body) in enumerate(cards):
                    row, col = divmod(index, columns)
                    x = 0.65 + col * (box_w + gap); y = 1.55 + row * (box_h + 0.28)
                    add_box(slide, x, y, box_w, box_h, PALE, LINE)
                    add_text(slide, x + 0.25, y + 0.28, box_w - 0.5, 0.35, heading, 13, TEAL, True)
                    add_text(slide, x + 0.25, y + 0.92, box_w - 0.5, box_h - 1.12, body, 16 if rows == 1 else 15, INK)
            elif kind == 'code':
                add_box(slide, 0.65, 1.55, 6.5, 4.95, NAVY, NAVY)
                add_text(slide, 0.95, 1.95, 5.9, 3.9, data['code'], 15, 'E6F6F4', font='Consolas')
                add_bullets(slide, data['bullets'], 7.45, 1.7, 4.9, 4.55, 16)
            if data.get('image') and (ROOT / data['image']).exists():
                image_path = ROOT / data['image']
                slide.shapes.add_picture(str(image_path), Inches(8.25), Inches(4.85), width=Inches(3.95))
        notes = slide.notes_slide.notes_text_frame
        notes.text = f"Timing: {data['duration']} minute(s).\n\n{data['notes']}\n\nEvidence and fallback: docs/evidence.md and docs/demo-runbook.md."

    path = OUT / 'devsecops-presentation.pptx'
    presentation.save(path)


def wrap_pdf(text: str, font: str, size: float, width: float):
    lines = []
    for source_line in text.split('\n'):
        words = source_line.split()
        line = ''
        for word in words:
            candidate = f'{line} {word}'.strip()
            if line and stringWidth(candidate, font, size) > width:
                lines.append(line); line = word
            else:
                line = candidate
        lines.append(line)
    return lines


def pdf_text(pdf, text, x, y, width, size=16, color=INK, font='Helvetica', leading=None, max_lines=None):
    leading = leading or size * 1.25
    pdf.setFont(font, size); pdf.setFillColor(HexColor(color))
    lines = wrap_pdf(text, font, size, width)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        pdf.drawString(x, y, line); y -= leading
    return y


def pdf_bullets(pdf, items, x, y, width, size=15):
    for item in items:
        pdf.setFillColor(HexColor(TEAL)); pdf.circle(x + 4, y + 4, 2.5, fill=1, stroke=0)
        y = pdf_text(pdf, item, x + 16, y, width - 16, size) - 10
    return y


def render_pdf() -> None:
    path = OUT / 'devsecops-presentation.pdf'
    pdf = canvas.Canvas(str(path, ), pagesize=(960, 540), pageCompression=1)
    pdf.setTitle('Acme Financial Services — DevSecOps Pipeline Implementation')
    pdf.setAuthor('Security Consultant')
    for number, data in enumerate(slides, 1):
        if data['kind'] == 'title':
            pdf.setFillColor(HexColor(NAVY)); pdf.rect(0, 0, 960, 540, fill=1, stroke=0)
            pdf.setFillColor(HexColor(TEAL)); pdf.rect(54, 48, 8, 420, fill=1, stroke=0)
            pdf_text(pdf, data['section'], 84, 475, 760, 12, '74D3CF', 'Helvetica-Bold')
            pdf_text(pdf, data['title'], 84, 390, 760, 40, WHITE, 'Helvetica-Bold', 49)
            pdf_text(pdf, data['subtitle'], 84, 265, 760, 23, 'D9E2EC')
            pdf_text(pdf, data['tag'], 84, 92, 760, 12, '9FB3C8')
        else:
            pdf.setFillColor(HexColor(WHITE)); pdf.rect(0, 0, 960, 540, fill=1, stroke=0)
            pdf_text(pdf, data['section'], 47, 510, 750, 10, TEAL, 'Helvetica-Bold')
            pdf_text(pdf, data['title'], 47, 473, 865, 27, NAVY, 'Helvetica-Bold', 32, 2)
            pdf.setStrokeColor(HexColor(LINE)); pdf.line(47, 27, 913, 27)
            pdf_text(pdf, 'ACME  /  DEVSECOPS', 47, 14, 350, 8, MUTED, 'Helvetica-Bold')
            pdf.setFont('Helvetica-Bold', 8); pdf.setFillColor(HexColor(MUTED)); pdf.drawRightString(913, 14, f"{data['duration']} MIN  ·  {number:02d}")
            kind = data['kind']
            if kind == 'statement':
                pdf.setFillColor(HexColor(TEAL_LIGHT)); pdf.roundRect(47, 320, 866, 92, 8, fill=1, stroke=0)
                pdf_text(pdf, data['headline'], 68, 382, 824, 21, NAVY, 'Helvetica-Bold', 27)
                pdf_bullets(pdf, data['bullets'], 65, 275, 820, 17)
            elif kind == 'bullets':
                if data.get('right'):
                    pdf_bullets(pdf, data['bullets'], 55, 410, 450, 15)
                    pdf.setFillColor(HexColor(TEAL_LIGHT)); pdf.roundRect(508, 95, 405, 330, 8, fill=1, stroke=0)
                    pdf_text(pdf, data['right_title'], 530, 390, 360, 15, TEAL, 'Helvetica-Bold')
                    pdf_bullets(pdf, data['right'], 530, 350, 350, 14)
                else:
                    pdf_bullets(pdf, data['bullets'], 60, 410, 820, 18)
            elif kind == 'table':
                widths = [w * 72 for w in data['widths']]
                row_count = len(data['rows']); row_h = 53 if row_count >= 5 else 65
                top = 420
                x = 47
                for index, header in enumerate(data['headers']):
                    pdf.setFillColor(HexColor(NAVY)); pdf.rect(x, top, widths[index], 34, fill=1, stroke=0)
                    pdf_text(pdf, header, x + 8, top + 12, widths[index] - 16, 11, WHITE, 'Helvetica-Bold')
                    x += widths[index]
                for row_index, row in enumerate(data['rows']):
                    x = 47; y = top - (row_index + 1) * row_h
                    for col, value in enumerate(row):
                        pdf.setFillColor(HexColor(WHITE if row_index % 2 == 0 else PALE)); pdf.rect(x, y, widths[col], row_h, fill=1, stroke=0)
                        color = RED if value == 'Critical' else INK
                        pdf_text(pdf, value, x + 8, y + row_h - 18, widths[col] - 16, 10.5, color, 'Helvetica-Bold' if col == 0 else 'Helvetica', 13, 4)
                        x += widths[col]
            elif kind == 'flow':
                count = len(data['steps']); gap = 12; box_w = (866 - gap * (count - 1)) / count
                for index, step in enumerate(data['steps']):
                    x = 47 + index * (box_w + gap)
                    pdf.setFillColor(HexColor(TEAL_LIGHT if index < count - 1 else NAVY)); pdf.roundRect(x, 292, box_w, 110, 7, fill=1, stroke=0)
                    lines = wrap_pdf(step, 'Helvetica-Bold', 13, box_w - 20)
                    y = 355 + (len(lines) - 1) * 8
                    for line in lines:
                        pdf.setFont('Helvetica-Bold', 13); pdf.setFillColor(HexColor(NAVY if index < count - 1 else WHITE)); pdf.drawCentredString(x + box_w / 2, y, line); y -= 16
                pdf_bullets(pdf, data['bullets'], 62, 245, 810, 15)
            elif kind in ('timeline', 'cards'):
                cards = data['cards']; columns = len(cards) if len(cards) <= 3 else 3
                rows = (len(cards) + columns - 1) // columns; gap = 14
                box_w = (866 - gap * (columns - 1)) / columns; box_h = 132 if rows == 2 else 250
                for index, (heading, body) in enumerate(cards):
                    row, col = divmod(index, columns); x = 47 + col * (box_w + gap); y = 175 if rows == 1 else 285 - row * 155
                    pdf.setFillColor(HexColor(PALE)); pdf.setStrokeColor(HexColor(LINE)); pdf.roundRect(x, y, box_w, box_h, 7, fill=1, stroke=1)
                    pdf_text(pdf, heading, x + 17, y + box_h - 27, box_w - 34, 12, TEAL, 'Helvetica-Bold')
                    pdf_text(pdf, body, x + 17, y + box_h - 65, box_w - 34, 13.5 if rows == 1 else 12.5, INK, 'Helvetica', 17)
            elif kind == 'code':
                pdf.setFillColor(HexColor(NAVY)); pdf.roundRect(47, 78, 468, 345, 7, fill=1, stroke=0)
                pdf_text(pdf, data['code'], 70, 385, 420, 13, 'E6F6F4', 'Courier', 18)
                pdf_bullets(pdf, data['bullets'], 540, 400, 355, 13.5)
            if data.get('image') and (ROOT / data['image']).exists():
                pdf.drawImage(ImageReader(str(ROOT / data['image'])), 680, 65, width=220, height=110, preserveAspectRatio=True, mask='auto', anchor='se')
        pdf.showPage()
    pdf.save()


def write_notes() -> None:
    elapsed = 0
    lines = ['# Speaker notes — 45 minutes\n', 'Use `docs/demo-runbook.md` for detailed screen steps and backup handling. Run and pull-request links are maintained in `docs/evidence.md`.\n']
    for number, data in enumerate(slides, 1):
        start = elapsed; elapsed += data['duration']
        title = data['title'].replace('\n', ' ')
        lines.append(f"## {number}. {title} — {data['duration']} min ({start:02d}:00–{elapsed:02d}:00)\n")
        lines.append(data['notes'] + '\n')
    (OUT / 'speaker-notes.md').write_text('\n'.join(lines), encoding='utf-8')


if __name__ == '__main__':
    render_pptx()
    render_pdf()
    write_notes()
    print(f'Generated {len(slides)} slides, {sum(s["duration"] for s in slides)} minutes.')
    print(OUT / 'devsecops-presentation.pptx')
    print(OUT / 'devsecops-presentation.pdf')
    print(OUT / 'speaker-notes.md')
