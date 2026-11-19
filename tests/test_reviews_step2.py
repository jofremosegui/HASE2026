import copy
import unittest

from hase_lab.reviews.seed import demo_data
from hase_lab.reviews.rules import eligible
from hase_lab.reviews.ranking import ranked
from hase_lab.reviews.service import assign as commit


class RankingTests(unittest.TestCase):
    def test_interest_then_load(self):
        student, items = demo_data()
        # Use fresh demo data.
        candidates = [items["p3"], items["p1"], items["p2"]]
        self.assertEqual([x.item_id for x in ranked(student, candidates)], ['p2', 'p3', 'p1'])

    def test_ties_use_id_not_input_order(self):
        student, items = demo_data()
        items["p1"].reviewers.clear()
        result = ranked(student, [items["p2"], items["p1"]])
        self.assertEqual([x.item_id for x in result], ["p1", "p2"])

    def test_ranking_preserves_input_list_and_records(self):
        student, items = demo_data()
        candidates = [items["p3"], items["p1"], items["p2"]]
        before = copy.deepcopy((student, candidates))
        result = ranked(student, candidates)
        self.assertIsNot(result, candidates)
        self.assertEqual((student, candidates), before)

    def test_empty_candidates(self):
        student, _ = demo_data()
        self.assertEqual(ranked(student, []), [])
