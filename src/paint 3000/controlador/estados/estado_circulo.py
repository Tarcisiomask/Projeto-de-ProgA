from controlador.estados.estado import ToolState
from modelo.figuras import Circulo


class EstadoCirculo(ToolState):

    def iniciar(self, event) -> None:
        self.controlador.modelo.figura_nova = Circulo(
            event.x, event.y,
            self.controlador.visao.cor_borda_atual,
            self.controlador.visao.cor_preenchimento_atual,
        )

    def atualizar(self, event) -> None:
        fig = self.controlador.modelo.figura_nova
        if fig is None:
            return
        fig.atualizar(event.x, event.y)
        self.controlador.redesenhar()
        fig.desenhar_preview(self.controlador.visao.canvas)

    def finalizar(self, event) -> None:
        fig = self.controlador.modelo.figura_nova
        if fig is not None and not fig.incompleta():
            self.controlador.modelo.adicionar(fig)
        self.controlador.modelo.figura_nova = None
        self.controlador.redesenhar()
