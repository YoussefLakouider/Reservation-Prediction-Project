# Prédiction des réservations des box de self-stockage

## Présentation du projet
Ce projet propose une analyse exploratoire et prédiction du nombre de réservations à partir de données tabulaires anonymisées.
Il inclut :

- Nettoyage et préparation des données

- Visualisations statistiques et graphiques interactifs (Matplotlib, Seaborn, Plotly)

- Modélisation prédictive (Random Forest, XGBoost, LGBM)

- Réduction de dimension et analyse de variance (PCA)

- Clustering pour la segmentation des agences

## Contenu du dépôt
- prediction_reservation_clustring.ipynb : notebook principal avec tout le workflow (EDA, visualisation, modélisation, clustering).
- requirements.txt : liste des dépendances Python.

## Fonctionnalités principales
- Nettoyage et préparation des données.
- Analyse statistique et visualisation (matplotlib, seaborn, plotly).
- Modélisation prédictive (Random Forest, LGBM, etc.).
- Analyse de l’importance des variables et réduction de dimension (PCA).
- Clustering pour la segmentation des agences.

## Utilisation
1. Installez les dépendances :
   ```bash
   pip install -r Requirements.txt
   ```
2. Placez vos données anonymisées dans le même dossier que les scripts.
3. Ouvrez `reservation_clustering_analysis.ipynb` pour une exploration interactive.

## Avertissement
Ce projet ne contient aucune donnée confidentielle ou spécifique à une entreprise. Les noms de fichiers, variables et paramètres sont génériques et adaptés à un usage public.

## Personnalisation
Vous pouvez adapter ce projet à vos propres données en modifiant les chemins de fichiers et les noms de colonnes dans les scripts.

## Licence
Ce projet est fourni à des fins éducatives et de démonstration. Merci de respecter les bonnes pratiques de partage open source.
