import sys
import os
import unittest

# Adiciona a pasta paint 3000 no sistema de buscas do python, não importa onde rode o teste ele achará a pasta modelo sem erros
caminho_projeto = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/paint 3000'))
sys.path.insert(0, caminho_projeto)

from modelo.figuras import Circulo, Linha, Poligono


class TestGeometriaFiguras(unittest.TestCase):

    def test_criacao_e_atualizacao_circulo(self):
        """Testa se o círculo nasce no ponto certo e se calcula o raio corretamente."""
        # Cria um círculo no centro (x=200, y=200) com borda preta e preenchimento azul
        circulo = Circulo(cx=200, cy=200, cor_borda="black", cor_preenchimento="blue")
        
        self.assertEqual(circulo.cx, 200)
        self.assertEqual(circulo.cy, 200)
        self.assertEqual(circulo.raio, 0)
        self.assertTrue(circulo.incompleta())

        # Ao atualizar simulando o arrasto do mouse para (200, 250), o raio deve vira 50
        circulo.atualizar(200, 250)
        self.assertEqual(circulo.raio, 50)
        self.assertFalse(circulo.incompleta())

    def test_movimentacao_figuras(self):
        """Testa se mover desloca as figuras corretamente no plano cartesiano."""
        # Testa o Círculo
        circulo = Circulo(cx=100, cy=100)
        # Move 15 pixels para o lado (x) e -30 pixels para cima (y)
        circulo.mover(dx=15, dy=-30)
        self.assertEqual(circulo.cx, 115)
        self.assertEqual(circulo.cy, 70)

        # Testa a Linha
        linha = Linha(x1=10, y1=10)
        linha.atualizar(20, 20)  # Linha de (10,10) até (20,20)
        linha.mover(dx=5, dy=5)  # Move 5 para cada lado
        self.assertEqual(linha.x1, 15)
        self.assertEqual(linha.y1, 15)
        self.assertEqual(linha.x2, 25)
        self.assertEqual(linha.y2, 25)

    def test_colisao_clique_circulo(self):
        """Testa se o clique do mouse colide o círculo."""
        # Círculo com preenchimento, qualquer clique dentro da área deve colidir
        circulo_preenchido = Circulo(cx=100, cy=100, cor_preenchimento="red")
        circulo_preenchido.raio = 50

        # Um clique no ponto (110, 110) está dentro do raio (colide)
        self.assertTrue(circulo_preenchido.contem_ponto(110, 110))
        # Um clique no ponto (300, 300) está muito longe (não colide)
        self.assertFalse(circulo_preenchido.contem_ponto(300, 300))

        # Círculo sem preenchimento, colisão deve funcionar apenas perto da borda
        circulo_vazio = Circulo(cx=100, cy=100, cor_preenchimento="")
        circulo_vazio.raio = 50

        # Perto da borda (raio = 50, distância de 48 pixels é perto o suficiente)
        self.assertTrue(circulo_vazio.contem_ponto(100, 148))
        # Bem no centro (distância é 0, mas como não tem preenchimento, não deve detectar)
        self.assertFalse(circulo_vazio.contem_ponto(100, 100))

    def test_colisao_poligono(self):
        """Testa a colisão do polígono (clique dentro do polígono preenchido)."""
        # Criando um triângulo equilátero/simples preenchido
        triangulo = Poligono(x=10, y=10, cor_preenchimento="yellow")
        triangulo.adicionar_ponto(50, 10)
        triangulo.adicionar_ponto(30, 50)

        # Um ponto bem no meio do triângulo deve retornar verdadeiro
        self.assertTrue(triangulo.contem_ponto(30, 20))
        # Um ponto fora deve retornar falso
        self.assertFalse(triangulo.contem_ponto(100, 100))


if __name__ == "__main__":
    unittest.main()
