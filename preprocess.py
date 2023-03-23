from PIL import Image, ImageOps, ImageFilter
import pytesseract

image_file = "images/pc_raw.png"
img = Image.open(image_file)

def get_region(image):
    width, height = image.size
    
    # Ignores Title Bar for region calculation
    title_height = 30

    print(width, height)
    
    left = width * 0.307
    right = width * 0.74
    top = height * 0.1852
    bottom = height * 0.23148

    print(left, top + title_height, right, bottom)
    middle_height = height // 2
    top_margin = middle_height - 85 # Adjust this value to move the top of the region up or down
    bottom_margin = middle_height # Adjust this value to move the bottom of the region up or down
    return (left, top + title_height, right, bottom + title_height)

# 960,540
# 295, 

region = get_region(img)
img = img.crop(region)

img.save("images/cropped_raw.png")

# Binarization
def grayscale(image):
    return ImageOps.grayscale(image)

gray_image = grayscale(img)
gray_image.save("images/gray.png")

im_bw = gray_image.point(lambda x: 0 if x < 210 else 255)
im_bw.save("images/binarized.png")

# Noise Removal
def noise_removal(image):
    kernel = Image.new("1", (1, 1), 1)
    image = image.filter(ImageFilter.MaxFilter(size=3))
    image = image.filter(ImageFilter.MinFilter(size=3))
    image = image.filter(ImageFilter.MedianFilter(size=3))
    return image

no_noise = noise_removal(im_bw)
no_noise.save("images/no_noise.png")

# Dilation and Erosion
def thin_font(image):
    kernel = Image.new("1", (1, 1), 1)
    image = ImageOps.invert(image)
    image = image.filter(ImageFilter.MinFilter(size=3))
    image = ImageOps.invert(image)
    return image

eroded_image = thin_font(no_noise)
eroded_image.save("images/eroded_image.png")

def thick_font(image):
    kernel = Image.new("1", (2, 2), 1)
    image = ImageOps.invert(image)
    image = image.filter(ImageFilter.MaxFilter(size=3))
    image = ImageOps.invert(image)
    return image

dilated_image = thick_font(no_noise)
dilated_image.save("images/dilated_image.png")