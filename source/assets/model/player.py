import pyxel

class Player:
    IMG = 0
    WIDTH = 16
    HEIGHT = 16

    def __init__(self, world):
        # Cores
        pyxel.colors[1] = 0x000000 # Olhos/boca
        pyxel.colors[13] = 0xd3731c # Tom pele
        pyxel.colors[14] = 0xebff00 # Amarelo
        pyxel.colors[15] = 0x0039FF # Azul

        # Frames de animação
        self.anim_timer = 0
        self.frame = 0
        self.frame_star = 16
        self.frame_count = 2   # último frame (0,1,2)
        self.anim_dir = 1   # 1 = indo pra frente | -1 = voltando

        # Personagem
        self.player_x = 10
        self.player_y = 100
        self.facing = 1
        self.moving = False

        # Pulo
        self.jump_force = -10
        self.on_ground = False

        # Gravidade Velocidade
        self.vel_y = 0

        # Referência ao mundo (instância passada de main)
        self.world = world
    
    def update(self):
        # Gravidade
        self.vel_y += self.world.gravity
        self.player_y += self.vel_y

        # Movimento
        self.moving = False

        # Colisão Chão
        ground = self.world.chao_y - self.HEIGHT  # Altura do personagem

        # esta_no_chao_L = (self.player_x + self.WIDTH) >= self.world.chao_x
        # esta_no_chao_R = self.player_x <= (self.world.chao_x + self.world.chao_width)
        if (self.player_x + self.WIDTH) >= self.world.chao_x and self.player_x <= (self.world.chao_x + self.world.chao_width):
            esta_no_chao = True
        else:
            esta_no_chao = False
            self.on_ground = False

        if self.player_y >= ground and esta_no_chao:
            self.player_y = ground
            self.vel_y = 0
            self.on_ground = True

        ## Personagem
        # Movimentação
        if pyxel.btn(pyxel.KEY_D) and self.player_x <= ((self.world.chao_width + self.world.chao_x) - self.WIDTH):
            self.player_x += 2
            self.facing = 1
            self.moving = True
        
        if pyxel.btn(pyxel.KEY_A) and self.player_x >= 0:
            self.player_x -= 2
            self.facing = -1
            self.moving = True
        
        if pyxel.btnp(pyxel.KEY_W) and self.on_ground:
            self.vel_y = self.jump_force
            self.on_ground = False

        # Animação
        if self.moving:
            self.anim_timer += 1

            if self.anim_timer >= 8:
                self.anim_timer = 0
                self.frame += self.anim_dir
                
                # Se chegou no fim, começa a voltar
                if self.frame >= self.frame_count:
                    self.frame = self.frame_count
                    self.anim_dir = -1

                # Se chegou no começo, começa a ir
                elif self.frame <= 0:
                    self.frame = 0
                    self.anim_dir = 1
        else:
            self.frame = 0
    
    def draw(self):
        # Centraliza a câmera no jogador
        cam_x = max(0, min((self.player_x + self.WIDTH // 2) - pyxel.width // 2, self.world.chao_width - pyxel.width))
        cam_y = max(0, min(self.player_y - pyxel.height // 2, 200 - pyxel.height))

        pyxel.camera(cam_x, cam_y)

        # Player
        pyxel.blt(
            self.player_x,
            self.player_y, 
            self.IMG, 
            self.frame_star + self.frame * 16,
            0, 
            self.WIDTH * self.facing, 
            self.HEIGHT, 
            0
        )
