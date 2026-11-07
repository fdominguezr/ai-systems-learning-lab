# SPDX-License-Identifier: MIT
"""Characterization tests: PASS does not mean the toy candidate is safe."""
import unittest
from example import (Case, ORIGINAL_CASES, CHALLENGE_CASES, baseline, candidate,
                     score, known_errors)

class CharacterizationTests(unittest.TestCase):
    def test_challenge_cases_are_distinct_from_original_phrases(self):
        original = {c.text for c in ORIGINAL_CASES}
        challenge = [c.text for c in CHALLENGE_CASES]
        self.assertEqual(len(challenge), len(set(challenge)))
        self.assertTrue(original.isdisjoint(challenge))

    def test_reuse_score_for_synthetic_order_notes(self):
        cases = (
            Case("Pedido entregado", "LISTO"),
            Case("Pedido pendiente", "REVISAR"),
            Case("Pedido entregado pero devuelto", "REVISAR"),
            Case("Pedido enviado", "REVISAR"),
        )
        def classify(text):
            return "LISTO" if text.strip().lower() == "pedido entregado" else "REVISAR"
        self.assertEqual(score(classify, cases), (4, 4))

    def test_original_baseline_2_of_4(self):
        self.assertEqual(score(baseline, ORIGINAL_CASES), (2, 4))

    def test_original_candidate_4_of_4(self):
        self.assertEqual(score(candidate, ORIGINAL_CASES), (4, 4))

    def test_challenge_baseline_1_of_6(self):
        self.assertEqual(score(baseline, CHALLENGE_CASES), (1, 6))

    def test_challenge_candidate_only_3_of_6(self):
        self.assertEqual(score(candidate, CHALLENGE_CASES), (3, 6))

    def test_three_defects_stay_visible(self):
        failures = known_errors()
        self.assertEqual([row[0] for row in failures], [
            "unapproved",
            "Approved, but revoke approval",
            "Approved, but not ready",
        ])
        self.assertTrue(all(expected == "BLOCK" and actual == "ALLOW"
                            for _, expected, actual in failures))

if __name__ == "__main__":
    unittest.main()
