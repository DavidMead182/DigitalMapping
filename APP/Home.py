from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog
from PyQt5 import QtCore
import sys
import minimap

class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Fire Fighter UAV")
        
        # Set custom window icon
        app_icon = QtGui.QIcon("images/floorplan.jpeg")
        self.setWindowIcon(app_icon)

        # Create a central widget and set a horizontal layout
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QHBoxLayout(central_widget)

        # Create a vertical layout for the buttons on the left
        button_layout = QtWidgets.QVBoxLayout()
        layout.addLayout(button_layout)

        # Add a button to upload an image
        self.upload_button = QPushButton('Upload Image', self)
        self.upload_button.setFixedSize(200, 50)
        self.upload_button.clicked.connect(self.upload_image)
        button_layout.addWidget(self.upload_button)

        # Add a button to open the minimap window
        self.minimap_button = QPushButton('Open Minimap', self)
        self.minimap_button.setFixedSize(200, 50)
        self.minimap_button.clicked.connect(self.open_minimap)
        button_layout.addWidget(self.minimap_button)

        # Add a spacer to push buttons to the top
        button_layout.addStretch()

        # Add a label to display the uploaded image on the right
        self.image_label = QLabel(self)
        self.image_label.setFixedSize(700, 400)
        self.image_label.setScaledContents(False)
        layout.addWidget(self.image_label)

    def upload_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp)", options=options)
        if file_name:
            pixmap = QtGui.QPixmap(file_name)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), QtCore.Qt.KeepAspectRatio))

    def open_minimap(self):
        self.minimap_window = minimap.FloorPlan(self)  # Assuming minimap.py has a class named MinimapWindow
        self.minimap_window.show()

def main():
    app = QApplication(sys.argv)
    
    # Load and apply the stylesheet
    with open("style.qss", "r") as file:
        app.setStyleSheet(file.read())
    
    ex = MyApp()
    ex.showMaximized()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
