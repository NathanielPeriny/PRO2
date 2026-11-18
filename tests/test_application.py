"""Tests de la classe Application (sans interface)."""

import pytest

from application import Application
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