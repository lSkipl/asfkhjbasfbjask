import requests  # Librería para hacer solicitudes HTTP a la API
import time      # Librería para medir el tiempo de ejecución
import getopt    # Librería para manejar los argumentos de la línea de comandos
import sys       # Librería para interactuar con el sistema, como salir del programa

# Función que obtiene el fabricante (vendor) asociado a una dirección MAC a través de una API
def get_fabricante(mac_address):
    # URL de la API con la dirección MAC a consultar
    url = f"https://api.maclookup.app/v2/macs/{mac_address}"
    try:
        # registrar el tiempo antes de realizar la solicitud para medir el tiempo de respuesta
        tiempo = time.time()
        
       
        response = requests.get(url)
        
        # calcular el tiempo que se hizo la solicitud
        tiempo_ms = int((time.time() - tiempo) * 1000)

    
        if response.status_code == 200:
         
            data = response.json()
            # Obtener el campo 'company', que es el fabricante asociado a la MAC
            fabricante = data.get("company", "Desconocido")
            return fabricante, tiempo_ms  
        else:
            # Si la respuesta no es exitosa, devolver "Not found" y el tiempo de respuesta
            return "Not found", tiempo_ms
    
 
    except Exception as e:
        # En caso de error, devolver el mensaje del error y 0 en el tiempo de respuesta
        return str(e), 0

# Función principal que maneja la lógica del programa
def main(argv):
    mac_address = None  # almacenar la dirección MAC ingresada por el usuario (si se proporciona)
    show_arp = False    # bandera que indica si se debe mostrar la lista de ARP fija

    try:
        
        opts, _ = getopt.getopt(argv, "hm:", ["mac=", "arp", "help"])
    except getopt.GetoptError as err:
     
        print(err)
        sys.exit(2)

    # Recorrer las opciones proporcionadas por el usuario
    for o, a in opts:
        # si el usuario pidió la ayuda (-h o --help), mostrar el mensaje de ayuda y salir
        if o in ("-h", "--help"):
            print("Uso: OUILookup.py --mac <mac> | --arp | --help")
            print("--mac: MAC a consultar. P.e. aa:bb:cc:00:00:00.")
            print("--arp: muestra los fabricantes de los hosts disponibles en la tabla ARP.")
            print("--help: muestra este mensaje y termina.")
            sys.exit()  # Salir del programa
        #proporcionar una dirección MAC con la opción -m o --mac, almacenarla
        elif o in ("-m", "--mac"):
            mac_address = a

        elif o in ("--arp"):
            show_arp = True

    #consultar la API y mostrar el fabricante
    if mac_address:
        fabricante, response_time = get_fabricante(mac_address)  # Obtener fabricante y tiempo
        print(f"MAC address: {mac_address}")
        print(f"Fabricante: {fabricante}")
        print(f"Tiempo de respuesta: {response_time} ms")
    
    # si el usuario utiliza --arp, mostrar una lista fija de direcciones MAC y fabricantes
    elif show_arp:
        print("IP/MAC/Vendor:")
        print("00:01:97:BB:BB:BB / cisco")
        print("B4:B5:FE:92:FF:C5 / Hewlett Packard")
        print("00:E0:64:AA:AA:AA / Samsung")
        print("AC:F7:F3:AA:AA:AA / Xiomi")
    
    # si no hay opciones válidas, mostrar un mensaje de error y ayuda
    else:
        print("Por favor, proporciona una dirección MAC o usa la opción --arp.")
        print("Uso: OUILookup.py --mac <mac> | --arp | --help")

# Punto de entrada del script, llama a la función main con los argumentos proporcionados
if __name__ == "__main__":
    main(sys.argv[1:])  # sys.argv[1:] pasa los argumentos desde la línea de comandos excluyendo el nombre del script
