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
        self.statusBar=self.statusBar()
        self.statusBar.showMessage("Listo")
        self.panelVoltaje=Panel("VOLTAJE")
        self.panelCorriente=Panel("CORRIENTE")
        botonRecibir=QPushButton("Lectura Voltaje")
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
        dialogoEnviar.setText("Desea medir voltaje?")
        dialogoEnviar.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        botonSeleccionado = dialogoEnviar.exec()
        if botonSeleccionado == QMessageBox.Yes:
            self.statusBar.showMessage("Abriendo Puerto")
            self.configuraPuerto()
        else:
            print("Cancel")

    def configuraPuerto(self):
        with serial.Serial() as self.puerto:
            self.puerto.baudrate=9600
            self.puerto.port= 'COM11'
            self.statusBar.showMessage("Configura Puerto")
            self.abrePuerto()

    def abrePuerto(self):
        self.statusBar.showMessage("Lectura")
        self.puerto.open()
        lecturaVoltaje=self.puerto.readline()
        svoltaje=lecturaVoltaje.decode('utf-8')
        voltaje=svoltaje.strip()
        #self.statusBar.showMessage(svoltaje)
        self.actualizaVoltaje(float(voltaje))
        self.puerto.close()
        self.statusBar.showMessage("Listo")



if __name__ == '__main__':
    aplicacion = QApplication([])
    ventanaPrincipal = VentanaPrincipal()
    ventanaPrincipal.show()
    ventanaPrincipal.actualizaVoltaje(25.003)
    ventanaPrincipal.actualizaCorriente(1500)
    aplicacion.exec()

