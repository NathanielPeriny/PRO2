"""Lecture, nettoyage et exploration du jeu de donnees."""

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

CHEMIN_CSV = os.path.join(os.path.dirname(__file__), "..", "donnees", "social_media.csv")
DOSSIER_FIGURES = os.path.join(os.path.dirname(__file__), "..", "figures")
COLONNE_CIBLE = "Academic_Performance_GPA"
COLONNES_RETIREES = ["Gender"]  # aucun effet sur le GPA (correlation proche de 0)


def charger_donnees(chemin: str = CHEMIN_CSV) -> pd.DataFrame:
    """Lit le jeu de donnees et le retourne en DataFrame.

       chemin : chemin du fichier CSV.
       Leve FileNotFoundError si le fichier n'existe pas.
       """
    if not os.path.exists(chemin):
        raise FileNotFoundError(f"Fichier introuvable : {chemin}")
    with open(chemin, encoding="utf-8") as fichier:
        return pd.read_csv(fichier)


def nettoyer_donnees(df: pd.DataFrame) -> pd.DataFrame:
    """Retourne une copie nettoyee du DataFrame.

       df : donnees brutes.
       Retire les colonnes sans effet sur la cible, retire les lignes sans GPA
       (on ne peut pas apprendre sans la reponse) et remplace le stress manquant
       par la mediane.
       """
    df = df.drop(columns=COLONNES_RETIREES)
    df = df.dropna(subset=[COLONNE_CIBLE]).copy()
    mediane_stress = df["Perceived_Stress_Score"].median()
    df["Perceived_Stress_Score"] = df["Perceived_Stress_Score"].fillna(mediane_stress)
    return df




#draw graph

def tracer_exploration(df: pd.DataFrame, chemin_sortie: str) -> None:
    """Trace le GPA selon les heures quotidiennes, avec la droite de tendance.

       df : donnees nettoyees.
       chemin_sortie : chemin du fichier image a creer (.png).
       """
    x = df["Daily_Usage_Hours"].to_numpy()
    y = df[COLONNE_CIBLE].to_numpy()

    pente, ordonnee = np.polyfit(x, y, 1)        # droite y = pente * x + ordonnee
    x_droite = np.linspace(x.min(), x.max(), 100)
    y_droite = pente * x_droite + ordonnee

    fig, ax = plt.subplots()
    ax.scatter(x, y, alpha=0.3, s=10, label="Etudiants")
    ax.plot(x_droite, y_droite, color="red", linewidth=2,
            label=f"Tendance : {pente:.2f} point de GPA par heure")
    ax.set_title("GPA selon le temps passe sur les reseaux sociaux")
    ax.set_xlabel("Heures par jour sur les reseaux sociaux")
    ax.set_ylabel("GPA")
    ax.legend()
    fig.savefig(chemin_sortie)
    plt.close(fig)


if __name__ == "__main__":
    donnees = charger_donnees()
    print("Avant nettoyage :", donnees.shape)
    print("Valeurs manquantes :")
    print(donnees.isna().sum())
    print(donnees.describe().T)   # .T : une ligne par colonne, plus lisible

    propres = nettoyer_donnees(donnees)
    print("Apres nettoyage :", propres.shape)

    if not os.path.exists(DOSSIER_FIGURES):
        os.mkdir(DOSSIER_FIGURES)
    chemin_figure = os.path.join(DOSSIER_FIGURES, "exploration_gpa.png")
    tracer_exploration(propres, chemin_figure)
    print("Graphique enregistre :", chemin_figure)