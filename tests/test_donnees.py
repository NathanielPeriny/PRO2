"""Tests du module donnees"""

import os
import pandas as pd
import pytest

from donnees import CHEMIN_CSV, COLONNE_CIBLE, charger_donnees, nettoyer_donnees


def test_fichier_donnees_existe():
    """Le jeu de donnees est bien present dans le dossier donnees/."""
    assert os.path.exists(CHEMIN_CSV)


def test_charger_fichier_inexistant():
    """Un chemin qui n'existe pas leve FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        charger_donnees("fichier_qui_nexiste_pas.csv")




def test_nettoyer_retire_gpa_manquant():
    """Apres le nettoyage, aucune ligne n'a de GPA manquant."""
    propres = nettoyer_donnees(charger_donnees())
    assert propres[COLONNE_CIBLE].isna().sum() == 0



def test_nettoyer_retire_gender():
    """La colonne Gender n'existe plus apres le nettoyage."""
    propres = nettoyer_donnees(charger_donnees())
    assert "Gender" not in propres.columns



def test_nettoyer_remplace_stress_par_mediane():
    """Un stress manquant est remplace par la mediane des autres valeurs."""
    df = pd.DataFrame({
        "Gender": ["Male", "Female", "Male"],
        COLONNE_CIBLE: [3.0, 3.5, 2.5],
        "Perceived_Stress_Score": [10.0, None, 20.0],
    })
    propres = nettoyer_donnees(df)
    assert propres["Perceived_Stress_Score"].iloc[1] == pytest.approx(15.0)