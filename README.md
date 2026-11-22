# PRO2 - Prédire le GPA selon les habitudes

Projet 2 INF1007 automne 2026
Nathaniel Periny et Lucas Renaud

## C'est quoi

Une petite application qui estime le GPA d'un étudiant selon ses habitudes : le temps passé sur les réseaux sociaux, le sommeil, le stress, etc. On entre ses infos, on clique sur Prédire, et l'appli donne un GPA estimé avec la marge d'erreur du modèle. Elle montre aussi où ce GPA se situe parmi les autres étudiants.

C'est un exercice pour le cours, pas un vrai outil pour prendre des décisions.

## Les données

On a pris le jeu *Impact of Social Media on Life* sur Kaggle (par harishyadav0506) :
https://www.kaggle.com/datasets/harishyadav0506/impact-of-social-media-on-life

La licence est CC0 (domaine public), donc on a pu mettre le fichier directement dans "donnees/".

Il y a un échantillon de 4500 étudiants. On essaie de prédire "Academic_Performance_GPA" (entre 1,9 et 4,0) à partir de 7 colonnes : âge, niveau d'études, réseau social principal, heures par jour sur les réseaux, heures de sommeil, qualité du sommeil et stress perçu.

Ce qu'on a nettoyé :
- 85 lignes n'avaient pas de GPA, on les a enlevées (sans la réponse, le modèle ne peut rien apprendre).
- 46 étudiants n'avaient pas de score de stress. On a mis la médiane (13) plutôt que la moyenne, parce qu'elle bouge moins à cause des valeurs extrêmes.
- On a enlevé "Gender" et "Weekend_Extra_Hours" parce qu'elles n'avaient aucun lien avec le GPA.
- On n'a pas trouvé de valeurs impossibles (heures par jour entre 0,9 et 14, sommeil entre 3 et 10,5).

On a supprimé 85 lignes, il reste donc 4415 lignes après le nettoyage.

À noter : les données ont l'air synthétiques. Le GPA est bloqué à 4,0 et les heures par jour à 14.

## Installer et lancer

```
git clone https://github.com/NathanielPeriny/PRO2.git
cd PRO2
pip install -r requirements.txt
```
(on a utilisé Python 3.12)

Pour ouvrir l'application :
```
python src/main.py
```

Si jamais le modèle manque, on peut le réentraîner avec "python src/modele.py". Ça recrée aussi le graphique "figures/predit_contre_reel.png".

Pour refaire le graphique d'exploration : "python src/donnees.py"

Pour les tests : "pytest"

## Organisation du code

```
donnees/      le CSV
figures/      les graphiques
modeles/      le modèle sauvegardé (.joblib) et ses métadonnées (.json)
src/
  donnees.py      chargement, nettoyage, graphique d'exploration
  exceptions.py   nos exceptions (ProjetError, DonneeInvalideError)
  variables.py    Variable et ses deux classes enfants
  modele.py       entraînement, évaluation et sauvegarde du modèle
  historique.py   l'historique des prédictions (fichier CSV)
  application.py  la logique de l'appli
  interface.py    la fenêtre Tkinter
  main.py         lance l'appli
tests/        les tests pytest
```

Quelques explications sur les classes :
- "Variable" est abstraite. "VariableNumerique" vérifie qu'on a bien un nombre dans le bon intervalle, et "VariableCategorielle" vérifie que le choix fait partie de la liste. Si la saisie n'est pas bonne, ça lève "DonneeInvalideError".
- "Modele" sépare les données, entraîne la régression et la compare à un modèle de référence.
- "Historique" écrit et relit les prédictions dans un CSV.
- "Application" regroupe le modèle, les variables et l'historique. Toute la logique est là.
- "Interface" s'occupe seulement de l'affichage : elle ne fait aucun calcul, elle appelle "Application".

Les champs de la fenêtre sont créés à partir de "modeles/metadonnees.json" : un champ texte pour les nombres, une liste déroulante pour les catégories.

## Résultats

On a utilisé une régression linéaire (scikit-learn), entraînée sur 80 % des données avec une graine fixe (42).

Pour savoir si le modèle est bon, on le compare à un modèle "paresseux" qui prédit toujours le GPA moyen (3,43) :
- modèle de référence : MAE de 0,332
- notre régression : MAE de 0,218

Donc le modèle se trompe en moyenne d'environ 0,22 point de GPA, à peu près un tiers de moins que la référence.

Ce qu'on remarque :
- C'est le temps sur les réseaux sociaux qui compte le plus : environ -0,07 point de GPA par heure. Le sommeil aide un peu (+0,04 par heure).
- Le réseau social utilisé, l'âge et le niveau d'études ne changent presque rien.
- Sur le graphique prédit contre réel, on voit que le modèle surestime les GPA faibles et sous-estime les GPA élevés. Il a tendance à revenir vers la moyenne.
- Comme beaucoup d'étudiants sont à 4,0, le modèle a du mal à les distinguer.

## Tests

Il y a 40 tests dans "tests/" : des cas normaux, des cas limites et des cas d'erreur. La CI (GitHub Actions) les lance à chaque push.

Pour voir la couverture :
```
coverage run -m pytest
coverage report --omit="tests/*"
```

On a 84 % de couverture sur "src/". L'interface n'est pas testée automatiquement, mais sa logique est dans "application.py", qui est couvert à 99 %.

## Outil du chapitre 7

On a mis un décorateur, "chronometrer", sur la méthode "entrainer()" : il affiche combien de temps prend l'entraînement. On utilise aussi un générateur ("Historique.lignes()", avec "yield") pour relire l'historique une ligne à la fois.

## Documentation consultée


- pandas "get_dummies" : https://pandas.pydata.org/docs/reference/api/pandas.get_dummies.html
- scikit-learn "LinearRegression" : https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
- scikit-learn "train_test_split" : https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
- Tkinter : https://docs.python.org/3/library/tkinter.html
- Matplotlib dans Tkinter : https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html

## Autres fichiers

"DECISIONS.md" explique nos choix, et "JOURNAL_IA.md" comment on a utilisé l'IA.
