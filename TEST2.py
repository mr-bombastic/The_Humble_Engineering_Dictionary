# Improting Image class from PIL module 
from PIL import Image

# Opens a image in RGB mode 
im = Image.open("Dictionary/all_latex_images/Pa.png")

# Size of the image in pixels (size of orginal image) 
# (This is not mandatory) 
width, height = im.size

crop_top = 0
crop_bot = 0
crop_left = 0
crop_right = 0

for w in range(0, width):
    for h in range(0, height):
        if im.getpixel((w, h)) != (255, 255, 255, 0):
            crop_left = w
            break
    else:
        continue
    break

for w in range(width-1, 0, -1):
    for h in range(height-1, 0, -1):
        if im.getpixel((w, h)) != (255, 255, 255, 0):
            crop_right = w+1
            break
    else:
        continue
    break

for h in range(0, height):
    for w in range(0, width):
        if im.getpixel((w, h)) != (255, 255, 255, 0):
            crop_top = h
            break
    else:
        continue
    break

for h in range(height-1, 0, -1):
    for w in range(width - 1, 0, -1):
        if im.getpixel((w, h)) != (255, 255, 255, 0):
            crop_bot = h+1
            break
    else:
        continue
    break


# Cropped image of above dimension 
# (It will not change orginal image) 
im1 = im.crop((crop_left, crop_top, crop_right, crop_bot))

im1.save("Dictionary/all_latex_images/Pa.png")
