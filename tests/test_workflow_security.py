"""Regression checks for the repository's workflow security boundaries."""

import re
import unittest
from pathlib import Path


WORKFLOWS = Path(__file__).resolve().parents[1] / ".github" / "workflows"


class WorkflowSecurityTests(unittest.TestCase):
    def test_integrity_gate_runs_when_pr_base_changes(self):
        workflow = (WORKFLOWS / "coderabbit-review-integrity.yml").read_text()
        event = re.search(
            r"^  pull_request_target:\n    types: \[([^\]]+)\]",
            workflow,
            re.MULTILINE,
        )
        self.assertIsNotNone(event)
        self.assertIn("edited", {value.strip() for value in event[1].split(",")})

    def test_tests_job_limits_token_to_repository_read(self):
        workflow = (WORKFLOWS / "tests.yml").read_text()
        job = re.search(r"^  unit-tests:\n((?:    .*\n|\n)+)", workflow, re.MULTILINE)
        self.assertIsNotNone(job)
        permissions = re.search(
            r"^    permissions:\n((?:      .*\n)+)", job[1], re.MULTILINE
        )
        self.assertIsNotNone(permissions)
        self.assertEqual(permissions[1].strip(), "contents: read")
