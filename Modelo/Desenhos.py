from Modelo.figuras import Figura

class Desenho:

    def __init__(self):
        self._figuras: list[Figura] = []
        self.figura_nova: Figura | None = None

    def adicionar(self, figura: Figura) -> None:
        self._figuras.append(figura)

    def removerUltima(self) -> None:
        if self._figuras:
            self._figuras.pop()

    def limpar (self) -> None:
        self._figuras.clear()
        self.figura_nova = None
        
    def ultima (self) -> Figura | None:
        return self._figuras[-1] if self._figuras else None

    def __iter__ (self):
        return iter(self._figuras)    

    def __len__(self):
        return len(self._figuras)
    
