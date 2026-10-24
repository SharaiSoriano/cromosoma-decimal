import random
from abc import ABC, abstractmethod
from typing import List
from CromosomaDecimal import CromosomaDecimal

class Seleccion(ABC):
    @abstractmethod
    def seleccion_poblacion(self, poblacion: List[CromosomaDecimal]) -> List[CromosomaDecimal]:
        pass

class SeleccionRuleta(Seleccion):
    def seleccion_poblacion(self, poblacion: List[CromosomaDecimal]) -> List[CromosomaDecimal]:
        ganadores = []
        total_score = sum(c.score for c in poblacion)
        
        if total_score == 0:
            return random.choices(poblacion, k=len(poblacion))

        # Suma acumulada para la ruleta
        probabilidades = [c.score / total_score for c in poblacion]
        
        for _ in range(len(poblacion)):
            ganador = random.choices(poblacion, weights=probabilidades, k=1)[0]
            ganadores.append(ganador)
            
        return ganadores