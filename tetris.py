import gamelib
import random


ANCHO_JUEGO, ALTO_JUEGO = 9, 18
IZQUIERDA, DERECHA = -1, 1

def procesar_rotacion(cadena):
  resultado = []
  res = cadena.split(';')
  for elem in res:
    sub = elem.split(', ')
    resultado.append(sub)
  x = tuple([tuple(map(int, elemento[0].split(','))) for elemento in resultado])
  return x

def procesar_linea(linea):
  a = linea.split()
  a = a[:-2]
  resultado = []
  for cadena in a:
    cadena_nueva = procesar_rotacion(cadena)
    resultado.append(cadena_nueva)
  return tuple(resultado) 

def leer_rotaciones():
  with open ('piezas.txt') as rotaciones:
    rotacion = []
    for linea in rotaciones:
      a = procesar_linea(linea)
      rotacion.append(a)
  res = rotacion
  res = res[:-3]
  return tuple(res) 



def generar_pieza(pieza=None):
    """
    Genera una nueva pieza de entre PIEZAS al azar. Si se especifica el parámetro pieza
    se generará una pieza del tipo indicado. Los tipos de pieza posibles
    están dados por las constantes CUBO, Z, S, I, L, L_INV, T.

    El valor retornado es una tupla donde cada elemento es una posición
    ocupada por la pieza, ubicada en (0, 0). Por ejemplo, para la pieza
    I se devolverá: ( (0, 0), (0, 1), (0, 2), (0, 3) ), indicando que 
    ocupa las posiciones (x = 0, y = 0), (x = 0, y = 1), ..., etc.
    """
    piezas = leer_rotaciones()
    i = random.choice(range(0, len(piezas)))
    return piezas[i][0]


def trasladar_pieza(pieza, dx, dy):
    """
    Traslada la pieza de su posición actual a (posicion + (dx, dy)).

    La pieza está representada como una tupla de posiciones ocupadas,
    donde cada posición ocupada es una tupla (x, y). 
    Por ejemplo para la pieza ( (0, 0), (0, 1), (0, 2), (0, 3) ) y
    el desplazamiento dx=2, dy=3 se devolverá la pieza 
    ( (2, 3), (2, 4), (2, 5), (2, 6) ).
    """
   
    lista_final = [] 
    for x, y in pieza:           
        posicion_desplazada = (dx + x), (dy + y)       
        lista_final.append(posicion_desplazada)           
    return tuple(lista_final)   


       
def crear_juego(pieza_inicial):
    """
    Crea un nuevo juego de Tetris.

    El parámetro pieza_inicial es una pieza obtenida mediante 
    pieza.generar_pieza. Ver documentación de esa función para más información.

    El juego creado debe cumplir con lo siguiente:
    - La grilla está vacía: hay_superficie da False para todas las ubicaciones
    - La pieza actual está arriba de todo, en el centro de la pantalla.
    - El juego no está terminado: terminado(juego) da False

    Que la pieza actual esté arriba de todo significa que la coordenada Y de 
    sus posiciones superiores es 0 (cero).
    """
    grilla = []  
    for i in range((ALTO_JUEGO)):
        grilla.append([0]*(ANCHO_JUEGO))          
    pieza_actual = trasladar_pieza(pieza_inicial, (ANCHO_JUEGO//2), 0)       
    return pieza_actual, grilla

    
def dimensiones(juego):
    """
    Devuelve las dimensiones de la grilla del juego como una tupla (ancho, alto).
    """     
    return (ANCHO_JUEGO, ALTO_JUEGO) 
    
def pieza_actual(juego):
    """
    Devuelve una tupla de tuplas (x, y) con todas las posiciones de la
    grilla ocupadas por la pieza actual.

    Se entiende por pieza actual a la pieza que está cayendo y todavía no
    fue consolidada con la superficie.

    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """  
    pieza_actual, _ = juego   
    return pieza_actual


def hay_superficie(juego, x, y):
    """
    Devuelve True si la celda (x, y) está ocupada por la superficie consolidada.
    
    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """   
    pieza_actual, grilla = juego       
    return grilla[y][x] != 0    

def esta_en_posicion_valida(juego, pieza_a_colocar): 
    pieza_actual, grilla = juego
    for x, y in pieza_a_colocar:
        if x>=0 and y>=0:
            if x >= ANCHO_JUEGO or y >= ALTO_JUEGO:
                return False     
            elif hay_superficie(juego, x, y):
                return False
        else:
            return False
    return True 


    

def mover(juego, direccion):
    """
    Mueve la pieza actual hacia la derecha o izquierda, si es posible.
    Devuelve un nuevo estado de juego con la pieza movida o el mismo estado 
    recibido si el movimiento no se puede realizar.

    El parámetro direccion debe ser una de las constantes DERECHA o IZQUIERDA.
    """   
    pieza_actual, grilla = juego    
    trasladada_izq = trasladar_pieza(pieza_actual, IZQUIERDA, 0)
    trasladada_der = trasladar_pieza(pieza_actual, DERECHA, 0)
    trasladada_abajo = trasladar_pieza(pieza_actual, 0, 1)   
    if direccion == IZQUIERDA:   
        if esta_en_posicion_valida(juego, trasladada_izq):
            juego = trasladada_izq, grilla    
        return juego           
    elif direccion == DERECHA:
        if esta_en_posicion_valida(juego, trasladada_der):
            juego = trasladada_der, grilla
        return juego
    elif direccion == 2:
        if esta_en_posicion_valida(juego, trasladada_abajo):
            juego = trasladada_abajo, grilla
        return juego
        


                   
def eliminar_lineas_completas(juego):
    pieza_actual, grilla = juego    
    grilla_nueva = []
    for fila in grilla:    
        if 0 not in fila:            
            grilla_nueva.insert(0, [0, 0, 0, 0, 0, 0, 0, 0, 0])
        else:
            grilla_nueva.append(fila)
    return grilla_nueva
    
def terminado(juego):
    """
    Devuelve True si el juego terminó, es decir no se pueden agregar
    nuevas piezas, o False si se puede seguir jugando.
    """
    pieza_actual, _ = juego
    if esta_en_posicion_valida(juego, pieza_actual):
        return False
    return True



def avanzar(juego, siguiente_pieza):
    """
    Avanza al siguiente estado de juego a partir del estado actual.
    
    Devuelve una tupla (juego_nuevo, cambiar_pieza) donde el primer valor
    es el nuevo estado del juego y el segundo valor es un booleano que indica
    si se debe cambiar la siguiente_pieza (es decir, se consolidó la pieza
    actual con la superficie).
    
    Avanzar el estado del juego significa:
     - Descender una posición la pieza actual.
     - Si al descender la pieza no colisiona con la superficie, simplemente
       devolver el nuevo juego con la pieza en la nueva ubicación.
     - En caso contrario, se debe
       - Consolidar la pieza actual con la superficie.
       - Eliminar las líneas que se hayan completado.
       - Cambiar la pieza actual por siguiente_pieza.

    Si se debe agregar una nueva pieza, se utilizará la pieza indicada en
    el parámetro siguiente_pieza. El valor del parámetro es una pieza obtenida 
    llamando a generar_pieza().

    **NOTA:** Hay una simplificación respecto del Tetris real a tener en
    consideración en esta función: la próxima pieza a agregar debe entrar 
    completamente en la grilla para poder seguir jugando, si al intentar 
    incorporar la nueva pieza arriba de todo en el medio de la grilla se
    pisara la superficie, se considerará que el juego está terminado.

    Si el juego está terminado (no se pueden agregar más piezas), la funcion no hace nada, 
    se debe devolver el mismo juego que se recibió.
    """
    
    pieza_actual, grilla = juego
    pieza_transladada = trasladar_pieza(pieza_actual, 0, 1)
    if terminado(juego):
        return juego, False
    if esta_en_posicion_valida(juego, pieza_transladada):
        juego_nuevo = pieza_transladada, grilla
        return (juego_nuevo, False) 
    else:
        for x, y in pieza_transladada:
            grilla[y-1][x] = 1
        #pieza_transladada = siguiente
        siguiente_pieza_centrada = trasladar_pieza(siguiente_pieza, (ANCHO_JUEGO//2), 0)    
        juego_nuevo = siguiente_pieza_centrada, eliminar_lineas_completas(juego)
        return (juego_nuevo, True)


def buscar_rotacion(pieza):
    piezas = leer_rotaciones()
    for i in range(len(piezas)):
        for e in range(len(piezas[i])):
            if piezas[i][e] == pieza:
                if piezas[i][e] == piezas[i][-1]:
                    return piezas[i][0]
                return piezas[i][e+1]
            
           

def rotar(juego):
    pieza_actual, grilla = juego
    pieza_ordenada = sorted(pieza_actual)
    primer_posicion = pieza_ordenada[0]
    dx, dy = primer_posicion
    pieza_en_origen = trasladar_pieza(pieza_ordenada, -dx, -dy)
    siguiente_rotacion = buscar_rotacion(pieza_en_origen)
    siguiente_rotacion_transladada = trasladar_pieza(siguiente_rotacion, dx, dy)
    if esta_en_posicion_valida(juego, siguiente_rotacion_transladada):
        juego_nuevo = siguiente_rotacion_transladada, grilla
        return juego_nuevo
    return juego      


