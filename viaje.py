import math

# Base de datos de ciudades con sus coordenadas
CIUDADES = {
    "santiago": {"nombre": "Santiago (Chile)", "lat": -33.4489, "lon": -70.6693},
    "arica": {"nombre": "Arica (Chile)", "lat": -18.4746, "lon": -70.2979},
    "lima": {"nombre": "Lima (Perú)", "lat": -12.0464, "lon": -77.0428},
    "tacna": {"nombre": "Tacna (Perú)", "lat": -18.0117, "lon": -70.2536}
}

# Opciones de transporte y sus velocidades promedios
TRANSPORTES = {
    "1": {"tipo": "Avión", "velocidad": 800},
    "2": {"tipo": "Autobús", "velocidad": 90}
}

def calcular_distancia_haversine(lat1, lon1, lat2, lon2):
    """Calcula la distancia geométrica real entre dos coordenadas en km"""
    radio_tierra = 6371.0
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radio_tierra * c

def ejecutar_sistema():
    while True:
        print("\n" + "="*50)
        print("    SISTEMA DE PLANIFICACIÓN DE VIAJES CHILE - PERÚ")
        print("="*50)
        print("Ciudades en sistema: Santiago, Arica, Lima, Tacna")
        print("Para salir en cualquier momento, presione 's'.")
        print("-"*50)

        # 1. Solicitar Ciudad de Origen
        origen_input = input("Ciudad de Origen: ").strip().lower()
        if origen_input == 's':
            print("Saliendo del programa. ¡Buen viaje!")
            break
        
        # 2. Solicitar Ciudad de Destino
        destino_input = input("Ciudad de Destino: ").strip().lower()
        if destino_input == 's':
            print("Saliendo del programa. ¡Buen viaje!")
            break

        # Validar existencia de las ciudades
        if origen_input not in CIUDADES or destino_input not in CIUDADES:
            print("[Error]: Una o ambas ciudades no están registradas. Intente de nuevo.")
            continue

        # 3. Elegir medio de transporte
        print("\nSeleccione su medio de transporte:")
        for clave, datos in TRANSPORTES.items():
            print(f" {clave}) {datos['tipo']} ({datos['velocidad']} km/h)")
        
        transporte_input = input("Opción: ").strip()
        if transporte_input == 's':
            print("Saliendo del programa. ¡Buen viaje!")
            break
            
        if transporte_input not in TRANSPORTES:
            print("[Error]: Opción de transporte inválida.")
            continue

        # --- PROCESAMIENTO DE DATOS ---
        ciudad_origen = CIUDADES[origen_input]
        ciudad_destino = CIUDADES[destino_input]
        transporte_elegido = TRANSPORTES[transporte_input]

        # Cálculo automático de distancias
        distancia_km = calcular_distancia_haversine(
            ciudad_origen["lat"], ciudad_origen["lon"], 
            ciudad_destino["lat"], ciudad_destino["lon"]
        )
        distancia_millas = distancia_km * 0.621371

        # Cálculo del tiempo estimado (Horas y Minutos)
        tiempo_horas_decimal = distancia_km / transporte_elegido["velocidad"]
        horas = int(tiempo_horas_decimal)
        minutos = int((tiempo_horas_decimal - horas) * 60)

        # --- MOSTRAR RESULTADOS REQUERIDOS ---
        print("\n" + "-"*50)
        print(f" VIAJE: {ciudad_origen['nombre']} ➔ {ciudad_destino['nombre']}")
        print("-"*50)
        print(f"Distancia en Kilómetros : {distancia_km:.2f} km")
        print(f"Distancia en Millas      : {distancia_millas:.2f} mi")
        print(f"Duración del viaje       : {horas} horas y {minutos} minutos ({transporte_elegido['tipo']})")
        print("-"*50)
        
        # Narrativa del viaje
        print("NARRATIVA DEL VIAJE:")
        print(f"Su travesía iniciará en {ciudad_origen['nombre']}. Utilizando como medio de ")
        print(f"transporte un {transporte_elegido['tipo'].lower()}, avanzará cruzando fronteras rumbo a ")
        print(f"{ciudad_destino['nombre']}. Durante este trayecto habrá completado un recorrido total ")
        print(f"de {distancia_km:.2f} kilómetros, tomándole un tiempo aproximado de {horas}h y {minutos}m.")
        print("="*50)

        # Opción de reiniciar ciclo o salir
        print("\n[Presione Enter para calcular otro viaje o 's' para salir]")
        control = input().strip().lower()
        if control == 's':
            print("Saliendo del programa. ¡Buen viaje!")
            break

if __name__ == "__main__":
    ejecutar_sistema()
