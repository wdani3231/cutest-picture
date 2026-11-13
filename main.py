from PIL import Image, ImageDraw
import os

os.makedirs("/output", exist_ok=True)
os.makedirs("output", exist_ok=True)

W, H = 1024, 1024
img = Image.new("RGB", (W, H), (255, 230, 240))
d = ImageDraw.Draw(img)

# Background
d.ellipse([50, 600, 974, 1000], fill=(255, 255, 255))
d.ellipse([100, 100, 600, 600], fill=(255, 245, 250))

# Kitten face
d.ellipse([150, 150, 650, 650], fill=(255, 255, 255), outline=(255, 200, 220), width=5)
d.polygon([(200, 200), (280, 60), (350, 220)], fill=(255, 255, 255), outline=(255, 180, 200))
d.polygon([(500, 200), (560, 60), (620, 220)], fill=(255, 255, 255), outline=(255, 180, 200))
# Eyes - big blue
d.ellipse([280, 380, 380, 480], fill=(30, 100, 200))
d.ellipse([310, 400, 350, 440], fill=(255, 255, 255))
d.ellipse([480, 380, 580, 480], fill=(30, 100, 200))
d.ellipse([510, 400, 550, 440], fill=(255, 255, 255))
# Nose + mouth
d.polygon([(410, 520), (450, 520), (430, 550)], fill=(255, 150, 180))
d.arc([380, 550, 430, 600], 0, 180, fill=(200, 100, 130), width=4)
d.arc([430, 550, 480, 600], 0, 180, fill=(200, 100, 130), width=4)

# Pink sweater
d.rectangle([180, 620, 620, 850], fill=(255, 180, 210))

# Chick
d.ellipse([600, 500, 900, 800], fill=(255, 230, 120))
d.ellipse([650, 550, 700, 600], fill=(0, 0, 0))
d.ellipse([800, 550, 850, 600], fill=(0, 0, 0))
d.polygon([(730, 620), (770, 620), (750, 660)], fill=(255, 150, 50))

# Hug arms
d.ellipse([550, 650, 700, 750], fill=(255, 255, 255), outline=(255, 200, 220))

img.save("/output/cutest.png")
img.save("output/cutest.png")
img.save("cutest.png")
print("Done: cutest.png created")
