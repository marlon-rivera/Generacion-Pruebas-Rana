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


class WindowGeneration(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Generacion de numeros")
        self.stylesheet = """
            WindowGeneration{
                border-image: url('./images/background1.jpg') 0 0 0 0 stretch stretch;
            }
        """
        self.showMaximized()
        self.setStyleSheet(self.stylesheet)
        self.meanSquaresButton = QPushButton("Medios cuadrados")
        self.meanSquaresButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.meanSquaresButton.clicked.connect(self.createMeanSquares)
        
        self.congruentialLinearButton = QPushButton("Congruencia Lineal")
        self.congruentialLinearButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.congruentialLinearButton.clicked.connect(self.createLinearCongruential)

        self.congruentialMultiplicative = QPushButton("Congruencia Multiplicativa")
        self.congruentialMultiplicative.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.congruentialMultiplicative.clicked.connect(self.createMultiplicativeCongruential)

        self.uniformButton = QPushButton("Distribucion uniforme")
        self.uniformButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.uniformButton.clicked.connect(self.createDistributionUniform)
        
        self.normalButton = QPushButton("Distribucion normal")
        self.normalButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.normalButton.clicked.connect(self.createDistributionNormal)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.mainLayout = QVBoxLayout(central_widget)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.meanSquaresButton)
        self.mainLayout.addWidget(self.congruentialLinearButton)
        self.mainLayout.addWidget(self.congruentialMultiplicative)
        self.mainLayout.addWidget(self.uniformButton)
        self.mainLayout.addWidget(self.normalButton)        
        
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.parent.showMainWindow()
    
    def createMeanSquares(self):
        self.hide()
        self.setDisabled(True)
        self.meanSquare = MeanSquareGeneration(self)
        self.meanSquare.destroyed.connect(self.showGenerationWindow)
        self.meanSquare.show()
    
    def createLinearCongruential(self):
        self.hide()
        self.setDisabled(True)
        self.linearCongruential = LinearCongruentialGeneration(self)
        self.linearCongruential.destroyed.connect(self.showGenerationWindow)
        self.linearCongruential.show()
        
    def createMultiplicativeCongruential(self):
        self.hide()
        self.setDisabled(True)
        self.multiplicativeCongruential = MultiplicativeCongruentialGeneration(self)
        self.multiplicativeCongruential.destroyed.connect(self.showGenerationWindow)
        self.multiplicativeCongruential.show()
    
    def createDistributionUniform(self):
        self.hide()
        self.setDisabled(True)
        self.distributionUniform = UniformGeneration(self)
        self.distributionUniform.destroyed.connect(self.showGenerationWindow)
        self.distributionUniform.show()
        
    def createDistributionNormal(self):
        self.hide()
        self.setDisabled(True)
        self.normalGeneration = NormalGeneration(self)
        self.normalGeneration.destroyed.connect(self.showGenerationWindow)
        self.normalGeneration.show()
    
    def showGenerationWindow(self):
        self.setDisabled(False)
        self.show()

class MeanSquareGeneration(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Cuadrados medios")
        self.stylesheet = """
            MeanSquareGeneration{
                border-image: url('./images/background1.jpg') 0 0 0 0 stretch stretch;
            }
        """
        self.setStyleSheet(self.stylesheet)
        self.showMaximized()
        
        self.labelSeed = QLabel("Semilla: ")
        self.font = QFont()
        self.font.setPointSize(18)
        self.font.setBold(True)
        self.labelSeed.setStyleSheet("""color:white;""")
        self.labelSeed.setFont(self.font)
        
        self.inputSeed = QLineEdit(self)
        self.inputSeed.setFixedSize(250,30)
        
        self.labelMin = QLabel("Min: ")
        self.font = QFont()
        self.font.setPointSize(18)
        self.font.setBold(True)
        self.labelMin.setStyleSheet("""color:white;""")
        self.labelMin.setFont(self.font)
        
        self.inputMin = QLineEdit(self)
        self.inputMin.setFixedSize(250,30)
        
        self.labelMax = QLabel("Max: ")
        self.font = QFont()
        self.font.setPointSize(18)
        self.font.setBold(True)
        self.labelMax.setStyleSheet("""color:white;""")
        self.labelMax.setFont(self.font)
        
        self.inputMax = QLineEdit(self)
        self.inputMax.setFixedSize(250,30)
        
        self.quantityLabel = QLabel("Cantidad: ")
        self.font = QFont()
        self.font.setPointSize(18)
        self.font.setBold(True)
        self.quantityLabel.setStyleSheet("""color:white;""")
        self.quantityLabel.setFont(self.font)
        
        self.inputSeed = QLineEdit(self)
        self.inputSeed.setFixedSize(250,30)
        self.inputSeed.textChanged.connect(self.validateDigit)
        
        self.inputQuantity = QLineEdit(self)
        self.inputQuantity.setFixedSize(250,30)
        self.inputQuantity.textChanged.connect(self.validateDigit)
        
        self.buttonGenerateMeanSquares = QPushButton("Generar")
        self.buttonGenerateMeanSquares.clicked.connect(self.generateNumbers)
        self.buttonGenerateMeanSquares.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        central_widget = QWidget()
        
        self.setCentralWidget(central_widget)
        self.mainLayout = QVBoxLayout(central_widget)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.labelSeed)
        self.mainLayout.addWidget(self.inputSeed)
        self.mainLayout.addWidget(self.labelMin)
        self.mainLayout.addWidget(self.inputMin)
        self.mainLayout.addWidget(self.labelMax)
        self.mainLayout.addWidget(self.inputMax)
        self.mainLayout.addWidget(self.quantityLabel)
        self.mainLayout.addWidget(self.inputQuantity)
        self.mainLayout.addWidget(self.buttonGenerateMeanSquares)
    
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.parent.showGenerationWindow()
    
    def generateNumbers(self):
        ri, xi, extractionArr, extensionArr, xsquareArr, ni = pse.generateNumbersByMeanSquares(int(self.inputSeed.text()), int(self.inputMin.text()), int(self.inputMax.text()), int(self.inputQuantity.text()))
        
        self.windowTable = QMainWindow()
        
        self.windowTable.setGeometry(50,50, 500, 300)
        self.windowTable.setWindowTitle("Resultado")
    
        table = QTableWidget()
        table.setRowCount(len(ri))
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(["Xi", "Xi^2", "Extension", "Extraction", "Ri", "Ni"])

        for row, values in enumerate(zip( xi, xsquareArr, extensionArr, extractionArr, ri, ni)):
            for col, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                table.setItem(row, col, item)
            
        self.windowTable.setCentralWidget(table)
        
        buttonBack = QPushButton("Regresar", self.windowTable)
        buttonBack.setStyleSheet("""color: white;
        font-size: 30px;
        line-height: 36px;
        border-radius: 15px;
        background-color: #6CC700;
        padding: 4px;""")
        buttonBack.setGeometry(950, 700, 350, 50)
        buttonBack.clicked.connect(self.hideWindowTable)
        buttonBack.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        buttonShowChart = QPushButton("Mostrar grafica", self.windowTable)
        buttonShowChart.setStyleSheet("""color: white;
        font-size: 30px;
        line-height: 36px;
        border-radius: 15px;
        background-color: #6CC700;
        padding: 4px;""")
        buttonShowChart.setGeometry(600, 700, 350, 50)
        buttonShowChart.clicked.connect(lambda x: self.showChart(ri))
        buttonShowChart.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.windowTable.show()

    def classify_data(self, data):
        counts = [0] * len(intervals)
        for value in data:
            for i, interval in enumerate(intervals):
                if interval["lower"] <= value < interval["upper"]:
                    counts[i] += 1
                    break

        return counts

    def showChart(self, ri):
        counts = self.classify_data(ri)
        
        self.windowChart = QMainWindow()
        
        self.windowChart.setGeometry(50,50, 500, 300)
        self.windowChart.setWindowTitle("Grafica")
        canvas = FigureCanvas(plt.Figure(figsize=(6, 4)))
        self.windowChart.setCentralWidget(canvas)
        
        ax = canvas.figure.add_subplot(111)
        ax.bar(range(len(intervals)), counts, tick_label=[f"[{interval['lower']}, {interval['upper']})" for interval in intervals])
        ax.set_xlabel("Intervalos")
        ax.set_ylabel("Frecuencia")
        ax.set_title("Gráfico de Barras")
        
        canvas.draw()
        self.windowChart.show()

        
    def hideWindowTable(self, event):
        self.windowTable.hide()

    def validateDigit(self):
        text = self.inputSeed.text()
        if text.isdigit() and int(text) > 0:
            pass
        else:
            self.inputSeed.setText(text[:-1])

class LinearCongruentialGeneration(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Congruencia Lineal")
        self.stylesheet = """
            LinearCongruentialGeneration{
                border-image: url('./images/background1.jpg') 0 0 0 0 stretch stretch;
            }
        """
        self.setStyleSheet(self.stylesheet)
        self.showMaximized()
        #Xo, k, c, g, quantity
        self.labelSeed = QLabel("Semilla: ")
        self.font = QFont()
        self.font.setPointSize(18)
        self.font.setBold(True)
        self.labelSeed.setStyleSheet("""color:white;""")
        self.labelSeed.setFont(self.font)
        
        self.inputSeed = QLineEdit(self)
        self.inputSeed.setFixedSize(250,30)
        self.inputSeed.textChanged.connect(self.validateDigit)
        
        self.labelK = QLabel("K: ")
        self.font = QFont()
        self.font.setPointSize(18)
        self.font.setBold(True)
        self.labelK.setStyleSheet("""color:white;""")
        self.labelK.setFont(self.font)
        
        self.inputK = QLineEdit(self)
        self.inputK.setFixedSize(250,30)
        self.inputK.textChanged.connect(self.validateDigit)
        
        self.labelC = QLabel("C: ")
        self.font = QFont()
        self.font.setPointSize(18)
        self.font.setBold(True)
        self.labelC.setStyleSheet("""color:white;""")
        self.labelC.setFont(self.font)
        
        self.inputC = QLineEdit(self)
        self.inputC.setFixedSize(250,30)
        self.inputC.textChanged.connect(self.validateDigit)
        
        self.labelG = QLabel("g: ")
        self.font = QFont()
        self.font.setPointSize(18)
        self.font.setBold(True)
        self.labelG.setStyleSheet("""color:white;""")
        self.labelG.setFont(self.font)
        
        self.inputG = QLineEdit(self)
        self.inputG.setFixedSize(250,30)
        self.inputG.textChanged.connect(self.validateDigit)
        
        self.labelMin = QLabel("Min: ")
        self.font = QFont()
        self.font.setPointSize(18)
        self.font.setBold(True)
        self.labelMin.setStyleSheet("""color:white;""")
        self.labelMin.setFont(self.font)
        
        self.inputMin = QLineEdit(self)
        self.inputMin.setFixedSize(250,30)
        
        self.labelMax = QLabel("Max: ")
        self.font = QFont()
        self.font.setPointSize(18)
        self.font.setBold(True)
        self.labelMax.setStyleSheet("""color:white;""")
        self.labelMax.setFont(self.font)
        
        self.inputMax = QLineEdit(self)
        self.inputMax.setFixedSize(250,30)
        
        self.quantityLabel = QLabel("Cantidad: ")
        self.font = QFont()
        self.font.setPointSize(18)
        self.font.setBold(True)
        self.quantityLabel.setStyleSheet("""color:white;""")
        self.quantityLabel.setFont(self.font)
        
        self.inputQuantity = QLineEdit(self)
        self.inputQuantity.setFixedSize(250,30)
        self.inputQuantity.textChanged.connect(self.validateDigit)
        
        self.buttonGenerateMeanSquares = QPushButton("Generar")
        self.buttonGenerateMeanSquares.clicked.connect(self.generateNumbers)
        self.buttonGenerateMeanSquares.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        central_widget = QWidget()
        
        self.setCentralWidget(central_widget)
        self.mainLayout = QVBoxLayout(central_widget)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.labelSeed)
        self.mainLayout.addWidget(self.inputSeed)
        self.mainLayout.addWidget(self.labelK)
        self.mainLayout.addWidget(self.inputK)
        self.mainLayout.addWidget(self.labelC)
        self.mainLayout.addWidget(self.inputC)
        self.mainLayout.addWidget(self.labelG)
        self.mainLayout.addWidget(self.inputG)
        self.mainLayout.addWidget(self.labelMin)
        self.mainLayout.addWidget(self.inputMin)
        self.mainLayout.addWidget(self.labelMax)
        self.mainLayout.addWidget(self.inputMax)
        self.mainLayout.addWidget(self.quantityLabel)
        self.mainLayout.addWidget(self.inputQuantity)
        self.mainLayout.addWidget(self.buttonGenerateMeanSquares)
    
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.parent.showGenerationWindow()
    
    def generateNumbers(self):
        ri, xi, ni = pse.generateNumbersByLinearCongruential(int(self.inputSeed.text()), int(self.inputK.text()), int(self.inputC.text()), int(self.inputG.text()), int(self.inputMin.text()), int(self.inputMax.text()), int(self.inputQuantity.text()))
        
        self.windowTable = QMainWindow()
        
        self.windowTable.setGeometry(50,50, 500, 300)
        self.windowTable.setWindowTitle("Resultado")
    
        table = QTableWidget()
        table.setRowCount(len(ri))
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Xi", "Ri", "Ni"])

        for row, values in enumerate(zip( xi, ri, ni)):
            for col, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                table.setItem(row, col, item)
            
        self.windowTable.setCentralWidget(table)
        
        buttonBack = QPushButton("Regresar", self.windowTable)
        buttonBack.setStyleSheet("""color: white;
        font-size: 30px;
        line-height: 36px;
        border-radius: 15px;
        background-color: #6CC700;
        padding: 4px;""")
        buttonBack.setGeometry(950, 700, 350, 50)
        buttonBack.clicked.connect(self.hideWindowTable)
        buttonBack.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        buttonShowChart = QPushButton("Mostrar grafica", self.windowTable)
        buttonShowChart.setStyleSheet("""color: white;
        font-size: 30px;
        line-height: 36px;
        border-radius: 15px;
        background-color: #6CC700;
        padding: 4px;""")
        buttonShowChart.setGeometry(600, 700, 350, 50)
        buttonShowChart.clicked.connect(lambda x: self.showChart(ri))
        buttonShowChart.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.windowTable.show()

    def classify_data(self, data):
        counts = [0] * len(intervals)
        for value in data:
            for i, interval in enumerate(intervals):
                if interval["lower"] <= value < interval["upper"]:
                    counts[i] += 1
                    break

        return counts

    def showChart(self, ri):
        counts = self.classify_data(ri)
        
        self.windowChart = QMainWindow()
        
        self.windowChart.setGeometry(50,50, 500, 300)
        self.windowChart.setWindowTitle("Grafica")
        canvas = FigureCanvas(plt.Figure(figsize=(6, 4)))
        self.windowChart.setCentralWidget(canvas)
        
        ax = canvas.figure.add_subplot(111)
        ax.bar(range(len(intervals)), counts, tick_label=[f"[{interval['lower']}, {interval['upper']})" for interval in intervals])
        ax.set_xlabel("Intervalos")
        ax.set_ylabel("Frecuencia")
        ax.set_title("Gráfico de Barras")
        
        canvas.draw()
        self.windowChart.show()

        
    def hideWindowTable(self, event):
        self.windowTable.hide()

    def validateDigit(self):
        text = self.inputSeed.text()
        if text.isdigit() and int(text) > 0:
            pass
        else:
            self.inputSeed.setText(text[:-1])

class MultiplicativeCongruentialGeneration(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Congruencia Multiplicativa")
        self.stylesheet = """
            MultiplicativeCongruentialGeneration{
                border-image: url('./images/background1.jpg') 0 0 0 0 stretch stretch;
            }
        """
        self.setStyleSheet(self.stylesheet)
        self.showMaximized()
        #Xo, t, g, quantity
        self.labelSeed = QLabel("Semilla: ")
        self.font = QFont()
        self.font.setPointSize(18)
        self.font.setBold(True)
        self.labelSeed.setStyleSheet("""color:white;""")
        self.labelSeed.setFont(self.font)
        
        self.inputSeed = QLineEdit(self)
        self.inputSeed.setFixedSize(250,30)
        self.inputSeed.textChanged.connect(self.validateDigit)
        
        self.labelT = QLabel("t: ")
        self.font = QFont()
        self.font.setPointSize(18)
        self.font.setBold(True)
        self.labelT.setStyleSheet("""color:white;""")
        self.labelT.setFont(self.font)
        
        self.inputT = QLineEdit(self)
        self.inputT.setFixedSize(250,30)
        self.inputT.textChanged.connect(self.validateDigit)

        self.labelG = QLabel("g: ")
        self.font = QFont()
        self.font.setPointSize(18)
        self.font.setBold(True)
        self.labelG.setStyleSheet("""color:white;""")
        self.labelG.setFont(self.font)
        
        self.inputG = QLineEdit(self)
        self.inputG.setFixedSize(250,30)
        self.inputG.textChanged.connect(self.validateDigit)
        
        self.labelMin = QLabel("Min: ")
        self.font = QFont()
        self.font.setPointSize(18)
        self.font.setBold(True)
        self.labelMin.setStyleSheet("""color:white;""")
        self.labelMin.setFont(self.font)
        
        self.inputMin = QLineEdit(self)
        self.inputMin.setFixedSize(250,30)
        
        self.labelMax = QLabel("Max: ")
        self.font = QFont()
        self.font.setPointSize(18)
        self.font.setBold(True)
        self.labelMax.setStyleSheet("""color:white;""")
        self.labelMax.setFont(self.font)
        
        self.inputMax = QLineEdit(self)
        self.inputMax.setFixedSize(250,30)
        
        self.quantityLabel = QLabel("Cantidad: ")
        self.font = QFont()
        self.font.setPointSize(18)
        self.font.setBold(True)
        self.quantityLabel.setStyleSheet("""color:white;""")
        self.quantityLabel.setFont(self.font)
        
        self.inputQuantity = QLineEdit(self)
        self.inputQuantity.setFixedSize(250,30)
        self.inputQuantity.textChanged.connect(self.validateDigit)
        
        self.buttonGenerateMeanSquares = QPushButton("Generar")
        self.buttonGenerateMeanSquares.clicked.connect(self.generateNumbers)
        self.buttonGenerateMeanSquares.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        central_widget = QWidget()
        
        self.setCentralWidget(central_widget)
        self.mainLayout = QVBoxLayout(central_widget)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.labelSeed)
        self.mainLayout.addWidget(self.inputSeed)
        self.mainLayout.addWidget(self.labelT)
        self.mainLayout.addWidget(self.inputT)
        self.mainLayout.addWidget(self.labelG)
        self.mainLayout.addWidget(self.inputG)
        self.mainLayout.addWidget(self.labelMin)
        self.mainLayout.addWidget(self.inputMin)
        self.mainLayout.addWidget(self.labelMax)
        self.mainLayout.addWidget(self.inputMax)
        self.mainLayout.addWidget(self.quantityLabel)
        self.mainLayout.addWidget(self.inputQuantity)
        self.mainLayout.addWidget(self.buttonGenerateMeanSquares)
    
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.parent.showGenerationWindow()
    
    def generateNumbers(self):
        ri, xi, ni = pse.generateNumbersByMultiplicativeCongruential(int(self.inputSeed.text()), int(self.inputT.text()), int(self.inputG.text()), int(self.inputMin.text()), int(self.inputMax.text()), int(self.inputQuantity.text()))
        
        self.windowTable = QMainWindow()
        
        self.windowTable.setGeometry(50,50, 500, 300)
        self.windowTable.setWindowTitle("Resultado")
    
        table = QTableWidget()
        table.setRowCount(len(ri))
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Xi", "Ri", "Ni"])

        for row, values in enumerate(zip( xi, ri, ni)):
            for col, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                table.setItem(row, col, item)
            
        self.windowTable.setCentralWidget(table)
        
        buttonBack = QPushButton("Regresar", self.windowTable)
        buttonBack.setStyleSheet("""color: white;
        font-size: 30px;
        line-height: 36px;
        border-radius: 15px;
        background-color: #6CC700;
        padding: 4px;""")
        buttonBack.setGeometry(950, 700, 350, 50)
        buttonBack.clicked.connect(self.hideWindowTable)
        buttonBack.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        buttonShowChart = QPushButton("Mostrar grafica", self.windowTable)
        buttonShowChart.setStyleSheet("""color: white;
        font-size: 30px;
        line-height: 36px;
        border-radius: 15px;
        background-color: #6CC700;
        padding: 4px;""")
        buttonShowChart.setGeometry(600, 700, 350, 50)
        buttonShowChart.clicked.connect(lambda x: self.showChart(ri))
        buttonShowChart.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.windowTable.show()

    def classify_data(self, data):
        counts = [0] * len(intervals)
        for value in data:
            for i, interval in enumerate(intervals):
                if interval["lower"] <= value < interval["upper"]:
                    counts[i] += 1
                    break

        return counts

    def showChart(self, ri):
        counts = self.classify_data(ri)
        
        self.windowChart = QMainWindow()
        
        self.windowChart.setGeometry(50,50, 500, 300)
        self.windowChart.setWindowTitle("Grafica")
        canvas = FigureCanvas(plt.Figure(figsize=(6, 4)))
        self.windowChart.setCentralWidget(canvas)
        
        ax = canvas.figure.add_subplot(111)
        ax.bar(range(len(intervals)), counts, tick_label=[f"[{interval['lower']}, {interval['upper']})" for interval in intervals])
        ax.set_xlabel("Intervalos")
        ax.set_ylabel("Frecuencia")
        ax.set_title("Gráfico de Barras")
        
        canvas.draw()
        self.windowChart.show()

        
    def hideWindowTable(self, event):
        self.windowTable.hide()

    def validateDigit(self):
        text = self.inputSeed.text()
        if text.isdigit() and int(text) > 0:
            pass
        else:
            self.inputSeed.setText(text[:-1])

import numpy as np

class UniformGeneration(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Congruencia Multiplicativa")
        self.stylesheet = """
            UniformGeneration{
                border-image: url('./images/background1.jpg') 0 0 0 0 stretch stretch;
            }
        """
        self.setStyleSheet(self.stylesheet)
        self.showMaximized()
        #max - min - cantidad
        self.labelMax = QLabel("Max: ")
        self.font = QFont()
        self.font.setPointSize(18)
        self.font.setBold(True)
        self.labelMax.setStyleSheet("""color:white;""")
        self.labelMax.setFont(self.font)
        
        self.inputMax = QLineEdit(self)
        self.inputMax.setFixedSize(250,30)
        self.inputMax.textChanged.connect(self.validateDigit)
        
        self.labelMin = QLabel("Min: ")
        self.font = QFont()
        self.font.setPointSize(18)
        self.font.setBold(True)
        self.labelMin.setStyleSheet("""color:white;""")
        self.labelMin.setFont(self.font)
        
        self.inputMin = QLineEdit(self)
        self.inputMin.setFixedSize(250,30)
        self.inputMin.textChanged.connect(self.validateDigit)

        self.labelQuantity = QLabel("Cantidad: ")
        self.font = QFont()
        self.font.setPointSize(18)
        self.font.setBold(True)
        self.labelQuantity.setStyleSheet("""color:white;""")
        self.labelQuantity.setFont(self.font)
        
        self.inputQuantity = QLineEdit(self)
        self.inputQuantity.setFixedSize(250,30)
        self.inputQuantity.textChanged.connect(self.validateDigit)
        
        self.buttonGenerate = QPushButton("Generar")
        
        
        self.buttonGenerate.clicked.connect(self.generateNumbers)
        self.buttonGenerate.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.buttonGenerate.clicked.connect(self.generateNumbers)
        central_widget = QWidget()
        
        self.setCentralWidget(central_widget)
        self.mainLayout = QVBoxLayout(central_widget)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.labelMin)
        self.mainLayout.addWidget(self.inputMin)
        self.mainLayout.addWidget(self.labelMax)
        self.mainLayout.addWidget(self.inputMax)
        self.mainLayout.addWidget(self.labelQuantity)
        self.mainLayout.addWidget(self.inputQuantity)
        self.mainLayout.addWidget(self.buttonGenerate)
        
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.parent.showGenerationWindow()
    
    def generateNumbers(self):
        ri, xi, ni = pse.generateNumbersByUniformDistribution(int(self.inputMin.text()), int(self.inputMax.text()), int(self.inputQuantity.text()))
        
        self.windowTable = QMainWindow()
        
        self.windowTable.setGeometry(50,50, 500, 300)
        self.windowTable.setWindowTitle("Resultado")
    
        table = QTableWidget()
        table.setRowCount(len(ri))
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Xi", "Ri", "Ni"])

        for row, values in enumerate(zip( xi, ri, ni)):
            for col, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                table.setItem(row, col, item)
            
        self.windowTable.setCentralWidget(table)
        
        buttonBack = QPushButton("Regresar", self.windowTable)
        buttonBack.setStyleSheet("""color: white;
        font-size: 30px;
        line-height: 36px;
        border-radius: 15px;
        background-color: #6CC700;
        padding: 4px;""")
        buttonBack.setGeometry(950, 700, 350, 50)
        buttonBack.clicked.connect(self.hideWindowTable)
        buttonBack.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        buttonShowChart = QPushButton("Mostrar grafica", self.windowTable)
        buttonShowChart.setStyleSheet("""color: white;
        font-size: 30px;
        line-height: 36px;
        border-radius: 15px;
        background-color: #6CC700;
        padding: 4px;""")
        buttonShowChart.setGeometry(600, 700, 350, 50)
        buttonShowChart.clicked.connect(lambda x: self.showChart(ni))
        buttonShowChart.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.windowTable.show()

    def classify_data(self, data, intervalsData):
        counts = [0] * len(intervalsData)
        
        for value in data:
            for i, interval in enumerate(intervalsData):
                if interval["lower"] <= value < interval["upper"]:
                    counts[i] += 1
                    break

        return counts

    def calculate_intervals(self, min_value, max_value, n_intervals):
        intervals = np.linspace(min_value, max_value, num=n_intervals+1)
        return [{"lower": intervals[i], "upper": intervals[i+1]} for i in range(len(intervals)-1)]

    def showChart(self, ni):
        intervalsUniform = self.calculate_intervals(int(self.inputMin.text()), int(self.inputMax.text()), 20)
        
        counts = self.classify_data(ni, intervalsUniform)
        self.windowChart = QMainWindow()
        
        
        self.windowChart.setGeometry(50,50, 500, 300)
        self.windowChart.setWindowTitle("Grafica")
        canvas = FigureCanvas(plt.Figure(figsize=(6, 4)))
        self.windowChart.setCentralWidget(canvas)
        
        ax = canvas.figure.add_subplot(111)
        ax.bar(range(len(intervalsUniform)), counts, tick_label=[f"[{interval['lower']}, {interval['upper']})" for interval in intervalsUniform])
        ax.set_xlabel("Intervalos")
        ax.set_ylabel("Frecuencia")
        ax.set_title("Gráfico de Barras")
        
        canvas.draw()
        self.windowChart.show()

        
    def hideWindowTable(self, event):
        self.windowTable.hide()

    def validateDigit(self):
        text = self.inputMax.text()
        if text.isdigit() and int(text) > 0:
            pass
        else:
            self.inputMax.setText(text[:-1])
            
class NormalGeneration(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Congruencia Multiplicativa")
        self.stylesheet = """
            UniformGeneration{
                border-image: url('./images/background1.jpg') 0 0 0 0 stretch stretch;
            }
        """
        self.setStyleSheet(self.stylesheet)
        self.showMaximized()
        #max - min - cantidad
        self.labelMax = QLabel("Media: ")
        self.font = QFont()
        self.font.setPointSize(18)
        self.font.setBold(True)
        self.labelMax.setStyleSheet("""color:white;""")
        self.labelMax.setFont(self.font)
        
        self.inputMax = QLineEdit(self)
        self.inputMax.setFixedSize(250,30)
        self.inputMax.textChanged.connect(self.validateDigit)
        
        self.labelMin = QLabel("Desv Est.: ")
        self.font = QFont()
        self.font.setPointSize(18)
        self.font.setBold(True)
        self.labelMin.setStyleSheet("""color:white;""")
        self.labelMin.setFont(self.font)
        
        self.inputMin = QLineEdit(self)
        self.inputMin.setFixedSize(250,30)
        self.inputMin.textChanged.connect(self.validateDigit)

        self.labelQuantity = QLabel("Cantidad: ")
        self.font = QFont()
        self.font.setPointSize(18)
        self.font.setBold(True)
        self.labelQuantity.setStyleSheet("""color:white;""")
        self.labelQuantity.setFont(self.font)
        
        self.inputQuantity = QLineEdit(self)
        self.inputQuantity.setFixedSize(250,30)
        self.inputQuantity.textChanged.connect(self.validateDigit)
        
        self.buttonGenerate = QPushButton("Generar")
        
        
        self.buttonGenerate.clicked.connect(self.generateNumbers)
        self.buttonGenerate.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.buttonGenerate.clicked.connect(self.generateNumbers)
        central_widget = QWidget()
        
        self.setCentralWidget(central_widget)
        self.mainLayout = QVBoxLayout(central_widget)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.labelMin)
        self.mainLayout.addWidget(self.inputMin)
        self.mainLayout.addWidget(self.labelMax)
        self.mainLayout.addWidget(self.inputMax)
        self.mainLayout.addWidget(self.labelQuantity)
        self.mainLayout.addWidget(self.inputQuantity)
        self.mainLayout.addWidget(self.buttonGenerate)
        
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.parent.showGenerationWindow()
    
    def generateNumbers(self):
        ri, xi, ni = pse.generateNumbersByNormalDistribution(int(self.inputMin.text()), int(self.inputMax.text()), int(self.inputQuantity.text()))
        
        self.windowTable = QMainWindow()
        
        self.windowTable.setGeometry(50,50, 500, 300)
        self.windowTable.setWindowTitle("Resultado")
    
        table = QTableWidget()
        table.setRowCount(len(ri))
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Xi", "Ri", "Ni"])

        for row, values in enumerate(zip( xi, ri, ni)):
            for col, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                table.setItem(row, col, item)
            
        self.windowTable.setCentralWidget(table)
        
        buttonBack = QPushButton("Regresar", self.windowTable)
        buttonBack.setStyleSheet("""color: white;
        font-size: 30px;
        line-height: 36px;
        border-radius: 15px;
        background-color: #6CC700;
        padding: 4px;""")
        buttonBack.setGeometry(950, 700, 350, 50)
        buttonBack.clicked.connect(self.hideWindowTable)
        buttonBack.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        buttonShowChart = QPushButton("Mostrar grafica", self.windowTable)
        buttonShowChart.setStyleSheet("""color: white;
        font-size: 30px;
        line-height: 36px;
        border-radius: 15px;
        background-color: #6CC700;
        padding: 4px;""")
        buttonShowChart.setGeometry(600, 700, 350, 50)
        buttonShowChart.clicked.connect(lambda x: self.showChart(ni))
        buttonShowChart.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.windowTable.show()

    def classify_data(self, data, intervalsData):
        counts = [0] * len(intervalsData)
        
        for value in data:
            for i, interval in enumerate(intervalsData):
                if interval["lower"] <= value < interval["upper"]:
                    counts[i] += 1
                    break

        return counts

    def calculate_intervals(self, min_value, max_value, n_intervals):
        intervals = np.linspace(min_value, max_value, num=n_intervals+1)
        return [{"lower": intervals[i], "upper": intervals[i+1]} for i in range(len(intervals)-1)]

    def showChart(self, ni):
        min = np.min(ni)
        max = np.max(ni)
        intervalsUniform = self.calculate_intervals(min, max, 20)
        
        counts = self.classify_data(ni, intervalsUniform)
        self.windowChart = QMainWindow()
        
        
        self.windowChart.setGeometry(50,50, 500, 300)
        self.windowChart.setWindowTitle("Grafica")
        canvas = FigureCanvas(plt.Figure(figsize=(6, 4)))
        self.windowChart.setCentralWidget(canvas)
        
        ax = canvas.figure.add_subplot(111)
        ax.bar(range(len(intervalsUniform)), counts, tick_label=[f"[{interval['lower']}, {interval['upper']})" for interval in intervalsUniform])
        ax.set_xlabel("Intervalos")
        ax.set_ylabel("Frecuencia")
        ax.set_title("Gráfico de Barras")
        
        canvas.draw()
        self.windowChart.show()

        
    def hideWindowTable(self, event):
        self.windowTable.hide()

    def validateDigit(self):
        text = self.inputMax.text()
        if text.isdigit() and int(text) > 0:
            pass
        else:
            self.inputMax.setText(text[:-1])