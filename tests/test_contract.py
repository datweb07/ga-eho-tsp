"""Hợp đồng không cần import EHO hoặc GUI."""

from dataclasses import asdict, fields
import json
import sys

from ga_eho_tsp.algorithms.ga import solve
from ga_eho_tsp.domain.models import EHOConfig, GAConfig, RunResult, TSPProblem
from ga_eho_tsp.domain.protocols import Solver


def test_shared_contract_and_serialization():
    solver: Solver[GAConfig] = solve
    problem = TSPProblem('triangle', ((0,1,2),(1,0,3),(2,3,0)))
    result = solver(problem, GAConfig(generations=1))
    expected = {'algorithm','problem_name','best_route','best_distance','iterations_completed',
        'evaluations','elapsed_seconds','seed','history','config_snapshot','stopping_reason','is_valid','metadata'}
    assert {field.name for field in fields(RunResult)} == expected
    record = json.loads(json.dumps(asdict(result)))
    assert record['best_route'][0] == 0 and len(record['best_route']) == 3
    assert record['best_distance'] == 6
    assert EHOConfig().population_size == GAConfig().population_size == 80
    assert not any(name.startswith('ga_eho_tsp.algorithms.eho') for name in sys.modules)
    assert 'tkinter' not in sys.modules and 'matplotlib.pyplot' not in sys.modules
