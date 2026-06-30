# estado.py
# Centraliza o estado global da aplicação para evitar importações circulares.

figuras = []
figura_nova = None

cor_borda_atual = "black"
cor_preenchimento_atual = ""

# Referências para os componentes da interface gráfica (inicializados no main.py)
canvas = None
tipo_figura_var = None
amostra_borda = None
amostra_preenchimento = None