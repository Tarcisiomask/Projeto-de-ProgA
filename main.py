import tkinter as tk
from tkinter import ttk, colorchooser

# Quando mouse é pressionado
def iniciar_figura_nova(event):
    global figura_nova
    tipo = tipo_figura_var.get()
    if tipo == 'Linha':
        figura_nova = ("linha", (event.x, event.y, event.x, event.y), cor_borda_atual, cor_preenchimento_atual)
    elif tipo == 'Retângulo':
        figura_nova = ("retangulo", (event.x, event.y, event.x, event.y), cor_borda_atual, cor_preenchimento_atual)
    elif tipo == 'Oval':
        figura_nova = ("oval", (event.x, event.y, event.x, event.y), cor_borda_atual, cor_preenchimento_atual)
    else:  # Rabisco
        figura_nova = ("rabisco", [(event.x, event.y)], cor_borda_atual, cor_preenchimento_atual)

# Quando mouse é movido com o botão pressionado
def atualizar_figura_nova(event):
    global figura_nova
    fig, values, cor_b, cor_p = figura_nova
    if fig == "rabisco":
        values.append((event.x, event.y))
    else:  # fig == "linha", "retangulo" ou "oval"
        figura_nova = (fig, (values[0], values[1], event.x, event.y), cor_b, cor_p)
    desenhar()
    desenhar_figura_nova()

# Quando mouse é solto
def incluir_figura_nova(event):
    if not incompleta(figura_nova):  # para evitar incluir figuras incompletas
        figuras.append(figura_nova)
    desenhar()

def desenhar():
    canvas.delete("all")
    for fig, values, cor_b, cor_p in figuras:
        if fig == "linha":
            canvas.create_line(values[0], values[1], values[2], values[3], fill=cor_b)
        elif fig == "retangulo":
            canvas.create_rectangle(values[0], values[1], values[2], values[3], outline=cor_b, fill=cor_p)
        elif fig == "oval":
            canvas.create_oval(values[0], values[1], values[2], values[3], outline=cor_b, fill=cor_p)
        else:  # fig == "rabisco" (não tem área interna, logo não recebe preenchimento)
            canvas.create_line(values, fill=cor_b)

def desenhar_figura_nova():
    fig, values, cor_b, cor_p = figura_nova
    if fig == "linha":
        canvas.create_line(values[0], values[1], values[2], values[3], fill=cor_b, dash=(4, 2))
    elif fig == "retangulo":
        canvas.create_rectangle(values[0], values[1], values[2], values[3], outline=cor_b, fill=cor_p, dash=(4, 2))
    elif fig == "oval":
        canvas.create_oval(values[0], values[1], values[2], values[3], outline=cor_b, fill=cor_p, dash=(4, 2))
    else:  # fig == "rabisco"
        canvas.create_line(values, fill=cor_b, dash=(4, 2))

def incompleta(figura):
    fig, values, cor_b, cor_p = figura
    if fig == "rabisco":
        return len(values) <= 1
    else:  # fig == "linha", "retangulo" ou "oval"
        return (values[0], values[1]) == (values[2], values[3])

# Abre o seletor de cores do sistema e guarda a cor escolhida para a borda
def escolher_cor_borda():
    global cor_borda_atual
    cor = colorchooser.askcolor(color=cor_borda_atual, title="Escolha a cor da borda")[1]
    if cor:  # None se o usuário cancelar
        cor_borda_atual = cor
        amostra_borda.config(bg=cor_borda_atual)

# Abre o seletor de cores do sistema e guarda a cor escolhida para o preenchimento
def escolher_cor_preenchimento():
    global cor_preenchimento_atual
    cor = colorchooser.askcolor(color=cor_preenchimento_atual or "white",
                                 title="Escolha a cor de preenchimento")[1]
    if cor:  # None se o usuário cancelar
        cor_preenchimento_atual = cor
        amostra_preenchimento.config(bg=cor_preenchimento_atual)

# "" instrui o Canvas a não preencher a figura (fica transparente)
def remover_preenchimento():
    global cor_preenchimento_atual
    cor_preenchimento_atual = ""
    amostra_preenchimento.config(bg="white")


figuras = []        # Todas as figuras desenhadas
figura_nova = None  # Figura que está sendo desenhada, mas ainda não foi incluída em figuras
cor_borda_atual = "black"        # Cor de borda usada nas próximas figuras
cor_preenchimento_atual = ""     # Cor de preenchimento usada nas próximas figuras ("" = sem preenchimento)


def main():
    global canvas, tipo_figura_var, amostra_borda, amostra_preenchimento

    root = tk.Tk()
    frame = tk.Frame(root)

    # Widgets arranjados com Layout grid dentro de frame
    paddings = {'padx': 5, 'pady': 5}

    # label
    label = ttk.Label(frame, text='Ferramenta:')
    label.grid(column=0, row=0, sticky=tk.W, **paddings)

    # option menu
    tipo_figura_var = tk.StringVar(root)  # Guarda o tipo de figura selecionado
    option_menu = ttk.OptionMenu(frame, tipo_figura_var,
                                 'Linha', 'Linha', 'Rabisco', 'Retângulo', 'Oval')
    option_menu.grid(column=1, row=0, sticky=tk.W, **paddings)

    # Seletor de cor de borda
    label_cor_borda = ttk.Label(frame, text='Cor da borda:')
    label_cor_borda.grid(column=2, row=0, sticky=tk.W, **paddings)

    amostra_borda = tk.Label(frame, bg=cor_borda_atual, width=3, relief=tk.SUNKEN)
    amostra_borda.grid(column=3, row=0, sticky=tk.W, **paddings)

    botao_cor_borda = ttk.Button(frame, text='Escolher...', command=escolher_cor_borda)
    botao_cor_borda.grid(column=4, row=0, sticky=tk.W, **paddings)

    # Seletor de cor de preenchimento
    label_cor_preenchimento = ttk.Label(frame, text='Preenchimento:')
    label_cor_preenchimento.grid(column=0, row=1, sticky=tk.W, **paddings)

    amostra_preenchimento = tk.Label(frame, bg="white", width=3, relief=tk.SUNKEN)
    amostra_preenchimento.grid(column=1, row=1, sticky=tk.W, **paddings)

    botao_cor_preenchimento = ttk.Button(frame, text='Escolher...', command=escolher_cor_preenchimento)
    botao_cor_preenchimento.grid(column=2, row=1, sticky=tk.W, **paddings)

    botao_sem_preenchimento = ttk.Button(frame, text='Sem preenchimento', command=remover_preenchimento)
    botao_sem_preenchimento.grid(column=3, row=1, columnspan=2, sticky=tk.W, **paddings)

    # Área de desenho
    canvas = tk.Canvas(frame, bg='white', width=600, height=600)
    canvas.grid(column=0, row=2, columnspan=5, sticky=tk.W, **paddings)

    frame.pack()

    # Eventos de mouse associados ao canvas - com seus callbacks
    canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
    canvas.bind('<B1-Motion>', atualizar_figura_nova)
    canvas.bind('<ButtonRelease-1>', incluir_figura_nova)

    root.mainloop()


if __name__ == "__main__":
    main()

