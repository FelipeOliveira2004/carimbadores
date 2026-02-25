# import pyxel

# class Enemy:
#     IMG = 0
#     WIDTH = 16
#     HEIGHT = 16

#     def __init__(self, world, x, y):

#         # Inimigo
#         self.enemy_x = x
#         self.enemy_y = y

#         self.width = 16
#         self.height = 16

#         self.frame_start = 0
#         self.frame = 0
#         self.facing = 1

#         self.world = world

#     def draw(self):
#         pyxel.blt(
#             self.enemy_x,
#             self.enemy_y,
#             self.IMG,
#             0, 16,
#             self.WIDTH * self.facing,
#             self.HEIGHT,
#             0
#         )


import pyxel

class Enemy:
    IMG = 0

    def __init__(self, world, x, y):
        self.world = world

        # Cores
        pyxel.colors[11] = 0xD78D36
        pyxel.colors[12] = 0x89501B

        # Posição
        self.x = x
        self.y = y

        # Hitbox
        self.width = 16
        self.height = 16

        # Movimento
        self.vx = 1
        self.vy = 0
        self.facing = 1

    # Tile de colisão
    def is_solid(self, x, y):
        tile_x = int(x // self.world.TILE_SIZE)
        tile_y = int(y // self.world.TILE_SIZE)

        if tile_x < 0 or tile_y < 0:
            return False
        if tile_y >= len(self.world.world_map):
            return False
        if tile_x >= len(self.world.world_map[0]):
            return False

        tile = self.world.world_map[tile_y][tile_x]
        return tile in (self.world.CHAO_1, self.world.CHAO_2, self.world.FAIXA)

    def update(self):

        # Gravidade
        self.vy += self.world.gravity
        if self.vy > 6:
            self.vy = 6

        # Movimento vertical
        step = 1 if self.vy > 0 else -1
        for _ in range(int(abs(self.vy))):

            self.y += step

            bottom = self.y + self.height - 1
            top = self.y
            left = self.x
            right = self.x + self.width - 1

            # Caindo
            if step > 0:
                if self.is_solid(left, bottom) or self.is_solid(right, bottom):
                    tile_y = bottom // self.world.TILE_SIZE
                    self.y = tile_y * self.world.TILE_SIZE - self.height
                    self.vy = 0
                    break
            else:
                if self.is_solid(left, top) or self.is_solid(right, top):
                    tile_y = top // self.world.TILE_SIZE
                    self.y = (tile_y + 1) * self.world.TILE_SIZE
                    self.vy = 0
                    break

        # Movimento horizontal
        self.x += self.vx * self.facing

        front = self.x + (self.width if self.facing > 0 else 0)

        if (
            self.is_solid(front, self.y) or
            self.is_solid(front, self.y + self.height - 1)
        ):
            self.facing *= -1

    def draw(self):
        pyxel.blt(
            self.x,
            self.y,
            self.IMG,
            0, 16,
            self.width * self.facing,
            self.height,
            0
        )

        # Debug Hitbox
        # pyxel.rectb(self.x, self.y, self.width, self.height, 8)