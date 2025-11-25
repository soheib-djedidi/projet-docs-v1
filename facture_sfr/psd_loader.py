"""Utilitaires pour charger et interroger un PSD."""
from __future__ import annotations

from pathlib import Path
from typing import Tuple

from psd_tools import PSDImage
from psd_tools.api.layers import Layer


class LayerNotFoundError(RuntimeError):
    """Exception levée lorsque le calque n'est pas trouvé."""


def load_psd(path: str | Path) -> PSDImage:
    """Charge un fichier PSD et retourne l'objet :class:`PSDImage`.

    Args:
        path: Chemin vers le fichier PSD.
    """

    return PSDImage.open(path)


def find_layer(psd: PSDImage, layer_name: str) -> Layer:
    """Trouve un calque dans un PSD en se basant sur son nom exact."""

    for layer in psd.descendants():
        if layer.name == layer_name:
            return layer
    raise LayerNotFoundError(f"Calque '{layer_name}' introuvable dans le PSD.")


def get_layer_bbox(psd: PSDImage, layer_name: str) -> Tuple[int, int, int, int]:
    """Retourne la bounding box (x1, y1, x2, y2) d'un calque."""

    layer = find_layer(psd, layer_name)
    return tuple(layer.bbox)


__all__ = ["load_psd", "find_layer", "get_layer_bbox", "LayerNotFoundError"]
