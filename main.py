import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

bg = pygame.image.load('bg.jpg')

current_level_no = 0
change_level = False

class Player(pygame.sprite.Sprite):
 right = True
 def __init__(self):
    super().__init__()
    self.image = pygame.image.load('idle.png')
    self.rect = self.image.get_rect()
    self.change_x = 0
    self.change_y = 0

 def update(self):
    global current_level_no, change_level
    self.calc_grav()
    self.rect.x += self.change_x
    block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
    for block in block_hit_list:
       if self.change_x > 0:
          self.rect.right = block.rect.left
       elif self.change_x < 0:
          self.rect.left = block.rect.right
    self.rect.y += self.change_y

    block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
    for block in block_hit_list:
       if self.change_y > 0:
          self.rect.bottom = block.rect.top
       elif self.change_y < 0:
          self.rect.top = block.rect.bottom
       self.change_y = 0

    #spikes_hit_list = pygame.sprite.spritecollide(self, self.level.spikes_list, False)
    #if spikes_hit_list != []:
        #main()

    portal_hit_list = pygame.sprite.spritecollide(self, self.level.portal_list, False)
    if portal_hit_list != []:
        current_level_no = 1
        change_level = True

    spikes_hit_list = pygame.sprite.spritecollide(self, self.level.spikes_list, False)
    for spike in spikes_hit_list:
        if self.rect.colliderect(spike.rect):
            spike.kill()

 def calc_grav(self):
    if self.change_y == 0:
       self.change_y = 1
    else:
       self.change_y += .95

    if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
       self.change_y = 0
       self.rect.y = SCREEN_HEIGHT - self.rect.height

 def jump(self):
    self.rect.y += 10
    platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
    self.rect.y -= 10

    if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
       self.change_y = -16

 def go_left(self):
    self.change_x = -9
    if(self.right):
       self.flip()
       self.right = False

 def go_right(self):
    self.change_x = 9
    if (not self.right):
       self.flip()
       self.right = True

 def stop(self):
    self.change_x = 0

 def flip(self):
    self.image = pygame.transform.flip(self.image, True, False)


class Platform(pygame.sprite.Sprite):
 def __init__(self, width, height):
    super().__init__()
    self.image = pygame.image.load('platform.png')
    self.rect = self.image.get_rect()

class Spike(pygame.sprite.Sprite):
 def __init__(self, width, height):
    super().__init__()
    self.image = pygame.image.load('spike.png')
    self.image = pygame.transform.scale(self.image, (width, height))
    self.rect = self.image.get_rect()

class Portal(pygame.sprite.Sprite):
 def __init__(self, width, height):
    super().__init__()
    self.image = pygame.image.load('portal.png')
    self.image = pygame.transform.scale(self.image, (width, height))
    self.rect = self.image.get_rect()

class Level(object):
 def __init__(self, player):
    self.platform_list = pygame.sprite.Group()
    self.spikes_list = pygame.sprite.Group()
    self.portal_list = pygame.sprite.Group()
    self.player = player
 def update(self):
    self.platform_list.update()
 def draw(self, screen):
    screen.blit(bg, (0, 0))
    self.platform_list.draw(screen)
    self.portal_list.draw(screen)
    self.spikes_list.draw(screen)

class Level_01(Level):
 def __init__(self, player):
    Level.__init__(self, player)
    level = [
       [210, 32, 500, 500],
       [210, 32, 200, 400],
       [210, 32, 600, 300],
    ]
    for platform in level:
       block = Platform(platform[0], platform[1])
       block.rect.x = platform[2]
       block.rect.y = platform[3]
       block.player = self.player
       self.platform_list.add(block)
    spikes = [
        [10, 20, 550, 485],
        [10, 20, 200, 400],
        [10, 20, 600, 300],
    ]
    for spike in spikes:
        block = Spike(spike[0], spike[1])
        block.rect.x = spike[2]
        block.rect.y = spike[3]
        block.player = self.player
        self.spikes_list.add(block)
    portals = [
        [100, 100, 580, 395]
    ]
    for portal in portals:
        block = Portal(portal[0], portal[1])
        block.rect.x = portal[2]
        block.rect.y = portal[3]
        block.player = self.player
        self.portal_list.add(block)

class Level_02(Level):
 def __init__(self, player):
    Level.__init__(self, player)
    level = [
       [210, 32, 300, 300],
       [210, 32, 500, 450],
       [210, 32, 300, 200],
    ]
    for platform in level:
       block = Platform(platform[0], platform[1])
       block.rect.x = platform[2]
       block.rect.y = platform[3]
       block.player = self.player
       self.platform_list.add(block)
    spikes = [
        [10, 20, 550, 485],
        [10, 20, 200, 400],
        [10, 20, 600, 300],
    ]
    for spike in spikes:
        block = Spike(spike[0], spike[1])
        block.rect.x = spike[2]
        block.rect.y = spike[3]
        block.player = self.player
        self.spikes_list.add(block)

def main():
 global change_level
 pygame.init()
 size = [SCREEN_WIDTH, SCREEN_HEIGHT]
 screen = pygame.display.set_mode(size)
 pygame.display.set_caption("Платформер")
 player = Player()
 level_list = []
 level_list.append(Level_01(player))
 level_list.append(Level_02(player))

 current_level = level_list[current_level_no]

 active_sprite_list = pygame.sprite.Group()
 player.level = current_level

 player.rect.x = 340
 player.rect.y = SCREEN_HEIGHT - player.rect.height
 active_sprite_list.add(player)

 done = False
 clock = pygame.time.Clock()
 while not done:
    current_level = level_list[current_level_no]
    if current_level_no > 0 and change_level == True:
        active_sprite_list = pygame.sprite.Group()
        player.level = current_level
        player.rect.x = 340
        player.rect.y = SCREEN_HEIGHT - player.rect.height
        active_sprite_list.add(player)
        change_level = False
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
          done = True
       if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_LEFT:
             player.go_left()
          if event.key == pygame.K_RIGHT:
             player.go_right()
          if event.key == pygame.K_UP:
             player.jump()

       if event.type == pygame.KEYUP:
          if event.key == pygame.K_LEFT and player.change_x < 0:
             player.stop()
          if event.key == pygame.K_RIGHT and player.change_x > 0:
             player.stop()
    active_sprite_list.update()
    current_level.update()

    if player.rect.right > SCREEN_WIDTH:
       player.rect.right = SCREEN_WIDTH

    if player.rect.left < 0:
       player.rect.left = 0

    current_level.draw(screen)
    active_sprite_list.draw(screen)
    clock.tick(30)
    pygame.display.flip()
 pygame.quit()
main()



