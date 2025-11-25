"""Génération d'une facture à partir d'un PSD de template."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from PIL import ImageDraw, ImageFont

from .config import AppConfig, FieldConfig
from .psd_loader import get_layer_bbox, load_psd


@dataclass
class InvoiceData:
    """Données principales à injecter dans la facture."""

    nom: str
    adresse1: str
    adresse2: str | None
    cp: str
    ville: str
    date: str
    montant: str
    numero_facture: str

    def to_field_mapping(self) -> Dict[str, str]:
        """Retourne un mapping champ -> texte multi-ligne à dessiner."""

        lignes_adresse = [self.nom, self.adresse1]
        if self.adresse2:
            lignes_adresse.append(self.adresse2)
        lignes_adresse.append(f"{self.cp} {self.ville}")

        return {
            "adresse_client": "\n".join(lignes_adresse),
            "date_facture": self.date,
            "num_facture": self.numero_facture,
            "montant_ttc": self.montant,
        }


class InvoiceGenerator:
    """Classe orchestrant la génération d'une facture PDF."""

    def __init__(self, config: AppConfig):
        self.config = config

    def _resolve_font(self, field_cfg: FieldConfig) -> ImageFont.FreeTypeFont:
        size = field_cfg.font_size or self.config.font_size
        try:
            return ImageFont.truetype(str(self.config.font_path), size)
        except OSError:
            return ImageFont.load_default()

    def _hide_layers(self, psd, fields: Dict[str, FieldConfig]) -> None:
        for field in fields.values():
            if field.hide_original:
                try:
                    layer = next(
                        l for l in psd.descendants() if l.name == field.layer_name
                    )
                    layer.visible = False
                except StopIteration:
                    continue

    def generate(self, data: InvoiceData, output_path: Path | None = None) -> Path:
        """Génère la facture et retourne le chemin du PDF produit."""

        psd = load_psd(self.config.template_psd)
        self._hide_layers(psd, self.config.fields)
        image = psd.composite().convert("RGB")

        drawer = ImageDraw.Draw(image)
        field_values = data.to_field_mapping()

        for field_name, field_cfg in self.config.fields.items():
            if field_name not in field_values:
                continue
            bbox = get_layer_bbox(psd, field_cfg.layer_name)
            x1, y1, x2, y2 = bbox
            font = self._resolve_font(field_cfg)
            drawer.multiline_text(
                (x1, y1),
                field_values[field_name],
                font=font,
                fill=field_cfg.fill,
                spacing=field_cfg.line_spacing,
            )

        output_dir = self.config.output_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        if output_path is None:
            safe_name = data.nom.replace(" ", "_")
            filename = f"facture_{data.numero_facture}_{safe_name}.pdf"
            output_path = output_dir / filename

        image.save(output_path, "PDF", resolution=300.0)
        return output_path


__all__ = ["InvoiceGenerator", "InvoiceData"]
