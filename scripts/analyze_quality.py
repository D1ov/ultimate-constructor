#!/usr/bin/env python3
"""
Quality Analyzer - Deep quality analysis for components.

Analyzes against quality criteria and provides detailed scoring.
Used by the constructor-reviewer agent.
"""

import json
import re
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass


@dataclass
class QualityCriterion:
    name: str
    weight: int
    score: int
    max_score: int
    findings: List[str]
    suggestions: List[str]


class QualityAnalyzer:
    """Analyze component quality against criteria."""

    CRITERIA_WEIGHTS = {
        "trigger_specificity": 20,
        "progressive_disclosure": 15,
        "boundaries_clarity": 15,
        "antipattern_awareness": 15,
        "resource_organization": 10,
        "writing_style": 10,
        "examples_quality": 10,
        "documentation": 5
    }

    def __init__(self, component_path: str):
        self.path = Path(component_path)
        self.criteria: Dict[str, QualityCriterion] = {}
        self.content = ""
        self.frontmatter = {}

    def analyze(self) -> Dict[str, Any]:
        """Run full quality analysis."""
        self._load_content()

        # Analyze each criterion
        self._analyze_trigger_specificity()
        self._analyze_progressive_disclosure()
        self._analyze_boundaries()
        self._analyze_antipatterns()
        self._analyze_organization()
        self._analyze_writing_style()
        self._analyze_examples()
        self._analyze_documentation()

        # Calculate totals
        total_score = sum(c.score for c in self.criteria.values())
        max_possible = sum(c.max_score for c in self.criteria.values())

        return {
            "analysis_complete": True,
            "component": str(self.path),
            "total_score": total_score,
            "max_possible": max_possible,
            "percentage": round((total_score / max_possible) * 100) if max_possible > 0 else 0,
            "criteria": {
                name: {
                    "score": c.score,
                    "max": c.max_score,
                    "weight": c.weight,
                    "findings": c.findings,
                    "suggestions": c.suggestions
                }
                for name, c in self.criteria.items()
            },
            "strengths": self._get_strengths(),
            "improvements": self._get_improvements(),
            "recommendation": self._get_recommendation(total_score)
        }

    def _load_content(self) -> None:
        """Load component content."""
        main_file = self._find_main_file()
        if not main_file:
            return

        self.content = main_file.read_text(encoding='utf-8')

        try:
            parts = self.content.split('---', 2)
            self.frontmatter = yaml.safe_load(parts[1]) or {}
        except:
            self.frontmatter = {}

    def _find_main_file(self) -> Path:
        """Find main content file."""
        if self.path.is_file():
            return self.path
        if (self.path / "SKILL.md").exists():
            return self.path / "SKILL.md"
        md_files = list(self.path.glob("*.md"))
        return md_files[0] if md_files else None

    def _analyze_trigger_specificity(self) -> None:
        """Analyze trigger phrase quality."""
        weight = self.CRITERIA_WEIGHTS["trigger_specificity"]
        findings = []
        suggestions = []

        desc = self.frontmatter.get('description', '')

        # Count trigger indicators
        trigger_patterns = [
            r'use when',
            r'use for',
            r'when user (?:mentions?|asks?|wants?)',
            r'"[^"]+?"',  # Quoted phrases
        ]

        trigger_count = 0
        for pattern in trigger_patterns:
            matches = re.findall(pattern, desc.lower())
            trigger_count += len(matches)

        # Score based on trigger count
        if trigger_count >= 5:
            score = weight
            findings.append(f"Excellent: {trigger_count} trigger phrases found")
        elif trigger_count >= 3:
            score = int(weight * 0.75)
            findings.append(f"Good: {trigger_count} trigger phrases")
            suggestions.append("Consider adding 2 more trigger phrases")
        elif trigger_count >= 1:
            score = int(weight * 0.5)
            findings.append(f"Fair: Only {trigger_count} trigger phrase(s)")
            suggestions.append("Add specific phrases like: 'Use when user mentions X, Y, Z'")
        else:
            score = 0
            findings.append("No trigger phrases found")
            suggestions.append("Add trigger phrases: 'Use when user mentions \"phrase1\", \"phrase2\"'")

        self.criteria["trigger_specificity"] = QualityCriterion(
            "Trigger Specificity", weight, score, weight, findings, suggestions
        )

    def _analyze_progressive_disclosure(self) -> None:
        """Analyze content layering."""
        weight = self.CRITERIA_WEIGHTS["progressive_disclosure"]
        findings = []
        suggestions = []

        lines = len(self.content.split('\n'))
        has_references = 'references/' in self.content or '/references/' in self.content

        if lines <= 300:
            score = weight
            findings.append(f"Excellent: {lines} lines (well under 500)")
        elif lines <= 500:
            if has_references:
                score = int(weight * 0.9)
                findings.append(f"Good: {lines} lines with references")
            else:
                score = int(weight * 0.7)
                findings.append(f"Fair: {lines} lines")
                suggestions.append("Consider splitting details into references/")
        else:
            if has_references:
                score = int(weight * 0.5)
                findings.append(f"Long: {lines} lines but has references")
            else:
                score = int(weight * 0.3)
                findings.append(f"Too long: {lines} lines without references")
                suggestions.append("Split detailed content into references/ directory")

        self.criteria["progressive_disclosure"] = QualityCriterion(
            "Progressive Disclosure", weight, score, weight, findings, suggestions
        )

    def _analyze_boundaries(self) -> None:
        """Analyze boundary clarity."""
        weight = self.CRITERIA_WEIGHTS["boundaries_clarity"]
        findings = []
        suggestions = []

        content_lower = self.content.lower()
        desc_lower = self.frontmatter.get('description', '').lower()

        has_not_for = 'not for' in desc_lower or 'not for' in content_lower
        has_dont = "don't" in content_lower or "do not" in content_lower
        has_avoid = 'avoid' in content_lower
        has_section = '## when not' in content_lower or "## don't" in content_lower

        boundary_count = sum([has_not_for, has_dont, has_avoid, has_section])

        if has_section and has_not_for:
            score = weight
            findings.append("Excellent: Clear boundary section and description")
        elif boundary_count >= 2:
            score = int(weight * 0.7)
            findings.append("Good: Multiple boundary indicators")
            if not has_section:
                suggestions.append("Add dedicated '## When NOT to Use' section")
        elif boundary_count >= 1:
            score = int(weight * 0.5)
            findings.append("Fair: Some boundary indication")
            suggestions.append("Add clear DO/DON'T sections")
        else:
            score = 0
            findings.append("Missing: No boundary guidance found")
            suggestions.append("Add 'NOT for:' in description and '## When NOT to Use' section")

        self.criteria["boundaries_clarity"] = QualityCriterion(
            "Boundaries Clarity", weight, score, weight, findings, suggestions
        )

    def _analyze_antipatterns(self) -> None:
        """Analyze antipattern documentation."""
        weight = self.CRITERIA_WEIGHTS["antipattern_awareness"]
        findings = []
        suggestions = []

        content_lower = self.content.lower()

        antipattern_indicators = [
            'anti-pattern', 'antipattern', 'common mistake',
            'wrong', 'incorrect', 'deprecated', '❌'
        ]

        found = [i for i in antipattern_indicators if i in content_lower]

        if len(found) >= 3:
            score = weight
            findings.append(f"Excellent: {len(found)} antipattern indicators")
        elif len(found) >= 1:
            score = int(weight * 0.6)
            findings.append(f"Fair: Some antipattern guidance ({', '.join(found)})")
            suggestions.append("Add dedicated '## Common Mistakes' section")
        else:
            score = 0
            findings.append("Missing: No antipattern documentation")
            suggestions.append("Document common mistakes and what to avoid")

        self.criteria["antipattern_awareness"] = QualityCriterion(
            "Antipattern Awareness", weight, score, weight, findings, suggestions
        )

    def _analyze_organization(self) -> None:
        """Analyze resource organization."""
        weight = self.CRITERIA_WEIGHTS["resource_organization"]
        findings = []
        suggestions = []

        if self.path.is_file():
            score = int(weight * 0.7)
            findings.append("Single file component")
        else:
            has_scripts = (self.path / "scripts").exists()
            has_refs = (self.path / "references").exists()

            if has_scripts and has_refs:
                score = weight
                findings.append("Excellent: scripts/ and references/ directories")
            elif has_scripts or has_refs:
                score = int(weight * 0.7)
                findings.append("Good: Has some organization")
                if not has_refs:
                    suggestions.append("Consider adding references/ for detailed docs")
            else:
                score = int(weight * 0.5)
                findings.append("Basic: Flat structure")
                suggestions.append("Add scripts/ and/or references/ directories")

        self.criteria["resource_organization"] = QualityCriterion(
            "Resource Organization", weight, score, weight, findings, suggestions
        )

    def _analyze_writing_style(self) -> None:
        """Analyze writing style."""
        weight = self.CRITERIA_WEIGHTS["writing_style"]
        findings = []
        suggestions = []

        desc = self.frontmatter.get('description', '')

        # Check for first/second person in description
        first_second = re.findall(r'\b(i|you|your|my|we|our)\b', desc.lower())

        # Check for imperative voice in body
        body = self.content.split('---', 2)[-1] if '---' in self.content else self.content
        imperative_indicators = ['create', 'run', 'check', 'use', 'add', 'configure']
        has_imperative = any(i in body.lower()[:500] for i in imperative_indicators)

        if not first_second and has_imperative:
            score = weight
            findings.append("Excellent: Third person, imperative style")
        elif not first_second:
            score = int(weight * 0.8)
            findings.append("Good: Third person description")
            suggestions.append("Use more imperative verbs in body")
        elif has_imperative:
            score = int(weight * 0.5)
            findings.append("Fair: Has imperative voice but uses I/you")
            suggestions.append(f"Remove first/second person from description: {first_second}")
        else:
            score = int(weight * 0.3)
            findings.append("Needs work: Style issues")
            suggestions.append("Use third person, imperative style")

        self.criteria["writing_style"] = QualityCriterion(
            "Writing Style", weight, score, weight, findings, suggestions
        )

    def _analyze_examples(self) -> None:
        """Analyze example quality."""
        weight = self.CRITERIA_WEIGHTS["examples_quality"]
        findings = []
        suggestions = []

        code_blocks = self.content.count('```')
        example_count = code_blocks // 2  # Each example has opening and closing

        if example_count >= 3:
            score = weight
            findings.append(f"Excellent: {example_count} code examples")
        elif example_count >= 2:
            score = int(weight * 0.7)
            findings.append(f"Good: {example_count} examples")
            suggestions.append("Consider adding 1 more example")
        elif example_count >= 1:
            score = int(weight * 0.5)
            findings.append("Fair: 1 example found")
            suggestions.append("Add 2 more working examples")
        else:
            score = 0
            findings.append("Missing: No code examples")
            suggestions.append("Add working examples in code blocks")

        self.criteria["examples_quality"] = QualityCriterion(
            "Examples Quality", weight, score, weight, findings, suggestions
        )

    def _analyze_documentation(self) -> None:
        """Analyze documentation presence."""
        weight = self.CRITERIA_WEIGHTS["documentation"]
        findings = []
        suggestions = []

        has_readme = (self.path / "README.md").exists() if self.path.is_dir() else False
        has_headers = self.content.count('## ') >= 3

        if has_readme and has_headers:
            score = weight
            findings.append("Excellent: README and structured content")
        elif has_headers:
            score = int(weight * 0.7)
            findings.append("Good: Structured sections")
        else:
            score = int(weight * 0.4)
            findings.append("Basic: Minimal structure")
            suggestions.append("Add more section headers for organization")

        self.criteria["documentation"] = QualityCriterion(
            "Documentation", weight, score, weight, findings, suggestions
        )

    def _get_strengths(self) -> List[str]:
        """Get list of strengths."""
        strengths = []
        for name, criterion in self.criteria.items():
            if criterion.score >= criterion.max_score * 0.8:
                strengths.append(f"{criterion.name}: {criterion.findings[0]}")
        return strengths

    def _get_improvements(self) -> List[Dict]:
        """Get prioritized improvements."""
        improvements = []
        for name, criterion in self.criteria.items():
            if criterion.suggestions:
                priority = "HIGH" if criterion.score < criterion.max_score * 0.5 else "MEDIUM"
                improvements.append({
                    "area": name,
                    "priority": priority,
                    "current_score": criterion.score,
                    "max_score": criterion.max_score,
                    "suggestions": criterion.suggestions,
                    "expected_gain": criterion.max_score - criterion.score
                })
        return sorted(improvements, key=lambda x: -x["expected_gain"])

    def _get_recommendation(self, score: int) -> str:
        """Get recommendation based on score."""
        percentage = (score / 100) * 100
        if percentage >= 80:
            return "approve"
        elif percentage >= 60:
            return "refactor"
        else:
            return "redesign"


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_quality.py <component_path>")
        sys.exit(1)

    component_path = sys.argv[1]
    analyzer = QualityAnalyzer(component_path)
    results = analyzer.analyze()

    print(json.dumps(results, indent=2))

    # Summary
    print(f"\nScore: {results['percentage']}%", file=sys.stderr)
    print(f"Recommendation: {results['recommendation']}", file=sys.stderr)


if __name__ == '__main__':
    main()
