import tetris
import gamelib
import csv
import pickle
import  time

ESPERA_DESCENDER = 8


def dibujar_superficie(juego):
  '''Se dibujara la grilla del tetris'''
  gamelib.draw_image('img/fondo6.gif', -80, 10)
  ancho, alto = tetris.dimensiones(juego)
  gamelib.draw_line(600, 250, 900, 250, fill='white', width=3)
  gamelib.draw_text('PRÓXIMA PIEZA:', 630, 10, fill='white', anchor='nw')
  for x in range (0, 600, 66):
    gamelib.draw_line(x, 0, x, 900, fill='white', width=2) 
  for y in range (0, 900, 50):
    gamelib.draw_line(0, y, 595, y, fill='white', width=2)  
  for y in range(alto):
        for x in range(ancho):
            if tetris.hay_superficie(juego, x, y):  
              gamelib.draw_rectangle(x*66, y*50, (x+1)*66, (y+1)*50, outline='white', fill='purple')
  

def dibujar_pieza(juego):
  '''Se dibujara cada pieza del tetris'''
  pieza_actual = tetris.pieza_actual(juego)
  for x, y in pieza_actual:
      gamelib.draw_rectangle(x*66, y*50, (x+1)*66, (y+1)*50, outline='white', fill='red')


def dibujar_siguiente(juego, siguiente):
  '''Se dibujara la proxima pieza'''
  for x,y in siguiente:
    gamelib.draw_rectangle(602+x*66, 45+y*50, 602+(x+1)*66, 45+(y+1)*50, outline='white', fill='salmon')
    


def leer_teclas():
  '''Recorre un archivo con las teclas y devuelve una lista con ellas'''
  with open ('teclas.txt') as teclas:
    lista_t = []
    for linea in teclas:
      for palabra in linea.split():
        if palabra== 'w' or palabra == 'a' or palabra == 'd' or palabra == 's' or palabra == 'g' or palabra =='c' or palabra == 'Esc':
          lista_t.append(palabra)       
  return(sorted(lista_t)) 
  

def procesar_rotacion(cadena):
  '''Procesa las rotaciones'''
  resultado = []
  res = cadena.split(';')
  for elem in res:
    sub = elem.split(', ')
    resultado.append(sub)
  x = tuple([tuple(map(int, elemento[0].split(','))) for elemento in resultado])
  return x


def procesar_linea(linea):
  '''Procesa una linea de  un archivo'''
  a = linea.split()
  a = a[:-2]
  resultado = []
  for cadena in a:
    cadena_nueva = procesar_rotacion(cadena)
    resultado.append(cadena_nueva)
  return tuple(resultado) 

def leer_rotaciones():
  '''Recorre un archivo con las piezas, y las interpreta'''
  with open ('piezas.txt') as rotaciones:
    rotacion = []
    for linea in rotaciones:
      a = procesar_linea(linea)
      rotacion.append(a)
  res = rotacion
  res = res[:-3]
  return tuple(res)




def guardar_partida(juego):
    '''Guarda la partida en el momento actual'''
    with open('partida_guardada.txt', "wb") as partida:
        pickle.dump(juego, partida, pickle.HIGHEST_PROTOCOL)


def recuperar_partida():
    '''Devuelve la ultima instancia del juego en la que se guardo la partida'''
    with open('partida_guardada.txt', "rb") as partida:
        return pickle.load(partida)
     

def puntuaciones(tiempo):
  nombre = gamelib.input('Ingrese su nombre')
  with open('puntuaciones.txt', 'a') as puntuaciones:
    puntuaciones.write(nombre + ' ')
    puntuaciones.write(str(tiempo) + ' ' + 'segundos')
    puntuaciones.write('\n')

def puntuaciones_lista():
  lista = []
  with open('puntuaciones.txt', 'r') as puntuaciones:
    for linea in puntuaciones:
      linea = linea.rstrip('\n').split()
      lista.append(linea)
    return lista

def ordenar_puntuaciones():
  gamelib.draw_rectangle(595, 250, 800, 900, outline='white', fill='#000')
  gamelib.draw_text('TOP MEJORES TIEMPOS: ', 600, 270, size=13, fill='#fff', anchor='nw')
  puntuaciones = puntuaciones_lista()
  tiempos = []
  e = 350
  a = 0
  for i in range(len(puntuaciones)):
    tiempo = float(puntuaciones[i][1])
    tiempos.append(tiempo)
  tiempos_ordenados = sorted(tiempos)
  for elemento in tiempos_ordenados:
    if a >= 10:
      return
    gamelib.draw_text(f'{elemento}, segs', 596, e, size=12, fill='#fff', anchor='nw')  
    e+=50
    a+=1



def main():
    # Inicializar el estado del juego
    #siguiente_pieza = tetris.generar_pieza()
    siguiente = tetris.generar_pieza()
    t1= time.time()
    juego = tetris.crear_juego(tetris.generar_pieza())
    ancho, alto = tetris.dimensiones(juego)
    lista_teclas = leer_teclas()  
    gamelib.resize(800, 900)
    timer_bajar = ESPERA_DESCENDER
    while gamelib.loop(fps=30):
        gamelib.draw_begin()
        dibujar_superficie(juego)
        dibujar_pieza(juego)
        dibujar_siguiente(juego, siguiente)
        gamelib.draw_end()  
        for event in gamelib.get_events():
          if not event:
              break
          if event.type == gamelib.EventType.KeyPress:
              tecla = event.key
              if tecla == lista_teclas[1]:
                juego = tetris.mover(juego, -1)
              if tecla == lista_teclas[3]:
                juego = tetris.mover(juego, 1) 
              if tecla == lista_teclas[5]:
                juego = tetris.mover(juego, 2)
              if tecla == lista_teclas[0]:
                return
              if tecla == lista_teclas[6]:
                juego = tetris.rotar(juego)    
              if tecla == lista_teclas[4]:
                guardar_partida(juego)
              if tecla == lista_teclas[2]:
                juego = recuperar_partida()                           
              # Actualizar el juego, según la tecla presionada
        timer_bajar -= 1
        if timer_bajar == 0:  
            timer_bajar = ESPERA_DESCENDER 
            juego, siguiente_pieza = tetris.avanzar(juego, siguiente)
            if siguiente_pieza:
              siguiente = tetris.generar_pieza()
            if tetris.terminado(juego):
              gamelib.draw_image('img/perdiste.gif', 50, 200)
              t2 = time.time()
              tiempo_final = t2- t1
              gamelib.draw_rectangle(0, 0, 595, 60, outline='white', fill='salmon')
              gamelib.draw_text('Tu tiempo fue de {} segundos'.format(tiempo_final), 10, 17, fill='#000', size=18, anchor='nw')
              puntuaciones(tiempo_final)
              break

    while gamelib.is_alive():
      ordenar_puntuaciones()
      event = gamelib.wait(gamelib.EventType.KeyPress)
          # Descender la pieza automáticamente
gamelib.init(main)