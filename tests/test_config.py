from pathlib import Path

from facture_sfr.config import AppConfig, load_config


def test_load_config(tmp_path):
    cfg_path = tmp_path / "cfg.yaml"
    cfg_path.write_text(
        """
        template_psd: tpl.psd
        font_path: font.ttf
        font_size: 14
        output_dir: out
        fields:
          adresse_client:
            layer_name: adr
        """,
        encoding="utf-8",
    )

    cfg = load_config(cfg_path)
    assert isinstance(cfg, AppConfig)
    assert cfg.font_size == 14
    assert "adresse_client" in cfg.fields
    assert cfg.fields["adresse_client"].layer_name == "adr"
