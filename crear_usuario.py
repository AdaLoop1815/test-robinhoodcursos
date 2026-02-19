import os
import random
import string
from dotenv import load_dotenv
from supabase import create_client, Client

def obtener_cliente() -> Client:
    # Cargamos las variables ocultas desde el archivo .env
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    # Validamos que las credenciales existan para no tener errores raros despues
    if not url or not key:
        raise ValueError("Error: Faltan SUPABASE_URL o SUPABASE_KEY en el archivo .env")
    
    # Retornamos la conexion activa a Supabase
    return create_client(url, key)

def generar_correo_aleatorio():
    # Creamos una lista de letras minusculas y numeros
    caracteres = string.ascii_lowercase + string.digits
    
    # Elegimos 10 caracteres al azar y los unimos en un solo texto
    nombre_usuario = ''.join(random.choice(caracteres) for _ in range(10))
    
    # Le damos formato de correo electronico
    return f"admin_test_{nombre_usuario}@example.com"

def crear_usuario_prueba():
    # Intentamos conectarnos a la base de datos
    try:
        cliente = obtener_cliente()
    except ValueError as e:
        print(e)
        return

    # Preparamos los datos del nuevo usuario
    correo = generar_correo_aleatorio()
    contrasena = "SuperSecretPassword123!"

    print("--- Creador de Usuarios de Prueba ---")
    print(f"Intentando registrar el correo: {correo}")

    try:
        # Usamos el metodo sign_up de Supabase para registrar la cuenta en el sistema de autenticacion
        respuesta = cliente.auth.sign_up({
            "email": correo,
            "password": contrasena
        })
        
        # Extraemos los datos del usuario recien creado
        usuario = respuesta.user
        
        # Si Supabase nos devuelve un usuario, significa que se creo correctamente
        if usuario:
            print("Registro completado con exito.")
            print(f"ID de Usuario: {usuario.id}")
            print(f"Correo generado: {correo}")
            print(f"Contrasena: {contrasena}")
            print("Guarda estos datos para iniciar sesion o darle permisos luego.")
        else:
            # Esto pasa si tu Supabase exige confirmar el correo antes de crear el usuario
            print("El registro se ejecuto, pero no se obtuvo una sesion.")
            print("Nota: Verifica si tienes activada la confirmacion por correo en Supabase.")
            
    except Exception as e:
        print(f"Fallo al crear el usuario: {e}")

# Este bloque asegura que el codigo solo corra si ejecutamos este archivo directamente
if __name__ == "__main__":
    crear_usuario_prueba()
