from PIL import Image, ImageDraw, ImageFont
import os
import tempfile
from typing import Tuple, Dict, List
import math
import platform


class VisualGenerator:
    """Generates visual elements (shapes, colors) as images for PDF embedding"""

    def __init__(self):
        self.image_cache = {}  # Cache generated images
        self.temp_dir = tempfile.mkdtemp()  # Temporary directory for images

        # Standard colors with their hex values
        self.colors = {
            "red": "#FF0000",
            "blue": "#0066FF",
            "green": "#00AA00",
            "yellow": "#FFD700",
            "purple": "#8A2BE2",
            "orange": "#FF8C00",
            "pink": "#FF69B4",
            "brown": "#8B4513",
            "crimson": "#DC143C",
            "navy": "#000080",
            "forest": "#228B22",
        }

        # Standard size
        self.shape_size = 30  # pixels
        self.image_size = 40  # pixels (with padding)

        # Animal mappings for emoji to simple drawing
        self.animal_mappings = {
            "🐱": {"name": "cat", "color": "#FFA500", "shape": "round_with_ears"},
            "🐶": {"name": "dog", "color": "#8B4513", "shape": "round_with_snout"},
            "🐮": {"name": "cow", "color": "#000000", "shape": "round_with_spots"},
            "🐷": {"name": "pig", "color": "#FFB6C1", "shape": "round_with_snout"},
            "🐑": {"name": "sheep", "color": "#F5F5F5", "shape": "fluffy_round"},
            "🦆": {"name": "duck", "color": "#FFD700", "shape": "oval_with_beak"},
        }

        # Try to get system font for emoji rendering as fallback
        self.emoji_font = self._get_emoji_font()

    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

    def _get_emoji_font(self):
        """Try to get a system font that supports emoji rendering"""
        try:
            system = platform.system()
            if system == "Darwin":  # macOS
                # Try Apple's emoji font
                font_paths = [
                    "/System/Library/Fonts/Apple Color Emoji.ttc",
                    "/Library/Fonts/Apple Color Emoji.ttc",
                ]
            elif system == "Windows":
                font_paths = [
                    "C:/Windows/Fonts/seguiemj.ttf",  # Segoe UI Emoji
                    "C:/Windows/Fonts/NotoColorEmoji.ttf",
                ]
            else:  # Linux
                font_paths = [
                    "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",
                    "/usr/share/fonts/TTF/NotoColorEmoji.ttf",
                ]

            for font_path in font_paths:
                if os.path.exists(font_path):
                    return ImageFont.truetype(font_path, size=24)

            # Fallback to default font
            return ImageFont.load_default()
        except:
            return ImageFont.load_default()

    def _create_emoji_image(self, emoji: str) -> str:
        """Create an image from an emoji character using system font"""
        cache_key = f"emoji_{emoji}"
        if cache_key in self.image_cache:
            return self.image_cache[cache_key]

        # Create image with white background
        img = Image.new(
            "RGBA", (self.image_size, self.image_size), (255, 255, 255, 255)
        )
        draw = ImageDraw.Draw(img)

        # Try to center the emoji
        try:
            # Get text bounding box for centering
            bbox = draw.textbbox((0, 0), emoji, font=self.emoji_font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            x = (self.image_size - text_width) // 2 - bbox[0]
            y = (self.image_size - text_height) // 2 - bbox[1]

            # Draw the emoji
            draw.text((x, y), emoji, font=self.emoji_font, fill=(0, 0, 0))
        except:
            # Fallback positioning
            draw.text(
                (self.image_size // 4, self.image_size // 4),
                emoji,
                font=self.emoji_font,
                fill=(0, 0, 0),
            )

        # Save to temporary file
        filename = os.path.join(self.temp_dir, f"emoji_{ord(emoji[0])}.png")
        img.save(filename, "PNG")

        self.image_cache[cache_key] = filename
        return filename

    def _create_animal_shape(self, animal_data: Dict) -> str:
        """Create a stylized animal shape based on the animal mapping"""
        animal_name = animal_data["name"]
        color = animal_data["color"]
        shape_type = animal_data["shape"]

        cache_key = f"animal_{animal_name}"
        if cache_key in self.image_cache:
            return self.image_cache[cache_key]

        # Create image
        img = Image.new("RGBA", (self.image_size, self.image_size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        # Get color
        rgb_color = self._hex_to_rgb(color)
        center_x = center_y = self.image_size // 2

        # Draw different shapes based on animal type
        if shape_type == "round_with_ears":  # Cat
            # Main head (circle)
            radius = self.shape_size // 3
            draw.ellipse(
                [
                    center_x - radius,
                    center_y - radius,
                    center_x + radius,
                    center_y + radius,
                ],
                fill=rgb_color,
                outline=(0, 0, 0),
                width=1,
            )

            # Ears (triangles)
            ear_size = radius // 2
            # Left ear
            draw.polygon(
                [
                    (center_x - radius + 3, center_y - radius),
                    (center_x - radius // 2, center_y - radius - ear_size),
                    (center_x - radius // 3, center_y - radius),
                ],
                fill=rgb_color,
                outline=(0, 0, 0),
            )
            # Right ear
            draw.polygon(
                [
                    (center_x + radius // 3, center_y - radius),
                    (center_x + radius // 2, center_y - radius - ear_size),
                    (center_x + radius - 3, center_y - radius),
                ],
                fill=rgb_color,
                outline=(0, 0, 0),
            )

        elif shape_type == "round_with_snout":  # Dog/Pig
            # Main head (circle)
            radius = self.shape_size // 3
            draw.ellipse(
                [
                    center_x - radius,
                    center_y - radius,
                    center_x + radius,
                    center_y + radius,
                ],
                fill=rgb_color,
                outline=(0, 0, 0),
                width=1,
            )

            # Snout (smaller circle)
            snout_radius = radius // 3
            draw.ellipse(
                [
                    center_x - snout_radius,
                    center_y + radius // 2,
                    center_x + snout_radius,
                    center_y + radius // 2 + snout_radius,
                ],
                fill=rgb_color,
                outline=(0, 0, 0),
                width=1,
            )

        elif shape_type == "round_with_spots":  # Cow
            # Main head (circle)
            radius = self.shape_size // 3
            draw.ellipse(
                [
                    center_x - radius,
                    center_y - radius,
                    center_x + radius,
                    center_y + radius,
                ],
                fill=(255, 255, 255),
                outline=(0, 0, 0),
                width=1,
            )

            # Black spots
            spot_size = radius // 4
            draw.ellipse(
                [
                    center_x - radius // 2,
                    center_y - radius // 2,
                    center_x - radius // 2 + spot_size,
                    center_y - radius // 2 + spot_size,
                ],
                fill=(0, 0, 0),
            )
            draw.ellipse(
                [
                    center_x + radius // 3,
                    center_y + radius // 4,
                    center_x + radius // 3 + spot_size,
                    center_y + radius // 4 + spot_size,
                ],
                fill=(0, 0, 0),
            )

        elif shape_type == "fluffy_round":  # Sheep
            # Main body (fluffy circle with multiple small circles)
            radius = self.shape_size // 3
            # Draw multiple small circles to create fluffy texture
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    small_radius = radius // 4
                    x = center_x + i * small_radius
                    y = center_y + j * small_radius
                    draw.ellipse(
                        [
                            x - small_radius,
                            y - small_radius,
                            x + small_radius,
                            y + small_radius,
                        ],
                        fill=rgb_color,
                        outline=(0, 0, 0),
                        width=1,
                    )
            # Center circle
            draw.ellipse(
                [
                    center_x - radius // 2,
                    center_y - radius // 2,
                    center_x + radius // 2,
                    center_y + radius // 2,
                ],
                fill=rgb_color,
                outline=(0, 0, 0),
                width=1,
            )

        elif shape_type == "oval_with_beak":  # Duck
            # Main body (oval)
            radius_x = self.shape_size // 3
            radius_y = self.shape_size // 4
            draw.ellipse(
                [
                    center_x - radius_x,
                    center_y - radius_y,
                    center_x + radius_x,
                    center_y + radius_y,
                ],
                fill=rgb_color,
                outline=(0, 0, 0),
                width=1,
            )

            # Beak (triangle)
            draw.polygon(
                [
                    (center_x - radius_x, center_y),
                    (center_x - radius_x - radius_x // 2, center_y - radius_y // 3),
                    (center_x - radius_x - radius_x // 2, center_y + radius_y // 3),
                ],
                fill=(255, 165, 0),
                outline=(0, 0, 0),
            )
        else:
            # Default to simple circle
            radius = self.shape_size // 3
            draw.ellipse(
                [
                    center_x - radius,
                    center_y - radius,
                    center_x + radius,
                    center_y + radius,
                ],
                fill=rgb_color,
                outline=(0, 0, 0),
                width=1,
            )

        # Save to temporary file
        filename = os.path.join(self.temp_dir, f"animal_{animal_name}.png")
        img.save(filename, "PNG")

        self.image_cache[cache_key] = filename
        return filename

    def _create_circle(self, color: str) -> str:
        """Create a colored circle image and return the file path"""
        cache_key = f"circle_{color}"
        if cache_key in self.image_cache:
            return self.image_cache[cache_key]

        # Create image with transparent background
        img = Image.new("RGBA", (self.image_size, self.image_size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        # Get color
        rgb_color = self._hex_to_rgb(self.colors.get(color, "#FF0000"))

        # Calculate circle bounds (centered with padding)
        padding = (self.image_size - self.shape_size) // 2
        x1, y1 = padding, padding
        x2, y2 = self.image_size - padding, self.image_size - padding

        # Draw filled circle with outline
        draw.ellipse([x1, y1, x2, y2], fill=rgb_color, outline=(0, 0, 0), width=2)

        # Save to temporary file
        filename = os.path.join(self.temp_dir, f"circle_{color}.png")
        img.save(filename, "PNG")

        self.image_cache[cache_key] = filename
        return filename

    def _create_square(self, color: str = None) -> str:
        """Create a square image and return the file path"""
        cache_key = f"square_{color or 'default'}"
        if cache_key in self.image_cache:
            return self.image_cache[cache_key]

        # Create image
        img = Image.new("RGBA", (self.image_size, self.image_size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        # Get color (default to gray for shapes)
        if color and color in self.colors:
            fill_color = self._hex_to_rgb(self.colors[color])
        else:
            fill_color = (100, 100, 100)  # Gray

        # Calculate square bounds
        padding = (self.image_size - self.shape_size) // 2
        x1, y1 = padding, padding
        x2, y2 = self.image_size - padding, self.image_size - padding

        # Draw filled square with outline
        draw.rectangle([x1, y1, x2, y2], fill=fill_color, outline=(0, 0, 0), width=2)

        # Save to temporary file
        filename = os.path.join(self.temp_dir, f"square_{color or 'default'}.png")
        img.save(filename, "PNG")

        self.image_cache[cache_key] = filename
        return filename

    def _create_triangle(self, color: str = None) -> str:
        """Create a triangle image and return the file path"""
        cache_key = f"triangle_{color or 'default'}"
        if cache_key in self.image_cache:
            return self.image_cache[cache_key]

        # Create image
        img = Image.new("RGBA", (self.image_size, self.image_size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        # Get color
        if color and color in self.colors:
            fill_color = self._hex_to_rgb(self.colors[color])
        else:
            fill_color = (100, 100, 100)  # Gray

        # Calculate triangle points (equilateral triangle)
        padding = (self.image_size - self.shape_size) // 2
        center_x = self.image_size // 2
        top_y = padding
        bottom_y = self.image_size - padding

        # Triangle points
        points = [
            (center_x, top_y),  # Top point
            (padding, bottom_y),  # Bottom left
            (self.image_size - padding, bottom_y),  # Bottom right
        ]

        # Draw filled triangle with outline
        draw.polygon(points, fill=fill_color, outline=(0, 0, 0))

        # Save to temporary file
        filename = os.path.join(self.temp_dir, f"triangle_{color or 'default'}.png")
        img.save(filename, "PNG")

        self.image_cache[cache_key] = filename
        return filename

    def _create_star(self, color: str = None) -> str:
        """Create a star image and return the file path"""
        cache_key = f"star_{color or 'default'}"
        if cache_key in self.image_cache:
            return self.image_cache[cache_key]

        # Create image
        img = Image.new("RGBA", (self.image_size, self.image_size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        # Get color
        if color and color in self.colors:
            fill_color = self._hex_to_rgb(self.colors[color])
        else:
            fill_color = (255, 215, 0)  # Gold

        # Calculate star points
        center_x = center_y = self.image_size // 2
        outer_radius = self.shape_size // 2
        inner_radius = outer_radius * 0.4

        points = []
        for i in range(10):  # 5 outer + 5 inner points
            angle = math.pi * i / 5 - math.pi / 2  # Start from top
            if i % 2 == 0:  # Outer points
                x = center_x + outer_radius * math.cos(angle)
                y = center_y + outer_radius * math.sin(angle)
            else:  # Inner points
                x = center_x + inner_radius * math.cos(angle)
                y = center_y + inner_radius * math.sin(angle)
            points.append((x, y))

        # Draw filled star with outline
        draw.polygon(points, fill=fill_color, outline=(0, 0, 0))

        # Save to temporary file
        filename = os.path.join(self.temp_dir, f"star_{color or 'default'}.png")
        img.save(filename, "PNG")

        self.image_cache[cache_key] = filename
        return filename

    def _create_heart(self, color: str = None) -> str:
        """Create a heart image and return the file path"""
        cache_key = f"heart_{color or 'default'}"
        if cache_key in self.image_cache:
            return self.image_cache[cache_key]

        # Create image
        img = Image.new("RGBA", (self.image_size, self.image_size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        # Get color
        if color and color in self.colors:
            fill_color = self._hex_to_rgb(self.colors[color])
        else:
            fill_color = (255, 20, 147)  # Deep pink

        # Heart shape using two circles and a triangle
        center_x = self.image_size // 2
        size = self.shape_size

        # Draw two circles for top of heart
        radius = size // 6
        circle1_center = (center_x - radius // 2, center_x - radius)
        circle2_center = (center_x + radius // 2, center_x - radius)

        # Two circles
        draw.ellipse(
            [
                circle1_center[0] - radius,
                circle1_center[1] - radius,
                circle1_center[0] + radius,
                circle1_center[1] + radius,
            ],
            fill=fill_color,
        )
        draw.ellipse(
            [
                circle2_center[0] - radius,
                circle2_center[1] - radius,
                circle2_center[0] + radius,
                circle2_center[1] + radius,
            ],
            fill=fill_color,
        )

        # Triangle for bottom of heart
        points = [
            (center_x - size // 4, center_x - radius // 2),
            (center_x + size // 4, center_x - radius // 2),
            (center_x, center_x + size // 4),
        ]
        draw.polygon(points, fill=fill_color)

        # Save to temporary file
        filename = os.path.join(self.temp_dir, f"heart_{color or 'default'}.png")
        img.save(filename, "PNG")

        self.image_cache[cache_key] = filename
        return filename

    def _create_number_image(self, number: str) -> str:
        """Create an image with a number for number patterns"""
        cache_key = f"number_{number}"
        if cache_key in self.image_cache:
            return self.image_cache[cache_key]

        # Create image with white background
        img = Image.new(
            "RGBA", (self.image_size, self.image_size), (255, 255, 255, 255)
        )
        draw = ImageDraw.Draw(img)

        # Try to get a larger font for numbers
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", size=20)
        except:
            try:
                font = ImageFont.load_default()
            except:
                font = None

        # Draw a circle background
        padding = 3
        draw.ellipse(
            [padding, padding, self.image_size - padding, self.image_size - padding],
            fill=(240, 240, 240),
            outline=(0, 0, 0),
            width=2,
        )

        # Center the number text
        if font:
            bbox = draw.textbbox((0, 0), number, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (self.image_size - text_width) // 2 - bbox[0]
            y = (self.image_size - text_height) // 2 - bbox[1]
            draw.text((x, y), number, font=font, fill=(0, 0, 0))
        else:
            # Fallback positioning
            draw.text(
                (self.image_size // 3, self.image_size // 3), number, fill=(0, 0, 0)
            )

        # Save to temporary file
        filename = os.path.join(self.temp_dir, f"number_{number}.png")
        img.save(filename, "PNG")

        self.image_cache[cache_key] = filename
        return filename

    def create_visual_element(self, element_type: str, element_data: Dict) -> str:
        """Create a visual element image based on type and data"""

        # Extract information from element data
        name = element_data.get("name", "")
        color = None

        # Check if this is a color element
        if "symbol" in element_data and element_data["symbol"] in [
            "🔴",
            "🔵",
            "🟢",
            "🟡",
            "🟣",
            "🟠",
            "🩷",
            "🤎",
        ]:
            color = name
            return self._create_circle(color)

        # Shape elements
        if name == "circle":
            return self._create_circle(color or "gray")
        elif name == "square":
            return self._create_square(color)
        elif name == "triangle":
            return self._create_triangle(color)
        elif name == "star":
            return self._create_star(color)
        elif name == "heart":
            return self._create_heart(color)
        else:
            # Default to circle
            return self._create_circle(color or "gray")

    def create_pattern_images(self, pattern_items: List[str]) -> List[str]:
        """Create a list of image paths for a pattern sequence"""
        image_paths = []

        for item in pattern_items:
            if isinstance(item, dict):
                # Item is a visual element dictionary
                image_path = self.create_visual_element("auto", item)
                image_paths.append(image_path)
            else:
                # Item is a simple string/symbol - try to create appropriate image
                # First check if it's an animal emoji
                if item in self.animal_mappings:
                    # Create stylized animal shape
                    animal_data = self.animal_mappings[item]
                    image_path = self._create_animal_shape(animal_data)
                    image_paths.append(image_path)
                # Color circles
                elif item in ["🔴", "red"]:
                    image_paths.append(self._create_circle("red"))
                elif item in ["🔵", "blue"]:
                    image_paths.append(self._create_circle("blue"))
                elif item in ["🟢", "green"]:
                    image_paths.append(self._create_circle("green"))
                elif item in ["🟡", "yellow"]:
                    image_paths.append(self._create_circle("yellow"))
                elif item in ["🟣", "purple"]:
                    image_paths.append(self._create_circle("purple"))
                elif item in ["🟠", "orange"]:
                    image_paths.append(self._create_circle("orange"))
                elif item in ["🩷", "pink"]:
                    image_paths.append(self._create_circle("pink"))
                elif item in ["🤎", "brown"]:
                    image_paths.append(self._create_circle("brown"))
                # Shapes (use symbols from patterns.json)
                elif item in ["⭕", "●", "circle"]:
                    image_paths.append(self._create_circle("gray"))
                elif item in ["⬜", "■", "square"]:
                    image_paths.append(self._create_square())
                elif item in ["🔺", "▲", "triangle"]:
                    image_paths.append(self._create_triangle())
                elif item in ["⭐", "★", "star"]:
                    image_paths.append(self._create_star())
                elif item in ["❤️", "♥", "heart"]:
                    image_paths.append(self._create_heart())
                elif item in ["💎", "♦", "diamond"]:
                    image_paths.append(
                        self._create_star("purple")
                    )  # Use star as diamond placeholder
                elif item in ["⬡", "hexagon"]:
                    image_paths.append(
                        self._create_star("green")
                    )  # Use star as hexagon placeholder
                elif item in ["🥚", "○", "oval"]:
                    image_paths.append(
                        self._create_circle("white")
                    )  # Use circle for oval
                elif item in ["🟪", "▬", "rectangle"]:
                    image_paths.append(
                        self._create_square("purple")
                    )  # Use square for rectangle
                # If it looks like an emoji (unicode character), try emoji rendering
                elif len(item) == 1 and ord(item) > 127:
                    # Try to create emoji image
                    try:
                        image_path = self._create_emoji_image(item)
                        image_paths.append(image_path)
                    except:
                        # Fallback to gray circle
                        image_paths.append(self._create_circle("gray"))
                # Number patterns
                elif item.isdigit():
                    # Create a simple number image
                    image_path = self._create_number_image(item)
                    image_paths.append(image_path)
                else:
                    # Default fallback
                    image_paths.append(self._create_circle("gray"))

        return image_paths

    def cleanup(self):
        """Clean up temporary files"""
        for filename in self.image_cache.values():
            try:
                os.remove(filename)
            except:
                pass
        try:
            os.rmdir(self.temp_dir)
        except:
            pass


# Global instance
visual_generator = VisualGenerator()
