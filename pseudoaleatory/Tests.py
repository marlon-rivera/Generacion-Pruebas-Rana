import taller_sc as pse
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QCheckBox, QVBoxLayout, QWidget, QRadioButton, QLabel, QLineEdit, QButtonGroup, QTableWidget, QTableWidgetItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import pandas as pd
 
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Interfaz")
        self.setGeometry(100, 100, 400, 300)

        self.btn_generar = QPushButton("Generar", self)
        self.btn_generar.setGeometry(50, 50, 100, 30)

        self.btn_subir_archivo = QPushButton("Subir Archivo", self)
        self.btn_subir_archivo.setGeometry(50, 100, 100, 30)

        self.checkbox_medias = QCheckBox("Medias", self)
        self.checkbox_medias.setGeometry(200, 50, 100, 30)

        self.checkbox_varianzas = QCheckBox("Varianzas", self)
        self.checkbox_varianzas.setGeometry(200, 80, 100, 30)

        self.checkbox_uniformidad = QCheckBox("Uniformidad (Chi2)", self)
        self.checkbox_uniformidad.setGeometry(200, 110, 150, 30)

        self.checkbox_ks = QCheckBox("KS", self)
        self.checkbox_ks.setGeometry(200, 140, 100, 30)

        self.checkbox_poker = QCheckBox("Poker", self)
        self.checkbox_poker.setGeometry(200, 170, 100, 30)

        self.btn_generar.clicked.connect(self.generar_clicked)
        self.btn_subir_archivo.clicked.connect(self.subir_archivo_clicked)

    def generar_clicked(self):
        self.second_window = SecondWindow(self)
        self.second_window.show()
        
        
    def subir_archivo_clicked(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Subir Archivo", "", "*.csv")
        if filename:
            df = pd.read_csv(filename)
            result = []
            self.ri = df.values.tolist()
            for num in self.ri:
                result.append(num[0])
            self.ri = result
        self.second_window = SecondWindow(self, self.ri)
        self.second_window.show()

class SecondWindow(QMainWindow):
    def __init__(self, parent, ri = None):
        super().__init__(parent)
        self.parent = parent
        self.ri = ri
        self.setWindowTitle("Parametros")
        self.setGeometry(200, 200, 400, 300)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        labels = {
            "Xo": "Xo:",
            "K": "K:",
            "C": "C:",
            "g": "g:",
            "t": "t:",
            "min": "Mínimo:",
            "max": "Máximo:",
            "num_intervalos": "# de Intervalos:",
            "cantidad": "Cantidad:"
        }

        self.inputs = {}
        for name, label_text in labels.items():
            label = QLabel(label_text)
            input_field = QLineEdit()
            input_field.setText("0")
            self.layout.addWidget(label)
            self.layout.addWidget(input_field)
            self.inputs[name] = input_field

        self.radio_group = QButtonGroup(self.central_widget)
        self.radio_group.setExclusive(True)

        self.radio_cuadrados_medios = QRadioButton("Cuadrados Medios")
        self.radio_group.addButton(self.radio_cuadrados_medios)
        self.layout.addWidget(self.radio_cuadrados_medios)

        self.radio_congruencia_lineal = QRadioButton("Congruencia Lineal")
        self.radio_group.addButton(self.radio_congruencia_lineal)
        self.layout.addWidget(self.radio_congruencia_lineal)

        self.radio_congruencia_multiplicativa = QRadioButton("Congruencia Multiplicativa")
        self.radio_group.addButton(self.radio_congruencia_multiplicativa)
        self.layout.addWidget(self.radio_congruencia_multiplicativa)

        self.aceptar_boton = QPushButton("Aceptar")
        self.aceptar_boton.clicked.connect(self.generateNumbers)
        self.layout.addWidget(self.aceptar_boton)

    def get_values(self):
        values = {}
        for name, input_field in self.inputs.items():
            values[name] = int(input_field.text())
        return values
    
    def generateNumbers(self):
        self.values = self.get_values()
        ri = []
        if(self.ri is not None):
            ri = self.ri
            result = [ri[0]]
            for i in range(1, len(ri)):
                if(ri[i] == 0.0 or ri[i] == 1.0):
                    continue
                if("-" in str(ri[i])):
                    continue
                result.append(pse.truncate(ri[i]))
            ri = result
        else:
            selected_button = self.radio_group.checkedButton().text()
            if selected_button == "Cuadrados Medios":
                ri = pse.generateNumbersByMeanSquares(self.values["Xo"], self.values["min"], self.values["max"], self.values["cantidad"])[0]
            elif selected_button == "Congruencia Lineal":
                ri = pse.generateNumbersByLinearCongruential(self.values["Xo"], self.values["K"], self.values["C"], self.values["g"], self.values["min"], self.values["max"], self.values["cantidad"])[0]
            elif selected_button == "Congruencia Multiplicativa":
                ri = pse.generateNumbersByMultiplicativeCongruential(self.values["Xo"], self.values["t"], self.values["g"], self.values["min"], self.values["max"], self.values["cantidad"])[0]
        if self.parent.checkbox_medias.isChecked():
            mean = StatsWindow(pse.meanTest(ri), self)
            mean.show()
        if self.parent.checkbox_varianzas.isChecked():
            variance = Variance(pse.varianceTest(ri), self)
            variance.show()
        if self.parent.checkbox_uniformidad.isChecked():
            chi2 = Chi2(pse.testChi2Uniformity(ri, self.values["num_intervalos"]), self)
            chi2.show()
        if self.parent.checkbox_ks.isChecked():
            ks = KS(pse.testKS(ri, self.values["num_intervalos"]), self)
            ks.show()
        if self.parent.checkbox_poker.isChecked():
            poker = Poker(pse.testPoker(ri), self)
            poker.show()

class StatsWindow(QMainWindow):
    def __init__(self, results, parent=None):
        super().__init__(parent)
        #mean >= Li and mean <= Ls, alpha, size, mean, aux, Z, Li, Ls
        self.setWindowTitle("Prueba de Medias")
        self.setGeometry(100, 100, 400, 300)

        # Crear el layout principal
        layout = QVBoxLayout()

        # Aceptar y alpha
        accept_label = QLabel("Aceptación:  95%")
        alpha_label = QLabel("Alpha: " + str(results[1]))
        layout.addWidget(accept_label)
        layout.addWidget(alpha_label)

        # Cantidad de datos
        data_count_label = QLabel("Cantidad de datos: " + str(results[2]))
        layout.addWidget(data_count_label)

        # Media del arreglo
        mean_label = QLabel("Media: " + str(results[3]))
        layout.addWidget(mean_label)

        # 1-(alpha/2)
        one_minus_alpha_label = QLabel("1 - (alpha/2): " + str(results[4]))
        layout.addWidget(one_minus_alpha_label)

        # Z, Li, Ls
        z_label = QLabel("Z: " + str(results[5]))
        li_label = QLabel("Li: " + str(results[6]))
        ls_label = QLabel("Ls: " + str(results[7]))
        layout.addWidget(z_label)
        layout.addWidget(li_label)
        layout.addWidget(ls_label)

        # Resultado de la prueba
        result_label = QLabel("Resultado de la prueba: " + str(results[0]))
        layout.addWidget(result_label)

        # Botón de Aceptar
        accept_button = QPushButton("Aceptar")
        accept_button.clicked.connect(self.close)
        layout.addWidget(accept_button)

        # Crear el widget central y establecer el layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

class Variance(QMainWindow):
    def __init__(self, values, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Prueba de Varianza")
        self.setGeometry(100, 100, 400, 300)

        # Crear el layout principal
        layout = QVBoxLayout()

        # Aceptación y alpha
        accept_label = QLabel("Aceptación: 95%")
        alpha_label = QLabel("Alpha: " + str(values[1]))
        layout.addWidget(accept_label)
        layout.addWidget(alpha_label)

        # n, R, σ^2
        n_label = QLabel("n: " + str(values[2]))
        r_label = QLabel("R: " + str(values[4]))
        sigma_squared_label = QLabel("σ^2: " + str(values[3]))
        layout.addWidget(n_label)
        layout.addWidget(r_label)
        layout.addWidget(sigma_squared_label)

        # alpha/2, 1-(alpha/2)
        alpha_half_label = QLabel("Alpha/2: " + str(values[5]))
        one_minus_alpha_half_label = QLabel("1 - (Alpha/2): " + str(values[6]))
        layout.addWidget(alpha_half_label)
        layout.addWidget(one_minus_alpha_half_label)

        # X^2(alpha/2), X^2(1-(alpha/2))
        chi_square_alpha_half_label = QLabel("X^2(Alpha/2): " + str(values[7]))
        chi_square_one_minus_alpha_half_label = QLabel("X^2(1 - (Alpha/2)): " + str(values[8]))
        layout.addWidget(chi_square_alpha_half_label)
        layout.addWidget(chi_square_one_minus_alpha_half_label)

        # LIR, LSR
        lir_label = QLabel("LIR: " + str(values[9]))
        lsr_label = QLabel("LSR: " + str(values[10]))
        layout.addWidget(lir_label)
        layout.addWidget(lsr_label)
        
        # Resultado de la prueba
        result_label = QLabel("Resultado de la prueba: " + str(values[0]))
        layout.addWidget(result_label)

        # Botón de Aceptar
        accept_button = QPushButton("Aceptar")
        accept_button.clicked.connect(self.close)
        layout.addWidget(accept_button)

        # Crear el widget central y establecer el layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

class Chi2(QMainWindow):
    def __init__(self, values, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Prueba de uniformidad Chi2")
        self.setGeometry(100, 100, 800, 600)
        # Crear layout principal
        layout = QVBoxLayout()
        # intervals, frequencies, expectedFrequency, chi2Values, sum(frequencies), sum(expectedFrequency), sum(chi2Values), nIntervals - 1, chi2.isf(0.05, nIntervals - 1)
        # Crear la gráfica de barras
        self.figure = plt.Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)
        self.plot_bar_chart(values[1], values[2].values())
        layout.addWidget(self.canvas)

        # Crear la tabla
        self.table = QTableWidget()
        self.setup_table(self.table, values[1])
        self.populate_table(values[1], values[2].values(), values[3], values[4])
        layout.addWidget(self.table)

        # Crear los labels con las sumatorias y otros valores
        sum_frequencies_label = QLabel(f"Suma de Frecuencias: {values[5]}")
        sum_expected_frequencies_label = QLabel(f"Suma de Frecuencias Esperadas: { sum([values[6]]*len(values[2]))}")
        sum_chi2_values_label = QLabel(f"Suma de Valores Chi2: {values[7]}")
        gl_label = QLabel(f"Grados de Libertad (GL): {values[8]}")
        chi2_isf_label = QLabel(f"Chi2.isf(0.05, GL): {values[9]}")
        result_label = QLabel("Resultado de la prueba: " + str(values[0]))
        layout.addWidget(sum_frequencies_label)
        layout.addWidget(sum_expected_frequencies_label)
        layout.addWidget(sum_chi2_values_label)
        layout.addWidget(gl_label)
        layout.addWidget(chi2_isf_label)
        layout.addWidget(result_label)
        
        accept_button = QPushButton("Aceptar")
        accept_button.clicked.connect(self.close)
        layout.addWidget(accept_button)

        # Establecer el layout en el widget central
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def plot_bar_chart(self, intervals, frequencies):
        self.figure.set_figwidth(10)  # Ancho de la figura
        self.figure.set_figheight(6)  # Alto de la figura
        ax = self.figure.add_subplot(111)
        labels = [f"{t[0]:.4f}-{t[1]:.4f}" for t in intervals]
        ax.bar(labels, frequencies)
        ax.set_xlabel("Intervalos")
        ax.set_xticklabels(labels, rotation=45, ha='right')
        ax.set_ylabel("Frecuencia")
        ax.set_title("Gráfico de Barras")

    def setup_table(self, table, intervals):
        table.setRowCount(len(intervals))
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Intervalo", "Frecuencia Observada", "Frecuencia Esperada", "Valor Chi2"])

    def populate_table(self, intervals, frequencies, expected_frequencies, chi2_values):
        expected_frequencies = [expected_frequencies] * len(frequencies)
        for i, (interval, frequency, expected_frequency, chi2_value) in enumerate(zip(intervals, frequencies, expected_frequencies, chi2_values)):
            table_item_interval = QTableWidgetItem(str(interval))
            table_item_frequency = QTableWidgetItem(str(frequency))
            table_item_expected_frequency = QTableWidgetItem(str(expected_frequency))
            table_item_chi2_value = QTableWidgetItem(str(chi2_value))
            self.table.setItem(i, 0, table_item_interval)
            self.table.setItem(i, 1, table_item_frequency)
            self.table.setItem(i, 2, table_item_expected_frequency)
            self.table.setItem(i, 3, table_item_chi2_value)

class KS(QMainWindow):
    def __init__(self, values, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Prueba KS")
        self.setGeometry(100, 100, 800, 600)
        #len(Ri), np.mean(Ri), minRi, maxRi, intervals, frequencies, cumulativeFrequency, percentageObtained, expectedFrequencies, percentageExpected, difference, maxDiff, dMaxP
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        labels = ["Aceptación: 95%", "Alpha: 5%", "n: " + str(values[1]), "R: " + str(values[2]), "Mínimo: " + str(values[3]), "Máximo: " + str(values[4])]
        for label in labels:
            layout.addWidget(QLabel(label))

        # Bar Chart
        self.figure = plt.Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.plot_bar_chart(values[5], values[6])

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Intervalos", "Frecuencia Obtenida", "Frecuencia Obtenida Acumulada",
                                               "Probabilidad Obtenida", "Frecuencia Esperada Acumulada",
                                               "Probabilidad Esperada", "Diferencia"])
        self.table.setRowCount(len(values[5]))
        self.populate_table(values[5], values[6], values[7], values[8], values[9], values[10], values[11])
        layout.addWidget(self.table)

        labels2 = ["DMAX: " + str(values[12]), "DMAXP: " + str(values[13]), "Resultado de la Prueba: " + str(values[0])]
        for label in labels2:
            layout.addWidget(QLabel(label))

        self.btn_accept = QPushButton("Aceptar")
        self.btn_accept.clicked.connect(self.close)
        layout.addWidget(self.btn_accept)

    def plot_bar_chart(self, intervals, frequencies):
        
        self.figure.set_figwidth(10)
        self.figure.set_figheight(6) 
        ax = self.figure.add_subplot()
        labels = [f"{t[0]:.4f}-{t[1]:.4f}" for t in intervals]

        ax.bar(labels, frequencies.values())
        ax.set_xlabel("Intervalos")
        ax.set_xticklabels(labels, rotation=45, ha='right')
        ax.set_ylabel("Frecuencia Obtenida")
        ax.set_title("Gráfico de Barras")


    def populate_table(self, intervals, frequencies, cumulativeFrequencies, percentageObtaineds, expectedFrequencies, percentageExpecteds, differences):
        
        for i, (interval, frequency, cumulativeFrequency, percentageObtained, expectedFrequency, percentageExpected, difference) in enumerate(zip(intervals, frequencies.values(), cumulativeFrequencies, percentageObtaineds, expectedFrequencies, percentageExpecteds, differences)):
            table_item_interval = QTableWidgetItem(str(interval))
            table_item_frequency = QTableWidgetItem(str(frequency))
            table_item_cumulativeFrequency = QTableWidgetItem(str(cumulativeFrequency))
            table_item_percentageObtained = QTableWidgetItem(str(percentageObtained))
            table_item_expectedFrequency = QTableWidgetItem(str(expectedFrequency))
            table_item_percentageExpected = QTableWidgetItem(str(percentageExpected))
            table_item_difference = QTableWidgetItem(str(difference))
            self.table.setItem(i, 0, table_item_interval)
            self.table.setItem(i, 1, table_item_frequency)
            self.table.setItem(i, 2, table_item_cumulativeFrequency)
            self.table.setItem(i, 3, table_item_percentageObtained)
            self.table.setItem(i, 4, table_item_expectedFrequency)
            self.table.setItem(i, 5, table_item_percentageExpected)
            self.table.setItem(i, 6, table_item_difference)
            
class Poker(QMainWindow):
    def __init__(self, values, parent=None):
        super().__init__(parent)
        #n Cat.	Oi	Prob.	Ei	(Ei - Oi)^2  /  Ei Σ X^2 alpha
        self.setWindowTitle("Prueba Poker")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Label for 'n'
        layout.addWidget(QLabel("n: " + str(values[1])))

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Cat.", "Oi", "Prob.", "Ei", "(Ei - Oi)^2 / Ei"])
        self.populate_table(values[2], values[3], values[4] ,values[5] , values[6])
        layout.addWidget(self.table)

        # Labels for Σ and X^2 alpha
        layout.addWidget(QLabel(f"Σ: {values[7]}"))
        layout.addWidget(QLabel(f"X^2 alpha: {values[8]}"))

        # Label for result
        layout.addWidget(QLabel(f"Resultado de la Prueba: {values[0]}"))

        # Button to close window
        self.btn_accept = QPushButton("Aceptar")
        self.btn_accept.clicked.connect(self.close)
        layout.addWidget(self.btn_accept)

    def populate_table(self, categories, observeds, probabilities, eis, eisaux):
        self.table.setRowCount(len(categories))
        for i, (category, observed, probability, ei, eiaux) in enumerate(zip(categories, observeds, probabilities, eis, eisaux)):
            table_item_category = QTableWidgetItem(str(category))
            table_item_observed = QTableWidgetItem(str(observed))
            table_item_probability = QTableWidgetItem(str(probability))
            table_item_ei = QTableWidgetItem(str(ei))
            table_item_eiaux = QTableWidgetItem(str(eiaux))
            self.table.setItem(i, 0, table_item_category)
            self.table.setItem(i, 1, table_item_observed)
            self.table.setItem(i, 2, table_item_probability)
            self.table.setItem(i, 3, table_item_ei)
            self.table.setItem(i, 4, table_item_eiaux)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
