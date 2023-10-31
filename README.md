# Calculadora de Tarifa Eléctrica

Este proyecto permite calcular la tarifa eléctrica diaria basada en la potencia, corriente y horas de uso de distintos dispositivos eléctricos. La interfaz gráfica permite al usuario seleccionar dispositivos de un carrusel, ingresar sus detalles y visualizar la tarifa total y el dispositivo con la mayor suma de potencia y corriente.

## Requisitos

- Python 3.8 o superior.
- Bibliotecas externas: `PyQt5`. Puedes instalarlo con:
  ```bash
  pip install PyQt5

## Inicialización

1. Clona este repositorio en tu computadora local o descarga los archivos fuente.
2. Asegúrate de tener todas las bibliotecas mencionadas en "Requisitos" instaladas.
3. Navega hasta la carpeta del proyecto en tu terminal o línea de comandos.

## Correr el Proyecto

Desde la línea de comandos o terminal, simplemente ejecuta:
   
   ```bash
   python [nombre-del-archivo-principal].py
   ```


Por supuesto, reemplaza `[nombre-del-archivo-principal]` con el nombre del archivo Python principal que contiene la interfaz gráfica y las funciones de cálculo, en este caso `main.py`.

## Uso

1. **Selección de Dispositivo**: Navega entre los dispositivos disponibles en el carrusel utilizando los botones "Anterior" y "Siguiente".
2. **Ingreso de Detalles del Dispositivo**:
   - **Potencia (W)**: Ingresa la potencia del dispositivo en watts.
   - **Corriente (A):**: Ingresa la corriente del dispositivo en amperios.
    - **Horas de Uso (h)**: Ingresa la cantidad de horas que el dispositivo estará encendido.
3. **Cálculo y Visualización**:
   - Haz clic en el botón "Calcular Tarifa" para obtener la tarifa total diaria y el dispositivo con la mayor suma de potencia y corriente.
   - Observa los resultados en la sección de texto inferior.