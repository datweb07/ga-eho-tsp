import math
import random
from random import Random

import pytest

from ga_eho_tsp.algorithms.eho.separation import separate
from ga_eho_tsp.domain.objective import validate_route
from ga_eho_tsp.domain.operators import random_permutation


def test_replaces_exact_worst_elephants_and_keeps_others():
    n = 15
    init_rng = Random(7)
    clan = [random_permutation(n, init_rng) for _ in range(6)]
    costs = [120.0, 500.0, 80.0, 350.0, 90.0, 420.0]
    # 2 cá thể tệ nhất nằm ở index 1 (500.0) và index 5 (420.0)

    result = separate(clan, costs, separation_count=2, n=n, rng=Random(42))

    assert len(result) == len(clan)
    for idx in (0, 2, 3, 4):
        assert result[idx] == clan[idx]
    for route in result:
        assert type(route) is tuple
        validate_route(route, n)
    # Với n=15, xác suất random trùng lại đúng tour cũ gần như bằng 0
    assert result[1] != clan[1]
    assert result[5] != clan[5]


def test_separation_count_zero_is_noop_and_does_not_touch_rng():
    clan = [(0, 1, 2, 3), (0, 2, 1, 3), (0, 3, 2, 1)]
    costs = [10.0, 20.0, 30.0]
    rng = Random(123)
    state_before = rng.getstate()

    result = separate(clan, costs, separation_count=0, n=4, rng=rng)

    assert result == clan
    assert result is not clan
    assert rng.getstate() == state_before


def test_separation_count_one_and_full_clan():
    n = 10
    clan = [random_permutation(n, Random(i)) for i in range(5)]
    costs = [50.0, 10.0, 99.0, 20.0, 40.0]

    # separation_count = 1 -> chỉ thay index 2
    res_one = separate(clan, costs, separation_count=1, n=n, rng=Random(99))
    assert len(res_one) == 5
    for idx in (0, 1, 3, 4):
        assert res_one[idx] == clan[idx]
    validate_route(res_one[2], n)
    assert res_one[2] != clan[2]

    # separation_count = nc -> thay toàn bộ clan
    res_all = separate(clan, costs, separation_count=5, n=n, rng=Random(99))
    assert len(res_all) == 5
    for i, route in enumerate(res_all):
        validate_route(route, n)
        assert route != clan[i]


def test_ties_and_all_equal_costs_are_deterministic():
    n = 15
    clan = [random_permutation(n, Random(i)) for i in range(4)]
    costs = [100.0, 100.0, 100.0, 100.0]

    res1 = separate(clan, costs, separation_count=2, n=n, rng=Random(77))
    res2 = separate(clan, costs, separation_count=2, n=n, rng=Random(77))

    assert res1 == res2
    assert len(res1) == 4
    # Tie-break ưu tiên chỉ số nhỏ hơn (0 và 1), giữ nguyên 2 và 3
    assert res1[2] == clan[2]
    assert res1[3] == clan[3]
    for route in res1:
        validate_route(route, n)


@pytest.mark.parametrize("n", [3, 4, 6, 15, 26, 42, 48])
@pytest.mark.parametrize("sep_count", [0, 1, 3, 5])
def test_valid_permutations_and_size_preserved_across_sizes(n, sep_count):
    rng = Random(n * 100 + sep_count)
    clan = [random_permutation(n, rng) for _ in range(5)]
    costs = [float(i * 10 + 1) for i in range(5)]

    result = separate(clan, costs, separation_count=sep_count, n=n, rng=rng)

    assert len(result) == len(clan) == 5
    for route in result:
        assert type(route) is tuple
        validate_route(route, n)


def test_immutability_and_no_global_rng_side_effects():
    global_state_before = random.getstate()

    clan = [[0, 1, 2, 3, 4], [0, 4, 3, 2, 1], [0, 2, 4, 1, 3]]
    costs = [15.0, 45.0, 25.0]
    clan_snapshot = [list(r) for r in clan]
    costs_snapshot = list(costs)

    result = separate(clan, costs, separation_count=2, n=5, rng=Random(11))

    assert clan == clan_snapshot
    assert costs == costs_snapshot
    assert result is not clan
    assert all(type(r) is tuple for r in result)
    assert random.getstate() == global_state_before


def test_reproducibility_with_same_seed():
    n = 48
    clan = [random_permutation(n, Random(i)) for i in range(20)]
    costs = [float(i) for i in range(20)]

    r1 = separate(clan, costs, separation_count=3, n=n, rng=Random(2026))
    r2 = separate(clan, costs, separation_count=3, n=n, rng=Random(2026))
    r3 = separate(clan, costs, separation_count=3, n=n, rng=Random(9999))

    assert r1 == r2
    assert r1 != r3


@pytest.mark.parametrize("bad_count", [-1, 4, 100, True, False, 1.5, "1"])
def test_invalid_separation_count_rejected(bad_count):
    clan = [(0, 1, 2), (0, 2, 1), (0, 1, 2)]
    costs = [1.0, 2.0, 3.0]
    with pytest.raises(ValueError):
        separate(clan, costs, separation_count=bad_count, n=3, rng=Random(1))


def test_invalid_inputs_rejected():
    rng = Random(1)
    valid_clan = [(0, 1, 2), (0, 2, 1)]
    valid_costs = [5.0, 10.0]

    # Clan rỗng
    with pytest.raises(ValueError):
        separate([], [], 0, 3, rng)
    # Sai độ dài clan vs costs
    with pytest.raises(ValueError):
        separate(valid_clan, [5.0], 1, 3, rng)
    # n < 3 hoặc bool
    for bad_n in (0, 2, True, 3.0):
        with pytest.raises(ValueError):
            separate(valid_clan, valid_costs, 1, bad_n, rng)
    # Route không hợp lệ trong clan
    with pytest.raises(ValueError):
        separate([(1, 0, 2), (0, 2, 1)], valid_costs, 1, 3, rng)
    # Cost không hợp lệ
    for bad_cost in (-1.0, math.nan, math.inf, -math.inf, True, "5"):
        with pytest.raises(ValueError):
            separate(valid_clan, [5.0, bad_cost], 1, 3, rng)
    # clan hoặc costs không phải sequence
    with pytest.raises(ValueError):
        separate(None, valid_costs, 1, 3, rng)
    with pytest.raises(ValueError):
        separate(valid_clan, None, 1, 3, rng)
