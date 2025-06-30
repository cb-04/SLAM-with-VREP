from zmqRemoteApi import RemoteAPIClient
import numpy as np
import matplotlib.pyplot as plt

client = RemoteAPIClient('127.0.0.1', 23000)
sim = client.getObject('sim')

# MANUALLY specify script type as integer
script_type = 1  # sim.scripttype_childscript

# Call Lua function
success, points = sim.callScriptFunction(
    'getLaserPointsForPython@Pioneer_p3dx', 
    1,  # child script type
    []
)

if success and points:
    points = np.array(points).reshape(-1, 3)
    plt.scatter(points[:, 0], points[:, 1], s=2, c='red')
    plt.title("LIDAR Scan from fastHokuyo")
    plt.axis('equal')
    plt.grid(True)
    plt.show()
else:
    print("Failed to get laser data or no points returned.")
