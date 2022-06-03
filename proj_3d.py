"""Plot curves in 3D with projection on the x-axis"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def divide_list(x, n):
    """Get n roughly evenly spaced samples from list x
    
    Parameters
    ----------
    x : Sequence
        A python sequence from which to sample.
    n : int
        Number of samples to take.
    
    Returns
    -------
    list
        The samples, length n.
    
    """
    if n < 2 or n > len(x):
        raise(ValueError("n must be >= 2 and <= the length of the input list"))
    new_list = [x[0]]
    if n == 2:
        new_list.append(x[-1])
        return new_list
    points_to_add = n - 1
    len_minus_start = len(x) - 1
    interval = len_minus_start / (points_to_add)
    i = interval
    while len(new_list) < n - 1:
        new_list.append(x[round(i)])
        i += interval
    new_list.append(x[-1])
    return new_list


def get_verts(x, y, z, minz, n=2):
    """
    Get the enpoints of vertical lines to plot from XY plane to data in 3d space.
    
    Parameters
    ----------
    x : Sequence of float
        The x-coordinates of the 3D data. One-dimensional list or array.
    y : Sequence of float
        The y-coordinates of the 3D data. One-dimensional list or array.
    z : Sequence of float
        The z-coordinates of the 3D data. One-dimensional list or array.
    minz : float
        The value of z to be taken as the xy-plane
    n: int, optional
        The number of vertical lines to get. Must be <= number of data points.
        
    Returns: list of tuple of list, list, list
        [((xa0, xa1), (ya0, ya1), (za0, za1)), ((xb0, xb1), (yb0, yb1), (zb0, zb1)), ...]
    """
    verts = []
    for xe, ye, ze in zip(divide_list(x, n), divide_list(y, n), divide_list(z, n)):
        verts.append(([xe, xe], [ye, ye], [minz, ze]))
    return verts

if __name__ == "__main__":
    fig, ax = plt.subplots(figsize=(10,10),subplot_kw={'projection': '3d'})

    eps = 0.5  # distance of xy-plane below lowest data z-value
    
    # generate data
    x1 = np.arange(0, 4, 0.02)
    y1 = x1**2
    z1 = x1 * np.sin(y1/2)
    
    x2 = np.arange(0, 4, 0.02)
    y2 = 16 - 1.5*x2**2
    z2 = x2 * np.cos(y2/4)

    minz = np.min([np.min(z1), np.min(z2)]) - eps

    ax.plot(x1, y1, z1, color='tab:red', label='$L=1$', linewidth=5)
    ax.plot(x2, y2, z2, color='tab:blue', label='$L=2$', linewidth=5)

    ax.plot(x1, y1, np.ones(z1.shape)*minz, color='tab:red', alpha=0.4, linewidth=5)
    ax.plot(x2, y2, np.ones(z2.shape)*minz, color='tab:blue', alpha=0.4, linewidth=5)

    n = 10
    v1 = get_verts(x1, y1, z1, minz, n=n)
    v2 = get_verts(x2, y2, z2, minz, n=n)

    for v_1, v_2 in zip(v1, v2):
        ax.plot(v_1[0], v_1[1], v_1[2], color='tab:red', alpha=0.6, linestyle='dashed', linewidth=2, marker='o')
        ax.plot(v_2[0], v_2[1], v_2[2], color='tab:blue', alpha=0.6, linestyle='dashed', linewidth=2, marker='o')


    ax.tick_params(labelsize=14)
    ax.set_xlabel(r'Y / Units', fontsize=18, labelpad=15)
    ax.set_ylabel(r'Y / Units', fontsize=18, labelpad=15)
    ax.set_zlabel(r'Z / Units', fontsize=18, labelpad=15)
    ax.view_init(azim=10,elev=15)
    plt.legend()
    plt.tight_layout()
    plt.show()