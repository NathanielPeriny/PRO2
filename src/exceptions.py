"""Exceptions du projet"""

class ProjetError(Exception):
    """Erreur de base du projet"""

class DonneeInvalideError(ProjetError):
    """Une saise de l'utilisateur est invalide"""