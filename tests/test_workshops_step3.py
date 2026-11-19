import copy
import unittest

from hase_lab.workshops.seed import demo_data
from hase_lab.workshops.rules import eligible
from hase_lab.workshops.ranking import ranked
from hase_lab.workshops.service import register as commit


class CommitmentTests(unittest.TestCase):
    def test_success_updates_both_records(self):
        student, items = demo_data()
        self.assertIs(commit(student, items, "w1"), True)
        self.assertEqual(student.registrations, ["w1"])
        self.assertEqual(items["w1"].attendees, ["s2", "s1"])

    def test_duplicate_rejected_without_changes(self):
        student, items = demo_data()
        student.registrations.append("w1")
        items["w1"].attendees.append(student.student_id)
        before = copy.deepcopy((student, items))
        self.assertIs(commit(student, items, "w1"), False)
        self.assertEqual((student, items), before)

    def test_second_allowed_third_rejected(self):
        student, items = demo_data()
        student.registrations.append("w1")
        items["w1"].attendees.append(student.student_id)
        self.assertIs(commit(student, items, "w2"), True)
        before = copy.deepcopy((student, items))
        self.assertIs(commit(student, items, "w3"), False)
        self.assertEqual((student, items), before)

    def test_unknown_full_and_incompatible_are_rejected(self):
        for target in ("missing", "w5", "w4"):
            with self.subTest(target=target):
                student, items = demo_data()
                before = copy.deepcopy((student, items))
                self.assertIs(commit(student, items, target), False)
                self.assertEqual((student, items), before)
