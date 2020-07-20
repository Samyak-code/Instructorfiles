# Example 1
depth_image = rc.camera.get_depth_image()
depth_image = depth_image[0 : rc.camera.get_height() * 2 // 3, :]

# Example 2
depth_image = rc.camera.get_depth_image()
depth_image = (depth_image - 0.01) % rc.camera.get_max_range()

# Example 3
depth_image = rc.camera.get_depth_image()
temp = np.copy(depth_image)

for r in range(1, rc.camera.get_height() - 1):
    for c in range(1, rc.camera.get_width() - 1):
        temp[r][c] = (
            depth_image[r - 1][c - 1]
            + depth_image[r - 1][c]
            + depth_image[r - 1][c + 1]
            + depth_image[r][c - 1]
            + depth_image[r][c]
            + depth_image[r][c + 1]
            + depth_image[r + 1][c - 1]
            + depth_image[r + 1][c]
            + depth_image[r + 1][c + 1]
        ) / 9

depth_image = temp
