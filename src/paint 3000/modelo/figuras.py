import tkinter as tk
from abc import ABC, abstractmethod
import math #importante para o cálculo do círculo 

# =============================================================================
# Hierarquia de classes
# =============================================================================

class Figura(ABC):
    """Classe base abstrata para todas as figuras."""

    def __init__(self, cor_borda: str = "black", cor_preenchimento: str = ""):
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento

    """Define a classe herdando de ABC, para que assim seja uma classe abstrata em python, salva também as cores padrões das bordas, o preto, e do preenchimento que é transparente representado pelo """

    @abstractmethod
    def desenhar(self, canvas: tk.Canvas) -> None:
        """Desenha a figura definitivamente no canvas."""

    @abstractmethod
    def desenhar_preview(self, canvas: tk.Canvas) -> None:
        """Desenha a figura como prévia (tracejada) enquanto o usuário arrasta."""

    @abstractmethod
    def atualizar(self, x: int, y: int) -> None:
        """Atualiza a figura com a posição atual do mouse (usado durante criação)."""

    @abstractmethod
    def incompleta(self) -> bool:
        """Retorna True se a figura ainda não tem dimensão mínima para ser salva."""

    def iniciar_redimensionamento(self, x: int, y: int) -> None:
        """Chamado no clique inicial antes do arraste de redimensionamento."""
        pass

    def redimensionar(self, x: int, y: int) -> None:
        """Redimensiona a figura já salva. Por padrão delega a atualizar()."""
        self.atualizar(x, y)


# -----------------------------------------------------------------------------
# Figuras
# -----------------------------------------------------------------------------

class Linha(Figura):
    def __init__(self, x1: int, y1: int, cor_borda: str = "black", cor_preenchimento: str = ""):
        super().__init__(cor_borda, cor_preenchimento)
        self.x1 = x1 # X inicial 
        self.y1 = y1 # Y inicial 
        self.x2 = x1 # X final 
        self.y2 = y1 # Y final

    def atualizar(self, x: int, y: int) -> None:
        self.x2 = x
        self.y2 = y

        ''' Atualiza apenas os X e Y finais, deixando os iniciais estáticos'''

    def desenhar(self, canvas: tk.Canvas) -> None:
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.cor_borda)

    def desenhar_preview(self, canvas: tk.Canvas) -> None:
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.cor_borda, dash=(4, 2))

        ''' o dash=(4,2) significa que será criado um traço de 4 pixels em que a cada 2 pixels ou eles são preenchidos ou ficam vazios, é a lógica do tracejado das figuras incompletas'''

    def incompleta(self) -> bool:
        return (self.x1, self.y1) == (self.x2, self.y2)


class MaoLivre(Figura):
    """Traço livre composto por todos os pontos percorridos pelo mouse."""

    def __init__(self, x: int, y: int, cor_borda: str = "black", cor_preenchimento: str = ""):
        super().__init__(cor_borda, cor_preenchimento)
        self.pontos: list[tuple[int, int]] = [(x, y)]

        ''' self.pontos é uma lista de tuplas que recebem dois valores int, em que o primeiro é sempre o valor do x e o segundo é sempre o valor do y, é uma remodelação da versão original'''

    def atualizar(self, x: int, y: int) -> None:
        self.pontos.append((x, y))

        ''' para atualizar a mão livre é só adicionar cada novo ponto selecionado pelo usuário pelo arrasto do mouse a lista de tuplas que definimos acima'''

    def iniciar_redimensionamento(self, x: int, y: int) -> None:
        self._pontos_base = list(self.pontos)
        self._min_x = min(p[0] for p in self.pontos)
        self._min_y = min(p[1] for p in self.pontos)
        self._max_x = max(p[0] for p in self.pontos)
        self._max_y = max(p[1] for p in self.pontos)

        ''' A lógica aqui é a seguinte:
        - Primeiro nós fazemos uma "fotografia" da figura desenhada pelo modo de mão livre de forma a salvar de forma exata todos os pontos da forma original, é preciso ser assim para não corromper o formato desenhado no aumento ou redução de escala
        - o min_x e o max_x pegam a menor e a maior coordenada horizontal da figura
        - o min_y e o max_y pegam a maenor e a maior coordenada vertical da figura
        É preciso ser assim porque essa feature só funciona do jeito certo com uma caixa delimitadora porque desse jeito temos salvos todos os pontos, os menores e maiores pontos x e y, além de um "retrato" de onde estão esses maiores e menores valores, dessa forma temos então a "fotografia verdadeira" de toda a figura '''

    def redimensionar(self, x: int, y: int) -> None:
        if not hasattr(self, '_pontos_base'):
            self.iniciar_redimensionamento(x, y)

        larg_base = self._max_x - self._min_x
        alt_base = self._max_y - self._min_y

        if larg_base == 0: larg_base = 1
        if alt_base == 0: alt_base = 1

        ''' o primeiro if serve apenas como trava de segurança, se por algum motivo o clique inicial for perdido, a função anterior é executada a força, sim eu peguei trauma quando não consegui fazer o ponto inicial ser processado na aula
        o larg_base e o alt_base serve apenas para definir a altura e largura originais da figura em pixels, com os ifs subsequentes servindo como forma de assegurar que não vai existir nenhuma divisão por 0, o que poderia travar o programa'''

        escala_x = (x - self._min_x) / larg_base
        escala_y = (y - self._min_y) / alt_base

        self.pontos = [
            (int(self._min_x + (p[0] - self._min_x) * escala_x),
             int(self._min_y + (p[1] - self._min_y) * escala_y))
            for p in self._pontos_base
        ]

    def desenhar(self, canvas: tk.Canvas) -> None:
        if not self.incompleta():
            canvas.create_line(self.pontos, fill=self.cor_borda)

    def desenhar_preview(self, canvas: tk.Canvas) -> None:
        if not self.incompleta():
            canvas.create_line(self.pontos, fill=self.cor_borda, dash=(4, 2))

    def incompleta(self) -> bool:
        return len(self.pontos) <= 1


class Oval(Figura):
    """Elipse definida por dois cantos opostos do retângulo delimitador."""

    def __init__(self, x1: int, y1: int, cor_borda: str = "black", cor_preenchimento: str = ""):
        super().__init__(cor_borda, cor_preenchimento)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x1
        self.y2 = y1

    def atualizar(self, x: int, y: int) -> None:
        self.x2 = x
        self.y2 = y

    def desenhar(self, canvas: tk.Canvas) -> None:
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2, outline=self.cor_borda, fill=self.cor_preenchimento)

    def desenhar_preview(self, canvas: tk.Canvas) -> None:
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2, outline=self.cor_borda, fill=self.cor_preenchimento, dash=(4, 2))

    def incompleta(self) -> bool:
        return (self.x1, self.y1) == (self.x2, self.y2)

''' Tudo em oval funciona do mesmo jeito que funciona em linha, então as mesmas explicações se aplicam também, mudando apenas a função de criação para create_oval'''


class Circulo(Figura):
    """Círculo definido por centro e raio."""

    def __init__(self, cx: int, cy: int, cor_borda: str = "black", cor_preenchimento: str = ""):
        super().__init__(cor_borda, cor_preenchimento)
        self.cx = cx
        self.cy = cy
        self.raio = 0

        ''' A principal diferença entre o círculo e as outras figuras é que os pontos salvos representam os valores X e Y do centro da figura, fiz dessa forma para ficar mais fácil, enquanto que o raio tem como valor padrão o 0, o que é uma escolha de design nossa, dá para ele ter valores iniciais expressivos também'''

    def atualizar(self, x: int, y: int) -> None:
        self.raio = int(math.hypot(x - self.cx, y - self.cy))

        ''' É justamente a função math.hypot que torna possível a criação do círculo já que ela calcula a distância em linha reta entre o centro (o clique inicial) e onde o mouse está no momento (calculando a hipotenusa de um triângulo retângulo imaginário) o que defini o tamanho exato do raio'''

    def _bbox(self) -> tuple[int, int, int, int]:
        r = self.raio
        return self.cx - r, self.cy - r, self.cx + r, self.cy + r

        ''' O Tkinter não tem uma função própria para a criação de círculos, então a ideia é criar um "quaadrado invisível" que envolve o círculo, dessa forma a função calcula os 4 cantos dessa caixa inviśivel subtraindo e somando o raio do centro, as funções desenhar e desenhar_preview apenas passam desse "quadrado" para o Tkinter'''

    def desenhar(self, canvas: tk.Canvas) -> None:
        canvas.create_oval(*self._bbox(), outline=self.cor_borda, fill=self.cor_preenchimento)

    def desenhar_preview(self, canvas: tk.Canvas) -> None:
        canvas.create_oval(*self._bbox(), outline=self.cor_borda, fill=self.cor_preenchimento, dash=(4, 2))

        '''a ideia do create_oval é porque uma figura oval é uma elipse e um círculo pode ser considerado uma elipse com excentricidade 0, ou seja, com os eixos vertical e horizontal com o mesmo tamanho, se usarmos os valores dessa função como os valores do "quadrado invisível" que formamos geometricamente temos um círculo'''

    def incompleta(self) -> bool:
        return self.raio == 0


class Poligono(Figura):
    """Polígono livre construído clique a clique."""
    
    def __init__(self, x: int, y: int, cor_borda: str = "black", cor_preenchimento: str = ""):
        super().__init__(cor_borda, cor_preenchimento)
        self.pontos: list[tuple[int, int]] = [(x, y)]
        self.mouse_x = x
        self.mouse_y = y

    def adicionar_ponto(self, x: int, y: int) -> None:
        self.pontos.append((x, y))

    def atualizar(self, x: int, y: int) -> None:
        """Durante a construção: move apenas o cursor de prévia, sem adicionar vértice."""
        self.mouse_x = x
        self.mouse_y = y

    def iniciar_redimensionamento(self, x: int, y: int) -> None:
        """Salva a geometria base do polígono para cálculo de proporção."""
        self._pontos_base = list(self.pontos)
        self._min_x = min(p[0] for p in self.pontos)
        self._min_y = min(p[1] for p in self.pontos)
        self._max_x = max(p[0] for p in self.pontos)
        self._max_y = max(p[1] for p in self.pontos)

    def redimensionar(self, x: int, y: int) -> None:
        """Aplica escala nos vértices tendo o canto superior esquerdo como âncora."""
        if not hasattr(self, '_pontos_base'):
            self.iniciar_redimensionamento(x, y)

        larg_base = self._max_x - self._min_x
        alt_base = self._max_y - self._min_y

        if larg_base == 0: larg_base = 1
        if alt_base == 0: alt_base = 1

        escala_x = (x - self._min_x) / larg_base
        escala_y = (y - self._min_y) / alt_base

        self.pontos = [
            (int(self._min_x + (p[0] - self._min_x) * escala_x),
             int(self._min_y + (p[1] - self._min_y) * escala_y))
            for p in self._pontos_base
        ]

        ''' As duas funções de redimensionamento seguem a mesma ideia tanto para os polígonos quanto para a mão livre porque as duas figuras são "complexas" do ponto de vista que não existe uma forma padrão para elas, por isso essa é a forma que encontramos de fazer iso funcionar'''

    def desenhar(self, canvas: tk.Canvas) -> None:
        if not self.incompleta():
            coords = [c for p in self.pontos for c in p]
            canvas.create_polygon(coords, outline=self.cor_borda, fill=self.cor_preenchimento)

    def desenhar_preview(self, canvas: tk.Canvas) -> None:
        pontos_preview = self.pontos + [(self.mouse_x, self.mouse_y)]
        coords = [c for p in pontos_preview for c in p]
        if len(coords) >= 4:
            canvas.create_line(coords, fill=self.cor_borda, dash=(4, 2))

    def incompleta(self) -> bool:
        return len(self.pontos) < 3