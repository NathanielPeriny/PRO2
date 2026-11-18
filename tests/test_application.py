"""Tests de la classe Application (sans interface)."""

from exceptions import DonneeInvalideError

import pytest

from application import Application, formater_nombre
from variables import VariableCategorielle, VariableNumerique


@pytest.fixture
def application():
    """Application chargee depuis le vrai dossier modeles/."""
    return Application()


def test_application_construit_les_variables(application):
    """Les 7 variables du JSON sont creees avec la bonne classe."""
    variables = application.variables
    assert len(variables) == 7
    numeriques = [v for v in variables if isinstance(v, VariableNumerique)]
    categorielles = [v for v in variables if isinstance(v, VariableCategorielle)]
    assert len(numeriques) == 5
    assert len(categorielles) == 2


def test_application_dossier_absent(tmp_path):
    """Un dossier sans modele leve FileNotFoundError (cas d'erreur)."""
    with pytest.raises(FileNotFoundError):
        Application(str(tmp_path))



@pytest.fixture
def saisies():
    """Saisies valides d'un etudiant typique (du texte, comme dans l'interface)."""
    return {
        "Age": "19",
        "Academic_Level": "Undergraduate",
        "Primary_Platform": "TikTok",
        "Daily_Usage_Hours": "3",
        "Sleep_Duration_Hours": "8",
        "Sleep_Quality_Score": "4",
        "Perceived_Stress_Score": "10",
    }


def test_predire_cas_usuel(application, saisies):
    """Une saisie valide donne un GPA entre 0 et 4."""
    assert 0.0 <= application.predire(saisies) <= 4.0


def test_predire_bonnes_habitudes_meilleur_gpa(application, saisies):
    """Moins d'ecran, plus de sommeil et moins de stress donnent un GPA plus eleve."""
    mauvaises = dict(saisies, Daily_Usage_Hours="12", Sleep_Duration_Hours="4",
                     Perceived_Stress_Score="35")
    assert application.predire(saisies) > application.predire(mauvaises)


def test_predire_plafonne_a_4(application, saisies):
    """Le profil ideal donnerait plus de 4 : le resultat est limite a 4 (cas limite)."""
    ideal = dict(saisies, Daily_Usage_Hours="0,9", Sleep_Duration_Hours="10,5",
                 Sleep_Quality_Score="5", Perceived_Stress_Score="0")
    assert application.predire(ideal) == pytest.approx(4.0)


def test_predire_saisie_vide(application, saisies):
    """Un champ vide leve DonneeInvalideError (cas d'erreur)."""
    saisies["Daily_Usage_Hours"] = ""
    with pytest.raises(DonneeInvalideError):
        application.predire(saisies)


def test_predire_hors_intervalle(application, saisies):
    """Des heures de sommeil impossibles levent DonneeInvalideError (cas d'erreur)."""
    saisies["Sleep_Duration_Hours"] = "30"
    with pytest.raises(DonneeInvalideError):
        application.predire(saisies)


def test_predire_categorie_inconnue(application, saisies):
    """Une plateforme absente de la liste leve DonneeInvalideError (cas d'erreur)."""
    saisies["Primary_Platform"] = "MySpace"
    with pytest.raises(DonneeInvalideError):
        application.predire(saisies)


def test_formater_nombre_virgule():
    """Les nombres sont affiches avec une virgule et 2 decimales."""
    assert formater_nombre(3.456) == "3,46"


def test_decrire_resultat(application):
    """Le texte donne le GPA et une marge bornee a 4 (cas limite)."""
    texte = application.decrire_resultat(3.9)
    assert "3,90 sur 4" in texte
    assert "et 4,00" in texte


def test_figure_sans_prediction(application):
    """Avant toute prediction : histogramme avec titre et axes, sans ligne rouge."""
    axe = application.creer_figure_distribution().axes[0]
    assert axe.get_title() != ""
    assert axe.get_xlabel() == "GPA"
    assert axe.get_ylabel() == "Nombre d'étudiants"
    assert len(axe.lines) == 0


def test_figure_avec_prediction(application):
    """Apres une prediction : une ligne rouge et une legende."""
    axe = application.creer_figure_distribution(3.5).axes[0]
    assert len(axe.lines) == 1
    assert axe.get_legend() is not None
    