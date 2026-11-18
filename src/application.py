"""Logique de l'application : charge le modele et construit les variables."""

import os

import joblib

from modele import (DOSSIER_MODELES, NOM_FICHIER_METADONNEES, NOM_FICHIER_MODELE,
                    charger_metadonnees)
from variables import Variable, VariableCategorielle, VariableNumerique


def creer_variable(description: dict) -> Variable:
    """Cree la bonne sorte de Variable a partir de sa description JSON.

       description : un element de la liste "variables" des metadonnees.
       Retourne une VariableNumerique ou une VariableCategorielle.
       """
    if description["type"] == "numerique":
        return VariableNumerique(description["nom"], description["description"],
                                 description["min"], description["max"])
    return VariableCategorielle(description["nom"], description["description"],
                                description["choix"])


class Application:
    """Contient le modele entraine et la liste des variables (composition)."""

    def __init__(self, dossier: str = DOSSIER_MODELES) -> None:
        """Charge le modele et ses metadonnees depuis le dossier.

           dossier : dossier qui contient le .joblib et le .json.
           Leve FileNotFoundError si un des deux fichiers est absent.
           """
        chemin_modele = os.path.join(dossier, NOM_FICHIER_MODELE)
        if not os.path.exists(chemin_modele):
            raise FileNotFoundError(
                f"Modele introuvable : {chemin_modele}. Lancer d'abord python src/modele.py")
        self._metadonnees = charger_metadonnees(os.path.join(dossier, NOM_FICHIER_METADONNEES))
        self._regression = joblib.load(chemin_modele)
        self._variables = [creer_variable(d) for d in self._metadonnees["variables"]]

    @property
    def variables(self) -> list[Variable]:
        """Copie de la liste des variables (pour construire les champs)."""
        return list(self._variables)

    @property
    def mae(self) -> float:
        """Erreur moyenne du modele sur le test (pour l'afficher a l'utilisateur)."""
        return self._metadonnees["mae_modele"]

    def __repr__(self) -> str:
        return f"Application({len(self._variables)} variables, MAE={self.mae:.3f})"