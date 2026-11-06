"""Monitoring nhẹ trên population commit, không đánh giá thêm objective."""

from ...domain.objective import Route
from ...domain.models import GAConfig


def population_diversity(population: list[Route]) -> float:
    """(unique symmetric tours−1)/(P−1); route đảo chiều được coi tương đương."""
    if len(population) <= 1:
        return 0.0
    canonical = {min(route, (0, *route[:0:-1])) for route in population}
    return (len(canonical)-1) / (len(population)-1)


def effective_mutation_rate(config: GAConfig, stagnation: int, diversity: float) -> float:
    """Tăng tuyến tính theo stagnation; diversity≤0.1 đặt pressure tối thiểu 0.5."""
    if not config.adaptive_mutation:
        return config.mutation_rate
    base = min(config.adaptive_max_rate, max(config.adaptive_min_rate, config.mutation_rate))
    pressure = min(1.0, stagnation / config.adaptive_patience)
    if diversity <= 0.1:
        pressure = max(pressure, 0.5)
    return base + (config.adaptive_max_rate-base)*pressure
