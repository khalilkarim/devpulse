import unittest
from collections import defaultdict
from extract import _group_skills, match_skills_in_text


def test_group_skills():
    matching_skills = [(1,5), (1,4), (2, 5), (2,10)]
    result = _group_skills(matching_skills)
    assert result == {1: [5, 4], 2: [5, 10]}

def test_group_skills_groups_by_posting_id():
    matching_skills = [(1, 5), (1, 8), (2, 5)]
    result = _group_skills(matching_skills)
    assert result == {1: [5, 8], 2: [5]}


def test_finds_java_in_text():
    skills = [(4, "Java"), (5, "Python")]
    result = match_skills_in_text("looking for java engineer", skills)   # ← CALLS it
    assert result == [4]




