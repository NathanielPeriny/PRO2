"""Logique de l'application : charge le modele et construit les variables."""

import os

import joblib
import numpy as np
import pandas as pd
from matplotlib.figure import Figure
from historique import Historique

from modele import (DOSSIER_MODELES, NOM_FICHIER_METADONNEES, NOM_FICHIER_MODELE,
charger_metadonnees)
from donnees import COLONNE_CIBLE, charger_donnees, nettoyer_donnees

from variables import Variable, VariableCategorielle, VariableNumerique

GPA_MIN = 0.0
GPA_MAX = 4.0
CHEMIN_HISTORIQUE = os.path.join(os.path.dirname(__file__), "..", "historique", "historique.csv")

def formater_nombre(valeur: float) -> str:
    """Retourne le nombre avec 2 decimales et une virgule (ex. 3.456 -> "3,46")."""
    return f"{valeur:.2f}".replace(".", ",")

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

    def __init__(self, dossier: str = DOSSIER_MODELES, chemin_historique: str = CHEMIN_HISTORIQUE) -> None:
        """Charge le modele et ses metadonnees depuis le dossier.

           dossier : dossier qui contient le .joblib et le .json.
           chemin_historique : fichier CSV ou enregistrer les predictions.
           Leve FileNotFoundError si un des deux fichiers est absent.
           """
        chemin_modele = os.path.join(dossier, NOM_FICHIER_MODELE)
        if not os.path.exists(chemin_modele):
            raise FileNotFoundError(
                f"Modele introuvable : {chemin_modele}. Lancer d'abord python src/modele.py")
        self._metadonnees = charger_metadonnees(os.path.join(dossier, NOM_FICHIER_METADONNEES))
        self._regression = joblib.load(chemin_modele)
        self._variables = [creer_variable(d) for d in self._metadonnees["variables"]]
        self._gpa_etudiants = nettoyer_donnees(charger_donnees())[COLONNE_CIBLE].to_numpy()
        self._historique = Historique(chemin_historique, [v.nom for v in self._variables])
    
    @property
    def variables(self) -> list[Variable]:
        """Copie de la liste des variables (pour construire les champs)."""
        return list(self._variables)

    @property
    def mae(self) -> float:
        """Erreur moyenne du modele sur le test (pour l'afficher a l'utilisateur)."""
        return self._metadonnees["mae_modele"]
    @property
    def historique(self) -> Historique:
        """Historique des predictions (pour l'afficher dans l'interface)."""
        return self._historique

    def valider_saisies(self, saisies: dict[str, str]) -> dict:
        """Valide chaque saisie avec la Variable correspondante.

           saisies : {nom de colonne: texte tape ou choisi par l'utilisateur}.
           Retourne {nom de colonne: valeur convertie (float ou str)}.
           Leve DonneeInvalideError a la premiere saisie vide, non numerique,
           hors intervalle ou hors des choix permis.
           """
        valeurs = {}
        for variable in self._variables:
            valeurs[variable.nom] = variable.valider(saisies.get(variable.nom, ""))
        return valeurs

    def predire(self, saisies: dict[str, str]) -> float:
        """Valide les saisies et predit le GPA, limite entre GPA_MIN et GPA_MAX.

           saisies : {nom de colonne: texte tape ou choisi par l'utilisateur}.
           Retourne le GPA estime.
           Leve DonneeInvalideError si une saisie est invalide.
           """
        valeurs = self.valider_saisies(saisies)
        ligne = pd.get_dummies(pd.DataFrame([valeurs]), dtype=float)
        ligne = ligne.reindex(columns=self._metadonnees["colonnes_modele"], fill_value=0.0)
        gpa = float(self._regression.predict(ligne)[0])
        return float(np.clip(gpa, GPA_MIN, GPA_MAX))
    
    def enregistrer(self, saisies: dict[str, str], gpa: float) -> None:
        """Ajoute une prediction valide a l'historique.

           saisies : textes de l'utilisateur. gpa : GPA estime par predire().
           Leve DonneeInvalideError si une saisie est invalide.
           """
        self._historique.ajouter(self.valider_saisies(saisies), gpa)
        
    def decrire_resultat(self, gpa: float) -> str:
        """Explique le GPA estime a un non-informaticien, avec l'erreur moyenne.

           gpa : GPA estime par predire().
           Retourne un texte de deux phrases.
           """
        bas = max(GPA_MIN, gpa - self.mae)
        haut = min(GPA_MAX, gpa + self.mae)
        return (f"GPA estimé : {formater_nombre(gpa)} sur 4.\n"
                f"En moyenne, le modèle se trompe de {formater_nombre(self.mae)} point : "
                f"le vrai GPA se situe souvent entre {formater_nombre(bas)} "
                f"et {formater_nombre(haut)}.")
    def creer_figure_distribution(self, gpa: float | None = None) -> Figure:
        """Histogramme des GPA du jeu de donnees, avec le GPA estime s'il est donne.

           gpa : GPA estime a placer sur le graphique (None avant la 1re prediction).
           Retourne une figure Matplotlib avec titre, axes etiquetes et legende.
           """
        figure = Figure(figsize=(5, 3.5))
        axe = figure.add_subplot()
        axe.hist(self._gpa_etudiants, bins=30, color="steelblue", alpha=0.7,
                 label="Étudiants du jeu de données")
        if gpa is not None:
            axe.axvspan(max(GPA_MIN, gpa - self.mae), min(GPA_MAX, gpa + self.mae),
                        color="red", alpha=0.15, label="Marge d'erreur moyenne")
            axe.axvline(gpa, color="red", linewidth=2,
                        label=f"Votre GPA estimé ({formater_nombre(gpa)})")
        axe.set_title(f"Votre GPA estimé parmi {len(self._gpa_etudiants)} étudiants")
        axe.set_xlabel("GPA")
        axe.set_ylabel("Nombre d'étudiants")
        axe.legend(loc="upper left")
        figure.tight_layout()
        return figure

    def __repr__(self) -> str:
        return f"Application({len(self._variables)} variables, MAE={self.mae:.3f})"