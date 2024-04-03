from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLCDNumber,QLabel,QPushButton, QMessageBox)
import serial, time
class Display(QLCDNumber):
    def __init__(self, parent=None):
        super().__init__(parent)
        #Numero
        self.setSegmentStyle(QLCDNumber.Filled)
        self.setDigitCount(10)
        self.resize(400, 400)
        self.display(0)
        self.setStyleSheet('QLCDNumber {background-color: #000080; color: #FFFFFF; }')
    def actualiza(self, valor):
        self.display(valor)

class Panel(QWidget):
    def __init__(self, titulo, parent=None):
        super().__init__(parent)
        # Etiqueta
        self.titulo = titulo
        self.etiqueta = QLabel(titulo)
        self.etiqueta.setStyleSheet('QLabel { color: #000080; }')
        self.display=Display()
        layoutHorizontal = QHBoxLayout()
        layoutHorizontal.addWidget(self.etiqueta)
        layoutHorizontal.addWidget(self.display)
        self.setLayout(layoutHorizontal)
    def actualiza(self, valor):
        self.display.actualiza(valor)

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        # llamada a constructor de la clase padre
        super().__init__()
        # widgets
        self.setWindowTitle("Multimetro PC")
        self.setFixedWidth(500)
        self.setFixedHeight(300)
        self.panelVoltaje=Panel("VOLTAJE")
        self.panelCorriente=Panel("CORRIENTE")
        botonRecibir=QPushButton("Abre Puerto")
        botonRecibir.clicked.connect(self.confirma)
        # layout
        layoutVertical = QVBoxLayout()
        # Asigancaion del layout
        layoutVertical.addWidget(self.panelVoltaje)
        layoutVertical.addWidget(self.panelCorriente)
        layoutVertical.addWidget(botonRecibir)
        widget = QWidget()
        widget.setLayout(layoutVertical)
        self.setCentralWidget(widget)
    def actualizaVoltaje(self,valor):
        self.panelVoltaje.actualiza(valor)
    def actualizaCorriente(self,valor):
        self.panelCorriente.actualiza(valor)

    def confirma(self):
        dialogoEnviar = QMessageBox(self)
        dialogoEnviar.setWindowTitle("Monitor")
        dialogoEnviar.setText("Desea Abrir el puerto?")
        dialogoEnviar.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        botonSeleccionado = dialogoEnviar.exec()
        if botonSeleccionado == QMessageBox.Yes:
            self.abrePuerto()
        else:
            print("Cancel")

    def abrePuerto(self):
        #while True:
            with serial.Serial('/dev/ttyACM0', 9600) as ser:
                line = ser.readline()
                cadena=line.decode("utf-8")
                self.actualizaVoltaje(cadena)


if __name__ == '__main__':
    aplicacion = QApplication([])
    ventanaPrincipal = VentanaPrincipal()
    ventanaPrincipal.show()
    ventanaPrincipal.actualizaVoltaje(25.003)
    ventanaPrincipal.actualizaCorriente(1500)
    aplicacion.exec()

