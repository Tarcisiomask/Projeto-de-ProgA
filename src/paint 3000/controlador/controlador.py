from tkinter import colorchooser

from controlador.estados import (
    ToolState,
    EstadoLinha,
    EstadoMaoLivre,
    EstadoOval,
    EstadoCirculo,
    EstadoPoligono,
)
# IMPORT NOVO
from controlador.estados.estado_selecao import EstadoSelecao

# Adicionamos "Selecionar" no dicionário de estados
_ESTADOS: dict[str, type[ToolState]] = {
    "Selecionar": EstadoSelecao,
    "Linha":     EstadoLinha,
    "Mão livre": EstadoMaoLivre,
    "Oval":      EstadoOval,
    "Círculo":   EstadoCirculo,
    "Polígono":  EstadoPoligono,
}


class Controlador:

    def __init__(self, modelo, visao):
        self.modelo = modelo
        self.visao  = visao
        self.estado_atual: ToolState = EstadoLinha(self)

    def configurar_eventos(self) -> None:
        self.visao._tipo_figura_var.trace_add(
            "write", 
            lambda *args: self.trocar_ferramenta(self.visao.tipo_figura_selecionado())
        )

        self.visao._btn_cor_borda.config(command=self.escolher_cor_borda)
        self.visao._btn_cor_preenchimento.config(command=self.escolher_cor_preenchimento)
        self.visao._btn_sem_preenchimento.config(command=self.remover_preenchimento)
        self.visao._btn_limpar.config(command=self.limpar_tela)

        self.visao.canvas.bind("<ButtonPress-1>", self.iniciar_figura_nova)
        self.visao.canvas.bind("<B1-Motion>",     self.atualizar_figura_nova)
        self.visao.canvas.bind("<ButtonRelease-1>", self.incluir_figura_nova)

        self.visao.canvas.bind("<ButtonPress-3>", self.iniciar_redimensionamento_ultima)
        self.visao.canvas.bind("<ButtonPress-2>", self.iniciar_redimensionamento_ultima)
        self.visao.canvas.bind("<B3-Motion>",     self.redimensionar_ultima)
        self.visao.canvas.bind("<B2-Motion>",     self.redimensionar_ultima)

        self.visao.canvas.bind("<Motion>", self.mover_preview_poligono)
        
        # Teclado
        self.visao.root.bind("<Return>", self.finalizar_poligono)
        # ATALHOS NOVOS: Apagar figura selecionada
        self.visao.root.bind("<Delete>", self.apagar_selecionada)
        self.visao.root.bind("<BackSpace>", self.apagar_selecionada)


    def trocar_ferramenta(self, nome: str) -> None:
        classe = _ESTADOS.get(nome)
        if classe and not isinstance(self.estado_atual, classe):
            self.modelo.figura_nova = None
            # Limpa a seleção ao trocar de ferramenta (evita bugs de apagar algo enquanto desenha)
            self.modelo.selecionar(None) 
            self.redesenhar()
            self.estado_atual = classe(self)


    def redesenhar(self) -> None:
        self.visao.limpar_canvas()
        
        # Desenha todas as figuras normais primeiro
        for fig in self.modelo:
            fig.desenhar(self.visao.canvas)
            
        # Desenha o highlight (caixa tracejada azul) POR ÚLTIMO para ficar por cima de tudo
        selecionada = self.modelo.selecionada()
        if selecionada:
            selecionada.desenhar_selecionado(self.visao.canvas)


    # NOVO MÉTODO: Apagar figura
    def apagar_selecionada(self, event=None) -> None:
        self.modelo.remover_selecionada()
        self.redesenhar()


    # ... (Os métodos de clique de mouse, redimensionamento e cores continuam iguais ao que já tínhamos) ...

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

    def limpar_tela(self) -> None:
        self.modelo.limpar()
        self.redesenhar()