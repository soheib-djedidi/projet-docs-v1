"""Utilitaires pour charger et interroger un PSD."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, Tuple

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


def _filter_layers(psd: PSDImage, layer_name: str) -> Iterable[Layer]:
    """Retourne les calques correspondant à un nom donné."""

    return (layer for layer in psd.descendants() if layer.name == layer_name)


def find_layer(psd: PSDImage, layer_name: str, occurrence: int | None = None) -> Layer:
    """Trouve un calque dans un PSD en se basant sur son nom.

    - Si ``occurrence`` est fourni, on retourne l'occurrence correspondante
      dans l'ordre des descendants.
    - Sinon, on choisit le calque avec la plus grande surface (bbox) pour
      éliminer les doublons potentiels (ex. plusieurs cadres d'adresse).
    """

    candidates = list(_filter_layers(psd, layer_name))
    if not candidates:
        raise LayerNotFoundError(f"Calque '{layer_name}' introuvable dans le PSD.")

    if occurrence is not None:
        try:
            return candidates[occurrence]
        except IndexError:
            raise LayerNotFoundError(
                f"Calque '{layer_name}' occurrence {occurrence} introuvable dans le PSD."
            ) from None

    def _area(layer: Layer) -> int:
        bbox = layer.bbox
        width = getattr(bbox, "width", bbox[2] - bbox[0])
        height = getattr(bbox, "height", bbox[3] - bbox[1])
        return width * height

    return max(candidates, key=_area)


def get_layer_bbox(
    psd: PSDImage, layer_name: str, occurrence: int | None = None
) -> Tuple[int, int, int, int]:
    """Retourne la bounding box (x1, y1, x2, y2) d'un calque.

    Args:
        psd: Image PSD ouverte.
        layer_name: Nom du calque recherché.
        occurrence: Occurrence souhaitée (0-based). Si ``None``, sélectionne
            le calque de plus grande surface.
    """

    layer = find_layer(psd, layer_name, occurrence)
    return tuple(layer.bbox)


__all__ = ["load_psd", "find_layer", "get_layer_bbox", "LayerNotFoundError"]
