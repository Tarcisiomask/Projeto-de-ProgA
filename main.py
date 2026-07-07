import sys
import os

# Garante que 'src/projeto_desenho' esteja no path ao rodar diretamente
sys.path.insert(0, os.path.dirname(_file_))

from modelo.desenho       import Desenho
from visao.janela         import JanelaPrincipal
from controlador.controlador import Controlador


def main():
    modelo = Desenho()
    visao  = JanelaPrincipal()
    controlador = Controlador(modelo, visao)
    visao.configurar_eventos(controlador)
    visao.root.mainloop()


if _name_ == "_main_":
    main()
