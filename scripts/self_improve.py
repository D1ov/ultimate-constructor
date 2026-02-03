#!/usr/bin/env python3
"""
Self-Improvement Engine - Learn from sessions and improve over time.

Processes extracted patterns and updates knowledge base.
Called by SessionEnd hook.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional


class SelfImprover:
    """Self-improvement engine for Ultimate Constructor."""

    def __init__(self, plugin_root: str = None):
        self.plugin_root = Path(plugin_root or os.environ.get('CLAUDE_PLUGIN_ROOT', '.'))
        self.learned_dir = self.plugin_root / 'learned'
        self.patterns_file = self.learned_dir / 'patterns.json'
        self.stats_file = self.learned_dir / 'stats.json'
        self.improvements_dir = self.learned_dir / 'improvements'

        # Ensure directories exist
        self.learned_dir.mkdir(parents=True, exist_ok=True)
        self.improvements_dir.mkdir(parents=True, exist_ok=True)

    def load_patterns(self) -> Dict[str, Any]:
        """Load existing patterns."""
        if self.patterns_file.exists():
            return json.loads(self.patterns_file.read_text())
        return {"patterns": [], "last_updated": None}

    def save_patterns(self, data: Dict[str, Any]) -> None:
        """Save patterns to file."""
        data["last_updated"] = datetime.now().isoformat()
        self.patterns_file.write_text(json.dumps(data, indent=2))

    def load_stats(self) -> Dict[str, Any]:
        """Load statistics."""
        if self.stats_file.exists():
            return json.loads(self.stats_file.read_text())
        return {
            "total_components": 0,
            "by_type": {},
            "total_patterns": 0,
            "average_score": 0,
            "first_pass_rate": 0,
            "sessions_analyzed": 0
        }

    def save_stats(self, data: Dict[str, Any]) -> None:
        """Save statistics."""
        data["last_updated"] = datetime.now().isoformat()
        self.stats_file.write_text(json.dumps(data, indent=2))

    def add_patterns(self, new_patterns: List[Dict]) -> int:
        """Add new patterns, deduplicating."""
        data = self.load_patterns()
        existing_names = {p['name'] for p in data['patterns']}
        added = 0

        for pattern in new_patterns:
            if pattern['name'] not in existing_names:
                # Add with timestamp
                pattern['added'] = datetime.now().isoformat()
                data['patterns'].append(pattern)
                existing_names.add(pattern['name'])
                added += 1
            else:
                # Update confidence if higher
                for existing in data['patterns']:
                    if existing['name'] == pattern['name']:
                        if pattern.get('confidence', 0) > existing.get('confidence', 0):
                            existing['confidence'] = pattern['confidence']
                            existing['updated'] = datetime.now().isoformat()

        self.save_patterns(data)
        return added

    def update_component_stats(
        self,
        component_type: str,
        score: int,
        first_pass: bool
    ) -> None:
        """Update statistics after component creation."""
        stats = self.load_stats()

        # Update counts
        stats['total_components'] = stats.get('total_components', 0) + 1
        if component_type not in stats['by_type']:
            stats['by_type'][component_type] = {'count': 0, 'total_score': 0}
        stats['by_type'][component_type]['count'] += 1
        stats['by_type'][component_type]['total_score'] += score

        # Update averages
        total_score = sum(t['total_score'] for t in stats['by_type'].values())
        total_count = sum(t['count'] for t in stats['by_type'].values())
        stats['average_score'] = round(total_score / total_count) if total_count > 0 else 0

        # Update first pass rate
        if 'first_pass_count' not in stats:
            stats['first_pass_count'] = 0
        if first_pass:
            stats['first_pass_count'] += 1
        stats['first_pass_rate'] = round(
            stats['first_pass_count'] / stats['total_components'] * 100
        ) / 100 if stats['total_components'] > 0 else 0

        self.save_stats(stats)

    def log_improvement(
        self,
        component: str,
        improvement_type: str,
        details: Dict[str, Any]
    ) -> None:
        """Log an improvement application."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{component}_{improvement_type}.json"
        filepath = self.improvements_dir / filename

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "component": component,
            "type": improvement_type,
            "details": details
        }

        filepath.write_text(json.dumps(log_entry, indent=2))

    def analyze_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a session for learnable content."""
        learnings = {
            "patterns_found": [],
            "improvements_suggested": [],
            "stats_updated": False
        }

        # Check for patterns in session data
        if 'patterns' in session_data:
            added = self.add_patterns(session_data['patterns'])
            learnings['patterns_found'] = session_data['patterns']
            learnings['patterns_added'] = added

        # Update stats if component was created
        if 'component_created' in session_data:
            comp = session_data['component_created']
            self.update_component_stats(
                comp.get('type', 'unknown'),
                comp.get('score', 0),
                comp.get('first_pass', False)
            )
            learnings['stats_updated'] = True

        # Log any improvements that were applied
        if 'improvements_applied' in session_data:
            for improvement in session_data['improvements_applied']:
                self.log_improvement(
                    improvement.get('component', 'unknown'),
                    improvement.get('type', 'unknown'),
                    improvement
                )

        return learnings

    def get_pattern_suggestions(self, context: str) -> List[Dict]:
        """Get relevant patterns for a context."""
        data = self.load_patterns()
        relevant = []

        context_lower = context.lower()
        for pattern in data['patterns']:
            # Check if any triggers match
            triggers = pattern.get('triggers', [])
            if any(t.lower() in context_lower for t in triggers):
                relevant.append(pattern)

        # Sort by confidence
        return sorted(relevant, key=lambda p: -p.get('confidence', 0))

    def prune_low_confidence(self, threshold: int = 50) -> int:
        """Remove patterns below confidence threshold."""
        data = self.load_patterns()
        original_count = len(data['patterns'])

        data['patterns'] = [
            p for p in data['patterns']
            if p.get('confidence', 0) >= threshold
        ]

        removed = original_count - len(data['patterns'])
        if removed > 0:
            self.save_patterns(data)

        return removed

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of learned knowledge."""
        patterns = self.load_patterns()
        stats = self.load_stats()

        # Count patterns by type
        by_type = {}
        for p in patterns['patterns']:
            ptype = p.get('type', 'unknown')
            by_type[ptype] = by_type.get(ptype, 0) + 1

        return {
            "total_patterns": len(patterns['patterns']),
            "patterns_by_type": by_type,
            "high_confidence": len([
                p for p in patterns['patterns']
                if p.get('confidence', 0) >= 80
            ]),
            "total_components": stats.get('total_components', 0),
            "average_score": stats.get('average_score', 0),
            "first_pass_rate": stats.get('first_pass_rate', 0),
            "last_updated": patterns.get('last_updated')
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: python self_improve.py <command> [args]")
        print("\nCommands:")
        print("  analyze <session_json>  - Analyze session for learnings")
        print("  summary                 - Show learning summary")
        print("  suggest <context>       - Get pattern suggestions")
        print("  prune [threshold]       - Remove low-confidence patterns")
        sys.exit(1)

    improver = SelfImprover()
    command = sys.argv[1]

    if command == 'analyze':
        session_data = json.loads(sys.stdin.read() if len(sys.argv) < 3 else sys.argv[2])
        result = improver.analyze_session(session_data)
        print(json.dumps(result, indent=2))

    elif command == 'summary':
        summary = improver.get_summary()
        print(json.dumps(summary, indent=2))

    elif command == 'suggest':
        context = sys.argv[2] if len(sys.argv) > 2 else ""
        suggestions = improver.get_pattern_suggestions(context)
        print(json.dumps(suggestions, indent=2))

    elif command == 'prune':
        threshold = int(sys.argv[2]) if len(sys.argv) > 2 else 50
        removed = improver.prune_low_confidence(threshold)
        print(f"Removed {removed} patterns below {threshold}% confidence")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
