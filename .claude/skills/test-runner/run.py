#!/usr/bin/env python
"""Test runner skill for running unit and integration tests in parallel.

Enhanced with:
- CLI argument parsing (--type, --format, --timeout, --coverage)
- pytest-cov integration for code coverage reporting
- JSON output generation for CI/CD pipelines
- Configurable parallel execution per suite or all at once
"""

import argparse
import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Optional


class Args:
    """Command line argument parser."""

    @staticmethod
    def parse() -> dict:
        """Parse command line arguments and return as dictionary."""
        parser = argparse.ArgumentParser(
            description="Run unit and integration tests with parallel execution",
            epilog="Example: python run.py --type unit,integration --format json --coverage"
        )

        # Test type selection
        parser.add_argument(
            "--type", "-t",
            default="all",
            choices=["unit", "integration", "all"],
            help="Test type(s) to run: unit, integration, or all (default)"
        )

        # Output format
        parser.add_argument(
            "--format", "-f",
            default="text",
            choices=["text", "json"],
            help="Output format: text report or json (default: text)"
        )

        # Timeout in seconds
        parser.add_argument(
            "--timeout",
            type=int,
            default=300,
            help="Test timeout in seconds per suite (default: 300)"
        )

        # Coverage options
        parser.add_argument(
            "--coverage", "-c",
            action="store_true",
            default=False,
            help="Enable pytest-cov coverage reporting"
        )

        # Coverage reporter
        parser.add_argument(
            "--cov-report",
            dest="cov_reporter",
            choices=["term", "html", "xml", "json"],
            default="term",
            help="Coverage reporter: term, html, xml, json (default: term)"
        )

        # Coverage config path
        parser.add_argument(
            "--cov-config",
            dest="cov_config_path",
            default=None,
            help="Path to coverage configuration file"
        )

        # JSON output file path
        parser.add_argument(
            "--output-results",
            dest="json_output_path",
            type=str,
            default=None,
            help="Path to save JSON results (e.g., results.json)"
        )

        # Fail fast option
        parser.add_argument(
            "--fail-fast",
            action="store_true",
            default=False,
            help="Stop running tests after first failure in each suite"
        )

        # Verbose output
        parser.add_argument(
            "--verbose", "-v",
            action="store_true",
            default=True,
            help="Show verbose output (default)"
        )

        return vars(parser.parse_args())


class Config:
    """Configuration manager for test runner."""

    @staticmethod
    def load(cli_args: Optional[dict] = None) -> dict:
        """Load configuration from settings.json or CLI arguments."""
        config_path = Path(__file__).parent / "config" / "settings.json"

        try:
            with open(config_path) as f:
                base_config = json.load(f)
        except FileNotFoundError:
            base_config = {
                "timeout_seconds": 300,
                "parallel_execution": True,
                "output_format": "text",
                "json_output_path": None,
                "fail_fast": False,
                "coverage_enabled": False,
                "cov_reporter": "term"
            }

        # CLI args override config file
        if cli_args:
            base_config.update({
                "timeout_seconds": cli_args.get("timeout", base_config["timeout_seconds"]),
                "output_format": cli_args.get("format", base_config["output_format"]),
                "json_output_path": cli_args.get("json_output_path"),
                "fail_fast": cli_args.get("fail_fast", base_config["fail_fast"]),
                "coverage_enabled": cli_args.get("coverage", False),
                "cov_reporter": cli_args.get("cov_reporter", base_config["cov_reporter"])
            })

        return base_config


def build_pytest_command(
    suite_name: str,
    base_dir: Path,
    config: dict,
    args: dict
) -> Optional[list]:
    """Build pytest command with optional coverage flags."""
    tests_config = {
        "unit": ("tests/unit", "-v"),
        "integration": ("tests/integration", "-v")
    }

    if suite_name not in tests_config:
        return None

    suffix = tests_config[suite_name][1]
    tests_dir = tests_config[suite_name][0]

    # Build base command
    cmd = ["python", "-m", "pytest"] + suffix + [str(base_dir / tests_dir)]

    # Add coverage flags if enabled
    if config["coverage_enabled"]:
        cov_opts = []

        # Default coverage config
        cov_config = args.get("cov_config_path") or "app"
        cov_opts.append(f"--cov={cov_config}")

        # Add reporter option (skip term for file output)
        if args.get("cov_reporter") and args["cov_reporter"] != "term":
            cov_opts.append(f"--cov-report={args['cov_reporter']}")

        cmd = cmd + cov_opts

    # Add fail-fast flag
    if config["fail_fast"]:
        cmd.append("--exitfirst")

    return cmd


def run_pytest_suite(
    suite_name: str,
    base_dir: Optional[Path],
    config: Optional[dict],
    args: Optional[dict] = None
) -> dict:
    """Run a single test suite (unit or integration)."""
    if not suite_name:
        return {
            "passed": False,
            "tests_run": 0,
            "duration_s": 0.0,
            "stdout": "",
            "stderr": "No test name provided"
        }

    # Calculate relative path from skills location to project root
    if base_dir is None:
        base_dir = Path(__file__).parent.parent.parent

    cmd = build_pytest_command(suite_name, base_dir, config or {}, args or {})

    if not cmd:
        return {
            "passed": False,
            "tests_run": 0,
            "duration_s": 0.0,
            "stdout": "",
            "stderr": f"Test directory not found for: {suite_name}"
        }

    start_time = time.time()

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=config["timeout_seconds"] if config else 300
        )

        duration_s = time.time() - start_time

        # Parse test count from output
        import re
        test_count = 0
        if result.stdout:
            match = re.search(r"(\d+)\s+passed", result.stdout)
            if match:
                test_count = int(match.group(1))

        return {
            "name": suite_name,
            "passed": result.returncode == 0,
            "tests_run": test_count,
            "duration_s": round(duration_s, 2),
            "stdout": result.stdout[:500] + "\n..." if len(result.stdout) > 500 else result.stdout,
            "stderr": result.stderr[:300] if len(result.stderr) > 300 else result.stderr,
            "returncode": result.returncode
        }

    except subprocess.TimeoutExpired:
        return {
            "name": suite_name,
            "passed": False,
            "tests_run": 0,
            "duration_s": config["timeout_seconds"] if config else 300,
            "stdout": "",
            "stderr": f"Timeout after {(config['timeout_seconds'] if config else 300)}s",
            "returncode": -1
        }

    except Exception as e:
        return {
            "name": suite_name,
            "passed": False,
            "tests_run": 0,
            "duration_s": time.time() - start_time,
            "stdout": "",
            "stderr": f"{type(e).__name__}: {str(e)}",
            "returncode": -1
        }


def run_tests_parallel(suites: list) -> dict:
    """Run selected test suites in parallel."""
    results = {}

    if not suites:
        return results

    # Get config for this call (defaults to project root)
    base_dir = Path(__file__).parent.parent.parent

    if not suites:
        return results

    # Get config for this call (defaults to project root)
    base_dir = Path(__file__).parent.parent.parent

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {}

        # Submit unit tests if requested
        if "unit" in suites:
            futures[executor.submit(run_pytest_suite, "unit", base_dir, None)] = "unit"

        # Submit integration tests if requested and directory exists
        if "integration" in suites and (base_dir / "tests" / "integration").exists():
            futures[executor.submit(run_pytest_suite, "integration", base_dir, None)] = "integration"

        # Process futures as they complete
        for future, suite_name in list(futures.items()):
            try:
                results[suite_name] = future.result()
            except Exception as e:
                results[suite_name] = {
                    "name": suite_name,
                    "passed": False,
                    "tests_run": 0,
                    "duration_s": 0.0,
                    "stdout": "",
                    "stderr": f"Exception: {type(e).__name__}: {str(e)}",
                    "returncode": -1
                }

    return results


def run_tests_sequential(suites: list) -> dict:
    """Run selected test suites sequentially."""
    results = {}

    for suite_name in ["unit", "integration"]:
        if suite_name not in suites:
            continue

        result = run_pytest_suite(suite_name, None, None)
        results[suite_name] = result

    return results


def generate_text_report(results: dict) -> str:
    """Generate formatted text report."""
    lines = []
    lines.append("=" * 60)
    lines.append("TEST RESULTS SUMMARY")
    lines.append("=" * 60)
    lines.append("")

    total_passed = 0
    total_failed = 0

    for suite_name in ["unit", "integration"]:
        if suite_name not in results:
            continue

        result = results[suite_name]
        status_symbol = "✓ PASSED" if result["passed"] else "✗ FAILED"

        lines.append(f"[{status_symbol}] {result['name'].upper()}")
        lines.append(f"    Duration: {result['duration_s']:.2f}s")
        lines.append(f"    Tests run: {result['tests_run']}")

        if not result["passed"]:
            error_preview = result.get("stderr", "")[:200]
            lines.append(f"    Error: {error_preview}" if error_preview else "    Failed")

        if result["passed"]:
            total_passed += result["tests_run"]
        else:
            total_failed += 1

    lines.append("")
    lines.append("=" * 60)

    overall_status = "SUCCESS" if total_failed == 0 else "FAILURE"
    lines.append(f"OVERALL STATUS: {overall_status}")
    lines.append("=" * 60)

    return "\n".join(lines)


def generate_json_report(results: dict, overall_status: str, timestamp: float) -> dict:
    """Generate JSON report for CI/CD."""
    json_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp)),
        "overall_status": overall_status,
        "results": {k: {**v} for k, v in results.items()},
        "summary": {}
    }

    json_data["summary"]["total_passed"] = total_passed
    json_data["summary"]["total_failed"] = total_failed

    # Calculate totals
    total_passed = 0
    total_failed = 0
    for result in results.values():
        if result.get("passed"):
            total_passed += result.get("tests_run", 0)
        else:
            total_failed += 1

    json_data["summary"]["total_passed"] = total_passed
    json_data["summary"]["total_failed"] = total_failed

    return json_data


def main():
    """Main entry point for test runner."""
    args = Args.parse()
    config = Config.load(args)

    # Calculate base directory from skills location
    base_dir = Path(__file__).parent.parent.parent

    print(f"Starting test suite...")
    print(f"Configuration: parallel={config['parallel_execution']}, format={config['output_format']}")
    print(f"Timeout: {config['timeout_seconds']}s, Coverage: {config['coverage_enabled']}")
    print("")

    # Determine which test suites to run
    suites = []
    if args["type"] == "all":
        # Check which test directories exist
        if (base_dir / "tests" / "unit").exists():
            suites.append("unit")
        if (base_dir / "tests" / "integration").exists():
            suites.append("integration")
    elif args["type"] == "unit":
        suites = ["unit"]
    elif args["type"] == "integration":
        suites = ["integration"]

    try:
        # Run tests based on parallel config
        if config["parallel_execution"]:
            results = run_tests_parallel(suites)
        else:
            results = run_tests_sequential(suites)

        # Generate report based on format
        if config["output_format"] == "json":
            json_report = generate_json_report(results, "SUCCESS" if all(r.get("passed") for r in results.values()) else "FAILURE", time.time())

            print(json.dumps(json_report, indent=2))

            # Save to file if specified
            if args["json_output_path"]:
                try:
                    with open(args["json_output_path"], "w") as f:
                        json.dump(json_report, f, indent=2)
                    print(f"\nJSON report saved to: {args['json_output_path']}")
                except Exception as e:
                    print(f"Warning: Could not save JSON report: {e}")

        else:
            text_report = generate_text_report(results)
            print(text_report)

        # Exit with appropriate code
        overall_passed = all(r.get("passed", False) for r in results.values()) if results else True
        sys.exit(0 if overall_passed else 1)

    except KeyboardInterrupt:
        print("\nTest run interrupted.")
        sys.exit(130)


if __name__ == "__main__":
    main()
