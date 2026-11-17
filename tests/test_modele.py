"""Tests du module modele."""

import numpy as np
import pytest
import os 
import joblib
from sklearn.metrics import mean_absolute_error

from donnees import charger_donnees, nettoyer_donnees
from modele import Modele, calculer_mae, charger_metadonnees, chronometrer


def test_mae_valeur_connue():
    """Sur un petit exemple calcule a la main : (0,2 + 0,3 + 0,1) / 3 = 0,2."""
    assert calculer_mae([3.5, 2.8, 3.9], [3.3, 3.1, 3.8]) == pytest.approx(0.2)


def test_mae_egale_scikit_learn():
    """Notre MAE (NumPy) donne le meme resultat que celle de scikit-learn."""
    reel = np.array([2.0, 3.0, 3.5, 4.0])
    predit = np.array([2.5, 2.9, 3.0, 3.8])
    assert calculer_mae(reel, predit) == pytest.approx(mean_absolute_error(reel, predit))

@pytest.fixture
def modele_entraine():
    """Modele prepare et entraine sur le vrai jeu de donnees."""
    modele = Modele(nettoyer_donnees(charger_donnees()))
    modele.preparer()
    modele.entrainer()
    return modele


def test_modele_bat_la_reference(modele_entraine):
    """Le modele se trompe moins que s'il predisait toujours le GPA moyen."""
    resultats = modele_entraine.evaluer()
    assert resultats["mae_modele"] < resultats["mae_reference"]
    assert resultats["amelioration_pct"] > 0


def test_evaluer_avant_entrainement():
    """Evaluer un modele pas encore entraine leve RuntimeError (cas d'erreur)."""
    modele = Modele(nettoyer_donnees(charger_donnees()))
    modele.preparer()
    with pytest.raises(RuntimeError):
        modele.evaluer()

def test_chronometrer_garde_resultat_et_nom():
    """Le decorateur ne change ni le resultat ni le nom de la fonction."""
    @chronometrer
    def additionner(a, b):
        return a + b

    assert additionner(2, 3) == 5
    assert additionner.__name__ == "additionner"


def test_figure_predit_reel(modele_entraine):
    """Le graphique a un titre, des axes etiquetes et une legende."""
    axe = modele_entraine.creer_figure_predit_reel().axes[0]
    assert axe.get_title() != ""
    assert axe.get_xlabel() == "GPA reel"
    assert axe.get_ylabel() == "GPA predit"
    assert axe.get_legend() is not None


def test_sauvegarder_puis_recharger(modele_entraine, tmp_path):
    """Le modele recharge depuis le fichier predit exactement la meme chose."""
    chemin = modele_entraine.sauvegarder(str(tmp_path))
    assert os.path.exists(chemin)
    recharge = joblib.load(chemin)
    attendu = modele_entraine.predire_test()
    obtenu = recharge.predict(modele_entraine._x_test)
    assert obtenu == pytest.approx(attendu)


def test_sauvegarder_avant_entrainement(tmp_path):
    """Sauvegarder un modele pas entraine leve RuntimeError (cas d'erreur)."""
    modele = Modele(nettoyer_donnees(charger_donnees()))
    with pytest.raises(RuntimeError):
        modele.sauvegarder(str(tmp_path))


def test_json_contient_les_bonnes_cles(modele_entraine, tmp_path):
    """Le JSON contient la cible, les variables, les colonnes et les MAE."""
    meta = charger_metadonnees(modele_entraine.sauvegarder_metadonnees(str(tmp_path)))
    for cle in ("cible", "variables", "colonnes_modele", "mae_modele", "mae_reference"):
        assert cle in meta


def test_json_decrit_bien_les_variables(modele_entraine, tmp_path):
    """Chaque type de variable est decrit correctement, sans la cible."""
    meta = charger_metadonnees(modele_entraine.sauvegarder_metadonnees(str(tmp_path)))
    variables = {v["nom"]: v for v in meta["variables"]}
    assert variables["Daily_Usage_Hours"]["type"] == "numerique"
    assert variables["Daily_Usage_Hours"]["min"] <= variables["Daily_Usage_Hours"]["max"]
    assert variables["Primary_Platform"]["type"] == "categorielle"
    assert "TikTok" in variables["Primary_Platform"]["choix"]
    assert "Academic_Performance_GPA" not in variables


def test_charger_metadonnees_absent(tmp_path):
    """Un fichier de metadonnees absent leve FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        charger_metadonnees(os.path.join(str(tmp_path), "absent.json"))