"""
horas.py creado por martina vermiglio mas
"""

import re

def normalizaHoras(fictext, ficnorm):
    """
    normaliza las expresiones horarias de un texto a formato estándar hh:mm.
    lee las líneas de fictext, realiza las sustituciones y escribe en ficnorm.
    
    """
    # patron regex compuesto para abarcar la enorme variabilidad del lenguaje hablado.
    # agrupa por: separador de dos puntos, indicador 'h', texto natural y franja del día.
    patron_horas = re.compile(
        r'\b(?P<hora>\d{1,2})'
        r'(?:(?P<colon>:)(?P<min_colon>\d{1,2})|'
        r'(?P<h_char>h)(?P<min_h>\d{1,2})?m?|'
        r'(?P<texto_min>\s+(?:en punto|y cuarto|y media|menos cuarto)))?'
        r'(?P<mod>\s+(?:de la mañana|del mediodía|de la tarde|de la noche|de la madrugada))?\b',
        re.IGNORECASE
    )

    def evalua_hora(coincidencia):
        """
        funcion de evaluacion inyectada en re.sub para procesar dinamicamente 
        cada hallazgo y discriminar los falsos positivos de las horas reales.
        """
        original = coincidencia.group(0)
        hora = int(coincidencia.group('hora'))
        minutos = 0

        # descarte inicial: si es solo un numero suelto sin atributos horarios, se ignora
        if not coincidencia.group('colon') and not coincidencia.group('h_char') and not coincidencia.group('texto_min') and not coincidencia.group('mod'):
            return original

        # analisis logico para formato estandar con dos puntos
        if coincidencia.group('colon'):
            min_str = coincidencia.group('min_colon')
            # obligamos a que los minutos esten representados por exactamente dos digitos
            if len(min_str) != 2:
                return original
            minutos = int(min_str)
            if minutos > 59 or hora > 23:
                return original

        # analisis logico para formato alfanumerico (h y m)
        elif coincidencia.group('h_char'):
            if hora > 23:
                return original
            if coincidencia.group('min_h'):
                minutos = int(coincidencia.group('min_h'))
                if minutos > 59:
                    return original

        # analisis logico para minutos expresados en formato texto
        elif coincidencia.group('texto_min'):
            # descartamos el uso del sistema de 24 horas para expresiones coloquiales
            if hora > 12 or hora == 0:
                return original
            txt = coincidencia.group('texto_min').strip().lower()
            if txt == 'en punto':
                minutos = 0
            elif txt == 'y cuarto':
                minutos = 15
            elif txt == 'y media':
                minutos = 30
            elif txt == 'menos cuarto':
                minutos = 45
                hora -= 1
                # retroceso especial: la hora previa a la 1 son las 12
                if hora == 0:
                    hora = 12

        # aplicacion de desfases temporales segun el modificador de parte del dia
        if coincidencia.group('mod'):
            mod = coincidencia.group('mod').strip().lower()
            if hora > 12 or hora == 0:
                return original

            if mod == 'de la mañana':
                if not (4 <= hora <= 12):
                    return original
                if hora == 12:
                    hora = 0
            elif mod == 'del mediodía':
                if not (hora == 12 or 1 <= hora <= 3):
                    return original
                if hora != 12:
                    hora += 12
            elif mod == 'de la tarde':
                if not (3 <= hora <= 8):
                    return original
                if hora != 12:
                    hora += 12
            elif mod == 'de la noche':
                if not (8 <= hora <= 12 or 1 <= hora <= 4):
                    return original
                if 8 <= hora <= 11:
                    hora += 12
                elif hora == 12:
                    hora = 0
            elif mod == 'de la madrugada':
                if not (1 <= hora <= 6):
                    return original

        # ajuste complementario para horas coloquiales sin modificador (00:00 a 11:59)
        else:
            if coincidencia.group('texto_min'):
                if hora == 12:
                    hora = 0

        # barrera final de seguridad para atrapar anomalias fuera de rango
        if hora > 23 or minutos > 59:
            return original

        # devolvemos el resultado combinando formato de doble digito cero-alineado
        return f'{hora:02d}:{minutos:02d}'

    # procesamiento por bloques usando manejadores de contexto
    with open(fictext, 'r', encoding='utf-8') as archivo_entrada, \
         open(ficnorm, 'w', encoding='utf-8') as archivo_salida:
        for linea in archivo_entrada:
            # ejecutamos la sustitucion inyectando la logica personalizada
            linea_normalizada = patron_horas.sub(evalua_hora, linea)
            archivo_salida.write(linea_normalizada)