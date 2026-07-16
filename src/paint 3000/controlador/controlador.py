from tkinter import colorchooser

from controlador.estados import (
    ToolState,
    EstadoLinha,
    EstadoMaoLivre,
    EstadoOval,
    EstadoCirculo,
    EstadoPoligono,
)
from controlador.estados.estado_selecao import EstadoSelecao

# IMPORTAÇÕES DA ENTREGA 4 (Salvar/Abrir)
from controlador.imagem import Image
from modelo.figuras import Figura

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
        
        # Gerenciador de salvar/abrir
        self.gerenciador_imagem = Image(self.visao)

    def configurar_eventos(self) -> None:
        self.visao._tipo_figura_var.trace_add(
            "write", 
            lambda *args: self.trocar_ferramenta(self.visao.tipo_figura_selecionado())
        )

        self.visao._btn_cor_borda.config(command=self.escolher_cor_borda)
        self.visao._btn_cor_preenchimento.config(command=self.escolher_cor_preenchimento)
        self.visao._btn_sem_preenchimento.config(command=self.remover_preenchimento)
        self.visao._btn_limpar.config(command=self.limpar_tela)
        
        # Binds de Salvar e Abrir (Entrega 4)
        self.visao._btn_salvar.config(command=self.salvar_projeto)
        self.visao._btn_abrir.config(command=self.abrir_projeto)

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
        self.visao.root.bind("<Delete>", self.apagar_selecionada)
        self.visao.root.bind("<BackSpace>", self.apagar_selecionada)


    def trocar_ferramenta(self, nome: str) -> None:
        classe = _ESTADOS.get(nome)
        if classe and not isinstance(self.estado_atual, classe):
            self.modelo.figura_nova = None
            self.modelo.selecionar(None) 
            self.redesenhar()
            self.estado_atual = classe(self)


    def redesenhar(self) -> None:
        self.visao.limpar_canvas()
        
        for fig in self.modelo:
            fig.desenhar(self.visao.canvas)
            
        selecionada = self.modelo.selecionada()
        if selecionada:
            selecionada.desenhar_selecionado(self.visao.canvas)


    def apagar_selecionada(self, event=None) -> None:
        self.modelo.remover_selecionada()
        self.redesenhar()

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

    # ------------------------------------------------------------------
    # Métodos de Salvar/Abrir (Entrega 4)
    # ------------------------------------------------------------------
    def salvar_projeto(self) -> None:
        # Pega as figuras do modelo e manda salvar
        self.gerenciador_imagem.figuras = list(self.modelo)
        self.gerenciador_imagem.salvar_projeto_json()

    def abrir_projeto(self) -> None:
        # Usa Figura.from_dict como Factory para recriar as figuras do JSON
        self.gerenciador_imagem.abrir_projeto_json(Figura.from_dict)
        
        # Sincroniza o modelo com os dados carregados
        if self.gerenciador_imagem.figuras:
            self.modelo.limpar()
            for fig in self.gerenciador_imagem.figuras:
                self.modelo.adicionar(fig)
            self.redesenhar()