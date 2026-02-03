#!/usr/bin/env python3
"""
Pattern Extractor - Extract reusable patterns from conversation transcripts.

Analyzes conversation for:
- Error → Resolution pairs
- User corrections
- Repeated workflows
- Quality issues
"""

import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Pattern:
    """Extracted pattern from conversation."""
    id: str
    type: str  # workflow, validation, fix, antipattern
    name: str
    description: str
    confidence: int  # 0-100
    source_turns: List[int]
    triggers: List[str]
    suggested_component: str  # skill, agent, hook
    created: str


class PatternExtractor:
    """Extract patterns from conversation transcripts."""

    def __init__(self, transcript_path: str = None):
        self.transcript_path = transcript_path
        self.patterns: List[Pattern] = []
        self.pattern_counter = 0

    def extract_from_transcript(self, transcript: str) -> List[Pattern]:
        """Extract all patterns from transcript text."""
        self.patterns = []

        # Split into turns
        turns = self._parse_turns(transcript)

        # Detect different pattern types
        self._detect_error_resolutions(turns)
        self._detect_user_corrections(turns)
        self._detect_repeated_workflows(turns)
        self._detect_quality_issues(turns)

        return self.patterns

    def _parse_turns(self, transcript: str) -> List[Dict[str, Any]]:
        """Parse transcript into turns."""
        turns = []
        current_turn = {"role": None, "content": "", "index": 0}

        for i, line in enumerate(transcript.split('\n')):
            if line.startswith('Human:') or line.startswith('User:'):
                if current_turn["content"]:
                    turns.append(current_turn)
                current_turn = {"role": "user", "content": line, "index": len(turns)}
            elif line.startswith('Assistant:') or line.startswith('Claude:'):
                if current_turn["content"]:
                    turns.append(current_turn)
                current_turn = {"role": "assistant", "content": line, "index": len(turns)}
            else:
                current_turn["content"] += "\n" + line

        if current_turn["content"]:
            turns.append(current_turn)

        return turns

    def _detect_error_resolutions(self, turns: List[Dict]) -> None:
        """Detect error → resolution patterns."""
        error_patterns = [
            r'error[:\s]',
            r'failed[:\s]',
            r'exception[:\s]',
            r'not found',
            r'invalid',
        ]

        resolution_patterns = [
            r'fix(?:ed)?[:\s]',
            r'solved?[:\s]',
            r'resolv(?:ed)?[:\s]',
            r'work(?:s|ed)?[:\s]',
            r'success',
        ]

        for i, turn in enumerate(turns):
            content_lower = turn["content"].lower()

            # Check for error
            has_error = any(re.search(p, content_lower) for p in error_patterns)
            if not has_error:
                continue

            # Look for resolution in next few turns
            for j in range(i + 1, min(i + 5, len(turns))):
                next_content = turns[j]["content"].lower()
                has_resolution = any(re.search(p, next_content) for p in resolution_patterns)

                if has_resolution:
                    self._add_pattern(
                        type="fix",
                        name=self._generate_name("error-resolution", i),
                        description=f"Error at turn {i} resolved at turn {j}",
                        confidence=75,
                        source_turns=[i, j],
                        triggers=["error", "fix", "resolve"],
                        suggested_component="hook"
                    )
                    break

    def _detect_user_corrections(self, turns: List[Dict]) -> None:
        """Detect when user corrects Claude's approach."""
        correction_patterns = [
            r'no,?\s+(?:actually|instead|rather)',
            r"that's not (?:right|correct|what)",
            r'(?:should|could) (?:be|have been)',
            r'(?:wrong|incorrect)',
            r"don't (?:do|use)",
            r'(?:better|prefer) (?:to|if)',
        ]

        for i, turn in enumerate(turns):
            if turn["role"] != "user":
                continue

            content_lower = turn["content"].lower()
            for pattern in correction_patterns:
                if re.search(pattern, content_lower):
                    self._add_pattern(
                        type="antipattern",
                        name=self._generate_name("user-correction", i),
                        description=f"User corrected approach at turn {i}",
                        confidence=70,
                        source_turns=[i - 1, i] if i > 0 else [i],
                        triggers=["avoid", "don't", "wrong"],
                        suggested_component="skill"
                    )
                    break

    def _detect_repeated_workflows(self, turns: List[Dict]) -> None:
        """Detect repeated tool usage patterns."""
        tool_sequence = []
        tool_pattern = r'(?:Read|Write|Edit|Bash|Grep|Glob)\s*\('

        for turn in turns:
            if turn["role"] != "assistant":
                continue

            tools = re.findall(tool_pattern, turn["content"])
            if tools:
                tool_sequence.append({
                    "turn": turn["index"],
                    "tools": [t.strip('( ') for t in tools]
                })

        # Find repeated sequences
        if len(tool_sequence) >= 3:
            # Simple repetition detection
            sequences = [tuple(s["tools"]) for s in tool_sequence]
            for seq in set(sequences):
                count = sequences.count(seq)
                if count >= 2 and len(seq) >= 2:
                    self._add_pattern(
                        type="workflow",
                        name=self._generate_name("tool-sequence", 0),
                        description=f"Tool sequence {' → '.join(seq)} repeated {count} times",
                        confidence=60 + (count * 10),
                        source_turns=[s["turn"] for s in tool_sequence if tuple(s["tools"]) == seq],
                        triggers=list(seq),
                        suggested_component="skill"
                    )

    def _detect_quality_issues(self, turns: List[Dict]) -> None:
        """Detect quality-related discussions."""
        quality_patterns = [
            (r'missing\s+\w+', "missing content"),
            (r'should (?:have|include)', "incomplete"),
            (r'too (?:long|short|vague)', "content issue"),
            (r'not clear', "clarity issue"),
        ]

        for i, turn in enumerate(turns):
            content_lower = turn["content"].lower()
            for pattern, issue_type in quality_patterns:
                if re.search(pattern, content_lower):
                    self._add_pattern(
                        type="validation",
                        name=self._generate_name(issue_type, i),
                        description=f"Quality issue '{issue_type}' at turn {i}",
                        confidence=65,
                        source_turns=[i],
                        triggers=["validate", "check", "quality"],
                        suggested_component="hook"
                    )
                    break

    def _add_pattern(self, **kwargs) -> None:
        """Add a new pattern."""
        self.pattern_counter += 1
        pattern = Pattern(
            id=f"pat_{datetime.now().strftime('%Y%m%d')}_{self.pattern_counter:03d}",
            created=datetime.now().isoformat(),
            **kwargs
        )
        self.patterns.append(pattern)

    def _generate_name(self, prefix: str, turn: int) -> str:
        """Generate a pattern name."""
        return f"{prefix}-{turn}"

    def to_json(self) -> str:
        """Export patterns as JSON."""
        return json.dumps({
            "extracted": datetime.now().isoformat(),
            "count": len(self.patterns),
            "patterns": [asdict(p) for p in self.patterns]
        }, indent=2)

    def save(self, output_path: str) -> None:
        """Save patterns to file."""
        Path(output_path).write_text(self.to_json())


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        # Read from stdin
        transcript = sys.stdin.read()
    else:
        transcript_path = sys.argv[1]
        transcript = Path(transcript_path).read_text()

    extractor = PatternExtractor()
    patterns = extractor.extract_from_transcript(transcript)

    print(extractor.to_json())

    # Summary
    print(f"\n--- Summary ---", file=sys.stderr)
    print(f"Patterns found: {len(patterns)}", file=sys.stderr)
    by_type = {}
    for p in patterns:
        by_type[p.type] = by_type.get(p.type, 0) + 1
    for t, c in by_type.items():
        print(f"  {t}: {c}", file=sys.stderr)


if __name__ == '__main__':
    main()
