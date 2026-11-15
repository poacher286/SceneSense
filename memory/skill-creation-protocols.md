---
name: skill-creation-protocols
description: "Guidelines for creating skills in SceneSense project"
metadata:
  type: feedback
---

**When creating new skills:**
1. Always use `/superpowers:writing-skills` to create skills
2. Ask user confirmation before creating skills
3. For project-level skills (like SceneSense), create under `.claude/skills/<skill_name>/` within the project directory, NOT in root `.claude/skills/`
4. Each skill must include `SKILL.md` with proper Ponytail frontmatter: `name`, `description`, `homepage`, `license`

**Why:** Keeps project skills isolated and organized under their respective project directories while maintaining compatibility with Ponytail's skill discovery mechanism.

Link: [[test-output-location]]
