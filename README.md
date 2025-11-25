# Générateur de facture SFR

Outil Python pour générer une facture PDF à partir du template PSD SFR fourni. Le projet charge un PSD, masque les calques texte d'origine et redessine le contenu configurable via Pillow.

## Installation

1. Crée un environnement virtuel et active-le :
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Installe les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Le fichier `config.yaml` décrit la police, le template PSD et les champs à écrire. Exemple :

```yaml
template_psd: "Facture SFR.psd"
font_path: "fonts/arial.ttf"
font_size: 16
output_dir: "output"
fields:
  adresse_client:
    layer_name: "adresse_client"
    line_spacing: 4
    hide_original: true
  date_facture:
    layer_name: "date_facture"
    hide_original: true
  num_facture:
    layer_name: "num_facture"
    hide_original: true
  montant_ttc:
    layer_name: "montant_ttc"
    hide_original: true
```

Chaque champ utilise le nom du calque PSD pour récupérer la bbox et dessiner le texte dans la même zone. Le paramètre `hide_original` masque le calque source avant la composition.

## Génération d'une facture

Lance la commande suivante :

```bash
python -m facture_sfr \
  --nom "Jean Dupont" \
  --adresse1 "10 rue de Paris" \
  --adresse2 "Bâtiment B" \
  --cp "75001" \
  --ville "Paris" \
  --date "2025-01-15" \
  --montant "89.99" \
  --numero-facture "F2025-001"
```

Le PDF généré sera enregistré dans le dossier `output` sous la forme `facture_<numéro>_<nom>.pdf`. Ajoute `--interactive` pour que les champs manquants soient demandés au clavier.

## Architecture du code

- `facture_sfr/config.py` : chargement et validation basique de la configuration YAML.
- `facture_sfr/psd_loader.py` : utilitaires pour ouvrir le PSD et récupérer la bbox des calques.
- `facture_sfr/invoice_generator.py` : orchestration de la composition finale et de l'écriture du texte.
- `facture_sfr/cli.py` : interface en ligne de commande.
- `facture_sfr/clients.py` : stockage minimaliste des clients et de l'historique des factures.

## Tests

Exécute les tests unitaires avec :

```bash
pytest
```

## Roadmap

- Support d'une base SQLite optionnelle pour les clients.
- Interface graphique minimale.
- Validation plus poussée des champs.
