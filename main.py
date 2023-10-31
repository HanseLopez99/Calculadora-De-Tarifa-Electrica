import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QStackedWidget, QLabel, QVBoxLayout, 
                             QWidget, QFormLayout, QLineEdit, QComboBox, QTextEdit, QListWidget, QMessageBox, QHBoxLayout, QListWidgetItem, QSizePolicy)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from Functions import Dispositivo, Cable, calculate_tariff, day_tariff, dispositivo_con_mayor_suma

class ImageCarousel(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculadora de Tarifa Eléctrica")
        self.setGeometry(100, 100, 800, 800)
        self.lista_dispositivos = []
        self.selected_devices_details = {}
        self.device_items = {}

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

        self.reset_button = QPushButton("Reiniciar", self)
        self.reset_button.clicked.connect(self.reset_all)
        layout.addWidget(self.reset_button)

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

        # Botones para navegar en el carrusel
        navigation_layout = QHBoxLayout()  # Layout horizontal para los botones de navegación

        self.prev_button = QPushButton("Anterior", self)
        self.prev_button.clicked.connect(self.show_previous_image)
        navigation_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Siguiente", self)
        self.next_button.clicked.connect(self.show_next_image)
        navigation_layout.addWidget(self.next_button)

        layout.addLayout(navigation_layout)  # Agregar el layout de navegación al layout principald

        # Botón para seleccionar/des-seleccionar el dispositivo actual del carrusel
        button_layout = QVBoxLayout()  # Nuevo layout para el botón
        self.toggle_device_button = QPushButton("Agregar dispositivo", self)
        self.toggle_device_button.clicked.connect(self.toggle_dispositivo)

        # Cambia la política de tamaño del botón para que ocupe todo el espacio disponible
        self.toggle_device_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        button_layout.addWidget(self.toggle_device_button)

        # Campos para ingresar detalles del dispositivo
        form_layout = QVBoxLayout()
        self.potencia_label = QLabel("Potencia (W):", self)
        self.potencia_entry = QLineEdit(self)
        self.corriente_label = QLabel("Corriente (A):", self)
        self.corriente_entry = QLineEdit(self)
        self.hrs_dia_label = QLabel("Horas de uso por día:", self)
        self.hrs_dia_entry = QLineEdit(self)
        form_layout.addWidget(self.potencia_label)
        form_layout.addWidget(self.potencia_entry)
        form_layout.addWidget(self.corriente_label)
        form_layout.addWidget(self.corriente_entry)
        form_layout.addWidget(self.hrs_dia_label)
        form_layout.addWidget(self.hrs_dia_entry)

        # Lista para mostrar gráficamente los dispositivos seleccionados
        lista_layout = QVBoxLayout()
        self.dispositivos_lista = QListWidget(self)
        lista_layout.addWidget(QLabel("Dispositivos seleccionados:", self))
        lista_layout.addWidget(self.dispositivos_lista)

        self.dispositivos_lista.itemEntered.connect(self.show_device_details_tooltip)
        self.dispositivos_lista.itemClicked.connect(self.show_device_details_tooltip)
        self.dispositivos_lista.itemClicked.connect(self.show_device_in_carousel)

        # Layout horizontal para combinar ambos layouts verticales
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addLayout(lista_layout)
        horizontal_layout.addLayout(button_layout)  # Añade el layout del botón aquí
        horizontal_layout.addLayout(form_layout)

        layout.addLayout(horizontal_layout)

        # Botones para calcular tarifa y calibre
        self.calcular_tarifa_button = QPushButton("Calcular Tarifa", self)
        self.calcular_tarifa_button.clicked.connect(self.calcular_tarifa)
        layout.addWidget(self.calcular_tarifa_button)

        # Campo para ingresar el largo del cable
        self.largo_cable_label = QLabel("Largo del cable (m):", self)
        self.largo_cable_entry = QLineEdit(self)
        self.largo_cable_label.hide()  # Ocultar inicialmente
        self.largo_cable_entry.hide()  # Ocultar inicialmente
        layout.addWidget(self.largo_cable_label)
        layout.addWidget(self.largo_cable_entry)

        # Botón para calcular calibre
        self.calcular_calibre_button = QPushButton("Calcular Calibre", self)
        self.calcular_calibre_button.clicked.connect(self.calcular_calibre)
        self.calcular_calibre_button.hide()  # Ocultar inicialmente
        layout.addWidget(self.calcular_calibre_button)


        # Área de texto para mostrar resultados
        self.resultados_text = QTextEdit(self)
        layout.addWidget(self.resultados_text)

        main_widget.setLayout(layout)
    
    def show_device_details_tooltip(self, item):
      dispositivo_nombre = item.text()
      if dispositivo_nombre in self.selected_devices_details:
          dispositivo = self.selected_devices_details[dispositivo_nombre]
          tooltip_text = f"Potencia: {dispositivo.potencia}W\nCorriente: {dispositivo.corriente}A\nHoras: {dispositivo.hrs_dia}hrs"
          item.setToolTip(tooltip_text)

    def show_device_in_carousel(self, item):
      # Obtener el nombre del dispositivo seleccionado
      dispositivo_nombre = item.text()

      # Buscar el índice del dispositivo en la lista de nombres de dispositivos
      try:
          index = self.device_names.index(dispositivo_nombre)
      except ValueError:
          # Si el dispositivo no se encuentra en la lista, simplemente retorna
          return

      # Cambiar el índice actual y mostrar la imagen correspondiente en el carrusel
      self.current_index = index
      self.image_stack.setCurrentIndex(self.current_index)

      # Verificar si el dispositivo ya ha sido seleccionado
      if dispositivo_nombre in self.selected_devices:
          # Si el dispositivo ya está seleccionado, oculta los campos y cambia el texto del botón a "Quitar dispositivo"
          self.potencia_entry.setVisible(False)
          self.corriente_entry.setVisible(False)
          self.hrs_dia_entry.setVisible(False)
          self.toggle_device_button.setText("Quitar dispositivo")
      else:
          # Si el dispositivo no está seleccionado, muestra los campos y cambia el texto del botón a "Agregar dispositivo"
          self.potencia_entry.setVisible(True)
          self.corriente_entry.setVisible(True)
          self.hrs_dia_entry.setVisible(True)
          self.toggle_device_button.setText("Agregar dispositivo")

    def toggle_dispositivo(self):
      # Obtener el nombre del dispositivo actualmente visible
      dispositivo_nombre = self.device_names[self.current_index % len(self.device_names)]

      # Verificar si el dispositivo ya ha sido seleccionado
      if dispositivo_nombre in self.selected_devices:
          # Deseleccionar el dispositivo
          self.selected_devices.remove(dispositivo_nombre)
          self.dispositivos_lista.takeItem(self.dispositivos_lista.row(self.device_items[dispositivo_nombre]))
          del self.device_items[dispositivo_nombre]
          self.update_button_text()

          # Mostrar los campos de entrada y sus labels
          self.potencia_label.setVisible(True)
          self.potencia_entry.setVisible(True)
          self.corriente_label.setVisible(True)
          self.corriente_entry.setVisible(True)
          self.hrs_dia_label.setVisible(True)
          self.hrs_dia_entry.setVisible(True)
          self.toggle_device_button.setText("Agregar dispositivo")
      else:
          if len(self.selected_devices) < 10:
              # Verificar que los campos no estén vacíos
              if not self.potencia_entry.text():
                  QMessageBox.warning(self, "Advertencia", "Por favor, ingrese la potencia del dispositivo.")
                  return
              if not self.corriente_entry.text():
                  QMessageBox.warning(self, "Advertencia", "Por favor, ingrese la corriente del dispositivo.")
                  return
              if not self.hrs_dia_entry.text():
                  QMessageBox.warning(self, "Advertencia", "Por favor, ingrese las horas de uso del dispositivo.")
                  return
              
              # Almacenar los detalles del dispositivo
              potencia = float(self.potencia_entry.text())
              corriente = float(self.corriente_entry.text())
              hrs_dia = float(self.hrs_dia_entry.text())
              self.selected_devices_details[dispositivo_nombre] = Dispositivo(potencia, corriente, hrs_dia)

              # Continuar con la selección del dispositivo
              self.selected_devices.append(dispositivo_nombre)
              item = QListWidgetItem(dispositivo_nombre)
              item.setToolTip(f"Potencia: {potencia}W, Corriente: {corriente}A, Horas: {hrs_dia}h") 
              self.dispositivos_lista.insertItem(0, item)  # Agregar el dispositivo al inicio de la lista
              self.device_items[dispositivo_nombre] = item
              self.update_button_text()

              # Limpiar y ocultar los campos de entrada y sus labels
              self.potencia_label.setVisible(False)
              self.potencia_entry.clear()
              self.potencia_entry.setVisible(False)
              self.corriente_label.setVisible(False)
              self.corriente_entry.clear()
              self.corriente_entry.setVisible(False)
              self.hrs_dia_label.setVisible(False)
              self.hrs_dia_entry.clear()
              self.hrs_dia_entry.setVisible(False)
              self.toggle_device_button.setText("Quitar dispositivo")
          else:
              QMessageBox.warning(self, "Advertencia", "Has alcanzado el límite de 10 dispositivos.")


    def agregar_dispositivo(self):
      # Obtener el nombre del dispositivo actualmente visible
      dispositivo_nombre = self.device_names[self.current_index % len(self.device_names)]
      if len(self.selected_devices) < 10:
          self.dispositivos_lista.insertItem(0, dispositivo_nombre)
          self.selected_devices.append(dispositivo_nombre)
          self.toggle_device_button.setText("Quitar dispositivo")
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

    def update_input_fields_visibility(self):
      dispositivo_nombre = self.device_names[self.current_index % len(self.device_names)]
      if dispositivo_nombre in self.selected_devices:
          self.potencia_entry.setVisible(False)
          self.corriente_entry.setVisible(False)
          self.hrs_dia_entry.setVisible(False)
          self.potencia_label.setVisible(False)
          self.corriente_label.setVisible(False)
          self.hrs_dia_label.setVisible(False)
      else:
          self.potencia_entry.setVisible(True)
          self.corriente_entry.setVisible(True)
          self.hrs_dia_entry.setVisible(True)
          self.potencia_label.setVisible(True)
          self.corriente_label.setVisible(True)
          self.hrs_dia_label.setVisible(True)


    def show_previous_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.image_stack.setCurrentIndex(self.current_index)
            self.update_button_text()
            self.update_input_fields_visibility()

    def show_next_image(self):
        if self.current_index < len(self.image_paths) * 7 - 1:  # Ajuste para las 20 imágenes
            self.current_index += 1
            self.image_stack.setCurrentIndex(self.current_index)
            self.update_button_text()
            self.update_input_fields_visibility()

    def update_button_text(self):
      # Obtener el nombre del dispositivo actualmente visible
      dispositivo_nombre = self.device_names[self.current_index % len(self.device_names)]
      
      if dispositivo_nombre in self.selected_devices:
          self.toggle_device_button.setText("Quitar dispositivo")
          
          # Ocultar los campos y etiquetas
          self.potencia_label.hide()
          self.potencia_entry.hide()
          self.corriente_label.hide()
          self.corriente_entry.hide()
          self.hrs_dia_label.hide()
          self.hrs_dia_entry.hide()
      else:
          self.toggle_device_button.setText("Agregar dispositivo")
          
          # Mostrar los campos y etiquetas
          self.potencia_label.show()
          self.potencia_entry.show()
          self.corriente_label.show()
          self.corriente_entry.show()
          self.hrs_dia_label.show()
          self.hrs_dia_entry.show()


    def calcular_tarifa(self):
      dispositivos_seleccionados = [Dispositivo(item.potencia, item.corriente, item.hrs_dia) for item in self.selected_devices_details.values()]
      total_tarifa = day_tariff(dispositivos_seleccionados)
      self.resultados_text.append(f"Tarifa total por día para todos los dispositivos: Q {total_tarifa:.2f} (Tarifa social: Q 2.356041)")

      # Calcular el dispositivo con la mayor suma de potencia y corriente
      dispositivo_mayor = dispositivo_con_mayor_suma(dispositivos_seleccionados)
      if dispositivo_mayor:
          # Buscar el nombre del dispositivo con la mayor suma
          nombre_dispositivo_mayor = next((nombre for nombre, dispositivo in self.selected_devices_details.items() if dispositivo.potencia == dispositivo_mayor.potencia and dispositivo.corriente == dispositivo_mayor.corriente), None)
          
          self.resultados_text.append("\nDispositivo con la mayor suma de potencia y corriente: " + (nombre_dispositivo_mayor if nombre_dispositivo_mayor else "(Desconocido)"))
          self.resultados_text.append(f"Potencia: {dispositivo_mayor.potencia} W")
          self.resultados_text.append(f"Corriente: {dispositivo_mayor.corriente} A")
      
      # Mostrar el campo para ingresar el largo del cable y el botón para calcular calibre
      self.largo_cable_label.show()
      self.largo_cable_entry.show()
      self.calcular_calibre_button.show()

      # Ajustar el tamaño de la ventana
      self.resize(self.width(), self.height() + 200)  # Aumentar el alto en 100 pixels

      self.dispositivo_mayor = dispositivo_mayor


    def calcular_calibre(self):
      try:
          # Capturar el valor ingresado por el usuario
          largo_cable = float(self.largo_cable_entry.text())
      except ValueError:
          QMessageBox.warning(self, "Advertencia", "Por favor, ingrese un valor válido para el largo del cable.")
          return

      # Usar el dispositivo de mayor suma de potencia y corriente para calcular el calibre del cable
      dispositivo_mayor = self.dispositivo_mayor
      cable = Cable(largo_cable, dispositivo_mayor)

      # Mostrar el resultado en el área de texto
      self.resultados_text.append(f"\nDiámetro del cable: {cable.diametro:.2f} mm")
      self.resultados_text.append(f"Calibre del cable: {cable.calibre}")

    def reset_all(self):
      # Limpiar la lista de dispositivos seleccionados
      self.selected_devices.clear()
      self.selected_devices_details.clear()
      self.dispositivos_lista.clear()
      self.device_items.clear()

      # Restablecer el índice del carrusel
      self.current_index = 0
      

      # Limpiar y ocultar los campos de entrada y sus labels
      self.potencia_label.setVisible(True)
      self.potencia_entry.clear()
      self.potencia_entry.setVisible(True)
      self.corriente_label.setVisible(True)
      self.corriente_entry.clear()
      self.corriente_entry.setVisible(True)
      self.hrs_dia_label.setVisible(True)
      self.hrs_dia_entry.clear()
      self.hrs_dia_entry.setVisible(True)

      # Restablecer el texto del botón
      self.toggle_device_button.setText("Agregar dispositivo")

      # Restablecer largo del cable
      self.largo_cable_entry.clear()
      self.largo_cable_label.hide()
      self.largo_cable_entry.hide()
       
      # Restablecer el tamaño de la ventana
      self.resize(self.width(), 800)

      # Limpiar area de resultados
      self.resultados_text.clear()




    






if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageCarousel()
    window.show()
    sys.exit(app.exec())
