import random
from typing import List

class CromosomaDecimal(object):
    def __init__(self, genes: int = 6):
        self.n_genes: int = genes
        self.score: float = -1.0
        self.genes: List[int] = [1] * self.n_genes

    def llenar_random_data(self):
        self.genes = [random.randint(1, 3) for _ in range(self.n_genes)]

    def get_bits(self, gen: int) -> int:
        return self.genes[gen - 1]

    def set_bits(self, valor: int, gen: int) -> None:
        self.genes[gen - 1] = valor

    def a_string(self) -> str:
        return "".join(str(g) for g in self.genes)