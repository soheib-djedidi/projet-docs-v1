"""Gestion simple des clients et de leur historique."""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class InvoiceRecord:
    numero_facture: str
    date: str
    montant: str
    pdf_path: str


@dataclass
class Client:
    id: str
    nom: str
    adresse1: str
    adresse2: Optional[str]
    cp: str
    ville: str
    invoices: List[InvoiceRecord]


class ClientStore:
    """Stockage minimaliste des clients dans un fichier JSON."""

    def __init__(self, path: str | Path = "data/clients.json") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("{}", encoding="utf-8")

    def load(self) -> Dict[str, Client]:
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        clients: Dict[str, Client] = {}
        for client_id, payload in raw.items():
            invoices = [InvoiceRecord(**inv) for inv in payload.get("invoices", [])]
            clients[client_id] = Client(
                id=client_id,
                nom=payload["nom"],
                adresse1=payload["adresse1"],
                adresse2=payload.get("adresse2"),
                cp=payload["cp"],
                ville=payload["ville"],
                invoices=invoices,
            )
        return clients

    def save(self, clients: Dict[str, Client]) -> None:
        payload = {
            cid: asdict(client)
            for cid, client in clients.items()
        }
        self.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def get(self, client_id: str) -> Client:
        clients = self.load()
        if client_id not in clients:
            raise KeyError(f"Client inconnu : {client_id}")
        return clients[client_id]

    def upsert(self, client: Client) -> None:
        clients = self.load()
        clients[client.id] = client
        self.save(clients)


__all__ = ["ClientStore", "Client", "InvoiceRecord"]
