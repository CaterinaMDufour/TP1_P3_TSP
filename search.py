"""Este modulo define la clase LocalSearch.

LocalSearch representa un algoritmo de busqueda local general.

Las subclases que se encuentran en este modulo son:

* HillClimbing: algoritmo de ascension de colinas. Se mueve al sucesor con
mejor valor objetivo, y los empates se resuelvan de forma aleatoria.
Ya viene implementado.

* HillClimbingReset: algoritmo de ascension de colinas de reinicio aleatorio.
No viene implementado, se debe completar.

* Tabu: algoritmo de busqueda tabu.
No viene implementado, se debe completar.
"""


from __future__ import annotations
from problem import OptProblem, TSP
from random import choice
from time import time


class LocalSearch:
    """Clase que representa un algoritmo de busqueda local general."""

    def __init__(self) -> None:
        """Construye una instancia de la clase."""
        self.niters = 0  # Numero de iteraciones totales
        self.time = 0  # Tiempo de ejecucion
        self.tour = []  # Solucion, inicialmente vacia
        self.value = None  # Valor objetivo de la solucion

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion."""
        self.tour = problem.init
        self.value = problem.obj_val(problem.init)


class HillClimbing(LocalSearch):
    """Clase que representa un algoritmo de ascension de colinas.

    En cada iteracion se mueve al estado sucesor con mejor valor objetivo.
    El criterio de parada es alcanzar un optimo local.
    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Arrancamos del estado inicial
        actual = problem.init
        value = problem.obj_val(problem.init)

        while True:

            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual)

            # Buscar las acciones que generan el mayor incremento de valor obj
            max_acts = [act for act, val in diff.items() if val ==
                        max(diff.values())]

            # Elegir una accion aleatoria
            act = choice(max_acts)

            # Retornar si estamos en un optimo local 
            # (diferencia de valor objetivo no positiva)
            if diff[act] <= 0:

                self.tour = actual
                self.value = value
                end = time()
                self.time = end-start
                return

            # Sino, nos movemos al sucesor
            else:

                actual = problem.result(actual, act)
                value = value + diff[act]
                self.niters += 1


class HillClimbingReset(LocalSearch):
    """
    El algoritmo de Ascensión de Colinas con reinicio aleatorio realiza varias iteraciones. 
    Cuando alcanza un máximo local, reinicia desde un estado inicial aleatorio y retorna
    el mejor estado encontrado.
    """
    def solve(self, problem: TSP):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Arrancamos del estado inicial
        actual = problem.init
        value = problem.obj_val(problem.init)
        iteracionesRandom = 0
        mejorValor = []
        valoresIteraciones = {}
        while iteracionesRandom < 10:
            if(iteracionesRandom!=0):
                
                problem.init = problem.random_reset()
                start = time()
                self.niters = 0
                actual = problem.init
                value = problem.obj_val(problem.init)
            iteracionesRandom += 1

            while True:

                # Determinar las acciones que se pueden aplicar
                # y las diferencias en valor objetivo que resultan
                diff = problem.val_diff(actual)

                # Buscar las acciones que generan el mayor incremento de valor obj
                max_acts = [act for act, val in diff.items() if val ==
                            max(diff.values())]

                # Elegir una accion aleatoria
                act = choice(max_acts)

                # Retornar si estamos en un optimo local 
                # (diferencia de valor objetivo no positiva)
                if diff[act] <= 0:

                    self.tour = actual
                    self.value = value
                    end = time()
                    self.time = end-start
                    mejorValor.append(value)
                    valoresIteraciones[value] = [actual,value,self.time,self.niters]
                    break

                # Sino, nos movemos al sucesor
                else:

                    actual = problem.result(actual, act)
                    value = value + diff[act]
                    self.niters += 1
        if (iteracionesRandom >= 9):
            self.tour = valoresIteraciones[max(mejorValor)][0]
            self.value = valoresIteraciones[max(mejorValor)][1]
            self.time = valoresIteraciones[max(mejorValor)][2]
            self.niters = valoresIteraciones[max(mejorValor)][3]
            return

class Tabu(LocalSearch):
    """
    Algoritmo de búsqueda tabú.
    Utiliza una lista tabú para mantener un registro de los movimientos previamente realizados
    y evita quedar atrapado en ciclos o en óptimos locales utilizando estrategias.

    El criterio de parada que se utiliza es el de iteraciones sin mejora en el valor objetivo.
    """

    def solve(self, problem: TSP):
        """
        Resuelve un problema de optimización con búsqueda tabú.

        Argumentos:
        ==========
        problem: TSP
        """
        # Inicio del reloj
        start = time()

        # Arrancamos del estado inicial
        actual = problem.init
        value = problem.obj_val(problem.init)
        mejor = actual
        lista_tabu = set()
        iteraciones_sin_mejora = 0
        self.niters = 0

        # Parámetros del algoritmo
        max_iteraciones_sin_mejora = 70
        max_tabu_tam = 10

        while iteraciones_sin_mejora < max_iteraciones_sin_mejora:
            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual)

            # Buscar las acciones que generan el mayor incremento de valor obj
            max_acts = [act for act, val in diff.items() if val == max(diff.values())]

            # Elegir una acción aleatoria
            act = choice(max_acts)

            # Retornar si estamos en un óptimo local 
            # (diferencia de valor objetivo no positiva)
            if diff[act] <= 0:
                iteraciones_sin_mejora += 1
                continue
            else:
                vecino = problem.result(actual, act)
                vecino_tupla = tuple(vecino)
                if vecino_tupla not in lista_tabu:
                    # Actualizar la mejor solución si el vecino es mejor
                    if problem.obj_val(vecino) > problem.obj_val(mejor):
                        mejor = vecino
                        value = problem.obj_val(vecino)

                    # Actualizar lista tabú y reiniciar contador
                    lista_tabu.add(vecino_tupla)
                    iteraciones_sin_mejora = 0

                    # Gestión de la lista tabú (eliminando el elemento más antiguo si se excede el tamaño máximo)
                    if len(lista_tabu) >= max_tabu_tam:
                        lista_tabu.pop()

            # Sino, nos movemos al sucesor
            actual = vecino
            value = value + diff[act]
            self.niters += 1

        # Fin del reloj
        end = time()
        
        # Almacenar la información correspondiente
        self.time = end - start
        self.tour = mejor
        self.value = problem.obj_val(mejor)
        self.niters = self.niters
        return