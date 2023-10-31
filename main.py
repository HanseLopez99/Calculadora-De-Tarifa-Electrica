import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QStackedWidget, QLabel, QVBoxLayout, 
                             QWidget, QFormLayout, QLineEdit, QComboBox, QTextEdit, QListWidget, QMessageBox, QHBoxLayout)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class ImageCarousel(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculadora de Tarifa Eléctrica")
        self.setGeometry(100, 100, 800, 600)

        # Lista de imágenes para el carrusel
        self.image_paths = [
            "images/Microondas.jpg", 
            "images/Refrigerator.jpg", 
            "images/Televisor.jpg", 
            "images/Lavadora.jpg", 
            "images/Secadora.jpg", 
            "images/Computadora.jpg",
            "images/Tableta.jpg",
            "images/Cargador.jpg",
            "images/Impresora.jpg",
            "images/Router.jpg",
            "images/Consola.jpg",
            "images/Cafetera.jpg",
            "images/Licuadora.jpg",
            "images/Aspiradora.jpg",
            "images/Bocinas.jpg",
            "images/Camara.jpg",
            "images/Aire.jpg",
            "images/Lavavajillas.jpg",
            "images/Estufa.jpg",
            "images/Focos.jpg",
        ]
        
        self.current_index = 0

        # Lista de nombres para los dispositivos
        self.device_names = [
            "Horno de microondas", 
            "Refrigerador", 
            "Televisor", 
            "Lavadora", 
            "Secadora", 
            "Computadora",
            "Tableta",
            "Cargador de celular",
            "Impresora",
            "Router",
            "Consola de videojuegos",
            "Cafetera",
            "Licuadora",
            "Aspiradora",
            "Sistema de sonido",
            "Cámara de seguridad",
            "Aire acondicionado",
            "Lavavajillas",
            "Estufa",
            "Focos",
        ]

        # Lista para llevar un registro de los dispositivos ya seleccionados
        self.selected_devices = []

        # Widget principal
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # Layout principal
        layout = QVBoxLayout()

        # Carrusel de imágenes
        self.image_stack = QStackedWidget(self)
        for _ in range(7):  # Repetimos para tener al menos 20 imágenes
            for image_path in self.image_paths:
                pixmap = QPixmap(image_path)
                label = QLabel(self)
                label.setPixmap(pixmap.scaled(800, 400, Qt.AspectRatioMode.KeepAspectRatio))
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.image_stack.addWidget(label)

        layout.addWidget(self.image_stack)

        # Botón para seleccionar/des-seleccionar el dispositivo actual del carrusel
        self.toggle_device_button = QPushButton("Seleccionar dispositivo", self)
        self.toggle_device_button.clicked.connect(self.toggle_dispositivo)
        layout.addWidget(self.toggle_device_button)

        # Botones para navegar en el carrusel
        navigation_layout = QHBoxLayout()  # Layout horizontal para los botones de navegación

        self.prev_button = QPushButton("Anterior", self)
        self.prev_button.clicked.connect(self.show_previous_image)
        navigation_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Siguiente", self)
        self.next_button.clicked.connect(self.show_next_image)
        navigation_layout.addWidget(self.next_button)

        layout.addLayout(navigation_layout)  # Agregar el layout de navegación al layout principal

        # Campos para ingresar detalles del dispositivo
        form_layout = QFormLayout()
        self.potencia_entry = QLineEdit(self)
        self.corriente_entry = QLineEdit(self)
        self.horas_entry = QLineEdit(self)
        self.voltaje_entry = QLineEdit(self)
        self.largo_cable_entry = QLineEdit(self)
        self.tarifa_combo = QComboBox(self)
        self.tarifa_combo.addItems(["Baja Tensión Simple Social", "Baja Tensión Simple"])
        form_layout.addRow("Potencia:", self.potencia_entry)
        form_layout.addRow("Corriente:", self.corriente_entry)
        form_layout.addRow("Horas de uso:", self.horas_entry)
        form_layout.addRow("Voltaje:", self.voltaje_entry)
        form_layout.addRow("Largo del cable:", self.largo_cable_entry)
        form_layout.addRow("Tipo de tarifa:", self.tarifa_combo)

        # Campo para ingresar el valor del costo de energía
        self.costo_energia_entry = QLineEdit(self)
        form_layout.addRow("Costo de energía (Q/KWh):", self.costo_energia_entry)

        # Lista para mostrar gráficamente los dispositivos seleccionados
        self.dispositivos_lista = QListWidget(self)
        form_layout.addRow("Dispositivos seleccionados:", self.dispositivos_lista)

        # Opción para elegir el intervalo de tiempo
        self.intervalo_combo = QComboBox(self)
        self.intervalo_combo.addItems(["Día", "Mes", "Año"])
        form_layout.addRow("Intervalo de tiempo:", self.intervalo_combo)

        layout.addLayout(form_layout)

        # Botones para calcular tarifa y calibre
        self.calcular_tarifa_button = QPushButton("Calcular Tarifa", self)
        self.calcular_tarifa_button.clicked.connect(self.calcular_tarifa)
        layout.addWidget(self.calcular_tarifa_button)

        self.calcular_calibre_button = QPushButton("Calcular Calibre", self)
        self.calcular_calibre_button.clicked.connect(self.calcular_calibre)
        layout.addWidget(self.calcular_calibre_button)

        # Área de texto para mostrar resultados
        self.resultados_text = QTextEdit(self)
        layout.addWidget(self.resultados_text)

        main_widget.setLayout(layout)

    def toggle_dispositivo(self):
      # Obtener el nombre del dispositivo actualmente visible
      dispositivo_nombre = self.device_names[self.current_index % len(self.device_names)]
      if dispositivo_nombre in self.selected_devices:
          self.des_seleccionar_dispositivo()
      else:
          self.agregar_dispositivo()

    def agregar_dispositivo(self):
      # Obtener el nombre del dispositivo actualmente visible
      dispositivo_nombre = self.device_names[self.current_index % len(self.device_names)]
      if len(self.selected_devices) < 10:
          self.dispositivos_lista.insertItem(0, dispositivo_nombre)
          self.selected_devices.append(dispositivo_nombre)
          self.toggle_device_button.setText("Des-seleccionar dispositivo")
      else:
          QMessageBox.warning(self, "Advertencia", "Has alcanzado el límite de 10 dispositivos.")

    def des_seleccionar_dispositivo(self):
      # Obtener el nombre del dispositivo actualmente visible
      dispositivo_nombre = self.device_names[self.current_index % len(self.device_names)]
      if dispositivo_nombre in self.selected_devices:
          item = self.dispositivos_lista.findItems(dispositivo_nombre, Qt.MatchFlag.MatchExactly)[0]
          row = self.dispositivos_lista.row(item)
          self.dispositivos_lista.takeItem(row)
          self.selected_devices.remove(dispositivo_nombre)
          self.toggle_device_button.setText("Seleccionar dispositivo")

    def show_previous_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.image_stack.setCurrentIndex(self.current_index)
            self.update_button_text()

    def show_next_image(self):
        if self.current_index < len(self.image_paths) * 7 - 1:  # Ajuste para las 20 imágenes
            self.current_index += 1
            self.image_stack.setCurrentIndex(self.current_index)
            self.update_button_text()

    def update_button_text(self):
        # Obtener el nombre del dispositivo actualmente visible
        dispositivo_nombre = self.device_names[self.current_index % len(self.device_names)]
        if dispositivo_nombre in self.selected_devices:
            self.toggle_device_button.setText("Des-seleccionar dispositivo")
        else:
            self.toggle_device_button.setText("Seleccionar dispositivo")

    def calcular_tarifa(self):
        # Aquí puedes agregar el código para calcular la tarifa
        # Por ahora, solo muestra un mensaje en el área de texto
        self.resultados_text.append("Tarifa calculada (ejemplo).")

    def calcular_calibre(self):
        # Aquí puedes agregar el código para calcular el calibre del cable
        # Por ahora, solo muestra un mensaje en el área de texto
        self.resultados_text.append("Calibre del cable calculado (ejemplo).")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageCarousel()
    window.show()
    sys.exit(app.exec())
