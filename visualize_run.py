"""
Script chạy giải thuật Di truyền (GA) và trực quan hóa:
1. Đồ thị mạng lưới các thành phố và Chu trình tối ưu (NetworkX + Matplotlib)
2. Biểu đồ đường cong hội tụ Fitness qua các thế hệ
"""
import os
import sys
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'src'))

from GA import genetic_algorithm
from TSP import read_matrix, visualize

def run_and_plot(data_filename='15Cities-1194.txt', pop_size=200, gens=150, mut_rate=0.02,
                 sel_alg='tournament', cross_alg='order', mut_alg='inversion'):
    data_file = os.path.join(BASE_DIR, 'data', data_filename)
    print(f"=== ĐANG CHẠY BÀI TOÁN: {data_filename} ===")
    distances = read_matrix(data_file)
    n_cities = len(distances)
    
    # 1. Chạy GA
    solution = genetic_algorithm(
        n_cities=n_cities,
        distances=distances,
        population_size=pop_size,
        generations=gens,
        mutation_rate=mut_rate,
        selection_algorithm=sel_alg,
        crossover_algorithm=cross_alg,
        mutation_algorithm=mut_alg
    )
    
    best_route = solution['route']
    best_dist = solution['distance']
    fitness_history = solution['fitness']
    
    print("\n--- KẾT QUẢ ---")
    print(f"Lộ trình tối ưu tìm được: {best_route}")
    print(f"Tổng khoảng cách: {best_dist}")
    
    # 2. Vẽ biểu đồ đường cong hội tụ Fitness
    plt.figure(figsize=(9, 4))
    plt.plot(fitness_history, color='blue', linewidth=2, label='Khoảng cách ngắn nhất qua từng thế hệ')
    plt.title(f"Quá trình Hội tụ GA - {data_filename} (Kết quả: {best_dist})")
    plt.xlabel("Thế hệ (Generation)")
    plt.ylabel("Tổng khoảng cách (Fitness)")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # 3. Trực quan hóa lộ trình đồ thị (chuyển đổi index về 0-based để khớp ma trận NetworkX)
    route_0_based = [c - 1 for c in best_route[:-1]]
    visualize(distances, route_0_based, draw_weight=False, initial=True)

if __name__ == '__main__':
    # Bạn có thể đổi file dữ liệu hoặc tham số tại đây
    run_and_plot('15Cities-1194.txt', pop_size=200, gens=150, mut_rate=0.02,
                 sel_alg='tournament', cross_alg='order', mut_alg='inversion')
