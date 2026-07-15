import tkinter as tk
from abc import ABC, abstractmethod
import math

# Função auxiliar matemática para calcular distância de um ponto a um segmento de reta
def _dist_ponto_segmento(px: float, py: float, x1: float, y1: float, x2: float, y2: float) -> float:
    tamanho_quadrado = (x2 - x1)**2 + (y2 - y1)**2
    if tamanho_quadrado == 0:
        return math.hypot(px - x1, py - y1)
    
    # Projeção do ponto no segmento
    t = max(0, min(1, ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / tamanho_quadrado))
    proj_x = x1 + t * (x2 - x1)
    proj_y = y1 + t * (y2 - y1)
    
    return math.hypot(px - proj_x, py - proj_y)


# =============================================================================
# Hierarquia de classes
# =============================================================================

class Figura(ABC):
    """Classe base abstrata para todas as figuras."""

    def __init__(self, cor_borda: str = "black", cor_preenchimento: str = ""):
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento

    @abstractmethod
    def desenhar(self, canvas: tk.Canvas) -> None:
        """Desenha a figura definitivamente no canvas."""

    @abstractmethod
    def desenhar_preview(self, canvas: tk.Canvas) -> None:
        """Desenha a figura como prévia (tracejada) enquanto o usuário arrasta."""

    @abstractmethod
    def atualizar(self, x: int, y: int) -> None:
        """Atualiza a figura com a posição atual do mouse (usado durante criação)."""

    @abstractmethod
    def incompleta(self) -> bool:
        """Retorna True se a figura ainda não tem dimensão mínima para ser salva."""

    @abstractmethod
    def to_dict(self) -> dict:
        """Serializa a figura para um dicionário."""

    @staticmethod
    def from_dict(dados: dict) -> "Figura":
        tipo = dados.get("tipo")
        if tipo == "Linha":
            return Linha.from_dict(dados)
        if tipo == "Retangulo":
            return Retangulo.from_dict(dados)
        if tipo == "Oval":
            return Oval.from_dict(dados)
        if tipo == "Rabisco":
            return Rabisco.from_dict(dados)
        if tipo == "MaoLivre":
            return MaoLivre.from_dict(dados)
        if tipo == "Circulo":
            return Circulo.from_dict(dados)
        if tipo == "Poligono":
            return Poligono.from_dict(dados)
        raise ValueError(f"Tipo de figura desconhecido: {tipo}")

    # -------------------------------------------------------------------------
    # Redimensionamento
    # -------------------------------------------------------------------------
    def iniciar_redimensionamento(self, x: int, y: int) -> None:
        pass

    def redimensionar(self, x: int, y: int) -> None:
        self.atualizar(x, y)

    # -------------------------------------------------------------------------
    # Manipulação e Seleção
    # -------------------------------------------------------------------------
    @abstractmethod
    def contem_ponto(self, x: int, y: int) -> bool:
        """Retorna True se a coordenada (x, y) bater (colidir) com a figura."""

    @abstractmethod
    def mover(self, dx: int, dy: int) -> None:
        """Desloca toda a figura nos eixos x e y."""

    @abstractmethod
    def bbox(self) -> tuple[int, int, int, int]:
        """Retorna a caixa delimitadora da figura: (min_x, min_y, max_x, max_y)."""

    def desenhar_selecionado(self, canvas: tk.Canvas) -> None:
        """Desenha uma borda azul ao redor da bounding box da figura selecionada."""
        if self.incompleta():
            return
        x1, y1, x2, y2 = self.bbox()
        pad = 4  # Margem de respiro para a seleção
        canvas.create_rectangle(
            x1 - pad, y1 - pad, x2 + pad, y2 + pad,
            outline="blue", dash=(4, 4), width=1.5, tags="selecao"
        )


# -----------------------------------------------------------------------------
# Figuras
# -----------------------------------------------------------------------------

class Linha(Figura):
    def __init__(self, x1: int, y1: int, cor_borda: str = "black", cor_preenchimento: str = ""):
        super().__init__(cor_borda, cor_preenchimento)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x1
        self.y2 = y1

    def atualizar(self, x: int, y: int) -> None:
        self.x2 = x
        self.y2 = y

    def desenhar(self, canvas: tk.Canvas) -> None:
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.cor_borda)

    def desenhar_preview(self, canvas: tk.Canvas) -> None:
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.cor_borda, dash=(4, 2))

    def incompleta(self) -> bool:
        return (self.x1, self.y1) == (self.x2, self.y2)

    def mover(self, dx: int, dy: int) -> None:
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def bbox(self) -> tuple[int, int, int, int]:
        return min(self.x1, self.x2), min(self.y1, self.y2), max(self.x1, self.x2), max(self.y1, self.y2)

    def contem_ponto(self, x: int, y: int) -> bool:
        TOLERANCIA = 5.0
        return _dist_ponto_segmento(x, y, self.x1, self.y1, self.x2, self.y2) <= TOLERANCIA

    def to_dict(self) -> dict:
        return {
            "tipo": "Linha",
            "x1": self.x1,
            "y1": self.y1,
            "x2": self.x2,
            "y2": self.y2,
            "cor_borda": self.cor_borda,
            "cor_preenchimento": self.cor_preenchimento,
        }

    @classmethod
    def from_dict(cls, dados: dict):
        figura = cls(
            dados["x1"],
            dados["y1"],
            dados.get("cor_borda", "black"),
            dados.get("cor_preenchimento", ""),
        )
        figura.x2 = dados["x2"]
        figura.y2 = dados["y2"]
        return figura


class Retangulo(Figura):
    def __init__(self, x1: int, y1: int, cor_borda: str = "black", cor_preenchimento: str = ""):
        super().__init__(cor_borda, cor_preenchimento)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x1
        self.y2 = y1

    def atualizar(self, x: int, y: int) -> None:
        self.x2 = x
        self.y2 = y

    def desenhar(self, canvas: tk.Canvas) -> None:
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline=self.cor_borda, fill=self.cor_preenchimento)

    def desenhar_preview(self, canvas: tk.Canvas) -> None:
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline=self.cor_borda, fill=self.cor_preenchimento, dash=(4, 2))

    def incompleta(self) -> bool:
        return (self.x1, self.y1) == (self.x2, self.y2)

    def mover(self, dx: int, dy: int) -> None:
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def bbox(self) -> tuple[int, int, int, int]:
        return min(self.x1, self.x2), min(self.y1, self.y2), max(self.x1, self.x2), max(self.y1, self.y2)

    def contem_ponto(self, x: int, y: int) -> bool:
        return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2 or self.x2 <= x <= self.x1 and self.y2 <= y <= self.y1

    def to_dict(self) -> dict:
        return {
            "tipo": "Retangulo",
            "x1": self.x1,
            "y1": self.y1,
            "x2": self.x2,
            "y2": self.y2,
            "cor_borda": self.cor_borda,
            "cor_preenchimento": self.cor_preenchimento,
        }

    @classmethod
    def from_dict(cls, dados: dict):
        figura = cls(
            dados["x1"],
            dados["y1"],
            dados.get("cor_borda", "black"),
            dados.get("cor_preenchimento", ""),
        )
        figura.x2 = dados["x2"]
        figura.y2 = dados["y2"]
        return figura


class Rabisco(Figura):
    def __init__(self, x: int, y: int, cor_borda: str = "black", cor_preenchimento: str = ""):
        super().__init__(cor_borda, cor_preenchimento)
        self.pontos: list[tuple[int, int]] = [(x, y)]

    def atualizar(self, x: int, y: int) -> None:
        self.pontos.append((x, y))

    def iniciar_redimensionamento(self, x: int, y: int) -> None:
        self._pontos_base = list(self.pontos)
        self._min_x, self._min_y, self._max_x, self._max_y = self.bbox()

    def redimensionar(self, x: int, y: int) -> None:
        if not hasattr(self, '_pontos_base'):
            self.iniciar_redimensionamento(x, y)

        larg_base = self._max_x - self._min_x
        alt_base = self._max_y - self._min_y
        if larg_base == 0:
            larg_base = 1
        if alt_base == 0:
            alt_base = 1

        escala_x = (x - self._min_x) / larg_base
        escala_y = (y - self._min_y) / alt_base

        self.pontos = [
            (int(self._min_x + (p[0] - self._min_x) * escala_x),
             int(self._min_y + (p[1] - self._min_y) * escala_y))
            for p in self._pontos_base
        ]

    def desenhar(self, canvas: tk.Canvas) -> None:
        if not self.incompleta():
            canvas.create_line(self.pontos, fill=self.cor_borda)

    def desenhar_preview(self, canvas: tk.Canvas) -> None:
        if not self.incompleta():
            canvas.create_line(self.pontos, fill=self.cor_borda, dash=(4, 2))

    def incompleta(self) -> bool:
        return len(self.pontos) <= 1

    def mover(self, dx: int, dy: int) -> None:
        self.pontos = [(px + dx, py + dy) for px, py in self.pontos]

    def bbox(self) -> tuple[int, int, int, int]:
        xs = [p[0] for p in self.pontos]
        ys = [p[1] for p in self.pontos]
        return min(xs), min(ys), max(xs), max(ys)

    def contem_ponto(self, x: int, y: int) -> bool:
        TOLERANCIA = 5.0
        for i in range(len(self.pontos) - 1):
            p1, p2 = self.pontos[i], self.pontos[i + 1]
            if _dist_ponto_segmento(x, y, p1[0], p1[1], p2[0], p2[1]) <= TOLERANCIA:
                return True
        return False

    def to_dict(self) -> dict:
        return {
            "tipo": self.__class__.__name__,
            "pontos": [[px, py] for px, py in self.pontos],
            "cor_borda": self.cor_borda,
            "cor_preenchimento": self.cor_preenchimento,
        }

    @classmethod
    def from_dict(cls, dados: dict):
        pontos = dados.get("pontos", [])
        if pontos:
            figura = cls(
                pontos[0][0],
                pontos[0][1],
                dados.get("cor_borda", "black"),
                dados.get("cor_preenchimento", ""),
            )
            figura.pontos = [(p[0], p[1]) for p in pontos]
            return figura

        figura = cls(0, 0, dados.get("cor_borda", "black"), dados.get("cor_preenchimento", ""))
        figura.pontos = []
        return figura


class MaoLivre(Rabisco):
    pass


class Oval(Figura):
    def __init__(self, x1: int, y1: int, cor_borda: str = "black", cor_preenchimento: str = ""):
        super().__init__(cor_borda, cor_preenchimento)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x1
        self.y2 = y1

    def atualizar(self, x: int, y: int) -> None:
        self.x2 = x
        self.y2 = y

    def desenhar(self, canvas: tk.Canvas) -> None:
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2, outline=self.cor_borda, fill=self.cor_preenchimento)

    def desenhar_preview(self, canvas: tk.Canvas) -> None:
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2, outline=self.cor_borda, fill=self.cor_preenchimento, dash=(4, 2))

    def incompleta(self) -> bool:
        return (self.x1, self.y1) == (self.x2, self.y2)

    def mover(self, dx: int, dy: int) -> None:
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def bbox(self) -> tuple[int, int, int, int]:
        return min(self.x1, self.x2), min(self.y1, self.y2), max(self.x1, self.x2), max(self.y1, self.y2)

    def contem_ponto(self, x: int, y: int) -> bool:
        cx = (self.x1 + self.x2) / 2
        cy = (self.y1 + self.y2) / 2
        rx = abs(self.x1 - self.x2) / 2
        ry = abs(self.y1 - self.y2) / 2

        if rx == 0 or ry == 0:
            return False

        valor = ((x - cx)**2) / (rx**2) + ((y - cy)**2) / (ry**2)

        if self.cor_preenchimento:
            return valor <= 1.0
        else:
            return 0.8 <= valor <= 1.2

    def to_dict(self) -> dict:
        return {
            "tipo": "Oval",
            "x1": self.x1,
            "y1": self.y1,
            "x2": self.x2,
            "y2": self.y2,
            "cor_borda": self.cor_borda,
            "cor_preenchimento": self.cor_preenchimento,
        }

    @classmethod
    def from_dict(cls, dados: dict):
        figura = cls(
            dados["x1"],
            dados["y1"],
            dados.get("cor_borda", "black"),
            dados.get("cor_preenchimento", ""),
        )
        figura.x2 = dados["x2"]
        figura.y2 = dados["y2"]
        return figura


class Circulo(Figura):
    def __init__(self, cx: int, cy: int, cor_borda: str = "black", cor_preenchimento: str = ""):
        super().__init__(cor_borda, cor_preenchimento)
        self.cx = cx
        self.cy = cy
        self.raio = 0

    def atualizar(self, x: int, y: int) -> None:
        self.raio = int(math.hypot(x - self.cx, y - self.cy))

    def bbox(self) -> tuple[int, int, int, int]:
        r = self.raio
        return self.cx - r, self.cy - r, self.cx + r, self.cy + r

    def desenhar(self, canvas: tk.Canvas) -> None:
        canvas.create_oval(*self.bbox(), outline=self.cor_borda, fill=self.cor_preenchimento)

    def desenhar_preview(self, canvas: tk.Canvas) -> None:
        canvas.create_oval(*self.bbox(), outline=self.cor_borda, fill=self.cor_preenchimento, dash=(4, 2))

    def incompleta(self) -> bool:
        return self.raio == 0

    def mover(self, dx: int, dy: int) -> None:
        self.cx += dx
        self.cy += dy

    def contem_ponto(self, x: int, y: int) -> bool:
        distancia = math.hypot(x - self.cx, y - self.cy)
        if self.cor_preenchimento:
            return distancia <= self.raio
        else:
            return abs(distancia - self.raio) <= 5.0

    def to_dict(self) -> dict:
        return {
            "tipo": "Circulo",
            "cx": self.cx,
            "cy": self.cy,
            "raio": self.raio,
            "cor_borda": self.cor_borda,
            "cor_preenchimento": self.cor_preenchimento,
        }

    @classmethod
    def from_dict(cls, dados: dict):
        figura = cls(
            dados["cx"],
            dados["cy"],
            dados.get("cor_borda", "black"),
            dados.get("cor_preenchimento", ""),
        )
        figura.raio = dados["raio"]
        return figura


class Poligono(Figura):
    def __init__(self, x: int, y: int, cor_borda: str = "black", cor_preenchimento: str = ""):
        super().__init__(cor_borda, cor_preenchimento)
        self.pontos: list[tuple[int, int]] = [(x, y)]
        self.mouse_x = x
        self.mouse_y = y

    def adicionar_ponto(self, x: int, y: int) -> None:
        self.pontos.append((x, y))

    def atualizar(self, x: int, y: int) -> None:
        self.mouse_x = x
        self.mouse_y = y

    def iniciar_redimensionamento(self, x: int, y: int) -> None:
        self._pontos_base = list(self.pontos)
        self._min_x, self._min_y, self._max_x, self._max_y = self.bbox()

    def redimensionar(self, x: int, y: int) -> None:
        if not hasattr(self, '_pontos_base'):
            self.iniciar_redimensionamento(x, y)

        larg_base = self._max_x - self._min_x
        alt_base = self._max_y - self._min_y
        if larg_base == 0: larg_base = 1
        if alt_base == 0: alt_base = 1

        escala_x = (x - self._min_x) / larg_base
        escala_y = (y - self._min_y) / alt_base

        self.pontos = [
            (int(self._min_x + (p[0] - self._min_x) * escala_x),
             int(self._min_y + (p[1] - self._min_y) * escala_y))
            for p in self._pontos_base
        ]

    def desenhar(self, canvas: tk.Canvas) -> None:
        if not self.incompleta():
            coords = [c for p in self.pontos for c in p]
            canvas.create_polygon(coords, outline=self.cor_borda, fill=self.cor_preenchimento)

    def desenhar_preview(self, canvas: tk.Canvas) -> None:
        pontos_preview = self.pontos + [(self.mouse_x, self.mouse_y)]
        coords = [c for p in pontos_preview for c in p]
        if len(coords) >= 4:
            canvas.create_line(coords, fill=self.cor_borda, dash=(4, 2))

    def incompleta(self) -> bool:
        return len(self.pontos) < 3

    def mover(self, dx: int, dy: int) -> None:
        self.pontos = [(px + dx, py + dy) for px, py in self.pontos]

    def bbox(self) -> tuple[int, int, int, int]:
        xs = [p[0] for p in self.pontos]
        ys = [p[1] for p in self.pontos]
        return min(xs), min(ys), max(xs), max(ys)

    def contem_ponto(self, x: int, y: int) -> bool:
        if self.cor_preenchimento:
            n = len(self.pontos)
            dentro = False
            p1x, p1y = self.pontos[0]
            for i in range(n + 1):
                p2x, p2y = self.pontos[i % n]
                if y > min(p1y, p2y):
                    if y <= max(p1y, p2y):
                        if x <= max(p1x, p2x):
                            if p1y != p2y:
                                xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                            if p1x == p2x or x <= xinters:
                                dentro = not dentro
                p1x, p1y = p2x, p2y
            return dentro
        else:
            TOLERANCIA = 5.0
            n = len(self.pontos)
            for i in range(n):
                p1 = self.pontos[i]
                p2 = self.pontos[(i + 1) % n]
                if _dist_ponto_segmento(x, y, p1[0], p1[1], p2[0], p2[1]) <= TOLERANCIA:
                    return True
            return False

    def to_dict(self) -> dict:
        return {
            "tipo": "Poligono",
            "pontos": [[px, py] for px, py in self.pontos],
            "cor_borda": self.cor_borda,
            "cor_preenchimento": self.cor_preenchimento,
        }

    @classmethod
    def from_dict(cls, dados: dict):
        pontos = dados.get("pontos", [])
        if pontos:
            figura = cls(
                pontos[0][0],
                pontos[0][1],
                dados.get("cor_borda", "black"),
                dados.get("cor_preenchimento", ""),
            )
            figura.pontos = [(p[0], p[1]) for p in pontos]
            return figura
        
        figura = cls(0, 0, dados.get("cor_borda", "black"), dados.get("cor_preenchimento", ""))
        figura.pontos = []
        return figura
