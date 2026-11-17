"""Entrainement et evaluation du modele de prediction du GPA"""

import functools
import os
import time
import numpy as np
import pandas as pd
import joblib
from matplotlib.figure import Figure
from sklearn.linear_model import LinearRegression # le modele
from sklearn.model_selection import train_test_split # ca split les donnees

from donnees import COLONNE_CIBLE, DOSSIER_FIGURES, charger_donnees, nettoyer_donnees

GRAINE = 42             # graine (seed) fixe : le split est random mais separation est toujours la meme (le meme random a chaque fois)
PROPORTION_TEST = 0.2   # 20 % des lignes servent au test
DOSSIER_MODELES = os.path.join(os.path.dirname(__file__), "..", "modeles")
NOM_FICHIER_MODELE = "modele_gpa.joblib"

def chronometrer(fonction):
    """Decorateur qui mesure la duree d'execution d'une fonction.

       fonction : la fonction a chronometrer.
       Retourne une fonction enveloppe qui appelle fonction, affiche sa
       duree dans la console et retourne son resultat sans le modifier.
       """
    @functools.wraps(fonction)
    def enveloppe(*args, **kwargs):
        debut = time.perf_counter()
        resultat = fonction(*args, **kwargs)
        duree = time.perf_counter() - debut
        print(f"[chronometrer] {fonction.__name__} : {duree:.3f} s")
        return resultat
    return enveloppe

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
        self._est_entraine = False

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

    @chronometrer
    def entrainer(self) -> None:
        """Entraine la regression lineaire sur l'ensemble d'entrainement."""
        self._regression.fit(self._x_entrainement, self._y_entrainement) # fit est l'entrainement
        self._est_entraine = True

    def predire_test(self) -> np.ndarray:
        """Predit le GPA de chaque ligne de l'ensemble de test.

           Retourne un tableau NumPy de GPA predits.
           Leve RuntimeError si le modele n'est pas encore entraine.
           """
        if not self._est_entraine:
            raise RuntimeError("Appeler preparer() puis entrainer() avant de predire.")
        return self._regression.predict(self._x_test)
    
    def evaluer(self) -> dict[str, float]:
        """Compare la MAE du modele a celle de la reference, sur le test.

           Retourne un dictionnaire avec mae_modele, mae_reference et
           amelioration_pct (baisse de l'erreur en %, positive si le modele
           fait mieux que la reference).
           Leve RuntimeError si le modele n'est pas encore entraine.
           """
        y_predit = self.predire_test()
        y_reference = np.full(len(self._y_test), self._moyenne_reference)
        mae_modele = calculer_mae(self._y_test, y_predit)
        mae_reference = calculer_mae(self._y_test, y_reference)
        amelioration = 0.0
        if mae_reference > 0:
            amelioration = 100 * (mae_reference - mae_modele) / mae_reference
        return {
            "mae_modele": mae_modele,
            "mae_reference": mae_reference,
            "amelioration_pct": amelioration,
        }
    def creer_figure_predit_reel(self) -> Figure:
        """Cree le graphique GPA predit contre GPA reel sur l'ensemble de test.

           Retourne une figure Matplotlib avec titre, axes etiquetes et legende.
           Leve RuntimeError si le modele n'est pas encore entraine.
           """
        y_predit = self.predire_test()
        y_reel = np.asarray(self._y_test, dtype=float)
        mae = calculer_mae(y_reel, y_predit)

        figure = Figure(figsize=(6, 5))
        axe = figure.add_subplot()
        axe.scatter(y_reel, y_predit, alpha=0.4, s=15, label="Etudiants du test")
        bornes = [min(y_reel.min(), y_predit.min()), max(y_reel.max(), y_predit.max())]
        axe.plot(bornes, bornes, color="red", linestyle="--", label="Prediction parfaite")
        axe.axhline(self._moyenne_reference, color="gray", linestyle=":",
                    label=f"Reference (moyenne = {self._moyenne_reference:.2f})")
        axe.set_title(f"GPA predit contre GPA reel (MAE = {mae:.3f})")
        axe.set_xlabel("GPA reel")
        axe.set_ylabel("GPA predit")
        axe.legend()
        figure.tight_layout()
        return figure
    
    def sauvegarder(self, dossier: str = DOSSIER_MODELES) -> str:
        """Enregistre la regression entrainee dans un fichier joblib.

           dossier : dossier de destination (cree s'il n'existe pas).
           Retourne le chemin du fichier cree.
           Leve RuntimeError si le modele n'est pas encore entraine.
           """
        if not self._est_entraine:
            raise RuntimeError("Entrainer le modele avant de le sauvegarder.")
        os.makedirs(dossier, exist_ok=True)
        chemin_modele = os.path.join(dossier, NOM_FICHIER_MODELE)
        joblib.dump(self._regression, chemin_modele)
        return chemin_modele    


    
if __name__ == "__main__":
    modele = Modele(nettoyer_donnees(charger_donnees())) # le modele utilise les donnees qu'on veut qu'il utilise
    modele.preparer() # appelle la methode
    print("Lignes d'entrainement :", len(modele._x_entrainement))
    print("Lignes de test        :", len(modele._x_test))
    print("Reference (GPA moyen) :", round(modele._moyenne_reference, 2))

    modele.entrainer()
    for colonne, poids in zip(modele._colonnes, modele._regression.coef_): #coef est le poids (pondération)
        print(f"{colonne:40} {poids:+.3f}")

    resultats = modele.evaluer()
    print("MAE du modele     :", round(resultats["mae_modele"], 3))
    print("MAE de reference  :", round(resultats["mae_reference"], 3))
    print("Amelioration      :", round(resultats["amelioration_pct"], 1), "%")    

    os.makedirs(DOSSIER_FIGURES, exist_ok=True)
    chemin_figure = os.path.join(DOSSIER_FIGURES, "predit_contre_reel.png")
    modele.creer_figure_predit_reel().savefig(chemin_figure, dpi=150)

    print("Graphique enregistre :", chemin_figure)
    print("Modele enregistre :", modele.sauvegarder())
