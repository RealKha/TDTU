import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math

def exercise1():
    A = np.array([[2, 2], [2, 3]])
    b = np.array([4, 6])

    AT_A = np.dot(A.T, A)
    AT_b = np.dot(A.T, b)

    x = np.linalg.solve(AT_A, AT_b)

    return x

def exercise2():
    A = np.array([
        [0, 0, 1],
        [0, 1, 1],
        [1, 2, 1],
        [1, 0, 1],
        [4, 1, 1],
        [4, 2, 1]
    ])
    b = np.array([0.5, 1.6, 2.8, 0.8, 5.1, 5.9])

    x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)

    return x, residuals

def exercise3(points):
    x = [p[0] for p in points]
    y = [p[1] for p in points]

    A = np.column_stack((np.ones(len(x)), x))

    params, residuals, rank, s = np.linalg.lstsq(A, y, rcond=None)

    a0, a1 = params
    return a0, a1

def exercise4():
    mileage = np.array([2000, 6000, 20000, 30000, 40000])
    friction_index = np.array([20, 18, 10, 6, 2])

    A = np.column_stack((np.ones(len(mileage)), mileage))

    params, residuals, rank, s = np.linalg.lstsq(A, friction_index, rcond=None)

    a0, a1 = params

    x_fit = np.linspace(0, 45000, 100)
    y_fit = a0 + a1 * x_fit

    plt.figure(figsize=(10, 6))
    plt.scatter(mileage, friction_index, color='red', marker='o', label='Data points')
    plt.plot(x_fit, y_fit, 'b-', label=f'Fitted line: y = {a0:.4f} + {a1:.8f}x')
    plt.xlabel('Mileage')
    plt.ylabel('Friction Index')
    plt.title('Friction Index vs Mileage')
    plt.legend()
    plt.grid(True)

    return a0, a1

def exercise5():
    x_data = np.array([1, 2, 3])
    y_data = np.array([7.9, 5.4, -9])

    A = np.column_stack((np.cos(x_data), np.sin(x_data)))

    params, residuals, rank, s = np.linalg.lstsq(A, y_data, rcond=None)

    A_coef, B_coef = params

    x_fit = np.linspace(0, 4, 100)
    y_fit = A_coef * np.cos(x_fit) + B_coef * np.sin(x_fit)

    plt.figure(figsize=(10, 6))
    plt.scatter(x_data, y_data, color='red', marker='o', label='Data points')
    plt.plot(x_fit, y_fit, 'b-', label=f'Fitted curve: y = {A_coef:.4f}*cos(x) + {B_coef:.4f}*sin(x)')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Least Squares Fit with A*cos(x) + B*sin(x)')
    plt.legend()
    plt.grid(True)

    return A_coef, B_coef

def exercise6():
    time = np.array([1, 2, 3, 4, 5, 6])
    grams = np.array([2.1, 3.5, 4.2, 3.1, 4.4, 6.8])

    A = np.column_stack((time**3, time**2, time, np.ones(len(time))))

    params, residuals, rank, s = np.linalg.lstsq(A, grams, rcond=None)

    a, b, c, d = params

    x_fit = np.linspace(0, 7, 100)
    y_fit = a * x_fit**3 + b * x_fit**2 + c * x_fit + d

    plt.figure(figsize=(10, 6))
    plt.scatter(time, grams, color='red', marker='o', label='Data points')
    plt.plot(x_fit, y_fit, 'b-', label=f'Fitted curve: y = {a:.4f}x³ + {b:.4f}x² + {c:.4f}x + {d:.4f}')
    plt.xlabel('Time (days)')
    plt.ylabel('Bacteria Growth (grams)')
    plt.title('Bacteria Growth over Time')
    plt.legend()
    plt.grid(True)

    return a, b, c, d

def exercise7():

    x = np.linspace(-5, 5, 10)
    y = np.linspace(-5, 5, 10)
    X, Y = np.meshgrid(x, y)
    points = np.vstack([X.flatten(), Y.flatten()])

    S_2_2 = np.array([[2, 0], [0, 2]])
    S_05_05 = np.array([[0.5, 0], [0, 0.5]])
    S_1_n1 = np.array([[1, 0], [0, -1]])
    S_n1_1 = np.array([[-1, 0], [0, 1]])

    points_S_2_2 = np.dot(S_2_2, points)
    points_S_05_05 = np.dot(S_05_05, points)
    points_S_1_n1 = np.dot(S_1_n1, points)
    points_S_n1_1 = np.dot(S_n1_1, points)

    fig, axs = plt.subplots(2, 2, figsize=(12, 12))

    axs[0, 0].scatter(points[0], points[1], color='blue', s=10, label='Original')

    axs[0, 0].scatter(points_S_2_2[0], points_S_2_2[1], color='red', s=10, label='S_2_2')
    axs[0, 0].set_title('λ=2, μ=2 (Uniform scaling by 2)')
    axs[0, 0].grid(True)
    axs[0, 0].legend()

    axs[0, 1].scatter(points[0], points[1], color='blue', s=10, label='Original')
    axs[0, 1].scatter(points_S_05_05[0], points_S_05_05[1], color='red', s=10, label='S_0.5_0.5')
    axs[0, 1].set_title('λ=0.5, μ=0.5 (Uniform scaling by 0.5)')
    axs[0, 1].grid(True)
    axs[0, 1].legend()

    axs[1, 0].scatter(points[0], points[1], color='blue', s=10, label='Original')
    axs[1, 0].scatter(points_S_1_n1[0], points_S_1_n1[1], color='red', s=10, label='S_1_-1')
    axs[1, 0].set_title('λ=1, μ=-1 (Reflection about x-axis)')
    axs[1, 0].grid(True)
    axs[1, 0].legend()

    axs[1, 1].scatter(points[0], points[1], color='blue', s=10, label='Original')
    axs[1, 1].scatter(points_S_n1_1[0], points_S_n1_1[1], color='red', s=10, label='S_-1_1')
    axs[1, 1].set_title('λ=-1, μ=1 (Reflection about y-axis)')
    axs[1, 1].grid(True)
    axs[1, 1].legend()

    plt.tight_layout()

    return {
        'S_2_2': S_2_2,
        'S_05_05': S_05_05,
        'S_1_n1': S_1_n1,
        'S_n1_1': S_n1_1
    }

def exercise8():

    x = np.linspace(-5, 5, 10)
    y = np.linspace(-5, 5, 10)
    X, Y = np.meshgrid(x, y)
    points = np.vstack([X.flatten(), Y.flatten()])

    theta_pi = np.pi
    R_pi = np.array([
        [np.cos(theta_pi), -np.sin(theta_pi)],
        [np.sin(theta_pi), np.cos(theta_pi)]
    ])

    theta_pi_3 = np.pi/3
    R_pi_3 = np.array([
        [np.cos(theta_pi_3), -np.sin(theta_pi_3)],
        [np.sin(theta_pi_3), np.cos(theta_pi_3)]
    ])

    points_R_pi = np.dot(R_pi, points)
    points_R_pi_3 = np.dot(R_pi_3, points)

    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    axs[0].scatter(points[0], points[1], color='blue', s=10, label='Original')

    axs[0].scatter(points_R_pi[0], points_R_pi[1], color='red', s=10, label='R_π')
    axs[0].set_title('Rotation by π (180°)')
    axs[0].grid(True)
    axs[0].legend()

    axs[1].scatter(points[0], points[1], color='blue', s=10, label='Original')
    axs[1].scatter(points_R_pi_3[0], points_R_pi_3[1], color='red', s=10, label='R_π/3')
    axs[1].set_title('Rotation by π/3 (60°)')
    axs[1].grid(True)
    axs[1].legend()

    plt.tight_layout()

    return {
        'R_pi': R_pi,
        'R_pi_3': R_pi_3
    }

def exercise9():

    house = np.array([
        [0, 0, 4, 4, 2, 0],
        [0, 4, 4, 0, 6, 0]
    ])

    tx, ty = 2, 4
    translation_matrix = np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ])

    house_homogeneous = np.vstack([house, np.ones(house.shape[1])])

    translated_house = np.dot(translation_matrix, house_homogeneous)

    alpha = np.pi/3
    rotation_matrix = np.array([
        [np.cos(alpha), -np.sin(alpha), 0],
        [np.sin(alpha), np.cos(alpha), 0],
        [0, 0, 1]
    ])

    rotated_house = np.dot(rotation_matrix, house_homogeneous)

    sx, sy = 2, 3
    scaling_matrix = np.array([
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ])

    scaled_house = np.dot(scaling_matrix, house_homogeneous)

    shx = 0.5
    shear_x_matrix = np.array([
        [1, shx, 0],
        [0, 1, 0],
        [0, 0, 1]
    ])

    sheared_x_house = np.dot(shear_x_matrix, house_homogeneous)

    shy = -1.5
    shear_y_matrix = np.array([
        [1, 0, 0],
        [shy, 1, 0],
        [0, 0, 1]
    ])

    sheared_y_house = np.dot(shear_y_matrix, house_homogeneous)

    fig, axs = plt.subplots(2, 3, figsize=(15, 10))

    axs[0, 0].plot(house[0], house[1], 'b-')
    axs[0, 0].set_title('Original House')
    axs[0, 0].set_xlim(-2, 10)
    axs[0, 0].set_ylim(-2, 10)
    axs[0, 0].grid(True)

    axs[0, 1].plot(house[0], house[1], 'b--', alpha=0.5)
    axs[0, 1].plot(translated_house[0], translated_house[1], 'r-')
    axs[0, 1].set_title(f'Translation (tx={tx}, ty={ty})')
    axs[0, 1].set_xlim(-2, 10)
    axs[0, 1].set_ylim(-2, 10)
    axs[0, 1].grid(True)

    axs[0, 2].plot(house[0], house[1], 'b--', alpha=0.5)
    axs[0, 2].plot(rotated_house[0], rotated_house[1], 'g-')
    axs[0, 2].set_title(f'Rotation (α=π/3)')
    axs[0, 2].set_xlim(-7, 7)
    axs[0, 2].set_ylim(-7, 7)
    axs[0, 2].grid(True)

    axs[1, 0].plot(house[0], house[1], 'b--', alpha=0.5)
    axs[1, 0].plot(scaled_house[0], scaled_house[1], 'c-')
    axs[1, 0].set_title(f'Scaling (sx={sx}, sy={sy})')
    axs[1, 0].set_xlim(-2, 10)
    axs[1, 0].set_ylim(-2, 20)
    axs[1, 0].grid(True)

    axs[1, 1].plot(house[0], house[1], 'b--', alpha=0.5)
    axs[1, 1].plot(sheared_x_house[0], sheared_x_house[1], 'm-')
    axs[1, 1].set_title(f'Shear along x (sh_x={shx})')
    axs[1, 1].set_xlim(-2, 10)
    axs[1, 1].set_ylim(-2, 10)
    axs[1, 1].grid(True)

    axs[1, 2].plot(house[0], house[1], 'b--', alpha=0.5)
    axs[1, 2].plot(sheared_y_house[0], sheared_y_house[1], 'y-')
    axs[1, 2].set_title(f'Shear along y (sh_y={shy})')
    axs[1, 2].set_xlim(-10, 10)
    axs[1, 2].set_ylim(-10, 10)
    axs[1, 2].grid(True)

    plt.tight_layout()

    return {
        'translation_matrix': translation_matrix,
        'rotation_matrix': rotation_matrix,
        'scaling_matrix': scaling_matrix,
        'shear_x_matrix': shear_x_matrix,
        'shear_y_matrix': shear_y_matrix
    }

def exercise10():

    P = np.array([1, 1])
    Q = np.array([3, 1])
    R = np.array([1, 3])

    A = np.column_stack((P, Q, R))

    neg_I = -np.eye(2)

    transformed_A = np.dot(neg_I, A)

    P_transformed = transformed_A[:, 0]
    Q_transformed = transformed_A[:, 1]
    R_transformed = transformed_A[:, 2]

    plt.figure(figsize=(8, 8))

    plt.plot([P[0], Q[0]], [P[1], Q[1]], 'b-', label='Original')
    plt.plot([Q[0], R[0]], [Q[1], R[1]], 'b-')
    plt.plot([R[0], P[0]], [R[1], P[1]], 'b-')
    plt.scatter([P[0], Q[0], R[0]], [P[1], Q[1], R[1]], color='blue')
    plt.annotate('P', P, xytext=(P[0]-0.3, P[1]-0.3))
    plt.annotate('Q', Q, xytext=(Q[0]+0.1, Q[1]-0.3))
    plt.annotate('R', R, xytext=(R[0]-0.3, R[1]+0.1))

    plt.plot([P_transformed[0], Q_transformed[0]], [P_transformed[1], Q_transformed[1]], 'r-', label='Transformed')
    plt.plot([Q_transformed[0], R_transformed[0]], [Q_transformed[1], R_transformed[1]], 'r-')
    plt.plot([R_transformed[0], P_transformed[0]], [R_transformed[1], P_transformed[1]], 'r-')
    plt.scatter([P_transformed[0], Q_transformed[0], R_transformed[0]], [P_transformed[1], Q_transformed[1], R_transformed[1]], color='red')
    plt.annotate('P\'', P_transformed, xytext=(P_transformed[0]-0.3, P_transformed[1]-0.3))
    plt.annotate('Q\'', Q_transformed, xytext=(Q_transformed[0]+0.1, Q_transformed[1]-0.3))
    plt.annotate('R\'', R_transformed, xytext=(R_transformed[0]-0.3, R_transformed[1]+0.1))

    plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    plt.grid(True)
    plt.axis('equal')
    plt.xlim(-4, 4)
    plt.ylim(-4, 4)
    plt.title('Triangle Transformation under (-I)')
    plt.legend()

    return {
        'original_vertices': {'P': P, 'Q': Q, 'R': R},
        'transformed_vertices': {'P': P_transformed, 'Q': Q_transformed, 'R': R_transformed}
    }

def exercise11():

    F = np.array([
        [0, 1, 1, 0, 0],
        [0, 0, 1, 1, 0]
    ])

    F_homogeneous = np.vstack([F, np.ones(F.shape[1])])

    T1 = np.array([
        [-1, 0, 0],
        [0, -1, 0],
        [0, 0, 1]
    ])

    T2 = np.array([
        [1/4, 0, 0],
        [0, 1/4, 0],
        [0, 0, 1]
    ])

    T3 = np.array([
        [1, 0, 5/4],
        [0, 1, -5/4],
        [0, 0, 1]
    ])

    T4 = np.array([
        [1/4, 0, 5/4],
        [0, 1/4, -5/4],
        [0, 0, 1]
    ])

    T5 = np.array([
        [-1/4, 0, 0],
        [0, -1/4, 0],
        [0, 0, 1]
    ])

    T6 = np.array([
        [-1/4, 0, -5/4],
        [0, -1/4, 5/4],
        [0, 0, 1]
    ])

    T7 = np.array([
        [1, -1, 5/4],
        [0, 0, 5/4],
        [0, 0, 1]
    ])

    F1 = np.dot(T1, F_homogeneous)
    F2 = np.dot(T2, F_homogeneous)
    F3 = np.dot(T3, F_homogeneous)
    F4 = np.dot(T4, F_homogeneous)
    F5 = np.dot(T5, F_homogeneous)
    F6 = np.dot(T6, F_homogeneous)
    F7 = np.dot(T7, F_homogeneous)

    fig, axs = plt.subplots(2, 4, figsize=(16, 8))

    axs[0, 0].plot(F[0], F[1], 'b-')
    axs[0, 0].set_title('Original Figure F')
    axs[0, 0].set_xlim(-2, 2)
    axs[0, 0].set_ylim(-2, 2)
    axs[0, 0].grid(True)

    axs[0, 1].plot(F[0], F[1], 'b--', alpha=0.3)
    axs[0, 1].plot(F1[0], F1[1], 'r-')
    axs[0, 1].set_title('T1: Reflection about origin')
    axs[0, 1].set_xlim(-2, 2)
    axs[0, 1].set_ylim(-2, 2)
    axs[0, 1].grid(True)

    axs[0, 2].plot(F[0], F[1], 'b--', alpha=0.3)
    axs[0, 2].plot(F2[0], F2[1], 'g-')
    axs[0, 2].set_title('T2: Scaling by 1/4')
    axs[0, 2].set_xlim(-2, 2)
    axs[0, 2].set_ylim(-2, 2)
    axs[0, 2].grid(True)

    axs[0, 3].plot(F[0], F[1], 'b--', alpha=0.3)
    axs[0, 3].plot(F3[0], F3[1], 'c-')
    axs[0, 3].set_title('T3: Translation (5/4, -5/4)')
    axs[0, 3].set_xlim(-2, 3)
    axs[0, 3].set_ylim(-2, 2)
    axs[0, 3].grid(True)

    axs[1, 0].plot(F[0], F[1], 'b--', alpha=0.3)
    axs[1, 0].plot(F4[0], F4[1], 'm-')
    axs[1, 0].set_title('T4: Scale by 1/4 + Translation')
    axs[1, 0].set_xlim(-2, 3)
    axs[1, 0].set_ylim(-2, 2)
    axs[1, 0].grid(True)

    axs[1, 1].plot(F[0], F[1], 'b--', alpha=0.3)
    axs[1, 1].plot(F5[0], F5[1], 'y-')
    axs[1, 1].set_title('T5: Scale by -1/4')
    axs[1, 1].set_xlim(-2, 2)
    axs[1, 1].set_ylim(-2, 2)
    axs[1, 1].grid(True)

    axs[1, 2].plot(F[0], F[1], 'b--', alpha=0.3)
    axs[1, 2].plot(F6[0], F6[1], 'k-')
    axs[1, 2].set_title('T6: Scale by -1/4 + Translation')
    axs[1, 2].set_xlim(-3, 2)
    axs[1, 2].set_ylim(-2, 3)
    axs[1, 2].grid(True)

    axs[1, 3].plot(F[0], F[1], 'b--', alpha=0.3)
    axs[1, 3].plot(F7[0], F7[1], 'purple')
    axs[1, 3].set_title('T7: Shear + Translation')
    axs[1, 3].set_xlim(-2, 3)
    axs[1, 3].set_ylim(-2, 3)
    axs[1, 3].grid(True)

    plt.tight_layout()

    T = np.array([
        [1, 0, -2],
        [0, -2, 1],
        [9, 0, 1]
    ])

    F_T = np.dot(T, F_homogeneous)

    plt.figure(figsize=(8, 8))
    plt.plot(F[0], F[1], 'b--', alpha=0.3, label='Original')
    plt.plot(F_T[0], F_T[1], 'r-', label='Transformed')
    plt.title('Figure F transformed by matrix T')
    plt.grid(True)
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    plt.legend()

    return {
        'transformations': {
            'T1': T1, 'T2': T2, 'T3': T3, 'T4': T4,
            'T5': T5, 'T6': T6, 'T7': T7, 'T': T 
        }
    }