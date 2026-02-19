import os
import csv
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client

def obtener_cliente() -> Client:
    # Conexion basica a Supabase usando variables de entorno
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise ValueError("Faltan las variables en el archivo .env")
    return create_client(url, key)

def realizar_backup():
    try:
        cliente = obtener_cliente()
    except ValueError as e:
        print(e)
        return

    # Definimos el nombre del archivo de texto que contendra la lista de tablas
    archivo_tablas = 'tables_list.txt'
    
    # Validamos que el archivo exista antes de continuar
    if not os.path.exists(archivo_tablas):
        print(f"Error: Crea un archivo llamado '{archivo_tablas}' con los nombres de las tablas, uno por linea.")
        return

    # Abrimos el archivo y leemos cada linea limpiando espacios en blanco
    with open(archivo_tablas, 'r') as f:
        tablas = [linea.strip() for linea in f if linea.strip()]

    # Si el archivo existe pero esta vacio, detenemos el proceso
    if not tablas:
        print("No hay tablas para descargar en el archivo de texto.")
        return

    # Generamos un nombre de carpeta unico usando la fecha y hora actual (ej. BACKUP_20260219_153000)
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    directorio = os.path.join(os.getcwd(), f"BACKUP_{fecha}")
    
    # Creamos la carpeta
    os.makedirs(directorio, exist_ok=True)
    print(f"Iniciando respaldo en la nueva carpeta: {directorio}")

    # Iteramos por cada tabla que encontramos en el archivo de texto
    for tabla in tablas:
        print(f"Descargando tabla: {tabla}...")
        try:
            # Hacemos un SELECT * de la tabla completa
            respuesta = cliente.table(tabla).select("*").execute()
            datos = respuesta.data

            # Si la base de datos responde vacio, lo avisamos y pasamos a la siguiente tabla
            if not datos:
                print(f"La tabla {tabla} esta vacia o no tienes permisos para leerla.")
                continue

            # Creamos la ruta del archivo CSV (ej. BACKUP_2026.../usuarios.csv)
            ruta_csv = os.path.join(directorio, f"{tabla}.csv")
            
            # Abrimos el archivo CSV en modo escritura
            with open(ruta_csv, 'w', newline='', encoding='utf-8') as archivo_csv:
                # Extraemos los nombres de las columnas usando las llaves del primer registro
                columnas = datos[0].keys()
                
                # Configuramos el escritor de CSV
                escritor = csv.DictWriter(archivo_csv, fieldnames=columnas)
                
                # Escribimos la cabecera (nombres de columnas)
                escritor.writeheader()
                # Escribimos todas las filas de la base de datos
                escritor.writerows(datos)
                
            print(f"Guardado exitoso: {len(datos)} registros exportados de la tabla '{tabla}'.")
            
        except Exception as e:
            # Capturamos cualquier error (como tablas que no existen) para que el script no se caiga
            print(f"Error descargando {tabla}: {e}")

if __name__ == "__main__":
    realizar_backup()
