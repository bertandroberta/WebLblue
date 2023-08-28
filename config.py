'''
Function:
	config file.
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import os



'''train'''
batch_size = 32
max_explore_iterations = 5000
max_memory_size = 100000
max_train_iterations = 100000
save_interval = 10000
save_dir = 'model_saved'
frame_size = None # calculated automatically according to the layout file
num_continuous_frames = 1
logfile = 'train.log'
eps_start = 1.0 # prob to explore at first # 探索概率逐渐降低
eps_end = 0.1 # prob to explore finally
eps_num_steps = 10000

'''test'''
weightspath = os.path.join(save_dir, str(max_train_iterations)+'.pkl') # trained model path

'''game'''
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
SKYBLUE = (0, 191, 255)
lblue_image_path = 'LB.png'
cake_image_path = 'Cake.png'
gao_image_path = 'gmf.png'
jian_image_path = 'LJ.png'
begin1_image = 'begin1.png'
begin2_image = 'begin2.png'
end1_image = 'end1.png'
end2_image = 'end2.png'
title_image = 'title.png'
bg2_play1 = 'play1.png'
bg2_play2 = 'play2.png'
bg = 'PosterFormal.jpg'
bg2 = 'bg2.png'
layout_filepath = 'layouts/mediumClassic.lay' # decide the game map
ghost_image_paths = [(each.split('.')[0], os.path.join(os.getcwd(), each)) for each in ['gameAPI/images/Blinky.png', 'gameAPI/images/Inky.png', 'gameAPI/images/Pinky.png', 'gameAPI/images/Clyde.png']]
scaredghost_image_path = os.path.join(os.getcwd(), 'gameAPI/images/scared.png')
pacman_image_path = ('pacman', os.path.join(os.getcwd(), 'gameAPI/images/pacman.png'))
font_path = os.path.join(os.getcwd(), 'gameAPI/font/ALGER.TTF')
grid_size = 96
operator = 'person' # 'person' or 'ai', used in demo.py
