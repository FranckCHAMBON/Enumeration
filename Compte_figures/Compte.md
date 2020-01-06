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

...

Le gros du travail.

...

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
