---
name: test-runner
description: "Parallel test runner with coverage and JSON reporting for pytest projects"
homepage: https://github.com/SceneSense/SceneSense
license: MIT
---

# Test Runner Skill

Run unit and integration tests in parallel with configurable options.

## Usage

```bash
/test-runner --type unit,integration --format text --coverage
```

## Options

- `--type`: Run "unit", "integration", or "all" (default)
- `--format`: Output as "text" or "json"
- `--timeout`: Timeout in seconds per test suite
- `--coverage`: Enable pytest-cov coverage reporting
- `--parallel`: Number of concurrent test processes

## Example

```bash
# Run all tests with coverage and JSON output
/test-runner --type all --format json --coverage

# Run only integration tests with parallel execution
/test-runner --type integration --parallel 4
```
