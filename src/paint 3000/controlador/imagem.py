import json
from tkinter import filedialog, messagebox

class Image:
    def __init__(self, app_ui):
        self.app_ui = app_ui
        self.figuras = []

    def salvar_projeto_json(self):
        caminho_arquivo = filedialog.asksaveasfilename(defaultextension=".json", 
                                                       filetypes=[("Arquivos JSON", "*.json"), ("Todos os arquivos", "*.*")])
        if not caminho_arquivo:
            return # Usuário cancelou
        try:
            lista_figura_dict = [figura.to_dict() for figura in self.figuras]
            dados_do_projeto = {
                "formato": "MeuPaintVetorial",
                "versao" : "1.4",
                "canvas_gb": self.app_ui.canvas.cget("background"),
                "figuras": lista_figura_dict
            }

            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                json.dump(dados_do_projeto, f, indent=4)

            messagebox.showinfo("Salvar", "Projeto Salvo")
        except Exception as e:
            messagebox.showerror("Erro", f"Não salvo: {str(e)}")
    
    def abrir_projeto_json(self, factory_figuras):
        caminho_arquivo = filedialog.askopenfilename(filetypes=[("Arquivos JSON", "*.json"), ("Todos os arquivos", "*.*")])
        if not caminho_arquivo:
            return #usuario cancelou
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                dados_do_projeto = json.load(f)
            
            if dados_do_projeto.get("formato") != "MeuPaintVetorial":
                raise ValueError("Formato de arquivo incompatível")
            
            self.figuras.clear()
            cor_fundo = dados_do_projeto.get("canvas_gb", "white")
            self.app_ui.canvas.config(bg=cor_fundo)
            
            for figura_dict in dados_do_projeto.get("figuras", []):
                nova_figura = factory_figuras(figura_dict)
                self.figuras.append(nova_figura)
                
            messagebox.showinfo("Abrir", "Projeto carregado com sucesso")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar: {str(e)}")