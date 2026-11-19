import math
import random
from random import Random

import pytest

from ga_eho_tsp.algorithms.eho.discrete_ops import (
    hamming_distance,
    move_toward_best,
    update_matriarch,
)
from ga_eho_tsp.domain.objective import validate_route
from ga_eho_tsp.domain.operators import random_permutation


def test_hamming_distance_properties():
    a = (0, 1, 2, 3, 4)
    b = (0, 1, 4, 3, 2)
    c = (0, 2, 3, 4, 1)
    assert hamming_distance(a, a) == 0
    assert hamming_distance(a, b) == 2
    assert hamming_distance(b, a) == 2
    assert hamming_distance(a, c) == 4


@pytest.mark.parametrize("n", [3, 4, 6, 15, 26, 42, 48])
@pytest.mark.parametrize("strength", [0.0, 0.25, 0.5, 0.7, 0.99, 1.0])
def test_move_and_update_valid_permutations_across_sizes(n, strength):
    for seed in range(15):
        rng = Random(seed)
        current = random_permutation(n, rng)
        pbest = random_permutation(n, rng)
        center = random_permutation(n, rng)

        moved = move_toward_best(current, pbest, strength, rng)
        updated = update_matriarch(pbest, center, strength, rng)

        assert type(moved) is tuple
        assert type(updated) is tuple
        validate_route(moved, n)
        validate_route(updated, n)
        # Guided swaps không bao giờ làm tăng khoảng cách Hamming tới đích
        assert hamming_distance(moved, pbest) <= hamming_distance(current, pbest)
        assert hamming_distance(updated, center) <= hamming_distance(pbest, center)


def test_edge_cases_boundaries():
    rng = Random(42)
    current = (0, 1, 2, 3, 4, 5)
    pbest = (0, 5, 4, 3, 2, 1)

    # alpha = 0 -> không đổi
    assert move_toward_best(current, pbest, 0.0, rng) == current
    assert move_toward_best(current, pbest, 0, rng) == current
    # alpha = 1 -> trở thành pbest
    assert move_toward_best(current, pbest, 1.0, rng) == pbest
    assert move_toward_best(current, pbest, 1, rng) == pbest
    # current == pbest -> no-op với mọi alpha
    for a in (0.0, 0.3, 0.7, 1.0):
        assert move_toward_best(current, current, a, rng) == current

    # beta = 0 / 1 và matriarch == clan_center
    assert update_matriarch(pbest, current, 0.0, rng) == pbest
    assert update_matriarch(pbest, current, 1.0, rng) == current
    for b in (0.0, 0.3, 0.7, 1.0):
        assert update_matriarch(pbest, pbest, b, rng) == pbest


def test_minimum_tsp_n3():
    a = (0, 1, 2)
    b = (0, 2, 1)
    assert hamming_distance(a, b) == 2
    assert move_toward_best(a, b, 0.0, Random(0)) == a
    assert move_toward_best(a, b, 1.0, Random(0)) == b
    assert update_matriarch(a, b, 0.0, Random(0)) == a
    assert update_matriarch(a, b, 1.0, Random(0)) == b

    seen = set()
    for seed in range(50):
        out = move_toward_best(a, b, 0.7, Random(seed))
        validate_route(out, 3)
        seen.add(out)
    # Với alpha=0.7 và d=2, floor(0.7 * r * 2) có thể là 0 (giữ a) hoặc 1 (swap 1 lần -> thành b)
    assert seen == {a, b}


def test_parent_immutability_and_no_global_rng_mutation():
    global_state_before = random.getstate()

    current_list = [0, 3, 1, 4, 2, 5]
    pbest_list = [0, 5, 2, 4, 1, 3]
    current_copy = list(current_list)
    pbest_copy = list(pbest_list)

    out1 = move_toward_best(current_list, pbest_list, 0.7, Random(99))
    out2 = update_matriarch(pbest_list, current_list, 0.3, Random(99))

    assert current_list == current_copy
    assert pbest_list == pbest_copy
    assert type(out1) is tuple
    assert type(out2) is tuple
    assert random.getstate() == global_state_before


def test_reproducibility_with_fixed_seed():
    n = 48
    current = random_permutation(n, Random(10))
    pbest = random_permutation(n, Random(20))
    center = random_permutation(n, Random(30))

    r1 = move_toward_best(current, pbest, 0.7, Random(12345))
    r2 = move_toward_best(current, pbest, 0.7, Random(12345))
    assert r1 == r2

    m1 = update_matriarch(pbest, center, 0.3, Random(54321))
    m2 = update_matriarch(pbest, center, 0.3, Random(54321))
    assert m1 == m2


def test_higher_alpha_moves_closer_on_average():
    n = 48
    rng_init = Random(7)
    current = random_permutation(n, rng_init)
    pbest = random_permutation(n, rng_init)
    initial_dist = hamming_distance(current, pbest)
    assert initial_dist > 30

    trials = 200
    low_dists = [hamming_distance(move_toward_best(current, pbest, 0.15, Random(s)), pbest) for s in range(trials)]
    high_dists = [hamming_distance(move_toward_best(current, pbest, 0.85, Random(s)), pbest) for s in range(trials)]

    assert sum(high_dists) / trials < sum(low_dists) / trials < initial_dist


@pytest.mark.parametrize("bad_strength", [-0.01, 1.01, math.nan, math.inf, -math.inf, True, False, "0.5"])
def test_invalid_strength_rejected(bad_strength):
    a = (0, 1, 2, 3)
    b = (0, 3, 2, 1)
    with pytest.raises(ValueError):
        move_toward_best(a, b, bad_strength, Random(1))
    with pytest.raises(ValueError):
        update_matriarch(a, b, bad_strength, Random(1))


def test_invalid_routes_rejected():
    rng = Random(1)
    # Quá ngắn (< 3)
    with pytest.raises(ValueError):
        move_toward_best((0, 1), (0, 1), 0.5, rng)
    # Khác độ dài
    with pytest.raises(ValueError):
        move_toward_best((0, 1, 2), (0, 1, 2, 3), 0.5, rng)
    # Không bắt đầu bằng 0
    with pytest.raises(ValueError):
        move_toward_best((1, 0, 2), (0, 1, 2), 0.5, rng)
    # Trùng đỉnh
    with pytest.raises(ValueError):
        update_matriarch((0, 1, 1), (0, 1, 2), 0.5, rng)
    # Hamming với route sai
    with pytest.raises(ValueError):
        hamming_distance((0, 1, 2), (0, 1, 2, 3))
    # Không phải sequence hợp lệ
    for bad in (None, 123, "012", b"012"):
        with pytest.raises(ValueError):
            move_toward_best(bad, (0, 1, 2), 0.5, rng)
        with pytest.raises(ValueError):
            update_matriarch((0, 1, 2), bad, 0.5, rng)
