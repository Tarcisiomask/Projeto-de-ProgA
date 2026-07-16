import sys
import os
import unittest

# Adiciona a pasta paint 3000 no sistema de buscas do python, não importa onde rode o teste ele achará a pasta modelo sem erros
caminho_projeto = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/paint 3000'))
sys.path.insert(0, caminho_projeto)

from modelo.figuras import Circulo, Figura, Grupo, Linha, Poligono


class TestGeometriaFiguras(unittest.TestCase):

    def test_criacao_e_atualizacao_circulo(self):
        """Testa se o círculo nasce no ponto certo e se calcula o raio corretamente."""
        circulo = Circulo(cx=200, cy=200, cor_borda="black", cor_preenchimento="blue")
        
        self.assertEqual(circulo.cx, 200)
        self.assertEqual(circulo.cy, 200)
        self.assertEqual(circulo.raio, 0)
        self.assertTrue(circulo.incompleta())

        circulo.atualizar(200, 250)
        self.assertEqual(circulo.raio, 50)
        self.assertFalse(circulo.incompleta())

    def test_movimentacao_figuras(self):
        """Testa se mover desloca as figuras corretamente no plano cartesiano."""
        circulo = Circulo(cx=100, cy=100)
        circulo.mover(dx=15, dy=-30)
        self.assertEqual(circulo.cx, 115)
        self.assertEqual(circulo.cy, 70)

        linha = Linha(x1=10, y1=10)
        linha.atualizar(20, 20)
        linha.mover(dx=5, dy=5)
        self.assertEqual(linha.x1, 15)
        self.assertEqual(linha.y1, 15)
        self.assertEqual(linha.x2, 25)
        self.assertEqual(linha.y2, 25)

    def test_colisao_clique_circulo(self):
        """Testa se o clique do mouse colide o círculo."""
        circulo_preenchido = Circulo(cx=100, cy=100, cor_preenchimento="red")
        circulo_preenchido.raio = 50
        self.assertTrue(circulo_preenchido.contem_ponto(110, 110))
        self.assertFalse(circulo_preenchido.contem_ponto(300, 300))

        circulo_vazio = Circulo(cx=100, cy=100, cor_preenchimento="")
        circulo_vazio.raio = 50
        self.assertTrue(circulo_vazio.contem_ponto(100, 148))
        self.assertFalse(circulo_vazio.contem_ponto(100, 100))

    def test_colisao_poligono(self):
        """Testa a colisão do polígono (clique dentro do polígono preenchido)."""
        triangulo = Poligono(x=10, y=10, cor_preenchimento="yellow")
        triangulo.adicionar_ponto(50, 10)
        triangulo.adicionar_ponto(30, 50)
        self.assertTrue(triangulo.contem_ponto(30, 20))
        self.assertFalse(triangulo.contem_ponto(100, 100))

    def test_serializacao_desserializacao(self):
        """Teste da Entrega 4: round-trip de figura -> dicionário -> figura."""
        # Cria e atualiza a figura
        linha_original = Linha(10, 20, "red", "blue")
        linha_original.atualizar(30, 40)
        
        # 1. Figura -> Dicionário
        dicionario = linha_original.to_dict()
        self.assertEqual(dicionario["tipo"], "Linha")
        self.assertEqual(dicionario["x2"], 30)
        self.assertEqual(dicionario["cor_borda"], "red")
        
        # 2. Dicionário -> Figura
        linha_recuperada = Linha.from_dict(dicionario)
        
        self.assertIsInstance(linha_recuperada, Linha)
        self.assertEqual(linha_recuperada.x1, 10)
        self.assertEqual(linha_recuperada.y1, 20)
        self.assertEqual(linha_recuperada.x2, 30)
        self.assertEqual(linha_recuperada.y2, 40)
        self.assertEqual(linha_recuperada.cor_borda, "red")
        self.assertEqual(linha_recuperada.cor_preenchimento, "blue")

    def test_grupo_serializa_e_reconstrui_filhos(self):
        """Teste para o padrão Composite: um grupo deve serializar e reconstruir suas subfiguras."""
        linha = Linha(10, 20, "red", "")
        linha.atualizar(30, 40)
        circulo = Circulo(100, 100, "black", "blue")
        circulo.raio = 20

        grupo = Grupo([linha, circulo])
        dados = grupo.to_dict()

        self.assertEqual(dados["tipo"], "Grupo")
        self.assertEqual(len(dados["figuras"]), 2)

        grupo_recuperado = Figura.from_dict(dados)
        self.assertIsInstance(grupo_recuperado, Grupo)
        self.assertEqual(len(grupo_recuperado.figuras), 2)
        self.assertIsInstance(grupo_recuperado.figuras[0], Linha)
        self.assertIsInstance(grupo_recuperado.figuras[1], Circulo)

if __name__ == "__main__":
    unittest.main()
