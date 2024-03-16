import pygame
import random

# Configuración de colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)

# Definir tamaño de pantalla
LARGO_PANTALLA = 600
ALTO_PANTALLA = 600

# Definir tamaño de bloques y cantidad de bloques en el tablero
LARGO_BLOQUE = 20
ALTO_BLOQUE = 20
CANTIDAD_BLOQUES_ANCHO = 15
CANTIDAD_BLOQUES_ALTO = 30

# Fuente para puntajes
pygame.font.init()
fuente = pygame.font.Font(None, 36)

def cargar_imagen(ruta):
    imagen = pygame.image.load(ruta)
    return pygame.transform.scale(imagen, (LARGO_PANTALLA, ALTO_PANTALLA))

def generar_pieza():
    piezas = [
        [[1, 1, 1, 1]],  # I
        [[1, 1, 1], [0, 1, 0]],  # T
        [[1, 1, 1], [1, 0, 0]],  # L
        [[1, 1, 1], [0, 0, 1]],  # J
        [[1, 1], [1, 1]],  # O
        [[0, 1, 1], [1, 1, 0]],  # S
        [[1, 1, 0], [0, 1, 1]]   # Z
    ]
    return random.choice(piezas)

def crear_tablero():
    tablero = [[0 for _ in range(CANTIDAD_BLOQUES_ANCHO)] for _ in range(CANTIDAD_BLOQUES_ALTO)]
    return tablero

def dibujar_bloque(pantalla, x, y):
    pygame.draw.rect(pantalla, AZUL, (x, y, LARGO_BLOQUE, ALTO_BLOQUE))
    pygame.draw.rect(pantalla, BLANCO, (x, y, LARGO_BLOQUE, ALTO_BLOQUE), 1)

def dibujar_tablero(pantalla, tablero, siguiente_pieza, puntaje, puntaje_maximo):
    # Dibujar fondo de pantalla
    pantalla.fill(NEGRO)
    # Dibujar imagen de fondo
    pantalla.blit(fondo, (0, 0))
    
    # Dibujar borde blanco
    pygame.draw.rect(pantalla, BLANCO, (0, 0, CANTIDAD_BLOQUES_ANCHO * LARGO_BLOQUE, CANTIDAD_BLOQUES_ALTO * ALTO_BLOQUE), 1)
    
    # Dibujar bloques de juego
    for fila in range(len(tablero)):
        for columna in range(len(tablero[fila])):
            if tablero[fila][columna] == 1:
                dibujar_bloque(pantalla, columna * LARGO_BLOQUE, fila * ALTO_BLOQUE)

    # Dibujar siguiente pieza
    texto_siguiente_pieza = fuente.render("Siguiente pieza:", True, BLANCO)
    pantalla.blit(texto_siguiente_pieza, (CANTIDAD_BLOQUES_ANCHO * LARGO_BLOQUE + 20, 20))
    y_siguiente_pieza = 60
    for fila in siguiente_pieza:
        x_siguiente_pieza = CANTIDAD_BLOQUES_ANCHO * LARGO_BLOQUE + 20
        for bloque in fila:
            if bloque == 1:
                dibujar_bloque(pantalla, x_siguiente_pieza, y_siguiente_pieza)
            x_siguiente_pieza += LARGO_BLOQUE
        y_siguiente_pieza += ALTO_BLOQUE * 1

    # Dibujar puntaje
    texto_puntaje = fuente.render(f"Puntaje: {puntaje}", True, BLANCO)
    pantalla.blit(texto_puntaje, (CANTIDAD_BLOQUES_ANCHO * LARGO_BLOQUE + 20, 220))

    # Dibujar puntaje máximo alcanzado
    texto_puntaje_maximo = fuente.render(f"Puntaje máximo: {puntaje_maximo}", True, BLANCO)
    pantalla.blit(texto_puntaje_maximo, (CANTIDAD_BLOQUES_ANCHO * LARGO_BLOQUE + 20, 270))

def verificar_lineas_completas(tablero):
    lineas_completas = []
    for fila in range(len(tablero)):
        if all(tablero[fila]):
            lineas_completas.append(fila)
    return lineas_completas

def eliminar_lineas_completas(tablero, lineas_completas):
    for fila in lineas_completas:
        del tablero[fila]
        tablero.insert(0, [0 for _ in range(CANTIDAD_BLOQUES_ANCHO)])

def main():
    pygame.init()

    # Configuración de pantalla
    pantalla = pygame.display.set_mode((LARGO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Tetris")

    reloj = pygame.time.Clock()

    # Cargar imagen de fondo
    global fondo
    fondo = cargar_imagen("fondo.jpg")

    pieza_actual = generar_pieza()
    siguiente_pieza = generar_pieza()
    tablero = crear_tablero()

    tiempo_caida = 0
    velocidad_caida_normal = 300  # Milisegundos
    velocidad_caida_rapida = 50  # Milisegundos

    # Posición inicial de la pieza
    x_pieza = CANTIDAD_BLOQUES_ANCHO // 2 - len(pieza_actual[0]) // 2
    y_pieza = 0

    girar = False
    puntaje = 0
    puntaje_maximo = 0
    velocidad_actual = velocidad_caida_normal

    juego_terminado = False

    while not juego_terminado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                juego_terminado = True
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:
                    girar = True
                elif evento.key == pygame.K_LEFT:
                    if x_pieza > 0:
                        x_pieza -= 1
                        if any(x_pieza + columna < 0 for columna in range(len(pieza_actual[0]))):
                            x_pieza += 1
                elif evento.key == pygame.K_RIGHT:
                    if x_pieza + len(pieza_actual[0]) < CANTIDAD_BLOQUES_ANCHO:
                        x_pieza += 1
                        if any(x_pieza + columna >= CANTIDAD_BLOQUES_ANCHO for columna in range(len(pieza_actual[0]))):
                            x_pieza -= 1
                elif evento.key == pygame.K_DOWN:
                    velocidad_actual = velocidad_caida_rapida

            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_DOWN:
                    velocidad_actual = velocidad_caida_normal

        tiempo_caida += reloj.get_rawtime()
        reloj.tick()

        if tiempo_caida > velocidad_actual:
            tiempo_caida = 0
            y_pieza += 1

            # Verificar si la pieza alcanzó el fondo o colisionó con otras piezas
            if (y_pieza + len(pieza_actual) > CANTIDAD_BLOQUES_ALTO) or \
               any(tablero[y_pieza + fila][x_pieza + columna] == 1 for fila in range(len(pieza_actual)) for columna in range(len(pieza_actual[0])) if pieza_actual[fila][columna] == 1 and 0 <= x_pieza + columna < CANTIDAD_BLOQUES_ANCHO and 0 <= y_pieza + fila < CANTIDAD_BLOQUES_ALTO):
                # Actualizar el tablero con la posición de la pieza
                for fila in range(len(pieza_actual)):
                    for columna in range(len(pieza_actual[fila])):
                        if pieza_actual[fila][columna] == 1:
                            tablero[y_pieza - 1 + fila][x_pieza + columna] = 1

                # Verificar si el juego termina
                if any(y_pieza + fila <= 0 for fila in range(len(pieza_actual))):
                    juego_terminado = True

                # Verificar y eliminar líneas completas
                lineas_completas = verificar_lineas_completas(tablero)
                if lineas_completas:
                    puntaje += len(lineas_completas) * 10
                    puntaje_maximo = max(puntaje_maximo, puntaje)
                    eliminar_lineas_completas(tablero, lineas_completas)

                # Generar una nueva pieza
                pieza_actual = siguiente_pieza
                siguiente_pieza = generar_pieza()
                x_pieza = CANTIDAD_BLOQUES_ANCHO // 2 - len(pieza_actual[0]) // 2
                y_pieza = 0

        dibujar_tablero(pantalla, tablero, siguiente_pieza, puntaje, puntaje_maximo)

        # Dibujar pieza actual
        for fila in range(len(pieza_actual)):
            for columna in range(len(pieza_actual[fila])):
                if pieza_actual[fila][columna] == 1:
                    dibujar_bloque(pantalla, (columna + x_pieza) * LARGO_BLOQUE, (fila + y_pieza) * ALTO_BLOQUE)

        if girar:
            pieza_actual_temp = [list(reversed(columna)) for columna in zip(*pieza_actual)]
            if x_pieza + len(pieza_actual_temp[0]) <= CANTIDAD_BLOQUES_ANCHO:
                pieza_actual = pieza_actual_temp
            girar = False

        if juego_terminado:
            # Mostrar "GAME OVER"
            texto_game_over = fuente.render("GAME OVER", True, ROJO)
            pantalla.blit(texto_game_over, ((LARGO_PANTALLA - texto_game_over.get_width()) // 2, (ALTO_PANTALLA - texto_game_over.get_height()) // 2))

        pygame.display.update()

if __name__ == "__main__":
    main()
