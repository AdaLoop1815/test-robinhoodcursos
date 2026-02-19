import os
from dotenv import load_dotenv
from supabase import create_client, Client

def obtener_cliente() -> Client:
    # Inicializamos la conexion a Supabase usando el .env
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise ValueError("Faltan las variables SUPABASE_URL y SUPABASE_KEY en el archivo .env")
    return create_client(url, key)

def configurar_cuenta(email, password):
    cliente = obtener_cliente()
    print(f"Iniciando configuracion para la cuenta: {email}")
    
    # --- PASO 1: Autenticacion ---
    try:
        print("Autenticando usuario...")
        # Primero intentamos crear la cuenta por si no existe
        respuesta = cliente.auth.sign_up({"email": email, "password": password})
        
        # Si no nos devuelve usuario (porque ya existe o pide confirmacion), forzamos el login
        if not respuesta.user:
            respuesta = cliente.auth.sign_in_with_password({"email": email, "password": password})
        
        # Guardamos el ID unico del usuario porque lo usaremos en los siguientes pasos
        user_id = respuesta.user.id
        print(f"Usuario autenticado correctamente con ID: {user_id}")
    except Exception as e:
        print(f"Error critico en autenticacion: {e}")
        return # Si falla el login, detenemos todo el script

    # --- PASO 2: Permisos de Administrador ---
    try:
        print("Otorgando permisos de administrador...")
        # Llamamos a una funcion remota (RPC) creada en Supabase llamada 'update_user_role'
        # Le pasamos el ID del usuario y el rol que queremos darle
        cliente.rpc('update_user_role', {'user_id': user_id, 'role': 'admin'}).execute()
        print("Permisos concedidos correctamente.")
    except Exception as e:
        # Si esto falla, puede ser porque la funcion RPC no existe o no tenemos permisos
        print(f"Nota en elevacion de permisos: {e}")

    # --- PASO 3: Activar Suscripcion de por vida ---
    try:
        print("Activando suscripcion Lifetime...")
        # Preparamos los datos tal cual los espera la tabla 'profiles'
        actualizaciones = {
            "is_paid": True,
            "is_active": True,
            "plan_name": "Lifetime",
            "subscription_expires_at": "2099-12-31T23:59:59.999Z" # Fecha muy lejana
        }
        
        # Hacemos un UPDATE en la tabla 'profiles' donde el ID coincida con nuestro usuario
        cliente.table('profiles').update(actualizaciones).eq('id', user_id).execute()
        print("Suscripcion Lifetime activada con exito.")
    except Exception as e:
        print(f"Error al activar suscripcion: {e}")

if __name__ == "__main__":
    # Pedimos al usuario que ingrese los datos manualmente en la consola
    correo = input("Ingresa el correo del usuario: ")
    clave = input("Ingresa la contrasena: ")
    configurar_cuenta(correo, clave)
