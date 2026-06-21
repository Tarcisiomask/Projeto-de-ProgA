import tkinter as tk
from tkinter import ttk

# Quando mouse é pressionado
def iniciar_figura_nova(event):
    global figura_nova
    tipo = tipo_figura_var.get()
    
    if tipo == 'Linha':
        figura_nova = ("linha", (event.x, event.y, event.x, event.y))
    elif tipo == 'Retângulo':
        figura_nova = ("retangulo", (event.x, event.y, event.x, event.y))
    else:  # Rabisco
        figura_nova = ("rabisco", [(event.x, event.y)])

# Quando mouse é movido com o botão pressionado
def atualizar_figura_nova(event):
    global figura_nova
    fig, values = figura_nova
    
    if fig == "rabisco":
        values.append((event.x, event.y))
    else:  # fig == "linha" ou fig == "retangulo"
        figura_nova = (fig, (values[0], values[1], event.x, event.y))
        
    desenhar()
    desenhar_figura_nova()

# Quando mouse é solto
def incluir_figura_nova(event):
    if not incompleta(figura_nova):  # Evita incluir figuras sem dimensão (cliques acidentais)
        figuras.append(figura_nova)
    desenhar()

# Redesenha todas as figuras salvas
def desenhar():
    canvas.delete("all")
    for fig, values in figuras:
        if fig == "linha":
            canvas.create_line(values[0], values[1], values[2], values[3])
        elif fig == "retangulo":
            canvas.create_rectangle(values[0], values[1], values[2], values[3])
        else:  # fig == "rabisco"
            canvas.create_line(values)

# Desenha a figura atual (tracejada) enquanto o mouse é arrastado
def desenhar_figura_nova():
    if figura_nova is None:
        return
        
    fig, values = figura_nova
    if fig == "linha":
        canvas.create_line(values[0], values[1], values[2], values[3], dash=(4, 2))
    elif fig == "retangulo":
        canvas.create_rectangle(values[0], values[1], values[2], values[3], dash=(4, 2))
    else:  # fig == "rabisco"
        canvas.create_line(values, dash=(4, 2))

# Verifica se a figura é apenas um ponto (clique sem arrastar)
def incompleta(figura):
    if figura is None:
        return True
        
    fig, values = figura
    if fig == "rabisco":
        return len(values) <= 1
    else:  # fig == "linha" ou fig == "retangulo"
        return (values[0], values[1]) == (values[2], values[3])


# Variáveis Globais de Estado
figuras = []       # Todas as figuras desenhadas e finalizadas
figura_nova = None # Figura que está sendo desenhada no momento


def main():
    global canvas, tipo_figura_var

    root = tk.Tk()
    root.title("Ferramenta de Desenho")
    frame = tk.Frame(root)

    # Configuração de padding para o grid
    paddings = {'padx': 5, 'pady': 5}

    # Label do menu
    label = ttk.Label(frame, text='Ferramenta:')
    label.grid(column=0, row=0, sticky=tk.W, **paddings)

    # Menu de opções (Dropdown)
    tipo_figura_var = tk.StringVar(root)
    option_menu = ttk.OptionMenu(frame, tipo_figura_var,
                                 'Linha', 'Linha', 'Rabisco', 'Retângulo')
    option_menu.grid(column=1, row=0, sticky=tk.W, **paddings)

    # Área de desenho (Canvas)
    canvas = tk.Canvas(frame, bg='white', width=600, height=600)
    canvas.grid(column=0, row=1, columnspan=2, sticky=tk.W, **paddings)

    frame.pack()

    # Associação (bind) dos eventos do mouse com as funções criadas
    canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
    canvas.bind('<B1-Motion>', atualizar_figura_nova)
    canvas.bind('<ButtonRelease-1>', incluir_figura_nova)

    root.mainloop()


if __name__ == "__main__":
    main()