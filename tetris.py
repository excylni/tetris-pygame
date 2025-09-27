import pygame
import sys
import os
from game import Game

dark_blue = (30, 40, 120)
light_blue = (90, 100, 160)
white = (255, 255, 255)

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

font_path = os.path.join(base_path, "gomarice_no_continue.ttf")

pygame.init()
icon = pygame.image.load("tetris.png")
pygame.display.set_icon(icon)
title_font = pygame.font.Font(font_path, 40)
score_surface = title_font.render("Score", True, white)
next_surface = title_font.render("Next", True, white)
game_over_surface = title_font.render("GAME OVER", True, white)


score_rect = pygame.Rect(320, 75, 170, 60)
next_rect = pygame.Rect(320, 235, 170, 180)


screen = pygame.display.set_mode((500, 650))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()


game = Game(base_path)

GAME_EVENT = pygame.USEREVENT
BLOCK_DROP = pygame.USEREVENT + 1
ANIM_EVENT = pygame.USEREVENT + 2

pygame.time.set_timer(ANIM_EVENT, 100)
pygame.time.set_timer(BLOCK_DROP, 50)
pygame.time.set_timer(GAME_EVENT, 200)

# Game Loop
while True:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if game.game_over:
                game.game_over = False
                game.reset()
            if event.key == pygame.K_LEFT and not game.game_over:
                game.move_left()
            if event.key == pygame.K_RIGHT and not game.game_over:
                game.move_right()
            if event.key == pygame.K_SPACE and not game.game_over:
                game.rotate_block()
        if event.type == GAME_EVENT and not game.game_over:
            game.move_down()
            game.grid.update_effects(dt)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == BLOCK_DROP and not game.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN] and not game.game_over:
                game.update_score(0, 1)
                game.move_down()
                game.grid.update_effects(dt)

    score_value_surface = title_font.render(str(game.score), True, white)
    screen.fill(dark_blue)
    screen.blit(score_surface, (350, 20, 50, 50))
    screen.blit(next_surface, (360, 180, 50, 50))
    pygame.draw.rect(screen, light_blue, score_rect, 0, 10)
    pygame.draw.rect(screen, light_blue, next_rect, 0, 10)
    screen.blit(score_value_surface,
                score_value_surface.get_rect(centerx=score_rect.centerx,
                                             centery=score_rect.centery)) 

    if game.game_over is True:
        screen.blit(game_over_surface, (315, 450, 50, 50))

    game.draw(screen)
    pygame.display.update()
