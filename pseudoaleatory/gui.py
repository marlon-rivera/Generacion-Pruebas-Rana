from PyQt6.QtCore import Qt
import taller_sc as pse
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QComboBox, QHBoxLayout, QLineEdit
from PyQt6.QtGui import QCloseEvent, QCursor, QFont
from PyQt6.QtCore import QSize
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from WindowGeneration import WindowGeneration
from Frog import WindowFrog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Taller Pseudoaleatorios")
        self.showMaximized()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title = QLabel("SIMULACIÓN PSEUDOALEATORIA")
        self.font = QFont()
        self.font.setPointSize(24)
        self.font.setBold(True)
        self.title.setStyleSheet("""color:white;""")
        self.title.setFont(self.font)
        layout.addWidget(self.title)

        self.generationButton = QPushButton("Generador de numeros")
        self.generationButton.clicked.connect(self.showGenerationWindow)
        self.generationButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        layout.addWidget(self.generationButton)

        self.frogProblemButton = QPushButton("Problema de la rana")
        self.frogProblemButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.frogProblemButton.clicked.connect(self.showFrogWindow)
        layout.addWidget(self.frogProblemButton)

    def showGenerationWindow(self):
        self.setDisabled(True)
        self.hide()
        self.generationWindow = WindowGeneration(self)
        self.generationWindow.destroyed.connect(self.showMainWindow)

    def showFrogWindow(self):
        self.setDisabled(True)
        self.hide()
        self.frogWindow = WindowFrog(self)
        self.frogWindow.destroyed.connect(self.showMainWindow)

    def showMainWindow(self):
        self.show()
        self.setDisabled(False)   
        


   
stylesheet = """
    MainWindow {
        border-image: url('./images/background.jpg') 0 0 0 0 stretch stretch;
    }
    MainWindow QPushButton {
        color: white;
        font-size: 30px;
        line-height: 36px;
        border-radius: 15px;
        background-color: #6CC700;
        padding: 4px;
    }
"""      

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    
if __name__ == "__main__":
    main()