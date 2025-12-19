from PIL import Image, ImageDraw, ImageFont

# Create a simple demo image
img = Image.new('RGB', (100, 100), color=(70, 130, 180))
draw = ImageDraw.Draw(img)

# Draw a simple pattern
draw.rectangle([10, 10, 90, 90], outline=(255, 255, 255), width=3)
draw.text((30, 40), "IMG", fill=(255, 255, 255))

# Save the image
img.save('images/demo_image.png')
print("Demo image created successfully!")
