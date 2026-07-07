import sys
import os



from Modelo.Desenhos       import Desenho
from Visão.janela_principal         import JanelaPrincipal
from Controlador.controlador import Controladorr

# Garante que 'src/projeto_desenho' esteja no path ao rodar diretamente
sys.path.insert(0, os.path.dirname(__file__))

def main():
    modelo = Desenho()
    visao  = JanelaPrincipal()
    controlador = Controladorr(modelo, visao)
    visao.configurar_eventos(controlador)
    visao.root.mainloop()


if __name__ == "_main_":
    main()
