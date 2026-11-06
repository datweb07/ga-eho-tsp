"""Compatibility launcher cho CLI benchmark mới."""
import sys
from ga_eho_tsp.cli import main

if __name__ == "__main__":
    raise SystemExit(main(["benchmark", *sys.argv[1:]]))
