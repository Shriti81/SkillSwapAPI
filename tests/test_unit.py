import pytest
from schemas import UserCreate
from crud import find_matches

class FakeUser:
    def __init__(self, id, skills_offered, skills_needed):
        self.id = id
        self.skills_offered = skills_offered
        self.skills_needed = skills_needed

def test_match_logic():
    user = FakeUser(1, '["Python"]', '["React"]')
    users = [
        FakeUser(2, '["React"]', '["Python"]'),
        FakeUser(3, '["Java"]', '["C++"]')
    ]
    matches = []
    user_needed = set(["React"])
    user_offered = set(["Python"])
    for u in users:
        offered = set(eval(u.skills_offered))
        needed = set(eval(u.skills_needed))
        if user_needed & offered and user_offered & needed:
            matches.append(u)
    assert len(matches) == 1
