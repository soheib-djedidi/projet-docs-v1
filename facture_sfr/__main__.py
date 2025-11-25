"""Point d'entrée exécutable via ``python -m facture_sfr``."""

from .cli import main


if __name__ == "__main__":  # pragma: no cover - délègue au CLI
    raise SystemExit(main())
