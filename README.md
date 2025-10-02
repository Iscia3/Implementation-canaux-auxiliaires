# Implementation-canaux-auxiliaires
Ce projet s'inscrit dans le cadre de l'UE Outils Statistiques, en master 1. Il consiste en l'implémentation de la méthode des slices (conversion en poids de Hamming de mesures bruitées) et de la méthode du maximum de vraisemblance.

**Méthode des Slices** : simulation des mesures bruitées de consommations de courant, utilisation de la méthode des slices décrite dans le papier *"Improved Blind Side-Channel Analysis by Exploitation of Joint Distributions of Leakages", C. Clavier, L. Reynaud* pour convertir un ensemble de consommations en l'ensemble des poids de Hamming qui leur correspondent. 

**Méthode du maximum de vraisemblance** : on considère ici que le processus qui permet de transformer des consommations en poids de Hamming ne donne pas des valeurs entières de poids de Hamming, mais des valeurs réelles (dans $\mathbb{R}$) bruitées. Par la formule de Bayes et le théorème des probabilités totales, on calcule la vraisemblance de chaque clé. 
