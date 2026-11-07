# SPDX-License-Identifier: MIT
"""Toy deterministic rules for teaching test leakage and adversarial examples.
NOT an LLM, permission engine, authorization system or security control.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Case:
    text: str
    expected: str

ORIGINAL_CASES = (
    Case("Approved for sandbox demo", "ALLOW"),
    Case("Not approved for sandbox demo", "BLOCK"),
    Case("Approval still pending", "BLOCK"),
    Case("Approved for sandbox demo after review", "ALLOW"),
)
# Reviewer-written challenge cases. These are NOT independent random holdout data.
CHALLENGE_CASES = (
    Case("unapproved", "BLOCK"),
    Case("Approved, but revoke approval", "BLOCK"),
    Case("Approved, but not ready", "BLOCK"),
    Case("Not approved for demo", "BLOCK"),
    Case("Review pending for next week", "BLOCK"),
    Case("Approved for an event handout", "ALLOW"),
)

def baseline(_: str) -> str:
    return "ALLOW"

def candidate(text: str) -> str:
    lower = text.lower()
    if "not approved" in lower or "pending" in lower:
        return "BLOCK"
    return "ALLOW" if "approved" in lower else "BLOCK"

def score(fn, cases) -> tuple[int, int]:
    return sum(fn(case.text) == case.expected for case in cases), len(cases)

def known_errors():
    return [(case.text, case.expected, candidate(case.text))
            for case in CHALLENGE_CASES if candidate(case.text) != case.expected]

if __name__ == "__main__":
    print("ORIGINAL_BASELINE", score(baseline, ORIGINAL_CASES))
    print("ORIGINAL_CANDIDATE", score(candidate, ORIGINAL_CASES))
    print("CHALLENGE_BASELINE", score(baseline, CHALLENGE_CASES))
    print("CHALLENGE_CANDIDATE", score(candidate, CHALLENGE_CASES))
    print("KNOWN_ERRORS", known_errors())
