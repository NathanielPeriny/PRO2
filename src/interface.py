"""Interface graphique Tkinter : affiche et appelle Application, sans calculs."""

import tkinter as tk
from tkinter import ttk

from application import Application
from variables import VariableCategorielle
from exceptions import DonneeInvalideError
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Interface:
    """Fenetre principale : un champ par variable du modele."""

    def __init__(self, racine: tk.Tk, application: Application) -> None:
        """racine : fenetre Tkinter principale.
           application : logique du projet (modele et variables).
           """
        self._racine = racine
        self._application = application
        self._champs: dict[str, ttk.Widget] = {}
        self._canevas: FigureCanvasTkAgg | None = None

        self._racine.title("Estimation du GPA selon les habitudes")
        self._cadre_saisies = ttk.LabelFrame(self._racine, text="Vos habitudes", padding=10)
        self._cadre_saisies.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self._creer_champs()
        self._creer_zone_resultat()
        self._afficher_graphique()

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
    def _creer_zone_resultat(self) -> None:
        """Cree le bouton Predire et l'etiquette qui affiche le resultat."""
        cadre = ttk.Frame(self._racine, padding=(10, 0, 10, 10))
        cadre.grid(row=1, column=0, sticky="nsew")
        bouton = ttk.Button(cadre, text="Prédire", command=self._au_clic_predire)
        bouton.grid(row=0, column=0, sticky="w")
        self._etiquette_resultat = ttk.Label(cadre, text="", wraplength=380, justify="left")
        self._etiquette_resultat.grid(row=1, column=0, sticky="w", pady=(10, 0))

    def _au_clic_predire(self) -> None:
        """Lit les champs, predit et affiche le resultat ou l'erreur en rouge."""
        try:
            gpa = self._application.predire(self.lire_saisies())
        except DonneeInvalideError as erreur:
            self._etiquette_resultat.config(text=str(erreur), foreground="red")
            return
        self._etiquette_resultat.config(text=self._application.decrire_resultat(gpa),
                                        foreground="black")
        self._afficher_graphique(gpa)
        
    def _afficher_graphique(self, gpa: float | None = None) -> None:
        """Remplace le graphique de la fenetre par un nouveau (avec le GPA s'il est donne)."""
        if self._canevas is not None:
            self._canevas.get_tk_widget().destroy()
        figure = self._application.creer_figure_distribution(gpa)
        self._canevas = FigureCanvasTkAgg(figure, master=self._racine)
        self._canevas.draw()
        self._canevas.get_tk_widget().grid(row=0, column=1, rowspan=2, padx=10, pady=10)

    def lire_saisies(self) -> dict[str, str]:
        """Retourne {nom de colonne: texte du champ} pour toutes les variables."""
        return {nom: champ.get() for nom, champ in self._champs.items()}