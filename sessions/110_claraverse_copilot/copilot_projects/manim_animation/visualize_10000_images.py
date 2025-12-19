from manim import *
import numpy as np

class Visualize10000Images(Scene):
    def construct(self):
        # Title
        title = Text("Visualizing 10,000 Images", font_size=48)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))
        
        # Step 1: Single image
        self.show_single_image()
        
        # Step 2: 10 images in a row
        self.show_10_images()
        
        # Step 3: 10x10 = 100 images in a grid
        self.show_100_images()
        
        # Final message
        final_text = Text("Next: Let's go 3D!", font_size=48)
        self.play(Write(final_text))
        self.wait(2)
    
    def show_single_image(self):
        """Show a single image"""
        step_title = Text("Step 1: A single image", font_size=36).to_edge(UP)
        self.play(Write(step_title))
        
        # Create a small square to represent an image
        img = ImageMobject("images/demo_image.png").scale(0.3)
        count_text = Text("1 image", font_size=24).next_to(img, DOWN, buff=0.5)
        
        self.play(FadeIn(img))
        self.play(Write(count_text))
        self.wait(2)
        self.play(FadeOut(img), FadeOut(count_text), FadeOut(step_title))
    
    def show_10_images(self):
        """Show 10 images in a row"""
        step_title = Text("Step 2: 10 images in a row", font_size=36).to_edge(UP)
        self.play(Write(step_title))
        
        images = Group()
        for i in range(10):
            img = ImageMobject("images/demo_image.png").scale(0.15)
            img.shift(RIGHT * (i - 4.5) * 0.7)
            images.add(img)
        
        count_text = Text("10 images", font_size=24, color=YELLOW).next_to(images, DOWN, buff=0.5)
        
        self.play(FadeIn(images), run_time=1.5)
        self.play(Write(count_text))
        self.wait(2)
        self.play(FadeOut(images), FadeOut(count_text), FadeOut(step_title))
    
    def show_100_images(self):
        """Show 10x10 = 100 images in a grid"""
        step_title = Text("Step 3: 10 rows × 10 columns = 100 images", font_size=32).to_edge(UP)
        self.play(Write(step_title))
        
        images = Group()
        for i in range(10):
            for j in range(10):
                img = ImageMobject("images/demo_image.png").scale(0.08)
                img.shift(RIGHT * (j - 4.5) * 0.45 + DOWN * (i - 4.5) * 0.45 + UP * 0.3)
                images.add(img)
        
        count_text = Text("10 × 10 = 100 images", font_size=24, color=YELLOW).to_edge(DOWN)
        
        self.play(FadeIn(images), run_time=2)
        self.play(Write(count_text))
        self.wait(2)
        self.play(FadeOut(images), FadeOut(count_text), FadeOut(step_title))


class Visualize10000Images3D(ThreeDScene):
    def construct(self):
        # Set up the camera
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        # Title for 3D part
        title = Text("Step 4: Adding depth - 10 layers", font_size=32)
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        self.wait(1)
        
        # Create a 3D representation of the cube (10x10x10)
        # We'll use small cubes to represent image stacks
        cubes = VGroup()
        
        # Create a more sparse representation for performance
        spacing = 0.4
        for i in range(10):
            for j in range(10):
                for k in range(10):
                    # Only show outer layer for performance
                    if i == 0 or i == 9 or j == 0 or j == 9 or k == 0 or k == 9:
                        cube = Cube(side_length=0.15, fill_opacity=0.7, fill_color=BLUE)
                        cube.shift(
                            RIGHT * (i - 4.5) * spacing +
                            UP * (j - 4.5) * spacing +
                            OUT * (k - 4.5) * spacing
                        )
                        cubes.add(cube)
        
        count_text = Text("10 × 10 × 10 = 1,000 images", font_size=28, color=YELLOW)
        count_text.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(count_text)
        
        self.play(Create(cubes), run_time=3)
        self.play(Write(count_text))
        
        # Rotate the camera to show the 3D structure
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        
        self.wait(1)
        
        # Now show 10 of these cubes
        step5_title = Text("Step 5: 10 cubes = 10,000 images!", font_size=32)
        step5_title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(step5_title)
        self.play(FadeOut(title), FadeIn(step5_title))
        
        # Scale down the first cube
        self.play(cubes.animate.scale(0.3), run_time=1)
        
        # Create 10 cubes arranged in a line
        all_cubes = VGroup()
        for i in range(10):
            cube_copy = cubes.copy()
            cube_copy.shift(RIGHT * (i - 4.5) * 1.5)
            all_cubes.add(cube_copy)
        
        self.play(
            FadeOut(cubes),
            FadeIn(all_cubes),
            run_time=2
        )
        
        final_count = Text("10 × 1,000 = 10,000 images!", font_size=32, color=GREEN)
        final_count.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(final_count)
        self.play(FadeOut(count_text), FadeIn(final_count))
        
        # Final rotation
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(5)
        self.stop_ambient_camera_rotation()
        
        # Final message
        final_message = Text("That's a LOT of images!", font_size=40, color=YELLOW)
        final_message.move_to(ORIGIN)
        self.add_fixed_in_frame_mobjects(final_message)
        self.play(
            FadeOut(all_cubes),
            FadeOut(step5_title),
            FadeOut(final_count),
            run_time=1
        )
        self.play(Write(final_message))
        self.wait(2)
