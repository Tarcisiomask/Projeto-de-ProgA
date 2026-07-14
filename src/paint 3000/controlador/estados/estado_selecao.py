from controlador.estados.estado import ToolState

class EstadoSelecao(ToolState):
    """
    Ferramenta de seleção e movimentação de figuras.
    """

    def __init__(self, controlador):
        super().__init__(controlador)
        self._ultimo_x = 0
        self._ultimo_y = 0

    def iniciar(self, event) -> None:
        # Pede para o modelo procurar uma figura na coordenada clicada
        fig_clicada = self.controlador.modelo.figura_em(event.x, event.y)
        
        # Atualiza a seleção (se clicou no vazio, fig_clicada é None, o que limpa a seleção)
        self.controlador.modelo.selecionar(fig_clicada)
        
        # Salva o ponto inicial do clique para calcular o delta (dx, dy) no arraste
        self._ultimo_x = event.x
        self._ultimo_y = event.y
        
        # Redesenha a tela para exibir (ou remover) a caixa tracejada azul da seleção
        self.controlador.redesenhar()

    def atualizar(self, event) -> None:
        # Pega a figura que está selecionada no momento
        fig = self.controlador.modelo.selecionada()
        
        # Se houver uma figura selecionada, fazemos a movimentação
        if fig is not None:
            # Calcula o deslocamento (delta) em pixels desde o último milissegundo
            dx = event.x - self._ultimo_x
            dy = event.y - self._ultimo_y
            
            # Move a figura geometricamente
            fig.mover(dx, dy)
            
            # Atualiza o "último ponto" para o próximo passo do mouse
            self._ultimo_x = event.x
            self._ultimo_y = event.y
            
            # Atualiza a tela para o usuário ver a figura se movendo
            self.controlador.redesenhar()

    def finalizar(self, event) -> None:
        # Quando o usuário solta o botão do mouse, não fazemos nada.
        # A figura permanece selecionada para caso ele queira apertar <Delete>.
        pass