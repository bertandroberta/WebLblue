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
import os
import random

# 根据Text文件生成地图
'''layout file parser'''
class LayoutParser():
	def __init__(self, config, times = 0, **kwargs):
		self.gamemapRoot = config.layout_fileroot
		lay_outFile = []
		for root, dirs, files in os.walk(self.gamemapRoot):
			for file in files:
				if file.split('.')[-1] == 'lay':
					lay_outFile.append(os.path.join(self.gamemapRoot,file))
		if times > 0:
			layout = random.choice(lay_outFile)
		else:
			layout = config.layout_filepath
		self.gamemap = self.__parse(layout) # 二维
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
	def __init__(self, config, times = 0, **kwargs):
		self.config = config
		self.layout = LayoutParser(config, times = times)
		self.screen_width = self.layout.width * config.grid_size
		self.screen_height = self.layout.height * config.grid_size
		self.bg = pygame.image.load(config.bg)
		self.bg = pygame.transform.scale(self.bg, (self.bg.get_width() * 0.8, self.bg.get_height() * 0.8))
		wall_color = [self.config.WHITE,self.config.BLUE,self.config.GREEN,self.config.RED,self.config.YELLOW,
					  self.config.PURPLE,self.config.SKYBLUE]
		self.wall_color = random.choice(wall_color)
		self.reset()


	'''reset'''
	def reset(self):
		self.screen, self.font = self.__initScreen() # 初始化屏幕
		self.wall_sprites, self.lblue_sprites, self.gao_sprites, self.cake_sprites, self.jian_sprites = self.__createGameMap()
		self.actions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
		self.score = 0


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
					wall_sprites.add(Wall(*position, self.config.grid_size, self.config.grid_size, self.wall_color))
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
		screen = pygame.display.set_mode([self.bg.get_width(), self.bg.get_height()]) # 设置屏幕大小
		pygame.display.set_caption('布布姐的蛋糕冲锋！')
		font = pygame.font.Font(self.config.font_path, 24)
		return screen, font