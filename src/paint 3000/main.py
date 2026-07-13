import sys
import os
from modelo.desenhos       import Desenho
from visão.janela_principal         import JanelaPrincipal
from controlador.controlador import Controlador

# Garante que 'src/projeto_desenho' esteja no path ao rodar diretamente
sys.path.insert(0, os.path.dirname(__file__))

def main():
    modelo = Desenho()
    visao  = JanelaPrincipal()
    controlador = Controlador(modelo, visao)
    visao.configurar_eventos(controlador)
    visao.root.mainloop()


if __name__ == "__main__":
    main()
