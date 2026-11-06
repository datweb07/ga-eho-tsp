from itertools import permutations
from pathlib import Path
from random import Random

import pytest

from ga_eho_tsp.data.matrix_loader import load_matrix
from ga_eho_tsp.data.registry import DATASET_NAMES, dataset_registry
from ga_eho_tsp.domain.models import TSPProblem, GAConfig, EHOConfig
from ga_eho_tsp.domain.objective import validate_route
from ga_eho_tsp.domain.operators import random_permutation

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def triangle():
    return TSPProblem("triangle", ((0, 1, 2), (1, 0, 3), (2, 3, 0)))


def test_objective_and_immutable_input(triangle):
    route = [0, 1, 2]
    assert triangle.route_length(route) == triangle.route_length((0, 2, 1)) == 6
    assert route == [0, 1, 2]
    matrix = [[0, 1, 2], [1, 0, 3], [2, 3, 0]]
    problem = TSPProblem("copy", matrix)
    matrix[0][1] = 999
    assert problem.distance_matrix[0][1] == 1
    with pytest.raises(TypeError):
        problem.metadata["x"] = 1


@pytest.mark.parametrize("route", [None, '012', (0, 1), (0, 1, 1), (1, 0, 2), (0, 1, 2, 0), (0, True, 2), (0, 1.0, 2), (0, 1, 3)])
def test_bad_routes(route):
    with pytest.raises(ValueError):
        validate_route(route, 3)


@pytest.mark.parametrize("matrix", [None, (1,2,3), (), ((0, 1), (1, 0)), ((0, 1, 2),)*3,
    ((0, 1, 2), (1, 0), (2, 3, 0)), ((0, -1, 2), (-1, 0, 3), (2, 3, 0)),
    ((0, float('nan'), 2), (1, 0, 3), (2, 3, 0)),
    ((0, float('inf'), 2), (1, 0, 3), (2, 3, 0)),
    ((0, 2, 2), (1, 0, 3), (2, 3, 0)), ((0, 'x', 2), (1, 0, 3), (2, 3, 0))])
def test_bad_matrices(matrix):
    with pytest.raises(ValueError):
        TSPProblem("bad", matrix)


def test_zero_edges_and_symmetry_tolerance():
    assert TSPProblem("zero", ((0, 0, 0),)*3).route_length((0, 1, 2)) == 0
    TSPProblem("float", ((0., 1., 2.), (1.+1e-10, 0., 3.), (2., 3., 0.)))
    with pytest.raises(ValueError):
        TSPProblem("int", ((0, 10**20, 2), (10**20+1, 0, 3), (2, 3, 0)))


@pytest.mark.parametrize("name,n,cost", zip(DATASET_NAMES, [3,4,6,15,26,42,48], [6,224,1248,1312,1140,699,157553]))
def test_datasets(name, n, cost):
    problem = load_matrix(ROOT / "data/legacy" / name)
    assert problem.dimension == n
    assert problem.route_length(tuple(range(n))) == cost
    assert problem.known_optimum is None
    assert len(problem.metadata["sha256"]) == 64


def test_small_optima():
    for name, optimum in zip(DATASET_NAMES[:3], [6,189,1248]):
        p = load_matrix(ROOT / "data/legacy" / name)
        assert min(p.route_length((0, *tail)) for tail in permutations(range(1, p.dimension))) == optimum
    assert all(v['known_optimum'] is None for v in dataset_registry(ROOT / 'data/legacy').values())


@pytest.mark.parametrize("content", ["", "0 x\n1 0", "0 1 2\n\n1 0 3\n2 3 0", "0 1\n1 0", "0 nan 2\n1 0 3\n2 3 0"])
def test_loader_errors(tmp_path, content):
    p = tmp_path / 'bad.txt'
    p.write_text(content)
    with pytest.raises(ValueError):
        load_matrix(p)


@pytest.mark.parametrize("kwargs", [dict(population_size=3), dict(population_size=True), dict(elite_count=80),
    dict(tournament_size=81), dict(mutation_rate=-.1), dict(crossover_rate=float('nan')),
    dict(generations=0), dict(seed=-1), dict(max_iterations=0), dict(max_evaluations=2),
    dict(record_history_every=0), dict(time_limit_seconds=0), dict(selection_method='elitism'),
    dict(crossover_method='uniform'), dict(local_search_enabled=True), dict(initialization_method='nn')])
def test_ga_config_validation(kwargs):
    with pytest.raises(ValueError):
        GAConfig(**kwargs)


@pytest.mark.parametrize("kwargs", [dict(clan_count=1), dict(elephants_per_clan=2), dict(alpha=2),
    dict(beta=float('nan')), dict(separation_count_per_clan=20), dict(preserve_global_best=False),
    dict(iterations=0), dict(max_evaluations=1)])
def test_eho_schema_validation(kwargs):
    with pytest.raises(ValueError):
        EHOConfig(**kwargs)


def test_rng_and_eho_defaults():
    assert EHOConfig().population_size == 80
    assert random_permutation(6, Random(9)) == random_permutation(6, Random(9))
    with pytest.raises(ValueError):
        random_permutation(2, Random(1))
