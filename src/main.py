"""Point d'entree : lance l'application de prediction du GPA."""

import tkinter as tk
from tkinter import messagebox

from application import Application
from interface import Interface


def main() -> None:
    """Charge le modele et ouvre la fenetre principale."""
    racine = tk.Tk()
    try:
        application = Application()
    except FileNotFoundError as erreur:
        racine.withdraw()
        messagebox.showerror("Modele introuvable", str(erreur))
        return
    Interface(racine, application)
    racine.mainloop()


if __name__ == "__main__":
    main()