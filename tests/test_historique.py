"""Tests de la classe Historique."""

import pytest

from historique import Historique


@pytest.fixture
def historique(tmp_path):
    """Historique vide dans un dossier temporaire."""
    return Historique(str(tmp_path / "sous_dossier" / "historique.csv"), ["Heures", "Plateforme"])


def test_historique_vide(historique):
    """Sans fichier, l'historique est vide (cas limite)."""
    assert len(historique) == 0
    assert list(historique.lignes()) == []


def test_ajouter_puis_relire(historique):
    """Une prediction ajoutee est relue avec ses valeurs et son GPA arrondi."""
    historique.ajouter({"Heures": 3.0, "Plateforme": "TikTok"}, 3.456)
    ligne = next(historique.lignes())
    assert ligne["Plateforme"] == "TikTok"
    assert float(ligne["gpa_estime"]) == pytest.approx(3.46)


def test_en_tete_ecrit_une_seule_fois(historique):
    """Deux ajouts donnent deux lignes : l'en-tete n'est pas repete."""
    historique.ajouter({"Heures": 3.0, "Plateforme": "TikTok"}, 3.4)
    historique.ajouter({"Heures": 9.0, "Plateforme": "YouTube"}, 2.9)
    assert len(historique) == 2