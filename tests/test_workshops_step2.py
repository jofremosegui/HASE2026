import copy
import unittest

from hase_lab.workshops.seed import demo_data
from hase_lab.workshops.rules import eligible
from hase_lab.workshops.ranking import ranked
from hase_lab.workshops.service import register as commit


class RankingTests(unittest.TestCase):
    def test_interest_then_load(self):
        student, items = demo_data()
        # Use fresh demo data.
        candidates = [items["w3"], items["w1"], items["w2"]]
        self.assertEqual([x.item_id for x in ranked(student, candidates)], ['w2', 'w1', 'w3'])

    def test_ties_use_id_not_input_order(self):
        student, items = demo_data()
        items["w1"].attendees.clear()
        result = ranked(student, [items["w2"], items["w1"]])
        self.assertEqual([x.item_id for x in result], ["w1", "w2"])

    def test_ranking_preserves_input_list_and_records(self):
        student, items = demo_data()
        candidates = [items["w3"], items["w1"], items["w2"]]
        before = copy.deepcopy((student, candidates))
        result = ranked(student, candidates)
        self.assertIsNot(result, candidates)
        self.assertEqual((student, candidates), before)

    def test_empty_candidates(self):
        student, _ = demo_data()
        self.assertEqual(ranked(student, []), [])
