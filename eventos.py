import tkinter as tk
import estado
from figuras import Linha, MaoLivre, Oval, Circulo, Poligono

_FABRICA = {
    "Linha":     Linha,
    "Mão livre": MaoLivre,
    "Oval":      Oval,
    "Círculo":   Circulo,
}

def desenhar():
    estado.canvas.delete("all")
    for fig in estado.figuras:
        fig.desenhar(estado.canvas)

def limpar_tela():
    estado.figuras.clear()
    estado.figura_nova = None
    desenhar()

def iniciar_figura_nova(event):
    tipo = estado.tipo_figura_var.get()

    if tipo == "Polígono":
        if estado.figura_nova is None:
            estado.figura_nova = Poligono(event.x, event.y, estado.cor_borda_atual, estado.cor_preenchimento_atual)
        else:
            estado.figura_nova.adicionar_ponto(event.x, event.y)
        desenhar()
        estado.figura_nova.desenhar_preview(estado.canvas)
        return

    classe = _FABRICA.get(tipo)
    if classe:
        estado.figura_nova = classe(event.x, event.y, estado.cor_borda_atual, estado.cor_preenchimento_atual)

    ''' Não guardei a classe polígonos na fábrica, porque ele tem uma lógica específica, como todas as outras figuras seguem uma lógica semelhante fica mais fácil chamar a fábrica para elas'''

def atualizar_figura_nova(event):
    if estado.figura_nova is None:
        return
    estado.figura_nova.atualizar(event.x, event.y)
    desenhar()
    estado.figura_nova.desenhar_preview(estado.canvas)

def incluir_figura_nova(event):
    if isinstance(estado.figura_nova, Poligono):
        return
    if estado.figura_nova is not None and not estado.figura_nova.incompleta():
        estado.figuras.append(estado.figura_nova)
    estado.figura_nova = None
    desenhar()

def finalizar_poligono(event):
    """Enter: fecha o polígono livre em construção se tiver vértices suficientes."""
    if isinstance(estado.figura_nova, Poligono):
        if not estado.figura_nova.incompleta():
            estado.figuras.append(estado.figura_nova)
        estado.figura_nova = None
        desenhar()

def iniciar_redimensionamento_ultima(event):
    """Captura a proporção exata da última figura salva antes de esticá-la."""
    if not estado.figuras:
        return
    estado.figuras[-1].iniciar_redimensionamento(event.x, event.y)

def redimensionar_ultima(event):
    """Arrasto com botão direito: redimensiona a última figura salva."""
    if not estado.figuras:
        return
    estado.figuras[-1].redimensionar(event.x, event.y)
    desenhar()
    if estado.figura_nova is not None:
        estado.figura_nova.desenhar_preview(estado.canvas)

def mover_preview_poligono(event):
    """Movimento livre do mouse: atualiza a prévia do próximo lado do polígono livre."""
    if isinstance(estado.figura_nova, Poligono):
        estado.figura_nova.atualizar(event.x, event.y)
        desenhar()
        estado.figura_nova.desenhar_preview(estado.canvas)
