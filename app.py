import pygame, sys, math, random, time
from pygame.locals import *
from datetime import datetime
from pygame import mixer
from pygame.draw import rect

# 1. 게임 초기화
pygame.init()
playgameover = True # 게임오버사운드 한번만 재생하기 위한 메인루프에 playgameover값 True설정
playwin = True


clock = pygame.time.Clock()
while pygame.mixer.get_busy():
    clock.tick(10)
    pygame.event.poll()

# 2. 게임 창 옵션 설정
size = [800, 800]
screen = pygame.display.set_mode(size)

# 3. 게임 이름 설정
title = "AttaBooi"
pygame.display.set_caption(title)
favicon = pygame.image.load("data/images/title.png")     #favicon 설정
pygame.display.set_icon(favicon)

# 4. 게임 내 필요한 설정
clock = pygame.time.Clock()    #시간변수 생성


class obj():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.move = 0           # 객체에 좌표와 속도개념 붙이기

    def put_img(self, address):
        if address[-3:] == "png":  # address 값의 마지막 3글자가 png일 경우. [-3:]으로표현
            self.img = pygame.image.load(address).convert_alpha()
        else:
            self.img = pygame.image.load(address)
            self.sx, self.sy = self.img.get_size()

    def change_size(self, sx, sy):
        self.img = pygame.transform.scale(self.img, (sx, sy))  # 이미지 크기 받아오는 함수
        self.sx, self.sy = self.img.get_size()

    def show(self):
        screen.blit(self.img, (self.x, self.y))

class Mario():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.move = 0
        self.isJump = False            # 점프 기능 만들기, 디폴트값은 점프 중이 아니다
        self.jumpCount = 10
    def jump(self):
        if self.isJump:
            if self.jumpCount >= -10:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y -= self.jumpCount ** 2 * 0.1 * neg         # 점프 속도 및 크기
                self.jumpCount -= 1   # 하강
            else:
                self.isJump = False
                self.jumpCount = 10

    def put_img(self, address):
        if address[-3:] == "png":  # address 값의 마지막 3글자가 png일 경우. [-3:]으로표현
            self.img = pygame.image.load(address).convert_alpha()
        else:
            self.img = pygame.image.load(address)
            self.sx, self.sy = self.img.get_size()

    def change_size(self, sx, sy):
        self.img = pygame.transform.scale(self.img, (sx, sy))  # 이미지 크기 받아오는 함수
        self.sx, self.sy = self.img.get_size()

    def show(self):
        screen.blit(self.img, (self.x, self.y))

def crash(a, b):
    if (a.x - b.sx <= b.x) and (b.x <= a.x + a.sx):
        if (a.y - b.sy <= b.y) and (b.y <= a.y + a.sy):
            return True
        else:
            return False
    else:
        return False

def pause():                # 일시정지 기능 만들기

    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:         #마우스 버튼 클릭시 다시 시작
                    paused = False


        font1 = pygame.font.Font("data/font/AGENCYB.TTF", 100)
        text_paused = font1.render("Paused", True, (0, 0, 0))
        screen.blit(text_paused, (size[0] / 2 - 130, round(size[1] / 2 - 100)))

        font2 = pygame.font.Font("data/font/AGENCYB.TTF", 50)
        text_paused = font2.render("continue to click", True, (0, 0, 0))
        screen.blit(text_paused, (size[0] / 2 - 150, round(size[1] / 2 )))

        pygame.display.update()
        clock.tick(5)





left_go = False
right_go = False
space_go = False

kill = 0
loss = 0

shots_list = []  # 미사일이 화면 밖으로 나갔을때 데이터를 지워주기
b_list = []
f_list = [] # 꽃 리스트
m_list = []
a_list = []

black = (0, 0, 0)
white = (255, 255, 255)
k = 0
GO = 0

# 사운드
bgm = pygame.mixer.Sound("data/sound/Mario World 1.mp3")
bgm.play(-1).set_volume(0.05)

# 5-0. 게임 시작 대기 화면
SB = 0
player = Mario()

if SB == 0:
    player.put_img("data/images/1111.png")
    player.change_size(50, 50)
    player.x = round(size[0] / 2 - player.sx / 2)
    player.y = round(size[1] - player.sy - 15)
    player.move = 13

while SB == 0:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                SB = 1
    screen.fill(white)
    font = pygame.font.Font("data/font/AGENCYB.TTF", 30)
    text = font.render("PRESS SPACE KEY TO START THE GAME", True, (0, 0, 0))
    screen.blit(text, (size[0] / 2 - 200, round(size[1] / 2 - 50)))
    pygame.display.flip()

# 5. 메인 이벤트
start_time = datetime.now()
SB = 0
while SB == 0:
    player.jump()

    # FPS 설정
    clock.tick(60)  # 1초에 while문이 60번 실행된다

    # 각종 입력 감지
    for event in pygame.event.get():  # 게임에서 행해지는 이벤트
        if event.type == pygame.QUIT:
            SB = 1
        if event.type == pygame.KEYDOWN:  # 키가 눌렸을떄
            if event.key == pygame.K_LEFT:  # 눌렸을때 그 눌린키가 왼쪽일때
                left_go = True
            elif event.key == pygame.K_RIGHT:  # 눌렸을떄 그 눌린키가 오른쪽일때
                right_go = True
            elif event.key == pygame.K_SPACE:
                player.isJump = True
                space_go = True
                k = 0  # 스페이스를 눌렀을때마다 k를 0으로 만들어서 누를때마다 나가게 만들기(프레임이 6으로 안나누어져도)
            elif event.key == pygame.K_p:
                pause()
        elif event.type == pygame.KEYUP:  # 키를 뗏을떄
            if event.key == pygame.K_LEFT:
                left_go = False
            elif event.key == pygame.K_RIGHT:
                right_go = False
            elif event.key == pygame.K_SPACE:
                space_go = False

    #### 입력, 시간에 따른 변화
    now_time = datetime.now()  ### 시간정보
    delta_time = round((now_time - start_time).total_seconds())

    if left_go == True:
        player.x -= player.move  # 이동속도만큼 왼쪽 이동
        if player.x <= 0:  # 맵 끝의 crash개념을 추가, 위치가 0일떄 0에 고정
            player.x = 0

    elif right_go == True:
        player.x += player.move
        if player.x >= size[0] - player.sx:  # 맵 끝의 crash개념 추가, 위치가 우측 끝(screen x축값에 player size를 빼준것
            player.x = size[0] - player.sx

    if space_go == True and k % 6 == 0:  # 총알이 나가는 게 너무 빨라서 fps/6 의 속도로 나가게 함
        shot = obj()
        shot.put_img("data/images/fire.png")
        shot.change_size(10, 10)
        shot.x = round(player.x + player.sx / 2 - shot.sx / 2)
        shot.y = player.y - shot.sy - 10
        shot.move = 15
        shots_list.append(shot)

    k += 1

    d_list = []
    for i in range(len(shots_list)):  # 미사일이 발생하는 것
        shots = shots_list[i]
        shots.y -= shots.move  # 미사일 속도만큼 위로
        if shots.y <= - shots.sy:  # 화면 밖으로나갔을떄
            d_list.append(i)  # d_list에 추가해라
    for d in d_list:
        del shots_list[d]  # d_list 삭제


    score = kill - loss         # score 개념 추가하기
    if score >= 500:    # 게임 승리 조건
        SB = 2

    life = (5 - loss)           # player의 life 개념 만들기
    if life == 0:
        SB = 1
        GO = 1

    # boo 생성함수

    if random.random() > 0.98 and score >= -2:
        boo = obj()
        boo.put_img("data/images/boo.png")
        boo.change_size(40, 40)
        boo.x = random.randrange(0, size[0] - boo.sx - round(player.sx) / 2)
        boo.y = 10
        boo.move = 6
        b_list.append(boo)

    elif random.random() > 0.98 and score >= 15:
        booo = obj()
        booo.put_img("data/images/booo.png")
        booo.change_size(50, 50)
        booo.x = random.randrange(0, size[0] - booo.sx - round(player.sx) / 2)
        booo.y = 10
        booo.move = 10
        b_list.append(booo)
        angry = pygame.mixer.Sound("data/Sound/Super Mario Fireball.mp3")
        angry.play(loops=0).set_volume(0.05)


    d_list = []
    for i in range(len(b_list)):  # boo가 화면 밖으로 나갔을때 없애주는 코드
        b = b_list[i]
        b.y += b.move
        if b.y >= size[1]:
            d_list.append(i)
    for d in d_list:
        del b_list[d]
        loss += 1
        ouch = pygame.mixer.Sound("data/Sound/wwoods-snes_cpu5.wav")
        ouch.play(loops=0).set_volume(0.05)


    # 충돌개념
    dm_list = []
    da_list = []
    for i in range(len(shots_list)):
        for j in range(len(b_list)):
            shots = shots_list[i]
            b = b_list[j]
            if crash(shots, b) == True:
                dm_list.append(i)
                da_list.append(j)
    dm_list = list(set(dm_list))  # dm_list의 중복을 제거한다. 제거됐을땐 set자료형이기 때문에 list로 다시 바꿔준다.
    da_list = list(set(da_list))

    for dm in dm_list:
        del shots_list[dm]
    for da in da_list:
        del b_list[da]
        kill += 1
        coin = pygame.mixer.Sound("data/Sound/Mario Coin.mp3")
        coin.play(loops=0).set_volume(0.05)

    for i in range(len(b_list)):
        b = b_list[i]
        if crash(b, player) == True:
            SB = 1
            GO = 1




    ##### 그리기
    screen.fill(white)
    player.show()

    font = pygame.font.Font("data/font/AGENCYB.TTF", 300)  ##score 나타내기    #### 폰트 출력 순서에 따라 덮어씌우는 순서가 정해짐
    text_score = font.render("{}".format(score), True, (200, 200, 200))
    screen.blit(text_score, (310, 200))

    for s in shots_list:
        s.show()
    for b in b_list:
        b.show()

    # 문자
    font = pygame.font.Font("data/font/AGENCYB.TTF", 50)  ##kill, loss 나타내기
    text_kill = font.render("hp : {}".format(life), True, (255, 200, 0))
    screen.blit(text_kill, (10, 5))

    font3 = pygame.font.Font("data/font/AGENCYB.TTF", 50)
    text_time = font3.render("time : {}".format(delta_time), True, (0, 0, 0))  ##time나타내기기
    screen.blit(text_time, (size[0] - 150, 5))

    highscore_value = open("data/serialisation/highscore.csv", "r").readline()
    text_highscore = font.render("Highscore: {}".format(highscore_value), True, (150, 200, 255))
    screen.blit(text_highscore, (size[0] - 530, 5))

    ##### 업데이트
    pygame.display.flip()

##### 게임종료

while SB == 2:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GO = 0
    if playwin:
        bgm.stop()
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('data/sound/wwoods-snes_cpu4.wav'))
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('data/sound/smw_bonus_game_end.wav'))
        playwin = False

    font = pygame.font.Font("data/font/AGENCYB.TTF", 70)
    text = font.render("YOU WIN !", True, (100, 255, 100))
    screen.blit(text, (size[0] / 2 - 130, round(size[1] / 2 - 50)))
    pygame.display.flip()
    time.sleep(5)                  # 게임 승리시 collision 나는 것을 그냥 5초후 break로 빠져나오게 함.
    break

while GO == 1:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GO = 0

    if playgameover:  ##게임오버시 사운드 한번만 재생되게 하는법.
        bgm.stop()
        gs = pygame.mixer.Sound("data/sound/smw_lost_a_life.wav")
        gs.play(loops=0)
        playgameover = False

    font = pygame.font.Font("data/font/AGENCYB.TTF", 70)
    text = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(text, (size[0] / 2 - 130, round(size[1] / 2 - 50)))
    pygame.display.flip()

if SB != 0 or GO ==1:
    old_highscore_value = open("data/serialisation/highscore.csv", "r").readline()          # highscore를 따로 액셀파일에 저장하고 출력하는 방식으로 구현
    try:
        if score > int(old_highscore_value):
            highscore_value = open("data/serialisation/highscore.csv", "w")
            highscore_value.write(str(score))
            highscore_value.close()
    except:
        pass




pygame.quit()
