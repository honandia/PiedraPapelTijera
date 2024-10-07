# Piedra, Papel o Tijera

La aplicación está desarrollada en Python utilizando FastAPI y SQLAlchemy para la gestión de las partidas y jugadores.

## Características
- **Modo humano vs máquina**: El jugador elige entre piedra, papel o tijera y compite contra la máquina.
- **Modo máquina vs máquina**: Dos máquinas juegan entre sí durante un número definido de partidas.
- **Gestión de jugadores y partidas**: Los datos de las partidas y jugadores se guardan en una base de datos para análisis posterior.
- **Estadísticas**: Información global de partidas, ranking de jugadores, mano más fuerte y más débil.
- **Logging**: Registro detallado de las acciones y resultados de las partidas.

## Requisitos

Antes de comenzar, asegúrate de tener lo siguiente instalado:

    Python 3.8+
    FastAPI (Para la API REST)
    SQLAlchemy (Para la base de datos)
    Uvicorn (Servidor ASGI)

## Instalación de dependencias

Para instalar las dependencias del proyecto, utiliza pip y el archivo requirements.txt:

`pip install -r requirements.txt`

## Configuración de la base de datos

Tras la primera ejecución, la base de datos se creará en /data/game.db

## Ejecución de la aplicación
**Modo 1: API REST**

Puedes ejecutar la aplicación y utilizar la API REST para interactuar con las partidas y obtener estadísticas. Para iniciar el servidor FastAPI:

`uvicorn main:app --reload`

Una vez iniciado, la API estará disponible en http://127.0.0.1:8000. La documentación interactiva (Swagger) estará disponible en http://127.0.0.1:8000/docs.

**Modo 2: Juego desde la consola**

Puedes jugar directamente desde la consola en los modos "humano vs máquina" o "máquina vs máquina". Para esto, simplemente ejecuta el siguiente comando:

`python main.py --modo humano`

Si quieres ejecutar el modo "máquina vs máquina", especifica el número de partidas con:

`python main.py --modo maquina --n_partidas 5`

## Endpoints de la API

A continuación se detallan los endpoints disponibles en la API:
1. Obtener información global de las partidas

    URL: /get_global_info
    Método: GET
    Descripción: Devuelve un resumen global con estadísticas de partidas ganadas, perdidas y porcentaje de victorias.

2. Obtener la mano más fuerte

    URL: /mano_fuerte
    Método: GET
    Descripción: Retorna la mano (piedra, papel o tijera) que más veces ha ganado y su porcentaje de victorias.

3. Obtener la mano más débil

    URL: /mano_debil
    Método: GET
    Descripción: Retorna la mano que más veces ha perdido y su porcentaje de derrotas.

4. Ranking de jugadores

    URL: /ranking
    Método: GET
    Descripción: Devuelve el ranking de los 3 mejores jugadores según sus puntos acumulados.

5. Estadísticas de partidas

    URL: /estadisticas
    Método: GET
    Descripción: Devuelve estadísticas generales de las partidas, incluyendo el número total, las ganadas y las abandonadas.

Pruebas

Este proyecto cuenta con una serie de tests unitarios para garantizar que todas las funcionalidades se comporten correctamente. Para ejecutar las pruebas, puedes usar pytest:

`pytest /tests`