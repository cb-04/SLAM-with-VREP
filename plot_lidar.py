from zmqRemoteApi import RemoteAPIClient
import numpy as np
import matplotlib.pyplot as plt

# Connect to CoppeliaSim
client = RemoteAPIClient('127.0.0.1', 23000)
sim = client.getObject('sim')

# Call Lua function
success, points = sim.callScriptFunction(
    'getLaserPointsForPython@Pioneer_p3dx', 
    sim.scripttype_childscript, 
    []
)

if success and points and len(points) > 0:
    points = np.array(points).reshape(-1, 3)
    x = points[:, 0]
    y = points[:, 1]

    plt.figure(figsize=(8, 8))
    plt.scatter(x, y, s=2, c='red')
    plt.title("🔥 LIDAR Scan from fastHokuyo (Pioneer)")
    plt.axis('equal')
    plt.grid(True)
    plt.show()

else:
    print("💥 Failed to get laser data or no points returned.")
