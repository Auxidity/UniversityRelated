from ascii_magic import AsciiArt
"""from PIL import Image, ImageOps

image = Image.open('althalus.jpg')
image = ImageOps.grayscale(image)
image = ImageOps.autocontrast(image)
image = ImageOps.invert(image)

image.save('althalus_preprocessed.jpg')
"""

my_art = AsciiArt.from_image('althalus.jpg')
my_art.to_terminal()

