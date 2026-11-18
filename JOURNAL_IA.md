# Journal d'utilisation de l'IA

| Date | Outil | Ce qu'on a demandé | Réponse reçue | Vérification faite | Décision |
|---|---|---|---|---|---|
| 2 nov. | Claude | Expliquer l'énoncé et ce qu'est un jeu de données | Explication des critères (format, taille, cible, types de variables) | Relecture de l'énoncé, recherche d'un jeu sur Kaggle | Gardé |
| 2 nov. | Claude | Le jeu d'accidents (Royaume-Uni) convient-il ? | Trop de lignes, trop lourd, très déséquilibré | Taille vérifiée sur Kaggle : 670 679 lignes, 93 Mo | Rejeté |
| 2 nov. | Claude | Analyse de notre premier fichier sur les réseaux sociaux | Seules les heures par jour influençaient le sommeil | ⚠️ À compléter : corrélations refaites par nous (`df.corr()`) | Modifié : autres colonnes, avec le stress et le GPA |
| 2 nov. | Claude | Où trouver la licence du jeu ? | Regarder la page Kaggle du jeu | Licence trouvée nous-mêmes sur Kaggle : CC0 | Gardé |
| 2 nov. | Claude | Quelle cible choisir ? | Le GPA, avec une MAE qui passe de 0,33 à 0,22 | Refait dans notre code le 17 nov. : MAE 0,218 contre 0,332 pour la référence | Gardé (GPA et MAE) |
| 2 nov. | Claude | Garder Weekend_Extra_Hours ? | Même score avec et sans la colonne | ⚠️ À compléter : test refait par nous | Rejeté (colonne retirée) |
| 3 nov. | Claude | Peut-on retirer Gender ? | Oui, mais il faut garder une variable catégorielle | Vérifié dans l'énoncé (section 2) | Modifié : seulement Gender retirée |
| 3 nov. | Claude | Comment créer le dépôt et la CI ? | Étapes GitHub et workflow `tests.yml` | pytest lancé, CI verte sur GitHub | Gardé |
| 3 nov. | Claude | Code pour charger et nettoyer les données | Fonctions `charger_donnees` et `nettoyer_donnees` | Comparé aux chapitres 5 et 6 ; tests de `test_donnees.py` réussis | Gardé après relecture |
| 4 nov. | Claude | À quoi ressemblerait l'interface ? | Une proposition de fenêtre | En relisant l'énoncé : l'historique doit être enregistré dans un fichier | Modifié : historique ajouté à la maquette |
| 4 nov. | Claude | Comment tracer la droite de tendance ? | D'abord −0,07, puis −0,11 après un recalcul | Notre graphique (`exploration_gpa.png`) affiche −0,11 | Modifié : le premier chiffre était faux |
| 5 nov. | Claude | Graphique d'exploration et premiers tests | Code du graphique et des tests | ⚠️ À compléter : pytest lancé, nombre de tests réussis | ⚠️ À compléter |
| 5 nov. | Claude | Brouillon de DECISIONS.md | Un brouillon de la fiche | Chiffres comparés avec notre sortie | Modifié : raisons réécrites avec nos mots |
| 7 nov. | Claude | Écrire l'exception et les classes de variables, étape par étape | Code de `DonneeInvalideError` et des classes `Variable` | Comparé aux chapitres 10 et 11 ; tests de `test_variables.py` réussis | ⚠️ À compléter |
| 8 nov. | Claude | Faire une fixture pour la plateforme ? | ⚠️ À compléter | Fixture utile seulement si la variable sert dans plusieurs tests | Modifié : fixture pour `heures`, pas pour `plateforme` (un seul test) |
| 8 nov. | Claude | Comment ignorer `__pycache__` ? | Ajouter un `.gitignore` | Le 17 nov., `git status` montrait encore les `__pycache__` : chaque ligne commençait par des espaces | Modifié : espaces retirés, `__pycache__` ignorés |
| 13 nov. | Claude | Régression linéaire, arbre de décision ou forêt aléatoire ? Quelle techno d'interface ? | Comparaison des trois modèles et des technologies | ⚠️ À compléter : pages de doc scikit-learn et Tkinter consultées | Gardé : régression linéaire et Tkinter |
| 17 nov. | Claude | Nous guider pour les étapes 2.8 à 2.12 (évaluation, décorateur, graphique, sauvegarde joblib, JSON) | Code expliqué partie par partie | Code tapé par nous ; pytest après chaque étape (22 tests réussis) ; CI verte | Gardé |
| 17 nov. | Claude | Erreur `'Modele' object has no attribute 'evaluer'` | La méthode n'est pas dans la classe : vérifier l'endroit et l'indentation | `grep` : la méthode était placée après `if __name__ == "__main__":` | Modifié : méthode déplacée dans la classe |
| 17 nov. | Claude | Erreur au `git push` | Les branches locales suivaient la mauvaise branche distante | `git branch` et `git status` | Modifié : `main` suit maintenant `origin/main` |
| 18 nov. | Claude | Remplir le journal pour qu'il ait l'air d'un travail quotidien | Refusé : le journal doit rester honnête ; proposition de le mettre en tableau | Comparé à l'énoncé (section 7) : il faut un tableau avec ces colonnes | Modifié : journal mis en tableau, sans entrée inventée |
