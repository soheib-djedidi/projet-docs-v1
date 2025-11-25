from pathlib import Path
from types import SimpleNamespace

import pytest
from PIL import Image

from facture_sfr.config import AppConfig, FieldConfig
from facture_sfr.invoice_generator import InvoiceData, InvoiceGenerator


class DummyLayer:
    def __init__(self, name):
        self.name = name
        self.visible = True


class DummyPSD:
    def __init__(self, layers):
        self._layers = layers

    def descendants(self):
        return self._layers

    def composite(self):
        return Image.new("RGB", (200, 200), color="white")


@pytest.fixture()
def app_config(tmp_path):
    return AppConfig(
        template_psd=Path("dummy.psd"),
        font_path=Path("fonts/arial.ttf"),
        font_size=12,
        output_dir=tmp_path,
        fields={
            "adresse_client": FieldConfig(layer_name="adresse"),
        },
    )


def test_invoice_generator_hides_layer_and_outputs_pdf(monkeypatch, app_config):
    dummy_layer = DummyLayer("adresse")
    dummy_psd = DummyPSD([dummy_layer])

    def fake_load_psd(path):
        return dummy_psd

    def fake_get_bbox(psd, name):
        return (10, 10, 100, 100)

    monkeypatch.setattr("facture_sfr.invoice_generator.load_psd", fake_load_psd)
    monkeypatch.setattr("facture_sfr.invoice_generator.get_layer_bbox", fake_get_bbox)

    generator = InvoiceGenerator(app_config)
    data = InvoiceData(
        nom="Test User",
        adresse1="1 rue ici",
        adresse2=None,
        cp="75000",
        ville="Paris",
        date="2024-01-01",
        montant="99.99",
        numero_facture="F1",
    )

    output = generator.generate(data)
    assert output.exists()
    assert dummy_layer.visible is False
