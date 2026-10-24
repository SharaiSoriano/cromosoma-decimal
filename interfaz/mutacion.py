import random
from abc import ABC, abstractmethod
from typing import List
from CromosomaDecimal import CromosomaDecimal

class Mutacion(ABC):
    @abstractmethod
    def mutacion_poblacion(self, poblacion: List[CromosomaDecimal]):
        pass

class MutacionFlip(Mutacion):
    def __init__(self, probabilidad: float):
        super().__init__()
        self.prob = probabilidad

    def mutacion_poblacion(self, poblacion: List[CromosomaDecimal]):
        for crom in poblacion:
            for i in range(1, crom.n_genes + 1):
                if random.random() < self.prob:
                    nuevo_proc = random.randint(1, 3)
                    crom.set_bits(nuevo_proc, i)