# PRO2
projet2
<<<<<<< HEAD
# allo je m'appelle lucas
=======

Description
Notre application estime le GPA d'un étudiant à partir de ses habitudes. L'utilisateur entre son temps passé sur les réseaux sociaux, son sommeil et son stress. L'application lui donne un GPA estimé et le place sur un graphique.
C'est un exercice pédagogique, pas un outil pour prendre des décisions.
Données
Source : Impact of Social Media on Life, par harishyadav0506, sur Kaggle. https://www.kaggle.com/datasets/harishyadav0506/impact-of-social-media-on-life
Licence : CC0 : Public Domain. Le fichier est donc inclus dans le dossier donnees/.
Contenu : 4 500 étudiants. La cible est Academic_Performance_GPA (de 1,9 à 4,0). Les variables d'entrée sont l'âge, le niveau d'études, la plateforme principale, les heures par jour sur les réseaux sociaux, la durée du sommeil, la qualité du sommeil et le stress perçu.
Nettoyage :
On a retiré les 85 lignes sans GPA. On ne peut pas apprendre sans la réponse.
On a remplacé les 46 scores de stress manquants par la médiane (13). La médiane est moins sensible aux valeurs extrêmes que la moyenne.
On a retiré Gender et Weekend_Extra_Hours. Elles n'avaient aucun lien avec le GPA.
On n'a trouvé aucune valeur impossible. Les heures par jour vont de 0,9 à 14 h, le sommeil de 3 à 10,5 h.
Après le nettoyage, il reste 4 415 lignes.
Limites connues : les données semblent synthétiques. Le GPA est plafonné à 4,0 et les heures par jour à 14 h.
Installation
git clone https://github.com/NathanielPeriny/PRO2.git
cd PRO2
pip install -r requirements.txt
On a utilisé Python 3.12.
Lancement
Lancer l'application :
python src/main.py
Refaire l'exploration et le graphique (figures/exploration_gpa.png) :
python src/donnees.py
Lancer les tests :
pytest
>>>>>>> a616a7bb402e1d721323302d3e4c1e253b1d229e
