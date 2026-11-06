from ...domain.objective import Route


def select_elites(population: list[Route], costs: list[float], count: int) -> tuple[list[Route], list[float]]:
    """Giữ count index tốt nhất, thứ tự tie ổn định; tái dùng fitness."""
    indices = sorted(range(len(population)), key=lambda i: costs[i])[:count]
    return [population[i] for i in indices], [costs[i] for i in indices]
