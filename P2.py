import sys


class Atomo:
    def __init__(self, masa, carga):
        self.masa = masa
        self.carga = carga


class GrafoConectado:
    def __init__(self):
        pass
    
'''numero_casos = int(sys.stdin.readline())
for __ in range(numero_casos):
    case_list = list(map(int, sys.stdin.readline().split()))
    n = case_list.pop(0)
    movimientos = mover_fichas(case_list, n)
    print(f"{movimientos}")'''