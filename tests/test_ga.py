import random
from dataclasses import replace
from pathlib import Path
from random import Random
import pytest

from ga_eho_tsp.algorithms.ga import solve
from ga_eho_tsp.algorithms.ga.crossover import order_crossover
from ga_eho_tsp.algorithms.ga.initialization import initialize
from ga_eho_tsp.algorithms.ga.mutation import mutate
from ga_eho_tsp.algorithms.ga.selection import select_parent
from ga_eho_tsp.algorithms.ga.survivor import select_elites
from ga_eho_tsp.data.matrix_loader import load_matrix
from ga_eho_tsp.domain.models import GAConfig, TSPProblem
from ga_eho_tsp.domain.objective import validate_route

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize('n', [3,4,6,15,26,42,48])
def test_operators(n):
    for seed in range(30):
        rng = Random(seed)
        parents = initialize(n, 4, rng)
        before = parents.copy()
        children = order_crossover(parents[0], parents[1], rng)
        for child in children:
            validate_route(child, n)
            for method in ('swap','inversion','insertion','scramble'):
                assert mutate(child, 0, rng, method) == child
                validate_route(mutate(child, 1, rng, method), n)
        assert parents == before


def test_ox_example():
    class Cuts:
        def sample(self, values, k):
            return [1, 3]
    a, b = (0,1,2,3,4,5,6), (0,4,1,6,2,5,3)
    assert order_crossover(a,b,Cuts())[0] == (0,6,2,3,4,5,1)


@pytest.mark.parametrize('method', ['swap','inversion','insertion','scramble'])
def test_mutation_semantics(method):
    parent = (0,1,2)
    assert mutate(parent, 0, Random(0), method) == parent
    # Scramble có thể shuffle ra cùng route; inversion phải đổi n=3.
    if method != 'scramble':
        assert mutate(parent, 1, Random(0), method) == (0,2,1)
    assert parent == (0,1,2)


@pytest.mark.parametrize('method', ['tournament','rank','roulette_wheel'])
def test_selection_equal_and_direction(method):
    pop = [(0,i) for i in range(6)]
    rng = Random(42)
    costs = [0.]*6
    selected = [select_parent(pop,costs,rng,method) for _ in range(500)]
    assert len(set(selected)) > 1
    costs = list(range(6))
    chosen = [select_parent(pop,costs,rng,method,6) for _ in range(1000)]
    assert chosen.count(pop[0]) > chosen.count(pop[-1])
    assert costs == list(range(6))


def test_elites_distinct_indices():
    pop = [(0,1,2),(0,2,1),(0,1,2),(0,2,1)]
    costs = [10,20,30,40]
    elite, scores = select_elites(pop,costs,2)
    assert elite == pop[:2] and scores == [10,20]
    assert costs == [10,20,30,40]


@pytest.mark.parametrize('name', ['03Cities-6.txt','04Cities-189.txt','06Cities-1248.txt',
    '15Cities-1194.txt','26Cities-937.txt','42Cities-699.txt','48Cities-33523.txt'])
def test_solver_smoke(name):
    p = load_matrix(ROOT / 'data/legacy' / name)
    config = GAConfig(population_size=9,generations=20,record_history_every=3)
    stats = []
    result = solve(p,config,progress_callback=stats.append)
    validate_route(result.best_route,p.dimension)
    assert result.best_distance == p.route_length(result.best_route)
    assert result.evaluations == 9 + 20*7
    assert result.iterations_completed == 20
    assert result.history[0].iteration == 0 and result.history[-1].iteration == 20
    assert tuple(stats) == result.history
    assert all(b.best_so_far <= a.best_so_far for a,b in zip(stats,stats[1:]))


def test_reproducible_without_global_rng():
    p = load_matrix(ROOT / 'data/legacy/15Cities-1194.txt')
    config = GAConfig(population_size=11,generations=25)
    random.seed(999)
    state = random.getstate()
    a = solve(p,config)
    assert random.getstate() == state
    random.seed(2)
    b = solve(p,config)
    assert a.best_route == b.best_route
    assert [(s.iteration,s.best_so_far,s.mean_fitness,s.evaluations) for s in a.history] == [
        (s.iteration,s.best_so_far,s.mean_fitness,s.evaluations) for s in b.history]


def test_global_best_when_final_population_worse(monkeypatch):
    import ga_eho_tsp.algorithms.ga.solver as module
    p = TSPProblem('four', ((0,1,9,1),(1,0,1,9),(9,1,0,1),(1,9,1,0)))
    good, bad = (0,1,2,3), (0,2,1,3)
    monkeypatch.setattr(module, 'initialize', lambda *args: [good]*4)
    monkeypatch.setattr(module, 'mutate', lambda *args: bad)
    result = solve(p,GAConfig(population_size=4,generations=1,elite_count=0))
    assert result.best_route == good and result.best_distance == 4
    assert result.history[-1].best_current == 20


def test_stop_budgets_and_partial():
    p = load_matrix(ROOT / 'data/legacy/15Cities-1194.txt')
    config = GAConfig(population_size=9,generations=30)
    for budget in [9,10,15,16,17,22,23]:
        result = solve(p,replace(config,max_evaluations=budget))
        assert result.evaluations == budget
        assert result.stopping_reason == 'MAX_EVALUATIONS'
        assert result.history[-1].evaluations == budget
        assert result.best_distance == p.route_length(result.best_route)
    result = solve(p,config,stop_requested=lambda: True)
    assert result.stopping_reason == 'CANCELLED' and result.iterations_completed == 0
    result = solve(p,replace(config,time_limit_seconds=1e-12))
    assert result.stopping_reason == 'TIME_LIMIT' and result.iterations_completed == 0
    result = solve(p,replace(config,max_iterations=2))
    assert result.iterations_completed == 2


def test_callback_cancel_and_failure():
    p = load_matrix(ROOT / 'data/legacy/06Cities-1248.txt')
    seen = []
    result = solve(p,GAConfig(),progress_callback=seen.append,stop_requested=lambda: len(seen)>=3)
    assert result.stopping_reason == 'CANCELLED' and result.iterations_completed == 2
    def fail(stat):
        raise RuntimeError('callback failed')
    with pytest.raises(RuntimeError,match='callback failed'):
        solve(p,GAConfig(),progress_callback=fail)


def test_exact_objective_count_and_cancel_mid_iteration(monkeypatch):
    p = load_matrix(ROOT / 'data/legacy/15Cities-1194.txt')
    original = TSPProblem.route_length
    calls = []
    def counted(self, route):
        calls.append(route)
        return original(self, route)
    monkeypatch.setattr(TSPProblem, 'route_length', counted)
    result = solve(p, GAConfig(population_size=9), stop_requested=lambda: len(calls) >= 12)
    assert result.stopping_reason == 'CANCELLED'
    assert result.evaluations == len(calls) == 12
    assert result.iterations_completed == 0 and result.metadata['partial_iteration']
    assert result.best_distance == min(original(p, route) for route in calls)


@pytest.mark.parametrize('selection', ['tournament','rank','roulette_wheel'])
@pytest.mark.parametrize('mutation', ['swap','inversion','insertion','scramble'])
def test_zero_cost_solver(selection,mutation):
    p = TSPProblem('zero', ((0,0,0),)*3)
    result = solve(p,GAConfig(population_size=5,generations=3,selection_method=selection,mutation_method=mutation))
    assert result.best_distance == 0 and result.evaluations == 14
