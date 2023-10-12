import serial.tools.list_ports

def verificar_portas_arduino():
    # Obtém uma lista de todas as portas seriais disponíveis
    portas_disponiveis = list(serial.tools.list_ports.comports())

    portas_arduino = []
    
    for porta in portas_disponiveis:
        print(porta.device)
        # Verifica se a descrição da porta contém a palavra "Arduino"
        if "Arduino" in porta.description:
            portas_arduino.append(porta.device)

    if portas_arduino:
        print("Portas Arduino encontradas:")
        for porta in portas_arduino:
            print(porta)
    else:
        print("Nenhuma porta Arduino encontrada.")

if __name__ == "__main__":
    verificar_portas_arduino()
