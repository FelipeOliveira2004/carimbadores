import pyxel

class World:
    TILE_SIZE = 8

    def __init__(self):
        # Gravidade
        self.gravity = 1.25

        # Chão
        self.chao_x = 0
        self.chao_y = 200 - (3 * self.TILE_SIZE)
        self.chao_width = 64 * self.TILE_SIZE
    
    def update(self):
        return
    
    def draw(self):
        pyxel.bltm(
            self.chao_x,
            self.chao_y,
            0,
            0,
            13 * self.TILE_SIZE,
            self.chao_width,
            3 * self.TILE_SIZE
        )