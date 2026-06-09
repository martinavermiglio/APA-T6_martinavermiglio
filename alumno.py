""" 
alumno.py creado por martina vermiglio
"""

import re
import doctest

class Alumno:
    """
    clase usada para el tratamiento de las notas de los alumnos. cada uno
    incluye los atributos siguientes:

    numIden:   número de identificación. es un número entero que, en caso
               de no indicarse, toma el valor por defecto 'numIden=-1'.
    nombre:    nombre completo del alumno.
    notas:     lista de números reales con las distintas notas de cada alumno.
    """

    def __init__(self, nombre, numIden=-1, notas=[]):
        self.numIden = numIden
        self.nombre = nombre
        self.notas = [nota for nota in notas]

    def __add__(self, other):
        """
        devuelve un nuevo objeto 'alumno' con una lista de notas ampliada con
        el valor pasado como argumento. de este modo, añadir una nota a un
        alumno se realiza con la orden 'alumno += nota'.
        """
        return Alumno(self.nombre, self.numIden, self.notas + [other])

    def media(self):
        """
        devuelve la nota media del alumno.
        """
        return sum(self.notas) / len(self.notas) if self.notas else 0

    def __repr__(self):
        """
        devuelve la representación 'oficial' del alumno. a partir de copia
        y pega de la cadena obtenida es posible crear un nuevo alumno idéntico.
        """
        return f'Alumno("{self.nombre}", {self.numIden!r}, {self.notas!r})'

    def __str__(self):
        """
        devuelve la representación 'bonita' del alumno. visualiza en tres
        columnas separas por tabulador el número de identificación, el nombre
        completo y la nota media del alumno con un decimal.
        """
        return f'{self.numIden}\t{self.nombre}\t{self.media():.1f}'

def leeAlumnos(ficalum):
    """
    lee un fichero de texto con los datos de todos los alumnos y devuelve un
    diccionario en el que la clave es el nombre de cada alumno y su contenido
    el objeto 'alumno' correspondiente.

    >>> alumnos = leeAlumnos('alumnos.txt')
    >>> for alumno in alumnos:
    ...     print(alumnos[alumno])
    ...
    171	Blanca Agirrebarrenetse	9.5
    23	Carles Balcells de Lara	4.9
    68	David Garcia Fuster	7.0
    """
    # diccionario principal para almacenar las instancias creadas
    diccionario_alumnos = {}
    
    # patron regex estructurado en 3 grupos principales:
    # 1. id: extrae todos los digitos iniciales tras posibles espacios
    # 2. nombre: extrae los caracteres perezosamente hasta topar con los numeros
    # 3. notas: captura toda la secuencia final de digitos, espacios y puntos
    patron_linea = re.compile(r'^\s*(?P<id>\d+)\s+(?P<nombre>[^\d]+?)\s+(?P<notas>[\d\.\s]+)$')

    with open(ficalum, 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            # comprobamos si la linea actual encaja en nuestra expresion regular
            coincidencia = patron_linea.match(linea)
            if coincidencia:
                # conversion directa del identificador a tipo entero
                num_iden = int(coincidencia.group('id'))
                # eliminacion de espacios residuales al inicio o final del nombre
                nombre = coincidencia.group('nombre').strip()
                # troceamos la cadena de notas y convertimos cada valor a float
                notas = [float(nota) for nota in coincidencia.group('notas').split()]

                # instanciamos el objeto y lo guardamos usando el nombre como clave
                diccionario_alumnos[nombre] = Alumno(nombre, num_iden, notas)

    return diccionario_alumnos

if __name__ == '__main__':
    # ejecucion automatizada de las pruebas unitarias ignorando espacios extra
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
