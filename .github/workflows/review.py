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

prompt = f"""You are a senior software engineer reviewing a pull request.

Review the following diff and structure your response EXACTLY like this:

## Summary
One paragraph overview of what this PR does.

## 🐛 Bugs Found
List any bugs. If none, write "No bugs found."

## 🔒 Security Issues  
List security vulnerabilities (SQL injection, hardcoded secrets, etc). If none, write "None found."

## 💡 Suggestions
List code quality, performance, or readability improvements.

## ✅ What's Done Well
Mention 1-2 positive things about the code.

Be specific with line numbers from the diff when possible.

DIFF:
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
