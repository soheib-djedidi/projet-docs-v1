"""Interface en ligne de commande pour générer une facture."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

from .config import load_config
from .invoice_generator import InvoiceData, InvoiceGenerator


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Générateur de facture SFR")
    parser.add_argument("--config", default="config.yaml", help="Chemin du fichier de configuration")
    parser.add_argument("--nom", required=False)
    parser.add_argument("--adresse1", required=False)
    parser.add_argument("--adresse2", required=False)
    parser.add_argument("--cp", required=False)
    parser.add_argument("--ville", required=False)
    parser.add_argument("--date", required=False, dest="date_facture")
    parser.add_argument("--montant", required=False)
    parser.add_argument("--numero-facture", required=False, dest="numero_facture")
    parser.add_argument("--output", required=False, help="Chemin du PDF généré")
    parser.add_argument("--interactive", action="store_true", help="Saisie interactive des champs")
    return parser


def _prompt_if_missing(args: argparse.Namespace, field: str, label: str) -> str:
    value = getattr(args, field)
    if value:
        return value
    return input(f"{label}: ")


def build_invoice_data(args: argparse.Namespace) -> InvoiceData:
    nom = _prompt_if_missing(args, "nom", "Nom / Société")
    adresse1 = _prompt_if_missing(args, "adresse1", "Adresse ligne 1")
    adresse2: Optional[str] = None
    if args.interactive:
        adresse2 = _prompt_if_missing(args, "adresse2", "Adresse ligne 2 (optionnel)") or None
    else:
        adresse2 = args.adresse2

    cp = _prompt_if_missing(args, "cp", "Code postal")
    ville = _prompt_if_missing(args, "ville", "Ville")
    date = _prompt_if_missing(args, "date_facture", "Date de facture (YYYY-MM-DD)")
    montant = _prompt_if_missing(args, "montant", "Montant TTC")
    numero_facture = _prompt_if_missing(args, "numero_facture", "Numéro de facture")

    return InvoiceData(
        nom=nom,
        adresse1=adresse1,
        adresse2=adresse2,
        cp=cp,
        ville=ville,
        date=date,
        montant=montant,
        numero_facture=numero_facture,
    )


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    config = load_config(args.config)
    generator = InvoiceGenerator(config)
    invoice_data = build_invoice_data(args)

    output_path = Path(args.output) if args.output else None
    pdf_path = generator.generate(invoice_data, output_path=output_path)
    print(f"✅ PDF généré: {pdf_path}")
    return 0


if __name__ == "__main__":  # pragma: no cover - point d'entrée CLI
    raise SystemExit(main())
