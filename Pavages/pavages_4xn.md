---
export_on_save:
  html: true
print_background: true
---

# Pavages d'un rectangle 4×n par des rectangles d'aire 4 {ignore = true}

Auteur : Franck CHAMBON

```python {cmd="/home/francky/anaconda3/bin/python3" hide run_on_save output="html" id="pa"}
from ipythonblocks import BlockGrid, colors
grid = BlockGrid(width=8, height=4, block_size=50, fill=colors['White'])
grid[:, 0] = colors['Blue']
grid[:, 5] = colors['Blue']
grid[0, 1:5] = colors['LightGreen']
grid[3, 1:5] = colors['Green']
grid[1:3, 1:3] = colors['Red']
grid[1:3, 3:5] = colors['DarkRed']
grid[0:2, 6:8] = colors['Red']
grid[2:4, 6:8] = colors['DarkRed']
print(grid._repr_html_())
```

> Exemple de pavage d'un rectangle $4\times 8$ par des rectangles d'aire $4$.
> > **Combien y a-t-il de tels pavages ?**
> On notera $a_n$ le nombre de pavages pour un rectangle $4\times n$.

```python {cmd="/home/francky/anaconda3/bin/python3" hide run_on_save output="html"}
from ipythonblocks import BlockGrid, colors
grid = BlockGrid(width=10, height=4, block_size=50, fill=colors['White'])
grid[:, 0] = colors['Blue']
grid[0, 2:6] = colors['Green']
grid[0:2, 7:9] = colors['Red']
print(grid._repr_html_())
```
> Les trois motifs : les rectangles d'aire 4, à côtés entiers.

---

Ce problème est résolu de manière progressive, et c'est l'occasion d'utiliser :
* des méthodes de dénombrements de pavages ;
* des suites récurrentes linéaires (autres que la très classique suite de Fibonacci) ;
* des algorithmes de calcul de termes d'une telle suite :
    * par calcul successif ;
    * par calcul matriciel ;
    * par calcul polynomial.

> Table des matières
[TOC]

---

## Problème simplifié

* Si on ne pave qu'avec des barres verticales, il n'y a qu'une seule façon de paver un rectangle $4\times n$.
    * $\forall n \in \mathbb N \quad a_n = 1$
* Si on ne pave qu'avec des barres verticales et des carrés, il est facile de voir que $(a_n)_n$ correspond à la suite de Fibonacci décalée, à savoir :
    * $a_0 = a_1 = 1$, et $\forall n \in \mathbb N \quad a_{n+2} = a_{n+1} + a_n$

---

## Cas général

Pour tout $n$ entier, on note :

* $a_n$ le nombre de pavages d'un rectangle $4\times n$.
* $b_n$ le nombre de pavages d'un rectangle $4\times n$ modifié :
    * on y ajoute un carré $2\times2$ à droite (en haut ou en bas).
* $c_n$ le nombre de pavages d'un rectangle $4\times n$ modifié :
    * on y ajoute un carré $2\times2$ à droite au milieu.

---

```python {cmd="/home/francky/anaconda3/bin/python3" hide run_on_save output="html"}
from ipythonblocks import BlockGrid, colors
grid = BlockGrid(width=10, height=4, block_size=50, fill=colors['Black'])
grid[:, 8:10] = (255, 255, 255)
print(grid._repr_html_())
```
> Un rectangle $4 \times 8$.
>> Il y a $a_8$ façons de le paver.

---

```python {cmd="/home/francky/anaconda3/bin/python3" hide run_on_save output="html"}
from ipythonblocks import BlockGrid, colors
grid = BlockGrid(width=10, height=4, block_size=50, fill=colors['Black'])
grid[0:2, 8:10] = (255, 255, 255)
print(grid._repr_html_())
```
>Un rectangle $4\times 8$ avec un carré $2\times2$ à droite en bas.
>> Il y a $b_8$ façons de le paver.

---

```python {cmd="/home/francky/anaconda3/bin/python3" hide run_on_save output="html"}
from ipythonblocks import BlockGrid, colors
grid = BlockGrid(width=10, height=4, block_size=50, fill=colors['Black'])
grid[0, 8:10] = (255, 255, 255)
grid[3, 8:10] = (255, 255, 255)
print(grid._repr_html_())
```
> Un rectangle $4\times 8$ avec un carré $2\times2$ à droite au milieu.
>> Il y a $c_8$ façons de le paver.

---

Typiquement, ce genre de problème possède une solution avec une suite récurrente linéaire.
* Il est nécessaire de déterminer les premiers termes,
* puis d'établir une formule de récurrence pour $a_n$, $b_n$ et $c_n$.

### Premières valeurs

1. $a_n$ pour $n<4$
    * $a_0 = 1$, il y a une unique façon de paver le vide ;
    * $a_1 = 1$, une barre verticale ;
    * $a_2 = 2$, deux barres verticales, ou bien deux carrés ;
    * $a_3 = 3$, trois barres verticales, ou bien deux carrés flanqués d'une barre verticale (à gauche ou à droite).

2. $b_n$ pour $n<2$
    * $b_0 = 1$, un carré ;
    * $b_1 = 1$, un carré et une barre verticale ;

3. $c_n$ pour $n<4$
Pour $n<4$, on ne peut rien mettre d'autre qu'un carré à droite, et alors on a $c_n=a_n$ pour $n<4$.
    * $c_0 = 1$ ;
    * $c_1 = 1$ ;
    * $c_2 = 2$ ;
    * $c_3 = 3$ ;


### Récurrence pour $a_n$

Il y a plusieurs cas de motifs pour la partie droite d'un pavage de rectangle $4\times n$, avec $n\geqslant 4$ :
1. il y a une barre verticale ;
2. il y a $4$ barres horizontales ;
3. il y a $2$ carrés ;
4. il y a un carré et deux barres horizontales
    1. carré en haut ;
    2. carré au milieu ;
    3. carré en bas.

Graphiquement, cela donne :

---

```python {cmd="/home/francky/anaconda3/bin/python3" hide run_on_save output="html"}
from ipythonblocks import BlockGrid, colors
grid = BlockGrid(width=8, height=4, block_size=50, fill=colors['Black'])
grid[:, 7] = colors['Blue']
print(grid._repr_html_())
```

> Dans ce cas, il y a $a_{n-1}$ façons de paver ce qu'il reste.

---

```python {cmd="/home/francky/anaconda3/bin/python3" hide run_on_save output="html"}
from ipythonblocks import BlockGrid, colors
grid = BlockGrid(width=8, height=4, block_size=50, fill=colors['Black'])
grid[0, 4:8] = colors['Green']
grid[1, 4:8] = colors['LightGreen']
grid[2, 4:8] = colors['Green']
grid[3, 4:8] = colors['LightGreen']
print(grid._repr_html_())
```

> Dans ce cas, il y a $a_{n-4}$ façons de paver ce qu'il reste.

---

```python {cmd="/home/francky/anaconda3/bin/python3" hide run_on_save output="html"}
from ipythonblocks import BlockGrid, colors
grid = BlockGrid(width=8, height=4, block_size=50, fill=colors['Black'])
grid[0:2, 6:8] = colors['DarkRed']
grid[2:4, 6:8] = colors['Red']
print(grid._repr_html_())
```

> Dans ce cas, il y a $a_{n-2}$ façons de paver ce qu'il reste.

---

```python {cmd="/home/francky/anaconda3/bin/python3" hide run_on_save output="html"}
from ipythonblocks import BlockGrid, colors
grid = BlockGrid(width=8, height=4, block_size=50, fill=colors['Black'])
grid[0:2, 6:8] = colors['Red']
grid[2, 4:8] = colors['Green']
grid[3, 4:8] = colors['LightGreen']
print(grid._repr_html_())
```

> Dans ce cas, *par symétrie horizontale*, il y a $b_{n-4}$ façons de paver ce qu'il reste.

---

```python {cmd="/home/francky/anaconda3/bin/python3" hide run_on_save output="html"}
from ipythonblocks import BlockGrid, colors
grid = BlockGrid(width=8, height=4, block_size=50, fill=colors['Black'])
grid[0, 4:8] = colors['Green']
grid[1:3, 6:8] = colors['Red']
grid[3, 4:8] = colors['LightGreen']
print(grid._repr_html_())
```

> Dans ce cas, il y a $c_{n-4}$ façons de paver ce qu'il reste.

---

```python {cmd="/home/francky/anaconda3/bin/python3" hide run_on_save output="html"}
from ipythonblocks import BlockGrid, colors
grid = BlockGrid(width=8, height=4, block_size=50, fill=colors['Black'])
grid[0, 4:8] = colors['Green']
grid[1, 4:8] = colors['LightGreen']
grid[2:4, 6:8] = colors['Red']
print(grid._repr_html_())
```

> Dans ce cas, il y a $b_{n-4}$ façons de paver ce qu'il reste.

---

**Bilan** : pour $n\geqslant 4$, on a $a_n = a_{n-1} + a_{n-4} + a_{n-2} + 2b_{n-4} + c_{n-4}$

---

### Récurrence pour $b_n$

Il y a plusieurs cas de motifs pour la partie droite d'un pavage de rectangle $4\times n$ flanqué d'un carré à droite en bas, avec $n\geqslant 2$ :
1. il y a un carré ;
2. il y a $2$ barres horizontales.

---

```python {cmd="/home/francky/anaconda3/bin/python3" hide run_on_save output="html"}
from ipythonblocks import BlockGrid, colors
grid = BlockGrid(width=10, height=4, block_size=50, fill=colors['Black'])
grid[0:2, 8:10] = colors['White']
grid[2:4, 8:10] = colors['Red']
print(grid._repr_html_())
```


> Dans ce cas, il y a $a_{n}$ façons de paver ce qu'il reste.

---

```python {cmd="/home/francky/anaconda3/bin/python3" hide run_on_save output="html"}
from ipythonblocks import BlockGrid, colors
grid = BlockGrid(width=10, height=4, block_size=50, fill=colors['Black'])
grid[0:2, 8:10] = colors['White']
grid[2, 6:10] = colors['Green']
grid[3, 6:10] = colors['LightGreen']
print(grid._repr_html_())
```

> Dans ce cas, il y a $b_{n-2}$ façons de paver ce qu'il reste.

---

**Bilan** : pour $n\geqslant 2$, on a $b_n = b_{n-2} + a_{n}$

---

### Récurrence pour $c_n$

Il y a plusieurs cas de motifs pour la partie droite d'un pavage de rectangle $4\times n$ flanqué d'un carré à droite au milieu, avec $n\geqslant 4$ :
1. il y a un carré ;
2. il y a $2$ barres horizontales.

---

```python {cmd="/home/francky/anaconda3/bin/python3" hide run_on_save output="html"}
from ipythonblocks import BlockGrid, colors
grid = BlockGrid(width=10, height=4, block_size=50, fill=colors['Black'])
grid[0, 8:10] = colors['White']
grid[3, 8:10] = colors['White']
grid[1:3, 8:10] = colors['Red']
print(grid._repr_html_())
```

> Dans ce cas, il y a $a_{n}$ façons de paver ce qu'il reste.

---

```python {cmd="/home/francky/anaconda3/bin/python3" hide run_on_save output="html"}
from ipythonblocks import BlockGrid, colors
grid = BlockGrid(width=10, height=4, block_size=50, fill=colors['Black'])
grid[0, 8:10] = colors['White']
grid[3, 8:10] = colors['White']
grid[1, 6:10] = colors['Green']
grid[2, 6:10] = colors['LightGreen']
grid[3, 4:8] = colors['Green']
grid[0, 4:8] = colors['LightGreen']
print(grid._repr_html_())
```

> Dans ce cas, il y a $c_{n-4}$ façons de paver ce qu'il reste.

---

**Bilan** : pour $n\geqslant 4$, on a $c_n = c_{n-4} + a_{n}$

---

## Calcul des valeurs suivantes

On utilise les premières valeurs et les relations de récurrence :
* d'abord pour calculer $b_2$ et $b_3$
    * $b_2 = b_0 + a_2 = 1+2 = 3$
    * $b_3 = b_1 + a_3 = 1+3 = 4$
* ensuite pour calculer des valeurs suivantes.

```python {cmd="python3" run_on_save id="valeurs" output="none"}
a = [1, 1, 2, 3]
b = [1, 1, 3, 4]
c = [1, 1, 2, 3]
for n in range(4, 24):
    # On ajoute a[n], puis b[n], puis c[n]
    a.append(a[n-1] + a[n-2] + a[n-4] + 2*b[n-4] + c[n-4])
    b.append(a[n] + b[n-2])
    c.append(a[n] + c[n-4])
```

```python {cmd="python3" run_on_save hide continue="valeurs" output="markdown"}
def markdown(a, ni, nf):
    """Retourne un joli tableau markdown des valeurs de
    la suite a_n pour n dans [ni, nf["""
    ans = "|$n$|"
    for n in range(ni, nf): ans += f"${n}$|"
    ans += "\n|---|"
    for n in range(ni, nf): ans += "---|"
    ans+= "\n|$a_n$|"
    for n in range(ni, nf): ans += f"${a[n]}$|"
    return ans+"\n"
print(markdown(a, 0, 15))
print(markdown(a, 15, 24))
```

### Relation d'ordre $8$ pour $a_n$

#### D'après OEIS<sup>®</sup>

Sur [*On-Line Encyclopedia of Integer Sequences*](oeis.org), cette suite est référencée sous [A220123](http://oeis.org/A220123). On y découvre une autre relation de récurrence :
> Pour $n\geqslant8$, on a : $-a_{n-8}+a_{n-6}-a_{n-5}+5a_{n-4}+a_{n-2}+a_{n-1} = a_{n}$

On peut vérifier cette relation sur nos valeurs :

```python
for n in range(8, 24):
    assert  -a[n-8] +a[n-6] -a[n-5] +5*a[n-4] +a[n-2] +a[n-1] == a[n], f"Échec avec n = {n}"
```

**Remarque :** Pour une suite qui ne serait pas référencée, [l' algorithme de Berlekamp–Massey (*en*)](https://en.wikipedia.org/wiki/Berlekamp%E2%80%93Massey_algorithm) permet de déterminer une relation de récurrence en fonction des premiers termes.


#### Preuve de cette relation de récurrence

Pour $n\geqslant 8$, on a :
* $a_n = a_{n-1} + a_{n-4} + a_{n-2} + 2b_{n-4} + c_{n-4} \quad (I)$
* $b_{n-4} = b_{n-6} + a_{n-4} = b_{n-8} + a_{n-6} + a_{n-4}$
* $c_{n-4} = c_{n-8} + a_{n-4}$

On déduit :
* $a_n = a_{n-1} + a_{n-4} + a_{n-2} + 2b_{n-8}+ 2a_{n-6} +2a_{n-4}+ c_{n-8} + a_{n-4}\quad (II)$ 

Or, d'après $(I)$ (valable aussi pour $n\geqslant 4$), on a pour $n\geqslant 8$ :
* $a_{n-4} = a_{n-5} + a_{n-8} + a_{n-6} + 2b_{n-8} + c_{n-8}\quad (III)$

Par soustraction de $(II)$ par $(III)$, on obtient pour $n\geqslant 8$ :
* $a_{n} = -a_{n-8}+a_{n-6}-a_{n-5}+5a_{n-4}+a_{n-2}+a_{n-1}$

CQFD.

### Calculs successifs des premiers termes

On ajoute à la liste des valeurs initiales les nouvelles valeurs avec la relation de récurrence.
> Dans notre exemple la valeur suivante est environ le double de la précédente, donc nécessite environ un bit de plus en moyenne. Le stockage de 200 000 valeurs prend donc une place mémoire de plus de 20 milliards de bits ; environ 3 Go.

```python {cmd="python3"}
from time import time
from sys import getsizeof

a = [1, 1, 2, 3, 9, 16, 35, 65] # valeurs initiales
r = [-1, 0, 1, -1, 5, 0, 1, 1] # relation de récurrence
n = 200_000 # rang du terme à calculer

t0 = time()
for _ in range(8, n + 1):
    a.append(sum(ai * ri for ai, ri in zip(a[-8:], r)))
t1 = time()

print(f"Durée : {round(t1 - t0, 2)}s")
print(f"Taille des données : {round(sum(map(getsizeof, a))/10**9, 2)}Go")

m = 10**9 + 7
print(f"Preuve de calcul : {a[-1] % m}")
```

* C'est la bonne méthode à employer si on a besoin de (*presque*) tous les premiers termes d'une suite récurrente linéaire.
* La dernière instruction affiche le dernier terme calculé, qui est très très grand, modulo un grand nombre premier sur 32bits. Cette *preuve* de calcul a plusieurs utilités :
    * elle initie au calcul modulaire omniprésent en cryptographie,
    * elle permet de vérifier plus aisément des calculs sur de grands nombres par différentes méthodes,
    * ou par différents langages qui ne travaillent pas avec des nombres plus grands que les mots machine.

> Sans stocker toutes les valeurs, juste les huit précédentes, peut-on calculer beaucoup plus de termes ?
> * Il suffit de supprimer, avec `del a[0]`, le terme qui devient inutile à chaque tour de boucle. Cette opération est peu coûteuse en Python ; on ne déplace pas les autres éléments de la liste, ce n'est pas un tableau !!!

```python {cmd="python3"}
from time import time
from sys import getsizeof

a = [1, 1, 2, 3, 9, 16, 35, 65] # valeurs initiales
r = [-1, 0, 1, -1, 5, 0, 1, 1] # relation de récurrence
n = 200_000 # rang du terme à calculer

t0 = time()
for _ in range(8, n + 1):
    a.append(sum(ai * ri for ai, ri in zip(a, r)))
    del a[0]
t1 = time()

print(f"Durée : {round(t1 - t0, 2)}s")
print(f"Taille des données : {round(sum(map(getsizeof, a))/10**3, 2)}ko")

m = 10**9 + 7
print(f"Preuve de calcul : {a[-1] % m}")
```

C'est à peine plus rapide, mais l'empreinte mémoire est bien plus faible.

Dans un fichier `outils.py`, créons une fonction `rec_lin_suc` qui retourne un terme d'une suite récurrente linéaire par calcul des termes successifs.

@import "outils.py" {line_begin=0 line_end=18}

Utilisation :

```python {cmd="python3"}
from time import time

from outils import rec_lin_suc

a = [1, 1, 2, 3, 9, 16, 35, 65] # valeurs initiales
r = [-1, 0, 1, -1, 5, 0, 1, 1] # relation de récurrence
n = 200_000 # rang du terme à calculer

t0 = time()
a_n = rec_lin_suc(a, r, n)
t1 = time()

print(f"Durée : {round(t1 - t0, 2)}s")
m = 10**9 + 7
print(f"Preuve de calcul : {a_n % m}")
```


> Peut-on calculer un terme lointain plus rapidement avec une autre méthode ?
> * Oui, avec l'exponentiation rapide de matrices.
> * Oui, avec l'exponentiation rapide modulaire de polynômes.


### Calcul matriciel d'un terme lointain

Dans le code précédent, les deux instructions :
```python
a.append(sum(ai * ri for ai, ri in zip(a, r)))
del a[0]
```

peuvent être traduites sous forme matricielle par :
>  $a \leftarrow aM$,
>*  où $M$ est la [matrice compagnon](https://fr.wikipedia.org/wiki/Matrice_compagnon) associée au
polynôme unitaire $P(X) = 1 - X^2 + X^3 -5X^4 - X^6 - X^7 + X^8$ ;
> * et où $a$ est un vecteur ligne.
> * On a :
>   * $P(X) = 0 \iff X^8 = -1 + X^2 - X^3 +5X^4 + X^6 + X^7$
>   * La dernière colonne de la matrice est notre vecteur de la relation de récurrence linéaire.

$$
M = \begin{pmatrix}
0 & 0 & 0 & 0 & 0 & 0 & 0 & -1 \\
1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 & 0 & 0 & 0 & 1 \\
0 & 0 & 1 & 0 & 0 & 0 & 0 & -1 \\
0 & 0 & 0 & 1 & 0 & 0 & 0 & 5 \\
0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 1 & 0 & 1 \\
0 & 0 & 0 & 0 & 0 & 0 & 1 & 1 \\
\end{pmatrix}
$$

Avec $a = (a_0, a_1, a_2, a_3, a_4, a_5, a_6, a_7)$, on a pour $n\in \mathbb N$ :

$$aM^n = (a_{n}, a_{n+1}, a_{n+2}, a_{n+3}, a_{n+4}, a_{n+5}, a_{n+6}, a_{n+7})$$

De sorte que l'on peut calculer plus rapidement $a_n$ avec l'exponentiation rapide de matrices.
> Si la récurrence est d'ordre $d$, 
> * le temps de calcul est en $\Theta(d^3 \log n)$ opérations élémentaires (pas secondes) ;
> * l'empreinte mémoire est en $\Theta(d^2)$ coefficients (pas bits) ;
> * **Attention**, les coefficients peuvent être de grands nombres, et donc le temps de calcul en secondes peut ne pas être en $\Theta(d^3 \log n)$...

> Comparons avec notre exemple, et un code non optimisé inclus dans notre petit module `outils.py`.

```python {cmd="python3"}
from time import time

from outils import rec_lin_mat

a = [1, 1, 2, 3, 9, 16, 35, 65] # valeurs initiales
r = [-1, 0, 1, -1, 5, 0, 1, 1] # relation de récurrence
n = 200_000 # rang du terme à calculer

t0 = time()
a_n = rec_lin_mat(a, r, n)
t1 = time()

print(f"Durée : {round(t1 - t0, 2)}s")

m = 10**9 + 7
print(f"Preuve de calcul : {a_n % m}")
```

> On peut faire mieux en travaillant avec des polynômes.

### Calcul polynomial d'un terme lointain

Nous avons pu déterminer un terme de rang $n$ d'une suite récurrente linéaire d'ordre $d$ en regardant un élément du vecteur calculé avec $a\times M^n$, où $a$ est le vecteur des termes initiaux, et $M$ la matrice compagnon associée à la récurrence.

Le calcul de $M^n$ coûte $\Theta(d^3\times \log n)$ opérations élémentaires (entre des entiers dont la taille peut devenir très grande...)

On peut réduire sérieusement le coût en considérant que $M$ possède $P$ comme polynôme minimal, le polynôme associé à la récurrence, et que l'on peut calculer $Q_n = X^n \pmod P$, par exponentiation rapide ; le coût est $\Theta(d^2\times \log n)$. Il suffit d'évaluer $Q_n$ en $M$ au lieu de $X^n$ en $M$ afin d'obtenir $M^n$.


Mieux encore, on peut se passer totalement de la matrice $M$.
* On a besoin de la première colonne de $M^i$ pour $i\in [\![0..d[\![$,
* or il s'agit d'un simple vecteur colonne $(\delta_{i,j})_{j \in [\![0..d[\![}$ (0-indexation).

> **En résumé :**
> * Avec $Q_n = X^n \pmod P$, qui s'écrit : $q_0 + q_1X + \cdots + q_{d-1}X^{d-1}$
> * on a : $a_n = a_0\times q_0 + a_1\times q_1 + \cdots + a_{d-1}\times q_{d-1}$

```python {cmd="python3"}
from time import time

from outils import rec_lin_pol

a = [1, 1, 2, 3, 9, 16, 35, 65] # valeurs initiales
r = [-1, 0, 1, -1, 5, 0, 1, 1] # relation de récurrence
n = 200_000 # rang du terme à calculer

t0 = time()
a_n = rec_lin_pol(a, r, n)
t1 = time()

print(f"Durée : {round(t1 - t0, 2)}s")

m = 10**9 + 7
print(f"Preuve de calcul : {a_n % m}")
```

> **Conclusion :** L'exponentiation rapide de polynômes modulo la relation de récurrence permet d'avoir une bien meilleure complexité temporelle.
>
> Si la récurrence est d'ordre $d$ :
> * le temps de calcul est en $\Theta(d^2 \log n)$ opérations élémentaires (pas secondes) ;
> * l'empreinte mémoire est en $\Theta(d^2)$ coefficients (pas bits) ;
> * **Attention**, les coefficients peuvent être de grands nombres, et donc le temps de calcul en secondes peut ne pas être en $\Theta(d^2 \log n)$...
>
> **Peut-on faire mieux ?**
> * Oui, avec la [transformation de Fourier rapide](https://fr.wikipedia.org/wiki/Transformation_de_Fourier_rapide) (FFT) qui permet de faire la multiplication de deux polynômes de taille $d$ en $\Theta(d\log d)$ au lieu de $\Theta(d^2)$. Cela dépasse largement le niveau de papier.
> * Oui, si l'on fait du calcul modulaire en lieu et place du calcul sur les grands entiers. Il y a plusieurs justifications :
>   * Posséder plusieurs résidus permet de reconstruire un grand nombre avec le théorème des restes chinois.
>   * Le calcul de chaque résidu est parallélisable.
>   * Le calcul modulaire est pédagogique, et omniprésent en cryptographie.
>   * Le calcul modulaire est possible facilement avec la plupart des langages tant que le modulo tient sur un mot machine. Par contre le calcul sur les grands entiers est plus délicat, en C par exemple.
>   * Le calcul modulaire peut faire office de preuve de calcul dans la recherche de nouveaux algorithmes ou les exercices d'algorithmiques.

## Quelques problèmes similaires
Voici une liste d'exercices, parfois difficiles à résoudre avec Python3, autour des suites récurrentes linéaires.

Plusieurs problèmes de pavages en suivant ce lien : [M5TILE](https://www.spoj.com/problems/M5TILE/).
* Il y en a des plus faciles, comme [M3TILE](https://www.spoj.com/problems/M3TILE/) et [M4TILE](https://www.spoj.com/problems/GNY07H/).
* Il y en a des plus durs, comme [MNTILE](https://www.spoj.com/problems/MNTILE/), [DOJ1](https://www.spoj.com/problems/DOJ1/) et [DOJ2](https://www.spoj.com/problems/DOJ2/).

Des problèmes variés, de pavage ou non :

> * L'énoncé est en anglais.
> * *Solvers* indique une forme de difficulté ; le nombre de participants qui ont résolu le problème. Attention, beaucoup de participants utilisent le langage C.
> * Le temps indique un temps personnel en Python3 avec un code optimisé. C'est souvent le temps à battre.
> * Un titre en gras indique un problème particulièrement difficile en Python3 ; une première résolution en C étant conseillée.

|Title|Solvers|Time|
|:----|:-----:|---:|
|[Fibonacci Sum](https://www.spoj.com/problems/FIBOSUM/)|5227|0.02s|
|[Just Add It](https://www.spoj.com/problems/ZSUM/)|3985|0.01s|
|[Recursive Sequence](https://www.spoj.com/problems/SEQ/)|2110|1.12s|
|**[Flibonakki](https://www.spoj.com/problems/FLIB/)**|785|0.08s|
|**[Recursive Sequence (Version II)](https://www.spoj.com/problems/SPP/)**|710|0.04s|
|[Arya Rage](https://www.spoj.com/problems/MNNITAR/)|310|0.02s|
|**[Nacci Fear](https://www.spoj.com/problems/NACCI/)**|283|0.28s|
|[Fun with numbers](https://www.spoj.com/problems/NUMPLAY/)|263 | 0.01s|
|[Sum of products](https://www.spoj.com/problems/SUMMUL/)|255|0.02s|
|**[Sum of Tetranacci numbers](https://www.spoj.com/problems/TETRAHRD/)**|217|0.07s|
|[Fibonacci With a Square Root](https://www.spoj.com/problems/FIBOSQRT/)|139|2.73s|
|[R Numbers](https://www.spoj.com/problems/ITRIX12E/)|181|0.02s|
|[Easy Sequence!](https://www.spoj.com/problems/SEQAGAIN/)|136|0.32s|
|[Blocks for kids](https://www.spoj.com/problems/PBOARD/)|75|0.07s|
|[Snaky Numbers](https://www.spoj.com/problems/SNAKYNUM/)|73|0.08s|
|**[Grid Tiling](https://www.spoj.com/problems/BTCODE_J/)**|18|0.11s|
|[Moon Safari (Hard)](https://www.spoj.com/problems/MOON2/)|15|23.32s|
|[100pct failure in 72 hours](https://www.spoj.com/problems/HAL9000/)|4|0.32s|

Des challenges (amélioration de la constante) sur ce genre de problèmes :
* [The SPP constant challenge](https://www.spoj.com/problems/SPPC/)
* [Matrix Exponentiation](https://www.spoj.com/problems/MATEX/)

Des problèmes difficiles sur les suites, en général.
|Title|Solvers|Time|
|:----|:-----:|---:|
|[A Summatory (HARD)](https://www.spoj.com/problems/ASUMHARD/)|52|0.77s|
|[Pibonacci](https://www.spoj.com/problems/PIB/)|41|0.54s|
|[Hofstadter–Conway 10000 dollar sequence](https://www.spoj.com/problems/HC10000/)|5|0.48s|

D'autres [problèmes](https://www.spoj.com/problems/FRANCKY/) essentiellement d'arithmétique.

## ANNEXE : fichier `outils.py`

@import "outils.py"