import config
from gameAPI.game import GamePacmanAgent
import asyncio
import pygame
from gameAPI.button import Button

game = GamePacmanAgent(config)

async def main(self):
    font_name = pygame.font.match_font('Microsoft YaHei')
    screen_font = pygame.font.Font(font_name, 48)
    self.screen.blit(self.bg, (0, 0))
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
            play_button = Button(screen_font, '开始游戏', self.config.RED, self.screen_width * 0.8,
                                 self.screen_height * 0.3)
        else:
            play_button = Button(screen_font, '开始游戏', self.config.WHITE, self.screen_width * 0.8,
                                 self.screen_height * 0.3)

        if exit_button.check_click(pygame.mouse.get_pos()):
            exit_button = Button(screen_font, '退出', self.config.RED, self.screen_width * 0.8, self.screen_height * 0.4)
        else:
            exit_button = Button(screen_font, '退出', self.config.WHITE, self.screen_width * 0.8,
                                 self.screen_height * 0.4)

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
            cake_eaten = pygame.sprite.spritecollide(lblue, self.cake_sprites, True)  # 设置碰撞，豆子被吃掉了

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
        clock.tick(30)  # 限制游戏循环的速率为每秒 30 帧
    if is_win:
        self.__showText(msg='You won!', position=(self.screen_width // 2 - 50, int(self.screen_height / 2.5)))
    else:
        self.__showText(msg='Game Over!', position=(self.screen_width // 2 - 80, int(self.screen_height / 2.5)))

asyncio.run(main(game))