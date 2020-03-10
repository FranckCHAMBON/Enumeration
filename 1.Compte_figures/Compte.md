---
export_on_save:
  html: true
print_background: true
---

# Compter le nombre de triangles dans un triangle {ignore = true}

Auteur : Franck CHAMBON

```python {cmd="/home/francky/anaconda3/bin/python3" hide run_on_save output="html"}
import drawSvg as draw

def lines(n, A, B, C):
    for i in range(1, 1+n):
        d.append(draw.Lines((i*A[0]+(n-i)*C[0])/n,
                            (i*A[1]+(n-i)*C[1])/n,
                            (i*B[0]+(n-i)*C[0])/n,
                            (i*B[1]+(n-i)*C[1])/n,
                            stroke='black'))

l = 100
d = draw.Drawing(2*l, 2*l, origin='center')

A = (-l, -75)
B = (+l, -75)
C = (0 , -75 + l*3**0.5)
n = 6
lines(n, A, B, C)
lines(n, B, C, A)
lines(n, C, A, B)

print(d._repr_svg_())
```

> Un triangle équilatéral est construit avec des petits triangles équilatéraux identiques, $n$ sur chaque côté. Dans cet exemple, $n=6$.
>> **Combien y a-t-il de triangles sur cette figure ?**
>> On compte tous les triangles équilatéraux dessinés.

---

Ce problème est résolu de manière progressive, et c'est l'occasion d'utiliser :
* des méthodes par force brute ;
* des méthodes par récurrence ;
* des méthodes avec les coefficients binomiaux.

> Table des matières
[TOC]

---

## Problème simplifié : Rectangles dans rectangle

On travaille avec une grille rectangulaire à côtés entiers : $n$ par $m$.
> On compte le nombre de rectangles dessinés, que l'on note $R_{n, m}$.


```python {cmd="/home/francky/anaconda3/bin/python3" hide run_on_save output="html"}
import drawSvg as draw

n, m = 6, 10
w = 25
l = (m//2)*w
d = draw.Drawing((m+2)*w, (n+2)*w, origin='center')


A = (-l, -75)
B = (-l + m*w, -75)
C = (-l, -75 + n*w)

for i in range(n+1):
    d.append(draw.Lines(A[0], A[1]+i*w,
                        B[0], B[1]+i*w,
                        stroke='black'))

for i in range(m+1):
    d.append(draw.Lines(A[0]+i*w, A[1],
                        C[0]+i*w, C[1],
                        stroke='black'))

print(d._repr_svg_())
```

On a aisément :
* $\forall n, m \in \mathbb N : R_{n, m} = R_{m, n}$ ;
* $\forall n \in \mathbb N : R_{n, 0} = 0$ ;
* $\forall n \in \mathbb N : R_{n, 1} = \sum_{i=0}^{n} i =\binom{n+1}2$.

On a aussi avec une récurrence sur $m$ :
* $\forall n, m \in \mathbb N^* : R_{n, m} = R_{n, m-1} + \sum_{i=0}^{n}m\times i$
* $\forall n, m \in \mathbb N^* : R_{n, m} = R_{n, m-1} + m\binom{n+1}2$
* $\forall n, m \in \mathbb N^* : R_{n, m} = \binom{n+1}2 \binom{m+1}2$

On peut aussi utiliser un algorithme par force brute pour vérifier :
```python {cmd="python3"}
from math import factorial as f

def comb(n, m):
    "Retourne le coefficient binomial (n, m)"
    if m > n: return 0
    return f(n) // f(m) // f(n-m)

def R(n, m):
    """Retourne de nombre de rectangles dessinés dans une grille n×m
    Force brute : complexité n²×m²
    """
    cpt = 0
    for Ax in range(m+1):
        for Ay in range(n+1):
            for Bx in range(m+1):
                for By in range(n+1):
                    if (Ax < Bx) and (Ay < By):
                        cpt += 1
    return cpt

for n in range(10):
    for m in range(10):
        assert R(n, m) == comb(n+1, 2) * comb(m+1, 2)
print("Succès aux tests")
```

Nous aurions aussi pu dès le départ établir une formule pour $R_{n, m}$ en affirmant que le nombre de rectangles est :
*  le nombre de façons de choisir un rectangle ;
* et le nombre de façons de choisir
    * deux abscisses parmi $m+1$,
    * et deux ordonnées parmi $n+1$.
* D'où le $ \binom{n+1}2 \binom{m+1}2$.

## Problème original : triangles dans triangle

### Construction des points

#### Avec un ensemble

En utilisant un repère dans un réseau triangulaire, on peut définir l'ensemble des points inclus dans un triangle de côté $n$.

```py
def ens_triangle(n):
    """retourne l'ensemble des points
        + à coordonnées entières ;
        + inclus dans le triangle de côté n."""
    points = {}
    for i in range(n+1):
        for j in range(n+1):
            if i + j <= n:
                points.add( (i, j) )
    return points
```

On a ici construit un ensemble (*set*) Python, on aurait pu aussi construite la liste de la même manière ; en effet, il n'y a pas de doublons créés.

#### Avec une liste

```py
def lst_triangle(n):
    """retourne la liste des points distincts
        + à coordonnées entières ;
        + inclus dans le triangle de côté n."""
    points = []
    for i in range(n+1):
        for j in range(n+1):
            if i + j <= n:
                points.append( (i, j) )
    return points
```

En dehors de la *docstring*, les différences sont :
+ `points` est initialisé à `[]` la liste vide, au lieu de `{}` l'ensemble vide.
+ `points` croît avec `append` qui ajoute en fin de liste, au lieu de `add` qui ajoute à l'ensemble (en vérifiant qu'il n'y ait pas de doublon).

#### Avec une liste en compréhension

> Cette technique est au programme en spé maths en classe de première. **Cependant**, nous le faisons ici avec une double boucle, ce qui n'est pas explicitement au programme...

```py
def lst_triangle(n):
    """retourne la liste des points distincts
        + à coordonnées entières ;
        + inclus dans le triangle de côté n."""
    return [ (i, j) for i in range(n+1) for j in range(n+1) if i + j <= n]
```

#### Avec un itérateur (pour aller plus loin)

On peut aussi construire un **itérateur** au lieu d'une liste : c'est un objet qui fabrique les éléments de la liste, l'un après l'autre, sans stocker la liste entière. Les itérateurs sont très utiles lorsqu'on veut pouvoir traiter un élément entièrement puis l'oublier.
> On ne crée pas la liste qui prendrait inutilement de la place en mémoire.

```py
def it_triangle(n):
    """retourne un itérateur des points distincts
        + à coordonnées entières ;
        + inclus dans le triangle de côté n."""
    for i in range(n+1):
        for j in range(n+1):
            if i + j <= n:
                yield (i, j)
```

### Utilisation

On souhaite compter le nombre de triangles à côtés entiers dont les sommets et côtés sont dans un réseau triangulaire le tout enceint dans un grand triangle de côté $n$.

Il suffit de faire une triple boucle sur la liste de points du réseau ; on obtient $A$, $B$, $C$, dont il suffit de vérifier qu'ils constituent bien un triangle respectant les contraintes, et que le triangle formé est unique.

Dans notre problème, il y a deux sortes de triangles à compter, ceux pointe en bas, et ceux pointe en haut.

* Pour les triangles pointe en haut, on note $A$ le sommet en bas à gauche, $B$ le sommet en bas à droite, et $C$ le sommet en haut. On a :
  * $A_j = B_j$ ; même ordonnée pour $A$ et $B$.
  * $A_i = C_i$ ; même abscisse pour $A$ et $C$.
  * $B_i - A_i = C_j - A_j \neq 0$ ; le côté du triangle.

* Pour les triangles pointe en bas, on note $A$ le sommet en haut à gauche, $B$ le sommet en haut à droite, et $C$ le sommet en bas. On a :
  * $A_j = B_j$ ; même ordonnée pour $A$ et $B$.
  * $A_i = C_i$ ; même abscisse pour $A$ et $C$.
  * $A_i - B_i = A_j - C_j \neq 0$ ; le côté du triangle.

On constate que ces conditions sont *in fine* les mêmes, ce qui nous conduit au test :

```py
def est_triangle(Ai, Aj, Bi, Bj, Ci, Cj):
    """retourne un booléen,
    + True, si ABC est un triangle sur le réseau ;
    + False, sinon"""
    return (Aj == Bj) and (Ai == Ci) and (Bi - Ai == Cj - Aj != 0)
```

### Algorithme force brute

```py
def force_brute(n):
    ans = 0
    points = lst_triangle(n)
    for (Ai, Aj) in points:
        for (Bi, Bj) in points:
            for (Ci, Cj) in points:
                if est_triangle(Ai, Aj, Bi, Bj, Ci, Cj):
                    ans += 1
    return ans
```

### Premières valeurs

```py
print([force_brute(n) for n in range(10)])
```

Résultat :

```py
[0, 1, 5, 13, 27, 48, 78, 118, 170, 235]
```


On peut parfois calculer par force_brute les premiers résultats d'un problème.

* Cela permet de comparer avec une nouvelle version d'un programme, plus efficace, plus complexe, donc possiblement avec quelques erreurs. C'est une bonne pratique !
* Cela permet de vérifier s'il existe des résultats similaires sur OEIS ; une encyclopédie qui peut donner de nouvelles pistes de travail. Testons !

### Informations trouvées sur [OEIS](https://oeis.org)

La [recherche](https://oeis.org/search?q=0%2C+1%2C+5%2C+13%2C+27%2C+48%2C+78%2C+118%2C+170%2C+235&language=english&go=Search) avec les premiers termes donne :

>
>Search: **seq:0,1,5,13,27,48,78,118,170,235**
>Displaying 1-1 of 1 result found. 
>[A002717](https://oeis.org/A002717) a(n) = floor(n(n+2)(2n+1)/8).

Puis des détails sur la seule suite concordante, d'index d'entrée A002717.

### Une nouvelle formule

On note $a_n$ la réponse à notre problème pour un grand triangle de taille $n$. Chaque côté possède $n+1$ points du réseau.

* $a_0 = 0$ ; avec un point, pas de triangle.
* $a_1 = 1$ ; trois points nous donnent un seul triangle.

Une relation de récurrence naturellement proposée est $a_n = a_{n-1} + \Delta_n + \nabla_n$, où
* $\Delta_n$ est le nombre de nouveaux triangles tête en haut ; la base est tout en bas.
* $\nabla_n$ est le nombre de nouveaux triangles tête en bas ; le sommet est tout en bas.

Il est très facile de trouver une formule pour $\Delta_n$, un peu plus délicat pour $\nabla_n$.

* $\Delta_n = \binom{n+1}2$ ; choisir les deux sommets de la base parmi les $n+1$.

* $\nabla_n$ peut s'exprimer en fonction de la parité de $n$ :
    * si $n$ est impair, $\nabla_n = 2\times\left(0+1+2+3+\cdots+\dfrac{n-1}2\right)$ ;
    * si $n$ est pair, $\nabla_n = 2\times\left(0+1+2+3+\cdots+\dfrac{n-2}2\right) + \dfrac{n}2$ ;

On peut certes obtenir deux formules polynomiales (deux proches, suivant la parité de $n$) pour exprimer $a_n$, il faut cependant penser à utiliser une autre base que la base canonique des polynômes ; celle des coefficients binomiaux se prête naturellement bien à la sommation ! On a, après calculs :

> $a_n = \dfrac{12\binom{n+2}3 - 2\binom{n+1}2 - \binom{n}1 - 2\cdot\bold1\!\!1_\text{impair}(n)}{8}$

On peut la réécrire aussi en termes de [*rising factorials*](https://en.wikipedia.org/wiki/Falling_and_rising_factorials), 

> $a_n = \dfrac{2n^{\overline3} - n^{\overline2} - n^{\overline1} - 2\cdot\bold1\!\!1_\text{impair}(n)}{8}$

Attention, $n^{\overline3} = n(n+1)(n+2)$

Une telle formule se prête bien aussi à une méthode d'évaluation proche de celle [Ruffini-Horner](https://fr.wikipedia.org/wiki/M%C3%A9thode_de_Ruffini-Horner).


```py
from math import factorial as f

def comb(n, k):
    "Retourne le nombre de combinaisons de k choix parmi n"
    if 0 <= k <= n:
        return f(n) // f(k) // f(n-k)
    else:
        return 0

def formule1(n):
    "Calcul rapide"
    return (12*comb(n+2, 3) - 2*comb(n+1, 2) - comb(n, 1) - (n&1)) // 8

for n in range(10):
        assert formule1(n) == force_brute(n), f"Échec avec n = {n}"


def formule2(n):
    "Calcul très efficace !!!"
    rising = n
    ans = -rising - (n&1)

    n += 1
    rising *= n
    ans += -rising
    
    n +=1
    rising *= n
    ans += 2*rising
    
    return ans >> 3

for n in range(100):
        assert formule1(n) == formule2(n), f"Échec avec n = {n}"
```

La formule2 est très efficace, elle ne fait aucune division.

## Problèmes étendus

### Triangles dans hexagone

```python {cmd="/home/francky/anaconda3/bin/python3" hide run_on_save output="html"}
import drawSvg as draw

def lines(n, A, B, C):
    for i in range(2*(n+1)//6, 4*(1+n)//6+1):
        d.append(draw.Lines((i*A[0]+(n-i)*C[0])/n,
                            (i*A[1]+(n-i)*C[1])/n,
                            (i*B[0]+(n-i)*C[0])/n,
                            (i*B[1]+(n-i)*C[1])/n,
                            stroke='black'))

l = 350
n = 5

h = l/3**0.5
d = draw.Drawing(3*l//2, 5*l//4, origin='center')
n *= 3
A = (-l, -h)
B = (+l, -h)
C = (0 , -h + l*3**0.5)

lines(n, A, B, C)
lines(n, B, C, A)
lines(n, C, A, B)

A = (+l, -h + 2*l/3**0.5)
B = (-l, -h + 2*l/3**0.5)
C = (0 , -h - 1*l/3**0.5)

lines(n, A, B, C)
lines(n, B, C, A)
lines(n, C, A, B)

print(d._repr_svg_())
```

> > **Combien y a-t-il de triangles dessinés dans un hexagone ?**
>
> On note $n$ le nombre de triangles sur chaque côté de l'hexagone. Ici, $n=5$.
>> Lien pour tester votre réponse : [Counting Triangles II](http://www.spoj.com/problems/TCOUNT2/).

### Triangles dans hexagone étoilé

```python {cmd="/home/francky/anaconda3/bin/python3" hide run_on_save output="html"}
import drawSvg as draw

def lines(n, A, B, C):
    for i in range(1+n):
        d.append(draw.Lines((i*A[0]+(n-i)*C[0])/n,
                            (i*A[1]+(n-i)*C[1])/n,
                            (i*B[0]+(n-i)*C[0])/n,
                            (i*B[1]+(n-i)*C[1])/n,
                            stroke='black'))

l = 200
n = 3

h = l/3**0.5
d = draw.Drawing(3*l, 5*l//2, origin='center')
n *= 3
A = (-l, -h)
B = (+l, -h)
C = (0 , -h + l*3**0.5)

lines(n, A, B, C)
lines(n, B, C, A)
lines(n, C, A, B)

A = (+l, -h + 2*l/3**0.5)
B = (-l, -h + 2*l/3**0.5)
C = (0 , -h - 1*l/3**0.5)

lines(n, A, B, C)
lines(n, B, C, A)
lines(n, C, A, B)

print(d._repr_svg_())
```
> > **Combien y a-t-il de triangles dessinés dans un hexagone ?**
>
> On note $n$ le nombre de triangles sur chaque côté de l'hexagone étoilé. Ici, $n=3$.
>> Lien pour tester votre réponse : [Counting Triangles III](http://www.spoj.com/problems/TCOUNT3/).
