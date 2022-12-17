'''    CreatedBy: Alejandro Granados Moncayo. 
Fecha de inicio del proyecto: 29 de noviembre del 2022.'''  
'''5 de diciembre del 2022: Agregue un incremento de los arrays iniciales y elimine un barco con valor 3, el primer barco con valor de 2 aparece en coordenadas random, arreglar eso.
6 de dicembre agregué contador de tiros para que el juego no sea infitinito, junto con esto agregre un if adicional para poder regresar al menú una vez terminado el juego. 
6 de diciembre del 2022 aún no funciona el los errores, los detecta pero no hace  el bloque de código de abajo, sigue sin hacer el bloque de código que se encuentra abajo de estas. 
6 de diciembre se agrego un menú para separar las reglas del modo de juego
7 de diciembre del 2022 se agregarón las instrucciones se modificó el contador y se agrego un end diferente al juego
7 de diciembre del 2022 modifique el vector y lo cambié por una tupla sigue sin reconocer el primer numero y se salta, agregue un cero pero tampoco lo reconoce
8 de diciembre se agregaro un nuevo menú para que el usuario decida si quier ejugar contra la IA o contra otra persona
9 de diciembre, se agregaron colores a los textos para darle un mejor diseño a la interfaz y se arreglo el bug de la detección de barcos'''
'''LIBRERIAS'''
import random
import msvcrt
'''VARIABLES CONSTANTES'''
TAMAÑO_DE_LOS_BARCOS = [2,3,3,4,5]
TABLERO_SIN_BARCOS = [[" "] * 10 for i in range(10)]
TABLERO_DEL_JUGADOR = [[" "] * 10 for i in range(10)]
TABLERO_DE_LA_IA = [[" "] * 10 for i in range(10)]
TABLERO_DE_HITS_JUGADOR = [[" "] * 10 for i in range(10)]
TABLERO_DE_HITS_IA = [[" "] * 10 for i in range(10)]
TABLERO_DEL_JUGADOR_UNO = [[" "] * 10 for i in range(10)]
TABLERO_DEL_JUGADOR_DOS = [[" "] * 10 for i in range(10)]  
TABLERO_DE_HITS_JUGADOR_UNO = [[" "] * 10 for i in range(10)]
TABLERO_DE_HITS_JUGADOR_DOS = [[" "] * 10 for i in range(10)] 
BOTON_DE_REGRESO = 1
LETRAS_A_NUMEROS = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7,'J':8,'K':9}
SEPARADOR = str('*-----------**-------------**-----------**-----------**-----------**-----------**-----------**-----------*')
'''FUNCIONES'''
def limpiar_matriz(tablero):
    """
    Esta función limpia la matriz y la restablece a espacios vacios.
    Parámetro: tablero
    """
    for i, e in enumerate(tablero):
        if isinstance(e, list):
            limpiar_matriz(e)
        else:
            tablero[i] = " " 
 

def impresion_del_tablero(tablero): 
    '''Imprime el tablero con las letras de la A hasta la K en la parte superior del tablero. 
    Imprime los números del 1 al 10 a la izquierda del tablero
    Parámetros: El tablero'''
    print("  A B C D E F G H J K".center(175))
    print("+-+-+-+-+-+-+-+-+-+-+".center(175))
    numero_de_fila = 1
    for fila in tablero:
        print("%d|%s|".center(160) %  (numero_de_fila,"|".join(fila)))
        numero_de_fila += 1


def posicion_de_los_barcos(tablero):
    '''
    Esta función toma como argumento el un tablero y coloca los barcos en él. 
    Parámetro: El tablero en el que se colocaran los barcos. '''
    for tamaño_de_los_barcos in (TAMAÑO_DE_LOS_BARCOS):
        while True:
            if tablero == TABLERO_DE_LA_IA:
                orientacion, fila, columna = random.choice(["H", "V"]), random.randint(0,10), random.randint(0,10)
                if comprobación_de_ajustes_del_barco(tamaño_de_los_barcos, fila, columna, orientacion): 
                    if superposiciones_del_barco(tablero, fila, columna, orientacion, tamaño_de_los_barcos) == False:
                        if orientacion == "H":
                            for i in range(columna, columna + tamaño_de_los_barcos):
                                tablero[fila][i] = "x"
                        else:
                            for i in range(fila, fila + tamaño_de_los_barcos):
                                tablero[i][columna] = "x"
                        break
            else:
                lugar_del_barco = True
                print('Coloca el barco de tamaño: ' + str(tamaño_de_los_barcos))
                fila, columna, orientacion = entrada_de_usuario(lugar_del_barco)
                if comprobación_de_ajustes_del_barco(tamaño_de_los_barcos, fila, columna, orientacion):
                    if superposiciones_del_barco(tablero, fila, columna, orientacion, tamaño_de_los_barcos) == False:
                        if orientacion == "H":
                            for i in range(columna, columna + tamaño_de_los_barcos):
                                tablero[fila][i] ="x"
                        else:
                            for i in range(fila, fila + tamaño_de_los_barcos):
                                tablero[i][columna] ="x"
                        impresion_del_tablero(TABLERO_DEL_JUGADOR)
                        break 


def comprobación_de_ajustes_del_barco(TAMAÑO_DEL_BARCO, fila, columna, orientacion):
    '''Esta función revisa si el barco se encuentra dentro de las dimensiones permitidas en el tablero (10*10).
    Parámetro: TAMAÑO_DEL_BARCO: El tamaño del barco. 
    Parámetro: fila: El número de la fila de la "Proa" del barco (Esto para saber si no se sale de las dimensiones.)
    Parámetro: columna: El número de la columna del barco. 
    Parámetro:  orientacion: "H" o "V"
    Retorna: True o False'''
    if orientacion == "H":
        if columna + TAMAÑO_DEL_BARCO > 10:
            return False
        else:
            return True
    else:
        if fila + TAMAÑO_DEL_BARCO > 10:
            return False
        else:
            return True


def superposiciones_del_barco(tablero, fila, columna, orientacion, tamaño_de_los_barcos):
    """
    Esta función devuelve un valor booleano True si el barco esta superposicionado con otro, en caso de que no devuelve un valor Booleano Falso.
    Parámetro: tablero: El tablero de la IA o del Usuario. 
    Parámetro: fila: La fila del barco. 
    Parámetro: columna:La columna donde se encuentra el barco. 
    Parámetro: orientacion: "H" or "V"
    Parámetro: tamaño_de_los_barcos: una lista del tamaño de los barcos. 
    Retorna: Cierto o Falso. 
    """
    if orientacion == "H":
        for i in range(columna, columna + tamaño_de_los_barcos):
            if tablero[fila][i] ==  "x":
                return True
    else:
        for i in range(fila, fila + tamaño_de_los_barcos):
            if tablero[i][columna] == "x":
                return True
    return False

def entrada_de_usuario(lugar_del_barco):
    '''Esta función toma un valor Booleano y regresa una tupla de tres valores si el Booleano es verdadero (Fila, columna, orientación). 
    Si el Booleano es falso regresa una tupla de dos valores (Fila, columna).
    Parámetros: lugar_del_barco: Este tiene un valor Booleano que determina si el usuario esta colocando un barco.
    Parámetro: lugar_del_barco 
    :retorna: La fila, la columna y la orientación.'''
    if lugar_del_barco == True:
        while True:
            try: 
                orientacion = input("introduce la orientacion (H o V): ").upper()
                if orientacion ==  "H" or orientacion ==  "V":
                    break
            except TypeError: 
                print('Introducce la horientación correcta ')   
        while True:
            try:  
                fila = input("introduce un número de fila entre 1 al 10 para el barco: ")
                if fila in  '12345678910':
                    fila = int(fila) -1
                    break
            except ValueError:
                 print('Fila fuera del rango :(')
                 print('introduce un número valido entre 1-10')
        while True:
            try: 
                columna = input("introduce la columna para el barco: ").upper()
                if columna in 'ABCDEFGHJK':
                    columna = LETRAS_A_NUMEROS[columna]
                    break
            except KeyError:
                 print('La columna que introdujiste es invalida :(')
                 print('introduce una letra valida entre A-K')
        return fila, columna, orientacion 
    else:
            while True:
                try: 
                    fila = input("introduce una fila del 1 al 10 para el barco: ")
                    if fila in  '12345678910':
                        fila = int(fila) - 1 
                        break
                except ValueError: 
                    print('La fila que introdujiste es invalida:(')
                    print('introduce una fila valida entre 1-10')
            while True:
                try: 
                    columna = input("introduce una columna de la A a la K para posicionar el barco el barco: ").upper()
                    if columna in   'ABCDEFGHJK':
                        columna = LETRAS_A_NUMEROS[columna]
                        break
                except KeyError:
                    print('La columna que introdujiste es invalida :(')
                    print('introduce una letra valida entre A-K')
            return fila, columna 

 
def turnos(tablero):
    """
    Esta función sirve para los turnos de la IA y el jugador, si el tablero es el del jugador, entonces este tendrá la oportunidad de ingresar las coordenadas deseadas para disparar y si el tablero es el de la I.A entonces la I.A de manera random ingresara coordanas para intentar acertar en el tablero del usuario. Si cualquiera de los dos jugadores acierta en la coordenada donde se encuente un barco (x), entonces automaticamente se cambiará por un "@", si el disparo falla entonces se imprentara un "-".
    
    Parámetro: tablero: El tablero donde esta jugando el juador o la IA. 
    """
    if tablero == TABLERO_DE_HITS_JUGADOR:
        fila, columna = entrada_de_usuario(TABLERO_DE_HITS_JUGADOR)  
        if tablero[fila][columna] == "-":
            turnos(tablero)
        elif tablero[fila][columna] == "@":
            turnos(tablero)
        elif TABLERO_DE_LA_IA[fila][columna] == "x":
            tablero[fila][columna] = "@"
            print('\n')
            mensaje_hit = nombre +' ' + 'ACERTASTE :)'
            print(mensaje_hit.center(865)) 
        else:
            tablero[fila][columna] = "-"
            print('\n')
            mensaje_miss = nombre + ' ' + 'FALLASTE :('
            print(mensaje_miss.center(865)) 
                   
    else:
        fila, columna = random.randint(0,9), random.randint(0,9)
        if tablero[fila][columna] ==  "-":
            turnos(tablero)
        elif tablero[fila][columna] == "@":
            turnos(tablero)
        elif TABLERO_DEL_JUGADOR[fila][columna] == "x":
            tablero[fila][columna] = "@"
            print('\n')
            print ('LA IA ACERTO'.center(865))
        else:
            tablero[fila][columna] = "-"
            print('\n')
            print ('LA IA FALLO'.center(865))


def contador_de_hits(tablero):
    """
    Esta función cuenta los hits que hay en el tablero
    Parámetro: Tablero.
    Retorna: Los números de hits.
    """
    count = 0 
    for fila in tablero:
        for columna in fila:
            if columna == "@":
                count += 1   
    return count
#------------------*----------------------*-----------------------------*--------------------------------*-------------------------
'''Funciones para modo Jugador vs Jugador'''

def posicion_de_los_barcos_dos_jugadores(tablero): 
    """
    Esta función toma como argumento un tablero y luego le pide al usuario que coloque un barco de cierto tamañaño en el. 
    Después le pide al usuario que ingrese, la fila, la columna y la horientación de su barco. 
    Luego la función comprobación_de_ajustes_del_barco() comprueba si el barco se puede colocar en la posición que el usuario eligió.
    Si la posición es correcta entonces se imprentará en el barco el simbolo "X". 
    En caso de lo contrario (Si no es correcto el posicionamiento), se le pide al usuario que ingrese la posición nuevamente.
    Esta función repite el mismo proceso para cada barco que se encuentre dentro de nuestra lista. 
    Parámetro: Tablero: El tablero del jugador uno o en su defecto el del jugador dos. 
    """
    for tamaño_de_los_barcos in (TAMAÑO_DE_LOS_BARCOS):      
        while True:
            if tablero == tablero:
                lugar_del_barco = True
                # *|MARCADOR_CURSOR|*
                print('Coloca el barco de tamaño: ' + str(tamaño_de_los_barcos))
                fila, columna, orientacion = entrada_de_usuario(lugar_del_barco)
                if comprobación_de_ajustes_del_barco(tamaño_de_los_barcos, fila, columna, orientacion):
                    if superposiciones_del_barco(tablero, fila, columna, orientacion, tamaño_de_los_barcos) == False:
                        if orientacion == "H":
                            for i in range(columna, columna + tamaño_de_los_barcos):
                                tablero[fila][i] =  "x"
                        else:
                            for i in range(fila, fila + tamaño_de_los_barcos):
                                tablero[i][columna] = "x"
                        break 


def turnos_dos_jugadores(tablero_hits,tablero_usuario,nombre):
    """
    Esta función toma un tablero como argumento y luego le pida al usuario que inserte una fila y una columna.
    Si la función de entrada_de_usuario() no es válida esta función se volverá a llamar a sí misma para que se inserten los datos correctos.
    Si la entrada del usuario es válida comprueba si el usuario acertó a un barco, si es así esta función imprimira un mensaje diciendo que el usario acertó e imprime un '@' en la posición indicada, sinoves así entonces imprime que el usario falló y un símbolo '-' en la posición indicada. 
    Este proceso también es repetido para la entrada del segundo usuario. 
    Parámetros: El tablero en el que esta jugando el jugador (Tablero de hits). 
    Parámetros: Tablero del jugador contrario. (posiciones de barcos)
    Parámetros: Nombre. 
    """
    if tablero_hits == tablero_hits:
        fila, columna = entrada_de_usuario_ramdon(tablero_hits)
        if tablero_hits[fila][columna] == "-":
            print('Coordenada repetida')
            turnos(tablero_hits)
        elif tablero_hits[fila][columna] == "@":
            print('Coordenada repetida')
            turnos(tablero_hits)
        elif tablero_usuario[fila][columna] == "x":
            tablero_hits[fila][columna] = "@"
            print(nombre.center(865))
            print('ACERTASTE'.center(865)) 
        else:
            tablero_hits[fila][columna] = "-"
            print(nombre.center(865))
            print ('FALLASTE'.center(865))     


''' Funciones Modo de juego Jugador vs Jugador Random'''
def posicion_de_los_barcos_random(tablero): 
    """
    Esta función toma como argumento un tablero y luego le pide al usuario que coloque un barco de cierto tamañaño en el. 
    Después le pide al usuario que ingrese, la fila, la columna y la horientación de su barco. 
    Luego la función comprobación_de_ajustes_del_barco() comprueba si el barco se puede colocar en la posición que el usuario eligió.
    Si la posición es correcta entonces se imprentará en el barco el simbolo "X". 
    En caso de lo contrario (Si no es correcto el posicionamiento), se le pide al usuario que ingrese la posición nuevamente.
    Esta función repite el mismo proceso para cada barco que se encuentre dentro de nuestra lista. 
    Parámetro: Tablero: El tablero del jugador uno o en su defecto el del jugador dos. 
    """
    for tamaño_de_los_barcos in (TAMAÑO_DE_LOS_BARCOS):      
        while True:
            if tablero == tablero:
                orientacion,fila,columna = random.choice(["H","V"]), random.randint(0,10), random.randint(0,10)
                if comprobación_de_ajustes_del_barco(tamaño_de_los_barcos, fila, columna, orientacion):
                    if superposiciones_del_barco(tablero, fila, columna, orientacion, tamaño_de_los_barcos) == False:
                        if orientacion == "H":
                            for i in range(columna, columna + tamaño_de_los_barcos):
                                tablero[fila][i] = "x"
                        else:
                            for i in range(fila, fila + tamaño_de_los_barcos):
                                tablero[i][columna] = "x"
                        break     

 
def entrada_de_usuario_ramdon(lugar_del_barco):
    ''' Toma una lista de tuplas como argumento y devuelve una tupla de dos enteros
    
    parámetro lugar_del_barco: Esta es una lista de tuplas que contienen las coordenadas del barco
    :return: la fila y la columna de la entrada del usuario.
    '''
    while True:
        try: 
            fila = input("introduce una fila para disparar: ")
            if fila in  '12345678910':
                fila = int(fila) - 1 
                break
        except ValueError: 
            print('La fila que introdujiste es invalida:(')
            print('introduce una fila valida entre 1-10')
    while True:
        try: 
            columna = input("introduce una columna de la A a la K para disparar: ").upper()
            if columna in   'ABCDEFGHJK':
                columna = LETRAS_A_NUMEROS[columna]
                break
        except KeyError:
            print('La columna que introdujiste es invalida :(')
            print('introduce una letra valida entre A-K')
    return fila, columna 
#--------*----------------*------------------*---------------------*---------------------------*--------------*------------*-------
'''MAIN CODE'''
print ('*--- BATTLESHIP ---*'.center(865)) 
print ('By: Alejandro Granados Moncayo'.center(865))
#Loop de para ciclar el menú de elecciones (Instrucciones, modos de juego, reglas, y creditos)
while BOTON_DE_REGRESO == 1:
    #Impresión de el menú al jugador. 
    print('INSERTA 1 PARA JUGAR BATTLESHIP'.center(865))
    print('INSERTA 2 PARA VER LAS REGLAS E INSTRUCCIONES PARA JUGAR BATTLESHIP'.center(865))
    print('INSERTA 3 PARA VER LOS CREDITOS'.center(865)) 
    #Lectura de teclado de la elección del usuario. 
    eleccion = int(input('Elige: '.center(865)))
    #Se limpian las matrices en dado caso de que se haya jugado previamente. 
    limpiar_matriz(TABLERO_DEL_JUGADOR)
    limpiar_matriz(TABLERO_DE_LA_IA)
    limpiar_matriz(TABLERO_DE_HITS_IA)
    limpiar_matriz(TABLERO_DE_HITS_JUGADOR)
    limpiar_matriz(TABLERO_DEL_JUGADOR_DOS)
    limpiar_matriz(TABLERO_DEL_JUGADOR_UNO)
    limpiar_matriz(TABLERO_DE_HITS_JUGADOR_UNO)
    limpiar_matriz(TABLERO_DE_HITS_JUGADOR_DOS)
    #Le preguntamos el usuario cuál será el modo en el que jugará, en base a esto se decidirá el flujo dle programa.
    if eleccion == 1:
        print('Inserta 1 si quieres jugar contra la IA')
        print('Inserta 2 si quieres jugar Jugador vs Jugador')
        modo_de_juego = int(input(' ')) 
        #Si el modo de juego que elige es uno entonces el programa ejecutara este bloque de código.      
        if modo_de_juego == 1:
            print('\n')
            print ('*--- BIENVENIDO AL MODO DE JUEGO JUGADOR VS I.A. ---*'.center(865))
            print('\n')
            #Se camputa el username del usuario. 
            nombre = input('Inserta tu nombre de usuario: ')
            print('\n')
            #Se le pide al jugador que inserte el número de oportunidades que tendra para disparar el y la I.A.
            turnos_jugador = int(input(f'Hola' + ' '+ nombre + ' '+ 'inserta el número de balas que la IA y tu tendrán para disparar: '))
            turnos_IA = turnos_jugador
            #Se abre este loop para que el jugador inserte un número mayor a 17, mientras esta codición no se cumpla entonces se quedará dentro de este loop. 
            while turnos_jugador <17:
                    print('\n')
                    print('Has ingresado muy poca munición, no seas tacaño :(')
                    turnos_jugador = int(input(nombre + ''+'inserta el número de balas que la IA y tu tendrán para disparar: ' ))
            #Si el usuario inserta el número que cumpla con la condición entonces se ejecutara el siguiente bloque de código. 
            if turnos_jugador >=17:
                print('\n')
                #Se le da una breve bienvenida al usuario se le muestran cuantos turnos tendrán y se mandan a llamar las funciones para posicionar los barcos, tanto de la I.A como del usuario y después se imprime el tablero del usuario cpon la posición de los barcos. 
                bienvenida = 'Hola' + ' ' + nombre + ' ' + 'este es tu tablero, introduce tus barcos por medio de coordenadas'
                print(bienvenida.center(878))
                print('Recuerda insertar tus barcos dispersados para que la I.A no tenga posibilidad de ganarte.'.center(865))
                print('\n')
                posicion_de_los_barcos(TABLERO_DE_LA_IA)
                impresion_del_tablero(TABLERO_DEL_JUGADOR)
                posicion_de_los_barcos(TABLERO_DEL_JUGADOR)
                print(SEPARADOR.center(865))
                #La variable de turnos de la I.A será igual a la de turnos del jugador. 
                turnos_IA = turnos_jugador
                #Abrimos un loop para que se repita el siguiente bloque de código donde se insertaran los turnos de la I.A y del usuario. 
                while (contador_de_hits(TABLERO_DE_HITS_JUGADOR) < 99 and contador_de_hits(TABLERO_DE_HITS_IA) < 99): 
                    #Turno del jugador.
                    print('--- ESCOGE LAS COORDENADAS PARA DISPARAR ---'.center(865))
                    impresion_del_tablero(TABLERO_DE_HITS_JUGADOR)
                    turnos(TABLERO_DE_HITS_JUGADOR)
                    contador_de_hits(TABLERO_DE_HITS_JUGADOR)
                    print('\n')
                    print((nombre + ' ' + 'lleva' + ' ' + str(contador_de_hits(TABLERO_DE_HITS_JUGADOR)) + ' ' + 'HITS').center(865))
                    turnos_jugador -= 1
                    balas_jugador = 'TE QUEDAN' + ' ' + str (turnos_jugador) + ' ' + 'BALAS PARA SEGUIR DISPARANDO'
                    print(balas_jugador.center(880))
                    print('\n')
                    print(('Tablero hits' + ' ' + nombre).center(865))
                    impresion_del_tablero(TABLERO_DE_HITS_JUGADOR)
                    print(SEPARADOR.center(865))
                    #Turno de la IA.
                    turnos(TABLERO_DE_HITS_IA)   
                    contador_de_hits(TABLERO_DE_HITS_IA)
                    print('Tablero de HITS de la IA'.center(865))
                    hits_IA = 'LLEVA' + ' ' + str (contador_de_hits(TABLERO_DE_HITS_IA)) +  ' ' + 'HITS'
                    print(f'La I.A {hits_IA}'.center(875))
                    turnos_IA -= 1 
                    balas_IA = 'LE QUEDAN' + ' ' + str(turnos_IA) + ' ' + 'BALAS A LA I.A PARA SEGUIR DISPARANDO'
                    print(balas_IA.center(875))
                    print('\n')     
                    impresion_del_tablero(TABLERO_DE_HITS_IA) 
                    print(SEPARADOR.center(865)) 
                    final_hits_jugador =nombre +  ' '  + 'acertaste' + ' '  + str (contador_de_hits(TABLERO_DE_HITS_JUGADOR)) + ' '  + 'disparos'  
                    final_hits_ia = 'La I.A acertó' + ' '  + str (contador_de_hits(TABLERO_DE_HITS_JUGADOR)) + ' '  + 'disparos' 
                    #El loop se rompera cuando el usuario o la I.A cumplan algunas de las siguientes condiciones. 
                    if contador_de_hits(TABLERO_DE_HITS_JUGADOR) == 17:
                        print(('¡¡FELICIDADES' + ' ' + nombre + ' ' + 'DERROTASTE A LA IA!!').center(865))
                        print((final_hits_jugador).center(865)) 
                        break 
                    elif contador_de_hits(TABLERO_DE_HITS_IA) == 17:
                        print(('LO SENTIMOS' + ' ' + nombre).center(865))
                        print('LA I.A TE DERROTO :('.center(865))
                        print(final_hits_ia.center(865))
                        break
                    elif (turnos_jugador == 0 and turnos_IA== 0) and (contador_de_hits(TABLERO_DE_HITS_JUGADOR) > contador_de_hits(TABLERO_DE_HITS_IA)): 
                        print('SE ACABARÓN TUS BALAS PERO...'.center(865))
                        print((nombre + ' ' + 'la victoria es tuya por mayoría de hits').center(865))
                        print(final_hits_jugador.center(865))
                        break
                    elif (turnos_jugador == 0 and turnos_IA== 0) and (contador_de_hits(TABLERO_DE_HITS_JUGADOR) < contador_de_hits(TABLERO_DE_HITS_IA)): 
                        print('la victoria es de la IA por mayoría de hits'.center(865))
                        print(final_hits_ia.center(865))
                        break
                    elif (turnos_jugador == 0 and turnos_IA== 0) and  (contador_de_hits(TABLERO_DE_HITS_JUGADOR) == contador_de_hits(TABLERO_DE_HITS_IA)):
                        print('¡¡¡ESTO ES ASOMBRO!!!')
                        print('¡¡¡EMPATE!!!') 
                        print(final_hits_jugador.center(865))
                        print(final_hits_ia.center(865))  
                        break
            #Cuando se agoten las opciones o se termine el juego el usuario podrá elegir si quiere regresar al menú de nuevo. 
            BOTON_DE_REGRESO = int(input('Si desear regresar al menu inserta un 1: ').center(865))
        #Si el usuario elige el modo de juego jugador vs jugador se desplegará este sub menú. 
        elif modo_de_juego == 2:
            print('*--- BIENVENIDO AL MODO DE JUEGO PLAYER VS PLAYER. ---*'.center(865))
            print('Escoge el modo de juego que desees')
            print('1.- Juego clasico (Los usuarios tendrán que elegir donde colocar sus barcos y cuánta munición tendrán.)')
            print('2.- Modo Random (El juego colocará de manera random los barcos y les asignará munición aleatoria.)')
            #Se captura la opción que el usuario elija. 
            modos_de_juego_player_vs_player = int(input(': '))
            #Si el usuario elige el modo clasico entonces capturaremos dos usernames. 
            if modos_de_juego_player_vs_player == 1:
                nombre_j1 = input('Jugador 1 inserta tu Username: ')
                nombre_j2 = input('Jugador 2 inserta tu Username: ')
                #Le pediremos al usuario 1 que introduzca que cantidad de disparos (turnos) habrá en la partida. 
                turnos_jugador_uno = int(input('Inserta el número de munición que tendrán para la batalla: '))
                turnos_jugador_dos = turnos_jugador_uno
                #Abrimos un pequeño loop que tiene como condicion insertar un numero mayor o igual a 17: 
                while turnos_jugador_uno < 17:
                    print('No sean tacaños, inserten más munición :(')
                    print('\n')
                    turnos_jugador_uno = int(input('Inserta el número de munición que tendrán para la batalla: ')) 
                    turnos_jugador_uno = turnos_jugador_uno
                    #Si la condicioón establecida anteriormente en el loop se cumple entonces el programa seguira el bloque de código que esta después de este if. 
                if turnos_jugador_uno >= 17 :
                    #Aqui se le indica a los jugadores d ecuantas balas disponen: 
                    print ('Ambos jugadores tienen' + ' ' + str(turnos_jugador_uno) + ' ' +  'balas para intentar acertar' )
                    #Turno de posicionamiento de barcos del jugador uno.
                    print((nombre_j1 + ' ' + 'escoge las coordenadas donde se ubicarán tus barcos: ').center(865))
                    impresion_del_tablero(TABLERO_SIN_BARCOS)
                    posicion_de_los_barcos_dos_jugadores(TABLERO_DEL_JUGADOR_UNO)
                    print(SEPARADOR)
                    #Turno de posicionamiento de barcos del jugador dos.
                    print((nombre_j2 + ' ' + 'escoge las coordenadas donde se ubicarán tus barcos: ').center(865))
                    impresion_del_tablero(TABLERO_SIN_BARCOS)
                    posicion_de_los_barcos_dos_jugadores(TABLERO_DEL_JUGADOR_DOS)
                    turnos_jugador_dos = turnos_jugador_uno
                    #Se abre un loop para que ambos jugadores puedan seguir tirando hasta cumplir cualquiera de las condiciones para la victoria, empate, etc. 
                    while (contador_de_hits(TABLERO_DE_HITS_JUGADOR_UNO) < 99 and contador_de_hits(TABLERO_DE_HITS_JUGADOR_DOS) < 99):
                        #Turno del jugador uno
                        print( nombre_j1.center(865))
                        print('Escoge las cordenadas para disparar'.center(865))
                        impresion_del_tablero(TABLERO_SIN_BARCOS)
                        turnos_dos_jugadores(TABLERO_DE_HITS_JUGADOR_UNO,TABLERO_DEL_JUGADOR_DOS,nombre_j1)
                        turnos_jugador_uno -= 1 
                        print((nombre_j1 + ' ' + 'te quedan' + ' ' + str(turnos_jugador_uno) + ' ' + 'disparos').center(865))
                        contador_j1 = nombre_j1 + ' ' + 'llevas' + ' ' + str(contador_de_hits(TABLERO_DE_HITS_JUGADOR_UNO)) + ' ' + 'HITS'
                        print(contador_j1.center(865))
                        print(('Tablero de HITS del jugador' + ' ' + nombre_j1).center(865))
                        impresion_del_tablero(TABLERO_DE_HITS_JUGADOR_UNO)
                        print(SEPARADOR)
                        #Turno del jugador dos.  
                        print(nombre_j2.center(865))
                        print('Escoge las cordenadas para disparar'.center(865))
                        impresion_del_tablero(TABLERO_SIN_BARCOS)
                        turnos_dos_jugadores(TABLERO_DE_HITS_JUGADOR_DOS,TABLERO_DEL_JUGADOR_UNO,nombre_j2)  
                        turnos_jugador_dos -= 1 
                        print((nombre_j2 + ' ' + 'te quedan' + ' ' + str(turnos_jugador_dos) + ' ' + 'disparos').center(865))
                        contador_j2 = nombre_j2 + ' ' + 'llevas' + ' ' + str(contador_de_hits(TABLERO_DE_HITS_JUGADOR_DOS)) + ' ' + 'HITS'
                        print(contador_j2.center(865))
                        print(('Tablero de HITS del jugador' + ' ' + nombre_j2).center(865))
                        impresion_del_tablero(TABLERO_DE_HITS_JUGADOR_DOS)  
                        print(SEPARADOR)   
                        final_hits_jugador1 = nombre_j1 + ' ' + 'acertaste ' + ' ' + str (contador_de_hits(TABLERO_DE_HITS_JUGADOR_UNO)) + ' ' +  'disparos'  
                        final_hits_jugador2 = nombre_j2 + ' ' + 'acertaste' + ' ' + str (contador_de_hits(TABLERO_DE_HITS_JUGADOR_DOS)) + ' ' +  'disparos'
                        #Cuando el jugador uno o el jugador dos llegue a cualquiera de las siguientes condiciones entonces el programa ejecutara el bloque que este debajo del if/elif del cuál se cumpla la condición. 
                        if contador_de_hits(TABLERO_DE_HITS_JUGADOR_UNO) == 17:
                            print(nombre_j1.center(865))
                            print("¡¡LA VICTORIA ES TUYA!!".center(865))
                            print(final_hits_jugador1.center(865))
                            break   
                        elif contador_de_hits(TABLERO_DE_HITS_JUGADOR_DOS) == 17:
                            print(nombre_j2.center(865))
                            print("¡¡LA VICTORIA ES TUYA!!".center(865))
                            print(final_hits_jugador2.center(865))
                            break 
                        elif (turnos_jugador_uno == 0 and turnos_jugador_dos== 0) and (contador_de_hits(TABLERO_DE_HITS_JUGADOR_UNO) > contador_de_hits(TABLERO_DE_HITS_JUGADOR_DOS)): 
                            print('SE ACABARÓN TUS BALAS PERO...'.center(865))
                            print ((nombre_j1 +   ' ' + 'la victoria es tuya por mayoría de hits').center(865))
                            print(final_hits_jugador1.center(865))
                            break
                        elif (turnos_jugador_uno == 0 and turnos_jugador_dos== 0) and (contador_de_hits(TABLERO_DE_HITS_JUGADOR_UNO) < contador_de_hits(TABLERO_DE_HITS_JUGADOR_DOS)): 
                            print('SE ACABARÓN TUS BALAS PERO...'.center(865))
                            print ((nombre_j2 +   ' ' + 'la victoria es tuya por mayoría de hits').center(865))
                            print(final_hits_jugador2.center(865))
                            break
                #Cuando se agoten las opciones o se termine el juego el usuario podrá elegir si quiere regresar al menú de nuevo. 
                BOTON_DE_REGRESO = int(input('Si desear regresar al menu inserta un 1: ').center(865))
            elif modos_de_juego_player_vs_player ==2: 
                #Si el usuario elige el modo random se desplegrá esta pequeña interfaz en la cual insertaran sus usernames.
                print('*-- BIENVENIDO AL MODO DE JUEGO RANDOM ---*'.center(865))
                nombre_1 = input('Jugador 1 inserta tu Username: ')
                nombre_2 = input('Jugador 2 inserta tu Username: ')
                #Por medio del modulo random almacenamos en los turnos de cada jugador una cantidad de disparos al azar (serán diferentes para ambos).
                turnos_jugador_uno = random.randint(17,99)
                turnos_jugador_dos = random.randint(17,99)
                #Se le dice a los usuarios cuantos tiros disponen para jugar. 
                print(nombre_1 +  ' ' + 'tienes' + ' ' + str(turnos_jugador_uno) + ' ' +  'disparos')
                print(nombre_2 +  ' ' + 'tienes' + ' ' + str(turnos_jugador_dos) + ' ' +  'disparos')
                #Se llama a ña función para posicionar los barcos de manera aleatoria, por ende, no se imprentaran los tableros. 
                posicion_de_los_barcos_random(TABLERO_DEL_JUGADOR_UNO)
                posicion_de_los_barcos_random(TABLERO_DEL_JUGADOR_DOS)
                #Abrimos un loop para que los usuarios puedan seguir jugando hasta agotar sus turnos o cumplir alguna condicion para ganar, empatar, etc. 
                while (contador_de_hits(TABLERO_DE_HITS_JUGADOR_UNO) < 100 and contador_de_hits(TABLERO_DE_HITS_JUGADOR_DOS) < 100):
                    #Turno del jugador uno. 
                    print((nombre_1 +  ' ' + 'Inserta las coordenadas para disparar').center(865))
                    impresion_del_tablero(TABLERO_SIN_BARCOS)
                    turnos_dos_jugadores(TABLERO_DE_HITS_JUGADOR_UNO,TABLERO_DEL_JUGADOR_DOS,nombre_1)
                    turnos_jugador_uno -= 1
                    contador_de_hits(TABLERO_DE_HITS_JUGADOR_UNO)
                    print((nombre_1 + ' ' + 'llevas' + ' ' + str(contador_de_hits(TABLERO_DE_HITS_JUGADOR_UNO)) + ' ' + 'HITS').center(865))
                    contador1 = nombre_1 + ' ' + 'te quedan' + ' ' + str(turnos_jugador_uno) +  ' ' + 'balas'
                    print(contador1.center(865))
                    impresion_del_tablero(TABLERO_DE_HITS_JUGADOR_UNO)
                    print(SEPARADOR.center(865))  
                    #Turno del jugador dos. 
                    print((nombre_2 +  ' ' + 'Inserta las coordenadas para disparar').center(865))
                    impresion_del_tablero(TABLERO_SIN_BARCOS)
                    turnos_dos_jugadores(TABLERO_DE_HITS_JUGADOR_DOS,TABLERO_DEL_JUGADOR_UNO,nombre_2)
                    turnos_jugador_dos -= 1
                    contador_de_hits(TABLERO_DEL_JUGADOR_UNO)
                    print((nombre_2 + ' ' + 'llevas' + ' ' + str(contador_de_hits(TABLERO_DE_HITS_JUGADOR_DOS)) + ' ' + 'HITS').center(865))
                    contador2 = nombre_2 + ' ' + 'te quedan' + ' ' + str(turnos_jugador_dos) +  ' ' + 'balas'
                    print(contador2.center(865))
                    impresion_del_tablero(TABLERO_DE_HITS_JUGADOR_DOS)
                    print(SEPARADOR)
                    #Alamcenamos en dos variables los aciertos de los jugadores. 
                    final_hits_jugador1 = nombre_1 + ' ' + 'acertaste' + ' ' + str (contador_de_hits(TABLERO_DE_HITS_JUGADOR_UNO)) + ' ' +  'disparos'  
                    final_hits_jugador2 = nombre_2 + ' ' + 'acertaste' + ' ' + str (contador_de_hits(TABLERO_DE_HITS_JUGADOR_DOS)) + ' ' +  'disparos' 
                    #Se agregan condiciones para elegir al ganador, depende a que se cumpla se ejecutara el bloque de código que se encuentra abajo de cada una. 
                    if contador_de_hits(TABLERO_DE_HITS_JUGADOR_UNO) == 17:
                        print(nombre_1.center(865))
                        print("¡¡VICTORIA!!".center(865))
                        print(final_hits_jugador1.center(865))
                        break   
                    elif contador_de_hits(TABLERO_DE_HITS_JUGADOR_DOS) == 17:
                        print(nombre_2.center(865))
                        print("¡¡VICTORIA!!".center(865))
                        print(final_hits_jugador2.center(865))
                        break 
                    elif (turnos_jugador_uno == 0 and turnos_jugador_dos== 0) and (contador_de_hits(TABLERO_DE_HITS_JUGADOR_UNO) > contador_de_hits(TABLERO_DE_HITS_JUGADOR_DOS)): 
                        print('SE ACABARÓN TUS BALAS PERO...'.center(865))
                        print ((nombre_1 + ' ' + 'la victoria es tuya por mayoría de hits').center(865))
                        print(final_hits_jugador1.center(865))
                        break
                    elif (turnos_jugador_uno == 0 and turnos_jugador_dos== 0) and (contador_de_hits(TABLERO_DE_HITS_JUGADOR_UNO) < contador_de_hits(TABLERO_DE_HITS_JUGADOR_DOS)): 
                        print('SE ACABARÓN TUS BALAS PERO...'.center(865))
                        print ((nombre_2 + ' ' + 'la victoria es tuya por mayoría de hits').center(865))
                        print(final_hits_jugador2.center(865))
                        break
                    elif (turnos_jugador_uno == 0 and turnos_jugador_dos== 0) and  (contador_de_hits(TABLERO_DE_HITS_JUGADOR_UNO) == contador_de_hits(TABLERO_DE_HITS_JUGADOR_DOS)):
                        print('¡¡¡ESTO ES ASOMBROSO!!!'.center(865))
                        print('¡¡¡EMPATE!!!'.center(865))
                        print(final_hits_jugador1.center(865))
                        print(final_hits_jugador2.center(865)) 
                        break
        #Cuando se agoten las opciones o se termine el juego el usuario podrá elegir si quiere regresar al menú de nuevo. 
        BOTON_DE_REGRESO = int(input('Si desear regresar al menu inserta un 1: ').center(865))
    elif eleccion == 2: 
        print('BIENVENIDO AL MENÚ DE INSTRUCCIONES'.center(865))
        print('INSERTA 1 PARA VER COMO SE JUEGA BATTLESHIP'.center(865)) 
        print('INSERTA 2 SI DESEAS SABER LAS REGLAS DEL JUEGO'.center(865)) 
        reglas_o_instrucciones = int(input(' '))
        if reglas_o_instrucciones == 1: 
            print('*--- ¿CÓMO SE JUEGA BATTLESHIP? ---*'.center(865))
            print('Inserta la opción que necesites :)'.center(865))
            print('1.-Instrucciones para jugar Jugador vs I.A'.center(865))
            print('2.-Instrucicones para Jugador Vs Jugador'.center(865))
            opcion_instrucciones_de_juego = int(input(' '))
            if opcion_instrucciones_de_juego == 1: 
                print('*--- INSTRUCCIONES MODO: JUGADOR VS I.A. ---*'.center(865))
                print('1.-El usuario dispondra de 5 barcos (de diferente tamaño), y tendrá que acomodarlos en el tablero por medio de números y letras (filas y columnas), que representarían las coordenadas donde estos se encontran, por su parte la I.A ingresará automaticamente y de manera aleatoria la misma cantidad de barcos en diferentes coordenadas.') 
                print('2.-Después de haber ingresado los barcos el usuario tendrá que "disparar" mediante coordenadas, intentando acertar en algún barco enemigo.')
                print('3.-Cada que el usuario o la IA acierten un disparo se reflejara en el tablero mediante el carácter "@" y cada que el usuario o la I.A fallen se representara en el tablero mediante el símbolo "-".')
                print('4.-Si el usuario y la I.A se quedan sin disparos entonces ganará quien tenga la mayor cantidad de disparos acertados (HITS)') 
                print('5.-Si el usuario llega a 17 disparos acertados (HITS), entonces ganará la partida, por el contrario, si la I.A llega primero al número de hits establecido, la I.A ganará la partida.')
            elif opcion_instrucciones_de_juego == 2:
                print('*--- INSTRUCCIONES MODO: JUGADOR VS JUGADOR ---*'.center(865))
                print('1.-Modo clásico.'.center(865))
                print('2.-Random.'.center(865))
                modo_reglas = int(input())
                if modo_reglas == 1:
                    print('*--- BIENVENIDO A LAS INSTRUCCIONES DEL MODO: JUGADOR VS JUGADOR CLÁSICO ---*'.center(865))
                    print("\n") 
                    print('1.-Los dos usuarios dispondrán de 5 barcos de diferente tamaño, estos tendrán que ser acomodades mediante números y letras (filas y columnas) que representaría coordenadas, primero el jugador 1 ingresará sus barcos, después de esto seguirá el turno del jugador dos para ingresar sus barcos.') 
                    print('2.-Después de haber ingresado los barcos el jugador uno tendrá que "disparar" mediante coordenadas, intentando acertar en algún barco del jugador 2 y viceversa.')
                    print('3.-Cada que el Jugador uno o el Jugador dos acierten un disparo se reflejara en el tablero mediante el carácter "@" y cada que el Jugador uno o Jugador dos fallen, se representara en el tablero mediante el símbolo "-".')
                    print('4.-Si el Jugador uno y el Jugador dos se quedan sin disparos entonces ganará quien tenga la mayor cantidad de disparos acertados (HITS)') 
                    print('5.-Si el Jugador uno llega a 17 disparos acertados (HITS), entonces ganará la partida, por el contrario, si el Jugador dos llega primero al número de hits establecido, entonces ganará la partida  ganará la partida.')
                elif modo_reglas == 2:
                    print('*--- BIENVENIDO A LAS INSTRUCCIONES DEL MODO: JUGADOR VS JUGADOR RANDOM ---*'.center(865))
                    print("\n") 
                    print('1.-Los dos usuarios dispondrán de 5 barcos de diferente tamaño') 
                    print('3.-Cada que el Jugador uno o el Jugador dos acierten un disparo se reflejara en el tablero mediante el carácter "@" y cada que el Jugador uno o Jugador dos fallen, se representara en el tablero mediante el símbolo "-".')
                    print('4.-Si el Jugador uno y el Jugador dos se quedan sin disparos entonces ganará quien tenga la mayor cantidad de disparos acertados (HITS)') 
                    print('5.-Si el Jugador uno llega a 17 disparos acertados (HITS), entonces ganará la partida, por el contrario, si el Jugador dos llega primero al número de hits establecido, entonces ganará la partida  ganará la partida.')
        elif reglas_o_instrucciones == 2:
            print('*--- REGLAS DE BATTLESHIP ---*'.center(865))
            print('Inserta la opción que necesites :)'.center(865))
            print('1.-Reglas del modo: Jugador vs I.A.'.center(865))
            print('2.-Reglas del modo: Jugador vs Jugador'.center(865))
            reglas_para_cada_modo = int(input())
            if reglas_para_cada_modo == 1: 
                print('*--- REGLAS PARA EL MODO: JUGADOR VS I.A ---*')
                print('1.-No modificar el código para ver donde estan los barcos de la IA')
                print('2.- Se tienen que ingresar todos los barcos')
                print('3.- No se pueden ingresar menos de 17 tiros')
            elif reglas_para_cada_modo == 2: 
                print('*--- REGLAS PARA EL MODO: JUGADOR VS JUGADOR ---*'.center(865))
                print('1.-Modo clásico.'.center(865))
                print('2.-Random.'.center(865))
                reglas = int(input(': '))
                if reglas == 1:
                    print('1.-No modificar el código para ver donde estan los barcos de los jugadores')
                    print('2.- Cada jugador asignara un aposición a sus barcos')
                    print('3.- El usuario tendrá que introducir cuantos tiros tendrán ambos jugadores (cantidad de tiros igual para ambos')
                elif reglas == 2:
                    print('1.-No modificar el código para ver donde estan los barcos de los jugadores')
                    print('2.- La I.A asignara la posición de los valores de manera aleatoriamente para cada jugador')
                    print('3.- La I.A asignara la cantidad de disparos aleatoriamente a cada jugador')
    elif eleccion==3: 
        print ('CREDITOS'.center(865))
        print('El código en el cuál se baso este programa es de la autoria de Garrett Broughton, su canal de youtube es: https://www.youtube.com/watch?v=tF1WRCrd_HQ&t=620s&ab_channel=KnowledgeMavens ') 
        print('\n')
        print('Las modificaciones y el rediseño de la interfaz y el código son de la autoria de Alejandro Granados Moncayo y Jonathan Anell Segovia')
        print('Toda la documentación correspondiente y la explicación detallada de las funciones se encuentran anexadas en el siguiente repositorio en GitHub: https://github.com/Crymetothemoon666/BATTLESHIP..gi') 
        print('\n')
    BOTON_DE_REGRESO = int(input('Si deseas regresar el menú inserta 1: '))
    
print('*--- GRACIAS POR JUGAR, REGRESA PRONTO ---*'.center(865))
msvcrt.getch()