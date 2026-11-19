import copy
import unittest

from hase_lab.buddies.seed import demo_data
from hase_lab.buddies.rules import eligible
from hase_lab.buddies.ranking import ranked
from hase_lab.buddies.service import join as commit


class CommitmentTests(unittest.TestCase):
    def test_success_updates_both_records(self):
        student, items = demo_data()
        self.assertIs(commit(student, items, "g1"), True)
        self.assertEqual(student.memberships, ["g1"])
        self.assertEqual(items["g1"].members, ["s2", "s1"])

    def test_duplicate_rejected_without_changes(self):
        student, items = demo_data()
        student.memberships.append("g1")
        items["g1"].members.append(student.student_id)
        before = copy.deepcopy((student, items))
        self.assertIs(commit(student, items, "g1"), False)
        self.assertEqual((student, items), before)

    def test_second_allowed_third_rejected(self):
        student, items = demo_data()
        student.memberships.append("g1")
        items["g1"].members.append(student.student_id)
        self.assertIs(commit(student, items, "g2"), True)
        before = copy.deepcopy((student, items))
        self.assertIs(commit(student, items, "g3"), False)
        self.assertEqual((student, items), before)

    def test_unknown_full_and_incompatible_are_rejected(self):
        for target in ("missing", "g5", "g4"):
            with self.subTest(target=target):
                student, items = demo_data()
                before = copy.deepcopy((student, items))
                self.assertIs(commit(student, items, target), False)
                self.assertEqual((student, items), before)
