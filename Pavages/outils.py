def rec_lin_suc(a, r, n):
    """Retourne le terme $a_n$ de la suite récurrente linéaire d'ordre $d$ où
    * $a$ est une liste de longueur $d$ : les valeurs initiales ;
    * $r$ est une liste de longueur $d$ : les coefficients de la récurrence ;
    * $n$ est un entier : le range du terme à calculer.
    Méthode avec calculs successifs, complexité O(d×n)
    """
    
    d = len(a) # l'ordre
    assert len(r) == d, "a et r doivent être de même longueur"
    assert n >= 0, "n doit être positif"
    
    if n < d: return a[n]
    a = a[:]
    for _ in range(d, n + 1):
        a.append(sum(ai * ri for ai, ri in zip(a, r)))
        del a[0]
    return a[-1]


def rec_lin_mat(a, r, n):
    """Retourne le terme $a_n$ de la suite récurrente linéaire d'ordre $d$ où
    * $a$ est une liste de longueur $d$ : les valeurs initiales ;
    * $r$ est une liste de longueur $d$ : les coefficients de la récurrence ;
    * $n$ est un entier : le range du terme à calculer.
    Méthode avec matrices, complexité Θ(d^3 log(n))
    """
    
    d = len(a) # l'ordre
    assert len(r) == d, "a et r doivent être de même longueur"
    assert n >= 0, "n doit être positif"

    def matrice_compagnon(r):
        """Retourne la matrice compagnon associée à la récurrence $r$"""
        d = len(r)
        M = [[0]*d for _ in range(d)]
        for i in range(d-1):
            M[i+1][i] = 1
        for i in range(d):
            M[i][-1] = r[i]
        return M

    def puissance(A, n):
        """Retourne la matrice A à la puissance n, où
        * A est une matrice carrée (taille d).
        * n entier positif ou nul.
        Exponentiation rapide, complexité Θ(d^3 log(n))"""

        def produit(A, B):
            """Retourne le produit des deux matrices carrées de taille d : A × B.
            Complexité Θ(d^3)"""
            d = len(A)
            M = [[0]*d for i in range(d)]
            for i in range(d):
                for j in range(d):
                    M[i][j] = sum(A[i][k] * B[k][j] for k in range(d))
            return M
        
        d = len(A)
        M = [[0]*d for i in range(d)]
        for i in range(d):
            M[i][i] = 1
        for digit in bin(n)[2:]:
            M = produit(M, M)
            if digit == "1":
                M = produit(M, A)
        return M

    A = puissance(matrice_compagnon(r), n)
    return sum(a[i] * A[i][0] for i in range(d))


def rec_lin_pol(a, r, n):
    """Retourne le terme $a_n$ de la suite récurrente linéaire d'ordre $d$ où
    * $a$ est une liste de longueur $d$ : les valeurs initiales ;
    * $r$ est une liste de longueur $d$ : les coefficients de la récurrence ;
    * $n$ est un entier : le range du terme à calculer.
    Méthode avec polynômes, complexité Θ(d^2 log(n))
    """
    
    # r = (r_0, r_1, ..., r_{d-1})
    # le calcul polynomial se fait modulo la relation :
    # X^d = r_0 + r_1×X + r_2×X^2 + ... r_{d-1}×X^{d-1}

    d = len(a) # l'ordre
    assert len(r) == d, "a et r doivent être de même longueur"
    assert n >= 0, "n doit être positif"

    def multX(A):
        """Multiplication du polynôme A par X,
        puis réduction modulo la relation.
        Complexité : Θ(d)
        """
        # Multiplication par X
        A.insert(0, 0)
        
        # Réduction
        c_d = A.pop()  # coeff dominant ; celui de X^d
        for i in range(d):
            A[i] += c_d * r[i]
    
    # pré-calcul de X^d à X^{2d-2}, dans liste Xdpi
    # Xdpi := X^{d+i}
    Xdpi =[r[:]]
    for _ in range(d - 2):
        Xdpi.append(Xdpi[-1][:])
        multX(Xdpi[-1])
    
    def produit(A, B):
        """Multiplication des polynômes A et B,
        puis réduction modulo la relation.
        Complexité : Θ(d^2)
        """
        # Multiplication Y := A×B
        Y = [0]*(2*d -1)
        for i in range(d):
            for j in range(d):
                Y[i+j] += A[i] * B[j]
        # Réduction
        for i in range(d - 2, -1, -1):
            ydpi = Y.pop()
            # ydpi est le coeff de X^{d+i} dans Y
            for j in range(d):
                Y[j] += ydpi * Xdpi[i][j]
        return Y

    # Calcul de X^n modulo la relation
    Xn = [0]*d
    Xn[0] = 1 # Xn := X^0
    for digit in bin(n)[2:]:
        Xn = produit(Xn, Xn)
        if digit == "1":
            multX(Xn)

    # Calcul du terme de la suite récurrente linéaire
    return sum(a[i] * Xn[i] for i in range(d))

