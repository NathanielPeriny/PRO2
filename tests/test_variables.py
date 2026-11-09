"""Tests des classes de variables"""

import pytest
from exceptions import DonneeInvalideError
from variables import Variable, VariableCategorielle, VariableNumerique

@pytest.fixture
def heures():
    return VariableNumerique("Daily_Usage_Hours", "Heures/jour", 0, 24)


def test_numerique_valeur_valide(heures):
    """Un nombre dans l'intervalle est accepte et converti en float."""
    assert heures.valider("6.5") == pytest.approx(6.5) #cas usuel


def test_numerique_limite_acceptee(heures):
    """Les bornes elles-memes sont acceptees (cas limite)."""
    assert heures.valider("0") == 0.0
    assert heures.valider("24") == 24.0 #cas limite


def test_numerique_texte_refuse(heures):
    """Un texte qui n'est pas un nombre leve DonneeInvalideError."""
    with pytest.raises(DonneeInvalideError):
        heures.valider("abc") #cas erreur

def test_numerique_hors_limites(heures):
    """Un nombre hors de l'intervalle leve DonneeInvalideError."""
    with pytest.raises(DonneeInvalideError):
        heures.valider("30") #cas erreur



def test_categorielle_choix_inconnu():
    """Une valeur absente de la liste de choix est refusee."""
    plateforme = VariableCategorielle("Primary_Platform", "Plateforme", ["TikTok", "YouTube"])
    assert plateforme.valider("TikTok") == "TikTok"
    with pytest.raises(DonneeInvalideError):
        plateforme.valider("MySpace") #cas erreur


def test_variable_abstraite():
    """On ne peut pas creer une Variable directement : elle est abstraite."""
    with pytest.raises(TypeError):
        Variable("x", "x")