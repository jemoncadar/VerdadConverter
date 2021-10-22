import itertools

CONECTIVAS = {
    'a': [0, None],
    'b': [0, None],
    'NOT': [1, lambda a: not a],
    'AND': [2, lambda a, b: a and b],
    'OR': [2, lambda a, b: a or b],
    'IMP': [2, lambda a, b: (not a) or b],
    'SII': [2, lambda a, b: (a and b) or (not a and not b)],
    'XOR': [2, lambda a, b: (a and not b) or (not a and b)],
    'NIMP': [2, lambda a, b: a and not b],
    'NAND': [2, lambda a, b: not (a and b)],
    'NOR': [2, lambda a, b: not (a or b)],
    'V': [0, True],
    'F': [0, False]
}


def lon(expr, i):
    len_expr = len(expr)
    conec = expr[i]
    if i >= len_expr:
        raise ValueError('Expr mal formada')

    try:
        if CONECTIVAS[conec][0] == 0:
            return 1
        elif CONECTIVAS[conec][0] == 1:
            return 1 + lon(expr, i + 1)
        elif CONECTIVAS[conec][0] == 2:
            long_izq = lon(expr, i + 1)
            long_der = lon(expr, i + long_izq + 1)
            return long_der + long_izq + 1
    except IndexError as e:
        #print(e)
        raise ValueError('Expr mal formada')


def exe(expr, i, interp):
    len_expr = len(expr)
    conec = expr[i]

    if i >= len_expr:
        raise ValueError('Expr mal formada')

    try:
        if CONECTIVAS[conec][0] == 0:
            if CONECTIVAS[conec][1] is None:
                return interp[conec]
            else:
                return CONECTIVAS[conec][1]
        elif CONECTIVAS[conec][0] == 1:
            return CONECTIVAS[conec][1](exe(expr, i + 1, interp))
        elif CONECTIVAS[conec][0] == 2:
            exe_izq = exe(expr, i + 1, interp)
            long_izq = lon(expr, i + 1)
            exe_der = exe(expr, i + long_izq + 1, interp)
            return CONECTIVAS[conec][1](exe_izq, exe_der)
    except IndexError as e:
        #print(e)
        raise ValueError('Expr mal formada')

def tab(expr):
    result = list()
    for (a, b) in (False, False), (False, True), (True, False), (True, True):
        interp = {'a': a, 'b': b}
        result.append(exe(expr, 0, interp))
    return result

if __name__ == '__main__':

    TAB_BUSCADA = tab(['AND', 'a', 'b']) # <---- Expresión de la que se quiere obtener el equivalente
    CON_DISP = ['SII', 'OR', 'a', 'b'] # <---- Expresiones que se pueden usar
    LIMIT = 20

    i = 1
    encontrada = False

    while not encontrada and i <= LIMIT:
        print('Comprobando long', i)
        for expr in itertools.product(CON_DISP, repeat=i):
            try:
                tab_calculada = tab(expr)
                if tab_calculada == TAB_BUSCADA:
                    print('ENCONTRADA!', expr)
                    encontrada = True
                    #break
            except ValueError:
                pass
        i += 1
    if not encontrada:
        print("No se encontró :(")
