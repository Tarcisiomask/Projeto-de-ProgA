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
from modelo.desenhos import Desenho
from controlador.imagem import Image
from modelo.figuras import Figura, Grupo

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
        
        self.visao._btn_salvar.config(command=self.salvar_projeto)
        self.visao._btn_abrir.config(command=self.abrir_projeto)
        
        self.visao._btn_subir_camada.config(command=self.camada_frente)
        self.visao._btn_descer_camada.config(command=self.camada_tras)
        self.visao._btn_agrupar.config(command=self.agrupar_selecionadas)
        self.visao._btn_desagrupar.config(command=self.desagrupar_selecionadas)
        self.visao.root.bind("<Up>", self.camada_frente)
        self.visao.root.bind("<Down>", self.camada_tras)

        self.visao.root.bind("<Control-c>", self.copiar_figuras)
        self.visao.root.bind("<Control-v>", self.colar_figuras)
        self.visao.root.bind("<Control-x>", self.recortar_figuras)
        self.visao.root.bind("<Control-g>", self.agrupar_selecionadas)
        self.visao.root.bind("<Control-u>", self.desagrupar_selecionadas)

        self.visao.canvas.bind("<ButtonPress-1>", self.iniciar_figura_nova)
        self.visao.canvas.bind("<B1-Motion>",     self.atualizar_figura_nova)
        self.visao.canvas.bind("<ButtonRelease-1>", self.incluir_figura_nova)

        self.visao.canvas.bind("<ButtonPress-3>", self.iniciar_redimensionamento_ultima)
        self.visao.canvas.bind("<ButtonPress-2>", self.iniciar_redimensionamento_ultima)
        self.visao.canvas.bind("<B3-Motion>",     self.redimensionar_ultima)
        self.visao.canvas.bind("<B2-Motion>",     self.redimensionar_ultima)

        self.visao.canvas.bind("<Motion>", self.mover_preview_poligono)
        
        self.visao.root.bind("<Return>", self.finalizar_poligono)
        self.visao.root.bind("<Delete>", self.apagar_selecionada)
        self.visao.root.bind("<BackSpace>", self.apagar_selecionada)

        self.visao.root.focus_set()


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
            
        # Agora iteramos sobre a lista de figuras selecionadas
        for fig_selecionada in self.modelo.selecionada():
            fig_selecionada.desenhar_selecionado(self.visao.canvas)


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
            self._aplicar_cor_selecionadas("borda", cor)

    def escolher_cor_preenchimento(self) -> None:
        cor = colorchooser.askcolor(
            color=self.visao.cor_preenchimento_atual or "white",
            title="Cor de preenchimento",
        )[1]
        if cor:
            self.visao.definir_cor_preenchimento(cor)
            self._aplicar_cor_selecionadas("preenchimento", cor)

    def remover_preenchimento(self) -> None:
        self.visao.definir_cor_preenchimento("")
        self._aplicar_cor_selecionadas("preenchimento", "")

    def _aplicar_cor_selecionadas(self, tipo: str, cor: str) -> None:
        """Função nova: Se houver algo selecionado, aplica a cor imediatamente."""
        selecionadas = self.modelo.selecionada()
        if selecionadas:
            for fig in selecionadas:
                if tipo == "borda":
                    fig.cor_borda = cor
                elif tipo == "preenchimento":
                    fig.cor_preenchimento = cor
            self.redesenhar()

    def limpar_tela(self) -> None:
        self.modelo.limpar()
        self.redesenhar()

    def salvar_projeto(self) -> None:
        self.gerenciador_imagem.figuras = list(self.modelo)
        self.gerenciador_imagem.salvar_projeto_json()

    def abrir_projeto(self) -> None:
        self.gerenciador_imagem.abrir_projeto_json(Figura.from_dict)
        if self.gerenciador_imagem.figuras:
            self.modelo.limpar()
            for fig in self.gerenciador_imagem.figuras:
                self.modelo.adicionar(fig)
            self.redesenhar()
            
    def camada_frente(self, event=None) -> None:
        self.modelo.avancar_camada()
        self.redesenhar()

    def camada_tras(self, event=None) -> None:
        self.modelo.recuar_camada()
        self.redesenhar()
    
    def copiar_figuras(self, event=None) -> None:
        self.modelo.copiar()

    def recortar_figuras(self, event=None) -> None:
        self.modelo.recortar()
        self.redesenhar()

    def agrupar_selecionadas(self, event=None) -> None:
        """Agrupa em um único grupo todas as figuras selecionadas."""
        selecionadas = list(self.modelo.selecionada())
        if len(selecionadas) <= 1:
            return

        novo_grupo = Grupo(selecionadas)
        for fig in selecionadas:
            self.modelo.remover_figura(fig)

        self.modelo.adicionar(novo_grupo)
        self.modelo.selecionar(novo_grupo)
        self.redesenhar()

    def desagrupar_selecionadas(self, event=None) -> None:
        """Separa os grupos selecionados em suas figuras internas."""
        selecionadas = list(self.modelo.selecionada())
        if not selecionadas:
            return

        novas_selecionadas = []
        for fig in selecionadas:
            if isinstance(fig, Grupo):
                self.modelo.remover_figura(fig)
                for sub_fig in fig.figuras:
                    self.modelo.adicionar(sub_fig)
                    novas_selecionadas.append(sub_fig)
            else:
                novas_selecionadas.append(fig)

        self.modelo.selecionadas.clear()
        self.modelo.selecionadas.extend(novas_selecionadas)
        self.redesenhar()

    def colar_figuras(self, event=None) -> None:
        """Pede ao modelo para colar as figuras e manda a visão desenhar os novos clones."""
        # O modelo cola e nos devolve a lista das novas instâncias que foram criadas
        novas = self.modelo.colar()
        
        if novas:
            self.redesenhar()

