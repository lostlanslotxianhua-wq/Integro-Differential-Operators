import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="whitegrid")

def possion_1d(q, f, start, end, m, boundary, dtype=np.float64):
    
    h = (end - start) / m
    x = np.linspace(start, end, m + 1, dtype=dtype)
    n = m - 1
    
    alpha = -1
    gamma = -1
    beta = 2 + h**2 * q(x[1:-1])
    
    d = h**2 * f(x[1:-1])
    d[0] += boundary[0]
    d[-1] += boundary[1]

    w = np.zeros(n, dtype=dtype)
    g = np.zeros(n, dtype=dtype)
    
    w[0] = gamma / beta[0]
    g[0] = d[0] / beta[0]
    
    for i in range(1, n):
        denom = beta[i] - alpha * w[i - 1]
        w[i] = gamma / denom
        g[i] = (d[i] - alpha * g[i - 1]) / denom

    u = np.zeros(m + 1, dtype = dtype)
    u[0] = boundary[0]
    u[-1] = boundary[1]

    u[m - 1] = g[-1]
    
    for i in range(n - 2, -1, -1):
        u[i + 1] = g[i] - w[i] * u[i + 2]
        
    return x, u


if __name__ == "__main__":

    start = 0
    end = np.pi
    m = 80
    boundary = [0, 0]

    def q(x):
        return np.ones_like(x)

    def f(x):
        return np.exp(x) * (np.sin(x) - 2 * np.cos(x))

    x, u_num = possion_1d(
        q=q, 
        start=start, 
        end=end, 
        m=m, 
        boundary=boundary, 
        f=f, 
        dtype=np.float64
    )

    u_exact = np.exp(x) * np.sin(x)

    print(f"{'x':<8} | {'numerical solution':<12}| {'abs error'}")

    for i in range(1, 5):
        idx = i * (m // 5) 
        val_num = u_num[idx]
        val_exact = u_exact[idx]
        error_abs = np.abs(val_num - val_exact)
        
        print(f"{f"{i}π/5":<8} | {val_num:<14.6f}| {error_abs:.6e}")

    plt.figure(figsize=(10, 6))
    sns.lineplot(x=x, y=u_num, label='Numerical Solution', color='gray', linewidth=2)
    sns.lineplot(x=x, y=u_exact, label='Analytical Solution', color='black', linestyle='--', linewidth=2)
    plt.title(f'Solution Comparison (m = {m})')
    plt.xlabel('x')
    plt.ylabel('u(x)')
    plt.legend()
    plt.show()


    error = np.abs(u_exact - u_num)
    print(f"max error: {np.max(error):.5e}")

    plt.figure(figsize=(10, 6))
    sns.lineplot(x=x, y=error, label='Error', color='black', linewidth=2)
    plt.title(f'Error Plot (m = {m})')
    plt.xlabel('x')
    plt.ylabel('Absolute Error')
    plt.legend()
    plt.show()
