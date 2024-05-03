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
        current = problem.init
        value = problem.obj_val(problem.init)

        while True:

            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(current)

            # Buscar las acciones que generan el mayor incremento de valor obj
            max_acts = [act for act, val in diff.items() if val ==
                        max(diff.values())]

            # Elegir una accion aleatoria
            act = choice(max_acts)

            # Retornar si estamos en un optimo local 
            # (diferencia de valor objetivo no positiva)
            if diff[act] <= 0:

                self.tour = current
                self.value = value
                end = time()
                self.time = end-start
                return

            # Sino, nos movemos al sucesor
            else:

                current = problem.result(current, act)
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
        current = problem.init
        value = problem.obj_val(problem.init)
        bestValue = []
        iteration_values = {}

        #
        for random_iterations in range(10):
            if(random_iterations!=0):
                
                problem.init = problem.random_reset()
                start = time()
                self.niters = 0
                current = problem.init
                value = problem.obj_val(problem.init)
            

            while True:

                # Determinar las acciones que se pueden aplicar
                # y las diferencias en valor objetivo que resultan
                diff = problem.val_diff(current)

                # Buscar las acciones que generan el mayor incremento de valor obj
                max_acts = [act for act, val in diff.items() if val ==
                            max(diff.values())]

                # Elegir una accion aleatoria
                act = choice(max_acts)

                # Retornar si estamos en un optimo local 
                # (diferencia de valor objetivo no positiva)
                if diff[act] <= 0:

                    self.tour = current
                    self.value = value
                    end = time()
                    self.time = end-start
                    bestValue.append(value)
                    iteration_values[value] = [current,value,self.time,self.niters]
                    break

                # Sino, nos movemos al sucesor
                else:

                    current = problem.result(current, act)
                    value = value + diff[act]
                    self.niters += 1
        
        #Guarda las variables del mejor recorrido 
        self.tour = iteration_values[max(bestValue)][0]
        self.value = iteration_values[max(bestValue)][1]
        self.time = iteration_values[max(bestValue)][2]
        self.niters = iteration_values[max(bestValue)][3]
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
        current = problem.init
        value = problem.obj_val(problem.init)
        best = current
        list_tabu = set()
        iterations_without_improvement = 0
        self.niters = 0

        # Parámetros del algoritmo
        max_iterations_without_improvement = 70
        max_tabu_size = 10

        while iterations_without_improvement < max_iterations_without_improvement:
            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(current)

            # Buscar las acciones que generan el mayor incremento de valor obj
            max_acts = [act for act, val in diff.items() if val == max(diff.values())]

            # Elegir una acción aleatoria
            act = choice(max_acts)

            # Retornar si estamos en un óptimo local 
            # (diferencia de valor objetivo no positiva)
            if diff[act] <= 0:
                iterations_without_improvement += 1
                continue
            else:
                neighbour = problem.result(current, act)
                neighbour_tuple = tuple(neighbour)
                if neighbour_tuple not in list_tabu:
                    # Actualizar la mejor solución si el vecino es mejor
                    if problem.obj_val(neighbour) > problem.obj_val(best):
                        best = neighbour
                        value = problem.obj_val(neighbour)

                    # Actualizar lista tabú y reiniciar contador
                    list_tabu.add(neighbour_tuple)
                    iterations_without_improvement = 0

                    # Gestión de la lista tabú (eliminando el elemento más antiguo si se excede el tamaño máximo)
                    if len(list_tabu) >= max_tabu_size:
                        list_tabu.pop()

            # Sino, nos movemos al sucesor
            current = neighbour
            value = value + diff[act]
            self.niters += 1

        # Fin del reloj
        end = time()
        
        # Almacenar la información correspondiente
        self.time = end - start
        self.tour = best
        self.value = problem.obj_val(best)
        self.niters = self.niters
        return