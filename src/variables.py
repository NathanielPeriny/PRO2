""" Classes qui decrivent et valident les variables saisies dans l'interface."""

from abc import ABC, abstractmethod

from exceptions import DonneeInvalideError

class Variable(ABC):
    """Variable d'entree du modele (classe abstraite)."""

    def __init__(self, nom: str, description: str) -> None:
        """nom : nom de la colonne dans le CSV.
           description : texte affiche a l'utilisateur.
           """
        self._nom = nom
        self._description = description



    @property
    def nom(self) -> str:
        """Nom de la colonne (lecture seule)."""
        return self._nom

    @property
    def description(self) -> str:
        """Texte affiche a l'utilisateur (lecture seule)."""
        return self._description

    @abstractmethod
    def valider(self, texte: str):
        """Verifie la saisie et retourne la valeur convertie.

           texte : ce que l'utilisateur a tape ou choisi.
           Leve DonneeInvalideError si la saisie est invalide.
           """


    def __str__(self) -> str:
        return self._description





class VariableNumerique(Variable):
    """Variable numerique avec un minimum et un maximum."""

    def __init__(self, nom: str, description: str, minimum: float, maximum: float) -> None:
        super().__init__(nom, description)
        self._minimum = minimum
        self._maximum = maximum

    def valider(self, texte: str) -> float:
        """Convertit le texte en float et verifie qu'il est dans [minimum, maximum].

           Leve DonneeInvalideError si ce n'est pas un nombre ou s'il est hors limites.
           """

        try:
            valeur = float(texte.strip().replace(",", ".")) #peut entrer 6,5 ou 6.5
        except ValueError:
            raise DonneeInvalideError(f"{self._description} : entrez un nombre.")
        if not self._minimum <= valeur <= self._maximum:
            raise DonneeInvalideError(
                f"{self._description} : entrez un nombre entre {self._minimum} et {self._maximum}.")
        return valeur

    def __repr__(self) -> str:
        return f"VariableNumerique({self._nom!r}, {self._minimum}, {self._maximum})" #met des "" autour du nom


class VariableCategorielle(Variable):
    """Variable dont la valeur doit etre l'un des choix permis"""

    def __init__(self, nom: str, description: str, choix: list[str]) -> None:
        super().__init__(nom, description)
        self._choix = list(choix)

    @property
    def choix(self) -> list[str]:
        """Choix permis (pour remplir la liste deroulante de l'interface)."""
        return list(self._choix) #encapsulation, personne peut changer liste par l'exterieur

    def valider(self, texte: str) -> str:
        """Verifie que le texte fait partie des choix permis et le retourne et leve DonneeInvalideError sinon"""

        if texte not in self._choix:
            raise DonneeInvalideError(f"{self._description} : choisissez une valeur dans la liste.")
        return texte

    def __repr__(self) -> str:
        return f"VariableCategorielle({self._nom!r}, {self._choix})"
