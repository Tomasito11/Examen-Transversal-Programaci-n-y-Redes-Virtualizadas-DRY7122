def evaluar_asn(asn):
    # Validar límites superiores e inferiores de 32 bits
    if asn < 0 or asn > 4294967295:
        return "Inválido (Fuera del rango estándar de BGP)"
    
    # Casos reservados por la IANA
    elif asn == 0 or asn == 65535 or asn == 4294967295:
        return "Reservado"
    
    # Rangos Privados (16 bits: 64512-65534 y 32 bits: 4200000000-4294967294)
    elif (64512 <= asn <= 65534) or (4200000000 <= asn <= 4294967294):
        return "Privado"
    
    # Por descarte, los demás números asignados son públicos
    else:
        return "Público"

def main():
    print("--- Verificador de ASN de BGP ---")
    try:
        user_input = input("Introduce el número de AS: ")
        as_number = int(user_input)
        
        resultado = evaluar_asn(as_number)
        print(f"El AS {as_number} se clasifica como: {resultado}")
        
    except ValueError:
        print("Error: Debes introducir un número entero válido.")

if __name__ == "__main__":
    main()
