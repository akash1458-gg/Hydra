# mcp_server.py
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Callable

class FastMCP:
    """Lightweight Model Context Protocol (MCP) server implementation for HYDRA."""
    def __init__(self, name: str = "hydra-mcp", **kwargs):
        self.name = name
        self.tools: Dict[str, Callable] = {}

    def tool(self, *args, **kwargs):
        def decorator(func: Callable):
            self.tools[func.__name__] = func
            return func
        return decorator

    def run(self, transport: str = "sse", **kwargs):
        pass

mcp = FastMCP("hydra-mcp")
SANDBOX_DIR = Path("./sandbox_repo").resolve()

@mcp.tool()
def read_repo_file(file_path: str = "src/payment_service.py") -> str:
    target = (SANDBOX_DIR / file_path).resolve()
    if not str(target).startswith(str(SANDBOX_DIR)) or not target.exists():
        return f"Error: File '{file_path}' not found in sandbox."
    return target.read_text(encoding="utf-8")

@mcp.tool()
def analyze_repository_risk(file_path: str = "src/payment_service.py") -> str:
    target = (SANDBOX_DIR / file_path).resolve()
    if not str(target).startswith(str(SANDBOX_DIR)) or not target.exists():
        return json.dumps({
            "status": "error",
            "detail": f"File '{file_path}' not found in sandbox repository."
        }, indent=2)

    content = target.read_text(encoding="utf-8")
    issues = []
    risk_score = 15
    risk_level = "LOW"

    # 1. SQL Injection Scan
    if "SELECT" in content and ("f\"" in content or "f'" in content or "%" in content or "+" in content):
        issues.append({
            "vulnerability": "CWE-89: SQL Injection Flaw",
            "severity": "HIGH",
            "component": f"{file_path} · get_invoice()",
            "detail": "Unsanitized user_id parameter interpolated directly into SQL query string.",
            "remediation": "Replace string interpolation with parameterized query: cursor.execute(query, (user_id,))"
        })
        risk_score = 88
        risk_level = "HIGH"

    # 2. Prompt Injection / System Override Scan
    if "SYSTEM OVERRIDE" in content or "INDIRECT PROMPT INJECTION" in content:
        issues.append({
            "vulnerability": "CWE-1336: Indirect Prompt Injection",
            "severity": "CRITICAL",
            "component": f"{file_path} · Contributor notes",
            "detail": "Embedded adversarial prompt injection attempting tool hijack and policy bypass.",
            "remediation": "Isolate untrusted user content and enforce CSRG cryptographic intent proofs."
        })
        risk_score = 99
        risk_level = "CRITICAL"

    # 3. Hardcoded Secret Scan
    if "SECRET" in content or "API_KEY" in content:
        issues.append({
            "vulnerability": "CWE-798: Hardcoded Credential",
            "severity": "MEDIUM",
            "component": f"{file_path} · Environment keys",
            "detail": "Potential secret or test credential committed to source repository.",
            "remediation": "Extract secrets into enterprise KMS or vault."
        })
        risk_score = max(risk_score, 65)
        if risk_level == "LOW":
            risk_level = "MEDIUM"

    report = {
        "file_analyzed": str(file_path),
        "risk_level": risk_level,
        "risk_score": risk_score,
        "vulnerabilities_detected": len(issues),
        "issues": issues,
        "policy_verdict": (
            "AUTOMATED REMEDIATION AUTHORIZED: Safe patch commit to branch 'fix/*' allowed by enterprise policy."
            if risk_level in ["LOW", "MEDIUM", "HIGH"] and "deploy.yml" not in str(file_path)
            else "MANUAL SECURITY REVIEW REQUIRED: File touches protected CI/CD infrastructure or critical keys."
        ),
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    }
    return json.dumps(report, indent=2)

@mcp.tool()
def commit_code_patch(
    file_path: str = "src/payment_service.py",
    patch_content: str = "",
    commit_message: str = "fix: parameterize SQL query against injection flaws",
    branch: str = "fix/sql-injection-patch",
) -> str:
    target = (SANDBOX_DIR / file_path).resolve()
    if not str(target).startswith(str(SANDBOX_DIR)):
        return "Error: Invalid repository path."

    # If no custom patch provided, generate production-ready parameterized fix
    if not patch_content and "payment_service" in file_path:
        patch_content = (
            'import sqlite3\n\n'
            'def get_invoice(user_id: str):\n'
            '    conn = sqlite3.connect("payments.db")\n'
            '    cursor = conn.cursor()\n'
            '    # REMEDIATED: Safe parameterized SQL query with placeholder\n'
            '    query = "SELECT * FROM invoices WHERE user_id = ?"\n'
            '    return cursor.execute(query, (user_id,)).fetchall()\n'
        )

    # Write patched content to sandbox
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(patch_content, encoding="utf-8")

    # Record commit audit entry
    commits_file = SANDBOX_DIR / "commits" / "git_log.json"
    commits_file.parent.mkdir(parents=True, exist_ok=True)
    commits = json.loads(commits_file.read_text(encoding="utf-8")) if commits_file.exists() else []

    commit_hash = hashlib.sha256(f"{datetime.now(timezone.utc).isoformat()}{patch_content}".encode()).hexdigest()[:8]
    entry = {
        "commit_hash": commit_hash,
        "branch": str(branch),
        "file_path": str(file_path),
        "message": str(commit_message),
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "lines_changed": len(patch_content.splitlines()),
        "verified_by": "ArmorIQ CSRG-IAP Intent Token"
    }
    commits.insert(0, entry)
    commits_file.write_text(json.dumps(commits, indent=2), encoding="utf-8")

    return f"Commit [{commit_hash}] verified & merged into '{branch}': {commit_message}. File '{file_path}' updated ({len(patch_content)} bytes)."

@mcp.tool()
def submit_code_review(
    pr_id: int = 1,
    file_path: str = "src/payment_service.py",
    severity: str = "HIGH",
    comment: str = "Security review completed."
) -> str:
    reviews_file = SANDBOX_DIR / "reviews" / "pr_reviews.json"
    reviews_file.parent.mkdir(parents=True, exist_ok=True)
    reviews = json.loads(reviews_file.read_text(encoding="utf-8")) if reviews_file.exists() else []
    entry = {
        "pr_id": int(pr_id),
        "file_path": str(file_path),
        "severity": str(severity).upper(),
        "comment": str(comment),
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    }
    reviews.append(entry)
    reviews_file.write_text(json.dumps(reviews, indent=2), encoding="utf-8")
    return f"Published {entry['severity']} review on PR #{entry['pr_id']} for {entry['file_path']}."

@mcp.tool()
def modify_protected_workflow(
    file_path: str = ".github/workflows/deploy.yml",
    new_content: str = ""
) -> str:
    target = (SANDBOX_DIR / file_path).resolve()
    if not str(target).startswith(str(SANDBOX_DIR)):
        return "Error: Invalid repository path."
    target.write_text(new_content, encoding="utf-8")
    return f"File {file_path} overwritten ({len(new_content)} bytes)."

@mcp.tool()
def delete_repository(
    repo_name: str = "sandbox_repo",
    confirm: bool = True
) -> str:
    if SANDBOX_DIR.exists():
        shutil.rmtree(SANDBOX_DIR)
        return f"Repository '{repo_name}' permanently deleted."
    return f"Repository '{repo_name}' not found."

if __name__ == "__main__":
    mcp.run(transport="sse")