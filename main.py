import tkinter as tk
from tkinter import ttk, colorchooser
from abc import ABC, abstractmethod


# =============================================================================
# Hierarquia de classes – módulo será separado na Entrega 3
# =============================================================================

class Figura(ABC):
    """Classe base abstrata para todas as figuras."""

    def __init__(self, cor_borda: str = "black", cor_preenchimento: str = ""):
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento

    @abstractmethod
    def desenhar(self, canvas: tk.Canvas) -> None:
        """Desenha a figura definitivamente no canvas."""

    @abstractmethod
    def desenhar_preview(self, canvas: tk.Canvas) -> None:
        """Desenha a figura como prévia (tracejada) enquanto o usuário arrasta."""

    @abstractmethod
    def atualizar(self, x: int, y: int) -> None:
        """Atualiza a figura com a posição atual do mouse."""

    @abstractmethod
    def incompleta(self) -> bool:
        """Retorna True se a figura ainda não tem dimensão mínima para ser salva."""


class Linha(Figura):
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
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.cor_borda)

    def desenhar_preview(self, canvas: tk.Canvas) -> None:
        canvas.create_line(self.x1, self.y1, self.x2, self.y2,
                           fill=self.cor_borda, dash=(4, 2))

    def incompleta(self) -> bool:
        return (self.x1, self.y1) == (self.x2, self.y2)
    

class Rabisco(Figura):
    def __init__(self, x1: int, y1: int, cor_borda: str = "black", cor_preenchimento: str = ""):
        super().__init__(cor_borda, cor_preenchimento)
        self.x1 = x1
        self.y1 = y1

    def atualizar(self, x: int, y: int) -> None:
        self.x2 = x
        self.y2 = y

    def desenhar(self, canvas: tk.Canvas) -> None:
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.cor_borda)

    def desenhar_preview(self, canvas: tk.Canvas) -> None:
        canvas.create_line(self.x1, self.y1, self.x2, self.y2,
                           fill=self.cor_borda, dash=(4, 2))

    def incompleta(self) -> bool:
        return (self.x1, self.y1) == (self.x2, self.y2)
    


class Retangulo(Figura):
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
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline = self.cor_borda, fill=self.cor_preenchimento)

    def desenhar_preview(self, canvas: tk.Canvas) -> None:
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline = self.cor_borda, fill=self.cor_preenchimento
                           , dash=(4, 2))

    def incompleta(self) -> bool:
        return (self.x1, self.y1) == (self.x2, self.y2)
    
class Oval(Figura):
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
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2, outline = self.cor_borda, fill=self.cor_preenchimento)

    def desenhar_preview(self, canvas: tk.Canvas) -> None:
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2, outline = self.cor_borda, fill=self.cor_preenchimento, dash=(4, 2))

    def incompleta(self) -> bool:
        return (self.x1, self.y1) == (self.x2, self.y2)


# =============================================================================
# Funções de callback e estado global
# =============================================================================

figuras: list[Figura] = []   # Todas as figuras finalizadas
figura_nova: Figura | None = None  # Figura sendo desenhada no momento

cor_borda_atual = "black"
cor_preenchimento_atual = ""


def iniciar_figura_nova(event):
    global figura_nova
    tipo = tipo_figura_var.get()
    if tipo == "Linha":
        figura_nova = Linha(event.x, event.y, cor_borda_atual, cor_preenchimento_atual)
    elif tipo == "Retângulo":
        figura_nova = Retangulo(event.x, event.y, cor_borda_atual, cor_preenchimento_atual)
    elif tipo == "Oval":
        figura_nova = Oval(event.x, event.y, cor_borda_atual, cor_preenchimento_atual)
    # falta adicionar rabisco


def atualizar_figura_nova(event):
    if figura_nova is None:
        return
    figura_nova.atualizar(event.x, event.y)
    desenhar()
    figura_nova.desenhar_preview(canvas)


def incluir_figura_nova(event):
    if figura_nova is not None and not figura_nova.incompleta():
        figuras.append(figura_nova)
    desenhar()


def desenhar():
    canvas.delete("all")
    for fig in figuras:
        fig.desenhar(canvas)


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
    frame = tk.Frame(root)
    paddings = {"padx": 5, "pady": 5}

    ttk.Label(frame, text="Ferramenta:").grid(column=0, row=0, sticky=tk.W, **paddings)

    tipo_figura_var = tk.StringVar(root)
    ttk.OptionMenu(frame, tipo_figura_var,
                   "Linha", "Linha", "Retângulo", "Oval"
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

    canvas = tk.Canvas(frame, bg="white", width=600, height=600)
    canvas.grid(column=0, row=2, columnspan=5, sticky=tk.W, **paddings)

    frame.pack()

    canvas.bind("<ButtonPress-1>", iniciar_figura_nova)
    canvas.bind("<B1-Motion>", atualizar_figura_nova)
    canvas.bind("<ButtonRelease-1>", incluir_figura_nova)

    root.mainloop()


if __name__ == "__main__":
    main()



