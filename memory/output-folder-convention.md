---
name: output-folder-convention
description: "Define /output folder structure for SceneSense test artifacts"
metadata:
  type: feedback
---

**Output Folder Structure:**

```
SceneSense/
├── output/
│   ├── reports/           # All test result HTML files
│   │   └── test-report-YYYY-MM-DD.html
│   ├── coverage/          # Coverage HTML reports
│   │   └── index.html
│   ├── json/              # JSON-formatted test results
│   ├── artifacts/         # Test fixtures, screenshots, etc.
│   └── logs/              # Test execution logs
├── .gitignore             # Ensure /output is ignored
```

**Implementation:**
1. Run `/test-runner` with `--format json` → output to `output/reports/`
2. Coverage reports → `output/coverage/htmlcov/`
3. Always check `.gitignore` contains `/output/`

Link: [[skill-creation-protocols]], [[test-output-location]]
