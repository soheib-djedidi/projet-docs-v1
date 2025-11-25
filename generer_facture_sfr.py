from psd_tools import PSDImage
from PIL import Image, ImageDraw, ImageFont

# -------- CONFIG --------
PSD_PATH = "Facture SFR.psd"            # ton fichier PSD
OUTPUT_PDF = "Facture_SFR_generee.pdf"  # nom de sortie

LAYER_ADRESSE = "adresse_client"        # nom du calque texte à utiliser pour l'adresse

# Police à utiliser (mets une vraie police existante sur ton PC)
FONT_PATH = "arial.ttf"                 # à adapter
FONT_SIZE = 16                          # ajuste si besoin
TEXT_COLOR = "black"


def find_layer_bbox(psd, layer_name):
    """
    Cherche un calque par son nom et retourne sa bounding box (x1, y1, x2, y2).
    """
    for layer in psd.descendants():
        if layer.name == layer_name:
            return layer.bbox  # (x1, y1, x2, y2)
    raise ValueError(f"Calque '{layer_name}' introuvable dans le PSD.")


def main():
    print("=== Générateur de facture SFR ===")

    # Demander les infos
    nom = input("Nom / Société : ")
    adresse_l1 = input("Adresse ligne 1 : ")
    adresse_l2 = input("Adresse ligne 2 (laisser vide si inutile) : ")
    cp = input("Code postal : ")
    ville = input("Ville : ")

    # Texte multi-ligne pour le bloc adresse
    lignes = [nom, adresse_l1]
    if adresse_l2.strip():
        lignes.append(adresse_l2)
    lignes.append(f"{cp} {ville}")

    adresse_text = "\n".join(lignes)

    # Charger le PSD
    psd = PSDImage.open(PSD_PATH)

    # Rendre tous les calques en une image
    img = psd.composite().convert("RGB")

    # Trouver la position du calque d'adresse
    x1, y1, x2, y2 = find_layer_bbox(psd, LAYER_ADRESSE)

    # Zone dispo pour le texte
    width = x2 - x1
    height = y2 - y1

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    # Option simple : écrire le texte en haut à gauche de la zone du calque
    # Tu peux aussi centrer verticalement si tu veux.
    draw.multiline_text(
        (x1, y1),
        adresse_text,
        font=font,
        fill=TEXT_COLOR,
        spacing=4
    )

    # Export en PDF
    img.save(OUTPUT_PDF, "PDF", resolution=300.0)
    print(f"\n✅ PDF généré : {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
