# Spec-Driven Development Workflow Guide

## Overview

This guide explains how to use **spec-driven development** in the SceneSense project. This approach ensures:

1. **Clear requirements** before implementation
2. **User approval** at each stage
3. **Testable specifications**
4. **Iterative refinement** through review loops

## When to Use Spec-Driven Development

Use this workflow for:
- ✅ New features affecting multiple components
- ✅ Architectural changes or refactors
- ✅ Complex integrations (e.g., new AI model, device driver)
- ✅ Features requiring design documentation

Do NOT use for:
- ❌ Simple bug fixes (use normal dev flow)
- ❌ One-line changes
- ❌ Documentation updates only

## The 5-Step Process

### Step 1: Clarify Requirements (Meets Your Goal #1)

If requirements aren't clear, ask questions before generating the spec.

**Example dialogue:**
```
You: "Add voice command support to the dashboard"
Me: "Questions before I write the spec:
1. What commands should be recognized?
2. Should this work offline or with cloud API?
3. Do you want a specific voice provider?"

You: "Recognize 'open profile', 'change scene', and 'help'. Use on-device Whisper. Voice UI only."
```

### Step 2: Generate Spec Document (Meets Your Goal #2)

I create the spec file in `docs/superpowers/specs/YYYY-MM-DD-topic-design.md`

**What goes in the spec:**
- Functional requirements (acceptance criteria)
- Non-functional requirements (performance, error handling)
- Design decisions and alternatives considered
- Open questions (TBD items)
- Success criteria (tests, metrics)

The spec is written in markdown and shown to you.

### Step 3: You Review the Spec (Meets Your Goal #2)

**How to review:**
1. Read the spec in chat or your file explorer (`docs/superpowers/specs/`)
2. Provide feedback: approve, suggest changes, or reject
3. Don't wait — give feedback immediately

**Example feedback:**
```
"Great start but I want to add:
- Support for TTS responses too, not just UI
- Add timeout handling for slow network calls
- The performance target should be <50ms latency"
```

### Step 4: Update Spec Based on Feedback (Meets Your Goal #3)

I incorporate your feedback and update the spec.

**Iterate until:**
- ✅ All requirements are clear
- ✅ No open questions remain (or they're documented as TBD)
- ✅ You approve the spec

You'll see updated content in chat with a diff or inline changes highlighted.

### Step 5: Approve Plan and Implement (Meets Your Goal #4)

Once you say "spec approved" or "looks good":

1. I commit the final spec to git
2. I invoke `writing-plans` skill
3. It generates detailed implementation plan
4. You approve the implementation approach
5. Implementation begins with TDD (tests first)

## Command Reference

| Command | Purpose |
|---------|---------|
| `/plan` or "Write a spec for X" | Starts brainstorming/spec generation |
| `/code-review --fix` | Reviews and applies code quality fixes |
| `/simplify` | Cleanup/reuse/efficiency improvements |
| `ExitPlanMode` | Ready to implement after approval |
| `EnterPlanMode` | Start planning before implementation |

## Example Workflow Session

```
User: "Add a new AI model that uses vision transformers instead of CLIP"

→ Brainstorming begins
Me: "Questions: Which VT architecture? Should we keep CLIP as fallback?"

User: "Use ViT-B/16, keep CLIP for small models only."

→ Spec generation starts
Me: [writes spec with ViT requirements, keeping CLIP compatibility]
[shows you the spec]

User: "Great, but I want to swap in a pre-trained model and not train from scratch. Also add GPU auto-detection."

Me: [updates spec with new requirements]
[shows updated spec]

User: "Approved"

→ writing-plans invoked
Me: Generates implementation plan (files to create/modify, test strategy)
[shows you the plan]

User: "Looks good"

→ Implementation begins
Me: Write tests first, implement incrementally, verify with pytest
```

## Quality Gates

Before implementing, the spec passes these checks:

- ✅ No "TODO" or "TBD" without notes
- ✅ Requirements are testable (can write acceptance criteria)
- ✅ Design decisions documented with alternatives considered
- ✅ Edge cases covered (error handling, logging needs)
- ✅ You explicitly approved the spec

## Common Mistakes to Avoid

| ❌ Don't | ✅ Do Instead |
|----------|---------------|
| Jump to implementation | Always review spec first |
| Skip requirements clarification | Ask questions before spec generation |
| Make one big change | Break into smaller specs if complex |
| Ignore feedback loops | Iterate on spec until approved |

## Files Created

- `docs/superpowers/specs/YYYY-MM-DD-topic-design.md` - The spec document
- Spec is committed to git after approval
- Implementation files go in standard locations (app/, tests/)

## See Also

- [CLAUDE.md](../../CLAUDE.md) - Project development guidelines
- [ARCHITECTURE](../architecture/) - System design documentation
- `docs/superpowers/specs/TEMPLATE.md` - Spec template
