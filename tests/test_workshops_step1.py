import copy
import unittest

from hase_lab.workshops.seed import demo_data
from hase_lab.workshops.rules import eligible
from hase_lab.workshops.ranking import ranked
from hase_lab.workshops.service import register as commit


class EligibilityTests(unittest.TestCase):
    def test_eligible_set_excludes_full_and_incompatible_items(self):
        student, items = demo_data()
        self.assertEqual({x.item_id for x in eligible(student, items)}, {"w1", "w2", "w3"})

    def test_domain_restriction_and_capacity(self):
        student, items = demo_data()
        items["w1"].capacity = len(items["w1"].attendees)
        self.assertNotIn("w1", [x.item_id for x in eligible(student, items)])
        self.assertNotIn("w4", [x.item_id for x in eligible(student, items)])

    def test_existing_commitment_is_excluded(self):
        student, items = demo_data()
        student.registrations.append("w2")
        self.assertNotIn("w2", [x.item_id for x in eligible(student, items)])

    def test_filter_does_not_mutate_inputs(self):
        student, items = demo_data()
        before = copy.deepcopy((student, items))
        eligible(student, items)
        self.assertEqual((student, items), before)
