"""ChatGPT second opinion for the deck (same idea as hl-scanner's gpt_chat.py).

  * Every pull request: ChatGPT reviews the diff and comments. Claude (the
    boss) fixes each real point or replies why not, before merging.
  * "@gpt <question>" in an issue / PR comment: ChatGPT answers there.

Needs the OPENAI_API_KEY repo secret. ~1c per review. It counts toward the
same OpenAI account limit as hl-scanner (set to $5 in OpenAI -> Limits).
"""

import json
import os
import urllib.request

TRIGGER = "@gpt"
MARK = "🧠 **ChatGPT**"
MAX_DIFF = 20000
MODEL = os.environ.get("OPENAI_MODEL", "").strip() or "gpt-5-mini"
AUTO_REVIEW = ("Review this pull request as a second opinion. It changes a single-page "
               "HTML/JS dashboard (index.html) that reads public Hyperliquid/CoinGecko "
               "data in the browser. List real problems first (broken layout on a "
               "phone, JS errors, wrong numbers shown, data or address leaks), then "
               "anything unclear. Finish with one line: 'Verdict: OK to merge' or "
               "'Verdict: fix first - <why>'.")
PROMPT = ("You answer on GitHub for the owner's crypto dashboard repo. The question "
          "comes from the owner or from Claude, the coding assistant. Plain English, "
          "short (max ~200 words), bullets welcome. Say so if unsure.\n\n"
          "Question:\n{q}\n\nThread: {title}\n{body}\n\nRecent comments:\n{comments}\n{diff}")


def gh(path, accept="application/vnd.github+json", data=None, method=None):
    req = urllib.request.Request(
        f"https://api.github.com/repos/{os.environ['GITHUB_REPOSITORY']}/{path}",
        data=json.dumps(data).encode() if data is not None else None, method=method,
        headers={"Authorization": "Bearer " + os.environ["GITHUB_TOKEN"],
                 "Accept": accept, "User-Agent": "hl-deck"})
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read()
    return raw.decode() if "diff" in accept else json.loads(raw or b"null")


def question_of(body):
    if not body or body.lstrip().startswith(MARK) or TRIGGER not in body.lower():
        return None
    i = body.lower().index(TRIGGER)
    return (body[:i] + body[i + len(TRIGGER):]).strip() or "Please review this thread."


def ask(prompt):
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        return None
    body = {"model": MODEL, "max_completion_tokens": 4000,
            "messages": [{"role": "user", "content": prompt}]}
    if MODEL.startswith(("gpt-5", "o")):
        body["reasoning_effort"] = "low"
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions", data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + key})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return (json.load(r)["choices"][0]["message"]["content"] or "").strip() or None
    except Exception as e:
        print("chatgpt failed:", str(e)[:200])
        return None


def run():
    with open(os.environ["GITHUB_EVENT_PATH"]) as f:
        ev = json.load(f)
    if "pull_request" in ev and "comment" not in ev:
        issue, q, who = ev["pull_request"], AUTO_REVIEW, "auto review"
    else:
        q = question_of(ev.get("comment", {}).get("body"))
        if not q:
            print("not a @gpt question")
            return
        issue, who = ev["issue"], "asked by @" + ev["comment"]["user"]["login"]
    n = issue["number"]
    comments = gh(f"issues/{n}/comments?per_page=30")
    diff = ""
    if issue.get("pull_request") or "pull_request" in ev:
        try:
            diff = gh(f"pulls/{n}", accept="application/vnd.github.v3.diff")
        except Exception as e:
            print("diff failed:", e)
    cm = "\n".join(f"- {c['user']['login']}: {c['body'][:600]}" for c in comments[-6:]) or "(none)"
    reply = ask(PROMPT.format(q=q, title=issue.get("title", ""), body=(issue.get("body") or "")[:3000],
                              comments=cm, diff=f"\nDiff (may be cut):\n{diff[:MAX_DIFF]}\n" if diff else ""))
    reply = reply or "_No answer: missing OPENAI_API_KEY secret, or ChatGPT errored (see the Actions log)._"
    gh(f"issues/{n}/comments", method="POST",
       data={"body": f"{MARK} ({who}):\n\n{reply}\n\n-# second opinion, not advice"[:60000]})
    print("answered on #", n)


if __name__ == "__main__":
    run()
