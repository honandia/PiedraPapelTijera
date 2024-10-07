import random
import sys
import argparse
from app.models import JugadaEnum
from app.database import SessionLocal, init_db
from app.services import JuegoService
from app.repositories import PartidaRepository, JugadorRepository


# Opciones de jugadas
opciones = {
    'piedra': JugadaEnum.PIEDRA,
    'papel': JugadaEnum.PAPEL,
    'tijera': JugadaEnum.TIJERA
}

# Función principal para el juego humano vs máquina
def jugar_partida_humano_vs_maquina():
    db = SessionLocal()
    jugador_repo = JugadorRepository(db)
    partida_repo = PartidaRepository(db)
    juego_service = JuegoService(partida_repo, jugador_repo)

    try:
        print("¡Iniciando partida de Piedra 🪨, Papel 📜 o Tijera ✂️!")

        nombreJugador = input("Intorduce el nombre del jugador: ")
        jugador = jugador_repo.get_or_create(nombreJugador, tipo="humano")
        maquina = jugador_repo.get_or_create("Máquina", tipo="maquina")
        partida = juego_service.iniciar_partida(jugador, maquina)

        
        jugadas_ganadas_humano = 0
        jugadas_ganadas_maquina = 0
        total_jugadas = 0 

        while total_jugadas in range(3):
            try:
                jugada_humano = input("Elige piedra, papel o tijera: ").lower()
                if jugada_humano not in opciones:
                    print("Entrada no válida. Intenta de nuevo.")
                    continue

                jugada_maquina = random.choice(list(opciones.values()))
                print(f"La máquina eligió: {jugada_maquina}")

                resultado = juego_service.registrar_jugada(partida, jugador, opciones[jugada_humano], jugada_maquina)
                if resultado == 'ganada':
                    jugadas_ganadas_humano += 1
                    print("Ganaste esta jugada.")
                elif resultado == 'perdida':
                    jugadas_ganadas_maquina += 1
                    print("La máquina ganó esta jugada.")
                else:
                    print("Empate en esta jugada.")
                total_jugadas += 1
                
            except KeyboardInterrupt:
                print("\nJuego interrumpido. La partida será considerada ganada por la máquina.")
                juego_service.marcar_abandonada(partida)
                sys.exit()

        # Determinar el ganador
        if jugadas_ganadas_humano > jugadas_ganadas_maquina:
            print("¡Ganaste la partida!")
        else:
            print("La máquina ganó la partida.")
        juego_service.finalizar_partida(partida, jugador if jugadas_ganadas_humano > jugadas_ganadas_maquina else maquina)

    finally:
        db.close()

# Función para el modo máquina vs máquina
def jugar_partida_maquina_vs_maquina(n_partidas):
    db = SessionLocal()
    jugador_repo = JugadorRepository(db)
    partida_repo = PartidaRepository(db)
    juego_service = JuegoService(partida_repo, jugador_repo)

    try:
        maquina_1 = jugador_repo.get_or_create("Máquina 1", tipo="maquina")
        maquina_2 = jugador_repo.get_or_create("Máquina 2", tipo="maquina")

        for partida_num in range(n_partidas):
            print(f"\nIniciando partida {partida_num + 1} de {n_partidas} entre Máquina 1 y Máquina 2...")
            partida = juego_service.iniciar_partida(maquina_1, maquina_2)

            jugadas_ganadas_maquina_1 = 0
            jugadas_ganadas_maquina_2 = 0
            total_jugadas = 0

            while total_jugadas in range(3):
                jugada_maquina_1 = random.choice(list(opciones.values()))
                jugada_maquina_2 = random.choice(list(opciones.values()))
                print(f"Máquina 1 eligió: {jugada_maquina_1}, Máquina 2 eligió: {jugada_maquina_2}")

                resultado = juego_service.registrar_jugada(partida, maquina_1, jugada_maquina_1, jugada_maquina_2)
                if resultado == 'ganada':
                    jugadas_ganadas_maquina_1 += 1
                    print("Máquina 1 ganó esta jugada.")
                elif resultado == 'perdida':
                    jugadas_ganadas_maquina_2 += 1
                    print("Máquina 2 ganó esta jugada.")
                else:
                    print("Empate en esta jugada.")

                total_jugadas += 1

            # Determinar el ganador
            if jugadas_ganadas_maquina_1 > jugadas_ganadas_maquina_2:
                print("Máquina 1 ganó la partida.")
                juego_service.finalizar_partida(partida, maquina_1)
            else:
                print("Máquina 2 ganó la partida.")
                juego_service.finalizar_partida(partida, maquina_2)

    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Juego de Piedra, Papel o Tijera.")
    parser.add_argument('--modo', choices=['humano', 'maquina'], default='humano', help="Elige el modo de juego: 'humano' o 'maquina'.")
    parser.add_argument('--n_partidas', type=int, default=1, help="Número de partidas para el modo 'maquina'.")
    args = parser.parse_args()

    # Inicializar la base de datos (crear tablas)
    init_db()

    if args.modo == 'maquina':
        jugar_partida_maquina_vs_maquina(args.n_partidas)
    else:
        jugar_partida_humano_vs_maquina()
