import pygame, sys
from random import randint
import spritesheet

class Player(pygame.sprite.Sprite):
    def __init__(self, sheet):
        super().__init__()

        # Animation Setup
        self.anim_list = []
        self.anim_steps = [2,2,2,2,4,4,4,4]
        self.action = 0
        self.frame = 0
        self.walk_cd = 100
        self.sword_cd = 150
        self.last_update = pygame.time.get_ticks()
        self.can_move = True
        self.is_swording = False
        self.spawned_sword = False
        self.last_action = 'walk'
        LINK_BG_COLOUR = (116, 116, 116)

        step_counter = 0
        for anim in self.anim_steps:
            temp_img_list = []
            for _ in range(anim):
                temp_img_list.append(sheet.get_image(step_counter, 16, 16, 3, LINK_BG_COLOUR))
                step_counter += 1
            self.anim_list.append(temp_img_list)

        # Movement
        self.speed = 5
        self.direction = 0 # 0 down, 1 right, 2 up, 3 left

        # Setting up Image and Rect
        self.image = self.anim_list[self.action][self.frame]
        self.rect = self.image.get_rect(center = (100, randint(10, 200)))
        
    def updateImage(self):
        if self.last_action == 'walk':
            cd = self.walk_cd
        elif self.last_action == 'sword':
            cd = self.sword_cd
        if self.last_action != 'idle':
            curr_time = pygame.time.get_ticks()
            if curr_time - self.last_update >= cd:
                self.frame += 1
                self.last_update = curr_time
            if self.frame >= len(self.anim_list[self.action]):
                self.frame = 0
                if self.last_action == 'sword':
                    if self.direction == 0:
                        self.action = 0
                    if self.direction == 1:
                        self.action = 1
                    if self.direction == 2:
                        self.action = 2
                    if self.direction == 3:
                        self.action = 3
                    self.can_move = True
        self.image = self.anim_list[self.action][self.frame]

    def move(self):
        keys = pygame.key.get_pressed()

        if self.can_move == True:
            if keys[pygame.K_DOWN]:
                self.action = 0
                self.direction = 0
                self.last_action = 'walk'
                self.rect.y += self.speed
            elif keys[pygame.K_UP]:
                self.action = 2
                self.direction = 2
                self.last_action = 'walk'
                self.rect.y -= self.speed
            else:
                self.last_action = 'idle'

            if keys[pygame.K_RIGHT]:
                self.action = 1
                self.direction = 1
                self.last_action = 'walk'
                self.rect.x += self.speed
            elif keys[pygame.K_LEFT]:
                self.action = 3
                self.direction = 3
                self.last_action = 'walk'
                self.rect.x -= self.speed

            if self.is_swording == False:
                if keys[pygame.K_x] or keys[pygame.K_z]:
                    self.can_move = False
                    self.is_swording = True
                    self.last_action = 'sword'
                    if self.direction == 0:
                        self.action = 4
                    if self.direction == 1:
                        self.action = 5
                    if self.direction == 2:
                        self.action = 6
                    if self.direction == 3:
                        self.action = 7
                    self.frame = 0

        if self.is_swording == True and keys[pygame.K_x] == False and keys[pygame.K_z] == False:
            self.is_swording = False

        if (self.last_action == 'walk' and self.can_move) or self.last_action == 'sword':
            self.updateImage()

        if self.last_action == 'sword' and self.spawned_sword == False:
            self.spawnSword()

    def spawnSword(self):
        if self.direction == 0:
            pos = (self.rect.x, self.rect.y + self.rect.height)
        if self.direction == 1:
            pos = (self.rect.x + self.rect.width, self.rect.y)
        if self.direction == 2:
            pos = (self.rect.x, self.rect.y - self.rect.height)
        if self.direction == 3:
            pos = (self.rect.x - self.rect.width, self.rect.y)
        sword_image = pygame.image.load('graphics/sword sheet.png').convert()
        sword_sheet = spritesheet.SpriteSheet(sword_image)
        sword = Sword(sword_sheet, pos, self.direction)
        self.groups()[0].add(sword)
        self.spawned_sword = True

    def update(self):
        self.move()

class Sword(pygame.sprite.Sprite):
    def __init__(self, sheet, pos, action):
        super().__init__()

        # Animation Setup
        self.anim_list = []
        self.anim_steps = [4,4,4,4]
        self.action = action
        self.frame = 0
        self.cd = 150
        self.last_update = pygame.time.get_ticks()
        LINK_BG_COLOUR = (116, 116, 116)

        step_counter = 0
        for anim in self.anim_steps:
            temp_img_list = []
            for _ in range(anim):
                temp_img_list.append(sheet.get_image(step_counter, 16, 16, 3, LINK_BG_COLOUR))
                step_counter += 1
            self.anim_list.append(temp_img_list)

        # Movement
        self.direction = 0 # 0 down, 1 right, 2 up, 3 left

        # Setting up Image and Rect
        self.image = self.anim_list[self.action][self.frame]
        self.rect = self.image.get_rect(topleft = pos)

    def updateImage(self):
        curr_time = pygame.time.get_ticks()
        if curr_time - self.last_update >= self.cd:
            self.frame += 1
            self.last_update = curr_time
        if self.frame < len(self.anim_list[self.action]):
            self.image = self.anim_list[self.action][self.frame]
        else:
            self.groups()[0].sprites()[0].spawned_sword = False
            self.kill()

    def update(self):
        self.updateImage()


clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((400, 400))

link_image = pygame.image.load('graphics/link sheet.png').convert()
link_sheet = spritesheet.SpriteSheet(link_image)

player = pygame.sprite.Group(Player(link_sheet))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update Background
    screen.fill('Black')

    # Handle Player Movement
    player.update()
    player.draw(screen)


    pygame.display.update()
    clock.tick(60)
            
    
