import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
bg = pygame.image.load('icon/Bg.png')

bg = pygame.transform.scale(bg, (bg.get_width()//1.8, bg.get_height()//1.8))

class Player(pygame.sprite.Sprite):
    right = True

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((60, 70))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.change_x = 0
        self.change_y = 0

    def update(self):
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
        self.image = pygame.Surface((210, 30))
        self.image.fill((0, 255, 0))

        self.rect = self.image.get_rect()


class Level(object):
	def __init__(self, player):
		self.platform_list = pygame.sprite.Group()
		self.player = player

	def update(self):
		self.platform_list.update()

	def draw(self, screen):
		screen.blit(bg, (0, 0))

		self.platform_list.draw(screen)


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


def main():
	pygame.init()

	size = [SCREEN_WIDTH, SCREEN_HEIGHT]
	screen = pygame.display.set_mode(size)

	pygame.display.set_caption("Vocatio")
	icon = pygame.image.load('icon/ico.png')
	pygame.display.set_icon(icon)

	player = Player()

	level_list = []
	level_list.append(Level_01(player))

	current_level_no = 0
	current_level = level_list[current_level_no]

	active_sprite_list = pygame.sprite.Group()
	player.level = current_level

	player.rect.x = 340
	player.rect.y = SCREEN_HEIGHT - player.rect.height
	active_sprite_list.add(player)

	run_game = True

	clock = pygame.time.Clock()

	while run_game:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run_game = False

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


if __name__ == '__main__':
    main()
