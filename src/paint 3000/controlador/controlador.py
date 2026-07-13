from tkinter import colorchooser

from controlador.estados import (
    ToolState,
    EstadoLinha,
    EstadoMaoLivre,
    EstadoOval,
    EstadoCirculo,
    EstadoPoligono,
)


# Mapeamento nome do menu → classe de estado.
# Para adicionar uma nova ferramenta: criar EstadoX e incluir aqui.
_ESTADOS: dict[str, type[ToolState]] = {
    "Linha":     EstadoLinha,
    "Mão livre": EstadoMaoLivre,
    "Oval":      EstadoOval,
    "Círculo":   EstadoCirculo,
    "Polígono":  EstadoPoligono,
}


class Controlador:
    """
    Intermediário entre Modelo e Visão.

    Aplica o padrão State: cada ferramenta é um objeto de estado.
    Os métodos de evento apenas delegam ao estado atual —
    não há nenhum if/elif por tipo de ferramenta aqui.
    """

    def __init__(self, modelo, visao):
        self.modelo = modelo
        self.visao  = visao
        # Estado inicial: ferramenta Linha
        self.estado_atual: ToolState = EstadoLinha(self)

    # ------------------------------------------------------------------
    # Troca de ferramenta (chamada pela visão quando o menu muda)
    # ------------------------------------------------------------------

    def trocar_ferramenta(self, nome: str) -> None:
        """
        Instancia o estado correspondente ao nome da ferramenta
        e descarta qualquer figura_nova que estava em andamento.
        """
        classe = _ESTADOS.get(nome)
        if classe and not isinstance(self.estado_atual, classe):
            self.modelo.figura_nova = None
            self.redesenhar()
            self.estado_atual = classe(self)

    # ------------------------------------------------------------------
    # Redesenho
    # ------------------------------------------------------------------

    def redesenhar(self) -> None:
        self.visao.limpar_canvas()
        for fig in self.modelo:
            fig.desenhar(self.visao.canvas)

    # ------------------------------------------------------------------
    # Eventos do mouse — delegam ao estado atual, sem condicionais
    # ------------------------------------------------------------------

    def iniciar_figura_nova(self, event) -> None:
        self.estado_atual.iniciar(event)

    def atualizar_figura_nova(self, event) -> None:
        self.estado_atual.atualizar(event)

    def incluir_figura_nova(self, event) -> None:
        self.estado_atual.finalizar(event)

    def finalizar_poligono(self, event) -> None:
        self.estado_atual.finalizar_atalho(event)

    def mover_preview_poligono(self, event) -> None:
        self.estado_atual.mover(event)

    # ------------------------------------------------------------------
    # Redimensionamento da última figura (independente de ferramenta)
    # ------------------------------------------------------------------

    def iniciar_redimensionamento_ultima(self, event) -> None:
        ultima = self.modelo.ultima()
        if ultima:
            ultima.iniciar_redimensionamento(event.x, event.y)

    def redimensionar_ultima(self, event) -> None:
        ultima = self.modelo.ultima()
        if ultima is None:
            return
        ultima.redimensionar(event.x, event.y)
        self.redesenhar()
        if self.modelo.figura_nova is not None:
            self.modelo.figura_nova.desenhar_preview(self.visao.canvas)

    # ------------------------------------------------------------------
    # Cores (independente de ferramenta)
    # ------------------------------------------------------------------

    def escolher_cor_borda(self) -> None:
        cor = colorchooser.askcolor(
            color=self.visao.cor_borda_atual, title="Cor da borda"
        )[1]
        if cor:
            self.visao.definir_cor_borda(cor)

    def escolher_cor_preenchimento(self) -> None:
        cor = colorchooser.askcolor(
            color=self.visao.cor_preenchimento_atual or "white",
            title="Cor de preenchimento",
        )[1]
        if cor:
            self.visao.definir_cor_preenchimento(cor)

    def remover_preenchimento(self) -> None:
        self.visao.definir_cor_preenchimento("")

    # ------------------------------------------------------------------
    # Ações gerais
    # ------------------------------------------------------------------

    def limpar_tela(self) -> None:
        self.modelo.limpar()
        self.redesenhar()
