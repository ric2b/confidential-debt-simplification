from collections import defaultdict

from .services import simplify_debt


# TODO: add WAY more tests here

class TestSimplifyDebt:
    def test_basic_update_total(self):
        prev_totals = defaultdict(int)
        uome_list = [['A', 'B', 5], ['B', 'A', 2], ['B', 'C', 1], ['C', 'A', 4]]

        new_totals, simplified_debt = simplify_debt.update_total_debt(prev_totals, uome_list)

        assert new_totals == {'B': 2, 'A': 1, 'C': -3}
        assert simplified_debt == {'C': {'B': 2, 'A': 1}}
