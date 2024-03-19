from PIL import Image
import os

input_image_name = input("Enter the input image name: ")

if not os.path.isfile(input_image_name):
    print("No such file")
    exit()

if not input_image_name.lower().endswith('.bmp'):
    print("Input image must be in BMP format")
    exit()

img = Image.open(input_image_name)
img = img.convert("RGB")

width, height = img.size

pixels = img.load()

# Masks initialization
masks = [[[1, 2, 1], [0, 0, 0], [-1, -2, -1]], [[2, 1, 0], [1, 0, -1], [0, -1, -2]],
         [[1, 0, -1], [2, 0, -2], [1, 0, -1]], [[0, -1, -2], [1, 0, -1], [2, 1, 0]],
         [[-1, -2, -1], [0, 0, 0], [1, 2, 1]], [[-2, -1, 0], [-1, 0, 1], [0, 1, 2]],
         [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], [[0, 1, 2], [-1, 0, 1], [-2, -1, 0]]]

# Splitting into 3 channels
r, g, b = Image.Image.split(img)

zero_pixels = [0] * (height * width)

# Creating copies to store original values
# Creating arrays filled with zeros to store processed values
r_copy = r.copy()
r.putdata(zero_pixels)
g_copy = g.copy()
g.putdata(zero_pixels)
b_copy = b.copy()
b.putdata(zero_pixels)

print("Processing...")

for i in range(1, width - 1):
    for j in range(1, height - 1):
        for mask_number in range(len(masks)):
            # Resetting temporary values after each mask
            r_value, g_value, b_value = 0, 0, 0

            # Convolution operation for each channel
            for a in range(-1, 2):
                for c in range(-1, 2):
                    r_value += r_copy.getpixel((i + a, j + c)) * masks[mask_number][a + 1][c + 1]
                    g_value += g_copy.getpixel((i + a, j + c)) * masks[mask_number][a + 1][c + 1]
                    b_value += b_copy.getpixel((i + a, j + c)) * masks[mask_number][a + 1][c + 1]

            # Assigning convolved values to the output image
            # The value must be in the range of 0 to 255, and if it is greater than the previous one, it overrides it
            r.putpixel((i, j), max(r.getpixel((i, j)), min(255, r_value)))
            g.putpixel((i, j), max(g.getpixel((i, j)), min(255, g_value)))
            b.putpixel((i, j), max(b.getpixel((i, j)), min(255, b_value)))

pixels = Image.merge('RGB', (r, g, b))

output_image_name = input("Enter the output image name: ")

pixels.save(output_image_name)
img.close()

print("Done")
