from tkinter import colorchooser
import estado

def escolher_cor_borda():
    cor = colorchooser.askcolor(color=estado.cor_borda_atual, title="Cor da borda")[1]
    if cor:
        estado.cor_borda_atual = cor
        estado.amostra_borda.config(bg=estado.cor_borda_atual)

def escolher_cor_preenchimento():
    cor = colorchooser.askcolor(color=estado.cor_preenchimento_atual or "white",
                                 title="Cor de preenchimento")[1]
    if cor:
        estado.cor_preenchimento_atual = cor
        estado.amostra_preenchimento.config(bg=estado.cor_preenchimento_atual)

def remover_preenchimento():
    estado.cor_preenchimento_atual = ""
    estado.amostra_preenchimento.config(bg="white")
