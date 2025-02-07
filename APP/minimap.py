from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsEllipseItem
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import Qt
from functions.imageToArray import *

# Constants
TILE_SIZE = 1  # Size of each tile
PLAYER_SIZE = 10  # Size of red dot
TRAIL_SIZE = 10  # Number of steps to keep the trail

# Sample floor plan (1 = wall, 0 = open space)
FLOOR_PLAN = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

class FloorPlan(QGraphicsView):
    def __init__(self, floor_plan):
        super().__init__()

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        floor_plan = floorplan_to_maze("./images/floorplan.jpeg", scale_factor=0.5, blur_effect=40)
        self.setFixedSize(len(floor_plan[0]) * TILE_SIZE, len(floor_plan) * TILE_SIZE)

        self.walls = []
        self.players = []
        self.trail = []

        # Draw the floor plan
        self.load_floor_plan(floor_plan)

        # Focus to capture key events
        self.setFocus()

    def load_floor_plan(self, floor_plan):
        for row in range(len(floor_plan)):
            for col in range(len(floor_plan[row])):
                x, y = col * TILE_SIZE, row * TILE_SIZE
                if floor_plan[row][col] == 1:
                    wall = QGraphicsRectItem(x, y, TILE_SIZE, TILE_SIZE)
                    wall.setBrush(QBrush(Qt.black))
                    self.scene.addItem(wall)
                    self.walls.append(wall)
                else:
                    # Add a red dot at first empty space (you can change this to add more)
                    if not self.players:
                        self.add_red_dot(x + TILE_SIZE // 4, y + TILE_SIZE // 4)

    def add_red_dot(self, x, y):
        player = QGraphicsEllipseItem(x, y, PLAYER_SIZE, PLAYER_SIZE)
        player.setBrush(QBrush(Qt.red))
        self.scene.addItem(player)
        self.players.append(player)

    def keyPressEvent(self, event):
        if not self.players:
            return

        player = self.players[0]  # Single player for now
        dx, dy = 0, 0

        if event.key() == Qt.Key_Left:
            dx = -PLAYER_SIZE
        elif event.key() == Qt.Key_Right:
            dx = PLAYER_SIZE
        elif event.key() == Qt.Key_Up:
            dy = -PLAYER_SIZE
        elif event.key() == Qt.Key_Down:
            dy = PLAYER_SIZE
        else:
            return  # Ignore other keys

        # Compute new position
        new_x = player.x() + dx
        new_y = player.y() + dy

        # Collision check
        player_rect = player.sceneBoundingRect().translated(dx, dy)
        if not any(wall.sceneBoundingRect().intersects(player_rect) for wall in self.walls):
            # Add current position to trail
            trail_dot = QGraphicsEllipseItem(player.x(), player.y(), PLAYER_SIZE, PLAYER_SIZE)
            trail_dot.setBrush(QBrush(Qt.blue))
            self.scene.addItem(trail_dot)
            self.trail.append(trail_dot)

            # Remove old trail if it exceeds the limit
            if len(self.trail) > TRAIL_SIZE:
                old_trail_dot = self.trail.pop(0)
                self.scene.removeItem(old_trail_dot)

            # Move player
            player.setX(new_x)
            player.setY(new_y)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = FloorPlan(FLOOR_PLAN)
    window.show()
    sys.exit(app.exec_())
