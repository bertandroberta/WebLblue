'''
Function:
	define the game agent
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''

import sys
import asyncio
from .sprites import *
from .button import Button

# 根据Text文件生成地图
'''layout file parser'''
class LayoutParser():
	def __init__(self, config, **kwargs):
		self.gamemap = self.__parse(config.layout_filepath) # 二维
		self.height = len(self.gamemap)
		self.width = len(self.gamemap[0])
	'''parse .lay'''
	def __parse(self, filepath):
		gamemap = []
		f = open(filepath)
		for line in f.readlines():
			elements = []
			for c in line:
				if c == '%':
					elements.append('wall')
				elif c == '.':
					elements.append('cake')
				elif c == 'o':
					elements.append('cake')
				elif c == 'P':
					elements.append('Lblue')
				elif c in ['G']:
					elements.append('Gao')
				elif c == ' ':
					elements.append(' ')
				elif c == 'J':
					elements.append('Jian')
			gamemap.append(elements)
		f.close()
		return gamemap


'''define the game agent'''
class GamePacmanAgent():
	def __init__(self, config, **kwargs):
		self.config = config
		self.layout = LayoutParser(config)
		self.screen_width = self.layout.width * config.grid_size
		self.screen_height = self.layout.height * config.grid_size
		self.bg = bg = pygame.image.load(config.bg)
		self.reset()


	async def starting_screen(self):
		font_name = pygame.font.match_font('Microsoft YaHei')
		screen_font = pygame.font.Font(font_name, 48)
		self.screen.blit(self.bg, (0,0))
		game_title = screen_font.render('布布姐的蛋糕冲锋', True, self.config.BLUE)
		self.screen.blit(game_title, (self.screen_width * 0.8, self.screen_height * 0.2))

		play_button = Button(screen_font, '开始游戏', self.config.RED, self.screen_width * 0.8, self.screen_height * 0.3)
		exit_button = Button(screen_font, '退出', self.config.WHITE, self.screen_width * 0.8, self.screen_height * 0.4)
		play_button.display(self.screen)
		exit_button.display(self.screen)
		pygame.display.update()
		await asyncio.sleep(0)
		while True:
			if play_button.check_click(pygame.mouse.get_pos()):
				play_button = Button(screen_font, '开始游戏', self.config.RED, self.screen_width * 0.8, self.screen_height * 0.3)
			else:
				play_button = Button(screen_font, '开始游戏', self.config.WHITE, self.screen_width * 0.8, self.screen_height * 0.3)

			if exit_button.check_click(pygame.mouse.get_pos()):
				exit_button = Button(screen_font, '退出', self.config.RED, self.screen_width * 0.8, self.screen_height * 0.4)
			else:
				exit_button = Button(screen_font, '退出', self.config.WHITE, self.screen_width * 0.8, self.screen_height * 0.4)

			play_button.display(self.screen)
			exit_button.display(self.screen)
			pygame.display.update()
			await asyncio.sleep(0)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					raise SystemExit
			if pygame.mouse.get_pressed()[0]:
				if play_button.check_click(pygame.mouse.get_pos()):
					break
				if exit_button.check_click(pygame.mouse.get_pos()):
					break


	'''run game(user control, for test)'''
	async def runGame(self):
		self.starting_screen()
		clock = pygame.time.Clock()
		start_tick = pygame.time.get_ticks()
		total_time = 300
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(-1)
					pygame.quit()
			# 键盘控制操作
			pressed_keys = pygame.key.get_pressed()
			if pressed_keys[pygame.K_UP]:
				self.lblue_sprites.update([0, -1], self.wall_sprites)
			elif pressed_keys[pygame.K_DOWN]:
				self.lblue_sprites.update([0, 1], self.wall_sprites)
			elif pressed_keys[pygame.K_LEFT]:
				self.lblue_sprites.update([-1, 0], self.wall_sprites)
			elif pressed_keys[pygame.K_RIGHT]:
				self.lblue_sprites.update([1, 0], self.wall_sprites)

			for lblue in self.lblue_sprites:
				cake_eaten = pygame.sprite.spritecollide(lblue, self.cake_sprites, True) # 设置碰撞，豆子被吃掉了

			# nonscared_ghost_sprites = pygame.sprite.Group()
			# dead_ghost_sprites = pygame.sprite.Group()
			#
			# for ghost in self.ghost_sprites:
			# 	if ghost.is_scared:
			# 		if pygame.sprite.spritecollide(ghost, self.pacman_sprites, False): # 设置碰撞，但picman还存在
			# 			self.score += 6
			# 			dead_ghost_sprites.add(ghost)
			# 	else:
			# 		nonscared_ghost_sprites.add(ghost)
			# for ghost in dead_ghost_sprites:
			# 	ghost.reset()

			self.score += len(cake_eaten) * 2

			self.jian_sprites.update(self.wall_sprites, self.cake_sprites)
			self.gao_sprites.update(self.wall_sprites, self.cake_sprites)

			# update完了，绘制新的图像界面
			self.screen.fill(self.config.BLACK)
			self.wall_sprites.draw(self.screen)
			self.cake_sprites.draw(self.screen)
			self.lblue_sprites.draw(self.screen)
			self.gao_sprites.draw(self.screen)
			self.jian_sprites.draw(self.screen)

			# 计算李布得分和健哥得分
			text = self.font.render('SCORE: %s' % self.score, True, self.config.WHITE)
			self.screen.blit(text, (2, 2))
			gao_score = 0
			for gao in self.gao_sprites:
				gao_score += gao.score
			gao_text = self.font.render('GAO_SCORE: %s' % gao_score, True, self.config.RED)
			self.screen.blit(gao_text, (2, 32))

			# 倒计时
			current_time = pygame.time.get_ticks()
			rest_time = max(total_time - (current_time - start_tick) // 1000, 0)
			time_text = self.font.render('RestTime: %s s' % str(rest_time), True, self.config.RED)
			self.screen.blit(time_text, (2, 62))

			# 判断游戏结束
			if len(self.cake_sprites) == 0 or self.score == 200:
				is_win = True
				break
			if rest_time == 0:
				is_win = False
				break

			pygame.display.flip()
			await asyncio.sleep(0)
			clock.tick(30) # 限制游戏循环的速率为每秒 30 帧
		if is_win:
			self.__showText(msg='You won!', position=(self.screen_width//2-50, int(self.screen_height/2.5)))
		else:
			self.__showText(msg='Game Over!', position=(self.screen_width//2-80, int(self.screen_height/2.5)))


	'''reset'''
	def reset(self):
		self.screen, self.font = self.__initScreen() # 初始化屏幕
		self.wall_sprites, self.lblue_sprites, self.gao_sprites, self.cake_sprites, self.jian_sprites = self.__createGameMap()
		self.actions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
		self.score = 0

	'''show the game info'''
	async def __showText(self, msg, position):
		clock = pygame.time.Clock()
		text = self.font.render(msg, True, self.config.WHITE)
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
					pygame.quit()
			self.screen.fill(self.config.BLACK)
			self.screen.blit(text, position)
			pygame.display.flip()
			await asyncio.sleep(0)
			clock.tick(10)

	def __createGameMap(self):
		# sprite是游戏中处理图像，动画和碰撞检测的基本元素，可以是游戏中的角色，物体，粒子等
		wall_sprites = pygame.sprite.Group() # 墙
		lblue_sprites = pygame.sprite.Group() # 李布
		gao_sprites = pygame.sprite.Group() # 高老师
		cake_sprites = pygame.sprite.Group() # 蛋糕
		jian_sprites = pygame.sprite.Group() # 健哥


		for i in range(self.layout.height):
			for j in range(self.layout.width):
				elem = self.layout.gamemap[i][j]
				if elem == 'wall':
					position = [j * self.config.grid_size, i*self.config.grid_size]
					wall_sprites.add(Wall(*position, self.config.grid_size, self.config.grid_size, self.config.SKYBLUE))
				elif elem == 'cake':
					position = [j*self.config.grid_size+self.config.grid_size*0.5, i*self.config.grid_size+self.config.grid_size*0.5]
					cake_sprites.add(Cake(*position, self.config.cake_image_path, self.config.grid_size))
				elif elem == 'Lblue':
					position = [j*self.config.grid_size+self.config.grid_size*0.5, i*self.config.grid_size+self.config.grid_size*0.5]
					lblue_sprites.add(LBLUE(*position, self.config.lblue_image_path, self.config.grid_size))
				elif elem == 'Gao':
					position = [j*self.config.grid_size+self.config.grid_size*0.5, i*self.config.grid_size+self.config.grid_size*0.5]
					gao_sprites.add(Gao(*position, self.config.gao_image_path, self.config.grid_size,self.config))
				elif elem == 'Jian':
					position = [j*self.config.grid_size+self.config.grid_size*0.5, i*self.config.grid_size+self.config.grid_size*0.5]
					jian_sprites.add(Jian(*position, self.config.jian_image_path, self.config.grid_size,self.config))

		return wall_sprites, lblue_sprites, gao_sprites, cake_sprites, jian_sprites

	'''initialize the game screen'''
	def __initScreen(self):
		pygame.init()
		pygame.font.init()
		screen = pygame.display.set_mode([self.screen_width, self.screen_height]) # 设置屏幕大小
		pygame.display.set_caption('蛋糕冲锋！')
		font = pygame.font.Font(self.config.font_path, 24)
		return screen, font