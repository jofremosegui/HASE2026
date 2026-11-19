import copy
import unittest

from hase_lab.reviews.seed import demo_data
from hase_lab.reviews.rules import eligible
from hase_lab.reviews.ranking import ranked
from hase_lab.reviews.service import assign as commit


class CommitmentTests(unittest.TestCase):
    def test_success_updates_both_records(self):
        student, items = demo_data()
        self.assertIs(commit(student, items, "p1"), True)
        self.assertEqual(student.assignments, ["p1"])
        self.assertEqual(items["p1"].reviewers, ["s2", "s1"])

    def test_duplicate_rejected_without_changes(self):
        student, items = demo_data()
        student.assignments.append("p1")
        items["p1"].reviewers.append(student.student_id)
        before = copy.deepcopy((student, items))
        self.assertIs(commit(student, items, "p1"), False)
        self.assertEqual((student, items), before)

    def test_second_allowed_third_rejected(self):
        student, items = demo_data()
        student.assignments.append("p1")
        items["p1"].reviewers.append(student.student_id)
        self.assertIs(commit(student, items, "p2"), True)
        before = copy.deepcopy((student, items))
        self.assertIs(commit(student, items, "p3"), False)
        self.assertEqual((student, items), before)

    def test_unknown_full_and_incompatible_are_rejected(self):
        for target in ("missing", "p5", "p4"):
            with self.subTest(target=target):
                student, items = demo_data()
                before = copy.deepcopy((student, items))
                self.assertIs(commit(student, items, target), False)
                self.assertEqual((student, items), before)
