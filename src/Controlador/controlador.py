from tkinter import colorchooser
from Modelo.figuras import Linha, MaoLivre, Oval, Circulo, Poligono


# Mapeamento nome do menu → classe de figura
# Para adicionar um novo tipo basta incluir aqui — o controlador não precisa mudar.
_FABRICA: dict[str, type] = {
    "Linha":     Linha,
    "Mão livre": MaoLivre,
    "Oval":      Oval,
    "Círculo":   Circulo,
}


class Controladorr:
    """
    Recebe eventos da visão, atualiza o modelo e pede à visão que se redesenhe.

    Conhece o modelo e a visão, mas NÃO constrói widgets nem acessa o canvas
    diretamente, tudo que precisa do Tkinter passa pela visão.
    """

    def __init__(self, modelo, visao):
        self.Modelo = modelo   # instância de Desenho
        self.Visão  = visao    # instância de JanelaPrincipal

    # ------------------------------------------------------------------
    # Redesenho
    # ------------------------------------------------------------------

    def redesenhar(self) -> None:
        """Apaga o canvas e redesenha todas as figuras do modelo."""
        self.Visão.limpar_canvas()
        for fig in self.Modelo:
            fig.desenhar(self.Visão.canvas)

    # ------------------------------------------------------------------
    # Criação de figuras
    # ------------------------------------------------------------------

    def iniciar_figura_nova(self, event) -> None:
        tipo = self.Visão.tipo_figura_selecionado()

        if tipo == "Polígono":
            if self.Modelo.figura_nova is None:
                self.Modelo.figura_nova = Poligono(
                    event.x, event.y,
                    self.Visão.cor_borda_atual,
                    self.Visão.cor_preenchimento_atual,
                )
            else:
                self.Modelo.figura_nova.adicionar_ponto(event.x, event.y)
            self.redesenhar()
            self.Modelo.figura_nova.desenhar_preview(self.visao.canvas)
            return

        classe = _FABRICA.get(tipo)
        if classe:
            self.Modelo.figura_nova = classe(
                event.x, event.y,
                self.Visão.cor_borda_atual,
                self.Visão.cor_preenchimento_atual,
            )

    def atualizar_figura_nova(self, event) -> None:
        if self.Modelo.figura_nova is None:
            return
        self.Modelo.figura_nova.atualizar(event.x, event.y)
        self.redesenhar()
        self.Modelo.figura_nova.desenhar_preview(self.Visão.canvas)

    def incluir_figura_nova(self, event) -> None:
        fig = self.Modelo.figura_nova
        if isinstance(fig, Poligono):
            return
        if fig is not None and not fig.incompleta():
            self.Modelo.adicionar(fig)
        self.Modelo.figura_nova = None
        self.redesenhar()

    def finalizar_poligono(self, event) -> None:
        """Enter: fecha o polígono livre se tiver vértices suficientes."""
        fig = self.Modelo.figura_nova
        if isinstance(fig, Poligono):
            if not fig.incompleta():
                self.Modelo.adicionar(fig)
            self.Modelo.figura_nova = None
            self.redesenhar()

    # ------------------------------------------------------------------
    # Redimensionamento da última figura
    # ------------------------------------------------------------------

    def iniciar_redimensionamento_ultima(self, event) -> None:
        ultima = self.Modelo.ultima()
        if ultima:
            ultima.iniciar_redimensionamento(event.x, event.y)

    def redimensionar_ultima(self, event) -> None:
        ultima = self.Modelo.ultima()
        if ultima is None:
            return
        ultima.redimensionar(event.x, event.y)
        self.redesenhar()
        if self.Modelo.figura_nova is not None:
            self.Modelo.figura_nova.desenhar_preview(self.Visão.canvas)

    # ------------------------------------------------------------------
    # Prévia do polígono
    # ------------------------------------------------------------------

    def mover_preview_poligono(self, event) -> None:
        fig = self.Modelo.figura_nova
        if isinstance(fig, Poligono):
            fig.atualizar(event.x, event.y)
            self.redesenhar()
            fig.desenhar_preview(self.Visão.canvas)

    # ------------------------------------------------------------------
    # Cores
    # ------------------------------------------------------------------

    def escolher_cor_borda(self) -> None:
        cor = colorchooser.askcolor(
            color=self.Visão.cor_borda_atual, title="Cor da borda"
        )[1]
        if cor:
            self.Visão.definir_cor_borda(cor)

    def escolher_cor_preenchimento(self) -> None:
        cor = colorchooser.askcolor(
            color=self.Visão.cor_preenchimento_atual or "white",
            title="Cor de preenchimento",
        )[1]
        if cor:
            self.Visão.definir_cor_preenchimento(cor)

    def remover_preenchimento(self) -> None:
        self.Visão.definir_cor_preenchimento("")

    # ------------------------------------------------------------------
    # Outras ações
    # ------------------------------------------------------------------

    def limpar_tela(self) -> None:
        self.Modelo.limpar()
        self.redesenhar()
