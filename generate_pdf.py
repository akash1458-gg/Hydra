# generate_pdf.py
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        # Top banner background
        self.setStrokeColor(colors.HexColor("#0F172A"))
        self.setLineWidth(2)
        self.setFillColor(colors.HexColor("#DDD6FE"))
        self.rect(36, 545, 720, 26, fill=True, stroke=True)

        self.setFont("Courier-Bold", 9)
        self.setFillColor(colors.HexColor("#0F172A"))
        self.drawString(48, 554, "HYDRA_AI_FIREWALL.pdf // ZERO-TRUST MCP GATEKEEPER")
        self.drawRightString(744, 554, f"SLIDE {self._pageNumber} OF {page_count}")

        # Bottom footer line
        self.setStrokeColor(colors.HexColor("#0F172A"))
        self.setLineWidth(1.5)
        self.line(36, 32, 756, 32)
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(36, 20, "HYDRA &bull; Cryptographic Zero-Trust AI Agent Firewall &bull; Gemini Flash + ArmorIQ CSRG-IAP")
        self.drawRightString(756, 20, "https://github.com/akash1458-gg/Hydra")
        self.restoreState()

def build_pdf():
    pdf_filename = "HYDRA_AI_Agent_Firewall.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=landscape(letter),
        leftMargin=36,
        rightMargin=36,
        topMargin=50,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'SlideTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'SlideSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#475569"),
        spaceAfter=14
    )

    card_title_style = ParagraphStyle(
        'CardTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=4
    )

    card_body_style = ParagraphStyle(
        'CardBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#1E293B")
    )

    code_style = ParagraphStyle(
        'CodeText',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#F8FAFC")
    )

    story = []

    def make_card(title, body_text, bg="#FFFFFF", border="#0F172A"):
        content = [
            Paragraph(f"<b>{title}</b>", card_title_style),
            Spacer(1, 4),
            Paragraph(body_text, card_body_style)
        ]
        t = Table([[content]], colWidths=[350])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg)),
            ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor(border)),
            ('LEFTPADDING', (0,0), (-1,-1), 12),
            ('RIGHTPADDING', (0,0), (-1,-1), 12),
            ('TOPPADDING', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ]))
        return t

    slides_data = [
        # SLIDE 1
        (
            "HYDRA: Autonomous AI Agent Firewall",
            "Cryptographic Zero-Trust Security & Boundary Gatekeeper for Model Context Protocol (MCP) Agents",
            [
                ("✦ The Vision", "As software engineering transitions to autonomous AI agents wielding live execution tools (bash, git, terminal), security can no longer rely on fragile system prompts. HYDRA establishes the world's first cryptographic zero-trust firewall for MCP agents, mathematically binding every tool execution to signed developer intent.", "#FAF5FF"),
                ("✦ Core Value Proposition", "• Deterministic cryptographic intent proofs via ArmorIQ CSRG-IAP.<br/>• Sub-15ms real-time policy evaluation before tool execution.<br/>• Zero-Trust default-deny baseline blocking unauthorized capabilities.<br/>• Production-ready Neo-Brutalist HUD with live GitHub repo integration.", "#ECFDF5")
            ]
        ),
        # SLIDE 2
        (
            "The Vulnerability of Autonomous Agents",
            "Why traditional LLM guardrails fail the moment agents gain real execution tools",
            [
                ("🔨 Real Tools = Real Destruction", "Unlike chatbots, MCP agents execute terminal commands, edit CI/CD workflows, read database secrets, and push git commits. A hijacked agent acts as a rogue insider with admin rights.", "#FEE2E2"),
                ("🎭 Death of Prompt Filters", "System prompts ('Please do not delete files') fail against jailbreaks, token confusion, and indirect prompt injection. Probabilistic safety filters cannot defend system boundaries.", "#FEF3C7"),
                ("💉 Indirect Prompt Injection", "Attacks hide in innocent data: PR descriptions, markdown notes, or dependencies. When the agent inspects the file, the hidden payload hijacks tool calls. Ranked #1 in OWASP Top 10 for LLMs.", "#F1F5F9"),
                ("🏢 Enterprise Adoption Blocked", "78% of CISOs report fear of autonomous agent tool misuse as their primary barrier to adopting agentic workflows. SOC2 and ISO compliance demand deterministic control.", "#EFF6FF")
            ]
        ),
        # SLIDE 3
        (
            "HYDRA Zero-Trust Architecture",
            "End-to-end cryptographic lifecycle from developer directive to verified tool execution",
            [
                ("01 &bull; Developer Directive & Cognitive Planner", "The developer provides a natural-language task. Google Gemini 2.0 / Flash decomposes the prompt into an immutable, strictly typed JSON Execution Graph declaring every tool and argument.", "#DDD6FE"),
                ("02 &bull; ArmorIQ CSRG-IAP Token Minting", "ArmorIQ mints a Cryptographically Signed Request Guard (CSRG-IAP) Intent Token. This token acts as a cryptographic passport containing Merkle inclusion proofs of authorized tool actions.", "#A7F3D0"),
                ("03 &bull; Enterprise Policy Gatekeeper", "The gatekeeper evaluates each tool invocation against enterprise policies (armoriq.yaml) in under 15ms. Malicious commands and unauthorized branches are hard-blocked.", "#BAE6FD"),
                ("04 &bull; Hardened MCP Sandbox Runtime", "Benign tools execute safely against the target repository; hijacked tools and destructive operations are quarantined with instant telemetry alerts.", "#FDE68A")
            ]
        ),
        # SLIDE 4
        (
            "Cryptographic Proofs vs. Guesswork",
            "Replacing probabilistic heuristic filters with deterministic mathematical verification",
            [
                ("Traditional AI Safety (Heuristic Guessing)", "• Probabilistic: Guesses whether text 'looks' harmful based on embeddings.<br/>• Prompt-Layer Defense: Lives inside LLM context; easily subverted by jailbreaks.<br/>• Blind to Injections: Cannot distinguish developer instructions from third-party data.<br/>• Ephemeral Text Logging: Fails strict SOC2 and ISO audit standards.", "#FEE2E2"),
                ("HYDRA AI Agent Firewall (Deterministic Proofs)", "• Deterministic: Mathematically verifies cryptographic Merkle inclusion proofs.<br/>• Tool-Boundary Defense: Independent interceptor outside the LLM container.<br/>• Merkle Verification: Injected actions lack signed intent & are blocked instantly.<br/>• Tamper-Proof Audit: Every verdict, latency, and SHA-256 hash is permanently recorded.", "#DCFCE7")
            ]
        ),
        # SLIDE 5
        (
            "Four Battle-Tested Enforcement Vectors",
            "Real-world DevSecOps attack and defense scenarios running live in HYDRA",
            [
                ("🟩 Vector 01 // Authorized Code Audit", "<b>Target:</b> payment_service.py<br/>Inspects source code, flags CWE-89 SQL injection flaw, and publishes structured remediation review to PR #1.<br/><b>Verdict: ALLOWED & verified in 460ms via signed intent.</b>", "#DCFCE7"),
                ("🟥 Vector 02 // CI/CD Pipeline Tamper", "<b>Target:</b> .github/workflows/deploy.yml<br/>Attacker attempts to disable mandatory SAST security gates and delete repository.<br/><b>Verdict: BLOCKED in 15ms by enterprise policy.</b>", "#FEE2E2"),
                ("🟪 Vector 03 // Indirect Prompt Injection", "<b>Target:</b> external_pr_note.md<br/>Poisoned markdown contains hidden SYSTEM OVERRIDE attempting to hijack tool calls.<br/><b>Verdict: BLOCKED via ArmorIQ Merkle Proof Mismatch!</b>", "#F3E8FF"),
                ("🟨 Vector 04 // Risk-Based Patch Commit", "<b>Target:</b> Safe branch fix/sql-injection-patch<br/>Automated static security analysis followed by verified parameterized SQL query commit.<br/><b>Verdict: ALLOWED & patch merged into feature branch.</b>", "#FEF9C3")
            ]
        ),
        # SLIDE 6
        (
            "Universal GitHub Integration & Zero-Storage PAT",
            "Real-world DevSecOps security across private & public codebases",
            [
                ("🔗 Live Repository Connection", "• Connect any public or private GitHub repository (owner/repo).<br/>• Clones, indexes up to 50 source files, and renders live asset inspectors in the dashboard.<br/>• Allows switching between live external codebases and isolated demo scenarios with zero leftover state.", "#FFFFFF"),
                ("🔑 Zero-Storage Security & Live PRs", "• Zero-Storage PAT: Personal Access Tokens are held strictly in runtime memory—never written to disk.<br/>• MCP tools cannot exfiltrate credentials because tokens are isolated from read tools.<br/>• Direct commits to main/prod are hard-blocked by policy; safe patches are auto-pushed to fix/* with live Pull Request links!", "#DCFCE7")
            ]
        ),
        # SLIDE 7
        (
            "Enterprise-Grade Tech Stack & Performance",
            "Engineered for sub-15ms intercept latency and maximum reliability",
            [
                ("🧠 Google Gemini 2.0 / Flash", "Cognitive Planner generating structured JSON execution graphs via Google GenAI SDK with schema validation and intelligent reasoning.", "#EDE9FE"),
                ("🛡️ ArmorIQ CSRG-IAP", "Cryptographic Signed Request Guard SDK providing Merkle tree proof validation, sub-15ms policy enforcement, and compliance audit logging.", "#D1FAE5"),
                ("⚡ FastMCP Protocol", "Anthropic Model Context Protocol standard with strict path traversal validation and sandboxed file and git operations.", "#E0F2FE"),
                ("🎨 Neo-Brutalist HUD", "Custom Streamlit interface with Dark & Light modes, real-time telemetry HUD pills, git log viewer, and Docker containerization.", "#FEF08A")
            ]
        ),
        # SLIDE 8
        (
            "Business Value & Enterprise ROI",
            "Unlocking 10x engineering velocity without compromising security posture",
            [
                ("🛡️ Eliminate Supply Chain Poisoning", "Prevents AI agents from unintentionally introducing backdoors, overwriting CI/CD gates, or leaking production credentials. Default-deny blocks all unauthorized actions.", "#FEE2E2"),
                ("🚀 10x Autonomous Remediation Velocity", "Enables safe unattended bug fixes: agents can safely analyze flaws, commit parameterized fixes, and open PRs without security bottlenecks.", "#DCFCE7"),
                ("📋 Instant SOC2 & ISO Audit Trail", "Every single tool call is cryptographically signed and logged with latency, parameters, and policy verdicts, making compliance effortless.", "#FEF9C3"),
                ("🤝 CISO & CTO Alignment", "Allows engineering leaders to adopt autonomous AI coding agents while giving security teams deterministic cryptographic control.", "#EDE9FE")
            ]
        ),
        # SLIDE 9
        (
            "2-Minute Live Demo Sequence",
            "Step-by-step judge demonstration guide",
            [
                ("Step 01 // HUD Overview", "Show real-time status pills: GATEKEEPER: ACTIVE, CSRG-IAP: INTENT-BOUND.", "#FFFFFF"),
                ("Step 02 // Attack Attempt", "Click 'Load Vector 02 // Tamper' (directive to overwrite deploy.yml & delete repo).", "#FEE2E2"),
                ("Step 03 // Real-Time Intercept", "Click 'Execute Directive'. Show judges the red BLOCKED verdict in 15ms!", "#FEE2E2"),
                ("Step 04 // Indirect Injection", "Click 'Load Vector 03 // Hijack'. Agent reads external PR note with hidden override.", "#F3E8FF"),
                ("Step 05 // Merkle Proof Quarantine", "Show the PURPLE HIJACK BADGE intercepted by ArmorIQ intent mismatch.", "#F3E8FF"),
                ("Step 06 // Safe Remediation", "Click 'Load Vector 04 // Commit'. Agent analyzes SQL flaw and safely commits patch.", "#DCFCE7")
            ]
        ),
        # SLIDE 10
        (
            "Product Roadmap: From Repository to Swarm Defense",
            "Scaling from repository firewalls to distributed multi-agent mesh security",
            [
                ("Q1: Multi-Provider MCP Proxy", "Native protocol support for Anthropic Claude 3.7, OpenAI Swarm, and AWS Bedrock autonomous tool calls.", "#EDE9FE"),
                ("Q2: Agent-to-Agent Mesh Security", "Cryptographic intent delegation between cooperating agents in multi-agent swarms with mutual verification.", "#D1FAE5"),
                ("Q3: Autonomous Honeytokens", "Dynamic injection of synthetic API keys and decoy CI/CD workflows to trap rogue agent reconnaissance.", "#FEF9C3"),
                ("Q4: Native IDE Sidecar Extension", "VS Code, Cursor, and JetBrains plugins providing real-time firewall telemetry while coding.", "#E0F2FE")
            ]
        ),
        # SLIDE 11
        (
            "Why HYDRA Wins",
            "The defining competitive advantages setting HYDRA apart",
            [
                ("🏆 1. Cryptographic Math, Not Prompting", "First firewall combining Gemini cognitive planning with ArmorIQ CSRG-IAP Merkle proofs. Deterministic guarantees that cannot be bypassed by clever prompt manipulation.", "#DCFCE7"),
                ("⚡ 2. Sub-15ms Latency Overhead", "Zero performance bottleneck for autonomous developer workflows. Pre-execution gatekeeping stops damage before code touches disk.", "#FEF9C3"),
                ("🔒 3. Zero-Trust Default-Deny", "Unrecognized tools and unauthorized branches are hard-blocked by policy. Strict branch protection preserves main/prod repository integrity.", "#FEE2E2"),
                ("🎨 4. Production-Ready Developer UX", "High-contrast Neo-Brutalist HUD with Dark & Light modes, live external GitHub connectivity, file inspection, and complete audit trail.", "#EDE9FE")
            ]
        ),
        # SLIDE 12
        (
            "Secure the Future of Autonomous DevSecOps",
            "Experience the live HYDRA AI Agent Firewall",
            [
                ("🌐 Live Project Resources", "• <b>GitHub Repository:</b> https://github.com/akash1458-gg/Hydra<br/>• <b>Live Dashboard:</b> Deployed on Streamlit Cloud & Cloudflare<br/>• <b>License:</b> Enterprise Apache 2.0<br/>• <b>Documentation:</b> Quickstart, Docker setup, and API specifications included.", "#FFFFFF"),
                ("💬 Questions & Live Testing", "We are ready to take your questions!<br/>Ask us to run custom attack scenarios or test live prompts.<br/>• Cryptographic Merkle intent tokens<br/>• Indirect prompt injection quarantine<br/>• Connecting custom private GitHub repositories<br/><br/><b>Thank you!</b>", "#FAF5FF")
            ]
        ),
    ]

    for title, subtitle, cards in slides_data:
        story.append(Paragraph(title, title_style))
        story.append(Paragraph(subtitle, subtitle_style))
        
        # Render cards in 2 columns
        if len(cards) == 2:
            c1 = make_card(cards[0][0], cards[0][1], bg=cards[0][2])
            c2 = make_card(cards[1][0], cards[1][1], bg=cards[1][2])
            grid = Table([[c1, c2]], colWidths=[360, 360])
            grid.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('TOPPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ]))
            story.append(grid)
        elif len(cards) == 4:
            c1 = make_card(cards[0][0], cards[0][1], bg=cards[0][2])
            c2 = make_card(cards[1][0], cards[1][1], bg=cards[1][2])
            c3 = make_card(cards[2][0], cards[2][1], bg=cards[2][2])
            c4 = make_card(cards[3][0], cards[3][1], bg=cards[3][2])
            grid = Table([[c1, c2], [Spacer(1, 10), Spacer(1, 10)], [c3, c4]], colWidths=[360, 360])
            grid.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('TOPPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ]))
            story.append(grid)
        elif len(cards) == 6:
            # 6 demo steps in 2 columns of 3
            rows = []
            for i in range(0, 6, 2):
                ca = make_card(cards[i][0], cards[i][1], bg=cards[i][2])
                cb = make_card(cards[i+1][0], cards[i+1][1], bg=cards[i+1][2])
                rows.append([ca, cb])
                if i < 4:
                    rows.append([Spacer(1, 6), Spacer(1, 6)])
            grid = Table(rows, colWidths=[360, 360])
            grid.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('TOPPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ]))
            story.append(grid)

        story.append(PageBreak())

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generated successfully: {pdf_filename}")

if __name__ == "__main__":
    build_pdf()
