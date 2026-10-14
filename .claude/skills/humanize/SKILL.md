---
name: humanize
description: Rewrite any human-facing document (CV, cover letter, statement of purpose, report, any PDF) in plain, natural language a non-specialist interviewer understands in one read, without inflating or changing any claim. Use before producing or updating any PDF, and whenever the user says a text is "too complex", "too technical", "robotic", "AI-sounding" or "not human".
---

# Humanize

Make documents read as if a clear-thinking person wrote them for another person: short, concrete, honest. The reader is a busy recruiter or interviewer who is **not** a specialist and gives the page under a minute.

## When to use

- Before generating or regenerating **any PDF** (CV, cover letter, report, statement).
- When the user says a text is too complex, too technical, or sounds like AI.
- GitHub READMEs are written for engineers. Humanize only their top summary, not the methods sections.

## The five tests (every sentence must pass all of them)

1. **Interviewer test.** Could a non-specialist repeat it back after one read? If not, rewrite it.
2. **Plain-word test.** Use the everyday word unless the technical term *is* the skill being advertised (see the swap list).
3. **Result test.** Each bullet says *what I did*, then *what happened*, ideally with **one** number a layperson understands ("499 out of 500", "16% more").
4. **Truth test.** Simplifying must never strengthen a claim. Every number must trace to a result file or a repo. Keep honest caveats ("not peer-reviewed", "in a simulator").
5. **Length test.** Sentences under about 25 words. Bullets of 1–2 lines. At most 3 bullets per item.

## Swap list (technical → plain)

| Instead of | Write |
|---|---|
| agent-based simulator / stochastic model | simulation |
| reinforcement learning / PPO policy | trained an AI |
| reward hacking | the AI found a loophole / learned to "cheat" |
| potential-based reward shaping | fixed the reward |
| held-out evaluation / out-of-sample | tested on cases it had never seen |
| 95% CI, p-values, Wilcoxon, Holm | leave out of the CV; keep them in the repo |
| structurally identifiable parameters | unknowns the model could pin down |
| ODE / dynamical-systems model | mathematical model |
| Monte Carlo dispersion testing | tested in many random conditions (wind, gravity) |
| leveraged, utilised, spearheaded, synergy | used, led, worked with |
| in-silico | computer simulation |
| benchmarked against an oracle | compared with the best possible result |

Technical terms that *are* the skill (Python, PCR, machine learning, DNA sequencing) stay, usually in the Skills section.

## Patterns that sound robotic (remove them)

- Stacked adjectives and abstractions: "robust, scalable, end-to-end framework".
- Lists of three for rhythm: "rigorous, reproducible and principled".
- Empty openers: "Passionate about…", "Results-driven professional…".
- Explaining the method instead of the outcome.
- Colons and dashes chaining clauses together. Use two sentences instead.
- Long titles. A project title is the question it answers, in under 10 words ("Teaching an AI to land a rocket").

## Structure for a CV

1. Name, one-line plain tagline, contact (email, GitHub, ORCID; no phone number in public copies).
2. **About me**: 3–4 sentences. Background, what I build, what I want.
3. **Projects**: strongest first; plain title linked to the repo; 2–3 result bullets.
4. Research writing, Education, Experience, Skills. Keep it to two pages at most.

## Before / after (from this CV)

- **Before:** "Committing to the best option while abandoning projects on statistical evidence of overrun gave +15.8% capability over the best convergent baseline (95% CI 13.0–18.9%)."
  **After:** "The best strategy was 'commit fully, but quit a project once the evidence shows it is failing'. It achieved 16% more progress and cut wasted budget by more than half."
- **Before:** "Reproduced reward hacking: a per-frame 'upright and slow' bonus taught all 5 seeds to hover until timeout."
  **After:** "Showed how a badly designed reward makes an AI 'cheat': paid for staying upright, it learned to hover forever instead of landing."

## Process

1. Draft or edit the HTML source (for the CV: `cv/cv.html`).
2. Run the checker and fix every flagged line:
   `python .claude/skills/humanize/scripts/check_plain.py cv/cv.html`
3. Render the PDF with headless Chrome or Chromium:
   `chrome --headless=new --no-pdf-header-footer --print-to-pdf=cv/Kelechi_Ogbonna_CV.pdf cv/cv.html`
4. Look at the rendered pages. Check for orphaned headings, split sections, and two pages at most.
5. Re-check every number against its source repo before publishing.
