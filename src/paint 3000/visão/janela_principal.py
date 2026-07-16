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
        self.root.geometry("800x800")

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
            "Selecionar", "Linha", "Mão livre", "Oval", "Círculo", "Polígono",
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

        # — Linha 2: botão limpar + botões salvar/abrir + Up/Down —
        self._btn_limpar = ttk.Button(frame, text="Limpar")
        self._btn_limpar.grid(column=0, row=2, sticky=tk.W, **pad)
        
        # Mini-container para colar o Salvar e o Abrir na Coluna 1
        frame_arquivos = tk.Frame(frame)
        frame_arquivos.grid(column=1, row=2, sticky=tk.W, pady=5)
        
        self._btn_salvar = ttk.Button(frame_arquivos, text="💾", width=3)
        self._btn_salvar.grid(column=0, row=0, padx=(5, 0))
        
        self._btn_abrir = ttk.Button(frame_arquivos, text="📂", width=3)
        self._btn_abrir.grid(column=1, row=0, padx=(0, 5))
        
        self._btn_subir_camada = ttk.Button(frame, text="▲", width=3)
        self._btn_subir_camada.grid(column=3, row=2, sticky=tk.W, **pad)

        self._btn_descer_camada = ttk.Button(frame, text="▼", width=3)
        self._btn_descer_camada.grid(column=4, row=2, sticky=tk.W, **pad)

        self._btn_agrupar = ttk.Button(frame, text="Agrupar")
        self._btn_agrupar.grid(column=5, row=2, sticky=tk.W, **pad)

        self._btn_desagrupar = ttk.Button(frame, text="Desagrupar")
        self._btn_desagrupar.grid(column=6, row=2, sticky=tk.W, **pad)

        # — Linha 3: canvas de desenho —
        self.canvas = tk.Canvas(
            frame, bg="white", width=600, height=600,
            relief=tk.RAISED, bd=2,
        )
        self.canvas.grid(column=0, row=3, columnspan=7, sticky=tk.W, **pad)

        # — Linha 4: Dicas —
        
        ttk.Label(
            frame,
            text="Polígono livre: Clique = Vértice, Enter = fechar | Botão direito + Arrasto = Redimensionar última figura\n"
                 "Seleção Múltipla: SHIFT | Mudar camada da figura: Setas UP e DOWN | Agrupar/Desagrupar: Ctrl+G / Ctrl+U\n",
            foreground="gray",
        ).grid(column=0, row=4, columnspan=7, sticky=tk.W, **pad)
        
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
