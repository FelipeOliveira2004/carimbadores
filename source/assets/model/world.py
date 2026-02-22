import pyxel

class World:
    TILE_SIZE = 8

    HEIGHT = TILE_SIZE * 4
    WIDTH = TILE_SIZE * 8

    # X and Y
    VAZIO = (0, 0)
    CHAO_1 = (1, 0)
    CHAO_2 = (1, 1)
    FAIXA = (0, 1)

    def __init__(self):
        # Gravidade
        self.gravity = 1.25

        # Chão
        self.chao_x = 0
        self.chao_y = 200 - (3 * self.TILE_SIZE)
        self.chao_width = self.WIDTH * self.TILE_SIZE

        self.tilemap = pyxel.tilemaps[0]
        self.world_map = []
        
        for y in range(self.HEIGHT):
            self.world_map.append([])
            for x in range(self.WIDTH):
                if self.tilemap.pget(x, y) == self.CHAO_1:
                    self.world_map[y].append(self.CHAO_1)
                elif self.tilemap.pget(x, y) == self.CHAO_2:
                    self.world_map[y].append(self.CHAO_2)
                elif self.tilemap.pget(x, y) == self.FAIXA:
                    self.world_map[y].append(self.FAIXA)
                else:
                    self.world_map[y].append(self.VAZIO)
    
    def update(self):
        return
    
    def draw(self):
        # pyxel.bltm(
        #     self.chao_x,
        #     self.chao_y,
        #     0,
        #     0,
        #     13 * self.TILE_SIZE,
        #     self.chao_width,
        #     3 * self.TILE_SIZE
        # )

        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                world_item = self.world_map[y][x]
                
                pyxel.blt(
                    x * self.TILE_SIZE,
                    y * self.TILE_SIZE,
                    0,
                    world_item[0]  * self.TILE_SIZE,
                    world_item[1]  * self.TILE_SIZE,
                    self.TILE_SIZE,
                    self.TILE_SIZE
                )