image = rc.camera.get_color_image()

for r in range(0, rc.camera.get_height()):
    for c in range(0, rc.camera.get_width()):
        foo = (image[r][c][0] + image[r][c][1] + image[r][c][2]) // 3
        image[r][c][0] = foo
        image[r][c][1] = foo
        image[r][c][2] = foo

rc.display.show_color_image(image)

########################################################################################

image = rc.camera.get_color_image()

foo = 0
bar = (0, 0)

for r in range(0, rc.camera.get_height()):
    for c in range(0, rc.camera.get_width()):
        if image[r][c][0] > foo:
            foo = image[r][c][0]
            bar = (r, c)

print(bar)
