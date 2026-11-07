"""
Automated Test Suite and Edge Case Scenarios.
Verifies:
1. Multi-channel aggregation and timeline ordering
2. Sentiment shift anomaly detection
3. Changelog correlation to code changes
4. Hindsight 4-network retention, recall, and reflection
5. Edge cases: empty text, unusual characters, missing metadata, rapid swings
6. Domain learning and conversational recall
"""

import unittest
from datetime import datetime, timezone
from memory.hindsight_engine import HindsightMemoryEngine
from memory.memory_models import MemoryNetworkType
from agent.feedback_synthesizer import UserFeedbackSynthesizerAgent
from agent.sentiment_analyzer import SentimentShiftTracker
from agent.theme_extractor import ThemeExtractor
from evaluation.benchmark_comparison import BenchmarkComparator

class TestUserFeedbackSynthesizer(unittest.TestCase):
    def setUp(self):
        self.agent = UserFeedbackSynthesizerAgent()
        self.engine = self.agent.memory.embedded_engine

    def test_01_knowledge_base_bootstrapped(self):
        """Verify that World Facts, Entity Summaries, and Experiences are loaded."""
        self.assertGreater(len(self.engine.world_facts), 0, "World Facts should not be empty")
        self.assertGreater(len(self.engine.agent_experiences), 0, "Experiences should not be empty")
        self.assertGreater(len(self.engine.entity_summaries), 0, "Entity Summaries should not be empty")
        self.assertGreater(len(self.engine.evolving_beliefs), 0, "Evolving Beliefs should not be empty")

    def test_02_hindsight_recall_operation(self):
        """Verify multi-network parallel recall and reranking."""
        results = self.engine.recall(query="Okta SSO token disconnect", top_k=5)
        self.assertTrue(len(results) > 0, "Recall should return relevant memories")
        # Ensure highest ranked has positive score
        self.assertGreater(results[0].score, 0.0)
        # Check relevance breakdown exists
        self.assertIn("semantic", results[0].relevance_breakdown)
        self.assertIn("temporal", results[0].relevance_breakdown)

    def test_03_sentiment_anomaly_detection(self):
        """Verify sentiment plunge is accurately detected during Week 3."""
        tracker = SentimentShiftTracker()
        analysis = tracker.analyze_timeseries(self.agent.raw_feedback)
        self.assertIn("daily_trend", analysis)
        self.assertIn("anomalies", analysis)
        # Week 3 should have detected anomalies
        self.assertGreater(len(analysis["anomalies"]), 0)

    def test_04_changelog_correlation(self):
        """Verify feedback is bound to v2.4.0, v2.4.1, and v2.4.2."""
        correlations = self.agent.changelog_correlator.correlate_feedback_with_releases(self.agent.raw_feedback)
        self.assertTrue(any(c["version"] == "v2.4.1" and c["status"] == "REGRESSION" for c in correlations))
        self.assertTrue(any(c["version"] == "v2.4.2" and "RECOVERY" in c["status"] for c in correlations))

    def test_05_evolving_belief_resolution(self):
        """Verify evolving beliefs update and track state correctly."""
        beliefs = self.engine.evolving_beliefs
        self.assertTrue(any("sso" in b.lower() for b in beliefs.keys()))
        self.assertTrue(any("canvas" in b.lower() for b in beliefs.keys()))

    def test_06_edge_case_empty_and_special_characters(self):
        """Handle edge cases: emojis, special symbols, long text, empty metadata."""
        exp_id = "test_edge_001"
        exp = self.engine.retain_experience(
            experience_id=exp_id,
            channel="discord",
            author="tester🔥🚀",
            raw_content="🔥💥🚀 Complex board broke with €100k contract & Unicode: 漢字 and <script>alert(1)</script>",
            sentiment_score=-0.80,
            account_id="acc_acme_corp",
            tags=["edge_case", "unicode"],
        )
        self.assertEqual(exp.experience_id, exp_id)
        # Verify recall handles unicode without crashing
        results = self.engine.recall(query="漢字 alert unicode", top_k=3)
        self.assertTrue(any(r.item_id == exp_id for r in results))

    def test_07_side_by_side_benchmark(self):
        """Verify Before (Stateless) vs After (Hindsight) comparison runs cleanly."""
        comparator = BenchmarkComparator(self.agent)
        res = comparator.run_side_by_side_comparison("Why did enterprise users threaten to cancel?")
        self.assertIn("stateless_rag", res)
        self.assertIn("hindsight_agent", res)
        self.assertIn("comparison_matrix", res)
        self.assertEqual(res["hindsight_agent"]["spotted_causality"], True)
        self.assertEqual(res["stateless_rag"]["spotted_causality"], False)

    def test_08_domain_learning_multi_turn(self):
        """Verify agent records and recalls context from previous PM questions."""
        q1 = "What caused the login issues last week?"
        ans1 = self.agent.query(q1)
        self.assertIn("v2.4.1", ans1["answer"])
        self.assertEqual(len(self.agent.session_history), 1)

        q2 = "What should we build next to prevent this?"
        ans2 = self.agent.query(q2)
        self.assertIn("RBAC", ans2["answer"])
        self.assertEqual(len(self.agent.session_history), 2)

if __name__ == "__main__":
    unittest.main()

