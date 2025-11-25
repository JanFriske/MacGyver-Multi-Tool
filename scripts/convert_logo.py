from PIL import Image
from pathlib import Path
import sys

def convert_to_ico():
    try:
        base_dir = Path(__file__).parent.parent
        input_path = base_dir / "assets" / "images" / "logo.png"
        output_dir = base_dir / "assets" / "icons"
        output_path = output_dir / "icon.ico"

        # Ensure output directory exists
        output_dir.mkdir(parents=True, exist_ok=True)

        if not input_path.exists():
            print(f"Error: Input file not found at {input_path}")
            return

        img = Image.open(input_path)
        
        # Define icon sizes
        icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        
        img.save(output_path, format='ICO', sizes=icon_sizes)
        print(f"Successfully created icon at {output_path}")

    except ImportError:
        print("Error: Pillow library is not installed. Please install it with 'pip install Pillow'")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    convert_to_ico()
