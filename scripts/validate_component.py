#!/usr/bin/env python3
"""
Component Validator - Validate Claude Code component structure and content.

Validates:
- Skills (SKILL.md)
- Agents (.md files)
- Plugins (plugin.json)
- Hooks (hooks.json)
"""

import json
import re
import sys
import yaml
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


@dataclass
class Issue:
    severity: Severity
    code: str
    message: str
    file: str
    line: Optional[int] = None
    suggestion: Optional[str] = None


class ComponentValidator:
    """Validate Claude Code components."""

    def __init__(self, component_path: str):
        self.path = Path(component_path)
        self.issues: List[Issue] = []
        self.component_type: Optional[str] = None

    def validate(self) -> Tuple[int, List[Issue]]:
        """Run all validations and return score with issues."""
        self._detect_type()

        if self.component_type == "skill":
            self._validate_skill()
        elif self.component_type == "agent":
            self._validate_agent()
        elif self.component_type == "plugin":
            self._validate_plugin()
        elif self.component_type == "hooks":
            self._validate_hooks()
        else:
            self.issues.append(Issue(
                Severity.ERROR,
                "UNKNOWN_TYPE",
                "Could not determine component type",
                str(self.path)
            ))

        return self._calculate_score(), self.issues

    def _detect_type(self) -> None:
        """Detect component type from structure."""
        if self.path.is_file():
            if self.path.suffix == '.json':
                self.component_type = "hooks"
            elif self.path.suffix == '.md':
                self.component_type = "agent"
        elif self.path.is_dir():
            if (self.path / "SKILL.md").exists():
                self.component_type = "skill"
            elif (self.path / ".claude-plugin" / "plugin.json").exists():
                self.component_type = "plugin"
            elif (self.path / "plugin.json").exists():
                self.component_type = "plugin"

    def _validate_skill(self) -> None:
        """Validate skill structure."""
        skill_md = self.path / "SKILL.md"

        if not skill_md.exists():
            self.issues.append(Issue(
                Severity.ERROR, "MISSING_FILE",
                "SKILL.md not found", str(self.path)
            ))
            return

        content = skill_md.read_text(encoding='utf-8')
        self._validate_frontmatter(content, str(skill_md))
        self._validate_skill_content(content, str(skill_md))

    def _validate_agent(self) -> None:
        """Validate agent file."""
        if not self.path.exists():
            self.issues.append(Issue(
                Severity.ERROR, "MISSING_FILE",
                "Agent file not found", str(self.path)
            ))
            return

        content = self.path.read_text(encoding='utf-8')
        self._validate_frontmatter(content, str(self.path))
        self._validate_agent_content(content, str(self.path))

    def _validate_plugin(self) -> None:
        """Validate plugin structure."""
        plugin_json = self.path / ".claude-plugin" / "plugin.json"
        if not plugin_json.exists():
            plugin_json = self.path / "plugin.json"

        if not plugin_json.exists():
            self.issues.append(Issue(
                Severity.ERROR, "MISSING_FILE",
                "plugin.json not found", str(self.path)
            ))
            return

        try:
            manifest = json.loads(plugin_json.read_text())
            self._validate_plugin_manifest(manifest, str(plugin_json))
        except json.JSONDecodeError as e:
            self.issues.append(Issue(
                Severity.ERROR, "INVALID_JSON",
                f"Invalid JSON: {e}", str(plugin_json)
            ))

    def _validate_hooks(self) -> None:
        """Validate hooks configuration."""
        if not self.path.exists():
            self.issues.append(Issue(
                Severity.ERROR, "MISSING_FILE",
                "hooks.json not found", str(self.path)
            ))
            return

        try:
            config = json.loads(self.path.read_text())
            self._validate_hooks_config(config, str(self.path))
        except json.JSONDecodeError as e:
            self.issues.append(Issue(
                Severity.ERROR, "INVALID_JSON",
                f"Invalid JSON: {e}", str(self.path)
            ))

    def _validate_frontmatter(self, content: str, file: str) -> None:
        """Validate YAML frontmatter."""
        if not content.startswith('---'):
            self.issues.append(Issue(
                Severity.ERROR, "MISSING_FRONTMATTER",
                "File must start with YAML frontmatter (---)", file
            ))
            return

        try:
            parts = content.split('---', 2)
            if len(parts) < 3:
                raise ValueError("Incomplete frontmatter")
            frontmatter = yaml.safe_load(parts[1])
        except Exception as e:
            self.issues.append(Issue(
                Severity.ERROR, "INVALID_FRONTMATTER",
                f"Invalid YAML: {e}", file
            ))
            return

        # Required fields
        if 'name' not in frontmatter:
            self.issues.append(Issue(
                Severity.ERROR, "MISSING_NAME",
                "Missing required field: name", file
            ))
        else:
            name = frontmatter['name']
            if not re.match(r'^[a-z0-9-]+$', name):
                self.issues.append(Issue(
                    Severity.ERROR, "INVALID_NAME",
                    f"Name must be lowercase with hyphens: {name}", file,
                    suggestion="Use format: my-component-name"
                ))
            if len(name) > 64:
                self.issues.append(Issue(
                    Severity.ERROR, "NAME_TOO_LONG",
                    f"Name exceeds 64 characters: {len(name)}", file
                ))

        if 'description' not in frontmatter:
            self.issues.append(Issue(
                Severity.ERROR, "MISSING_DESCRIPTION",
                "Missing required field: description", file
            ))
        else:
            desc = frontmatter['description']
            if len(desc) > 1024:
                self.issues.append(Issue(
                    Severity.ERROR, "DESC_TOO_LONG",
                    f"Description exceeds 1024 characters: {len(desc)}", file
                ))
            if len(desc) < 20:
                self.issues.append(Issue(
                    Severity.WARNING, "DESC_TOO_SHORT",
                    "Description should be more detailed", file,
                    suggestion="Include what, when to use, and boundaries"
                ))

    def _validate_skill_content(self, content: str, file: str) -> None:
        """Validate skill-specific content."""
        lines = content.split('\n')

        # Line count
        if len(lines) > 500:
            self.issues.append(Issue(
                Severity.WARNING, "TOO_LONG",
                f"SKILL.md is {len(lines)} lines (max 500)", file,
                suggestion="Move detailed content to references/"
            ))

        # Check for boundaries
        content_lower = content.lower()
        if 'not for' not in content_lower and "don't" not in content_lower:
            self.issues.append(Issue(
                Severity.WARNING, "MISSING_BOUNDARIES",
                "No boundaries section found", file,
                suggestion="Add 'NOT for:' or 'When NOT to Use' section"
            ))

        # Check for examples
        if '```' not in content or content.count('```') < 2:
            self.issues.append(Issue(
                Severity.INFO, "MISSING_EXAMPLES",
                "No code examples found", file,
                suggestion="Add working examples in code blocks"
            ))

    def _validate_agent_content(self, content: str, file: str) -> None:
        """Validate agent-specific content."""
        try:
            parts = content.split('---', 2)
            frontmatter = yaml.safe_load(parts[1])
        except:
            return

        # Check for tools field
        if 'tools' not in frontmatter:
            self.issues.append(Issue(
                Severity.INFO, "NO_TOOLS",
                "No tools specified (will inherit all)", file
            ))

        # Check for model
        if 'model' not in frontmatter:
            self.issues.append(Issue(
                Severity.INFO, "NO_MODEL",
                "No model specified (will inherit)", file
            ))

    def _validate_plugin_manifest(self, manifest: Dict, file: str) -> None:
        """Validate plugin manifest."""
        required = ['name', 'version', 'description']
        for field in required:
            if field not in manifest:
                self.issues.append(Issue(
                    Severity.ERROR, f"MISSING_{field.upper()}",
                    f"Missing required field: {field}", file
                ))

        # Version format
        if 'version' in manifest:
            if not re.match(r'^\d+\.\d+\.\d+', manifest['version']):
                self.issues.append(Issue(
                    Severity.ERROR, "INVALID_VERSION",
                    "Version must be semantic (e.g., 1.0.0)", file
                ))

    def _validate_hooks_config(self, config: Dict, file: str) -> None:
        """Validate hooks configuration."""
        if 'hooks' not in config:
            self.issues.append(Issue(
                Severity.ERROR, "MISSING_HOOKS",
                "Missing 'hooks' wrapper object", file,
                suggestion="Plugin hooks.json requires {\"hooks\": {...}}"
            ))
            return

        valid_events = [
            'PreToolUse', 'PostToolUse', 'Stop', 'SubagentStop',
            'UserPromptSubmit', 'SessionStart', 'SessionEnd',
            'PreCompact', 'Notification'
        ]

        for event in config['hooks']:
            if event not in valid_events:
                self.issues.append(Issue(
                    Severity.WARNING, "UNKNOWN_EVENT",
                    f"Unknown hook event: {event}", file
                ))

    def _calculate_score(self) -> int:
        """Calculate validation score."""
        score = 100
        for issue in self.issues:
            if issue.severity == Severity.ERROR:
                score -= 20
            elif issue.severity == Severity.WARNING:
                score -= 5
            elif issue.severity == Severity.INFO:
                score -= 1
        return max(0, score)


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_component.py <component_path>")
        sys.exit(1)

    component_path = sys.argv[1]
    validator = ComponentValidator(component_path)
    score, issues = validator.validate()

    # Output results
    result = {
        "component": component_path,
        "type": validator.component_type,
        "score": score,
        "issues": [
            {
                "severity": i.severity.value,
                "code": i.code,
                "message": i.message,
                "file": i.file,
                "line": i.line,
                "suggestion": i.suggestion
            }
            for i in issues
        ]
    }

    print(json.dumps(result, indent=2))

    # Summary to stderr
    errors = sum(1 for i in issues if i.severity == Severity.ERROR)
    warnings = sum(1 for i in issues if i.severity == Severity.WARNING)
    print(f"\nScore: {score}/100", file=sys.stderr)
    print(f"Errors: {errors}, Warnings: {warnings}", file=sys.stderr)

    sys.exit(0 if errors == 0 else 1)


if __name__ == '__main__':
    main()
