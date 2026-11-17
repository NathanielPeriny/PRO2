faut ecrire les dates de validation
validations A, B, C, D: 13 novembre 2026

Domaine: 
On a envisagé la sécurité routière (accidents au Royaume-Uni) ; réseaux sociaux et vie étudiante, mais on a retenu 
"Réseaux sociaux et vie étudiante". C'est un sujet qui touche directement les étudiants ; un utilisateur peut tester l'effet de ses propres habitudes (temps d'écran, sommeil, stress) sur un GPA estimé.

Jeu de données: 
On a envisagé Accident Analysis (Kaggle, 670 679 lignes, 93 Mo) et Impact of Social Media on Life (Kaggle, 4 500 lignes). 
Le choix qu'on a retenu est Impact of Social Media on Life qu'on a trouvé sur Kaggle (harishyadav0506, Kaggle, licence CC0). 
Le jeu respecte les critères : 4 500 lignes, colonnes numériques et catégorielles, aucune donnée personnelle identifiante, 300 Ko (redistribuable dans le dépôt). Le jeu d'accidents dépassait la limite de 50000 lignes et de 25 Mo, était très déséquilibré (85 % d'accidents « Slight ») et contenait une colonne qui révèle presque la réponse (Number_of_Casualties).


Colonnes qu'on a enlevé: on voulait garder toutes les colonnes et retirer celles sans lien avec le GPA. Weekend_Extra_Hours et Gender retirées. Corrélation avec le GPA proche de 0, le modèle donne le même résultat avec ou sans elles. Les enlever simplifie l'interface. Academic_Level et Primary_Platform sont gardées pour conserver des variables catégorielles.


Valeurs manquantes: on voulait supprimer toutes les lignes incomplètes ou remplacer par la moyenne ou la médiane. On a fini par supprimer 85 lignes sans GPA (impossible d'apprendre sans la réponse). 46 scores de stress manquants remplacés par la médiane (13), moins sensible aux valeurs extrêmes que la moyenne ; on garde ainsi ces lignes. Aucune valeur aberrante impossible trouvée (describe()) : heures quotidiennes de 0,9 à 14 h, sommeil de 3 à 10,5 h, GPA de 1,9 à 4,0.

Cible à estimer: On voulait choisir entre GPA, score de stress et durée du sommeil. On a retenu le GPA (régression), métrique MAE : erreur moyenne en points de GPA, facile à expliquer à un non-informaticien (« le modèle se trompe en moyenne de 0,2 point »).

Modèle: On a voulu faire une régression linéaire, arbre de décision (forêt aléatoire). On a fini par choisir une régression linéaire, comparée au modèle de référence (toujours prédire le GPA moyen). Simple, rapide et explicable : chaque coefficient indique l'effet d'une variable. 

Technologie d'interface: On se décidait entre Streamlit, Gradio et Tkinter. On a choisi Tkinter c'est inclus avec Python, ça fonctionne hors ligne en application de bureau, et on peut y intégrer matplotlib avec FigureCanvasTkAgg. Streamlit et Gradio donnent une interface web plus moderne, mais on doit dépendre sur un serveur à lancer.