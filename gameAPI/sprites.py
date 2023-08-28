import pygame
import random


'''define the wall'''
class Wall(pygame.sprite.Sprite):
	def __init__(self, x, y, width, height, color, **kwargs):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([width, height])
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.rect.left = x
		self.rect.top = y


class Cake(pygame.sprite.Sprite):
	def __init__(self, x, y, image_path, image_size):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(pygame.image.load(image_path).convert(),(image_size, image_size))
		self.rect = self.image.get_rect() # 获得食物图像的矩阵区域
		self.rect.center = (x, y) # 设置事物的初始位置

# 高老师是吃蛋糕的
class Gao(pygame.sprite.Sprite):
	def __init__(self, x, y, image_path, image_size, config):
		pygame.sprite.Sprite.__init__(self)
		self.ori_x, self.ori_y = x, y
		image_size = 0.9 * image_size # 为了不卡墙
		self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(),(image_size, image_size))
		self.config = config
		# 设置碰撞
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

		# 记录之前的位置
		self.prev_x, self.prev_y = x, y

		# 速度
		self.base_speed = [12, 12]
		self.speed = [0, 0]

		# 方向
		self.direction_now = None # 当前direction
		self.direction_legals = [] # 合法direction
		self.gain_directions = [] # 可获得收益的direction
		self.directions = [[-1, 0], [1, 0], [0, 1], [0, -1]]

		self.score = 0

	# 每一帧怎么动
	def update(self, wall_sprites, cake_sprites):

		self.direction_now = self.__chooseAction(self.__getLegalAction(wall_sprites),cake_sprites)
		ori_image = self.image
		if self.direction_now[0] < 0:
			self.image = pygame.transform.flip(ori_image, True, False)
		elif self.direction_now[0] > 0:
			self.image = ori_image.copy()
		elif self.direction_now[1] < 0:
			self.image = pygame.transform.rotate(ori_image, 90)
		elif self.direction_now[1] > 0:
			self.image = pygame.transform.rotate(ori_image, -90)
		self.speed = [self.direction_now[0] * self.base_speed[0], self.direction_now[1] * self.base_speed[1]]
		# 健哥自己也吃蛋糕
		cake_eaten = pygame.sprite.spritecollide(self, cake_sprites, True)
		self.score += len(cake_eaten) * 2
		# move
		self.rect.left += self.speed[0]
		self.rect.top += self.speed[1]
		return True

	# 选择怎么动：原则1. 去更多的空地 原则2. 保持动作惯性【我现在有两个动作，首先考虑等于self.direction_now
	def __chooseAction(self, direction_legals, cake_sprites):
		if len(direction_legals) == 1:
			return direction_legals[0]
		# 可以获得收益的方向
		gain_directions = []
		for direction in direction_legals:
			speed = [direction[0] * self.base_speed[0], direction[1] * self.base_speed[1]]
			next_posx, next_posy = (self.rect.left + speed[0], self.rect.top + speed[1])
			x_prev = self.rect.left
			y_prev = self.rect.top
			self.rect.left += next_posx
			self.rect.top += next_posy
			is_collide = pygame.sprite.spritecollide(self, cake_sprites, False)
			self.rect.left = x_prev
			self.rect.top = y_prev
			if not is_collide:
				gain_directions.append(direction)
		if len(gain_directions) > 0:
			if sorted(gain_directions) == sorted(self.gain_directions):
				return self.direction_now
			else:
				self.gain_directions = gain_directions
				return random.choice(self.gain_directions)
		else:
			# 如果下一步的合法位置都有蛋糕，那么应该以高概率向靠近蛋糕的位置走
			cake_poss = []
			for cake_sprite in cake_sprites:
				cake_poss.append(cake_sprite.rect.center)

			min_dis = float('inf')
			best_direction = None
			best_prob = 0.8

			for direction in direction_legals:
				speed = [direction[0] * self.base_speed[0], direction[1] * self.base_speed[1]]
				next_posx, next_posy = (self.rect.left + speed[0], self.rect.top + speed[1])
				dis = self.__calculateDistance(cake_poss, next_posx, next_posy)
				if dis < min_dis:
					min_dis = dis
					best_direction = direction

			probs = {}
			for direction in direction_legals:
				tuple_direction = tuple(direction)
				if direction == best_direction:
					probs[tuple_direction] = best_prob
				else:
					probs[tuple_direction] = (1 - best_prob) / (len(direction_legals) - 1)

			base = 0.0
			r = random.random()
			for key, value in probs.items():
				base += value
				if r <= base:
					return list(key)

	# 计算与蛋糕的距离和
	def __calculateDistance(self, cake_poss, x, y):
		dis = 0
		for cake_pos in cake_poss:
			cake_x, cake_y = cake_pos[0], cake_pos[1]
			dis += abs(x - cake_x) + abs(y - cake_y)
		return dis

	# 获得所有的合法动作
	def __getLegalAction(self, wall_sprites):
		direction_legals = []
		for direction in self.directions:
			if self.__isActionLegal(direction, wall_sprites):
				direction_legals.append(direction)
		if sorted(direction_legals) == sorted(self.direction_legals):
			return [self.direction_now]
		else:
			self.direction_legals = direction_legals
			return self.direction_legals

	# 判断动作是否会撞墙
	def __isActionLegal(self, direction, wall_sprites):
		speed = [direction[0] * self.base_speed[0], direction[1] * self.base_speed[1]]
		x_prev = self.rect.left
		y_prev = self.rect.top
		self.rect.left += speed[0]
		self.rect.top += speed[1]
		is_collide = pygame.sprite.spritecollide(self, wall_sprites, False) # pygame.sprite.spritecollide(sprite, group, dokill, collided=None)
		self.rect.left = x_prev
		self.rect.top = y_prev
		return not is_collide

# 健哥是放蛋糕的
class Jian(pygame.sprite.Sprite):
	def __init__(self, x, y, image_path, image_size, config):
		pygame.sprite.Sprite.__init__(self)
		self.ori_x, self.ori_y = x, y
		image_size = 0.9 * image_size # 为了不卡墙
		self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(),(image_size, image_size))
		self.config = config
		# 设置碰撞
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

		# 记录之前的位置
		self.prev_x, self.prev_y = x, y

		# 速度
		self.base_speed = [12, 12]
		self.speed = [0, 0]

		# 方向
		self.direction_now = None # 当前direction
		self.direction_legals = [] # 合法direction
		self.gain_directions = [] # 可获得收益的direction
		self.directions = [[-1, 0], [1, 0], [0, 1], [0, -1]]

	# 每一帧怎么动
	def update(self, wall_sprites, cake_sprites):

		self.direction_now = self.__chooseAction(self.__getLegalAction(wall_sprites),cake_sprites)
		ori_image = self.image
		if self.direction_now[0] < 0:
			self.image = pygame.transform.flip(ori_image, True, False)
		elif self.direction_now[0] > 0:
			self.image = ori_image.copy()
		elif self.direction_now[1] < 0:
			self.image = pygame.transform.rotate(ori_image, 90)
		elif self.direction_now[1] > 0:
			self.image = pygame.transform.rotate(ori_image, -90)
		self.speed = [self.direction_now[0] * self.base_speed[0], self.direction_now[1] * self.base_speed[1]]
		# 如果和已有的蛋糕不碰撞，那么放一个蛋糕
		if not pygame.sprite.spritecollide(self, cake_sprites, False):
			position = list(self.rect.center)
			cake_sprites.add(Cake(*position, self.config.cake_image_path, self.config.grid_size))
		# move
		self.rect.left += self.speed[0]
		self.rect.top += self.speed[1]
		return True

	# 选择怎么动：原则1. 去更多的空地 原则2. 保持动作惯性【我现在有两个动作，首先考虑等于self.direction_now
	def __chooseAction(self, direction_legals, cake_sprites):
		if len(direction_legals) == 1:
			return direction_legals[0]
		# 可以获得收益的方向
		gain_directions = []
		for direction in direction_legals:
			speed = [direction[0] * self.base_speed[0], direction[1] * self.base_speed[1]]
			next_posx, next_posy = (self.rect.left + speed[0], self.rect.top + speed[1])
			x_prev = self.rect.left
			y_prev = self.rect.top
			self.rect.left += next_posx
			self.rect.top += next_posy
			is_collide = pygame.sprite.spritecollide(self, cake_sprites, False)
			self.rect.left = x_prev
			self.rect.top = y_prev
			if not is_collide:
				gain_directions.append(direction)
		if len(gain_directions) > 0:
			if sorted(gain_directions) == sorted(self.gain_directions):
				return self.direction_now
			else:
				self.gain_directions = gain_directions
				return random.choice(self.gain_directions)
		else:
			# 如果下一步的合法位置都有蛋糕，那么应该以高概率向远离蛋糕的位置走
			cake_poss = []
			for cake_sprite in cake_sprites:
				cake_poss.append(cake_sprite.rect.center)

			max_dis = 0
			best_direction = None
			best_prob = 0.8

			for direction in direction_legals:
				speed = [direction[0] * self.base_speed[0], direction[1] * self.base_speed[1]]
				next_posx, next_posy = (self.rect.left + speed[0], self.rect.top + speed[1])
				dis = self.__calculateDistance(cake_poss, next_posx, next_posy)
				if dis > max_dis:
					max_dis = dis
					best_direction = direction

			probs = {}
			for direction in direction_legals:
				tuple_direction = tuple(direction)
				if direction == best_direction:
					probs[tuple_direction] = best_prob
				else:
					probs[tuple_direction] = (1 - best_prob) / (len(direction_legals) - 1)

			base = 0.0
			r = random.random()
			for key, value in probs.items():
				base += value
				if r <= base:
					return list(key)

	# 计算与蛋糕的距离和
	def __calculateDistance(self, cake_poss, x, y):
		dis = 0
		for cake_pos in cake_poss:
			cake_x, cake_y = cake_pos[0], cake_pos[1]
			dis += abs(x - cake_x) + abs(y - cake_y)
		return dis

	# 获得所有的合法动作
	def __getLegalAction(self, wall_sprites):
		direction_legals = []
		for direction in self.directions:
			if self.__isActionLegal(direction, wall_sprites):
				direction_legals.append(direction)
		if sorted(direction_legals) == sorted(self.direction_legals):
			return [self.direction_now]
		else:
			self.direction_legals = direction_legals
			return self.direction_legals

	# 判断动作是否会撞墙
	def __isActionLegal(self, direction, wall_sprites):
		speed = [direction[0] * self.base_speed[0], direction[1] * self.base_speed[1]]
		x_prev = self.rect.left
		y_prev = self.rect.top
		self.rect.left += speed[0]
		self.rect.top += speed[1]
		is_collide = pygame.sprite.spritecollide(self, wall_sprites, False) # pygame.sprite.spritecollide(sprite, group, dokill, collided=None)
		self.rect.left = x_prev
		self.rect.top = y_prev
		return not is_collide



'''define the LBLUE'''
class LBLUE(pygame.sprite.Sprite):
	def __init__(self, x, y, role_image_path, image_size, **kwargs):
		pygame.sprite.Sprite.__init__(self)
		self.role_name = role_image_path[0]
		image_size = 0.75 * image_size  # 为了不卡墙
		self.base_image = pygame.image.load(role_image_path).convert_alpha()
		self.base_image = pygame.transform.scale(self.base_image, (image_size, image_size))
		self.image = self.base_image.copy()
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.base_speed = [12, 12]
		self.speed = [0, 0]
	'''update'''
	def update(self, direction, wall_sprites):
		# update attributes
		if direction[0] < 0:
			self.image = pygame.transform.flip(self.base_image, True, False)
		elif direction[0] > 0:
			self.image = self.base_image.copy()
		elif direction[1] < 0:
			self.image = pygame.transform.rotate(self.base_image, 90)
		elif direction[1] > 0:
			self.image = pygame.transform.rotate(self.base_image, -90)
		self.speed = [direction[0] * self.base_speed[0], direction[1] * self.base_speed[1]]
		# try move
		x_prev = self.rect.left
		y_prev = self.rect.top
		self.rect.left += self.speed[0]
		self.rect.top += self.speed[1]
		is_collide = pygame.sprite.spritecollide(self, wall_sprites, False)

		if is_collide:
			self.rect.left = x_prev
			self.rect.top = y_prev
			return False
		return True