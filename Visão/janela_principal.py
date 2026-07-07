import tkinter as tk
from tkinter import ttk

class JanelaPrincipal:
    """
    Classe responsável APENAS pela interface gráfica (View no MVC).
    Não contém regras de negócio nem gere o estado dos dados.
    """
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Ferramenta de Desenho - Padrão MVC")
        
        # Frame principal para conter os elementos
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)
        
        self.paddings = {'padx': 5, 'pady': 5}
        
        # Inicializa todos os botões, menus e o canvas
        self._criar_interface()

    def _criar_interface(self):
        # Seletor de Ferramenta
        ttk.Label(self.frame, text='Ferramenta:').grid(column=0, row=0, sticky=tk.W, **self.paddings)
        self.tipo_figura_var = tk.StringVar(self.root)
        self.tipo_figura_var.set("Linha") # Valor por defeito
        
        self.option_menu = ttk.OptionMenu(self.frame, self.tipo_figura_var, "Linha", "Linha", "Rabisco", "Retângulo", "Oval")
        self.option_menu.grid(column=1, row=0, sticky=tk.W, **self.paddings)
        
        # Cor da Borda
        ttk.Label(self.frame, text="Cor da borda:").grid(column=2, row=0, sticky=tk.W, **self.paddings)
        self.amostra_borda = tk.Label(self.frame, bg="black", width=3, relief=tk.SUNKEN)
        self.amostra_borda.grid(column=3, row=0, sticky=tk.W, **self.paddings)
        
        self.botao_cor_borda = ttk.Button(self.frame, text="Escolher...")
        self.botao_cor_borda.grid(column=4, row=0, sticky=tk.W, **self.paddings)
        
        # Cor de Preenchimento
        ttk.Label(self.frame, text="Preenchimento:").grid(column=0, row=1, sticky=tk.W, **self.paddings)
        self.amostra_preenchimento = tk.Label(self.frame, bg="white", width=3, relief=tk.SUNKEN)
        self.amostra_preenchimento.grid(column=1, row=1, sticky=tk.W, **self.paddings)
        
        self.botao_cor_preenchimento = ttk.Button(self.frame, text="Escolher...")
        self.botao_cor_preenchimento.grid(column=2, row=1, sticky=tk.W, **self.paddings)
        
        self.botao_sem_preenchimento = ttk.Button(self.frame, text="Sem preench.")
        self.botao_sem_preenchimento.grid(column=3, row=1, columnspan=2, sticky=tk.W, **self.paddings)
        
        # Botão Limpar Tela
        self.botao_limpar = ttk.Button(self.frame, text="Limpar Tela")
        self.botao_limpar.grid(column=5, row=1, sticky=tk.W, **self.paddings)
        
        # Área de Desenho (Canvas)
        self.canvas = tk.Canvas(self.frame, bg='white', width=600, height=600)
        self.canvas.grid(column=0, row=2, columnspan=6, sticky=(tk.N, tk.W, tk.E, tk.S))

    def associar_controlador(self, controlador):
        """
        Delega as ações da interface para o Controlador. 
        A Visão não processa os cliques, apenas avisa quem sabe processar.
        """
        # Liga os cliques nos botões aos métodos do controlador
        self.botao_cor_borda.config(command=controlador.escolher_cor_borda)
        self.botao_cor_preenchimento.config(command=controlador.escolher_cor_preenchimento)
        self.botao_sem_preenchimento.config(command=controlador.remover_preenchimento)
        self.botao_limpar.config(command=controlador.limpar_tela)
        
        # Liga os eventos físicos do rato no Canvas ao controlador
        self.canvas.bind("<Button-1>", controlador.ao_clicar_rato)
        self.canvas.bind("<B1-Motion>", controlador.ao_arrastar_rato)
        self.canvas.bind("<ButtonRelease-1>", controlador.ao_soltar_rato)

    def obter_ferramenta_selecionada(self) -> str:
        """Devolve ao controlador qual a ferramenta (figura) escolhida na dropdown."""
        return self.tipo_figura_var.get()

    def atualizar_amostras_cores(self, cor_borda: str, cor_preenchimento: str):
        """Atualiza visualmente os quadrados de cores na interface."""
        self.amostra_borda.config(bg=cor_borda)
        # Se a cor de preenchimento for vazia (transparente), mostramos branco no seletor
        bg_preenchimento = cor_preenchimento if cor_preenchimento != "" else "white"
        self.amostra_preenchimento.config(bg=bg_preenchimento)

    def renderizar_figuras(self, lista_figuras, figura_em_andamento=None):
        """
        Limpa o Canvas e pede a cada objeto 'Figura' do Modelo que se desenhe.
        """
        self.canvas.delete("all")
        
        # Desenha as figuras que já estão guardadas no Modelo
        for figura in lista_figuras:
            figura.desenhar(self.canvas)
            
        # Se houver um desenho a ser arrastado neste instante, desenha-o de forma tracejada
        if figura_em_andamento:
            figura_em_andamento.desenhar_preview(self.canvas)