import numpy as np
from numpy.linalg import det, inv, solve, matrix_rank
import matplotlib.pyplot as plt
import sympy as sp

def exercise1():


    A_a = np.array([[1, 2, 1], [2, -1, 1], [2, 1, 0]])
    b_a = np.array([0, 0, 0])
    
    try:
        x_a = np.linalg.solve(A_a, b_a)
        print("(a) Solution:")
        print(f"x = {x_a[0]}, y = {x_a[1]}, z = {x_a[2]}")
    except np.linalg.LinAlgError:
        aug_rank = np.linalg.matrix_rank(np.column_stack((A_a, b_a)))
        A_rank = np.linalg.matrix_rank(A_a)
        
        if aug_rank == A_rank:
            print("(a) The system has infinitely many solutions.")
            x_a = np.linalg.pinv(A_a) @ b_a
            print("(a) One possible solution:")
            print(f"x = {x_a[0]}, y = {x_a[1]}, z = {x_a[2]}")
        else:
            print("(a) The system has no solution.")
    
    # (b)
    A_b = np.array([[2, 1, 1, 1], [1, 2, 1, 1], [1, 1, 2, 2], [1, 1, 1, 2]])
    b_b = np.array([1, 1, 1, 1])
    
    try:
        x_b = np.linalg.solve(A_b, b_b)
        print("\n(b) Solution:")
        print(f"x = {x_b[0]}, y = {x_b[1]}, z = {x_b[2]}, t = {x_b[3]}")
    except np.linalg.LinAlgError:
        aug_rank = np.linalg.matrix_rank(np.column_stack((A_b, b_b)))
        A_rank = np.linalg.matrix_rank(A_b)
        
        if aug_rank == A_rank:
            print("\n(b) The system has infinitely many solutions.")
            x_b = np.linalg.pinv(A_b) @ b_b
            print("(b) One possible solution:")
            print(f"x = {x_b[0]}, y = {x_b[1]}, z = {x_b[2]}, t = {x_b[3]}")
        else:
            print("\n(b) The system has no solution.")

def exercise2():

    def analyze_system_2var(a1, b1, c1, a2, b2, c2, a3, b3, c3):
        A = np.array([[a1, b1], [a2, b2], [a3, b3]])
        b = np.array([c1, c2, c3])
        
        x = np.linspace(-10, 10, 100)
        fig, ax = plt.subplots(figsize=(8, 6))
        
        for i in range(3):
            if A[i, 1] != 0:
                y = (b[i] - A[i, 0] * x) / A[i, 1]
                ax.plot(x, y, label=f"{A[i, 0]}x + {A[i, 1]}y = {b[i]}")
            else:
                if A[i, 0] != 0:
                    x_val = b[i] / A[i, 0]
                    ax.axvline(x=x_val, label=f"{A[i, 0]}x = {b[i]}")
        
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.grid(True)
        ax.axhline(y=0, color='k', linestyle='--', alpha=0.3)
        ax.axvline(x=0, color='k', linestyle='--', alpha=0.3)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('System of Linear Equations')
        ax.legend()
        
        rank_A = np.linalg.matrix_rank(A)
        rank_augmented = np.linalg.matrix_rank(np.column_stack((A, b)))
        
        if rank_augmented > rank_A:
            print("The system has no solutions.")
            solution_type = "No solution"
        elif rank_A < 2:
            print("The system has infinitely many solutions.")
            solution_type = "Infinitely many solutions"
        else:
            x_sol, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
            print(f"The system has a unique solution: x = {x_sol[0]}, y = {x_sol[1]}")
            ax.plot(x_sol[0], x_sol[1], 'ro', markersize=8, label='Solution')
            ax.legend()
            solution_type = "Unique solution"
        
        return solution_type
    
    print("\n(a) Example of a system with no solutions:")
    analyze_system_2var(1, 1, 2, 1, 1, 3, 1, 1, 4)
    
    print("\n(b) Example of a system with a unique solution:")
    analyze_system_2var(1, 1, 2, 2, 1, 3, 3, 2, 5)
    
    print("\n(c) Example of a system with infinitely many solutions:")
    analyze_system_2var(1, 1, 2, 2, 2, 4, 3, 3, 6)

def exercise3():

    def analyze_system_3var(a1, b1, c1, d1, a2, b2, c2, d2, a3, b3, c3, d3):
        A = np.array([[a1, b1, c1], [a2, b2, c2], [a3, b3, c3]])
        b = np.array([d1, d2, d3])
        
        rank_A = np.linalg.matrix_rank(A)
        rank_augmented = np.linalg.matrix_rank(np.column_stack((A, b)))
        
        if rank_augmented > rank_A:
            print("The system has no solutions.")
            solution_type = "No solution"
        elif rank_A < 3:
            print("The system has infinitely many solutions.")
            solution_type = "Infinitely many solutions"
        else:
            x_sol = np.linalg.solve(A, b)
            print(f"The system has a unique solution: x = {x_sol[0]}, y = {x_sol[1]}, z = {x_sol[2]}")
            solution_type = "Unique solution"
        
        return solution_type
    
    print("\n(a) Example of a system with no solutions:")
    analyze_system_3var(1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 3)
    
    print("\n(b) Example of a system with a unique solution:")
    analyze_system_3var(1, 1, 1, 6, 1, 2, 3, 14, 2, 3, 1, 11)
    
    print("\n(c) Example of a system with infinitely many solutions:")
    analyze_system_3var(1, 1, 1, 3, 2, 2, 2, 6, 3, 3, 3, 9)

def exercise4():
     
    A = np.array([[1, 1, 2], [3, 6, -5], [2, 4, -3]], dtype=float)
    b = np.array([1, -1, 0], dtype=float)
    
    det_A = np.linalg.det(A)
    print(f"(a) Determinant of A = {det_A}")
    if det_A != 0:
        print("   A is invertible.")
    else:
        print("   A is not invertible.")
    
    if det_A != 0:
        A_inv = np.linalg.inv(A)
        x_inv = np.dot(A_inv, b)
        print(f"(b) Solution using inverse: x = {x_inv[0]}, y = {x_inv[1]}, z = {x_inv[2]}")
    
    def gaussian_elimination(A, b):
        augmented = np.column_stack((A.copy(), b.copy()))
        n = len(b)
        
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(augmented[j, i]) > abs(augmented[max_row, i]):
                    max_row = j
            
            if max_row != i:
                augmented[[i, max_row]] = augmented[[max_row, i]]
            
            for j in range(i+1, n):
                factor = augmented[j, i] / augmented[i, i]
                augmented[j, i:] -= factor * augmented[i, i:]
        
        x = np.zeros(n)
        for i in range(n-1, -1, -1):
            x[i] = (augmented[i, -1] - np.dot(augmented[i, i+1:n], x[i+1:])) / augmented[i, i]
        
        return x
    
    x_gauss = gaussian_elimination(A, b)
    print(f"(c) Solution using Gaussian elimination: x = {x_gauss[0]}, y = {x_gauss[1]}, z = {x_gauss[2]}")
    
    def gaussian_elimination_partial_pivot(A, b):
        augmented = np.column_stack((A.copy(), b.copy()))
        n = len(b)
        
        for i in range(n):
            max_row = i + np.argmax(abs(augmented[i:, i]))
            
            if max_row != i:
                augmented[[i, max_row]] = augmented[[max_row, i]]
            
            for j in range(i+1, n):
                factor = augmented[j, i] / augmented[i, i]
                augmented[j, i:] -= factor * augmented[i, i:]
        
        x = np.zeros(n)
        for i in range(n-1, -1, -1):
            x[i] = (augmented[i, -1] - np.dot(augmented[i, i+1:n], x[i+1:])) / augmented[i, i]
        
        return x
    
    x_pivot = gaussian_elimination_partial_pivot(A, b)
    print(f"(d) Solution using Gaussian elimination with Partial Pivot: x = {x_pivot[0]}, y = {x_pivot[1]}, z = {x_pivot[2]}")
    
    def lu_decomposition(A):
        n = len(A)
        L = np.zeros((n, n))
        U = np.zeros((n, n))
        
        for i in range(n):
            for j in range(i, n):
                U[i, j] = A[i, j] - sum(L[i, k] * U[k, j] for k in range(i))
            
            L[i, i] = 1
            for j in range(i+1, n):
                L[j, i] = (A[j, i] - sum(L[j, k] * U[k, i] for k in range(i))) / U[i, i]
        
        return L, U
    
    def solve_lu(L, U, b):
        n = len(b)
        y = np.zeros(n)
        for i in range(n):
            y[i] = b[i] - sum(L[i, j] * y[j] for j in range(i))
        
        x = np.zeros(n)
        for i in range(n-1, -1, -1):
            x[i] = (y[i] - sum(U[i, j] * x[j] for j in range(i+1, n))) / U[i, i]
        
        return x
    
    L, U = lu_decomposition(A)
    x_lu = solve_lu(L, U, b)
    print(f"(e) Solution using LU method: x = {x_lu[0]}, y = {x_lu[1]}, z = {x_lu[2]}")

def exercise5():

    A = np.array([[1, 2, 1], [2, 2, 2], [2, 4, 1]], dtype=float)
    b = np.array([1, 1, 2], dtype=float)
    
    x_np = np.linalg.solve(A, b)
    print(f"Method 1 (numpy.linalg.solve): x = {x_np[0]}, y = {x_np[1]}, z = {x_np[2]}")
    
    A_inv = np.linalg.inv(A)
    x_inv = np.dot(A_inv, b)
    print(f"Method 2 (inverse matrix): x = {x_inv[0]}, y = {x_inv[1]}, z = {x_inv[2]}")
    
    def lu_decomposition(A):
        n = len(A)
        L = np.zeros((n, n))
        U = np.zeros((n, n))
        
        for i in range(n):
            for j in range(i, n):
                U[i, j] = A[i, j] - sum(L[i, k] * U[k, j] for k in range(i))
            
            L[i, i] = 1
            for j in range(i+1, n):
                L[j, i] = (A[j, i] - sum(L[j, k] * U[k, i] for k in range(i))) / U[i, i]
        
        return L, U
    
    def solve_lu(L, U, b):
        n = len(b)
        y = np.zeros(n)
        for i in range(n):
            y[i] = b[i] - sum(L[i, j] * y[j] for j in range(i))
        
        x = np.zeros(n)
        for i in range(n-1, -1, -1):
            x[i] = (y[i] - sum(U[i, j] * x[j] for j in range(i+1, n))) / U[i, i]
        
        return x
    
    L, U = lu_decomposition(A)
    x_lu = solve_lu(L, U, b)
    print(f"Method 3 (LU decomposition): x = {x_lu[0]}, y = {x_lu[1]}, z = {x_lu[2]}")

def exercise6():

    points = [(1, 6), (2, 15), (3, 38)]
    
    A = np.array([[1, x, x**2] for x, _ in points])
    b = np.array([y for _, y in points])
    
    a = np.linalg.solve(A, b)
    
    print(f"Interpolating polynomial: p(t) = {a[0]} + {a[1]}t + {a[2]}t^2")
    
    for x, y in points:
        p_x = a[0] + a[1]*x + a[2]*x**2
        print(f"p({x}) = {p_x}, original y = {y}")

def exercise7():

    A = np.array([[3, 3.2], [3.5, 3.6]])
    b = np.array([118.4, 135.2])
    
    solution = np.linalg.solve(A, b)
    
    children = round(solution[0])
    adults = round(solution[1])
    
    print(f"Number of children: {children}")
    print(f"Number of adults: {adults}")
    
    bus_cost = 3 * children + 3.2 * adults
    train_cost = 3.5 * children + 3.6 * adults
    print(f"Bus cost: ${bus_cost}")
    print(f"Train cost: ${train_cost}")

def exercise8():
    
    A = np.array([
        [2, -4, 4, 0.077],
        [0, -2, 2, -0.056],
        [2, -2, 0, 0]
    ])
    b = np.array([3.86, -3.47, 0])
    
    solution = np.linalg.solve(A, b)
    
    print(f"x = {solution[0]}")
    print(f"y = {solution[1]}")
    print(f"z = {solution[2]}")
    print(f"t = {solution[3]}")

def exercise9():
    
    A = np.array([
        [0.61, 0.29, 0.15],
        [0.35, 0.59, 0.063],
        [0.04, 0.12, 0.787]
    ])
    
    A_inv = np.linalg.inv(A)
    
    print("Conversion matrix from CIE (X,Y,Z) to (R,G,B):")
    print(A_inv)
    
    print("\nEquation:")
    print("R = {:.4f}X + {:.4f}Y + {:.4f}Z".format(A_inv[0,0], A_inv[0,1], A_inv[0,2]))
    print("G = {:.4f}X + {:.4f}Y + {:.4f}Z".format(A_inv[1,0], A_inv[1,1], A_inv[1,2]))
    print("B = {:.4f}X + {:.4f}Y + {:.4f}Z".format(A_inv[2,0], A_inv[2,1], A_inv[2,2]))

def exercise10():
    
    A = np.array([
        [0.25, 0.15, 0.1],
        [0.2, 0.05, 0.15],
        [0.15, 0.15, 0.1]
    ])
    
    d = np.array([100, 100, 100])
    
    I = np.eye(3)
    p = np.linalg.solve(I - A, d)
    
    print(f"Production vector p = [{p[0]}, {p[1]}, {p[2]}]")

def exercise11():
    
    A = np.array([
        [3, 0, -1, 0],    # Carbon
        [8, 0, 0, -2],    # Hydrogen
        [0, 2, -2, -1]    # Oxygen
    ])
    
    b = np.array([0, 0, 0])
    
    U, s, Vh = np.linalg.svd(A)
    
    null_space = Vh[3:]
    
    import sympy as sp
    
    x1, x2, x3, x4 = sp.symbols('x1 x2 x3 x4')
    
    c1 = 3*x1 - x3
    c2 = 8*x1 - 2*x4
    c3 = 2*x2 - 2*x3 - x4
    
    equations = [
        sp.Eq(c1, 0),
        sp.Eq(c2, 0),
        sp.Eq(c3, 0)
    ]
    
    solution = sp.solve(equations, [x1, x2, x3, x4])
    
    x4_val = 4
    x3_val = 3
    x1_val = solution[x1].subs(x3, x3_val)
    x2_val = solution[x2].subs({x3: x3_val, x4: x4_val})
    
    coeffs = [1, 5, 3, 4]
    
    print("Balanced chemical equation:")
    print(f"{coeffs[0]}C3H8 + {coeffs[1]}O2 → {coeffs[2]}CO2 + {coeffs[3]}H2O")
    
    c_atoms = 3*coeffs[0] - 1*coeffs[2]
    h_atoms = 8*coeffs[0] - 2*coeffs[3]
    o_atoms = 2*coeffs[1] - 2*coeffs[2] - 1*coeffs[3]
    
    print("\nVerification:")
    print(f"Carbon balance: {3*coeffs[0]} = {1*coeffs[2]} ({c_atoms == 0})")
    print(f"Hydrogen balance: {8*coeffs[0]} = {2*coeffs[3]} ({h_atoms == 0})")
    print(f"Oxygen balance: {2*coeffs[1]} = {2*coeffs[2] + 1*coeffs[3]} ({o_atoms == 0})")