import config
from gameAPI.game import GamePacmanAgent
import asyncio
import pygame
from gameAPI.button import Button, ButtonImage
import sys



async def main():
    times = 0
    while True:

        self = GamePacmanAgent(config,times)
        self.screen.blit(self.bg, (0, 0))
        self.bg_width = self.bg.get_width()
        self.bg_height = self.bg.get_height()

        game_title = pygame.image.load(config.title_image).convert()
        game_title= pygame.transform.scale(game_title, (game_title.get_width() * 2, game_title.get_height() * 2))

        # game_title  = pygame.transform.scale(game_title)

        self.screen.blit(game_title, (self.bg_width * 0.5, self.bg_height * 0.05))
        play_button_pos_x = self.bg_width * 0.7
        play_button_pos_y = self.bg_height * 0.2
        # exit_button_pos_x = self.bg_width * 0.7
        # exit_button_pos_y = self.bg_height * 0.35
        play_button = ButtonImage(self.config.begin1_image, play_button_pos_x, play_button_pos_y,ratio=0.8)
        # exit_button = ButtonImage(self.config.end1_image, exit_button_pos_x, exit_button_pos_y,ratio=0.8)

        play_button.display(self.screen)
        # exit_button.display(self.screen)
        pygame.display.update()
        await asyncio.sleep(0)
        while True:
            if play_button.check_click(pygame.mouse.get_pos()):
                play_button = ButtonImage(self.config.begin1_image, play_button_pos_x, play_button_pos_y, ratio=0.8)
            else:
                play_button = ButtonImage(self.config.begin2_image, play_button_pos_x, play_button_pos_y, ratio=0.8)

            # if exit_button.check_click(pygame.mouse.get_pos()):
            #     exit_button = ButtonImage(self.config.end1_image, exit_button_pos_x, exit_button_pos_y, ratio=0.8)
            # else:
            #     exit_button = ButtonImage(self.config.end2_image, exit_button_pos_x, exit_button_pos_y, ratio=0.8)

            play_button.display(self.screen)
            # exit_button.display(self.screen)
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
                    pygame.quit()
                    raise SystemExit

        # 规则界面
        bg2 = pygame.image.load(config.bg2)
        bg2= pygame.transform.scale(bg2, (bg2.get_width() * 0.6, bg2.get_height() * 0.6))

        self.screen = pygame.display.set_mode([bg2.get_width(), bg2.get_height()])  # 设置屏幕大小
        self.screen.blit(bg2, (0, 0))
        play_button_pos_x = bg2.get_width() * 0.85
        play_button_pos_y = bg2.get_height() * 0.9
        pygame.display.update()
        await asyncio.sleep(0)
        while True:
            if play_button.check_click(pygame.mouse.get_pos()):
                play_button = ButtonImage(self.config.bg2_play1, play_button_pos_x, play_button_pos_y, ratio=0.8)
            else:
                play_button = ButtonImage(self.config.bg2_play2, play_button_pos_x, play_button_pos_y, ratio=0.8)

            play_button.display(self.screen)
            pygame.display.update()
            await asyncio.sleep(0)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
            if pygame.mouse.get_pressed()[0]:
                if play_button.check_click(pygame.mouse.get_pos()):
                    break

        # 正式开始
        clock = pygame.time.Clock()
        start_tick = pygame.time.get_ticks()
        total_time = 60
        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])  # 设置屏幕大小
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
            if rest_time == 0 and self.score > gao_score:
                is_win = True
                break
            if rest_time == 0 and self.score <= gao_score:
                is_win = False
                break

            pygame.display.flip()
            await asyncio.sleep(0)
            clock.tick(30)  # 限制游戏循环的速率为每秒 30 帧

        if is_win:
            bg_end = pygame.image.load(config.bgend1)
            msg = 'You won!'
            position = (self.screen_width // 2 - 50, int(self.screen_height / 2.5))

        else:
            bg_end = pygame.image.load(config.bgend2)
            msg = 'Game Over!'
            position = (self.screen_width // 2 - 80, int(self.screen_height / 2.5))

        # 结束界面


        bg_end = pygame.transform.scale(bg_end, (bg_end.get_width() * 0.6, bg_end.get_height() * 0.6))
        self.screen = pygame.display.set_mode([bg_end.get_width(), bg_end.get_height()])  # 设置屏幕大小
        self.screen.blit(bg_end, (0, 0))
        back_button_pos_x = bg_end.get_width() * 0.8
        back_button_pos_y = bg_end.get_height() * 0.9
        back_button = ButtonImage(self.config.back2menublack, back_button_pos_x, back_button_pos_y, ratio=0.8)

        pygame.display.update()
        await asyncio.sleep(0)
        while True:
            if back_button.check_click(pygame.mouse.get_pos()):
                back_button = ButtonImage(self.config.back2menured, back_button_pos_x, back_button_pos_y, ratio=0.8)
            else:
                if is_win:
                    back_button = ButtonImage(self.config.back2menublack, back_button_pos_x, back_button_pos_y, ratio=0.8)
                else:
                    back_button = ButtonImage(self.config.back2menublue, back_button_pos_x, back_button_pos_y, ratio=0.8)

            back_button.display(self.screen)
            pygame.display.update()
            await asyncio.sleep(0)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
            if pygame.mouse.get_pressed()[0]:
                if back_button.check_click(pygame.mouse.get_pos()):
                    break
        times += 1
    # 结束界面
    # clock = pygame.time.Clock()
    # text = self.font.render(msg, True, self.config.WHITE)
    # while True:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             sys.exit()
    #             pygame.quit()
    #     self.screen.fill(self.config.BLACK)
    #     self.screen.blit(text, position)
    #     pygame.display.flip()
    #     await asyncio.sleep(0)
    #     clock.tick(10)

asyncio.run(main())