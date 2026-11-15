---
name: test-output-location
description: "Standardize test result output locations for SceneSense"
metadata:
  type: feedback
---

**Test Results Storage Rules:**
1. All test outputs (HTML reports, JSON results, markdown summaries) must be stored in `/output` folder within the project
2. For SceneSense project: `C:/Users/poach/IdeaProjects/SceneSense/output/`
3. File naming convention: `<test-type>-<date-time>.html`, `test-report-YYYY-MM-DD.html`
4. Coverage reports go to `/output/htmlcov/`
5. Never store test artifacts in root project directory or git-tracked folders

**Why:** Keeps workspace clean, ensures test results don't get committed to git accidentally, and provides consistent location for CI/CD pipelines.

Link: [[skill-creation-protocols]]
