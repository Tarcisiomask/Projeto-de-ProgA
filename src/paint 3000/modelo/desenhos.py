from modelo.figuras import Figura

class Desenho:

    def __init__(self):
        self._figuras: list[Figura] = []
        self.figura_nova: Figura | None = None
        # Agora guardamos uma lista de figuras selecionadas
        self.selecionadas: list[Figura] = []

    def adicionar(self, figura: Figura) -> None:
        self._figuras.append(figura)

    def removerUltima(self) -> None:
        if self._figuras:
            self._figuras.pop()

    def limpar(self) -> None:
        self._figuras.clear()
        self.figura_nova = None
        self.selecionadas.clear()
        
    def ultima(self) -> Figura | None:
        return self._figuras[-1] if self._figuras else None

    def __iter__(self):
        return iter(self._figuras)    

    def __len__(self):
        return len(self._figuras)

    # ------------------------------------------------------------------
    # Manipulação de Seleção (Entrega 5)
    # ------------------------------------------------------------------

    def selecionar(self, figura: Figura | None, adicionar: bool = False) -> None:
        """
        Se 'adicionar' for True (Shift pressionado), junta à seleção atual.
        Caso contrário, limpa a seleção anterior.
        """
        if not adicionar:
            self.selecionadas.clear()
            
        if figura is not None and figura not in self.selecionadas:
            self.selecionadas.append(figura)

    def selecionada(self) -> list[Figura]:
        """Retorna a lista de figuras selecionadas."""
        return self.selecionadas

    def remover_selecionada(self) -> None:
        """Remove todas as figuras selecionadas do canvas e limpa a seleção."""
        for fig in self.selecionadas:
            if fig in self._figuras:
                self._figuras.remove(fig)
        self.selecionadas.clear()

    def figura_em(self, x: int, y: int) -> Figura | None:
        """Busca de trás pra frente (respeitando a ordem visual - z-index)."""
        for fig in reversed(self._figuras):
            if fig.contem_ponto(x, y):
                return fig
        return None