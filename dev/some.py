import numpy as np
import matplotlib.pyplot as plt

mean = [0, 0, 0]
cov = [
    [2, 0.5, 0],
    [0.5, 1, 0.2],
    [0, 0.2, 3]
    ]

n_samples = 100
data_points = np.random.multivariate_normal(mean, cov, n_samples)

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(data_points[:, 0], data_points[:, 1], data_points[:, 2], s=1, alpha=0.3)
ax.set_title('3D Multivariate Normal Distribution (Point Cloud)')
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
plt.show()