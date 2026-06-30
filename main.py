import tkinter as tk
from tkinter import ttk
import estado
import eventos
import cores

def main():
    root = tk.Tk()
    root.title("Ferramenta de Desenho")
    root.geometry("750x750") 

    frame = tk.Frame(root)
    frame.pack(expand=True, anchor="center") 
    paddings = {"padx": 5, "pady": 5}

    ttk.Label(frame, text="Ferramenta:").grid(column=0, row=0, sticky=tk.W, **paddings)
    estado.tipo_figura_var = tk.StringVar(root)
    ttk.OptionMenu(
        frame, estado.tipo_figura_var,
        "Linha",        
        "Linha", "Mão livre",
        "Oval", "Círculo",
        "Polígono",
    ).grid(column=1, row=0, sticky=tk.W, **paddings)

    ttk.Label(frame, text="Cor da borda:").grid(column=2, row=0, sticky=tk.W, **paddings)
    estado.amostra_borda = tk.Label(frame, bg=estado.cor_borda_atual, width=3, relief=tk.SUNKEN)
    estado.amostra_borda.grid(column=3, row=0, sticky=tk.W, **paddings)
    ttk.Button(frame, text="Escolher...", command=cores.escolher_cor_borda).grid(
        column=4, row=0, sticky=tk.W, **paddings)

    ttk.Label(frame, text="Preenchimento:").grid(column=0, row=1, sticky=tk.W, **paddings)
    estado.amostra_preenchimento = tk.Label(frame, bg="white", width=3, relief=tk.SUNKEN)
    estado.amostra_preenchimento.grid(column=1, row=1, sticky=tk.W, **paddings)
    ttk.Button(frame, text="Escolher...", command=cores.escolher_cor_preenchimento).grid(
        column=2, row=1, sticky=tk.W, **paddings)
    ttk.Button(frame, text="Sem preenchimento", command=cores.remover_preenchimento).grid(
        column=3, row=1, columnspan=2, sticky=tk.W, **paddings)

    ttk.Button(frame, text="Limpar", command=eventos.limpar_tela).grid(
        column=0, row=2, sticky=tk.W, **paddings)
    ttk.Label(
        frame,
        text="Polígono livre: clique = vértice | Enter = fechar\n"
             "Botão direito + arrasto = redimensionar última figura",
        foreground="gray",
    ).grid(column=1, row=2, columnspan=4, sticky=tk.W, **paddings)

    estado.canvas = tk.Canvas(frame, bg="white", width=600, height=600, relief=tk.RAISED, bd=2)
    estado.canvas.grid(column=0, row=3, columnspan=5, sticky=tk.W, **paddings)

    # Associações de eventos do Canvas vinculadas ao módulo eventos
    estado.canvas.bind("<ButtonPress-1>", eventos.iniciar_figura_nova)
    estado.canvas.bind("<B1-Motion>", eventos.atualizar_figura_nova)
    estado.canvas.bind("<ButtonRelease-1>", eventos.incluir_figura_nova)
    
    # Eventos para capturar o exato momento que o redimensionamento começa
    estado.canvas.bind("<ButtonPress-3>", eventos.iniciar_redimensionamento_ultima)
    estado.canvas.bind("<ButtonPress-2>", eventos.iniciar_redimensionamento_ultima)
    
    # Eventos para o arrasto de redimensionamento
    estado.canvas.bind("<B3-Motion>", eventos.redimensionar_ultima)
    estado.canvas.bind("<B2-Motion>", eventos.redimensionar_ultima) 
    
    estado.canvas.bind("<Motion>", eventos.mover_preview_poligono)
    root.bind("<Return>", eventos.finalizar_poligono)

    root.mainloop()

if __name__ == "__main__":
    main()
