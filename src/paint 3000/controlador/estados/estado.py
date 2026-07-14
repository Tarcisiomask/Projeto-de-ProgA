from abc import ABC, abstractmethod


class ToolState(ABC):
    """
    Interface abstrata do padrão State.

    Cada ferramenta de desenho é uma subclasse concreta que implementa
    os três momentos de interação com o mouse.
    O Controlador mantém uma referência ao estado atual e delega
    todos os eventos a ele — sem nenhum if/elif por tipo de ferramenta.
    """

    def __init__(self, controlador):
        # Referência ao controlador para acessar modelo e visão quando necessário
        self.controlador = controlador

    @abstractmethod
    def iniciar(self, event) -> None:
        """Botão esquerdo pressionado."""

    @abstractmethod
    def atualizar(self, event) -> None:
        """Mouse arrastado com botão esquerdo pressionado."""

    @abstractmethod
    def finalizar(self, event) -> None:
        """Botão esquerdo solto."""

    def finalizar_atalho(self, event) -> None:
        """
        Ação de teclado (Enter) ou clique direito.
        A maioria das ferramentas não usa — apenas Polígono sobrescreve.
        """
        pass

    def mover(self, event) -> None:
        """
        Movimento do mouse sem botão pressionado.
        Usado por Polígono para atualizar a prévia do próximo lado.
        """
        pass
