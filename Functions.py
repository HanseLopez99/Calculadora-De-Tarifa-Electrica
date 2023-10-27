import math 


#Clase
class Dispositivo:
    def __init__(self, potencia, largo, corriente, hrs_dia):
        self.potencia = float(potencia)
        self.largo = float(largo)
        self.corriente = float(corriente)
        self.diametro = self.calculate_diametro()
        self.calibre = self.calculate_calibre()
        self.hrs_dia = float(hrs_dia)

    #Función para calcular el diametro
    def calculate_diametro(self):
        resistividad = 1.72 * 10**-8 #Se asume que el cable es de cobre.
        radio = ((self.largo * resistividad * self.corriente**2) / (math.pi * self.potencia))**0.5
        diametro = radio * 2
        return diametro

    
    #Funcion para calcular el calibre
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


#Funcion para calcular la tarifa a pagar por día de un dispositivo 
dispositivo = Dispositivo(100.5, 50.0, 10.2, 4)
def calculate_tariff(dispositivo):
    price = 0.2 #Esta linea hay que cambiarla 
    tariff_perDay = price * dispositivo.potencia * 10**-3 * dispositivo.hrs_dia
    return tariff_perDay
    
    
#Funcion para calcular la tarifa a pagar por día de una serie de dispositivos
estufa = Dispositivo(100.5, 50.0, 10.2, 4)
batidora = Dispositivo(50.5, 26.0, 5.2, 1)
dipositivos_list = [estufa, batidora]

def day_tariff(lista):
    total = 0.0
    for dispositivo in lista:
        tariff_perDay = calculate_tariff(dispositivo) 
        total = total + tariff_perDay
    return total
        
        











  


    

