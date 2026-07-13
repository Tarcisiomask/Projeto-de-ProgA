import tkinter as tk
from tkinter import ttk


class JanelaPrincipal:
    """
    Responsável exclusivamente por construir e exibir a interface gráfica.

    Não toma nenhuma decisão de negócio: delega tudo ao Controlador.
    Expõe ao Controlador apenas o necessário:
      - canvas          → para as figuras se desenharem
      - cor_borda_atual / cor_preenchimento_atual → lidas na criação de figuras
      - tipo_figura_selecionado()  → qual ferramenta está ativa
      - definir_cor_borda/preenchimento() → atualiza cor e a amostra visual
      - limpar_canvas() → apaga o canvas (chamado pelo Controlador antes de redesenhar)
    """

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ferramenta de Desenho")
        self.root.geometry("750x750")

        self.cor_borda_atual        = "black"
        self.cor_preenchimento_atual = ""

        self._construir_widgets()

    # ------------------------------------------------------------------
    # Construção dos widgets
    # ------------------------------------------------------------------

    def _construir_widgets(self) -> None:
        frame = tk.Frame(self.root)
        frame.pack(expand=True, anchor="center")
        pad = {"padx": 5, "pady": 5}

        # — Linha 0: seletor de ferramenta e cor de borda —
        ttk.Label(frame, text="Ferramenta:").grid(column=0, row=0, sticky=tk.W, **pad)

        self._tipo_figura_var = tk.StringVar(self.root)
        ttk.OptionMenu(
            frame, self._tipo_figura_var,
            "Linha",
            "Linha", "Mão livre", "Oval", "Círculo", "Polígono",
        ).grid(column=1, row=0, sticky=tk.W, **pad)

        ttk.Label(frame, text="Cor da borda:").grid(column=2, row=0, sticky=tk.W, **pad)
        self._amostra_borda = tk.Label(frame, bg=self.cor_borda_atual, width=3, relief=tk.SUNKEN)
        self._amostra_borda.grid(column=3, row=0, sticky=tk.W, **pad)
        self._btn_cor_borda = ttk.Button(frame, text="Escolher...")
        self._btn_cor_borda.grid(column=4, row=0, sticky=tk.W, **pad)

        # — Linha 1: cor de preenchimento —
        ttk.Label(frame, text="Preenchimento:").grid(column=0, row=1, sticky=tk.W, **pad)
        self._amostra_preenchimento = tk.Label(frame, bg="white", width=3, relief=tk.SUNKEN)
        self._amostra_preenchimento.grid(column=1, row=1, sticky=tk.W, **pad)
        self._btn_cor_preenchimento = ttk.Button(frame, text="Escolher...")
        self._btn_cor_preenchimento.grid(column=2, row=1, sticky=tk.W, **pad)
        self._btn_sem_preenchimento = ttk.Button(frame, text="Sem preenchimento")
        self._btn_sem_preenchimento.grid(column=3, row=1, columnspan=2, sticky=tk.W, **pad)

        # — Linha 2: botão limpar + dica —
        self._btn_limpar = ttk.Button(frame, text="Limpar")
        self._btn_limpar.grid(column=0, row=2, sticky=tk.W, **pad)
        ttk.Label(
            frame,
            text="Polígono livre: clique = vértice | Enter = fechar\n"
                 "Botão direito + arrasto = redimensionar última figura",
            foreground="gray",
        ).grid(column=1, row=2, columnspan=4, sticky=tk.W, **pad)

        # — Linha 3: canvas de desenho —
        self.canvas = tk.Canvas(
            frame, bg="white", width=600, height=600,
            relief=tk.RAISED, bd=2,
        )
        self.canvas.grid(column=0, row=3, columnspan=5, sticky=tk.W, **pad)

    # ------------------------------------------------------------------
    # Conexão com o Controlador
    # (chamado pelo main.py depois que o Controlador é criado)
    # ------------------------------------------------------------------

    def configurar_eventos(self, controlador) -> None:
        """Conecta todos os widgets e eventos ao Controlador."""
        
        # --- CORREÇÃO ADICIONADA AQUI ---
        # Avisa o controlador toda vez que o valor do menu (Linha, Oval, etc) mudar
        self._tipo_figura_var.trace_add("write", lambda *args: controlador.trocar_ferramenta(self.tipo_figura_selecionado()))

        # Botões da barra de ferramentas
        self._btn_cor_borda.config(command=controlador.escolher_cor_borda)
        self._btn_cor_preenchimento.config(command=controlador.escolher_cor_preenchimento)
        self._btn_sem_preenchimento.config(command=controlador.remover_preenchimento)
        self._btn_limpar.config(command=controlador.limpar_tela)

        # Eventos do canvas
        self.canvas.bind("<ButtonPress-1>", controlador.iniciar_figura_nova)
        self.canvas.bind("<B1-Motion>",     controlador.atualizar_figura_nova)
        self.canvas.bind("<ButtonRelease-1>", controlador.incluir_figura_nova)

        self.canvas.bind("<ButtonPress-3>", controlador.iniciar_redimensionamento_ultima)
        self.canvas.bind("<ButtonPress-2>", controlador.iniciar_redimensionamento_ultima)
        self.canvas.bind("<B3-Motion>",     controlador.redimensionar_ultima)
        self.canvas.bind("<B2-Motion>",     controlador.redimensionar_ultima)

        self.canvas.bind("<Motion>", controlador.mover_preview_poligono)
        self.root.bind("<Return>",   controlador.finalizar_poligono)

    # ------------------------------------------------------------------
    # Interface que o Controlador usa
    # ------------------------------------------------------------------

    def tipo_figura_selecionado(self) -> str:
        return self._tipo_figura_var.get()

    def limpar_canvas(self) -> None:
        self.canvas.delete("all")

    def definir_cor_borda(self, cor: str) -> None:
        self.cor_borda_atual = cor
        self._amostra_borda.config(bg=cor)

    def definir_cor_preenchimento(self, cor: str) -> None:
        self.cor_preenchimento_atual = cor
        self._amostra_preenchimento.config(bg=cor if cor else "white")