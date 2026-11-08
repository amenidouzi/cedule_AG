# Ordonnancement de la maintenance de centrales par algorithme génétique

Programme Python qui planifie la maintenance de 7 centrales électriques sur 4 intervalles de l'année, de façon à **maximiser la plus petite réserve de puissance**. Le problème vient de l'exemple « cédule de maintenance » du cours sur les algorithmes génétiques (AG).

## Le problème

| Unité | Capacité (MW) | Intervalles de maintenance requis |
|-------|---------------|-----------------------------------|
| 1     | 20            | 2 (consécutifs)                   |
| 2     | 15            | 2 (consécutifs)                   |
| 3     | 35            | 1                                 |
| 4     | 40            | 1                                 |
| 5     | 15            | 1                                 |
| 6     | 15            | 1                                 |
| 7     | 10            | 1                                 |

- Capacité totale : 150 MW.
- L'année est découpée en 4 intervalles, avec une demande de 80, 90, 65 et 70 MW.
- La maintenance d'une unité commence au début d'un intervalle et se termine à la fin d'un intervalle.

## Formulation

- **Encodage** : un gène de 4 bits par unité (1 = en maintenance pendant l'intervalle, 0 = en service). Un chromosome compte 7 gènes, soit 28 bits.
  - Gènes valides pour les unités 1 et 2 : `1100`, `0110`, `0011`.
  - Gènes valides pour les unités 3 à 7 : `1000`, `0100`, `0010`, `0001`.
  - Les contraintes de durée et de continuité sont donc intégrées au codage.
- **Réserve** à l'intervalle k : `R_k = capacité totale − puissance en maintenance(k) − demande(k)`.
- **Fonction objective (fitness)** : `f(c) = min_k R_k`, avec `f = 0` si une réserve est négative. On cherche à la maximiser.

## Opérateurs génétiques

- **Sélection par loterie (roulette)** : probabilité de choix proportionnelle à la fitness.
- **Croisement** : à un point, toujours placé entre deux gènes.
- **Mutation par inversion** : inversion de l'ordre d'un segment de gènes, au sein d'un groupe d'unités de même durée (unités 1-2, ou unités 3 à 7), pour que tous les gènes restent valides.
- **Mutation par remplacement** (celle du cours) : un gène est remplacé par un autre gène valide de la même unité. Elle sert de comparaison.
- **Élitisme** : le meilleur individu passe à la génération suivante.

## Paramètres par défaut

| Paramètre | Valeur | Remarque |
|-----------|--------|----------|
| Taille de la population | 49 | 7 fois le nombre d'unités (règle du cours : 6 à 7 fois) |
| Générations | 60 | |
| Probabilité de croisement | 0,8 | |
| Probabilité de mutation | 0,2 | à faire varier, comme le recommande le cours |

## Utilisation

Aucune dépendance : seule la bibliothèque standard de Python 3 est utilisée.

```bash
python ordonnancement_ag.py
```

Le script enchaîne quatre étapes :

1. évaluation du chromosome d'exemple du cours (réserves 20, 25, 35 et 30 MW, fitness 20) ;
2. une exécution de l'AG avec sélection par loterie et mutation par inversion ;
3. une recherche exhaustive sur les 9216 cédules possibles pour connaître l'optimum global ;
4. une comparaison des deux mutations sur 30 exécutions.

Pour l'utiliser comme module :

```python
from ordonnancement_ag import algorithme_genetique, afficher

meilleur, historique = algorithme_genetique("inversion", taille=49, generations=60, pc=0.8, pm=0.2, seed=42)
afficher(meilleur)
```

Le premier argument vaut `"inversion"` ou `"remplacement"`.

## Résultats observés

- L'optimum global est **25 MW** (vérifié par recherche exhaustive).
- Exemple de meilleure cédule : `1100 0110 0010 0001 0001 1000 1000`.
- Sur 30 exécutions, la mutation par inversion trouve l'optimum 30 fois sur 30 (génération moyenne : 4,5). La mutation par remplacement le trouve 29 fois sur 30 (génération moyenne : 5,9).

## Limites et pistes

- Les fitness étant proches (20 à 25), la sélection par loterie exerce peu de pression sélective. Sur un problème plus grand, on peut décaler ou classer les fitness avant le tirage.
- Le problème est petit : une recherche exhaustive suffit ici. L'AG sert surtout à illustrer la démarche (encodage, fitness, opérateurs, paramètres), réutilisable pour des problèmes plus grands.
- Pistes d'extension : croisement à deux points, autres sélections (tournoi, rang), critère d'arrêt sur stagnation.
