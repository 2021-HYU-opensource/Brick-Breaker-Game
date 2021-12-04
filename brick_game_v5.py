# *************************  BRICK BREAKER GAME ******************************

import pygame
import sys
from pygame.locals import *

# 오브젝트의 크기
screen_size = (850, 480)
brick_width = 50
brick_height = 50
paddle_width = 120
paddle_height = 20
ball_diameter = 24
ball_radius = ball_diameter // 2

# 새로운 벽돌 관련 변수들
nbrick_width = 80
nbrick_height = 60

# Boundaries
max_paddlex = screen_size[0] - paddle_width
max_ballx = screen_size[0] - ball_diameter
max_bally = screen_size[1] - ball_diameter

# Y 좌표
paddley = screen_size[1] - paddle_height - 10

# 색상
white = (255, 255, 255)
turqoise = (3, 155, 229)
grey2 = (44, 62, 80)
brown2 = (201,147,83)
yellow = (255, 255, 0)
ibory = (255, 248, 220)
brown = (205, 92, 92)
blue = (135, 206, 250)
pink = (218, 112, 214)
black = (0, 0, 0)

# States
state_ballinpaddle = 0
state_inplay = 1
state_won = 2
state_gameover = 3

# 속도 변수
vel = 5


class brickbreaker():

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("BrickBreaker")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont('Lucida Sans Roman', 20)
        self.init_game()

    def init_game(self):
        self.lives = 5
        self.score = 0
        self.state = state_ballinpaddle

        self.paddle = pygame.Rect(365, paddley, paddle_width, paddle_height)
        self.ball = pygame.Rect(365, paddley - ball_diameter, ball_diameter, ball_diameter)  # ball approximated to the rect object

        # self.ballvel = [0, -50000000000]  # 공의 속도

        self.create_bricks()
        self.create_new_bricks()

    # 벽돌 생성 함수
    def create_bricks(self):
        # x_brick, y_brick -> 벽돌 좌상단 좌표
        y_brick = 30
        self.bricks = [] # 벽돌의 정보를 리스트로 저장

        # 벽돌을 9 * 4로 나열
        for i in range(4):
            x_brick = 120
            for j in range(9):
                self.bricks.append(pygame.Rect(x_brick, y_brick, brick_width, brick_height)) # (x좌표, y좌표, 너비, 높이)
                x_brick += brick_width + 20
            y_brick += brick_height + 20

        # self.bricks.append(pygame.Rect(350, 300, 150, 50)) # 테스트용으로 추가

    # 특수 벽돌 생성 함수
    def create_new_bricks(self):
        # x_nbrick, y_nbrick -> 특수 벽돌 좌상단 좌표
        y_nbrick = 10
        self.newbricks = [] # 특수 벽돌 정보를 리스트로 저장

        # 벽돌을 2 * 4로 나열
        for i in range(4):
            x_nbrick = 20
            for j in range(2):
                self.newbricks.append(pygame.Rect(x_nbrick, y_nbrick, nbrick_width, nbrick_height)) # (x좌표, y좌표, 너비, 높이)
                x_nbrick += nbrick_width + 650
            y_nbrick += nbrick_height + 20

    # 벽돌 그리기 함수
    def draw_bricks(self):
        for brick in self.bricks:
            pygame.draw.rect(self.screen, brown, brick)
        
        # 새로운 벽돌 그리기
        for brick in self.newbricks:
            pygame.draw.rect(self.screen, brown2, brick)

    # 키보드 입력 함수
    def check_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.paddle.left -= 10
            if self.paddle.left < 0:
                self.paddle.left = 0

        if keys[pygame.K_RIGHT]:
            self.paddle.left += 10
            if self.paddle.left > max_paddlex:
                self.paddle.left = max_paddlex

        if keys[pygame.K_SPACE] and self.state == state_ballinpaddle:
            self.ballvel = [vel, -vel] # 여기가 진짜 속도
            self.state = state_inplay

        if keys[pygame.K_q] and (self.state == state_gameover or self.state == state_won):
            pygame.display.quit()
            pygame.quit()
            sys.exit()

        if keys[pygame.K_RETURN] and (self.state == state_gameover or self.state == state_won):  # enter = return
            self.init_game()

    # 공 이동 함수
    def move_ball(self):
        self.ball.left += self.ballvel[0]
        self.ball.top += self.ballvel[1]

        if self.ball.left <= 0:
            self.ball.left = 0
            self.ballvel[0] = -self.ballvel[0]

        elif self.ball.left >= max_ballx:
            self.ball.left = max_ballx
            self.ballvel[0] = -self.ballvel[0]

        if self.ball.top < 0:
            self.ballvel[1] = -self.ballvel[1]
            self.ball.top = 0

        # elif self.ball.top >= max_bally:
        #     self.ball.top =max_bally

    # 공이 오브젝트와 충돌 시
    def handle_coll(self):
        # 공이 벽돌과 충돌
        for brick in self.bricks:
            if self.ball.colliderect(brick):
                self.score += 1
                self.ballvel[1] = -self.ballvel[1]
                self.bricks.remove(brick)
                break

        # 공이 새로운 벽돌과 충돌
        for nbrick in self.newbricks:
            if self.ball.colliderect(nbrick):
                global vel
                self.score += 3
                vel += 1

                if self.ballvel[0] > 0:
                    self.ballvel[0] += 1
                else:
                    self.ballvel[0] -= 1
                
                if self.ballvel[1] > 0:
                    self.ballvel[1] += 1
                else:
                    self.ballvel[1] -= 1
                
                self.ballvel[1] = - self.ballvel[1]

                self.newbricks.remove(nbrick)
                self.size_up()
                break

        # 벽돌을 다 깼을 시
        if len(self.bricks) == 0 and len(self.newbricks) == 0:
            self.state = state_won

        # 공이 패들에 닿았을 때
        if self.ball.colliderect(self.paddle):
            self.ball.top = paddley - ball_diameter
            self.ballvel[1] = -self.ballvel[1]

        # 공이 패들 아래로 떨어졌을 때
        elif self.ball.top > self.paddle.top:
            self.lives -= 1
            if self.lives > 0:
                self.state = state_ballinpaddle
            else:
                self.state = state_gameover
                self.size_reset()
                
                
    # 공 사이즈 리셋 함수
    def size_reset(self):
        global ball_diameter
        global ball_radius
        ball_diameter = 24
        ball_radius = ball_diameter // 2

    # 공 커지게 하는 함수
    def size_up(self):
        global ball_diameter
        global ball_radius
        global max_ballx
        global max_bally
        ball_diameter += 12
        ball_radius = ball_diameter // 2
        max_ballx = screen_size[0] - ball_diameter
        max_bally = screen_size[1] - ball_diameter

    # 점수와 남은 목숨 표시
    def show_stats(self):
        font_surface = self.font.render("SCORE : " + str(self.score) + "  LIVES : " + str(self.lives), False, black)
        self.screen.blit(font_surface, (350, 5))

    # 화면에 메세지 출력
    def show_message(self, message):
        size = self.font.size(message)
        font_surface = self.font.render(message, False, black)
        x = (screen_size[0] - size[0]) / 2
        y = (screen_size[1] - size[1]) / 2
        self.screen.blit(font_surface, (x, y+80))

    # 1
    def run(self):

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()

            self.clock.tick(65)
            self.screen.fill(ibory)
            self.check_input()

            if self.state == state_ballinpaddle:
                self.ball.left = self.paddle.left + paddle_width / 2
                self.ball.top = self.paddle.top - ball_diameter
                self.show_message("Press Space to launch the ball")

            elif self.state == state_gameover:
                self.show_message("Game Over , Press Enter to Play again or Q to quit ")

            elif self.state == state_won:
                self.show_message("You Won! Press enter to play again or q to quit ")

            elif self.state == state_inplay:
                self.move_ball()
                self.handle_coll()

            # 패들 출력
            pygame.draw.rect(self.screen, blue, self.paddle)

            # 공 출력
            pygame.draw.circle(self.screen, pink, (self.ball.left + ball_radius, self.ball.top + ball_radius), ball_radius)

            # 벽돌 출력
            self.draw_bricks()

            # stats 출력
            self.show_stats()
            pygame.display.update()

game = brickbreaker()
game.run()