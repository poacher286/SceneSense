# test-runner

A skill for running unit and integration tests in parallel with aggregated reporting.

## Usage Examples

### Run all tests (default)
```bash
python .claude/skills/test-runner/run.py
```

### Run specific test type
```bash
python .claude/skills/test-runner/run.py --type unit    # Run only unit tests
python .claude/skills/test-runner/run.py --type integration  # Run only integration tests
```

### Generate JSON report
```bash
python .claude/skills/test-runner/run.py --format json --output-results results.json
```

### Enable code coverage
```bash
python .claude/skills/test-runner/run.py --coverage --cov-report=html
```

### Custom timeout
```bash
python .claude/skills/test-runner/run.py --timeout 600
```

## Features

- **CLI Argument Parsing**: `--type`, `--format`, `--timeout`, `--coverage` options
- **Parallel Execution**: Runs unit and integration tests concurrently by default
- **pytest-cov Integration**: Code coverage reporting with multiple output formats (html, xml, json)
- **JSON Output Generation**: Generate reports.json for CI/CD pipelines
- **Configurable Options**: Timeout, parallel execution, fail-fast modes in settings.json
- **Graceful Error Handling**: Partial results on partial failures

## Configuration

Edit `config/settings.json` to customize defaults:
```json
{
  "timeout_seconds": 300,
  "parallel_execution": true,
  "output_format": "text",
  "coverage_enabled": false,
  "cov_reporter": "term"
}
```

## Exit Codes

- `0`: All tests passed
- `1`: One or more tests failed
- `130`: Interrupted (Ctrl+C)

## Cleanup Notes

This skill replaces older implementations that lacked:
- CLI argument support
- Coverage reporting capabilities  
- JSON output for automation
