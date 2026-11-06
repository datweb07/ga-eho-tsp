"""Loader ma trận whitespace, không có dòng header."""

from hashlib import sha256
from pathlib import Path
from ..domain.models import TSPProblem


def load_matrix(path: str | Path) -> TSPProblem:
    path = Path(path)
    try:
        raw = path.read_bytes()
    except OSError as error:
        raise ValueError(f"Không mở được file ma trận {path}: {error}") from error
    rows = []
    try:
        for line in raw.decode("utf-8-sig").splitlines():
            if not line.strip():
                raise ValueError("Ma trận có dòng rỗng.")
            rows.append(tuple(int(v) if v.lstrip("+-").isdigit() else float(v) for v in line.split()))
    except (ValueError, UnicodeError) as error:
        raise ValueError(f"Không đọc được ma trận {path.name}: {error}") from error
    return TSPProblem(path.stem, tuple(rows), source=str(path.resolve()),
                      metadata={"sha256": sha256(raw).hexdigest(), "format": "explicit-whitespace"})
