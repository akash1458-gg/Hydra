# generate_deck.py
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color Palette (HYDRA Neo-Brutalist Theme)
    C_BG = RGBColor(245, 239, 235)        # #F5EFEB Warm retro paper
    C_NAVY = RGBColor(15, 23, 42)          # #0F172A Deep slate / border
    C_WHITE = RGBColor(255, 255, 255)      # Card background
    C_LAVENDER = RGBColor(221, 214, 254)   # #DDD6FE
    C_MINT = RGBColor(167, 243, 208)       # #A7F3D0
    C_CORAL = RGBColor(254, 202, 202)      # #FECACA
    C_YELLOW = RGBColor(253, 230, 138)     # #FDE68A
    C_BLUE = RGBColor(186, 230, 253)       # #BAE6FD
    C_MUTED = RGBColor(100, 116, 139)      # #64748B
    C_GREEN = RGBColor(34, 197, 94)        # #22C55E Emerald
    C_RED = RGBColor(239, 68, 68)          # #EF4444

    blank_layout = prs.slide_layouts[6]

    def set_slide_background(slide, color=C_BG):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_badge="HYDRA // FLOW STATE v3.8"):
        # Header Badge
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.5), Inches(3.2), Inches(0.42))
        badge.fill.solid()
        badge.fill.fore_color.rgb = C_LAVENDER
        badge.line.color.rgb = C_NAVY
        badge.line.width = Pt(2)
        tf = badge.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = category_badge
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_NAVY
        p.font.name = "Courier New"

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.0), Inches(11.7), Inches(0.8))
        tf_title = title_box.text_frame
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(26)
        p_title.font.bold = True
        p_title.font.color.rgb = C_NAVY
        p_title.font.name = "Arial"

    def add_card(slide, left, top, width, height, title, body_bullets, accent_color=C_WHITE, border_color=C_NAVY):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = accent_color
        card.line.color.rgb = border_color
        card.line.width = Pt(2)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.2)

        if title:
            p0 = tf.paragraphs[0]
            p0.text = title
            p0.font.size = Pt(15)
            p0.font.bold = True
            p0.font.color.rgb = C_NAVY
            p0.font.name = "Arial"
            p0.space_after = Pt(8)

        for item in body_bullets:
            p = tf.add_paragraph()
            p.text = "• " + item
            p.font.size = Pt(12)
            p.font.color.rgb = C_NAVY
            p.font.name = "Arial"
            p.space_after = Pt(4)
        return card

    # ==========================================
    # SLIDE 1: Title Slide
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, C_BG)

    title_window = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.2), Inches(11.33), Inches(5.1))
    title_window.fill.solid()
    title_window.fill.fore_color.rgb = C_WHITE
    title_window.line.color.rgb = C_NAVY
    title_window.line.width = Pt(3)

    tf1 = title_window.text_frame
    tf1.word_wrap = True
    tf1.margin_left = Inches(0.6)
    tf1.margin_top = Inches(0.6)

    p = tf1.paragraphs[0]
    p.text = "✦ ZERO-TRUST AI AGENT FIREWALL"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.font.name = "Courier New"
    p.space_after = Pt(14)

    p = tf1.add_paragraph()
    p.text = "HYDRA"
    p.font.size = Pt(50)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.font.name = "Arial"

    p = tf1.add_paragraph()
    p.text = "Cryptographic Intent Verification & Boundary Protection for MCP Agents"
    p.font.size = Pt(18)
    p.font.color.rgb = C_MUTED
    p.font.name = "Arial"
    p.space_after = Pt(28)

    p = tf1.add_paragraph()
    p.text = "Powered by Google Gemini 2.0 / Flash  •  ArmorIQ CSRG-IAP  •  FastMCP Protocol"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.font.name = "Courier New"

    s1.notes_slide.notes_text_frame.text = (
        "Hello everyone. Today we are presenting HYDRA, an enterprise-grade autonomous AI agent firewall. "
        "As software development transitions from human coders to autonomous agents with real execution tools, "
        "security cannot rely on fuzzy prompt engineering. HYDRA establishes the world's first cryptographic zero-trust "
        "firewall for Model Context Protocol agents, ensuring every single tool action is mathematically verified against signed user intent."
    )

    # ==========================================
    # SLIDE 2: The Core Problem
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "The Vulnerability of Autonomous Agents", "THE PROBLEM // ATTACK SURFACE")

    add_card(s2, 0.8, 1.8, 5.6, 2.3, "Real Tools = Real Destruction", [
        "MCP agents have real operating capabilities.",
        "They execute bash commands, edit CI/CD workflows, read database secrets, and push git commits.",
        "A hijacked agent is equivalent to a rogue insider with admin privileges."
    ], C_CORAL)

    add_card(s2, 6.8, 1.8, 5.6, 2.3, "Death of Prompt Filtering", [
        "System prompts ('Please do not delete files') fail routinely.",
        "Vulnerable to jailbreaks, token confusion, and multi-turn manipulation.",
        "Probabilistic text safety filters cannot guarantee boundary security."
    ], C_WHITE)

    add_card(s2, 0.8, 4.4, 5.6, 2.3, "Indirect Prompt Injection", [
        "Attacks hide in innocent data: PR descriptions, markdown notes, or dependencies.",
        "When the agent inspects the file, the embedded override hijacks execution tools.",
        "Ranked as the #1 critical vulnerability in the OWASP Top 10 for LLMs."
    ], C_WHITE)

    add_card(s2, 6.8, 4.4, 5.6, 2.3, "Enterprise Adoption Blocked", [
        "78% of CISOs cite fear of autonomous tool execution as the primary blocker to agent rollout.",
        "Compliance mandates (SOC2, ISO 27001) require deterministic, auditable access controls."
    ], C_YELLOW)

    s2.notes_slide.notes_text_frame.text = (
        "When you give an LLM access to MCP tools like git commit or delete_repository, traditional safety filters become useless. "
        "If an agent inspects an external pull request note containing a hidden prompt injection, the agent gets hijacked from the inside. "
        "Without an independent firewall, your CI/CD pipeline and codebase are entirely at the mercy of untrusted inputs."
    )

    # ==========================================
    # SLIDE 3: Architecture
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "HYDRA Zero-Trust Architecture", "SYSTEM PIPELINE // END-TO-END")

    add_card(s3, 0.8, 1.8, 2.7, 4.8, "01 DIRECTIVE", [
        "Natural language prompt.",
        "Developer specifies the goal (e.g. 'Audit payment_service.py').",
        "Target repository selected (demo sandbox or live GitHub)."
    ], C_BLUE)

    add_card(s3, 3.8, 1.8, 2.7, 4.8, "02 GEMINI PLANNER", [
        "Cognitive reasoning engine.",
        "Decomposes intent into a typed JSON execution graph.",
        "Declares tool names and inputs with strict schema validation."
    ], C_LAVENDER)

    add_card(s3, 6.8, 1.8, 2.7, 4.8, "03 CSRG-IAP GATE", [
        "ArmorIQ policy engine.",
        "Mints cryptographic intent token with Merkle proof.",
        "Evaluates each action in <15ms before execution."
    ], C_MINT)

    add_card(s3, 9.8, 1.8, 2.7, 4.8, "04 MCP RUNTIME", [
        "Hardened sandbox environment.",
        "Benign actions execute safely.",
        "Destructive commands and injected tools are hard-quarantined!"
    ], C_YELLOW)

    s3.notes_slide.notes_text_frame.text = (
        "HYDRA solves this with a 4-stage Zero-Trust architecture. First, the developer states their objective. "
        "Gemini parses this into a structured execution graph. Next, ArmorIQ mints a cryptographic intent token that acts as a digital passport. "
        "When the agent attempts any tool action, the HYDRA firewall evaluates whether that action has a valid cryptographic proof and complies with enterprise policy. "
        "If an injected tool call tries to execute, it is hard-blocked at the gate in under 15 milliseconds."
    )

    # ==========================================
    # SLIDE 4: Innovation
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Deterministic Cryptography vs. Probabilistic Guessing", "PARADIGM SHIFT // INNOVATION")

    add_card(s4, 0.8, 1.8, 5.6, 4.8, "Traditional AI Guardrails", [
        "Probabilistic: Guesses if an input 'looks' harmful based on text embeddings.",
        "Prompt-Layer Defense: Lives inside the LLM context; easily subverted by jailbreaks.",
        "Blind to Injections: Cannot distinguish between developer instructions and third-party file data.",
        "Ephemeral Logging: Standard console text; fails strict SOC2 audit standards.",
        "Outcome: Vulnerable to tool hijack and pipeline destruction."
    ], C_CORAL)

    add_card(s4, 6.8, 1.8, 5.6, 4.8, "HYDRA AI Agent Firewall", [
        "Deterministic: Mathematically verifies cryptographic Merkle inclusion proofs.",
        "Tool-Boundary Defense: Independent interceptor outside the LLM execution container.",
        "CSRG Merkle Verification: Injected actions lack the developer's signed token and are blocked instantly.",
        "Tamper-Proof Audit: Every verdict, latency metric, and SHA-256 hash is permanently recorded.",
        "Outcome: Mathematically guaranteed zero-trust boundary."
    ], C_MINT)

    s4.notes_slide.notes_text_frame.text = (
        "The critical innovation here is moving from heuristic guessing to deterministic cryptographic proofs. "
        "We do not ask an LLM 'Does this look safe?'. Instead, we mathematically verify whether the specific tool call was part "
        "of the original cryptographically signed intent. If an attacker injects a command through a poisoned markdown file, "
        "that command does not exist in the signed Merkle tree—and the firewall intercepts it with zero hesitation."
    )

    # ==========================================
    # SLIDE 5: 4 Enforcement Vectors
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Four Battle-Tested Attack & Defense Vectors", "LIVE SCENARIOS // PRODUCTION AUDIT")

    add_card(s5, 0.8, 1.8, 5.6, 2.3, "Vector 01 // Authorized Code Audit", [
        "Action: Inspects payment_service.py for security vulnerabilities.",
        "Detects CWE-89 SQL injection and submits review to PR #1.",
        "Verdict: ALLOWED & verified in 460ms via signed intent."
    ], C_MINT)

    add_card(s5, 6.8, 1.8, 5.6, 2.3, "Vector 02 // CI/CD Pipeline Tamper", [
        "Action: Attacker attempts to overwrite deploy.yml and delete sandbox.",
        "Aims to disable mandatory SAST tests in production CI/CD.",
        "Verdict: BLOCKED in 15ms by 'hydra-block-destructive-ops'."
    ], C_CORAL)

    add_card(s5, 0.8, 4.4, 5.6, 2.3, "Vector 03 // Indirect Prompt Injection", [
        "Action: Agent reads external_pr_note.md containing hidden SYSTEM OVERRIDE.",
        "Adversarial note attempts to hijack tools to erase the repository.",
        "Verdict: BLOCKED by ArmorIQ Merkle Proof Mismatch!"
    ], C_LAVENDER)

    add_card(s5, 6.8, 4.4, 5.6, 2.3, "Vector 04 // Risk-Based Patch Commit", [
        "Action: Static security scan of SQL flaw + automated parameterization.",
        "Branch Protection: Direct commit to main blocked; fix/* allowed.",
        "Verdict: ALLOWED & patch committed to feature branch."
    ], C_YELLOW)

    s5.notes_slide.notes_text_frame.text = (
        "To prove HYDRA in production, we built four comprehensive attack and defense vectors directly into the dashboard. "
        "We test authorized reviews, direct CI/CD pipeline destruction attacks, indirect prompt injection hijacks embedded in contributor notes, "
        "and end-to-end automated remediation patches with branch protection."
    )

    # ==========================================
    # SLIDE 6: External Repo Integration
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Universal GitHub Integration & Zero-Storage PAT", "CONNECT ANY REPOSITORY // PRODUCTION")

    add_card(s6, 0.8, 1.8, 5.6, 4.8, "Live Repository Connection", [
        "Boxed sidebar interface allows connecting any GitHub repo (owner/repo).",
        "Clones, indexes up to 50 source files, and renders live asset inspectors in the dashboard.",
        "Supports both public repositories and private enterprise codebases.",
        "Instant toggle between live repos and isolated demo scenarios."
    ], C_WHITE)

    add_card(s6, 6.8, 1.8, 5.6, 4.8, "Zero-Storage Security & Live PRs", [
        "Zero-Storage PAT: Personal Access Tokens are kept strictly in memory for git push and PR creation—never written to disk.",
        "MCP tools cannot exfiltrate credentials because tokens are isolated from read tools.",
        "Branch Protection Enforcement: Direct commits to main/prod are hard-blocked.",
        "Safe patches automatically pushed to fix/* branches with clickable Pull Request links!"
    ], C_MINT)

    s6.notes_slide.notes_text_frame.text = (
        "HYDRA isn't limited to a static sandbox. Developers can connect any public or private GitHub repository using our boxed Target Repository panel. "
        "HYDRA clones, indexes, and monitors the target repo. If you provide a write token, HYDRA commits safe patches to isolated branches and opens "
        "live Pull Requests directly on GitHub—while strictly enforcing branch protection policies on main."
    )

    # ==========================================
    # SLIDE 7: Tech Stack
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Enterprise-Grade Engineering & Tech Stack", "ARCHITECTURE // PERFORMANCE")

    add_card(s7, 0.8, 1.8, 2.7, 4.8, "Google Gemini", [
        "Gemini 2.0 / Flash.",
        "Structured JSON schema enforcement.",
        "Decomposes ambiguous prompts into precise action graphs.",
        "High-throughput reasoning."
    ], C_LAVENDER)

    add_card(s7, 3.8, 1.8, 2.7, 4.8, "ArmorIQ CSRG-IAP", [
        "Cryptographic intent tokens.",
        "Merkle tree proof validation.",
        "Sub-15ms policy gatekeeper.",
        "Enforces enterprise rules in armoriq.yaml."
    ], C_MINT)

    add_card(s7, 6.8, 1.8, 2.7, 4.8, "FastMCP Protocol", [
        "Anthropic Model Context Protocol standard.",
        "SSE and in-process execution.",
        "Strict path traversal validation.",
        "Sandboxed file & git operations."
    ], C_BLUE)

    add_card(s7, 9.8, 1.8, 2.7, 4.8, "Neo-Brutalist HUD", [
        "Streamlit frontend.",
        "Dark & Light mode support.",
        "Real-time telemetry pills.",
        "Git commit audit log viewer.",
        "Containerized with Docker."
    ], C_YELLOW)

    s7.notes_slide.notes_text_frame.text = (
        "Our stack combines the reasoning capabilities of Google Gemini with ArmorIQ's cryptographic policy engine, running on top of the FastMCP protocol. "
        "Policy evaluation takes less than 15 milliseconds, introducing virtually zero latency into the developer loop while providing uncompromised security."
    )

    # ==========================================
    # SLIDE 8: Business Value
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Business Value & Enterprise ROI", "IMPACT // COMPLIANCE")

    add_card(s8, 0.8, 1.8, 5.6, 2.3, "Eliminate Supply Chain Poisoning", [
        "Stops rogue agents from committing backdoors or deleting production repos.",
        "Zero-trust default-deny blocks all unauthorized actions."
    ], C_CORAL)

    add_card(s8, 6.8, 1.8, 5.6, 2.3, "10x Engineering Velocity", [
        "Allows safe unattended bug fixing: agents can safely analyze flaws, commit fixes, and open PRs.",
        "Removes manual security bottlenecks."
    ], C_MINT)

    add_card(s8, 0.8, 4.4, 5.6, 2.3, "Instant Compliance Audit Trail", [
        "Every decision, token, and tool verdict is logged with SHA-256 hashes.",
        "Fulfills SOC2 Type II, ISO 27001, and HIPAA compliance mandates."
    ], C_YELLOW)

    add_card(s8, 6.8, 4.4, 5.6, 2.3, "Executive Alignment (CTO + CISO)", [
        "CTOs gain the productivity of autonomous AI coding agents.",
        "CISOs get deterministic cryptographic boundary control."
    ], C_LAVENDER)

    s8.notes_slide.notes_text_frame.text = (
        "For enterprises, HYDRA is the missing bridge between AI productivity and security compliance. CTOs want the speed of autonomous coding agents, "
        "but CISOs cannot tolerate the risk of unattended repository writes. HYDRA satisfies both: agents can autonomously fix vulnerabilities and open "
        "pull requests, while the CISO has a mathematically verifiable cryptographic audit trail."
    )

    # ==========================================
    # SLIDE 9: Live Demo Playbook
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "2-Minute Hackathon Demonstration Playbook", "LIVE WALKTHROUGH SEQUENCE")

    add_card(s9, 0.8, 1.8, 11.7, 4.8, "Step-by-Step Judge Walkthrough", [
        "Step 01 // HUD Overview: Show live status pills (GATEKEEPER: ACTIVE, CSRG-IAP: INTENT-BOUND).",
        "Step 02 // Attack Attempt: Click 'Load Vector 02 // Tamper' (directive to overwrite deploy.yml & delete repo).",
        "Step 03 // Real-Time Intercept: Click 'Execute Directive'. Show judges the red BLOCKED verdict in 15ms!",
        "Step 04 // Indirect Injection: Click 'Load Vector 03 // Hijack'. Agent reads external PR note with hidden SYSTEM OVERRIDE.",
        "Step 05 // Merkle Proof Quarantine: Show the PURPLE HIJACK BADGE intercepted by ArmorIQ intent mismatch.",
        "Step 06 // Safe Remediation: Click 'Load Vector 04 // Commit'. Agent analyzes SQL flaw and safely commits patch.",
        "Step 07 // Git Proof: Expand 'Git Commit Log' to inspect the verified commit and Pull Request link."
    ], C_WHITE)

    s9.notes_slide.notes_text_frame.text = (
        "During our live demo, we will show judges exactly how HYDRA handles both direct attacks and hidden prompt injections in real time. "
        "We demonstrate the instant 15ms refusal of CI/CD tampering, the Merkle proof quarantine of indirect prompt injections, "
        "and finally the clean automated remediation of a live SQL vulnerability."
    )

    # ==========================================
    # SLIDE 10: Roadmap
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Product Roadmap: From Repository to Swarm Defense", "FUTURE VISION // EXPANSION")

    add_card(s10, 0.8, 1.8, 5.6, 2.3, "Q1: Multi-Provider MCP Proxy", [
        "Native protocol support for Anthropic Claude 3.7, OpenAI Swarm, and AWS Bedrock tools.",
        "Universal reverse-proxy for enterprise MCP deployments."
    ], C_LAVENDER)

    add_card(s10, 6.8, 1.8, 5.6, 2.3, "Q2: Agent-to-Agent Mesh Security", [
        "Cryptographic intent delegation between cooperating agents in multi-agent swarms.",
        "Mutual TLS and verifiable identity for autonomous agent chains."
    ], C_MINT)

    add_card(s10, 0.8, 4.4, 5.6, 2.3, "Q3: Autonomous Honeytokens", [
        "Dynamic injection of synthetic API keys and decoy CI/CD workflows.",
        "Traps rogue agent reconnaissance before any production assets are queried."
    ], C_YELLOW)

    add_card(s10, 6.8, 4.4, 5.6, 2.3, "Q4: Native IDE Sidecar Extension", [
        "VS Code, Cursor, and JetBrains plugins providing real-time firewall telemetry.",
        "Inline security alerts directly in the developer's editor."
    ], C_BLUE)

    s10.notes_slide.notes_text_frame.text = (
        "Looking ahead, HYDRA is expanding into a multi-agent mesh firewall. As software development evolves toward fleets of cooperating agents, "
        "HYDRA will enforce cryptographic intent delegation between agents, dynamic deception honeytokens, and native IDE sidecar integration."
    )

    # ==========================================
    # SLIDE 11: Competitive Edge
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Why HYDRA Wins the Category", "COMPETITIVE MOAT // KEY ADVANTAGES")

    add_card(s11, 0.8, 1.8, 5.6, 2.3, "1. Cryptographic Math, Not Prompting", [
        "First firewall combining Gemini cognitive graphs with ArmorIQ Merkle proofs.",
        "Deterministic security guarantees that cannot be bypassed by clever jailbreaks."
    ], C_MINT)

    add_card(s11, 6.8, 1.8, 5.6, 2.3, "2. Sub-15ms Real-Time Enforcement", [
        "Zero latency bottleneck for autonomous developer workflows.",
        "Pre-execution gatekeeping stops damage before code touches disk."
    ], C_YELLOW)

    add_card(s11, 0.8, 4.4, 5.6, 2.3, "3. Zero-Trust Default-Deny", [
        "Unrecognized tools and unauthorized branches are hard-blocked by policy.",
        "Strict branch protection preserves main/prod repository integrity."
    ], C_CORAL)

    add_card(s11, 6.8, 4.4, 5.6, 2.3, "4. Production-Ready Developer UX", [
        "High-contrast Neo-Brutalist HUD with Dark & Light modes.",
        "Live external GitHub connectivity, file inspection, and PR generation."
    ], C_LAVENDER)

    s11.notes_slide.notes_text_frame.text = (
        "To summarize: HYDRA is not another prompt wrapper. It is a genuine, low-latency zero-trust security layer that mathematically locks down MCP tool execution. "
        "It protects against direct attacks, supply chain tampering, and indirect prompt injections, making autonomous agent deployment safe and enterprise-ready."
    )

    # ==========================================
    # SLIDE 12: Conclusion & Q&A
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Secure the Future of Autonomous DevSecOps", "CONCLUSION // Q & A")

    add_card(s12, 0.8, 1.8, 5.6, 4.8, "Live Project Resources", [
        "GitHub Repository: https://github.com/akash1458-gg/Hydra",
        "Live Dashboard: Deployed on Streamlit Cloud",
        "License: Enterprise Open Source (Apache 2.0)",
        "Documentation: Full quickstart, Docker setup, and API specifications included.",
        "Testing: 100% test pass rate across all 4 enforcement attack vectors."
    ], C_WHITE)

    add_card(s12, 6.8, 1.8, 5.6, 4.8, "Questions & Live Attack Testing", [
        "We are ready to take your questions!",
        "Live Scenario Requests: Ask us to run custom prompts or attack vectors live on stage.",
        "Ask about:",
        "  • Cryptographic Merkle intent tokens",
        "  • Indirect prompt injection defense",
        "  • Connecting custom private GitHub repositories",
        "Thank you for your time!"
    ], C_LAVENDER)

    s12.notes_slide.notes_text_frame.text = (
        "Thank you for your time. The live dashboard is up and running, our repository is open on GitHub, "
        "and we'd be delighted to take any questions or run custom attack scenarios for you right now."
    )

    output_path = "HYDRA_AI_Agent_Firewall.pptx"
    prs.save(output_path)
    print(f"Presentation saved successfully to {output_path}")

if __name__ == "__main__":
    create_deck()
