# ==========================================
# Checker Premium M3U - IMHO PRO REAL
# Desarrollador: IMHOTEP
# ==========================================

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from datetime import datetime
import os

# Colores ANSI
ROJO = "\033[91m"
AZUL = "\033[94m"
BLANCO = "\033[97m"
RESET = "\033[0m"

HEADERS = {
    "User-Agent": "IMHO Checker Premium"
}

def limpiar():
    os.system("clear" if os.name != "nt" else "cls")

def banner():
    print(AZUL + """
██╗███╗   ███╗██╗  ██╗ ██████╗ 
██║████╗ ████║██║  ██║██╔═══██╗
██║██╔████╔██║███████║██║   ██║
██║██║╚██╔╝██║██╔══██║██║   ██║
██║██║ ╚═╝ ██║██║  ██║╚██████╔╝
╚═╝╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ 
""" + RESET)

    print(BLANCO + "        IMHO M3U CHECKER PRO\n" + RESET)
    print(ROJO + "        Desarrollador: IMHOTEP\n" + RESET)

def cargar_m3u(ruta):
    enlaces = []
    with open(ruta, "r", encoding="utf-8", errors="ignore") as f:
        for linea in f:
            if linea.startswith("http"):
                enlaces.append(linea.strip())
    return enlaces

def verificar(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=5, stream=True)
        return url, r.status_code == 200
    except:
        return url, False

def checker(ruta, hilos):
    enlaces = cargar_m3u(ruta)
    total = len(enlaces)

    print(BLANCO + f"\nTotal: {total} enlaces")
    print(AZUL + f"Hilos: {hilos}\n" + RESET)

    activos, caidos = [], []

    inicio = time.time()

    with ThreadPoolExecutor(max_workers=hilos) as executor:
        futures = [executor.submit(verificar, url) for url in enlaces]

        for i, future in enumerate(as_completed(futures), 1):
            url, ok = future.result()

            if ok:
                print(AZUL + "[OK]" + BLANCO, url)
                activos.append(url)
            else:
                print(ROJO + "[FAIL]" + BLANCO, url)
                caidos.append(url)

            print(f"{BLANCO}Progreso: {i}/{total}{RESET}", end="\r")

    fin = time.time()

    tiempo = round(fin - inicio, 2)
    porcentaje = (len(activos) / total * 100) if total > 0 else 0

    guardar_reporte(activos, caidos, total, tiempo, porcentaje)

    print(AZUL + "\n\n✔ Escaneo finalizado" + RESET)
    print(BLANCO + f"Activos: {len(activos)}")
    print(ROJO + f"Caídos: {len(caidos)}")
    print(AZUL + f"Efectividad: {round(porcentaje,2)}%" + RESET)
    print(BLANCO + "Archivo generado: resultado.txt\n")

def guardar_reporte(activos, caidos, total, tiempo, porcentaje):
    with open("resultado.txt", "w", encoding="utf-8") as f:
        f.write("=====================================\n")
        f.write(" IMHO CHECKER PREMIUM M3U\n")
        f.write(" Desarrollador: IMHOTEP\n")
        f.write("=====================================\n\n")

        f.write(f"Fecha: {datetime.now()}\n")
        f.write(f"Total: {total}\n")
        f.write(f"Activos: {len(activos)}\n")
        f.write(f"Caídos: {len(caidos)}\n")
        f.write(f"Efectividad: {round(porcentaje,2)}%\n")
        f.write(f"Tiempo: {tiempo}s\n\n")

        f.write("===== ACTIVOS =====\n")
        for url in activos:
            f.write(url + "\n")

        f.write("\n===== CAÍDOS =====\n")
        for url in caidos:
            f.write(url + "\n")

def menu():
    while True:
        limpiar()
        banner()

        print(BLANCO + "1. Iniciar Checker")
        print("2. Salir\n" + RESET)

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            ruta = input("Ruta del archivo M3U: ")
            hilos = input("Número de hilos (20-100 recomendado): ")

            try:
                hilos = int(hilos)
            except:
                hilos = 50

            checker(ruta, hilos)
            input("\nPresiona ENTER para continuar...")

        elif opcion == "2":
            break

        else:
            print("Opción inválida")
            time.sleep(1)

if __name__ == "__main__":
    menu()