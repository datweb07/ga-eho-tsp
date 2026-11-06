"""Registry không coi hậu tố tên file là optimum đã kiểm chứng."""

from pathlib import Path

DATASET_NAMES = (
    "03Cities-6.txt", "04Cities-189.txt", "06Cities-1248.txt",
    "15Cities-1194.txt", "26Cities-937.txt", "42Cities-699.txt", "48Cities-33523.txt",
)


def dataset_registry(data_dir: str | Path) -> dict[str, dict[str, object]]:
    return {name: {"path": str(Path(data_dir) / name), "known_optimum": None,
                   "name_hint": int(Path(name).stem.split("-")[1]),
                   "source": "ThienNguyen3001/Travelling-Salesman-Genetic-AI-Final; upstream dataset unverified"}
            for name in DATASET_NAMES}
