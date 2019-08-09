import sys
import pygame, subprocess
import random
from random import randint
from pygame.locals import *

#
# Proyecto: N EN RAYA TRIDIMENSIONAL
#
# DESCRIPCION: Parecido al juego 3 en raya, pero en este caso, el juego consta de N tableros de tamanyo NxN,
# 			donde, ademas de las lineas horizontales, verticales y diagonales en un mismo tablero, tambien se considerara
# 			una linea cuando un jugador consigue colocar una ficha en la misma casilla de los N tableros. Mas aun, el 
#			juego no se termina cuando un jugador logra una linea, sino que se sigue hasta que se completen las NxNxN 
#			casillas, considerandose ganador quien logre realizar mas lineas.
#
#
# Autor:
#		Amin Arriaga y Angel Garces
#
# Ultima modificacion: 11/06/2019


########################################### CLASE JUGADOR #####################################################
class Jugador:
    def __init__(self, nombre, turno):
    	# Guardamos el nombre del Jugador
    	self.nombre = nombre

    	# Guardamos el numero de lineas en filas, columnas, diagonales y entre tableros que ha hecho el Jugador
    	self.filas = 0
    	self.columnas = 0
    	self.diagonales = 0
    	self.enZ = 0

    	# Guardamos la posicion de las lineas en filas, columnas, diagonales y entre tableros que ha hecho el Jugador
    	self.lineasFila = []
    	self.lineasCol = []
    	self.lineasDiag = []
    	self.lineasEnZ = []

    	# Guardamos el turno correspondiente del Jugador
    	self.turn = turno

    	# Guardamos el numero de victorias de un Jugador
    	self.wins = 0



############################# CONSTANTES REFERENTE A LA RESOLUCION DE LA PANTALLA #############################
resolucion = [1366,750]
largo = 680
alto = 375
pygame.init()
pantalla = pygame.display.set_mode(resolucion)
reloj1 = pygame.time.Clock()



############################# IMAGENES QUE SE USARAN EN EL JUEGO ##############################################
triangulo = pygame.image.load("C:\\Users\\Amin\\Documents\\N_en_Raya_3D\\Imagenes\\Triangulo.png")
triangulo = pygame.transform.scale(triangulo, [40, 30])
triangulo2 = pygame.transform.scale(triangulo, [60, 50])
trianguloInv = pygame.image.load("C:\\Users\\Amin\\Documents\\N_en_Raya_3D\\Imagenes\\TrianguloInv.png")
trianguloInv1 = pygame.transform.scale(trianguloInv, [40, 30])
trianguloInv2 = pygame.transform.scale(trianguloInv, [60, 50])
fondo = pygame.image.load("C:\\Users\\Amin\\Documents\\N_en_Raya_3D\\Imagenes\\Fondo.jpg")
fondo = pygame.transform.scale(fondo, resolucion)



############################# FUENTES DE TEXTO ################################################################
subtitulos = pygame.font.Font("C:\\Users\\Amin\\Documents\\N_en_Raya_3D\\Fonts\\ka1.ttf", 50)
nombres = pygame.font.Font("C:\\Users\\Amin\\Documents\\N_en_Raya_3D\\Fonts\\ArcadeClassic.ttf", 70)
texto = pygame.font.Font("C:\\Users\\Amin\\Documents\\N_en_Raya_3D\\Fonts\\miracle.otf", 30)
titulos = pygame.font.Font("C:\\Users\\Amin\\Documents\\N_en_Raya_3D\\Fonts\\SEGA.ttf", 60)



############################# TEXTOS QUE SE USARAN EN EL JUEGO ################################################
Titulo1 = titulos.render("N EN RAYA", True, (0, 0, 0))
Titulo2 = titulos.render("TRIDIMENSIONAL", True, (0, 0, 0))
Jugador1 = subtitulos.render("Jugador 1: ", True, (0,0,0))
Jugador2 = subtitulos.render("Jugador 2: ", True, (0,0,0))
JugadorSolo = subtitulos.render("Jugador: ", True, (0,0,0))
Horizontal = texto.render("Lineas  Horizontales ", True, (0,0,0))
Vertical = texto.render("Lineas  Verticales ", True, (0,0,0))
Diagonal = texto.render("Lineas  Diagonales ", True, (0,0,0))
EntreTableros = texto.render("Lineas  Entre  Tableros ", True, (0,0,0))
Tablero = texto.render("Tablero", 0 ,(0,0,0))
Tab = texto.render("Tablero ", True, (0,0,0))
Fil = texto.render("Fila ", True, (0,0,0))
Col = texto.render("Columna ", True, (0,0,0))
MultJug = subtitulos.render("Multijugador", True, (0,0,0))
Computer = subtitulos.render("Individual", True, (0,0,0))
Exit = subtitulos.render("Salir", True, (0,0,0))
NumDim = subtitulos.render("Dimension  del  Tablero: ", True, (0,0,0))
Yes = texto.render("Si", True, (0,0,0))
Not = texto.render("No", True, (0,0,0))
YES = subtitulos.render("Si", True, (0,0,0))
NOT = subtitulos.render("No", True, (0,0,0))
Salir = texto.render("Salir", True, (0,0,0))
AsegurarSalida = texto.render("¿Esta seguro que desea salir?", True, (0,0,0))
AsegurarGuardar = texto.render("¿Desea guardar esta partida? Se eliminara la anterior.", True, (0,0,0))
CargarPartida = subtitulos.render("¿Desean  cargar  la  ultima  partida?", True, (0,0,0))
Recomendacion = texto.render("Para  dimensiones  mayores  a  3,  el  bot  tardara  en  responder  algunas  jugadas.", 
	True, (0,0,0))



############################################## SUBPROGRAMAS ###################################################
def quedanFichas(T: [[[int]]]) -> bool:
	"""Funcion que verifica si aun hay algun espacio donde se pueda colocar fichas en el supertablero.

	ENTRADAS:
	T: [[[int]]], matriz tridimensional que representa al Super-Tablero.
	SALIDAS:
	bool, indica si hay alguna casilla vacia en el Super-Tablero."""

	hayFichas = any( any( any(T[i][j][k]==0 for k in range(0, len(T))) for j in range(0, len(T))) for i in range(0, len(T)) )
	return hayFichas

def esValida(T: [[[int]]], tablero: int, fila: int, columna: int) -> bool:
	"""Funcion que verifica si la posicion donde se desea jugar es valida. Una jugada se considera valida si no hay
		 ninguna ficha en la posicion indicada.

	ENTRADAS:
	T: [[[int]]], matriz tridimensional que representa al Super-Tablero.
	tablero: int, indica el tablero donde se realizo la jugada.
	fila: int, indica la fila donde se realizo la jugada.
	columna: int, indica la columna donde se realizo la jugada.
	SALIDAS:
	bool, indica si el tablero, la fila y la columna estan dentro del Super-Tablero y en esa posicion hay un 0."""

	if tablero > len(T)-1 or tablero < 0 or fila > len(T)-1 or fila < 0 or columna > len(T)-1 or columna < 0:
		return False
	valido = (T[tablero][fila][columna] == 0)
	return valido

def hayLineaHorizontal(T: [[[int]]], tablero: int, fila: int, player: Jugador, minimax: bool) -> bool:
	"""Funcion que verifica si se formo una linea horizontal en la posicion donde se realizo la jugada.

	ENTRADAS:
	T: [[[int]]], matriz tridimensional que representa al Super-Tablero.
	tablero: int, indica el tablero donde se realizo la jugada.
	fila: int, indica la fila donde se realizo la jugada.
	player: Jugador, contiene los datos del jugador que realizo esta jugada.
	minimax: bool, indica si la funcion esta siendo llamada por la funcion miniMax. En caso de ser asi, no guardara las lineas
			que se hagan en los datos del jugador.
	SALIDAS:
	bool, indica si en la posicion que jugo el Jugador se realizo una linea horizontal."""

	turno = player.turn
	lineaHorizontal = all( T[tablero][fila][i]==turno for i in range(0, len(T)) )

	# Guardamos la posicion donde el jugador hizo una linea
	if lineaHorizontal and not minimax:
		player.lineasFila.append([tablero, fila])

	return lineaHorizontal

def hayLineaVertical(T: [[[int]]], tablero: int ,columna: int , player: Jugador, minimax: bool) -> bool:
	""" Verifica si se formo una linea vertical en la posicion donde se realizo la jugada.

	ENTRADAS:
	T: [[[int]]], matriz tridimensional que representa al Super-Tablero.
	tablero: int, indica el tablero donde se realizo la jugada.
	columna: int, indica la columna donde se realizo la jugada.
	player: Jugador, contiene los datos del jugador que realizo esta jugada.
	minimax: bool, indica si la funcion esta siendo llamada por la funcion miniMax. En caso de ser asi, no guardara las lineas
			que se hagan en los datos del jugador.
	SALIDAS:
	bool, indica si en la posicion que jugo el Jugador se realizo una linea vertical."""

	turno = player.turn
	lineaVertical = all( T[tablero][i][columna]==turno for i in range(0, len(T)) )

	# Guardamos la posicion donde el jugador hizo una linea
	if lineaVertical and not minimax:
		player.lineasCol.append([tablero, columna])

	return lineaVertical

def hayLineaDiagonal(T: [[[int]]], tablero: int , fila: int, columna: int, player: Jugador, minimax: bool) -> bool:
	""" Verifica si se formo una linea en la diagonal principal en la posicion donde se realizo la jugada.

	ENTRADAS:
	T: [[[int]]], matriz tridimensional que representa al Super-Tablero.
	tablero: int, indica el tablero donde se realizo la jugada.
	fila: int, indica la fila donde se realizo la jugada.
	columna: int, indica la columna donde se realizo la jugada.
	player: Jugador, contiene los datos del jugador que realizo esta jugada.
	minimax: bool, indica si la funcion esta siendo llamada por la funcion miniMax. En caso de ser asi, no guardara las lineas
			que se hagan en los datos del jugador.
	SALIDAS:
	bool, indica si en la posicion que jugo el Jugador se realizo una linea diagonal."""

	turno = player.turn

	lineaDiagonal = False
	if fila == columna:
		lineaDiagonal = all( T[tablero][i][i]==turno for i in range(0, len(T)) )

	# Guardamos la posicion donde el jugador hizo una linea
	if lineaDiagonal and not minimax:
		player.lineasDiag.append([tablero, 1])

	return lineaDiagonal

def hayLineaDiagonalInversa(T: [[[int]]], tablero: int , fila: int, columna: int, player: Jugador, minimax: bool) -> bool:
	""" Verifica si se formo una linea en la diagonal inversa en la posicion donde se realizo la jugada.

	ENTRADAS:
	T: [[[int]]], matriz tridimensional que representa al Super-Tablero.
	tablero: int, indica el tablero donde se realizo la jugada.
	fila: int, indica la fila donde se realizo la jugada.
	columna: int, indica la columna donde se realizo la jugada.
	player: Jugador, contiene los datos del jugador que realizo esta jugada.
	minimax: bool, indica si la funcion esta siendo llamada por la funcion miniMax. En caso de ser asi, no guardara las lineas
			que se hagan en los datos del jugador.
	SALIDAS:
	bool, indica si en la posicion que jugo el Jugador se realizo una linea diagonal inversa."""

	turno = player.turn

	lineaDiagonal = False
	if fila + columna == len(T)-1:
		lineaDiagonal = all( T[tablero][i][len(T)-1-i]==turno for i in range(0, len(T)) )
	
	# Guardamos la posicion donde el jugador hizo una linea
	if lineaDiagonal and not minimax:
		player.lineasDiag.append([tablero, 0])

	return lineaDiagonal

def hayLineaEnZ(T: [[[int]]], fila: int, columna: int, player: Jugador, minimax: bool) -> bool:
	""" Verifica si se formo una linea en todos los tableros en la posicion donde se realizo la jugada.

	ENTRADAS:
	T: [[[int]]], matriz tridimensional que representa al Super-Tablero.
	fila: int, indica la fila donde se realizo la jugada.
	columna: int, indica la columna donde se realizo la jugada.
	player: Jugador, contiene los datos del jugador que realizo esta jugada.
	minimax: bool, indica si la funcion esta siendo llamada por la funcion miniMax. En caso de ser asi, no guardara las lineas
			que se hagan en los datos del jugador.
	SALIDAS:
	bool, indica si en la posicion que jugo el Jugador se realizo una linea entre tableros."""

	turno = player.turn
	lineaEnZ = all( T[i][fila][columna]==turno for i in range(0, len(T)) )

	# Guardamos la posicion donde el jugador hizo una linea
	if lineaEnZ and not minimax:
		player.lineasEnZ.append([fila, columna])

	return lineaEnZ

def reflejarJugada(T: [[[int]]], tablero: int, fila: int, columna: int, turno: int):
	"""Procedimiento que modifica el Super-Tablero, reflejando la jugada realizada por cierto jugador.

	ENTRADAS-SALIDAS:
	T: [[[int]]], matriz tridimensional que representa al Super-Tablero.
	ENTRADAS:
	tablero: int, indica el tablero donde se realizo la jugada.
	fila: int, indica la fila donde se realizo la jugada.
	columna: int, indica la columna donde se realizo la jugada.
	turno: int, turno del jugador que realizo la jugada. Tambien representa la ficha del jugador en el Super-Tablero"""

	T[tablero][fila][columna] = turno

def hayLinea(T: [[[int]]], tablero: int, fila: int, columna: int, player: Jugador) -> str:
	"""Verifica si se formo alguna linea, en caso de ser asi, se lo indica a los jugadores y actualiza el contador de lineas.

	ENTRADAS:
	T: [[[int]]], matriz tridimensional que representa al Super-Tablero.
	tablero: int, indica el tablero donde se realizo la jugada.
	fila: int, indica la fila donde se realizo la jugada.
	columna: int, indica la columna donde se realizo la jugada.
	ENTRADAS-SALIDAS:
	player: Jugador, contiene los datos del jugador que realizo esta jugada.
	SALIDAS:
	str, Es vacio si no se hizo ninguna linea, en caso contrario, retorna un mensaje diciendo que se realizo una linea"""

	masPuntos = False # Esta variable se usa para indicarle a los jugadores si alguin hizo una o varias lineas

	# Se usan muchos if y no if/elif/else ya que se debe sumar puntos por cada linea hecha
	if hayLineaHorizontal(T, tablero, fila, player, False):
		player.filas += 1
		masPuntos = True
	if hayLineaVertical(T, tablero, columna, player, False):
		player.columnas += 1
		masPuntos = True
	if hayLineaDiagonal(T, tablero, fila, columna, player, False):
		player.diagonales += 1
		masPuntos = True
	if hayLineaDiagonalInversa(T, tablero, fila, columna, player, False):
		player.diagonales += 1
		masPuntos = True
	if hayLineaEnZ(T, fila, columna, player, False):
		player.enZ += 1
		masPuntos = True

	if masPuntos:
		return player.nombre + "  han  aumentados  tus  puntos!"
	else:
		return ""

def mostarPuntajes(player1: Jugador, player2: Jugador):
	"""Procedimiento que muestra graficamente el puntaje de cada jugador.

	ENTRADAS:
	player1: Jugador, contiene los datos del jugador 1.
	player2: Jugador, contiene los datos del jugador 2."""

	pantalla.blit(fondo, [0, 0]) 

	# Cargamos las imagenes de la X y el O. No se hizo antes pues su tamanyo depende de la dimensaion del tablero
	equis = pygame.image.load("Equis.png")
	equis = pygame.transform.scale(equis, [90, 70])
	circulo = pygame.image.load("Circulo.png")
	circulo = pygame.transform.scale(circulo, [100, 80])

	# Guardamos en vairables del tipo "surface" los datos del jugador 1
	name1 = subtitulos.render(str(player1.nombre) + " - " + str(player1.wins), True, (0,0,0))
	PFilas1 = texto.render(str(player1.filas), True, (0,0,0))
	PCol1 = texto.render(str(player1.columnas), True, (0,0,0))
	PDia1 = texto.render(str(player1.diagonales), True, (0,0,0))
	PenZ1 = texto.render(str(player1.enZ), True, (0,0,0))

	# Guardamos en vairables del tipo "surface" los datos del jugador 2
	name2 = subtitulos.render(str(player2.nombre) + " - " + str(player2.wins), True, (0,0,0))
	PFilas2 = texto.render(str(player2.filas), True, (0,0,0))
	PCol2 = texto.render(str(player2.columnas), True, (0,0,0))
	PDia2 = texto.render(str(player2.diagonales), True, (0,0,0))
	PenZ2 = texto.render(str(player2.enZ), True, (0,0,0))

	# Informacion del Jugador 1
	if player1.turn == 1:
		pantalla.blit(equis, [20, 5])
	else:
		pantalla.blit(circulo, [20, 5])
	pantalla.blit(name1, [120, 20])
	pantalla.blit(Horizontal, [10, 80])
	pantalla.blit(Vertical, [10, 110])
	pantalla.blit(Diagonal, [10, 140])
	pantalla.blit(EntreTableros, [10, 170])
	pantalla.blit(PFilas1, [560, 80])
	pantalla.blit(PCol1, [560, 110])
	pantalla.blit(PDia1, [560, 140])
	pantalla.blit(PenZ1, [560, 170])

	# Informacion del Jugador 2
	if player2.turn == 1:
		pantalla.blit(equis, [700, 5])
	else:
		pantalla.blit(circulo, [700, 5])
	pantalla.blit(name2, [800, 20])
	pantalla.blit(Horizontal, [660, 80])
	pantalla.blit(Vertical, [660, 110])
	pantalla.blit(Diagonal, [660, 140])
	pantalla.blit(EntreTableros, [660, 170])
	pantalla.blit(PFilas2, [1200, 80])
	pantalla.blit(PCol2, [1200, 110])
	pantalla.blit(PDia2, [1200, 140])
	pantalla.blit(PenZ2, [1200, 170])

def dibujarTab(Tab: [[int]], player1: Jugador, player2: Jugador, tablero: int):
	"""Procedimiento que muestra graficamente el tablero actual, con las correspondientes fichas de ambos jugadores.

	ENTRADAS:
	Tab: [[int]], matriz que representa al tablero actual.
	player1: Jugador, contiene los datos del jugador 1.
	player2: Jugador, contiene los datos del jugador 2.
	tablero: int, numero que representa al tablero actual en el Super-Tablero."""

	# Cargamos las imagenes de la X y el O. No se hizo antes pues su tamanyo depende de la dimensaion del tablero
	equis = pygame.image.load("Equis.png")
	equis = pygame.transform.scale(equis, [int(largo/len(Tab))-5, int(alto/len(Tab))-5])
	circulo = pygame.image.load("Circulo.png")
	circulo = pygame.transform.scale(circulo, [int(largo/len(Tab))-5, int(alto/len(Tab))-5])

	# Dibujamos la linea superior e izquierda del Tablero
	pygame.draw.line(pantalla, (0,0,0), [100, 320], [100+largo, 320], 4)
	pygame.draw.line(pantalla, (0,0,0), [100, 320], [100, 320+alto], 4)

	# Dibujamos las lineas internas del tablero 
	for i in range(0, len(Tab) + 1):
		pygame.draw.line(pantalla, (0,0,0), [100, 320 + i*(alto/len(Tab))], [100+largo, 320 + i*(alto/len(Tab))], 4)
		pygame.draw.line(pantalla, (0,0,0), [100 + i*(largo/len(Tab)), 320], [100 + i*(largo/len(Tab)), 320 + alto], 4)

	# Dibujamos las X's y O's correspondientes
	for i in range(0, len(Tab)):
		for j in range(0, len(Tab)):
			if Tab[i][j]==1:
				pantalla.blit(equis, [100 + j*(largo/len(Tab)) + 2, 320 + i*(alto/len(Tab)) + 2])
			elif Tab[i][j]==2:
				pantalla.blit(circulo, [100 + j*(largo/len(Tab)) + 2, 320 + i*(alto/len(Tab)) + 2])

	# Dibujamos las lineas correspondientes al Jugador 1
	# Lineas Horizontales
	for linea in player1.lineasFila:
		if linea[0] == tablero:
			pygame.draw.line(pantalla, (255,((1-player1.turn)**2)*255,0), [100, 320 + (linea[1] + 1/2)*(alto/len(Tab))],\
			 [100+largo, 320 + (linea[1] + 1/2)*(alto/len(Tab))], 4)
	# Lineas Verticales
	for linea in player1.lineasCol:
		if linea[0] == tablero:
			pygame.draw.line(pantalla, (255,((1-player1.turn)**2)*255,0), [100 + (linea[1] + 1/2)*(largo/len(Tab)), 320],\
			 [100 + (linea[1] + 1/2)*(largo/len(Tab)), 320 + alto], 4)
	# Lineas Diagonales
	for linea in player1.lineasDiag:
		if (linea[0] == tablero) and (linea[1] == 1):
			pygame.draw.line(pantalla, (255,((1-player1.turn)**2)*255,0), [100, 320], [100 + largo, 320 + alto], 4)
		elif (linea[0] == tablero) and (linea[1] == 0):
			pygame.draw.line(pantalla, (255,((1-player1.turn)**2)*255,0), [100 + largo, 320], [100, 320 + alto], 4)
	# Lineas entre Tableros
	for linea in player1.lineasEnZ:
		pygame.draw.rect(pantalla, (255,((1-player1.turn)**2)*255,0), [100 + linea[1]*(largo/len(Tab)), 320 + \
			linea[0]*(alto/len(Tab)), largo/(len(Tab)), alto/(len(Tab))], 4)


	# Dibujamos las lineas correspondientes al Jugador 2
	# Lineas Horizontales
	for linea in player2.lineasFila:
		if linea[0] == tablero:
			pygame.draw.line(pantalla, (255,((1-player2.turn)**2)*255,0), [100, 320 + (linea[1] + 1/2)*(alto/len(Tab))],\
			 [100+largo, 320 + (linea[1] + 1/2)*(alto/len(Tab))], 4)
	# Lineas Verticales
	for linea in player2.lineasCol:
		if linea[0] == tablero:
			pygame.draw.line(pantalla, (255,((1-player2.turn)**2)*255,0), [100 + (linea[1] + 1/2)*(largo/len(Tab)), 320],\
			 [100 + (linea[1] + 1/2)*(largo/len(Tab)), 320 + alto], 4)
	# Lineas Diagonales
	for linea in player2.lineasDiag:
		if (linea[0] == tablero) and (linea[1] == 1):
			pygame.draw.line(pantalla, (255,((1-player2.turn)**2)*255,0), [100, 320], [100 + largo, 320 + alto], 4)
		elif (linea[0] == tablero) and (linea[1] == 0):
			pygame.draw.line(pantalla, (255,((1-player2.turn)**2)*255,0), [100 + largo, 320], [100, 320 + alto], 4)
	# Lineas entre Tableros
	for linea in player2.lineasEnZ:
		pygame.draw.rect(pantalla, (255,((1-player2.turn)**2)*255,0), [100 + linea[1]*(largo/len(Tab)), 320 + \
			linea[0]*(alto/len(Tab)), largo/(len(Tab)), alto/(len(Tab))], 4)

def jugada(T: [[[int]]], player1: Jugador, player2: Jugador, IndJug, Mensaje, turno: int, bot: bool) -> (int, int, int, bool):
	"""Funcion que retorna la jugada que desea realizar el jugador correspondiente, junto a una expresion booleana que 
			indica si se salio del juego o no.

	ENTRADAS:
	T: [[[int]]], matriz tridimensional que representa al Super-Tablero.
	player1: Jugador, contiene los datos del jugador 1.
	player2: Jugador, contiene los datos del jugador 2.
	IndJug: Surface (pygame), contiene el mensaje que indica a quien le toca jugar.
	Mensja: Surface (pygame), contiene el ultimo mensaje que se le desea dar a los jugadores.
	SALIDAS:
	int, tablero elegido por el jugador.
	int, fila elegida por el jugador.
	int, columan elegida por el jugador.
	bool, es True si se decidio salir del juego sin elegir una jugada, False en caso contrario."""

	# Sera el texto que se mostrara en la interfaz, e indica lo que va escribiendo el jugador
	tablero = "0"
	fila = "0"
	columna = "0"

	# Indica que es lo siguiente que le toca al jugador elegir
	Etablero = True
	Ecolumna = False
	Efila = False
	opcSalir = False
	salir = False
	guardar = False

	# Indica si el jugador ya termino de elegir
	done = False

	# Variable para hacer aparecer y desaparecer la barra que indica donde debe escribir
	time = 0

	# Variable que mueve la flecha para indicar al jugador en que tablero se encuentra
	k = 0

	# Variable que mueve la flecha para indicar al jugador si esta en la opcion "si" o "no"
	m = 0

	while not done:
		for evt in pygame.event.get():
			if evt.type == KEYDOWN:
				if guardar:
					if evt.key == K_RIGHT:
						m = 1
					if evt.key == K_LEFT:
						m = 0
					if evt.key == K_RETURN and m == 0 and not bot:
						# Se decidio a salir y guardar la partida multijugador, por lo que procedemos a guardar
						#	 los datos de esta partida
						with open('Datos ultPartida.txt', 'w') as f:
							f.write(str(len(T)) + "\n")

							f.write(player1.nombre + "\n")
							f.write(str(player1.filas) + "\n")
							f.write(str(player1.columnas) + "\n")
							f.write(str(player1.diagonales) + "\n")
							f.write(str(player1.enZ) + "\n")
							f.write(str(player1.lineasFila) + "\n")
							f.write(str(player1.lineasCol) + "\n")
							f.write(str(player1.lineasDiag) + "\n")
							f.write(str(player1.lineasEnZ) + "\n")
							f.write(str(player1.turn) + "\n")
							f.write(str(player1.wins) + "\n")

							f.write(player2.nombre + "\n")
							f.write(str(player2.filas) + "\n")
							f.write(str(player2.columnas) + "\n")
							f.write(str(player2.diagonales) + "\n")
							f.write(str(player2.enZ) + "\n")
							f.write(str(player2.lineasFila) + "\n")
							f.write(str(player2.lineasCol) + "\n")
							f.write(str(player2.lineasDiag) + "\n")
							f.write(str(player2.lineasEnZ) + "\n")
							f.write(str(player2.turn) + "\n")
							f.write(str(player2.wins) + "\n")

							f.write(str(turno))

						with open('Tableros ultPartida.txt', 'w') as f:
							f.write(str(T))


						return 0, 0, 0, True
					if evt.key == K_RETURN and m == 0 and bot:
						# Se decidio a salir y guardar la partida individual, por lo que procedemos a guardar los datos
						#	 de esta partida
						with open('Datos ultPartida Bot.txt', 'w') as f:
							f.write(str(len(T)) + "\n")

							f.write(player1.nombre + "\n")
							f.write(str(player1.filas) + "\n")
							f.write(str(player1.columnas) + "\n")
							f.write(str(player1.diagonales) + "\n")
							f.write(str(player1.enZ) + "\n")
							f.write(str(player1.lineasFila) + "\n")
							f.write(str(player1.lineasCol) + "\n")
							f.write(str(player1.lineasDiag) + "\n")
							f.write(str(player1.lineasEnZ) + "\n")
							f.write(str(player1.turn) + "\n")
							f.write(str(player1.wins) + "\n")

							f.write(player2.nombre + "\n")
							f.write(str(player2.filas) + "\n")
							f.write(str(player2.columnas) + "\n")
							f.write(str(player2.diagonales) + "\n")
							f.write(str(player2.enZ) + "\n")
							f.write(str(player2.lineasFila) + "\n")
							f.write(str(player2.lineasCol) + "\n")
							f.write(str(player2.lineasDiag) + "\n")
							f.write(str(player2.lineasEnZ) + "\n")
							f.write(str(player2.turn) + "\n")
							f.write(str(player2.wins) + "\n")

							f.write(str(turno))

						with open('Tableros ultPartida Bot.txt', 'w') as f:
							f.write(str(T))



						return 0, 0, 0, True
					if evt.key == K_RETURN and m == 1:
						return 0, 0, 0, True


				if not salir or guardar:
					if evt.unicode.isnumeric() and int(tablero) < 3 and Etablero:
						tablero += evt.unicode
					elif evt.key == K_BACKSPACE and Etablero and len(tablero) > 1:
						tablero = tablero[:-1]
					elif evt.key == K_RETURN and Etablero and len(tablero) > 1 and not opcSalir:
						Etablero = False
						Efila = True

					elif evt.unicode.isnumeric() and int(fila) < 3 and Efila:
						fila += evt.unicode
					elif evt.key == K_BACKSPACE and Efila and len(fila) > 1:
						fila = fila[:-1]
					elif evt.key == K_BACKSPACE and Efila and len(fila) == 1:
						Efila = False
						Etablero = True
					elif evt.key == K_RETURN and Efila and len(fila) > 1 and not opcSalir:
						Efila = False
						Ecolumna = True

					elif evt.unicode.isnumeric() and int(columna) < 3 and Ecolumna:
						columna += evt.unicode
					elif evt.key == K_BACKSPACE and Ecolumna and len(columna) > 1:
						columna = columna[:-1]
					elif evt.key == K_BACKSPACE and Ecolumna and len(columna) == 1:
						Ecolumna = False
						Efila = True
					elif evt.key == K_RETURN and Ecolumna and len(columna) > 1 and not opcSalir:
						Ecolumna = False
						done = True


					if evt.key == K_UP and k > 0 and not opcSalir:
						k -= 1
					if evt.key == K_DOWN and k < len(T)-1 and not opcSalir:
						k += 1
					elif evt.key == K_DOWN and k == len(T)-1 and not opcSalir and not guardar:
						opcSalir = True
					if evt.key == K_UP and opcSalir:
						opcSalir = False
					elif evt.key == K_RETURN and opcSalir:
						salir = True

				elif salir and not guardar:
					if evt.key == K_RIGHT:
						m = 1
					if evt.key == K_LEFT:
						m = 0
					if evt.key == K_RETURN and m == 0:
						guardar = True
						opcSalir = False
					if evt.key == K_RETURN and m == 1:
						salir = False


			if evt.type == pygame.QUIT:
				pygame.quit()

		tableroAct = tablero
		columnaAct = columna
		filaAct = fila
		JTab = texto.render(tableroAct.lstrip("0"), True, (0,0,0))
		JCol = texto.render(columnaAct.lstrip("0"), True, (0,0,0))
		JFil = texto.render(filaAct.lstrip("0"), True, (0,0,0))

		mostarPuntajes(player1, player2)

		if not salir:
			if Etablero and time < 5 and len(tablero) < 3:
				pygame.draw.line(pantalla, (0,0,0), [220+10*(len(tablero)-1), 255], [235+10*(len(tablero)-1), 255], 4)
			elif Etablero and time < 5 and len(tablero) == 3:
				pygame.draw.line(pantalla, (0,0,0), [230, 255], [245, 255], 4)
			elif Efila and time < 5 and len(fila) < 3:
				pygame.draw.line(pantalla, (0,0,0), [630+10*(len(fila)-1), 255], [645+10*(len(fila)-1), 255], 4)
			elif Efila and time < 5 and len(fila) == 3:
				pygame.draw.line(pantalla, (0,0,0), [640, 255], [655, 255], 4)
			elif Ecolumna and time < 5 and len(columna) < 3:
				pygame.draw.line(pantalla, (0,0,0), [1130+10*(len(columna)-1), 255], [1145+10*(len(columna)-1), 255], 4)
			elif Ecolumna and time < 5 and len(columna) == 3:
				pygame.draw.line(pantalla, (0,0,0), [1140, 255], [1155, 255], 4)

		pantalla.blit(IndJug, [430, 200])
		pantalla.blit(Tab, [10, 230])
		pantalla.blit(Fil, [460, 230])
		pantalla.blit(Col, [910, 230])
		pantalla.blit(JTab, [220, 230])
		pantalla.blit(JFil, [630, 230])
		pantalla.blit(JCol, [1130, 230])
		pantalla.blit(Tablero, [980, 320])

		if not opcSalir:
			pantalla.blit(triangulo, [1050, 345 + k*30])
		elif not salir:
			pantalla.blit(triangulo, [1110, 375 + len(T)*30])
		if not salir and not guardar:
			pantalla.blit(Mensaje, [100, 260])
		elif salir and not guardar:
			pantalla.blit(AsegurarSalida, [100, 260])
			pantalla.blit(Yes, [900, 260])
			pantalla.blit(Not, [1100, 260])
			pantalla.blit(triangulo, [950 + m*220, 260])


		if guardar:
			pantalla.blit(AsegurarGuardar, [50, 260])
			pantalla.blit(Yes, [900, 260])
			pantalla.blit(Not, [1100, 260])
			pantalla.blit(triangulo, [950 + m*220, 260])


		for i in range(0, len(T)):
			Num = texto.render(str(i+1), True, (0,0,0))
			pantalla.blit(Num, [1020, 350 + i*30])

		if not guardar:
			pantalla.blit(Salir, [1020, 380 + len(T)*30])

		dibujarTab(T[k], player1, player2, k)

		pygame.display.update()

		time += 1

		if time == 10:
			time = 0
		reloj1.tick(20)

	return int(tablero), int(fila), int(columna), False

def pedirJugada(T: [[[int]]], player1: Jugador, player2: Jugador, UltMen: str, turno: int, bot: bool) -> (int, int, int, bool):
	"""Funcion que retorna la jugada que desea realizar alguno de los jugadores, junto a una expresion booleana que 
			indica si se salio del juego o no.

	ENTRADAS:
	T: [[[int]]], matriz tridimensional que representa al Super-Tablero.
	player1: Jugador, contiene los datos del jugador 1.
	player2: Jugador, contiene los datos del jugador 2.
	UltMen: str, contiene el ultimo mensaje que se le desea dar a los jugadores.
	turno: int, indica a que jugador le toca jugar."""

	IndJug1 = texto.render(player1.nombre + "  indique  su  jugada", True, (0,0,0))
	IndJug2 = texto.render(player2.nombre + "  indique  su  jugada", True, (0,0,0))
	Mens = texto.render(UltMen, True, (0,0,0))

	if player1.turn == turno:
		tablero, fila, columna, salir = jugada(T, player1, player2, IndJug1, Mens, turno, bot)
	elif player2.turn == turno and not bot:
		tablero, fila, columna, salir = jugada(T, player1, player2, IndJug2, Mens, turno, bot)
	elif player2.turn == turno and bot:
		jugadaBot = miniMax(T, 3, 0, player1, player2, True, 1, True)
		tablero = jugadaBot[0] + 1
		fila = jugadaBot[1] + 1
		columna = jugadaBot[2] + 1
		salir = False

	return tablero-1, fila-1, columna-1, salir

def resultado(T: [[[int]]], player1: Jugador, player2: Jugador, total1: int, total2: int) -> bool:
	"""Funcion que muestra el resultado de la partida.

	ENTRADAS:
	T: [[[int]]], matriz tridimensional que representa al Super-Tablero.
	player1: Jugador, contiene los datos del jugador 1.
	player2: Jugador, contiene los datos del jugador 2.
	total1: int, cantidad de lineas realizada por el jugador 1.
	total2: int, cantidad de lineas realizada por el jugador 2.
	SALIDAS:
	bool, indica si los jugadores desean jugar otra partida."""

	# Variable que mueve la flecha para indicar al jugador en que tablero se encuentra
	k = 0

	# Variable que mueve la flecha para indicar al jugador si desea jugar otra partida o no
	m = 0

	# Indica si el jugador ya termino de elegir
	done = False

	if total1 > total2:
		Mensj = texto.render(player1.nombre + "  ha  ganado  la  partida.  ¿Desean  jugar  otra?", True, (0,0,0))
		if player1.wins < 1000:
			player1.wins += 1
	elif total2 > total1:
		Mensj = texto.render(player2.nombre + "  ha  ganado  la  partida.  ¿Desean  jugar  otra?", True, (0,0,0))
		if player2.wins < 1000:
			player2.wins += 1
	else:
		Mensj = texto.render("El  juego  termino  en  empate.  ¿Desean  jugar  otra?", True, (0,0,0))

	while not done:
		for evt in pygame.event.get():
			if evt.type == KEYDOWN:
				if evt.key == K_UP and k > 0:
					k -= 1
				if evt.key == K_DOWN and k < len(T)-1:
					k += 1
				if evt.key == K_RIGHT:
					m = 1
				if evt.key == K_LEFT:
					m = 0
				if evt.key == K_RETURN and m == 0:
					return True
				if evt.key == K_RETURN and m == 1:
					return False

			if evt.type == pygame.QUIT:
				pygame.quit()


		mostarPuntajes(player1, player2)

		pantalla.blit(Tablero, [980, 320])
		pantalla.blit(triangulo, [1050, 345 + k*30])
		pantalla.blit(Mensj, [30, 260])
		pantalla.blit(Yes, [900, 260])
		pantalla.blit(Not, [1100, 260])
		pantalla.blit(triangulo, [950 + m*220, 260])

		for i in range(0, len(T)):
			Num = texto.render(str(i+1), 0, (0,0,0))
			pantalla.blit(Num, [1020, 350 + i*30])

		dibujarTab(T[k], player1, player2, k)

		pygame.display.update()
		reloj1.tick(20)

def guardarNombre(player1: Jugador, player2: Jugador, turn: int) -> str:
	"""Guarda el nombre indicado por el jugador correspondiente.

	ENTRADAS-SALIDAS:
	player1: Jugador, contiene los datos del jugador 1.
	player2: Jugador, contiene los datos del jugador 2.
	ENTRADA:
	turn: int, indica el turno del jugador.
	SALIDA:
	str, nombre que decidio el jugador."""

	# Indica cuando el jugador ya termino de colocar el nombre
	done = False

	if turn == 1:
		mensj = "Jugador 1   indique   su   nombre."
	else:
		mensj = "Jugador 2   indique   su   nombre."

	while not done:
		for evt in pygame.event.get():
			if turn == 1:
				if evt.type == KEYDOWN:
					if evt.unicode.isalpha() and len(player1.nombre) < 8:
						player1.nombre += evt.unicode
					elif evt.key == K_BACKSPACE:
						player1.nombre = player1.nombre[:-1]
					elif evt.key == K_RETURN and len(player1.nombre) > 0:
						done = True
				if evt.type == pygame.QUIT:
					pygame.quit()
			else:
				if evt.type == KEYDOWN:
					if evt.unicode.isalpha() and len(player2.nombre) < 8:
						player2.nombre += evt.unicode
					elif evt.key == K_BACKSPACE:
						player2.nombre = player2.nombre[:-1]
					elif evt.key == K_RETURN and len(player2.nombre) > 0:
						done = True
				if evt.type == pygame.QUIT:
					pygame.quit()

		pantalla.blit(fondo, [0, 0]) 
		pantalla.blit(Titulo1, [390, 70])
		pantalla.blit(Titulo2, [240, 170])
		pantalla.blit(Jugador1, [300, 375])
		pantalla.blit(Jugador2, [300, 495])
		pantalla.blit(NumDim, [100, 615])
		pantalla.blit(trianguloInv2, [180, 380 + (turn-1)*120])

		Mensj = texto.render(mensj, True, (0,0,0))
		pantalla.blit(Mensj, [400, 320])

		nombre1 = nombres.render(player1.nombre, True, (0,0,0))
		pantalla.blit(nombre1, [750, 375])

		nombre2 = nombres.render(player2.nombre, True, (0,0,0))
		pantalla.blit(nombre2, [750, 495])

		pygame.display.update()
		reloj1.tick(20) 

	if turn == 1:
		return nombre1
	else:
		return nombre2

def pantallaMultiJug(player1: Jugador, player2: Jugador) -> int:
	"""Representa una pantalla donde se jugara una partida multijugador y se le pide a los dos jugadores su nombre, 
			asi como la dimension del supertablero.

	ENTRADAS-SALIDAS:
	player1: Jugador, contiene los datos del jugador 1.
	player2: Jugador, contiene los datos del jugador 2.
	SALIDAS:
	int, dimension del Super-Tablero elegida por los jugadores."""

	# Dimension del tablero
	N = "0"

	# Nombres de los jugadores
	nombre1 = guardarNombre(player1, player2, 1)
	nombre2 = guardarNombre(player1, player2, 2)

	mensj = "Indiquen   la   dimension   del   super-tablero."

	# Indica cuando el usuario ya decidio la dimension del super-tablero
	done = False

	while not done:
		for evt in pygame.event.get():
			if evt.type == KEYDOWN:
				if evt.unicode.isnumeric() and len(N) < 3:
					N += evt.unicode
				elif evt.key == K_BACKSPACE and len(N) > 1:
					N = N[:-1]
				elif evt.key == K_RETURN and len(N) > 1 and int(N)<12:
					done = True
				elif evt.key == K_RETURN and len(N) > 1 and int(N)>11:
					mensj = "El   supertablero   no   puede   ser   tan   grande."
			if evt.type == pygame.QUIT:
				pygame.quit()

		pantalla.blit(fondo, [0, 0]) 
		pantalla.blit(Titulo1, [390, 70])
		pantalla.blit(Titulo2, [240, 170])
		pantalla.blit(Jugador1, [300, 375])
		pantalla.blit(Jugador2, [300, 495])
		pantalla.blit(NumDim, [100, 615])
		pantalla.blit(nombre1, [750, 375])
		pantalla.blit(nombre2, [750, 495])
		pantalla.blit(trianguloInv2, [10, 615])

		Mensj = texto.render(mensj, True, (0,0,0))
		pantalla.blit(Mensj, [400, 320])

		NAct = N

		Num = nombres.render(NAct.lstrip("0"), True, (0,0,0))
		pantalla.blit(Num, [1000, 615])

		pygame.display.update()
		reloj1.tick(20)


	return int(N)

def pantallaUniJug(player: Jugador) -> int:
	"""Representa una pantalla donde se jugara una partida individual y se le pide al jugador su nombre, asi como la
			dimension del supertablero.

	ENTRADAS-SALIDAS:
	player: Jugador, contiene los datos del jugador.
	SALIDAS:
	int, dimension del Super-Tablero elegida por el jugador."""

	# Dimension del tablero
	N = "0"

	# Indica cuando el jugador ya termino de colocar el nombre
	done = False

	mensj = "Jugador indique su nombre: "

	while not done:
		for evt in pygame.event.get():
			if evt.type == KEYDOWN:
				if evt.unicode.isalpha() and len(player.nombre) < 8:
					player.nombre += evt.unicode
				elif evt.key == K_BACKSPACE:
					player.nombre = player.nombre[:-1]
				elif evt.key == K_RETURN and len(player.nombre) > 0:
					done = True
			if evt.type == pygame.QUIT:
				pygame.quit()

		pantalla.blit(fondo, [0, 0]) 
		pantalla.blit(Titulo1, [390, 70])
		pantalla.blit(Titulo2, [240, 170])
		pantalla.blit(JugadorSolo, [300, 405])
		pantalla.blit(NumDim, [100, 550])
		pantalla.blit(Recomendacion, [100, 620])
		pantalla.blit(trianguloInv2, [180, 405])

		Mensj = texto.render(mensj, True, (0,0,0))
		pantalla.blit(Mensj, [400, 320])

		nombre1 = nombres.render(player.nombre, True, (0,0,0))
		pantalla.blit(nombre1, [750, 405])

		pygame.display.update()
		reloj1.tick(20) 

	mensj = "Indiquen   la   dimension   del   super-tablero."

	# Indica cuando el usuario ya decidio la dimension del super-tablero
	done = False

	while not done:
		for evt in pygame.event.get():
			if evt.type == KEYDOWN:
				if evt.unicode.isnumeric() and len(N) < 3:
					N += evt.unicode
				elif evt.key == K_BACKSPACE and len(N) > 1:
					N = N[:-1]
				elif evt.key == K_RETURN and len(N) > 1 and int(N)<12:
					done = True
				elif evt.key == K_RETURN and len(N) > 1 and int(N)>11:
					mensj = "El   supertablero   no   puede   ser   tan   grande."
			if evt.type == pygame.QUIT:
				pygame.quit()

		pantalla.blit(fondo, [0, 0]) 
		pantalla.blit(Titulo1, [390, 70])
		pantalla.blit(Titulo2, [240, 170])
		pantalla.blit(JugadorSolo, [300, 405])
		pantalla.blit(NumDim, [100, 550])
		pantalla.blit(Recomendacion, [100, 620])
		pantalla.blit(nombre1, [750, 405])
		pantalla.blit(trianguloInv2, [10, 550])

		Mensj = texto.render(mensj, True, (0,0,0))
		pantalla.blit(Mensj, [400, 320])

		NAct = N

		Num = nombres.render(NAct.lstrip("0"), True, (0,0,0))
		pantalla.blit(Num, [1000, 550])

		pygame.display.update()
		reloj1.tick(20)


	return int(N)

def pantallaCargarPart() -> bool:
	"""Funcion que representa una pantalla donde se le pregunta al usuario si desea cargar la ultima partida guardada.

	SALIDAS:
	bool, indica si el usuario desea cargar la ultima partida guardada."""

	# Variable que mueve la flecha para indicar al jugador si esta en la opcion "si" o "no"
	k = 0

	while True:
		for evt in pygame.event.get():
			if evt.type == KEYDOWN:
				if evt.key == K_UP:
					k = 0
				if evt.key == K_DOWN:
					k = 1
				if evt.key == K_RETURN and k == 0:
					return True
				if evt.key == K_RETURN and k == 1:
					return False
			if evt.type == pygame.QUIT:
				pygame.quit()

		pantalla.blit(fondo, [0, 0]) 
		pantalla.blit(Titulo1, [390, 70])
		pantalla.blit(Titulo2, [240, 170])
		pantalla.blit(CargarPartida, [20, 375])
		pantalla.blit(YES, [300, 495])
		pantalla.blit(NOT, [300, 615])
		pantalla.blit(trianguloInv2, [200, 500 + k*120])


		pygame.display.update()
		reloj1.tick(20)

def partida(T: [[[int]]], player1: Jugador, player2: Jugador, turno: int, UltMen: str, bot: bool, cargado: bool) -> bool:
	"""Pantalla donde se realiza un juego.

	ENTRADAS-SALIDAS:
	T: [[[int]]], matriz tridimensional que representa al Super-Tablero.
	player1: Jugador, contiene los datos del jugador 1.
	player2: Jugador, contiene los datos del jugador 2.
	ENTRADAS:
	turno: int, indica a que jugador le toca jugar.
	UltMen: str, contiene el ultimo mensaje que se le desea mostrar a los jugadores.
	bot: bool, indica si esta jugando un bot o no.
	cargado: bool, indica si es una partida cargada.
	SALIDAS:
	bool, es True si se termino la partida, False en caso contrario."""

	UltMen = "" # En esta variable se guardara el ultimo mensaje importante del juego

	jugada = [0, 0, 0] # En esta variable se guardara la jugada de los jugadores (solo se usara para indicar cual fue la 
	#						jugada del bot)

	valido = True # Indica si una jugada fue valida

	first = cargado # Guardamos el valor de cargado. Esta variable indicara si es el primer turno luego de cargar una partida

	while quedanFichas(T):
		if bot and valido and not first:
			UltMen = actualizar(T, player1, player2, UltMen, turno, jugada)
		elif first:
			first = False

		# Le pedimos al usuario correspondiente el taablero, fila y columna donde quiere jugar 
		tablero, fila, columna, salir = pedirJugada(T, player1, player2, UltMen, turno, bot)
		jugada = [tablero, fila, columna]

		# Mensaje que se le va informando a los jugadores
		UltMen = ""

		valido = esValida(T, tablero, fila, columna)
		if valido and not salir:

			reflejarJugada(T, tablero, fila, columna, turno)

			if turno==player1.turn:
				UltMen = hayLinea(T, tablero, fila, columna, player1)
				turno = 3 - turno
			else:
				UltMen = hayLinea(T, tablero, fila, columna, player2)
				turno = 3 - turno
		elif not salir:
			UltMen = "La  jugada  no  es  valida"
		else:
			return False

	return True

def pantallaPrinc() -> bool:
	"""Funcion que representa la pantalla principal, tiene las opciones de jugar multijugador, contra la computadora o 
			salir del juego

	SALIDAS:
	bool, indica si se desea jugar una partida multijugador, o no."""

	# Indica cuando el usuario ya decidio el modo de juego
	done = False

	# Variable que mueve la flecha para indicarle al usuario en cual opcion se encuentra
	k = 0

	while not done:
		for evt in pygame.event.get():
			if evt.type == KEYDOWN:
				if evt.key == K_UP and k > 0:
					k -= 1
				if evt.key == K_DOWN and k < 2:
					k += 1
				if evt.key == K_RETURN and k == 0:
					return True
				if evt.key == K_RETURN and k == 1:
					return False
				if evt.key == K_RETURN and k == 2:
					pygame.quit()
			if evt.type == pygame.QUIT:
				pygame.quit()

		pantalla.blit(fondo, [0, 0]) 
		pantalla.blit(Titulo1, [390, 70])
		pantalla.blit(Titulo2, [240, 170])
		pantalla.blit(MultJug, [375, 375])
		pantalla.blit(Computer, [375, 495])
		pantalla.blit(Exit, [375, 615])
		pantalla.blit(triangulo2, [900, 380 + k*120])

		pygame.display.update()
		reloj1.tick(20)

def actualizar(T: [[[int]]], player: Jugador, bot: Jugador, UltMen: str, turno: int, jugada: [int]) -> str:
	"""Funcion que actualiza momentaneamente la pantalla de la partida.

	ENTRADAS:
	T: [[[int]]], matriz tridimensional que representa al Super-Tablero.
	player: Jugador, contiene los datos del jugador.
	bot: Jugador, contiene los datos del bot.
	UltMen: str, contiene el ultimo mensaje que se le desea mostrar a los jugadores.
	turno: int, indica a que jugador le toca jugar.
	jugada: [int], contiene la ultima jugada realizada por alguno de los jugadores.
	SALIDAS:
	str, nuevo mensaje que se le desea mostrar a los jugadores."""

	done = False # Indica si ya ha pasado cierto tiempo

	time = 0 # Se usa para saber cuanto tiempo ha pasado desde que se llamo a la funcion

	ultMen = UltMen # Guardamos el ultimo mensaje que se desea dar a los jugadores

	while not done:
		for evt in pygame.event.get():
			if evt.type == pygame.QUIT:
				pygame.quit()

		mostarPuntajes(player, bot)

		if turno == player.turn and not supTabEmpty(T):
			IndJug = texto.render("El  Bot  jugo  en  el  tablero  " + str(jugada[0] + 1) + ",  fila  " + \
				str(jugada[1] + 1) + "  y  columna  " + str(jugada[2] + 1), True, (0,0,0))
			pantalla.blit(IndJug, [200, 200])
		elif turno == bot.turn:
			IndJug = texto.render("El  Bot  esta  eligiendo  su  siguiente  jugada.  Espere  por  favor...", True, (0,0,0))
			pantalla.blit(IndJug, [200, 200])

		Mens = texto.render(ultMen, True, (0,0,0))
		pantalla.blit(Mens, [100, 260])
		pantalla.blit(Tab, [10, 230])
		pantalla.blit(Fil, [460, 230])
		pantalla.blit(Col, [910, 230])
		pantalla.blit(Tablero, [980, 320])

		dibujarTab(T[jugada[0]], player, bot, jugada[0])

		pygame.display.update()

		time += 1

		if time == 10:
			done = True

		reloj1.tick(20)

	if turno == player.turn and not supTabEmpty(T) and ultMen != "":
		return ultMen + "  El  Bot  jugo  en  el  tablero  " + str(jugada[0] + 1) + ",  fila  " + str(jugada[1] + 1) +\
		 "  y  columna  " + str(jugada[2] + 1)
	elif turno == player.turn and not supTabEmpty(T) and ultMen == "":
		return "El  Bot  jugo  en  el  tablero  " + str(jugada[0] + 1) + ",  fila  " + str(jugada[1] + 1) +\
		 "  y  columna  " + str(jugada[2] + 1)
	else:
		return ultMen



############################## SUBPROGRAMAS CORRESPONDIENTES A LA I.A. ############################################
def supTabEmpty(T: [[[int]]]) -> bool:
	"""Funcion que verifica si el Super-Tablero esta vacio.

	ENTRADAS:
	T: [[[int]]], matriz tridimensional que representa al Super-Tablero.
	SALIDAS:
	bool, indica si el Super-Tablero esta vacio."""

	vacio = all( all( all(T[i][j][k] == 0 for k in range(0, len(T))) for j in range(0, len(T))) for i in range(0, len(T)))
	return vacio

def tabVacio(Tab: [[int]]) -> bool:
	"""Funcion que verifica si un tablero esta vacio.

	ENTRADAS:
	Tab: [[int]], matriz que representa al tablero.
	SALIDAS:
	bool, indica si el tablero esta vacio."""

	vacio = all( all(Tab[i][j] == 0 for j in range(0, len(Tab)) ) for i in range(0, len(Tab)) )
	return vacio

def tabLleno(Tab: [[int]]) -> bool:
	"""Funcion que verifica si un tablero esta lleno.

	ENTRADAS:
	Tab: [[int]], matriz que representa al tablero.
	SALIDAS:
	bool, indica si el tablero esta lleno."""

	lleno = all( all(Tab[i][j] != 0 for j in range(0, len(Tab)) ) for i in range(0, len(Tab)) )
	return lleno

def copiarSupTab(T: [[[int]]]) -> [[[int]]]:
	"""Funcion que copia todo un Super-Tablero.

	ENTRADAS:
	T: [[[int]]], matriz tridimensional que representa al Super-Tablero.
	SALIDAS:
	[[[int]]], copia del Super-Tablero."""

	M = [[[T[k][j][i] for i in range(0, len(T))] for j in range(0, len(T))] for k in range(0, len(T))]
	return M

def obtenerPuntos(T: [[[int]]], tablero: int, fila: int, columna: int, player: Jugador) -> int:
	"""Funcion que retorna cuantas lineas se obtendrian en el Super-Tablero T con la jugada: tablero, fila, columna.

	ENTRADAS:
	T: [[[int]]], matriz tridimensional que representa al Super-Tablero.
	tablero: int, indica el tablero donde se realizo la jugada.
	fila: int, indica la fila donde se realizo la jugada.
	columna: int, indica la columna donde se realizo la jugada.
	player: Jugador, contiene los datos del jugador que realizo esta jugada.
	SALIDAS:
	int, contiene cuantas lineas se harian con la jugada indicada."""

	lineas = 0

	if hayLineaHorizontal(T, tablero, fila, player, True):
		lineas += 1
	if hayLineaVertical(T, tablero, columna, player, True):
		lineas += 1
	if hayLineaDiagonal(T, tablero, fila, columna, player, True):
		lineas += 1
	if hayLineaDiagonalInversa(T, tablero, fila, columna, player, True):
		lineas += 1
	if hayLineaEnZ(T, fila, columna, player, True):
		lineas += 1

	return lineas

def tabsEmpty(T: [[[int]]]) -> bool:
	"""Funcion que cuenta los tableros vacios en un Super-Tablero.

	ENTRADAS:
	T: [[[int]]], matriz tridimensional que representa al Super-Tablero.
	SALIDAS:
	int, numero de tableros vacios en el Super-Tablero."""

	vacios = 0

	for i in range(0, len(T)):
		if all( all( T[i][j][k] == 0 for j in range(0, len(T))) for k in range(0, len(T))):
			vacios += 1

	return vacios

def emptyFull(T: [[[int]]]) -> bool:
	"""Funcion que verifica si todos los tableros del Super-Tablero estan llenos o vacios. Si hay alguno con 
		casillas vacias y otras ocupadas, retornara False.

	ENTRADAS:
	T: [[[int]]], matriz tridimensional que representa al Super-Tablero.
	SALIDAS:
	bool, indica si todos los tableros del Super-Tablero estan llenos o vacios"""

	emptyFull = True

	for i in range(0, len(T)):
		emptyFull = emptyFull and (tabVacio(T[i]) or tabLleno(T[i]))

	return emptyFull

def miniMax(T: [[[int]]], n: int, puntos: int, player: Jugador, bot: Jugador, Max: bool, p: float, first: bool) -> [int, int, int, float]:
	"""Funcion recursiva que calcula la jugada optima dado un estado del Super-Tablero actual.

	ENTRADAS:
	T: [[[int]]], matriz tridimensional que representa al Super-Tablero.
	n: int, profundidad de la funcion. Mientras mayor sea este numero, mas recursiones realizara la funcion, y por lo tanto,
			mas optima sera la jugada resultante. Sin embargo, tardara mas en llegar a la solucion.
	player: Jugador, contiene los datos del jugador.
	bot: Jugador, contiene los datos del bot.
	Max: bool, indica si hay que maximizar la proxima jugada.
	p: float, parametro que indica la importancia de la jugada actual. Su valor inicial debe ser 1 y va disminuyendo con cada
			recursion de la funcion. Es decir, mientras mas futura sea la jugada, menos importancia tendra.
	first: bool, indica si es la primera llamada de la funcion. Se usa para aumentar la importancia de las lineas hechas
			inmediatamente
	SALIDAS:
	[int, int, int, float], los tres enteros indican la jugada optima (tablero, fila y columna respectivamente). Mientras
			que el float indica la puntuacion aproximada de esta jugada.

	COTA: n+1"""
	
	lineas = puntos # Indica cuantos puntos se harian aproximadamente realizando una jugada particular

	vacio = supTabEmpty(T) # Indica si el Super-Tablero esta vacio

	jugadas = [] # Guardamos una lista con las posibles jugadas validas.
	for tablero in range(0, len(T)):

		# El siguiente if sirve para reducir la cantidad de jugadas que debe procesar la IA. Si el Super-Tablero esta vacio
		# solo eligira una aleatoria; si hay menos de dos tableros vacios, considerara todas las posibles jugadas;
		# si hay mas de un tablero vacio, solo considerara aquellos tableros con alguna ficha; y finalmente, si todos los
		# tableros estan llenos o vacio, considerara todas las posibles jugadas
		if (vacio or (tabsEmpty(T) < 2) or (tabsEmpty(T) > 1 and not tabVacio(T[tablero])) or emptyFull(T)  ):
			for fila in range(0, len(T)):
				for columna in range(0, len(T)):
					if esValida(T, tablero, fila, columna):
						jugadas.append([tablero, fila, columna, lineas])

	# Vamos a maximizar los puntos (es decir, que le toca al bot)
	if Max:
		for jugada in jugadas:
			C = copiarSupTab(T) # Creamos un Super-Tablero auxiliar

			reflejarJugada(C, jugada[0], jugada[1], jugada[2], bot.turn) # Aplicamos cada posible jugada en las guardadas 
									# anteriormente en el Super-Tablero auxiliar

			lineas += (p+5*int(first))*obtenerPuntos(C, jugada[0], jugada[1], jugada[2], bot) # Si se hizo alguna linea,
									# al parametro lineas lo aumentamos. La variable p sirve para disminuir el peso de cada
									# jugada futura. La variable first hace que le de prioridad a las lineas que se pueden
									# hacer en el turno inmediato

			# Si quedan fichas en el Super-Tablero auxiliar, aun la profundidad de la recursion no es cero (esto lo indica
			# la variable n) y el Super-Tablero original no esta vacio (esto para que no analice la primera jugada del juego, 
			# sino que elija aleatoriamente), entonces se aplica otra vez miniMax de cada posible jugada
			if quedanFichas(C) and n > 0 and not vacio:
				jugada[3] = miniMax(C, n-1, lineas, player, bot, False, p*(1/2), False)[3]

			# En caso contrario, el parametro de lineas de cada jugada seran las lineas que se hicieron directamente con dicha 
			# jugada
			else:
				jugada[3] = lineas

	# Vamos a minimizar los puntos (es decir, que le toca al player)
	else:
		for jugada in jugadas:
			C = copiarSupTab(T) # Creamos un Super-Tablero auxiliar

			reflejarJugada(C, jugada[0], jugada[1], jugada[2], player.turn) # Aplicamos cada posible jugada en las guardadas 
									# anteriormente en el Super-Tablero auxiliar

			lineas -= (p+2*int(first))*obtenerPuntos(C, jugada[0], jugada[1], jugada[2], player) # Si se hizo alguna linea,
									# al parametro lineas lo disminuimos. La variable p sirve para disminuir el peso de cada
									# jugada futura. La variable first hace que le de prioridad a las lineas que se pueden
									# hacer en el turno inmediato

			# Si quedan fichas en el Super-Tablero auxiliar, aun la profundidad de la recursion no es cero (esto lo indica
			# la variable n) y el Super-Tablero original no esta vacio (esto para que no analice la primera jugada del juego, 
			# sino que elija aleatoriamente), entonces se aplica otra vez miniMax de cada posible jugada
			if quedanFichas(C) and n > 0 and not vacio:
				jugada[3] = miniMax(C, n-1, lineas, player, bot, True, p*(1/2), False)[3]
			# En caso contrario, el parametro de lineas de cada jugada seran las lineas que se hicieron directamente con dicha 
			# jugada
			else:
				jugada[3] = lineas

	# Verificamos cual fue la mayor puntuacion entre todas las jugadas analizadas
	maxPuntos = max(jugada[3] for jugada in jugadas)

	# En esta variable guardaremos las jugadas con la puntuacion maxima (ya que varias pueden dar este parametro igual)
	bestJugadas = []

	# Esta variable guardara el promedio de la puntuacion obtenida en todas las jugadas
	promedio = 0

	for jugada in jugadas:
		promedio += jugada[3]
		if jugada[3] == maxPuntos:
			bestJugadas.append(jugada)

	promedio /= len(jugadas)

	# Elegimos alguna de las jugadas con la mejor puntuacion de manera aleatoria
	jugadaDef = random.choice(bestJugadas)

	# La puntuacion de esta jugada sera el promedio de las puntuaciones de las jugadas en esta capa 
	jugadaDef[3] = promedio


	return jugadaDef



def main():
	"""Subprograma Principal."""

	while True:
		# Mientras la variable otro sea True, se repetira la partida entre los dos jugadores
		otro = True

		# El primer turno siempre es 1
		turno = 1

		# Creamos la matriz tridimensional que representara al super-tablero
		T = []

		# Variable que indica si vamos a jugar una partida cargada
		cargarPartida = False

		# Abrimos el archivo con los datos de la ultima partida multijugador y contra el bot
		ultimaPartidaMulti = open('Datos ultPartida.txt', 'r')
		ultimaPartidaBot = open('Datos ultPartida Bot.txt', 'r')

		# Entramos al menu principal
		multijugador = pantallaPrinc()

		# Si el archivo con los datos de la ultima partida esta vacio, significa que no hay ninguna partida cargada y por lo tanto no es necesario entrar a la pantalla donde se debe preguntar si desea cargar la ultima aprtida
		if (ultimaPartidaMulti.readlines()[0] != " " and multijugador) or (ultimaPartidaBot.readlines()[0] != " " and not multijugador):
			cargarPartida = pantallaCargarPart()

		# Cerramos el archivo
		ultimaPartidaMulti.close()



		# Si se decidio jugar una partida multijugador
		if multijugador :
			while otro:
				# Creamos las dos instancias de la clase Jugador, los cuales tendran la informacion de ambos jugadores
				player1 = Jugador("", randint(1, 2))
				player2 = Jugador("", 3 - player1.turn)

				# Si decidimos jugar una partida nueva, llamamos a la pantalla donde los jugadores deciden sus nombres y la dimension del super-tablero
				if not cargarPartida:
					N = pantallaMultiJug(player1, player2)

				while otro:
					# Restauramos a 0 los puntajes de ambos jugadores
					player1.filas = 0
					player1.columnas = 0
					player1.diagonales = 0
					player1.enZ = 0

					player2.filas = 0
					player2.columnas = 0
					player2.diagonales = 0
					player2.enZ = 0


					# Restauramos a [] las lineas hechas de ambos jugadores
					player1.lineasFila = []
					player1.lineasCol = []
					player1.lineasDiag = []
					player1.lineasEnZ = []

					player2.lineasFila = []
					player2.lineasCol = []
					player2.lineasDiag = []
					player2.lineasEnZ = []

					# Vaciamos el super-tablero
					if not cargarPartida:
						T = [[[0 for i in range(0, N)] for j in range(0, N)] for k in range(0, N)]

					# Si se decide jugar una partida cargada
					else:
						with open('Datos ultPartida.txt', 'r') as f:
							lineas = f.readlines()

							# Leemos la dimension del supertablero
							N = int(lineas[0])

							# Leemos los datos del Jugador 1
							player1.nombre = lineas[1].replace("\n", "")
							player1.filas = int(lineas[2])
							player1.columnas = int(lineas[3])
							player1.diagonales = int(lineas[4])
							player1.enZ = int(lineas[5])

							first = True

							for char in lineas[6]:
								if char in "0123456789":
									if first:
										array = [int(char)]
										first = False
									else:
										first = True
										array.append(int(char))
										player1.lineasFila.append(array)


							for char in lineas[7]:
								if char in "0123456789":
									if first:
										array = [int(char)]
										first = False
									else:
										first = True
										array.append(int(char))
										player1.lineasCol.append(array)

							for char in lineas[8]:
								if char in "0123456789":
									if first:
										array = [int(char)]
										first = False
									else:
										first = True
										array.append(int(char))
										player1.lineasDiag.append(array)

							for char in lineas[9]:
								if char in "0123456789":
									if first:
										array = [int(char)]
										first = False
									else:
										first = True
										array.append(int(char))
										player1.lineasEnZ.append(array)


							player1.turn = int(lineas[10])
							player1.wins = int(lineas[11])


							# Leemos los datos del Jugador 2
							player2.nombre = lineas[12].replace("\n", "")
							player2.filas = int(lineas[13])
							player2.columnas = int(lineas[14])
							player2.diagonales = int(lineas[15])
							player2.enZ = int(lineas[16])

							first = True
							for char in lineas[17]:
								if char in "0123456789":
									if first:
										array = [int(char)]
										first = False
									else:
										first = True
										array.append(int(char))
										player2.lineasFila.append(array)


							for char in lineas[18]:
								if char in "0123456789":
									if first:
										array = [int(char)]
										first = False
									else:
										first = True
										array.append(int(char))
										player2.lineasCol.append(array)

							for char in lineas[19]:
								if char in "0123456789":
									if first:
										array = [int(char)]
										first = False
									else:
										first = True
										array.append(int(char))
										player2.lineasDiag.append(array)

							for char in lineas[20]:
								if char in "0123456789":
									if first:
										array = [int(char)]
										first = False
									else:
										first = True
										array.append(int(char))
										player2.lineasEnZ.append(array)

							player2.turn = int(lineas[21])
							player2.wins = int(lineas[22])


							turno = int(lineas[23])

						# Leemos los datos del Super-Tablero
						with open('Tableros ultPartida.txt', 'r') as f:
							lineas = f.readlines()

							ToneDim = []
							TbiDim = []
							for char in lineas[0]:
								if char in "0123456789":
									ToneDim.append(int(char))

							for i in range(0, N*N*N):
								if i % N == 0:
									array = [ToneDim[k] for k in range(i, i + N)]
									TbiDim.append(array)

							for i in range(0, N*N):
								if i % N == 0:
									array = [TbiDim[k] for k in range(i, i + N)]
									T.append(array)
									

					# Vaciamos el ultimo mensaje
					UltMen = ""

					# Llamamos a una partida. Termino sera True si la partida llega a su final
					termino = partida(T, player1, player2, turno, UltMen, False, cargarPartida)

					# Sumamos los puntos que obtuvieron el jugador1 y el jugador2 respectivamente
					total1 = player1.filas + player1.columnas + player1.diagonales + player1.enZ
					total2 = player2.filas + player2.columnas + player2.diagonales + player2.enZ

					# Verificamos si los jugadores quieren jugar otra partida
					if termino:
						otro = resultado(T, player1, player2, total1, total2)

						turno = 3 - turno

						# Si la partida actual era una partida cargada, entonces eliminamos los datos de dicha partida
						if cargarPartida:
							with open('Datos ultPartida.txt', 'w') as f:
								f.write(" ")
							with open('Tableros ultPartida.txt', 'w') as f:
								f.write(" ")

						cargarPartida = False

					else:
						otro = False

		else:
			while otro:
				# Creamos las dos instancias de la clase Jugador, los cuales tendran la informacion del jugador y del bot respectivamente
				player1 = Jugador("", randint(1, 2))
				player2 = Jugador("Bot", 3 - player1.turn)

				# Si decidimos jugar una partida nueva, llamamos a la pantalla donde los jugadores deciden sus nombres y la dimension del super-tablero
				if not cargarPartida:
					N = pantallaUniJug(player1)

				while otro:
					# Restauramos a 0 los puntajes de ambos jugadores
					player1.filas = 0
					player1.columnas = 0
					player1.diagonales = 0
					player1.enZ = 0

					player2.filas = 0
					player2.columnas = 0
					player2.diagonales = 0
					player2.enZ = 0


					# Restauramos a [] las lineas hechas de ambos jugadores
					player1.lineasFila = []
					player1.lineasCol = []
					player1.lineasDiag = []
					player1.lineasEnZ = []

					player2.lineasFila = []
					player2.lineasCol = []
					player2.lineasDiag = []
					player2.lineasEnZ = []

					# Vaciamos el super-tablero
					if not cargarPartida:
						T = [[[0 for i in range(0, N)] for j in range(0, N)] for k in range(0, N)]

					# Si se decide jugar una partida cargada
					else:
						with open('Datos ultPartida Bot.txt', 'r') as f:
							lineas = f.readlines()

							# Leemos la dimension del supertablero
							N = int(lineas[0])

							# Leemos los datos del Jugador 1
							player1.nombre = lineas[1].replace("\n", "")
							player1.filas = int(lineas[2])
							player1.columnas = int(lineas[3])
							player1.diagonales = int(lineas[4])
							player1.enZ = int(lineas[5])

							first = True

							for char in lineas[6]:
								if char in "0123456789":
									if first:
										array = [int(char)]
										first = False
									else:
										first = True
										array.append(int(char))
										player1.lineasFila.append(array)


							for char in lineas[7]:
								if char in "0123456789":
									if first:
										array = [int(char)]
										first = False
									else:
										first = True
										array.append(int(char))
										player1.lineasCol.append(array)

							for char in lineas[8]:
								if char in "0123456789":
									if first:
										array = [int(char)]
										first = False
									else:
										first = True
										array.append(int(char))
										player1.lineasDiag.append(array)

							for char in lineas[9]:
								if char in "0123456789":
									if first:
										array = [int(char)]
										first = False
									else:
										first = True
										array.append(int(char))
										player1.lineasEnZ.append(array)


							player1.turn = int(lineas[10])
							player1.wins = int(lineas[11])


							# Leemos los datos del Jugador 2
							player2.nombre = lineas[12].replace("\n", "")
							player2.filas = int(lineas[13])
							player2.columnas = int(lineas[14])
							player2.diagonales = int(lineas[15])
							player2.enZ = int(lineas[16])

							first = True
							for char in lineas[17]:
								if char in "0123456789":
									if first:
										array = [int(char)]
										first = False
									else:
										first = True
										array.append(int(char))
										player2.lineasFila.append(array)


							for char in lineas[18]:
								if char in "0123456789":
									if first:
										array = [int(char)]
										first = False
									else:
										first = True
										array.append(int(char))
										player2.lineasCol.append(array)

							for char in lineas[19]:
								if char in "0123456789":
									if first:
										array = [int(char)]
										first = False
									else:
										first = True
										array.append(int(char))
										player2.lineasDiag.append(array)

							for char in lineas[20]:
								if char in "0123456789":
									if first:
										array = [int(char)]
										first = False
									else:
										first = True
										array.append(int(char))
										player2.lineasEnZ.append(array)

							player2.turn = int(lineas[21])
							player2.wins = int(lineas[22])


							turno = int(lineas[23])

						# Leemos los datos del Super-Tablero
						with open('Tableros ultPartida Bot.txt', 'r') as f:
							lineas = f.readlines()

							ToneDim = []
							TbiDim = []
							for char in lineas[0]:
								if char in "0123456789":
									ToneDim.append(int(char))

							for i in range(0, N*N*N):
								if i % N == 0:
									array = [ToneDim[k] for k in range(i, i + N)]
									TbiDim.append(array)

							for i in range(0, N*N):
								if i % N == 0:
									array = [TbiDim[k] for k in range(i, i + N)]
									T.append(array)
									

					# Vaciamos el ultimo mensaje
					UltMen = ""

					# Llamamos a una partida. Termino sera True si la partida llega a su final
					termino = partida(T, player1, player2, turno, UltMen, True, cargarPartida)

					# Sumamos los puntos que obtuvieron el jugador1 y el jugador2 respectivamente
					total1 = player1.filas + player1.columnas + player1.diagonales + player1.enZ
					total2 = player2.filas + player2.columnas + player2.diagonales + player2.enZ

					# Verificamos si los jugadores quieren jugar otra partida
					if termino:
						otro = resultado(T, player1, player2, total1, total2)

						turno = 3 - turno

						# Si la partida actual era una partida cargada, entonces eliminamos los datos de dicha partida
						if cargarPartida:
							with open('Datos ultPartida Bot.txt', 'w') as f:
								f.write(" ")
							with open('Tableros ultPartida Bot.txt', 'w') as f:
								f.write(" ")

						cargarPartida = False

					else:
						otro = False

main()