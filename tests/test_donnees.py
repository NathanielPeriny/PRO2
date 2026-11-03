import os


def test_fichier_donnees_existe():
    """Le jeu de données est dans le dossier donnees/."""
    chemin = os.path.join(os.path.dirname(__file__), "..", "donnees", "social_media.csv")
    assert os.path.exists(chemin)