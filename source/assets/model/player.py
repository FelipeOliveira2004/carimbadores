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
        self.jump_force = -9.9
        self.on_ground = False

        # Gravidade Velocidade
        self.vel_y = 0
        self.vel_x = 0

        # Referência ao mundo (instância passada de main)
        self.world = world
    
    def update(self):
        # -------- MOVIMENTO HORIZONTAL --------
        self.vel_x = 0
        self.moving = False
        
        if pyxel.btn(pyxel.KEY_D) and self.player_x <= ((self.world.chao_width + self.world.chao_x) - self.WIDTH):
            self.vel_x = 2
            self.facing = 1
            self.moving = True
        if pyxel.btn(pyxel.KEY_A) and self.player_x > 0:
            self.vel_x = -2
            self.facing = -1
            self.moving = True

        self.player_x += self.vel_x
        self.resolve_horizontal_collision()

        # -------- GRAVIDADE --------
        self.vel_y += self.world.gravity
        self.vel_y = min(self.vel_y, 8)  # limite de queda
        # self.player_y += self.vel_y
        self.on_ground = False

        self.resolve_vertical_collision()

        # -------- PULO --------
        if pyxel.btnp(pyxel.KEY_W) and self.on_ground:
            self.vel_y = self.jump_force

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

    def is_solid(self, tile):
        return tile in (self.world.CHAO_1, self.world.CHAO_2, self.world.FAIXA)
    
    def is_solid_at_pixel(self, x, y):
        tile_x = int(x // self.world.TILE_SIZE)
        tile_y = int(y // self.world.TILE_SIZE)

        if tile_x < 0 or tile_x >= len(self.world.world_map[0]):
            return False
        if tile_y < 0 or tile_y >= len(self.world.world_map):
            return False

        return self.is_solid(self.world.world_map[tile_y][tile_x])
    
    def resolve_horizontal_collision(self):
        if self.vel_x > 0:  # Indo para direita
            right = self.player_x + self.WIDTH
            top = self.player_y
            bottom = self.player_y + self.HEIGHT - 1

            if (self.is_solid_at_pixel(right, top) or self.is_solid_at_pixel(right, bottom)):
                tile_x = right // self.world.TILE_SIZE
                self.player_x = tile_x * self.world.TILE_SIZE - self.WIDTH


        elif self.vel_x < 0:  # Indo para esquerda
            left = self.player_x
            top = self.player_y
            bottom = self.player_y + self.HEIGHT - 1

            if (self.is_solid_at_pixel(left, top) or self.is_solid_at_pixel(left, bottom)):
                tile_x = left // self.world.TILE_SIZE
                self.player_x = (tile_x + 1) * self.world.TILE_SIZE

    # def resolve_vertical_collision(self):
    #     if self.vel_y > 0:  # Caindo
    #         bottom = self.player_y + self.HEIGHT - 1
    #         left = self.player_x
    #         right = self.player_x + self.WIDTH - 1

    #         if (self.is_solid_at_pixel(left, bottom) or self.is_solid_at_pixel(right, bottom)):
    #             tile_y = bottom // self.world.TILE_SIZE
    #             self.player_y = tile_y * self.world.TILE_SIZE - self.HEIGHT
    #             self.vel_y = 0
    #             self.on_ground = True


    #     elif self.vel_y < 0:  # Subindo (batendo cabeça)
    #         top = self.player_y
    #         left = self.player_x
    #         right = self.player_x + self.WIDTH - 1

    #         if (self.is_solid_at_pixel(left, top) or self.is_solid_at_pixel(right, top)):
    #             tile_y = top // self.world.TILE_SIZE
    #             self.player_y = (tile_y + 1) * self.world.TILE_SIZE
    #             self.vel_y = 0

    def resolve_vertical_collision(self):

        step = 1 if self.vel_y > 0 else -1

        for _ in range(int(abs(self.vel_y))):

            self.player_y += step

            bottom = self.player_y + self.HEIGHT - 1
            top = self.player_y
            left = self.player_x
            right = self.player_x + self.WIDTH - 1

            # Player caindo
            if step > 0:
                if (
                    self.is_solid_at_pixel(left, bottom) or
                    self.is_solid_at_pixel(right, bottom)
                ):
                    tile_y = bottom // self.world.TILE_SIZE
                    self.player_y = tile_y * self.world.TILE_SIZE - self.HEIGHT
                    self.vel_y = 0
                    self.on_ground = True
                    return

            # Player subindo
            else:
                if (
                    self.is_solid_at_pixel(left, top) or
                    self.is_solid_at_pixel(right, top)
                ):
                    tile_y = top // self.world.TILE_SIZE
                    self.player_y = (tile_y + 1) * self.world.TILE_SIZE
                    self.vel_y = 0
                    return
