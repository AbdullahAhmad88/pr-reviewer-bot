import os
import requests
import json

# ── Config ──────────────────────────────────────────────
GITHUB_TOKEN  = os.environ["GITHUB_TOKEN"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
PR_NUMBER     = os.environ["PR_NUMBER"]
REPO          = os.environ["REPO"]

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

# ── 1. Fetch the PR diff ─────────────────────────────────
print(f"Fetching diff for PR #{PR_NUMBER}...")

diff_response = requests.get(
    f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}",
    headers={**HEADERS, "Accept": "application/vnd.github.diff"}
)
diff = diff_response.text[:8000]  # Limit to avoid token limits

# ── 2. Send to Gemini ────────────────────────────────────
print("Sending to Gemini for review...")

prompt = f"""You are a senior software engineer doing a code review.
Analyze this pull request diff and provide feedback on:
1. Bugs or logic errors
2. Security vulnerabilities  
3. Code quality improvements
4. Performance issues

Be specific, reference line numbers when possible, and be constructive.
Format your response in clear sections with markdown.

Here is the diff:
{diff}"""

gemini_response = requests.post(
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
    params={"key": GEMINI_API_KEY},
    json={
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.3}
    }
)

review_text = gemini_response.json()["candidates"][0]["content"]["parts"][0]["text"]

# ── 3. Post comment on the PR ─────────────────────────────
print("Posting review comment...")

comment_body = f"""## 🤖 AI Code Review

{review_text}

---
*Reviewed by AI PR Bot using Gemini 1.5 Flash*"""

requests.post(
    f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments",
    headers=HEADERS,
    json={"body": comment_body}
)

print("Done! Review posted successfully.")
