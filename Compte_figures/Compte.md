---
export_on_save:
  html: true
print_background: true
---

# Compter le nombre de triangles dans un triangle

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
