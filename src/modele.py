"""Entrainement et evaluation du modele de prediction du GPA"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression # le modele
from sklearn.model_selection import train_test_split # ca split les donnees

from donnees import COLONNE_CIBLE, charger_donnees, nettoyer_donnees

GRAINE = 42             # graine (seed) fixe : le split est random mais separation est toujours la meme (le meme random a chaque fois)
PROPORTION_TEST = 0.2   # 20 % des lignes servent au test

def calculer_mae(y_reel: np.ndarray, y_predit: np.ndarray) -> float:
    """Erreur absolue moyenne, calculee avec NumPy (sans boucle).

       y_reel : valeurs reelles.
       y_predit : valeurs predites, dans le meme ordre.
       Retourne la moyenne des ecarts absolus.
       """
    return float(np.mean(np.abs(np.asarray(y_reel) - np.asarray(y_predit)))) 
    # np.asarray transforme la liste en NumPy arrays
    # y_reel - y_predit donne toutes les erreurs en mm temps sans boucle (vectorization), on peut pas faire np.asarray(y_reel - y_predit)
    # on doit les transformer en NumPy arrays pour les soustraire.
    # np.abs enleve le signe puisqu'on regarde seulement si un ecart est trop grand peut importe la direction (haut ou bas)
    # np.mean donne la moyenne (mean)
    # float() retourne un nombre Python normal

class Modele:
    """Regression lineaire qui predit le GPA a partir des habitudes"""
    def __init__(self, donnees: pd.DataFrame) -> None:
        """donnees : DataFrame nettoye, qui contient la colonne cible."""
        self._donnees = donnees
        self._regression = LinearRegression()
        self._colonnes = []
        self._x_entrainement = None
        self._x_test = None
        self._y_entrainement = None
        self._y_test = None
        self._moyenne_reference = None

    def preparer(self) -> None:
        """Transforme les categories en colonnes 0/1 et separe entrainement / test.
           Calcule aussi la prediction de reference : le GPA moyen de l'entrainement.
           """
        x = pd.get_dummies(self._donnees.drop(columns=[COLONNE_CIBLE]), dtype=float) 
        
        # toutes les donnees sans GPA (habitudes)
        # pd.getdummies : un modèle comprend seulement les nombres donc Primary_Platform_Tiktok 
        # vaut 1 et les autres colonnes de platefroms vallent 0

        y = self._donnees[COLONNE_CIBLE] # GPA
        self._colonnes = list(x.columns)
        (self._x_entrainement, self._x_test, self._y_entrainement, self._y_test) = train_test_split(x, y, test_size=PROPORTION_TEST, random_state=GRAINE)
        self._moyenne_reference = float(self._y_entrainement.mean())

        # train_test_split mélange et coupe les donnees en 80% entrainement et 20% test (comme deux simule pratiques vs le vrai CP1)
        # self._moyenne_reference : le modele paresseux de base va toujours deviner cette valeur, Lucas va faire evaluer() pour voir
        # notre modele est plus precis

    def entrainer(self) -> None:
        """Entraine la regression lineaire sur l'ensemble d'entrainement."""
        self._regression.fit(self._x_entrainement, self._y_entrainement) # fit est l'entrainement
        # scikit-learn trouve les meilleures ponderation (a quelle pourcentage chaque covariable, 
        # fit recoit seulement
        # les donnees d'entrainement (80%) des donnees coupées par train_test_split, 
        # si le modele voyait les donnees test
        # c'est comme lui donner les reponses d'examen avant l'examen
        # au lieu de lui faire passer la simule seulement)


if __name__ == "__main__":
    modele = Modele(nettoyer_donnees(charger_donnees())) # le modele utilise les donnees qu'on veut qu'il utilise
    modele.preparer() # appelle la methode
    print("Lignes d'entrainement :", len(modele._x_entrainement))
    print("Lignes de test        :", len(modele._x_test))
    print("Reference (GPA moyen) :", round(modele._moyenne_reference, 2))

    modele.entrainer()
    for colonne, poids in zip(modele._colonnes, modele._regression.coef_): #coef est le poids (pondération)
        print(f"{colonne:40} {poids:+.3f}")

    y_predit = modele._regression.predict(modele._x_test)
    print("MAE du modele sur le test :", round(calculer_mae(modele._y_test, y_predit), 3)) # gpa testé et prédit

