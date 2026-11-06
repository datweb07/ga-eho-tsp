"""Tái hiện lỗi legacy headless; cần cài extra [legacy]. Không sửa code gốc."""

import hashlib
import json
import os
from pathlib import Path
import random
import sys
from time import perf_counter

ROOT = Path(__file__).resolve().parents[2]
os.environ["MPLBACKEND"] = "Agg"
sys.path.insert(0, str(ROOT / "legacy/original_src"))
import GA  # noqa: E402
import TSP  # noqa: E402
import numpy as np  # noqa: E402


def main() -> None:
    random.seed(42)
    np.random.seed(42)
    population = [[0, 1, 2], [0, 2, 1], [0, 1, 2], [0, 2, 1]]
    costs = [10, 20, 30, 40]
    report = {
        "elitism": GA.elitism_selection(population, costs),
        "costs_after_elitism": costs,
        "roulette_equal": GA.roulette_wheel_selection(population, [6]*4),
        "uniform": GA.uniform_crossover([0,1,2,3], [0,3,2,1]),
        "inversion_n3": GA.inversion_mutate([0,1,2], 1),
    }
    matrix = [[0,1,2],[1,0,3],[2,3,0]]
    for size in [2,3]:
        try:
            GA.genetic_algorithm(3, matrix, population_size=size, generations=2)
        except ValueError as error:
            report[f"population_{size}"] = str(error)
    original_fitness = GA.fitness
    lengths = []
    def tracked_fitness(population, distances):
        lengths.append(len(population))
        return original_fitness(population, distances)
    GA.fitness = tracked_fitness
    GA.genetic_algorithm(3, matrix, population_size=5, generations=3)
    GA.fitness = original_fitness
    report["odd_population_lengths"] = lengths
    # Xác nhận mất best bằng một run thực, không giả lập hàm GA.
    p = TSP.read_matrix(ROOT/'data/legacy/15Cities-1194.txt')
    for seed in range(100):
        random.seed(seed)
        result = GA.genetic_algorithm(15, p, population_size=10, generations=10,
            mutation_rate=1, selection_algorithm='tournament')
        if result['distance'] > min(result['fitness']):
            report['lost_global_best'] = {'seed':seed, **result}
            break
    report["source_checksums"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                   for p in (ROOT/'legacy').rglob('*') if p.suffix in {'.py','.ipynb'}}
    path = ROOT/'experiments/reports/legacy_regressions.json'
    path.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
