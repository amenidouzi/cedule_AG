
import random
from itertools import product

CAPACITES = [20, 15, 35, 40, 15, 15, 10]
DUREES = [2, 2, 1, 1, 1, 1, 1]
DEMANDE = [80, 90, 65, 70]

N_UNITES = len(CAPACITES)
N_INTERVALLES = len(DEMANDE)
CAPACITE_TOTALE = sum(CAPACITES)  # 150 MW


def genes_possibles(duree):
    return [
        "0" * debut + "1" * duree + "0" * (N_INTERVALLES - debut - duree)
        for debut in range(N_INTERVALLES - duree + 1)
    ]


GENES = [genes_possibles(d) for d in DUREES]
GROUPES = [[0, 1], [2, 3, 4, 5, 6]]

def reserves(chromosome):

    res = []
    for k in range(N_INTERVALLES):
        perdue = sum(CAPACITES[u] for u in range(N_UNITES) if chromosome[u][k] == "1")
        res.append(CAPACITE_TOTALE - perdue - DEMANDE[k])
    return res


def fitness(chromosome):
    return max(min(reserves(chromosome)), 0)
def individu_aleatoire():
    return [random.choice(GENES[u]) for u in range(N_UNITES)]


def selection_loterie(population, fits):
    total = sum(fits)
    if total == 0:
        return random.choice(population)
    tirage = random.uniform(0, total)
    cumul = 0.0
    for ind, f in zip(population, fits):
        cumul += f
        if cumul >= tirage:
            return ind
    return population[-1]


def croisement(p1, p2, pc):
    if random.random() >= pc:
        return p1[:], p2[:]
    point = random.randint(1, N_UNITES - 1)
    return p1[:point] + p2[point:], p2[:point] + p1[point:]


def mutation_inversion(chromosome, pm):
    if random.random() >= pm:
        return chromosome
    c = chromosome[:]
    groupe = random.choice(GROUPES)
    i, j = sorted(random.sample(range(len(groupe)), 2))
    unites = groupe[i : j + 1]
    genes_inverses = [c[u] for u in unites][::-1]
    for u, g in zip(unites, genes_inverses):
        c[u] = g
    return c


def mutation_remplacement(chromosome, pm):
    if random.random() >= pm:
        return chromosome
    c = chromosome[:]
    u = random.randrange(N_UNITES)
    c[u] = random.choice(GENES[u])
    return c


MUTATIONS = {
    "inversion": mutation_inversion,
    "remplacement": mutation_remplacement,
}
def algorithme_genetique(mutation="inversion", taille=49, generations=60,
                         pc=0.8, pm=0.2, seed=None):
    if seed is not None:
        random.seed(seed)
    muter = MUTATIONS[mutation]
    population = [individu_aleatoire() for _ in range(taille)]
    meilleur = max(population, key=fitness)
    historique = []

    for _ in range(generations):
        fits = [fitness(ind) for ind in population]
        courant = population[fits.index(max(fits))]
        if fitness(courant) > fitness(meilleur):
            meilleur = courant[:]
        historique.append(fitness(meilleur))

        nouvelle = [meilleur[:]]
        while len(nouvelle) < taille:
            p1 = selection_loterie(population, fits)
            p2 = selection_loterie(population, fits)
            f1, f2 = croisement(p1, p2, pc)
            nouvelle.append(muter(f1, pm))
            if len(nouvelle) < taille:
                nouvelle.append(muter(f2, pm))
        population = nouvelle

    return meilleur, historique

def afficher(chromosome):
    print("Chromosome :", " ".join(chromosome))
    for u in range(N_UNITES):
        ints = [str(k + 1) for k in range(N_INTERVALLES) if chromosome[u][k] == "1"]
        print(f"  Unité {u + 1} ({CAPACITES[u]} MW) : maintenance aux intervalles {', '.join(ints)}")
    for k, r in enumerate(reserves(chromosome)):
        print(f"  Intervalle {k + 1} : réserve = {r} MW")
    print("  Fitness (plus petite réserve) =", fitness(chromosome))


def optimum_exhaustif():
    return max(fitness(list(c)) for c in product(*GENES))


if __name__ == "__main__":
    print("=== Chromosome du cours ===")
    afficher("0110 0011 0001 1000 0100 0010 1000".split())
    print("\n=== Exécution de l'AG (loterie + inversion) ===")
    meilleur, hist = algorithme_genetique("inversion", seed=42)
    afficher(meilleur)
    print("Évolution de la meilleure fitness (toutes les 10 générations) :", hist[::10])
    opt = optimum_exhaustif()
    print(f"\nOptimum global (recherche exhaustive sur {3*3*4**5} cédules) : {opt}")
    print("\n=== Comparaison des mutations (30 exécutions, 60 générations) ===")
    for nom in MUTATIONS:
        succes, gens = 0, []
        for s in range(30):
            _, h = algorithme_genetique(nom, seed=s)
            if h[-1] == opt:
                succes += 1
                gens.append(h.index(opt) + 1)
        moy = sum(gens) / len(gens) if gens else float("nan")
        print(f"  {nom:13s}: optimum trouvé {succes}/30 fois, "
              f"génération moyenne d'atteinte = {moy:.1f}")