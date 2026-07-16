from controlador.estados.estado import ToolState

class EstadoSelecao(ToolState):
    """
    Ferramenta de seleção e movimentação de figuras.
    Suporta seleção múltipla utilizando a tecla Shift.
    """

    def __init__(self, controlador):
        super().__init__(controlador)
        self._ultimo_x = 0
        self._ultimo_y = 0

    def iniciar(self, event) -> None:
        # Detecta se a tecla Shift está pressionada (estado 0x0001 no Tkinter)
        shift_pressionado = (event.state & 0x0001) != 0
        
        # Pede para o modelo procurar uma figura na coordenada clicada
        fig_clicada = self.controlador.modelo.figura_em(event.x, event.y)
        
        selecionadas = self.controlador.modelo.selecionada()
        
        # Se clicou em uma figura já selecionada SEM o shift, 
        # não limpamos a seleção, pois o usuário pode querer arrastar o bloco todo.
        if fig_clicada and fig_clicada in selecionadas and not shift_pressionado:
            pass
        else:
            self.controlador.modelo.selecionar(fig_clicada, adicionar=shift_pressionado)
        
        # Salva o ponto inicial do clique para calcular o delta (dx, dy) no arraste
        self._ultimo_x = event.x
        self._ultimo_y = event.y
        
        # Redesenha a tela para exibir (ou remover) a caixa tracejada azul da seleção
        self.controlador.redesenhar()

    def atualizar(self, event) -> None:
        # Pega a lista de figuras selecionadas
        selecionadas = self.controlador.modelo.selecionada()
        
        # Se houver figuras selecionadas, fazemos a movimentação
        if selecionadas:
            # Calcula o deslocamento (delta) em pixels
            dx = event.x - self._ultimo_x
            dy = event.y - self._ultimo_y
            
            # Move TODAS as figuras selecionadas
            for fig in selecionadas:
                fig.mover(dx, dy)
            
            # Atualiza o "último ponto" para o próximo passo do mouse
            self._ultimo_x = event.x
            self._ultimo_y = event.y
            
            self.controlador.redesenhar()

    def finalizar(self, event) -> None:
        # Quando o usuário solta o botão do mouse, a figura permanece selecionada.
        pass