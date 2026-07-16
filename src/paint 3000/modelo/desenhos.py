from modelo.figuras import Figura
from copy import deepcopy

class Desenho:

    def __init__(self):
        self._figuras: list[Figura] = []
        self.figura_nova: Figura | None = None
        # Agora guardamos uma lista de figuras selecionadas
        self.selecionadas: list[Figura] = []
        self._clipboard: list[Figura] = []

    def adicionar(self, figura: Figura) -> None:
        self._figuras.append(figura)

    def removerUltima(self) -> None:
        if self._figuras:
            self._figuras.pop()

    def limpar(self) -> None:
        self._figuras.clear()
        self.figura_nova = None
        self.selecionadas.clear()
        self._clipboard.clear()
        
    def ultima(self) -> Figura | None:
        return self._figuras[-1] if self._figuras else None

    def __iter__(self):
        return iter(self._figuras)    

    def __len__(self):
        return len(self._figuras)
    
    def copiar(self)-> None:
        if not self.selecionadas:
            return
        # deepcopy garante que as cópias mudem de posição sem alterar as originais
        self._clipboard = deepcopy(self.selecionadas)
    
    def recortar(self) -> None:
        #Copia as figuras selecionadas e as remove do desenho imediatamente.
        if not self.selecionadas:
            return
            
        self.copiar() # Reutiliza a lógica de cópia profunda
        self.remover_selecionada() # Apaga do canvas e limpa a seleção

    def colar(self) -> list[Figura]:
        #Insere as figuras do clipboard no desenho
        if not self._clipboard:
            return []
        
        novas_figuras = []
        # Cria cópias do clipboard para colar mais de uma vez (Ctrl+V)
        figuras_a_inserir = deepcopy(self._clipboard)
        # Limpa a seleção antiga para que as novas figuras coladas se tornem as selecionadas
        self.selecionadas.clear()
        for fig in figuras_a_inserir:
            self.adicionar(fig)
            self.selecionadas.append(fig) # Destaca as figuras recém-coladas
            novas_figuras.append(fig)
            
        return novas_figuras



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
    
    # ------------------------------------------------------------------
    # Movimentação em Camadas (Entrega 5)
    # ------------------------------------------------------------------
    
    def avancar_camada(self) -> None:
        """Move as figuras selecionadas um passo para a frente."""
        indices = [i for i, f in enumerate(self._figuras) if f in self.selecionadas]
        
        for i in reversed(indices):
            if i < len(self._figuras) - 1:
                self._figuras[i], self._figuras[i + 1] = self._figuras[i + 1], self._figuras[i]

    def recuar_camada(self) -> None:
        """Move as figuras selecionadas um passo para trás."""
        indices = [i for i, f in enumerate(self._figuras) if f in self.selecionadas]
        
        for i in indices:
            if i > 0:
                self._figuras[i], self._figuras[i - 1] = self._figuras[i - 1], self._figuras[i]
