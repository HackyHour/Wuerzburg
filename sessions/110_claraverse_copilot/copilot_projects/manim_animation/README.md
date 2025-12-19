# Visualizing 10,000 Images with Manim

This project uses Manim (Mathematical Animation Engine) to visualize the scale of 10,000 images through a step-by-step progression.

## Visualization Steps

1. **Single Image**: Start with one image
2. **10 Images**: Show 10 images in a row
3. **100 Images**: Show 10×10 grid (100 images)
4. **1,000 Images**: Show 10×10×10 cube (1,000 images)
5. **10,000 Images**: Show 10 cubes (10,000 images)

## Files

- `visualize_10000_images.py`: Main Manim script with two scenes
  - `Visualize10000Images`: 2D scenes (steps 1-3)
  - `Visualize10000Images3D`: 3D scenes (steps 4-5)
- `images/demo_image.png`: Demo image used in the visualization
- `create_demo_image.py`: Script to create the demo image

## How to Run

### Render the 2D scenes (Steps 1-3):
```bash
manim -pql visualize_10000_images.py Visualize10000Images
```

### Render the 3D scenes (Steps 4-5):
```bash
manim -pql visualize_10000_images.py Visualize10000Images3D
```

### Render both scenes in high quality:
```bash
manim -pqh visualize_10000_images.py Visualize10000Images
manim -pqh visualize_10000_images.py Visualize10000Images3D
```

## Quality Options

- `-ql`: Low quality (fastest, 480p)
- `-qm`: Medium quality (720p)
- `-qh`: High quality (1080p)
- `-qk`: 4K quality (2160p)
- `-p`: Preview the animation when done

## Requirements

- Python 3.7+
- manim
- Pillow (PIL)

Install dependencies:
```bash
pip install manim Pillow
```
