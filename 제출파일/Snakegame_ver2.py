import pygame
import sys
import random
import time

pygame.init()

BACK_W =440
BACK_H=560
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
BLOCK_SIZE = 20


RED = 255, 0, 0        # 적색:   적 255, 녹   0, 청   0
GREEN = 0, 255, 0      # 녹색:   적   0, 녹 255, 청   0
BLUE = 0, 0, 255       # 청색:   적   0, 녹   0, 청 255
PURPLE = 127, 0, 127   # 보라색: 적 127, 녹   0, 청 127
BLACK = 0, 0, 0        # 검은색: 적   0, 녹   0, 청   0
GRAY = 127, 127, 127   # 회색:   적 127, 녹 127, 청 127
WHITE = 255, 255, 255  # 하얀색: 적 255, 녹 255, 청 255


DIRECTION_ON_KEY = {
    pygame.K_UP: 'north',
    pygame.K_DOWN: 'south',
    pygame.K_LEFT: 'west',
    pygame.K_RIGHT: 'east',
}


def draw_background(screen):
    """게임의 배경을 그린다"""
    background =pygame.Rect((20,140),(SCREEN_WIDTH,SCREEN_HEIGHT)) 
    pygame.draw.rect(SCREEN, WHITE, background)
    for i in range(21) :
        pygame.draw.line(SCREEN,GRAY,(20,140+i*20),(420,140+i*20))
        pygame.draw.line(SCREEN,GRAY,(20+i*20,140),(20+i*20,540))
    
def draw_block(screen, color, position):
    """position 위치에 color 색깔의 블록을 그린다"""
    block = pygame.Rect((position[1] * BLOCK_SIZE, position[0] * BLOCK_SIZE),(BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(SCREEN, color, block)
   
def draw_score(score) :
    
    score_img= scorefont.render("now score : {}".format(game_board.score),True,(0,255,0))
    SCREEN.blit(score_img,(20,20))
    pygame.display.flip()

scorefont=pygame.font.SysFont(None, 30)
SCREEN = pygame.display.set_mode((BACK_W,BACK_H))
SCREEN.fill((0,34,80))

class Snake:
    """뱀 클래스"""
    color =GREEN #뱀의 색

    def __init__(self):
        self.positions=[(12,6),(12,7),(12,8),(12,9)]#뱀의 위치
        self.direction ='north' #뱀의 방향

    def draw(self,screen):
        """뱀을 화면에 그린다"""
        for i in range(0,len(self.positions)):  # 뱀의 몸 블록들을 순회하며
            c = (0,255-(5*i),0) #그라데이션 넣어야지 예쁘게
            draw_block(screen, c, self.positions[i])  # 각 블록을 그린다

    def crawl(self):
        """뱀이 현재 방향으로 한 칸 기어간다."""
        head_position = self.positions[0]
        y, x = head_position
        if self.direction == 'north':
            self.positions = [(y - 1, x)] + self.positions[:-1]
        elif self.direction == 'south':
            self.positions = [(y + 1, x)] + self.positions[:-1]
        elif self.direction == 'west':
            self.positions = [(y, x - 1)] + self.positions[:-1]
        elif self.direction == 'east':
            self.positions = [(y, x + 1)] + self.positions[:-1]
    def grow(self):
        """뱀이 한 칸 자라나게 한다."""
        GAMESPEED.FPS += 0.5
        tail_position = self.positions[-1]
        y,x=tail_position
        if self.direction =='north':
            self.positions.append((y-1,x))
        elif self.direction =='south':
            self.positions.append((y+1,x))
        elif self.direction =='west':
            self.positions.append((y,x-1))
        elif self.direction =='east':
            self.positions.append((y,x+1))

    def turn(self,direction):
        """뱀의 방향을 바꾼다."""
        self.direction = direction

class Apple:
    """사과 클래스"""
    color =RED #사과의 색
    
    def __init__(self, position=(random.randint(0,19)+7, random.randint(0,19)+1)):
       self.position = position #사과의 위치

    def draw(self,screen):
        """사과를 화면에 그린다."""
        draw_block(screen, self.color, self.position)


class GameBoard:
    """게임판 클래스"""
    width=20 #게임판의 너비
    height =20 #게임판의 높이
    score=0
    def __init__(self):
        self.snake = Snake()
        self.apple = Apple()
    def draw(self,screen):
        """화면에 게임판의 구성요소를 그린다."""
        self.apple.draw(screen)
        self.snake.draw(screen)
        draw_score(self.score)
    def process_turn(self):
        """게임을 한 차례 진행한다."""
        self.snake.crawl()  # 뱀이 한 칸 기어간다.
        
        if self.snake.positions[0] in self.snake.positions[1:]:
            raise SnaekCollisionException()
        for i in range(1,22):
            if self.snake.positions[0] == (i+6,21): #서
                raise SnaekCollisionException()  # 뱀 충돌 예외를 일으킨다
            if self.snake.positions[0] == (27,i): #남
                raise SnaekCollisionException()  
            if self.snake.positions[0] == (i+6,0): #동
                raise SnaekCollisionException()  
            if self.snake.positions[0] == (6,i): #북
                raise SnaekCollisionException()

        if self.snake.positions[0] == self.apple.position:
            self.snake.grow()
            self.put_new_apple()
            SCREEN.fill((0,34,80))
            self.score+=1

         
        b_size = len(self.snake.positions) # 뱀의 사이즈를 측정
        if b_size > 400: #뱀 사이즈가 400을 넘을경우(게임판 크기 20x20)
            raise SnaekCollisionException() 

    def put_new_apple(self):
        """게임판에 새 사과를 놓는다"""  
        self.apple = Apple((random.randint(0,19)+7, random.randint(0,19)+1))
        for position in self.snake.positions:
            if self.apple.position == position:
               self.put_new_apple()
               break

class SnaekCollisionException(Exception):
    """뱀 충돌 예외"""
    pass
    
class GAMESPEED:
    FPS = 3.0
    CLOCK = pygame.time.Clock()






game_board=GameBoard()
game_speed = GAMESPEED


running =True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running=False
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key in DIRECTION_ON_KEY:
               game_board.snake.turn(DIRECTION_ON_KEY[event.key])
    
    
   
    
    pygame.display.update()
    try:
       game_board.process_turn()
       pygame.display.set_caption("Snake Game now score : {}".format(game_board.score))  
    except SnaekCollisionException:
         exit(0)
    game_speed.CLOCK.tick(game_speed.FPS)
    draw_background(SCREEN)
    game_board.draw(SCREEN)
    



