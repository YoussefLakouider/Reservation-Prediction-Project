# Prédiction des réservations des box de self-stockage

## Présentation du projet
Ce projet propose une analyse et une modélisation prédictive du nombre de réservations à partir de données tabulaires anonymisées. Il comprend des scripts Python et un notebook Jupyter pour l’exploration, la visualisation, la préparation des données et la mise en œuvre de modèles de machine learning.

## Contenu du dépôt
- `reservation_etl.py` : Script Python pour le traitement et la modélisation des données.
- `reservation_clustering_analysis.ipynb` : Notebook Jupyter détaillant l’analyse exploratoire, la préparation des données, la modélisation et l’évaluation des résultats.
- `Requirements.txt` : Liste des dépendances Python nécessaires.

## Fonctionnalités principales
- Nettoyage et préparation des données.
- Analyse statistique et visualisation (matplotlib, seaborn, plotly).
- Modélisation prédictive (Random Forest, XGBoost, LGBM, etc.).
- Analyse de l’importance des variables et réduction de dimension (PCA).
- Clustering pour la segmentation des agences.

## Utilisation
1. Installez les dépendances :
   ```bash
   pip install -r Requirements.txt
   ```
2. Placez vos données anonymisées dans le même dossier que les scripts.
3. Exécutez `reservation_etl.py` pour lancer le traitement automatisé ou ouvrez `reservation_clustering_analysis.ipynb` pour une exploration interactive.

## Avertissement
Ce projet ne contient aucune donnée confidentielle ou spécifique à une entreprise. Les noms de fichiers, variables et paramètres sont génériques et adaptés à un usage public.

## Personnalisation
Vous pouvez adapter ce projet à vos propres données en modifiant les chemins de fichiers et les noms de colonnes dans les scripts.

## Licence
Ce projet est fourni à des fins éducatives et de démonstration. Merci de respecter les bonnes pratiques de partage open source.
