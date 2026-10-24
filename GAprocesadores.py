import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import copy
from typing import List, Dict

from CromosomaDecimal import CromosomaDecimal
from interfaz.aptitud import AptitudProcesadores
from interfaz.seleccion import SeleccionRuleta
from interfaz.reproducion import ReproduccionUnCruce
from interfaz.mutacion import MutacionFlip

class GA(object):
    def __init__(self, num_inv: int, num_genes: int, hyperparams: Dict):
        self.poblacion: List[CromosomaDecimal] = [CromosomaDecimal(num_genes) for _ in range(num_inv)]
        self.num_inv: int = num_inv
        self.hyperparams: Dict = hyperparams
        self.evaluar = hyperparams["Aptitud"]
        self.seleccion = hyperparams["Seleccion"]
        self.reproducion = hyperparams["Reproduccion"]
        self.mutacion = hyperparams["Mutacion"]
        self.num_remplazo: int = int(hyperparams["por_remplazo"] * num_inv)

        for i in range(num_inv):
            self.poblacion[i].llenar_random_data()

    def buscar_solucion(self, tolerancia: float, var: Dict = None):
        avg_tol: float = 99999999.99
        sum_score_prev: float = 0.0
        generacion: int = 1

        fail: bool = False
        fail_count: int = 0
        fail_score: float = 0.0

        while not fail:
            self.evaluar.evaluar_poblacion(self.poblacion, var)
            sum_scores: float = sum(cromosoma.score for cromosoma in self.poblacion)
            sum_scores /= self.num_inv

            if sum_scores != 0:
                avg_tol = abs(sum_score_prev - sum_scores) / sum_scores

            if (generacion + 1) % 100 == 0:
                print(f"[{generacion:05d}] avg_err : {avg_tol:.5f} avg_score: {sum_scores:.5f}")

            if fail_score == avg_tol:
                fail_count += 1

            if fail_count >= 10:
                fail = True
                break

            if avg_tol < tolerancia:
                break

            fail_score = avg_tol
            sum_score_prev = sum_scores

            self.poblacion = sorted(self.poblacion, key=lambda c: c.score, reverse=True)
            mating_pool = self.seleccion.seleccion_poblacion(self.poblacion)
            generacion_nueva = copy.deepcopy(self.poblacion[: self.num_remplazo])

            self.reproducion.reproduccion_poblacion(generacion_nueva, mating_pool, self.num_inv)
            self.mutacion.mutacion_poblacion(generacion_nueva)

            generacion += 1
            self.poblacion = copy.deepcopy(generacion_nueva)


def detalle_carga(cromosoma: CromosomaDecimal):
    tiempos = [8, 5, 7, 3, 6, 4]
    cargas = {1: [], 2: [], 3: []}
    tiempos_cargas = {1: 0, 2: 0, 3: 0}

    for i in range(1, cromosoma.n_genes + 1):
        proc = cromosoma.get_bits(i)
        cargas[proc].append(f"T{i}")
        tiempos_cargas[proc] += tiempos[i - 1]

    print("\n Desglose de Asignación por Procesador ")
    for p in range(1, 4):
        tareas_str = ", ".join(cargas[p]) if cargas[p] else "Ninguna"
        print(f"Procesador {p}: Tareas [{tareas_str}] -> Tiempo Total: {tiempos_cargas[p]}")
    print(f"Carga Máxima M(x): {max(tiempos_cargas.values())}")


if __name__ == "__main__":
    num_genes = 6   # 6 Tareas
    cant_ind = 100  # Población

    gaparams = {}
    gaparams["Aptitud"] = AptitudProcesadores()
    gaparams["Seleccion"] = SeleccionRuleta()       
    gaparams["Reproduccion"] = ReproduccionUnCruce(num_genes)
    gaparams["Mutacion"] = MutacionFlip(0.05)
    gaparams["por_remplazo"] = 0.5

    algoritmoGA = GA(cant_ind, num_genes, gaparams)
    algoritmoGA.buscar_solucion(1e-4)

    solucion = sorted(algoritmoGA.poblacion, key=lambda c: c.score, reverse=True)
    
    print(f"\n{'id':<7} {'Cromosoma Decimal':<20} {'Fitness':<12} {'M(x)':<10}")
    for i, cromosoma in enumerate(solucion[:10]):
        m_x = round((1.0 / cromosoma.score) - 1.0)
        print(f"[{i + 1:>2} ] {cromosoma.a_string():<20} {cromosoma.score:<12.5f} {m_x:<10}")

    mejor = solucion[0]
    detalle_carga(mejor)