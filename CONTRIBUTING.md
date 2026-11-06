# Contributing

## Getting started

Read [README.md](README.md), [GUIDELINES.md](GUIDELINES.md), and [the architecture contract](docs/architecture.md). Use Python 3.11 or newer and install the project from the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Scope and ownership

- Trương Thành Đạt owns GA and the shared domain contract.
- EHO is planned and must be implemented as an independent solver using the shared models, objective, RNG, progress, and stopping semantics.
- Propose changes to `domain/`, the objective, solver protocols, or the frozen specification for leader review before implementing a contract change.
- Preserve the seven matrix files in `data/`; do not change data to improve benchmark results.
- Follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Pull requests

Keep changes focused and describe the problem, implementation, validation commands, results, and limitations. Explain algorithmic changes and credit the sources used. Include reproducible seeds and actual evaluation budgets for experiments; retain unsuccessful or negative results.

Run the applicable CLI/data checks described in README, the example benchmark, and affected notebooks from a fresh kernel. Do not claim checks passed unless they were executed. The current handoff excludes the pytest suite; agree with the leader on restoring regression coverage for algorithm or shared-contract changes.

Keep virtual environments, caches, and generated `outputs/` out of commits. Do not commit credentials or private reports. Review third-party provenance and licensing before adding material; see [source attribution](docs/source_attribution.md).

For security issues, use the private reporting process in [SECURITY.md](SECURITY.md).
