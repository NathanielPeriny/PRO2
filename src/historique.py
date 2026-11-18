"""Historique des predictions, enregistre dans un fichier CSV."""

import csv
import os
from datetime import datetime
from typing import Iterator


class Historique:
    """Ajoute et relit les predictions dans un fichier CSV."""

    def __init__(self, chemin: str, colonnes: list[str]) -> None:
        """chemin : fichier CSV de l'historique (cree a la 1re prediction).
           colonnes : noms des variables d'entree, dans l'ordre.
           """
        self._chemin = chemin
        self._colonnes = ["date"] + list(colonnes) + ["gpa_estime"]

    @property
    def colonnes(self) -> list[str]:
        """Copie des colonnes du fichier (pour construire le tableau de l'interface)."""
        return list(self._colonnes)

    def ajouter(self, valeurs: dict, gpa: float) -> None:
        """Ajoute une prediction a la fin du fichier (avec l'en-tete si nouveau).

           valeurs : {nom de colonne: valeur validee}.
           gpa : GPA estime.
           """
        dossier = os.path.dirname(self._chemin)
        if dossier:
            os.makedirs(dossier, exist_ok=True)
        nouveau = not os.path.exists(self._chemin)
        ligne = {"date": datetime.now().strftime("%Y-%m-%d %H:%M"), **valeurs,
                 "gpa_estime": round(gpa, 2)}
        with open(self._chemin, "a", newline="", encoding="utf-8") as fichier:
            ecrivain = csv.DictWriter(fichier, fieldnames=self._colonnes)
            if nouveau:
                ecrivain.writeheader()
            ecrivain.writerow(ligne)

    def lignes(self) -> Iterator[dict[str, str]]:
        """Generateur : donne les predictions une par une, de la plus ancienne a la plus recente.

           Ne donne rien si le fichier n'existe pas encore.
           """
        if not os.path.exists(self._chemin):
            return
        with open(self._chemin, newline="", encoding="utf-8") as fichier:
            for ligne in csv.DictReader(fichier):
                yield ligne

    def __len__(self) -> int:
        """Nombre de predictions enregistrees."""
        return sum(1 for _ in self.lignes())