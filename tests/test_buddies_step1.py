import copy
import unittest

from hase_lab.buddies.seed import demo_data
from hase_lab.buddies.rules import eligible
from hase_lab.buddies.ranking import ranked
from hase_lab.buddies.service import join as commit


class EligibilityTests(unittest.TestCase):
    def test_eligible_set_excludes_full_and_incompatible_items(self):
        student, items = demo_data()
        self.assertEqual({x.item_id for x in eligible(student, items)}, {"g1", "g2", "g3", "g6", "g7", "g8"})

    def test_domain_restriction_and_capacity(self):
        student, items = demo_data()
        items["g1"].capacity = len(items["g1"].members)
        self.assertNotIn("g1", [x.item_id for x in eligible(student, items)])
        self.assertNotIn("g4", [x.item_id for x in eligible(student, items)])

    def test_existing_commitment_is_excluded(self):
        student, items = demo_data()
        student.memberships.append("g2")
        self.assertNotIn("g2", [x.item_id for x in eligible(student, items)])

    def test_filter_does_not_mutate_inputs(self):
        student, items = demo_data()
        before = copy.deepcopy((student, items))
        eligible(student, items)
        self.assertEqual((student, items), before)
