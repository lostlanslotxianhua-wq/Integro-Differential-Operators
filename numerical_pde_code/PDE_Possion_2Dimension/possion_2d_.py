import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
sns.set_theme(style="whitegrid")




def poisson_2d_jacobi(psi, f, xl, xr, yb, yt, m1, m2, tol=0.5e-10, max_iter=50000):
    
    h1 = (xr - xl) / m1
    h2 = (yt - yb) / m2
    
    x = np.linspace(xl, xr, m1 + 1)
    y = np.linspace(yb, yt, m2 + 1)
    X, Y = np.meshgrid(x, y, indexing='ij')
    
    U = np.zeros((m1 + 1, m2 + 1))
    
    U[0, :]  = psi(x[0], y)  
    U[-1, :] = psi(x[-1], y)  
    U[:, 0]  = psi(x, y[0])   
    U[:, -1] = psi(x, y[-1]) 
    
    F = f(X, Y)
    c1 = 1.0 / (h1 ** 2)
    c2 = 1.0 / (h2 ** 2)
    denom = 2.0 * (c1 + c2)
    
    for k in range(max_iter):
        U_old = U.copy()
        
        U[1:-1, 1:-1] = (F[1:-1, 1:-1] + 
                         c2 * U_old[1:-1, :-2] + c1 * U_old[:-2, 1:-1] + 
                         c1 * U_old[2:, 1:-1]  + c2 * U_old[1:-1, 2:]) / denom
        
        if np.max(np.abs(U - U_old)) <= tol:
            print(f"收敛于第 {k+1} 步")
            break
            
    return X, Y, U


if __name__ == "__main__":
    
    # 初始化参数
    xl, xr = 0.0, 2.0
    yb, yt = 0.0, 1.0
    m1, m2 = 16, 8    # 对应 h1 = 1/8, h2 = 1/8
    
    # 定义右端函数 f(x, y)
    def f(x, y):
        return (np.pi**2 - 1.0) * np.exp(x) * np.sin(np.pi * y)
        
    # 定义边界条件函数 psi(x, y)
    def psi(x, y):
        return np.exp(x) * np.sin(np.pi * y)
        
    # 精确解
    def exact_solution(x, y):
        return np.exp(x) * np.sin(np.pi * y)


    # 求解
    X, Y, U_num = poisson_2d_jacobi(psi, f, xl, xr, yb, yt, m1, m2)
    
    U_exact = exact_solution(X, Y)

    # 输出对应点的数值
    test_points = [(0.5, 0.25), (1.0, 0.25), (1.5, 0.25), (0.5, 0.5), (1.0, 0.5)]
    
    print(f"{'(x, y)':<12} | {'数值解':<14} | {'绝对误差'}")
    
    h1 = (xr - xl) / m1
    h2 = (yt - yb) / m2
    
    for (px, py) in test_points:
        idx_i = int(round((px - xl) / h1))
        idx_j = int(round((py - yb) / h2))
        
        val_num = U_num[idx_i, idx_j]
        val_exact = U_exact[idx_i, idx_j]
        err = abs(val_num - val_exact)
        
        print(f"({px:.1f}, {py:.2f})  | {val_num:<14.6f} | {err:.6e}")
    
    max_error = np.max(np.abs(U_num - U_exact))
    print(f"max error: {max_error:.5e}\n")


    plt.style.use('default')
    fig = plt.figure(figsize=(18, 5))
    surf_kwargs = {'cmap': 'viridis', 'edgecolor': 'black', 'linewidth': 0.3, 'alpha': 0.9}

    ax1 = fig.add_subplot(1, 3, 1, projection='3d')
    ax1.plot_surface(X, Y, U_num, **surf_kwargs)
    ax1.set_title('Numerical Solution')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_zlabel('u_h(x, y)')

    ax2 = fig.add_subplot(1, 3, 2, projection='3d')
    ax2.plot_surface(X, Y, U_exact, **surf_kwargs)
    ax2.set_title('Exact Solution')
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    ax2.set_zlabel('u(x, y)')

    ax3 = fig.add_subplot(1, 3, 3, projection='3d')
    ax3.plot_surface(X, Y, np.abs(U_num - U_exact), cmap='viridis', edgecolor='black', linewidth=0.3, alpha=0.9)
    ax3.set_title('Error')
    ax3.set_xlabel('x')
    ax3.set_ylabel('y')
    ax3.set_zlabel('|Error|')

    plt.tight_layout()
    plt.show()