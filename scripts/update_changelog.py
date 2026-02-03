#!/usr/bin/env python3
"""
Changelog Updater - Auto-update CHANGELOG.md after component creation.

Adds entries for new components with quality metrics.
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional


class ChangelogUpdater:
    """Update CHANGELOG.md with component entries."""

    def __init__(self, changelog_path: str):
        self.path = Path(changelog_path)
        self.content = ""

    def load(self) -> bool:
        """Load existing changelog or create new."""
        if self.path.exists():
            self.content = self.path.read_text(encoding='utf-8')
            return True
        else:
            self.content = self._create_initial()
            return False

    def _create_initial(self) -> str:
        """Create initial changelog structure."""
        return """# Changelog

All notable changes to Ultimate Constructor will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

"""

    def add_component(
        self,
        component_name: str,
        component_type: str,
        score: int,
        metrics: Dict[str, Any] = None
    ) -> None:
        """Add a new component entry."""
        date = datetime.now().strftime("%Y-%m-%d")
        entry = self._format_entry(component_name, component_type, score, metrics, date)

        # Find [Unreleased] section
        unreleased_match = re.search(r'## \[Unreleased\]\n', self.content)
        if unreleased_match:
            insert_pos = unreleased_match.end()

            # Check if ### Added exists under Unreleased
            added_match = re.search(r'### Added\n', self.content[insert_pos:])
            if added_match:
                # Insert after ### Added
                insert_pos += added_match.end()
                self.content = (
                    self.content[:insert_pos] +
                    entry + "\n" +
                    self.content[insert_pos:]
                )
            else:
                # Add ### Added section
                self.content = (
                    self.content[:insert_pos] +
                    "\n### Added\n" + entry + "\n" +
                    self.content[insert_pos:]
                )
        else:
            # No Unreleased section, add one
            self.content += f"\n## [Unreleased]\n\n### Added\n{entry}\n"

    def add_quality_metrics(
        self,
        tester_score: int,
        reviewer_score: int,
        iterations: int
    ) -> None:
        """Add quality metrics section."""
        metrics_entry = f"""
### Quality Metrics
- Tester score: {tester_score}/100
- Reviewer score: {reviewer_score}/100
- Refactor iterations: {iterations}
- First-pass: {"Yes" if iterations == 0 else "No"}
"""

        # Find [Unreleased] section end
        unreleased_match = re.search(r'## \[Unreleased\]\n', self.content)
        if unreleased_match:
            # Find next ## section or end
            next_section = re.search(r'\n## \[', self.content[unreleased_match.end():])
            if next_section:
                insert_pos = unreleased_match.end() + next_section.start()
            else:
                insert_pos = len(self.content)

            # Check if Quality Metrics already exists
            if '### Quality Metrics' not in self.content[unreleased_match.end():insert_pos]:
                self.content = (
                    self.content[:insert_pos] +
                    metrics_entry +
                    self.content[insert_pos:]
                )

    def add_learned_pattern(self, pattern_name: str, pattern_type: str) -> None:
        """Add learned pattern entry."""
        entry = f"- Pattern: {pattern_name} ({pattern_type})\n"

        unreleased_match = re.search(r'## \[Unreleased\]\n', self.content)
        if unreleased_match:
            insert_pos = unreleased_match.end()

            learned_match = re.search(r'### Learned\n', self.content[insert_pos:])
            if learned_match:
                insert_pos += learned_match.end()
                self.content = (
                    self.content[:insert_pos] +
                    entry +
                    self.content[insert_pos:]
                )
            else:
                # Find position before next major section
                next_section = re.search(r'\n## \[', self.content[insert_pos:])
                if next_section:
                    section_pos = insert_pos + next_section.start()
                else:
                    section_pos = len(self.content)

                self.content = (
                    self.content[:section_pos] +
                    f"\n### Learned\n{entry}" +
                    self.content[section_pos:]
                )

    def _format_entry(
        self,
        name: str,
        type: str,
        score: int,
        metrics: Dict[str, Any],
        date: str
    ) -> str:
        """Format a changelog entry."""
        entry = f"- New {type}: {name} (Score: {score}/100)"

        if metrics:
            if 'description' in metrics:
                entry += f"\n  - {metrics['description']}"
            if 'features' in metrics:
                for feature in metrics['features'][:3]:
                    entry += f"\n  - {feature}"

        return entry

    def release_version(self, version: str) -> None:
        """Convert Unreleased to a version."""
        date = datetime.now().strftime("%Y-%m-%d")
        self.content = self.content.replace(
            '## [Unreleased]',
            f'## [Unreleased]\n\n## [{version}] - {date}'
        )

    def save(self) -> None:
        """Save changelog to file."""
        self.path.write_text(self.content, encoding='utf-8')

    def get_content(self) -> str:
        """Get current content."""
        return self.content


def main():
    if len(sys.argv) < 2:
        print("Usage: python update_changelog.py <changelog_path> [--add-component JSON]")
        sys.exit(1)

    changelog_path = sys.argv[1]
    updater = ChangelogUpdater(changelog_path)
    updater.load()

    # Parse additional arguments
    if len(sys.argv) > 2:
        if sys.argv[2] == '--add-component':
            data = json.loads(sys.argv[3])
            updater.add_component(
                data['name'],
                data['type'],
                data.get('score', 0),
                data.get('metrics', {})
            )

            if 'tester_score' in data:
                updater.add_quality_metrics(
                    data['tester_score'],
                    data.get('reviewer_score', 0),
                    data.get('iterations', 0)
                )

            updater.save()
            print(f"Updated changelog: {changelog_path}")

        elif sys.argv[2] == '--add-pattern':
            data = json.loads(sys.argv[3])
            updater.add_learned_pattern(data['name'], data['type'])
            updater.save()
            print(f"Added pattern to changelog: {data['name']}")

        elif sys.argv[2] == '--release':
            version = sys.argv[3]
            updater.release_version(version)
            updater.save()
            print(f"Released version: {version}")

    print(updater.get_content())


if __name__ == '__main__':
    main()
