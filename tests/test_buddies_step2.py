import copy
import unittest

from hase_lab.buddies.seed import demo_data
from hase_lab.buddies.rules import eligible
from hase_lab.buddies.ranking import ranked
from hase_lab.buddies.service import join as commit


class RankingTests(unittest.TestCase):
    def test_interest_then_load(self):
        student, items = demo_data()
        items["g1"].capacity = 5
        candidates = [items["g3"], items["g1"], items["g2"]]
        self.assertEqual([x.item_id for x in ranked(student, candidates)], ['g1', 'g2', 'g3'])

    def test_ties_use_id_not_input_order(self):
        student, items = demo_data()
        items["g1"].members.clear()
        result = ranked(student, [items["g2"], items["g1"]])
        self.assertEqual([x.item_id for x in result], ["g1", "g2"])

    def test_ranking_preserves_input_list_and_records(self):
        student, items = demo_data()
        candidates = [items["g3"], items["g1"], items["g2"]]
        before = copy.deepcopy((student, candidates))
        result = ranked(student, candidates)
        self.assertIsNot(result, candidates)
        self.assertEqual((student, candidates), before)

    def test_empty_candidates(self):
        student, _ = demo_data()
        self.assertEqual(ranked(student, []), [])
