from abc import ABC, abstractmethod
from typing import List, Dict
from CromosomaDecimal import CromosomaDecimal

class Aptitud(ABC):
    @abstractmethod
    def evaluar_poblacion(self, poblacion: List[CromosomaDecimal], var: Dict = None):
        pass

class AptitudProcesadores(Aptitud):
    def evaluar_poblacion(self, poblacion: List[CromosomaDecimal], var: Dict = None):
        tiempos = [8, 5, 7, 3, 6, 4] # T1, T2, T3, T4, T5, T6

        for cromosoma in poblacion:
            cargas = {1: 0, 2: 0, 3: 0} # Carga acumulada para P1, P2 y P3
            
            for i in range(1, cromosoma.n_genes + 1):
                procesador = cromosoma.get_bits(i)
                cargas[procesador] += tiempos[i - 1]

            max_carga = max(cargas.values())
            
            cromosoma.score = 1.0 / (1.0 + max_carga)