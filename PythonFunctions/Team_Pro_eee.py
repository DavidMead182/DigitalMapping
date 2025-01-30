import cv2
import numpy as np
from PIL import Image

def floorplan_to_maze(image_path, output_path):

    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    if image is None:
        raise FileNotFoundError(f"Image at {image_path} not found.")

    # Apply GaussianBlur to smooth out details and remove furniture or small objects
    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)

    # Threshold the image to create a binary map (black and white)
    _, binary_image = cv2.threshold(blurred_image, 175, 255, cv2.THRESH_BINARY_INV)

    # Use morphological operations to remove noise and small gaps (e.g., doors)
    kernel = np.ones((3, 3), np.uint8)
    cleaned_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)

    # Normalize the values to 0 and 1 for better representation of walls and paths
    maze = (cleaned_image > 128).astype(np.uint8)
    print(np.array2string(maze, threshold=np.inf))

    # Save the processed maze as an image without resizing
    maze_image = Image.fromarray((maze * 255).astype('uint8'))  # Scale back to 0-255
    maze_image.save(output_path)

    return maze

def add_person_to_maze(maze, position, dot_size=5):
    # Copy the maze to avoid modifying the original
    updated_maze = maze.copy()

    # Extract the position coordinates
    row, col = position

    # Calculate the bounds of the dot
    row_start = max(0, row - dot_size // 2)
    row_end = min(updated_maze.shape[0], row + dot_size // 2 + 1)
    col_start = max(0, col - dot_size // 2)
    col_end = min(updated_maze.shape[1], col + dot_size // 2 + 1)

    # Place the dot in the maze
    updated_maze[row_start:row_end, col_start:col_end] = 2

    return updated_maze

# Example usage 
maze = floorplan_to_maze("floorplan.jpeg", "maze_output.jpg")
updated_maze = add_person_to_maze(maze, (25, 25))

maze_image = Image.fromarray((updated_maze * 255).astype('uint8'))  # Scale back to 0-255
maze_image.save("maze_with_dot.jpeg")
 