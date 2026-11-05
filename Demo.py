import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
sys.path.append(os.path.abspath('./src'))
from src.GA import genetic_algorithm
from src.TSP import read_matrix

class UI:
    def __init__(self, root):
        self.root = root
        self.root.title("Genetic Algorithm for TSP")
        # Các mục nhập thông số
        self.parameters_frame = ttk.LabelFrame(root, text="Parameters")
        self.parameters_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Combobox chọn file dữ liệu
        self.data_files = [f"./data/{file}" for file in os.listdir("data") if file.endswith(".txt")]
        self.data_file_combobox = self.create_combobox(self.parameters_frame, "Data File", self.data_files, 0)

        # Kích thước quần thể
        self.population_size_entry = self.create_label_entry(self.parameters_frame, "Population Size:", 1, "100")

        # Số thế hệ
        self.generations_entry = self.create_label_entry(self.parameters_frame, "Generations:", 2, "100")

        # Tỷ lệ đột biến
        self.mutation_rate_entry = self.create_label_entry(self.parameters_frame, "Mutation Rate:", 3, "0.01")

        # Lựa chọn thuật toán cho từng bước
        self.selection_algorithm = self.create_combobox(self.parameters_frame, "Selection Algorithm", ["elitism", "rank", "tournament", "roulette_wheel"], 4)

        self.crossover_algorithm = self.create_combobox(self.parameters_frame, "Crossover Algorithm", ["order", "two_point", "single_point", "uniform"], 5)

        self.mutation_algorithm = self.create_combobox(self.parameters_frame, "Mutation Algorithm", ["swap", "scramble", "inversion", "insertion"], 6)

        # Nút chạy thuật toán
        self.run_button = tk.Button(root, text="Run", command=self.run_algorithm)
        self.run_button.grid(row=2, column=0, padx=10, pady=10)

        # Kết quả
        self.result_label = ttk.Label(root, text="")
        self.result_label.grid(row=3, column=0, padx=10, pady=10)

    def create_label_entry(self, parent, text, row, default_value=""):
        label = ttk.Label(parent, text=text)
        label.grid(row=row, column=0, padx=5, pady=5, sticky="w")

        entry = ttk.Entry(parent)
        entry.insert(0, default_value)
        entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        
        return entry

    def create_combobox(self, parent, label_text, values, row):
        label = ttk.Label(parent, text=label_text)
        label.grid(row=row, column=0, padx=5, pady=5, sticky="w")

        combobox = ttk.Combobox(parent, values=values, state="readonly")
        combobox.current(0)  
        combobox.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        
        return combobox

    def run_algorithm(self):
        try:
            population_size = int(self.population_size_entry.get())
            generations = int(self.generations_entry.get())
            mutation_rate = float(self.mutation_rate_entry.get())
            selection_algorithm = self.selection_algorithm.get()
            crossover_algorithm = self.crossover_algorithm.get()
            mutation_algorithm = self.mutation_algorithm.get()
            data_file_path = self.data_file_combobox.get()

            # Đọc ma trận khoảng cách từ file
            distances = read_matrix(data_file_path)
            # Xác định số lượng thành phố
            n_cities = len(distances)

            # Chạy giải thuật di truyền
            solution = genetic_algorithm(n_cities, distances, population_size, generations, mutation_rate,
                                         mutation_algorithm, selection_algorithm, crossover_algorithm)

            # Hiển thị kết quả
            result_text = f"Best Route: {solution['route']}\nDistance: {solution['distance']}"
            self.result_label.config(text=result_text)
        except ValueError:
            messagebox.showerror("Lỗi nhập", "Hãy nhập giá trị số")

if __name__ == "__main__":
    root = tk.Tk()
    app = UI(root)
    root.mainloop()
