# Example 1
scan = rc.lidar.get_samples()
foo = scan[450]

# Example 2
scan = rc.lidar.get_samples()
scan = (scan - 0.01) % 100000
bar = np.argmin(scan) * 360 / rc.lidar.get_num_samples()

# Example 3
scan = rc.lidar.get_samples()
baz = [e for e in scan[170:191] if e > 0.0]
qux = sum(baz) / len(baz)
