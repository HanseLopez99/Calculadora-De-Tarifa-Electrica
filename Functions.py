import math

# Clase Dispositivo
class Dispositivo:
    def __init__(self, potencia, corriente, hrs_dia):
        self.potencia = float(potencia)
        self.corriente = float(corriente)
        self.hrs_dia = float(hrs_dia)

# Clase Cable
class Cable:
    def __init__(self, largo, dispositivo):
        self.largo = float(largo)
        self.dispositivo = dispositivo
        self.diametro = self.calculate_diametro()
        self.calibre = self.calculate_calibre()
    
    def calculate_diametro(self):
        resistividad = 1.72 * 10**-8  # Se asume que el cable es de cobre.
        radio = ((self.largo * resistividad * self.dispositivo.corriente**2) / (math.pi * self.dispositivo.potencia))**0.5
        diametro = radio * 2
        return diametro
    
    def calculate_calibre(self):
        if 0.163 <= self.diametro < 0.205:
            return 14
        elif 0.205 <= self.diametro < 0.259:
            return 12
        elif 0.259 <= self.diametro < 0.326:
            return 10
        elif 0.326 <= self.diametro < 0.412:
            return 8
        elif 0.412 <= self.diametro < 0.462:
            return 6
        elif 0.462 <= self.diametro < 0.519:
            return 5
        elif 0.519 <= self.diametro < 1:
            return 4
        return None  # O algún otro valor por defecto

# Función para calcular la tarifa a pagar por día de un dispositivo
def calculate_tariff(dispositivo):
    price = 0.2
    tariff_per_day = price * dispositivo.potencia * 10**-3 * dispositivo.hrs_dia
    return tariff_per_day

# Función para calcular la tarifa a pagar por día de una serie de dispositivos
def day_tariff(dispositivos):
    total = 0.0
    for dispositivo in dispositivos:
        tariff_per_day = calculate_tariff(dispositivo)
        total += tariff_per_day
    return total

# Función para encontrar el dispositivo con la mayor suma de potencia y corriente
def dispositivo_con_mayor_suma(dispositivos):
    if not dispositivos:
        return None

    dispositivo_mayor = dispositivos[0]
    suma_mayor = dispositivo_mayor.potencia + dispositivo_mayor.corriente

    for dispositivo in dispositivos[1:]:
        suma_actual = dispositivo.potencia + dispositivo.corriente
        if suma_actual > suma_mayor:
            dispositivo_mayor = dispositivo
            suma_mayor = suma_actual

    return dispositivo_mayor

# Ejemplo de aplicación
dispositivo_a = Dispositivo(100.5, 10.2, 4)
dispositivo_b = Dispositivo(150.3, 15.5, 6)
dispositivo_c = Dispositivo(120.0, 12.0, 5)

lista_dispositivos = [dispositivo_a, dispositivo_b, dispositivo_c]

# Calcular la tarifa total por día para todos los dispositivos
tarifa_total = day_tariff(lista_dispositivos)
print("Tarifa total por día para todos los dispositivos:", tarifa_total)

# Encontrar el dispositivo con la mayor suma de potencia y corriente
dispositivo_mayor = dispositivo_con_mayor_suma(lista_dispositivos)
print("Dispositivo con la mayor suma de potencia y corriente:")
print("Potencia:", dispositivo_mayor.potencia)
print("Corriente:", dispositivo_mayor.corriente)

# Crear un objeto Cable y calcular su diámetro y calibre
cable = Cable(50, dispositivo_mayor)
print("Diámetro del cable:", cable.diametro)
print("Calibre del cable:", cable.calibre)














  


    

