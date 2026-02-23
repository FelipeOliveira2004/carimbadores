import pyxel

from assets.model.world import *
from assets.model.enemy import *
from assets.model.player import *

class Jogo:
    def __init__(self):
        pyxel.init(240, 200, "Carimbadores")
        pyxel.load('assets/game.pyxres')

        self.world = World()
        self.enemy = Enemy()
        self.player = Player(self.world)

        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.update()

    def draw(self):
        pyxel.cls(0)

        self.world.draw()
        self.enemy.draw()
        self.player.draw()
        
Jogo()
