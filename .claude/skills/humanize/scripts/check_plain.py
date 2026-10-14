"""Flag sentences that are too long or too technical for a non-specialist reader.

Usage: python check_plain.py FILE [FILE ...]   (HTML, Markdown or plain text)
Exit code 1 if anything is flagged.
"""
import html
import re
import sys

MAX_WORDS = 25
JARGON = [
    "agent-based", "stochastic", "reinforcement learning", "ppo", "potential-based", "reward shaping",
    "held-out", "out-of-sample", "confidence interval", "95% ci", "p =", "p-value", "wilcoxon", "holm",
    "bootstrap", "identifiab", "ode", "dynamical-systems", "monte carlo", "in silico", "in-silico",
    "oracle", "ablation", "baseline", "leverag", "utilis", "utiliz", "spearhead", "synerg",
    "end-to-end", "robust", "scalable", "paradigm", "passionate", "results-driven",
]


def text_of(path: str) -> str:
    raw = open(path, encoding="utf-8").read()
    raw = re.sub(r"(?s)<(style|script|head)\b.*?</\1>", " ", raw)
    raw = re.sub(r"<[^>]+>", "\n", raw)
    return html.unescape(raw)


def sentences(text: str):
    for block in re.split(r"\n\s*\n|\n", text):
        block = " ".join(block.split())
        for s in re.split(r"(?<=[.!?])\s+", block):
            if len(s.split()) >= 4:
                yield s


def main(paths) -> int:
    flagged = 0
    for path in paths:
        for s in sentences(text_of(path)):
            words = len(s.split())
            lower = s.lower()
            hits = [j for j in JARGON if re.search(r"\b" + re.escape(j), lower)]
            problems = []
            if words > MAX_WORDS:
                problems.append(f"{words} words (max {MAX_WORDS})")
            if hits:
                problems.append("jargon: " + ", ".join(hits))
            if problems:
                flagged += 1
                print(f"- {s}\n    -> {'; '.join(problems)}")
    print(f"\n{flagged} sentence(s) flagged.")
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
