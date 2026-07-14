from modelo.figuras import Figura

class Desenho:

    def __init__(self):
        self._figuras: list[Figura] = []
        self.figura_nova: Figura | None = None
        self._selecionada: Figura | None = None

    def adicionar(self, figura: Figura) -> None:
        self._figuras.append(figura)

    def removerUltima(self) -> None:
        if self._figuras:
            self._figuras.pop()

    def limpar(self) -> None:
        self._figuras.clear()
        self.figura_nova = None
        self._selecionada = None
        
    def ultima(self) -> Figura | None:
        return self._figuras[-1] if self._figuras else None

    def __iter__(self):
        return iter(self._figuras)    

    def __len__(self):
        return len(self._figuras)

    # ------------------------------------------------------------------
    # Manipulação de Seleção (Entrega 5)
    # ------------------------------------------------------------------

    def selecionar(self, figura: Figura | None) -> None:
        self._selecionada = figura

    def selecionada(self) -> Figura | None:
        return self._selecionada

    def remover_selecionada(self) -> None:
        if self._selecionada and self._selecionada in self._figuras:
            self._figuras.remove(self._selecionada)
            self._selecionada = None

    def figura_em(self, x: int, y: int) -> Figura | None:
        """Busca de trás pra frente (respeitando a ordem visual - z-index)."""
        for fig in reversed(self._figuras):
            if fig.contem_ponto(x, y):
                return fig
        return None