# Journal IA
 
On a surtout utilisé Claude
 
| Date | Outil | Ce qu'on a demandé | Réponse reçue | Vérification faite | Décision |
|---|---|---|---|---|---|
| 2 nov | Claude | Expliquer l'énoncé et ce que c'est un jeu de données | Il a expliqué les critères (taille, cible, types de colonnes) | On a relu l'énoncé et cherché un jeu sur Kaggle | Gardé |
| 2 nov | Claude | Si le jeu sur les accidents (UK) était correct | Trop de lignes, trop lourd, très déséquilibré | On a regardé sur Kaggle : 670 679 lignes, 93 Mo | Rejeté |
| 2 nov | Claude | Analyser notre premier fichier sur les réseaux sociaux | Seulement les heures par jour avaient un effet sur le sommeil | Le 21 nov on a refait les corrélations sur notre fichier final : heures par jour -0,71, stress -0,65, sommeil 0,60, qualité du sommeil 0,53, âge 0,03 | Modifié : on a pris d'autres colonnes, avec le stress et le GPA |
| 2 nov | Claude | Où trouver la licence | Sur la page Kaggle du jeu | On l'a trouvée nous-mêmes : CC0 | Gardé |
| 2 nov | Claude | Quelle cible choisir | Le GPA, avec une erreur qui passe de 0,33 à 0,22 | Refait dans notre code le 17 nov : MAE 0,218 contre 0,332 | Gardé |
| 2 nov | Claude | Si on garde Weekend_Extra_Hours | Même score avec ou sans | Refait par nous le 21 nov : MAE 0,215 avec et sans | Rejeté, colonne enlevée |
| 3 nov | Claude | Si on peut enlever Gender | Oui mais il faut garder une variable catégorielle | Vérifié dans l'énoncé (section 2) | Modifié : on enlève juste Gender |
| 3 nov | Claude | Comment faire le dépôt et la CI | Les étapes GitHub et le fichier tests.yml | pytest marche, CI verte sur GitHub | Gardé |
| 3 nov | Claude | Du code pour charger et nettoyer les données | charger_donnees et nettoyer_donnees | Comparé avec les chapitres 5 et 6, tests de test_donnees.py réussis | Gardé après relecture |
| 4 nov | Claude | À quoi pourrait ressembler l'interface | Une idée de fenêtre | En relisant l'énoncé on a vu que l'historique doit être dans un fichier | Modifié : historique ajouté |
| 4 nov | Claude | Comment tracer la droite de tendance | D'abord -0,07 puis -0,11 après un recalcul | Notre graphique affiche bien -0,11 | Modifié, le premier chiffre était faux |
| 5 nov | Claude | Le graphique d'exploration et les premiers tests | Le code du graphique et des tests | pytest : tests de test_donnees.py réussis, graphique ouvert | Gardé |
| 5 nov | Claude | Un brouillon de DECISIONS.md | Un brouillon | On a comparé les chiffres avec notre sortie | Modifié : raisons réécrites avec nos mots |
| 7 nov | Claude | Faire l'exception et les classes de variables étape par étape | Le code de DonneeInvalideError et des classes Variable | Comparé avec les chapitres 10 et 11, tests de test_variables.py réussis | Gardé |
| 8 nov | Claude | Si on peut faire une fixture pour la plateforme | Oui, et conftest.py permet de partager les fixtures | Une fixture sert surtout si l'objet est utilisé dans plusieurs tests | Modifié : fixture pour heures, pas pour plateforme |
| 8 nov | Claude | Comment ignorer __pycache__ | Ajouter un .gitignore | Le 17 nov git status montrait encore les __pycache__ (espaces au début des lignes) | Modifié : espaces enlevés |
| 13 nov | Claude | Régression linéaire, arbre ou forêt ? Et quelle techno pour l'interface | Comparaison des 3 modèles et des technos | On a lu la doc de scikit-learn (LinearRegression, train_test_split) et de Tkinter | Gardé : régression linéaire et Tkinter |
| 16-17 nov | Claude | Nous guider pour les étapes 2.2 à 2.7 | Le code expliqué partie par partie, avec ce que fait fit | Code tapé par nous, MAE 0,218, 13 tests réussis | Gardé |
| 17 nov | Claude | Erreurs NameError calculer_mae et ModuleNotFoundError modele | La fonction manquait, et les tests se lancent avec pytest, pas avec le bouton | Fonction ajoutée, pytest lancé dans le terminal | Modifié |
| 17 nov | Claude | Nous guider pour les étapes 2.8 à 2.12 | Le code expliqué partie par partie | Code tapé par nous, pytest après chaque étape (22 tests réussis), CI verte | Gardé |
| 17 nov | Claude | Erreur 'Modele' object has no attribute 'evaluer' | La méthode n'est pas dans la classe, vérifier l'indentation | La méthode était après le if __name__ == "__main__" | Modifié : méthode déplacée |
| 17 nov | Claude | Code envoyé sur main au lieu de P2Lucas | Pas besoin d'annuler, faire git pull origin main sur la branche de Lucas | Lucas a récupéré le code et a continué | Gardé |
| 17 nov | Claude | Erreur au git push | Les branches suivaient la mauvaise branche distante | git branch et git status | Modifié : main suit origin/main |
| 18 nov | Claude | Faire le journal pour qu'il ait l'air d'un travail de tous les jours | Il a refusé, le journal doit rester honnête | Énoncé (section 7) : il faut un tableau avec ces colonnes | Modifié : journal en tableau, rien d'inventé |
| 18 nov | Claude | Vérifier le projet sur GitHub | Conflit dans le README, __pycache__ encore là, une méthode en double dans l'interface | Dépôt recloné, 40 tests réussis | Modifié : corrigé le 21 nov |
| 18-19 nov | Claude | Préparer l'oral et expliquer des notions (_x, propriétés, classe abstraite, graine, couverture) | Un texte pour l'oral, une fiche de révision et des explications | Relu ensemble, texte adapté à ce qu'on a vraiment fait | Modifié |
| 21 nov | Claude | Récupérer modele.py après un Ctrl+Z | git restore src/modele.py | Vérifié avec git status | Gardé |
 