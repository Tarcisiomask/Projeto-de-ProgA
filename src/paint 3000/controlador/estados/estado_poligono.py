from controlador.estados.estado import ToolState
from modelo.figuras import Poligono


class EstadoPoligono(ToolState):
    """
    Ferramenta de polígono livre.

    Fluxo diferente das outras ferramentas:
      - iniciar()          → adiciona vértice (não arrasta)
      - atualizar()        → não faz nada (arrasto não tem significado aqui)
      - finalizar()        → não faz nada (soltar o botão também não)
      - mover()            → atualiza a prévia do próximo lado
      - finalizar_atalho() → Enter fecha o polígono
    """

    def iniciar(self, event) -> None:
        fig = self.controlador.modelo.figura_nova
        if fig is None:
            self.controlador.modelo.figura_nova = Poligono(
                event.x, event.y,
                self.controlador.visao.cor_borda_atual,
                self.controlador.visao.cor_preenchimento_atual,
            )
        else:
            fig.adicionar_ponto(event.x, event.y)
        self.controlador.redesenhar()
        self.controlador.modelo.figura_nova.desenhar_preview(
            self.controlador.visao.canvas
        )

    def atualizar(self, event) -> None:
        # Arrasto não tem significado para o polígono clique a clique
        pass

    def finalizar(self, event) -> None:
        # Soltar o botão também não fecha o polígono
        pass

    def mover(self, event) -> None:
        """Atualiza a linha de prévia do próximo lado enquanto o mouse se move."""
        fig = self.controlador.modelo.figura_nova
        if fig is None:
            return
        fig.atualizar(event.x, event.y)
        self.controlador.redesenhar()
        fig.desenhar_preview(self.controlador.visao.canvas)

    def finalizar_atalho(self, event) -> None:
        """Enter: fecha o polígono se tiver vértices suficientes."""
        fig = self.controlador.modelo.figura_nova
        if fig is None:
            return
        if not fig.incompleta():
            self.controlador.modelo.adicionar(fig)
        self.controlador.modelo.figura_nova = None
        self.controlador.redesenhar()
