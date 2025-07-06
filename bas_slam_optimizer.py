import zmq
import json
import numpy as np
import matplotlib.pyplot as plt

# === BAS function ===
def beetle_antennae_search(f, x0, num_iter=20, d=0.1, alpha=0.95):
    x = x0.copy()
    for i in range(num_iter):
        dir = np.random.randn(*x.shape)
        dir /= np.linalg.norm(dir)
        x_left = x + d * dir
        x_right = x - d * dir

        f_left = f(x_left)
        f_right = f(x_right)

        if f_left < f_right:
            x = x - d * dir * alpha
        else:
            x = x + d * dir * alpha

        d *= alpha
        print(f"Iter {i}, Error: {f(x):.4f}")
    return x

# === Error function example ===
def slam_error(x, poses, scans):
    corrected_poses = poses + x.reshape((-1, 3))
    error = np.sum(np.linalg.norm(corrected_poses[:, :2] - poses[:, :2], axis=1)**2)
    return error

# === ZeroMQ subscriber setup ===
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")
socket.setsockopt_string(zmq.SUBSCRIBE, "")

poses = []
scans = []

print("Listening for data from CoppeliaSim...")

try:
    while True:
        msg = socket.recv_string()
        data = json.loads(msg)

        pose = np.array(data['pose'])
        scan = data['scan']

        poses.append(pose)
        scans.append(scan)

        if len(poses) >= 20:  # Arbitrary buffer length to start optimization
            poses_np = np.array(poses)
            x0 = np.zeros(poses_np.shape).flatten()

            print("Starting BAS optimization...")
            x_opt = beetle_antennae_search(lambda x: slam_error(x, poses_np, scans), x0)

            corrected_poses = poses_np + x_opt.reshape((-1, 3))

            # Plot
            plt.figure()
            for p, s in zip(corrected_poses, scans):
                scan_arr = np.array(s).reshape(-1, 3)[:, :2]
                theta = p[2]
                R = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
                transformed = (R @ scan_arr.T).T + p[:2]
                plt.plot(transformed[:, 0], transformed[:, 1], 'r.', markersize=1)
            plt.title("Map after BAS optimization")
            plt.axis("equal")
            plt.grid(True)
            plt.show()

            # Reset buffer
            poses = []
            scans = []

except KeyboardInterrupt:
    print("Stopping optimization.")
finally:
    socket.close()
    context.term()
