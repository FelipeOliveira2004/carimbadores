# import pyxel

# from assets.model.world import *
# from assets.model.enemy import *
# from assets.model.player import *

# class Jogo:
#     def __init__(self):
#         pyxel.init(240, 200, "Carimbadores")
#         pyxel.load('assets/game.pyxres')

#         self.world = World()
#         self.player = Player(self.world)

#         self.enemies = []

#         for spawn in self.world.enemy_spawns:
#             self.enemies.append(Enemy(self.world, spawn[0], spawn[1]))
#             # self.enemies.append(enemy)

#         # self.enemies = [Enemy(self.world, 40, 40)]
#         # print("Spawns encontrados:", self.world.enemy_spawns)
#         pyxel.run(self.update, self.draw)

#     def update(self):
#         self.player.update()

#     def draw(self):
#         pyxel.cls(0)

#         self.world.draw()
#         self.player.draw()

#         for enemy in self.enemies:
#             enemy.draw()
        
# Jogo()

import pyxel
from assets.model.world import *
from assets.model.enemy import *
from assets.model.player import *

class Jogo:
    def __init__(self):
        pyxel.init(240, 200, "Carimbadores")
        pyxel.load('assets/game.pyxres')

        self.world = World()
        self.player = Player(self.world)

        # cria inimigos
        self.enemies = []
        for spawn in self.world.enemy_spawns:
            self.enemies.append(Enemy(self.world, spawn[0], spawn[1]))

        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.update()

        for enemy in self.enemies:
            enemy.update()

            # colisão player vs enemy
            if (
                self.player.player_x < enemy.x + enemy.width and
                self.player.player_x + self.player.WIDTH > enemy.x and
                self.player.player_y < enemy.y + enemy.height and
                self.player.player_y + self.player.HEIGHT > enemy.y
            ):
                print("COLIDIU COM INIMIGO")

    def draw(self):
        pyxel.cls(0)

        self.world.draw()
        self.player.draw()

        for enemy in self.enemies:
            enemy.draw()

Jogo()