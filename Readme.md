# Tumor Evolution Analysis Project

## Objectif
Ce projet vise à analyser l'évolution d'une tumeur à partir de deux scans IRM d'un même patient réalisés à des dates différentes. Il utilise les bibliothèques ITK (Insight Segmentation and Registration Toolkit) et VTK (Visualization Toolkit) pour effectuer le recalage des volumes, la segmentation des tumeurs et la visualisation des changements.

## Fonctionnalités

1. **Chargement de deux scans IRM au format NRRD**
2. **Recalage du deuxième scan sur le premier**
3. **Segmentation automatique des tumeurs dans les deux scans**
4. **Calcul de la différence entre les tumeurs segmentées**
5. **Visualisation 3D des changements de la tumeur**

## Compilation

Exécutez le script principal depuis la racine du projet :

**python main.py** 

Ce dernier permet de visualiser l'évolution de la tumeur entre les deux etats

## Détails techniques

## Recalage d'images

Utilisation de itk.ImageRegistrationMethodv4
Transformation : VersorRigid3D
Métrique : Mattes Mutual Information
Optimiseur : Regular Step Gradient Descent
Approche multi-résolution à 3 niveaux

## Segmentation des tumeurs

Méthode de seuillage d'Otsu pour déterminer automatiquement le seuil
Nettoyage post-segmentation avec un filtre médian

## Visualisation des changements

Calcul de la différence entre les tumeurs segmentées
Utilisation de VTK pour la visualisation 3D des changements
Rendu volumique avec une fonction de transfert de couleur et d'opacité personnalisée

## Limitations et améliorations possibles

Le principal point necessitant une amelioration est l'alignement des deux images pour n'avoir comme difference que la tumeur
La segmentation actuelle est basique et pourrait être améliorée avec des méthodes plus avancées
L'interface utilisateur pourrait être développée pour permettre une interaction plus poussée
Des métriques quantitatives supplémentaires pourraient être ajoutées pour l'analyse des changements

## Résultats

Les résultats montrent les différences de volume et d'intensité des voxels entre les deux tumeurs.

## Auteurs

Yacine Boureghda
Yanis Belami
