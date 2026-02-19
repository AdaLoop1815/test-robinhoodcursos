# Herramientas de Administración de Supabase

Este repositorio contiene los scripts necesarios para realizar respaldos de una base de datos en Supabase y para gestionar la creación y configuración de cuentas de administrador con suscripción de por vida.

## Requisitos previos

Antes de ejecutar los scripts, asegúrate de tener instaladas las dependencias necesarias. Puedes instalarlas ejecutando:

pip install supabase python-dotenv

## Configuración inicial

1. Crea un archivo llamado `.env` en la misma carpeta que los scripts.
2. Agrega tus credenciales de Supabase en el archivo `.env` con el siguiente formato:

SUPABASE_URL=tu_url_de_supabase
SUPABASE_KEY=tu_api_key_de_supabase

## Uso de los scripts

### 1. Gestionar Usuarios (gestor_usuarios.py)
Este script se utiliza para crear una nueva cuenta o iniciar sesión en una existente, darle permisos de administrador en la base de datos y asignarle una suscripción activa hasta el año 2099 en la tabla de perfiles.

**Cómo usarlo:**
Ejecuta el script en la terminal con `python gestor_usuarios.py`. Te pedirá que ingreses el correo y la contraseña directamente en la consola. El script se encargará de realizar las autenticaciones y las actualizaciones de permisos automáticamente.

### 2. Respaldo de Base de Datos (backup_supabase.py)
Este script lee una lista de tablas especificada por ti y las descarga localmente en archivos CSV dentro de una carpeta marcada con la fecha y hora actuales.

**Cómo usarlo:**
1. Crea un archivo de texto llamado `tables_list.txt` en la misma carpeta.
2. Escribe el nombre exacto de cada tabla que deseas respaldar, colocando un solo nombre por línea.
3. Ejecuta el script con `python backup_supabase.py`. Automáticamente se creará una carpeta nueva con todos los archivos descargados.

### 3. Crear Usuarios de Prueba (crear_usuario.py)
Este script genera automáticamente un correo electrónico aleatorio y registra una nueva cuenta en la base de datos de Supabase. Es ideal para crear cuentas de prueba rápidamente antes de asignarles permisos o suscripciones.

**Cómo usarlo:**
1. Asegúrate de tener tu archivo `.env` configurado.
2. Ejecuta el script en la terminal usando el comando: `python crear_usuario.py`
3. El programa imprimirá en la consola el correo generado, la contraseña por defecto y el ID único del usuario. Copia estos datos si necesitas pasarlos por los otros scripts de configuración o elevación de permisos.

