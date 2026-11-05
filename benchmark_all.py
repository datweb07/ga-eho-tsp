"""
Script chạy Benchmark tự động toàn bộ 7 bộ dữ liệu trong thư mục data/
So sánh kết quả tìm được với nghiệm tối ưu chuẩn (Ground Truth TSPLIB/FSU)
"""
import os
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'src'))

from GA import genetic_algorithm
from TSP import read_matrix

# Cấu hình từng bài toán kèm kết quả tối ưu chuẩn đã biết
BENCHMARKS = [
    {
        'file': os.path.join(BASE_DIR, 'data', '03Cities-6.txt'),
        'optimal': 6,
        'params': {'population_size': 50, 'generations': 30, 'mutation_rate': 0.01,
                   'selection_algorithm': 'elitism', 'crossover_algorithm': 'order', 'mutation_algorithm': 'swap'}
    },
    {
        'file': os.path.join(BASE_DIR, 'data', '04Cities-189.txt'),
        'optimal': 189,
        'params': {'population_size': 50, 'generations': 30, 'mutation_rate': 0.01,
                   'selection_algorithm': 'elitism', 'crossover_algorithm': 'order', 'mutation_algorithm': 'swap'}
    },
    {
        'file': os.path.join(BASE_DIR, 'data', '06Cities-1248.txt'),
        'optimal': 1248,
        'params': {'population_size': 100, 'generations': 50, 'mutation_rate': 0.01,
                   'selection_algorithm': 'elitism', 'crossover_algorithm': 'order', 'mutation_algorithm': 'swap'}
    },
    {
        'file': os.path.join(BASE_DIR, 'data', '15Cities-1194.txt'),
        'optimal': 1194,
        'params': {'population_size': 200, 'generations': 150, 'mutation_rate': 0.02,
                   'selection_algorithm': 'tournament', 'crossover_algorithm': 'order', 'mutation_algorithm': 'inversion'}
    },
    {
        'file': os.path.join(BASE_DIR, 'data', '26Cities-937.txt'),
        'optimal': 937,
        'params': {'population_size': 350, 'generations': 250, 'mutation_rate': 0.02,
                   'selection_algorithm': 'tournament', 'crossover_algorithm': 'order', 'mutation_algorithm': 'inversion'}
    },
    {
        'file': os.path.join(BASE_DIR, 'data', '42Cities-699.txt'),
        'optimal': 699,
        'params': {'population_size': 300, 'generations': 350, 'mutation_rate': 0.15,
                   'selection_algorithm': 'rank', 'crossover_algorithm': 'order', 'mutation_algorithm': 'inversion'}
    },
    {
        'file': os.path.join(BASE_DIR, 'data', '48Cities-33523.txt'),
        'optimal': 33523,
        'params': {'population_size': 350, 'generations': 350, 'mutation_rate': 0.15,
                   'selection_algorithm': 'rank', 'crossover_algorithm': 'order', 'mutation_algorithm': 'inversion'}
    }
]

def run_benchmarks():
    print("=" * 95)
    print("  BẮT ĐẦU CHẠY BENCHMARK TỰ ĐỘNG GIẢI THUẬT DI TRUYỀN (GA) TRÊN 7 BỘ DỮ LIỆU TSP")
    print("=" * 95)
    
    results = []
    
    for idx, item in enumerate(BENCHMARKS, start=1):
        file_path = item['file']
        optimal = item['optimal']
        params = item['params']
        file_name = os.path.basename(file_path)
        
        print(f"\n[{idx}/7] Đang xử lý {file_name} ...", end=" ", flush=True)
        
        distances = read_matrix(file_path)
        n_cities = len(distances)
        
        t0 = time.time()
        solution = genetic_algorithm(n_cities, distances, **params)
        duration = time.time() - t0
        
        found_dist = solution['distance']
        error_pct = ((found_dist - optimal) / optimal) * 100
        
        results.append({
            'name': file_name,
            'cities': n_cities,
            'optimal': optimal,
            'found': found_dist,
            'error_pct': error_pct,
            'time': duration,
            'route': solution['route']
        })
        print(f"Hoàn thành trong {duration:.2f}s! (Tìm được: {found_dist} | Chuẩn: {optimal})")
        
    print("\n" + "=" * 95)
    print(f"{'Bộ Dữ Liệu':<22} | {'Số Đỉnh':<8} | {'Nghiệm Chuẩn':<13} | {'Kết Quả GA':<12} | {'Độ Lệch (%)':<12} | {'Thời Gian (s)':<12}")
    print("-" * 95)
    for r in results:
        print(f"{r['name']:<22} | {r['cities']:<8} | {r['optimal']:<13} | {r['found']:<12} | {r['error_pct']:<11.2f}% | {r['time']:<12.2f}")
    print("=" * 95)
    print("Ghi chú: Độ lệch (%) càng gần 0% nghĩa là giải thuật tìm ra kết quả càng tiệm cận tối ưu.")

if __name__ == '__main__':
    run_benchmarks()
