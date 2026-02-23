import pyxel

class Enemy:
    IMG = 0
    WIDTH = 16
    HEIGHT = 16

    def __init__(self):
        # Cores
        pyxel.colors[11] = 0xD78D36
        pyxel.colors[12] = 0x89501B

        # Inimigo
        self.enemy_x = 20
        self.enemy_y = 100
        self.frame_start = 0
        self.frame = 16
        self.facing = 1

    # def update(self):
    #     return
    
    def draw(self):
        pyxel.blt(
            self.enemy_x,
            self.enemy_y,
            self.IMG,
            self.frame_start + self.frame * 16,
            0,
            self.WIDTH * self.facing,
            self.HEIGHT,
            0
        )
