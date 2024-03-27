from PyQt6.QtCore import Qt
import taller_sc as pse
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QComboBox, QHBoxLayout, QLineEdit
from PyQt6.QtGui import QCloseEvent, QCursor, QFont
from PyQt6.QtCore import QSize
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

intervals = [
    {"lower": 0.0, "upper": 0.1},
    {"lower": 0.1, "upper": 0.2},
    {"lower": 0.2, "upper": 0.3},
    {"lower": 0.3, "upper": 0.4},
    {"lower": 0.4, "upper": 0.5},
    {"lower": 0.5, "upper": 0.6},
    {"lower": 0.6, "upper": 0.7},
    {"lower": 0.7, "upper": 0.8},
    {"lower": 0.8, "upper": 0.9},
    {"lower": 0.9, "upper": 1.0}
]

class WindowFrog(QMainWindow):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Problema de la rana")
        self.stylesheet = """
            WindowFrog{
                border-image: url('./images/pond.png') 0 0 0 0 stretch stretch;
            }
            
        """
        self.showMaximized()
        self.setStyleSheet(self.stylesheet)
        
        self.oneDimensionButton = QPushButton("Una dimension - 1D")
        self.oneDimensionButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.oneDimensionButton.clicked.connect(self.show1D)
        
        self.twoDimensionButton = QPushButton("Dos dimensiones - 2D")
        self.twoDimensionButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.twoDimensionButton.clicked.connect(self.show2D)

        self.threeDimensionButton = QPushButton("Tres dimensiones - 3D")
        self.threeDimensionButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.threeDimensionButton.clicked.connect(self.show3D)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.mainLayout = QVBoxLayout(central_widget)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.oneDimensionButton)
        self.mainLayout.addWidget(self.twoDimensionButton)
        self.mainLayout.addWidget(self.threeDimensionButton)   
    
    def show1D(self):
        self.hide()
        self.setDisabled(True)
        self.oneD = oneD(self)
        self.oneD.destroyed.connect(self.showFrogWindow)
        self.oneD.show()
            
    def show2D(self):
        print()
    
    def show3D(self):
        print()
        
    def showFrogWindow(self):
        self.setDisabled(False)
        self.show()
    
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.parent.showMainWindow()
        
from collections import Counter
class oneD(QMainWindow):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("1D")
        self.stylesheet = """
            OneD{
                border-image: url('./images/pond.png') 0 0 0 0 stretch stretch;
            }
        """
        self.setStyleSheet(self.stylesheet)
        self.labelJumps = QLabel("Saltos: ")
        self.font = QFont()
        self.font.setPointSize(18)
        self.font.setBold(True)
        self.labelJumps.setStyleSheet("""color:#6CC700;""")
        self.labelJumps.setFont(self.font)
        
        self.inputJumps = QLineEdit(self)
        self.inputJumps.textChanged.connect(self.validateDigit)
        self.inputJumps.setFixedSize(250,30)
        
        self.simulateJumps = QPushButton("A saltar!")
        self.simulateJumps.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.simulateJumps.clicked.connect(self.showChartJumps)
        
        central_widget = QWidget()
        
        self.setCentralWidget(central_widget)
        self.mainLayout = QVBoxLayout(central_widget)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.labelJumps)
        self.mainLayout.addWidget(self.inputJumps)
        self.mainLayout.addWidget(self.simulateJumps)
    
    def showChartJumps(self):
        resultJumps = pse.simulateJumps1D(int(self.inputJumps.text()))
        x = [i for i in range(0, len(resultJumps))]
        self.windowChart = QMainWindow()
        
        self.windowChart.setGeometry(50,50, 500, 300)
        self.windowChart.setWindowTitle("Grafica")
        canvas = FigureCanvas(plt.Figure(figsize=(20, 8)))
        self.windowChart.setCentralWidget(canvas)
        
        ax = canvas.figure.add_subplot()
        ax.axvline(resultJumps[-1], color='r', linestyle='--')
        ax.text(resultJumps[-1], x[-1], f'({resultJumps[-1]}, {x[-1]})', fontsize=10, verticalalignment='bottom', horizontalalignment='right')


        ax.plot(resultJumps, x)
        
        ax.set_xlabel("Posicion")
        ax.set_ylabel("# Saltos")
        ax.set_title("Cantidad de saltos 1D")
        canvas.figure.savefig('grafica_pasos.png')
        self.showChatFrequencies(resultJumps)
    
    
    def showChatFrequencies(self, resultJumps):
        frequencies = Counter(resultJumps)

# Ordenar las claves del contador
        sorted_keys = sorted(frequencies.keys())

        # Graficar
        canvas = FigureCanvas(plt.Figure(figsize=(20, 8)))
        ax = canvas.figure.add_subplot()
        ax.bar(sorted_keys, [frequencies[key] for key in sorted_keys])

        # Configuración de los ejes y título
        ax.set_xlabel("Posicion")
        ax.set_ylabel("# Frecuencia")
        ax.set_title("Frecuencia de saltos 1D")

        # Guardar la gráfica
        canvas.figure.savefig('grafica_frecuencias.png')
    
    def validateDigit(self):
        text = self.inputJumps.text()
        if text.isdigit() and int(text) > 0:
            pass
        else:
            self.inputJumps.setText(text[:-1])
            
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.parent.showFrogWindow()
    