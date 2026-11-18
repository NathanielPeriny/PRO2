"""Interface graphique Tkinter : affiche et appelle Application, sans calculs."""

import tkinter as tk
from tkinter import ttk

from application import Application
from variables import VariableCategorielle


class Interface:
    """Fenetre principale : un champ par variable du modele."""

    def __init__(self, racine: tk.Tk, application: Application) -> None:
        """racine : fenetre Tkinter principale.
           application : logique du projet (modele et variables).
           """
        self._racine = racine
        self._application = application
        self._champs: dict[str, ttk.Widget] = {}

        self._racine.title("Estimation du GPA selon les habitudes")
        self._cadre_saisies = ttk.LabelFrame(self._racine, text="Vos habitudes", padding=10)
        self._cadre_saisies.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self._creer_champs()

    def _creer_champs(self) -> None:
        """Cree une etiquette et un champ adapte au type de chaque variable."""
        for ligne, variable in enumerate(self._application.variables):
            etiquette = ttk.Label(self._cadre_saisies, text=str(variable))
            etiquette.grid(row=ligne, column=0, sticky="w", pady=3)
            if isinstance(variable, VariableCategorielle):
                champ = ttk.Combobox(self._cadre_saisies, values=variable.choix,
                                     state="readonly", width=20)
            else:
                champ = ttk.Entry(self._cadre_saisies, width=22)
            champ.grid(row=ligne, column=1, sticky="w", padx=(10, 0), pady=3)
            self._champs[variable.nom] = champ

    def lire_saisies(self) -> dict[str, str]:
        """Retourne {nom de colonne: texte du champ} pour toutes les variables."""
        return {nom: champ.get() for nom, champ in self._champs.items()}