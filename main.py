import tkinter as tk
from tkinter import ttk, colorchooser
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


# =============================================================================
# Funções de callback e estado global
# =============================================================================

figuras: list[Figura] = []
figura_nova: Figura | None = None

cor_borda_atual = "black"
cor_preenchimento_atual = ""

_FABRICA: dict[str, type] = {
    "Linha":     Linha,
    "Mão livre": MaoLivre,
    "Oval":      Oval,
    "Círculo":   Circulo,
}

def iniciar_figura_nova(event):
    global figura_nova
    tipo = tipo_figura_var.get()

    if tipo == "Polígono":
        if figura_nova is None:
            figura_nova = Poligono(event.x, event.y, cor_borda_atual, cor_preenchimento_atual)
        else:
            figura_nova.adicionar_ponto(event.x, event.y)
        desenhar()
        figura_nova.desenhar_preview(canvas)
        return

    classe = _FABRICA.get(tipo)
    if classe:
        figura_nova = classe(event.x, event.y, cor_borda_atual, cor_preenchimento_atual)
''' Não guardei a classe polígonos na fábrica, porque ele tem uma lógica específica, como todas as outras figuras seguem uma lógica semelhante fica mais fácil chamar a fábrica para elas'''

def atualizar_figura_nova(event):
    if figura_nova is None:
        return
    figura_nova.atualizar(event.x, event.y)
    desenhar()
    figura_nova.desenhar_preview(canvas)

def incluir_figura_nova(event):
    global figura_nova
    if isinstance(figura_nova, Poligono):
        return
    if figura_nova is not None and not figura_nova.incompleta():
        figuras.append(figura_nova)
    figura_nova = None
    desenhar()

def finalizar_poligono(event):
    """Enter: fecha o polígono livre em construção se tiver vértices suficientes."""
    global figura_nova
    if isinstance(figura_nova, Poligono):
        if not figura_nova.incompleta():
            figuras.append(figura_nova)
        figura_nova = None
        desenhar()

def desenhar():
    canvas.delete("all")
    for fig in figuras:
        fig.desenhar(canvas)

def limpar_tela():
    global figuras, figura_nova
    figuras.clear()
    figura_nova = None
    desenhar()

def escolher_cor_borda():
    global cor_borda_atual
    cor = colorchooser.askcolor(color=cor_borda_atual, title="Cor da borda")[1]
    if cor:
        cor_borda_atual = cor
        amostra_borda.config(bg=cor_borda_atual)

def escolher_cor_preenchimento():
    global cor_preenchimento_atual
    cor = colorchooser.askcolor(color=cor_preenchimento_atual or "white",
                                 title="Cor de preenchimento")[1]
    if cor:
        cor_preenchimento_atual = cor
        amostra_preenchimento.config(bg=cor_preenchimento_atual)

def remover_preenchimento():
    global cor_preenchimento_atual
    cor_preenchimento_atual = ""
    amostra_preenchimento.config(bg="white")

# =============================================================================
# Interface
# =============================================================================

def main():
    global canvas, tipo_figura_var, amostra_borda, amostra_preenchimento

    root = tk.Tk()
    root.title("Ferramenta de Desenho")
    root.geometry("750x750") 

    frame = tk.Frame(root)
    frame.pack(expand=True, anchor="center") 
    paddings = {"padx": 5, "pady": 5}

    ttk.Label(frame, text="Ferramenta:").grid(column=0, row=0, sticky=tk.W, **paddings)
    tipo_figura_var = tk.StringVar(root)
    ttk.OptionMenu(
        frame, tipo_figura_var,
        "Linha",        
        "Linha", "Mão livre",
        "Oval", "Círculo",
        "Polígono",
    ).grid(column=1, row=0, sticky=tk.W, **paddings)

    ttk.Label(frame, text="Cor da borda:").grid(column=2, row=0, sticky=tk.W, **paddings)
    amostra_borda = tk.Label(frame, bg=cor_borda_atual, width=3, relief=tk.SUNKEN)
    amostra_borda.grid(column=3, row=0, sticky=tk.W, **paddings)
    ttk.Button(frame, text="Escolher...", command=escolher_cor_borda).grid(
        column=4, row=0, sticky=tk.W, **paddings)

    ttk.Label(frame, text="Preenchimento:").grid(column=0, row=1, sticky=tk.W, **paddings)
    amostra_preenchimento = tk.Label(frame, bg="white", width=3, relief=tk.SUNKEN)
    amostra_preenchimento.grid(column=1, row=1, sticky=tk.W, **paddings)
    ttk.Button(frame, text="Escolher...", command=escolher_cor_preenchimento).grid(
        column=2, row=1, sticky=tk.W, **paddings)
    ttk.Button(frame, text="Sem preenchimento", command=remover_preenchimento).grid(
        column=3, row=1, columnspan=2, sticky=tk.W, **paddings)

    ttk.Button(frame, text="Limpar", command=limpar_tela).grid(
        column=0, row=2, sticky=tk.W, **paddings)
    ttk.Label(
        frame,
        text="Polígono livre: clique = vértice | Enter = fechar",
        foreground="gray",
    ).grid(column=1, row=2, columnspan=4, sticky=tk.W, **paddings)

    canvas = tk.Canvas(frame, bg="white", width=600, height=600, relief=tk.RAISED, bd=2)
    canvas.grid(column=0, row=3, columnspan=5, sticky=tk.W, **paddings)

    canvas.bind("<ButtonPress-1>", iniciar_figura_nova)
    canvas.bind("<B1-Motion>", atualizar_figura_nova)
    canvas.bind("<ButtonRelease-1>", incluir_figura_nova)
    canvas.bind("<Motion>", mover_preview_poligono)
    root.bind("<Return>", finalizar_poligono)

    root.mainloop()

if __name__ == "__main__":
    main()
