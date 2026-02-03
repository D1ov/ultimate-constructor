#!/usr/bin/env python3
"""
Self-Test Runner - Execute validation tests for components.

Runs comprehensive tests and outputs results for the tester agent.
"""

import json
import sys
import subprocess
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TestResult:
    name: str
    passed: bool
    message: str
    duration_ms: int


class SelfTestRunner:
    """Run self-tests for components."""

    def __init__(self, component_path: str):
        self.path = Path(component_path)
        self.results: List[TestResult] = []

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all applicable tests."""
        start = datetime.now()

        # Structure tests
        self._test_structure()

        # Content tests
        self._test_content()

        # Quality tests
        self._test_quality()

        duration = (datetime.now() - start).total_seconds() * 1000

        passed = sum(1 for r in self.results if r.passed)
        failed = len(self.results) - passed
        score = int((passed / len(self.results)) * 100) if self.results else 0

        return {
            "test_complete": True,
            "component": str(self.path),
            "timestamp": datetime.now().isoformat(),
            "duration_ms": duration,
            "passed": passed,
            "failed": failed,
            "score": score,
            "results": [
                {
                    "name": r.name,
                    "passed": r.passed,
                    "message": r.message,
                    "duration_ms": r.duration_ms
                }
                for r in self.results
            ]
        }

    def _test_structure(self) -> None:
        """Test component structure."""
        start = datetime.now()

        # Test: Path exists
        exists = self.path.exists()
        self._add_result(
            "path_exists",
            exists,
            f"Path {'exists' if exists else 'not found'}: {self.path}",
            start
        )

        if not exists:
            return

        # Test: Is directory or valid file
        is_valid = self.path.is_dir() or self.path.suffix in ['.md', '.json']
        self._add_result(
            "valid_path_type",
            is_valid,
            f"Path is {'valid' if is_valid else 'invalid'} type",
            start
        )

        # Test: Main file exists (for directories)
        if self.path.is_dir():
            skill_md = self.path / "SKILL.md"
            plugin_json = self.path / ".claude-plugin" / "plugin.json"
            has_main = skill_md.exists() or plugin_json.exists()
            self._add_result(
                "main_file_exists",
                has_main,
                f"Main file {'found' if has_main else 'missing'}",
                start
            )

    def _test_content(self) -> None:
        """Test content validity."""
        start = datetime.now()

        # Find main file
        main_file = self._find_main_file()
        if not main_file:
            return

        content = main_file.read_text(encoding='utf-8')

        # Test: Has frontmatter
        has_frontmatter = content.startswith('---')
        self._add_result(
            "has_frontmatter",
            has_frontmatter,
            f"YAML frontmatter {'present' if has_frontmatter else 'missing'}",
            start
        )

        # Test: Frontmatter valid
        if has_frontmatter:
            try:
                import yaml
                parts = content.split('---', 2)
                yaml.safe_load(parts[1])
                frontmatter_valid = True
            except:
                frontmatter_valid = False

            self._add_result(
                "frontmatter_valid",
                frontmatter_valid,
                f"Frontmatter {'parses' if frontmatter_valid else 'invalid'}",
                start
            )

        # Test: Has name field
        has_name = 'name:' in content[:500]
        self._add_result(
            "has_name_field",
            has_name,
            f"Name field {'present' if has_name else 'missing'}",
            start
        )

        # Test: Has description field
        has_desc = 'description:' in content[:1000]
        self._add_result(
            "has_description_field",
            has_desc,
            f"Description field {'present' if has_desc else 'missing'}",
            start
        )

        # Test: No placeholder text
        placeholders = ['TODO', 'FIXME', 'XXX', '[placeholder]', '{placeholder}']
        has_placeholder = any(p in content for p in placeholders)
        self._add_result(
            "no_placeholders",
            not has_placeholder,
            f"Placeholder text {'found' if has_placeholder else 'not found'}",
            start
        )

    def _test_quality(self) -> None:
        """Test quality indicators."""
        start = datetime.now()

        main_file = self._find_main_file()
        if not main_file:
            return

        content = main_file.read_text(encoding='utf-8')
        content_lower = content.lower()

        # Test: Has triggers
        trigger_indicators = ['use when', 'use for', 'trigger', 'activate']
        has_triggers = any(t in content_lower for t in trigger_indicators)
        self._add_result(
            "has_triggers",
            has_triggers,
            f"Trigger phrases {'found' if has_triggers else 'missing'}",
            start
        )

        # Test: Has boundaries
        boundary_indicators = ['not for', "don't use", 'when not to', 'avoid']
        has_boundaries = any(b in content_lower for b in boundary_indicators)
        self._add_result(
            "has_boundaries",
            has_boundaries,
            f"Boundary section {'found' if has_boundaries else 'missing'}",
            start
        )

        # Test: Has examples
        has_examples = '```' in content and content.count('```') >= 2
        self._add_result(
            "has_examples",
            has_examples,
            f"Code examples {'found' if has_examples else 'missing'}",
            start
        )

        # Test: Line count reasonable
        lines = len(content.split('\n'))
        reasonable = lines < 500
        self._add_result(
            "reasonable_length",
            reasonable,
            f"Line count: {lines} ({'ok' if reasonable else 'too long'})",
            start
        )

        # Test: Third person description
        first_person = ['i ', 'i\'m', 'my ', 'we ', 'our ']
        second_person = ['you ', 'your ', "you're"]
        try:
            import yaml
            parts = content.split('---', 2)
            frontmatter = yaml.safe_load(parts[1])
            desc = frontmatter.get('description', '').lower()
            has_first_second = any(p in desc for p in first_person + second_person)
            self._add_result(
                "third_person_desc",
                not has_first_second,
                f"Description {'uses' if has_first_second else 'avoids'} first/second person",
                start
            )
        except:
            pass

    def _find_main_file(self) -> Path:
        """Find the main content file."""
        if self.path.is_file():
            return self.path
        if (self.path / "SKILL.md").exists():
            return self.path / "SKILL.md"
        # Look for any .md file
        md_files = list(self.path.glob("*.md"))
        if md_files:
            return md_files[0]
        return None

    def _add_result(self, name: str, passed: bool, message: str, start: datetime) -> None:
        """Add a test result."""
        duration = int((datetime.now() - start).total_seconds() * 1000)
        self.results.append(TestResult(name, passed, message, duration))


def main():
    if len(sys.argv) < 2:
        print("Usage: python run_self_tests.py <component_path>")
        sys.exit(1)

    component_path = sys.argv[1]
    runner = SelfTestRunner(component_path)
    results = runner.run_all_tests()

    print(json.dumps(results, indent=2))

    # Exit code based on pass rate
    if results["score"] >= 80:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
