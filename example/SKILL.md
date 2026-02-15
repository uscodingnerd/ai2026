---
name: code-summary
description: >
  Use this skill whenever the user wants to summarize code, explain what code does,
  or generate a structured summary of a code snippet, file, diff, or PR.
  Triggers include: "summarize this code", "use the template to generate a summary",
  "explain this code", "generate a summary for reviewers", "what does this code do",
  "TL;DR this code", or any request to document or describe code changes.
  Always use this skill when code is pasted and a summary or explanation is requested.
---

# Code Summary Skill

When the user provides code and asks for a summary, generate a structured
summary using the exact three-section template below. No extra sections,
no deviation from the format.

---

## Output Template

Always respond using this exact structure:

### TL;DR
[One sentence only. What does this code do at the highest level?]

### Problem
[2–4 sentences. What problem or need does this code address?
What would be missing or broken without it?]

### Solution
[2–4 sentences. How does the code solve the problem?
Name the specific function, class, pattern, or mechanism used.]

---
