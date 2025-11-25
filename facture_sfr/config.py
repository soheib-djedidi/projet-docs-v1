"""Gestion de la configuration du générateur de factures SFR."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional

import yaml


@dataclass
class FieldConfig:
    """Configuration pour un champ texte à dessiner sur la facture."""

    layer_name: str
    occurrence: int | None = None
    line_spacing: int = 4
    hide_original: bool = True
    font_size: Optional[int] = None
    fill: str = "black"


@dataclass
class AppConfig:
    """Configuration complète du projet."""

    template_psd: Path
    font_path: Path
    font_size: int
    output_dir: Path
    fields: Dict[str, FieldConfig] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict) -> "AppConfig":
        fields_data = data.get("fields", {})
        fields = {
            name: FieldConfig(**value) for name, value in fields_data.items()
        }
        return cls(
            template_psd=Path(data["template_psd"]),
            font_path=Path(data["font_path"]),
            font_size=int(data.get("font_size", 16)),
            output_dir=Path(data.get("output_dir", "output")),
            fields=fields,
        )


def load_config(path: str | Path) -> AppConfig:
    """Charge la configuration YAML fournie.

    Args:
        path: Chemin vers le fichier YAML de configuration.

    Returns:
        Une instance :class:`AppConfig`.
    """

    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    return AppConfig.from_dict(data)


__all__ = ["FieldConfig", "AppConfig", "load_config"]
