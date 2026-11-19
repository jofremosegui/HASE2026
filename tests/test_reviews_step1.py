import copy
import unittest

from hase_lab.reviews.seed import demo_data
from hase_lab.reviews.rules import eligible
from hase_lab.reviews.ranking import ranked
from hase_lab.reviews.service import assign as commit


class EligibilityTests(unittest.TestCase):
    def test_eligible_set_excludes_full_and_incompatible_items(self):
        student, items = demo_data()
        self.assertEqual({x.item_id for x in eligible(student, items)}, {"p1", "p2", "p3"})

    def test_domain_restriction_and_capacity(self):
        student, items = demo_data()
        items["p1"].capacity = len(items["p1"].reviewers)
        self.assertNotIn("p1", [x.item_id for x in eligible(student, items)])
        self.assertNotIn("p4", [x.item_id for x in eligible(student, items)])

    def test_existing_commitment_is_excluded(self):
        student, items = demo_data()
        student.assignments.append("p2")
        self.assertNotIn("p2", [x.item_id for x in eligible(student, items)])

    def test_filter_does_not_mutate_inputs(self):
        student, items = demo_data()
        before = copy.deepcopy((student, items))
        eligible(student, items)
        self.assertEqual((student, items), before)
