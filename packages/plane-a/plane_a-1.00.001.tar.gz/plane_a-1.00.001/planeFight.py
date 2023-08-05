import pygame
import sys
import math
import random
import os

# 初始化
pygame.init()
pygame.display.init()
# 建立窗口
screen = pygame.display.set_mode((480, 710))
# 把图片存到列表中待用：
startBackImg = [pygame.image.load("sources/background.png"),
                pygame.image.load("sources/loading.png"),
                pygame.image.load("sources/name.png")]
startBottomImg = [pygame.image.load("sources/game_loading1.png"),
                  pygame.image.load("sources/game_loading2.png"),
                  pygame.image.load("sources/game_loading3.png")]
startCenterImg = [pygame.image.load("sources/hero1.png"), pygame.image.load("sources/hero2.png")]
playBackImages = pygame.image.load("sources/background.png")
heroImages = [pygame.image.load("sources/hero1.png"), pygame.image.load("sources/hero2.png")]
isPlay = False
bulletList = []
bulletImage = pygame.image.load("sources/bullet2.png")
enemy1 = [pygame.image.load("sources/enemy1.png"), pygame.image.load("sources/enemy1_down1.png"),
          pygame.image.load("sources/enemy1_down2.png"), pygame.image.load("sources/enemy1_down3.png"),
          pygame.image.load("sources/enemy1_down4.png")]
enemy2 = [pygame.image.load("sources/enemy2.png"), pygame.image.load("sources/enemy2_down1.png"),
          pygame.image.load("sources/enemy2_down2.png"), pygame.image.load("sources/enemy2_down3.png"),
          pygame.image.load("sources/enemy2_down4.png")]
enemy0 = [pygame.image.load("sources/enemy0.png"), pygame.image.load("sources/enemy0_down1.png"),
          pygame.image.load("sources/enemy0_down2.png"), pygame.image.load("sources/enemy0_down3.png"),
          pygame.image.load("sources/enemy0_down4.png")]
heroDeathImgs = [pygame.image.load("sources/hero_blowup_n1.png"), pygame.image.load("sources/hero_blowup_n2.png"),
                 pygame.image.load("sources/hero_blowup_n3.png")]
enemyList = []

sounds = [
    pygame.mixer.Sound("sound/button.ogg"),
    pygame.mixer.Sound("sound/bullet.wav"),
    pygame.mixer.Sound("sound/enemy0_down.wav"),
    pygame.mixer.Sound("sound/use_bomb.ogg")
]

class startPanel:
    def __init__(self, startBackImg, startBottomImg, startCenterImg, screen):
        self.startBackImg = startBackImg
        self.startBottomImg = startBottomImg
        self.startCenterImg = startCenterImg
        self.screen = screen
        self.movingFactor = 0
        self.bottomIndex = 0
        self.i = 0
        self.centerIndex = 0
        # self.firstBg = 0
        # self.secondBg = self.firstBg - 852

    def startShow(self):  # 绘制startPanel
        self.screen.blit(self.startBackImg[0], (0, 0))
        self.movingFactor += 0.05
        self.screen.blit(self.startBackImg[1], (-15 + 10 * math.sin(self.movingFactor), 100))
        self.screen.blit(self.startBackImg[2], (25, 40 + 20 * math.sin(self.movingFactor)))
        # 底部三个图切换
        if self.bottomIndex == 3:
            self.bottomIndex = 0
        self.screen.blit(self.startBottomImg[self.bottomIndex], (150, 600))
        # 中间两个图切换
        if self.centerIndex == 2:
            self.centerIndex = 0
        self.screen.blit(self.startCenterImg[self.centerIndex], (190, 300))
        if self.i % 14 == 0:
            self.bottomIndex += 1
            self.centerIndex += 1
        self.i += 1

    # def playShow(self):
    #     self.screen.blit(self.startBackImg[0], (0, self.firstBg))
    #     self.screen.blit(self.startBackImg[0], (0, self.secondBg))
    #     self.firstBg += 1
    #     if self.firstBg


class playBackPanel:
    def __init__(self, backImages, screen, speed):  # 背景图片组，显示的母窗口，背景运动的速度
        self.backImage1 = backImages
        self.backImage2 = backImages.copy()
        self.screen = screen
        self.speed = speed
        self.rect1 = self.backImage1.get_rect()  # 把两个图片转化成对应的rect，以便后面的方法调用rect中的move方法
        self.rect2 = self.backImage2.get_rect()
        self.rect1.topleft = (0, 0)  # 初始化要显示的图片的位置
        self.rect2.topleft = (0, -852)  # 初始化上方图片的位置
        # self.firstBg = 0
        # self.secondBg = self.firstBg - 852

    def Show(self):  # 需要用到rect中自带的move方法,因为用的是向上的运动方向，故self.speed应为负值
        self.rect1 = self.rect1.move(0, self.speed)
        self.rect2 = self.rect2.move(0, self.speed)
        if self.rect1.y >= 720:
            self.rect1.y = self.rect2.y - 852
        if self.rect2.y >= 720:
            self.rect2.y = self.rect1.y - 852
        self.screen.blit(self.backImage1, self.rect1)
        self.screen.blit(self.backImage2, self.rect2)


class heroPlane(pygame.sprite.Sprite):
    up = False
    down = False
    left = False
    right = False

    def __init__(self, heroImages, screen, speed, hp, score):
        self.heroImages = heroImages
        self.hp = hp
        self.image = heroImages[0]
        self.rect = self.image.get_rect()  # 要调用move,故创建矩形对象
        self.rect.topleft = (190, 560)
        self.screen = screen
        self.speed = speed
        self.heroImagesIndex = 0
        self.deathImgIndex = 0
        self.isProtect = False
        self.reBirth = 0
        self.score = score
        self.i = 0  # 用来实现动图效果的因数
        self.bulletSound = AllSounds.PlaySound(1, -1)
        self.bulletSound.set_volume(0)

    def Move(self):
        if self.hp > 0:
            if heroPlane.down:  # 把heroPlane将要显示在的rect进行移动
                self.rect = self.rect.move(0, self.speed)
                # print(1)
            if heroPlane.up:
                self.rect = self.rect.move(0, -self.speed)
                # print(2)
            if heroPlane.left:
                self.rect = self.rect.move(-self.speed, 0)
            if heroPlane.right:
                self.rect = self.rect.move(self.speed, 0)

            if self.rect.x <= -45:  # 限制范围
                self.rect.x = -45
            if self.rect.x >= 425:
                self.rect.x = 425
            if self.rect.y <= 0:
                self.rect.y = 0
            if self.rect.y >= 590:
                self.rect.y = 590

            self.i += 1
            if self.i % 7 == 0:
                self.heroImagesIndex += 1
            if self.i % 5 == 0:  # 控制子弹发射速度
                Bullet(bulletImage, self.screen, 7, pos=self.rect.midtop)
            if self.heroImagesIndex == 2:
                self.heroImagesIndex = 0
            if self.isProtect == False:
                self.screen.blit(self.heroImages[self.heroImagesIndex], self.rect)  # 将heroPlane渲染在移动过的对应的heroRect中
            elif self.isProtect == True:
                self.speed = 20
                self.reBirth += 1
                if self.reBirth % 10 == 0:
                    self.screen.blit(self.heroImages[self.heroImagesIndex], self.rect)  # 将heroPlane渲染在移动过的对应的heroRect中
                if self.reBirth >= 200:
                    self.isProtect = False
            self.Collide()


        else:
            global isPlay
            self.i += 1
            self.screen.blit(heroDeathImgs[self.deathImgIndex], self.rect)
            if self.i % 7 == 0:
                self.i = 0
                self.deathImgIndex += 1
                if self.deathImgIndex == len(heroDeathImgs):
                    self.deathImgIndex = 0
                    enemyList.clear()
                    bulletList.clear()
                    FontDisplay.Update(self.score)
                    self.score = 0  # 分数归零
                    self.hp = 3  # 血量还原
                    self.isProtect = False
                    hero.rect.topleft = (190, 560)
                    pygame.time.wait(400)
                    isPlay = False  # 游戏结束，回到开始界面

    def Collide(self):
        global isPlay
        temp = pygame.sprite.spritecollideany(self, enemyList, collided=pygame.sprite.collide_mask)
        if temp != None:
            temp.hp = 0  # 敌机死亡
            self.hp -= 1  # 主角 减血
            enemyList.clear()
            if self.hp != 0:
                self.rect.topleft = (190, 560)  # 主角还原初始位置
                self.isProtect = True
                self.reBirth=0


class Bullet(pygame.sprite.Sprite):

    def __init__(self, image, screen, speed, pos):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.screen = screen
        self.speed = speed
        bulletList.append(self)

    def Fly(self):
        self.rect = self.rect.move(0, -self.speed)  # 对要显示子弹的bulletRect进行移动
        self.screen.blit(self.image, self.rect)

        if self.rect.y <= -20:  # 清除子弹的位置
            if self in bulletList:
                bulletList.remove(self)
        self.Collide()

    @staticmethod
    def AllButtetMove():
        for i in bulletList:
            if i != None and isinstance(i, Bullet):
                i.Fly()

        # 子弹碰撞敌机

    def Collide(self):
        temp = pygame.sprite.spritecollideany(self, enemyList, collided=pygame.sprite.collide_mask)
        # print(1)
        if temp != None:
            if self in bulletList:
                bulletList.remove(self)
                temp.hp -= 1


class Enemy(pygame.sprite.Sprite):
    CreateIndex = 0  # 用于产生敌机的变量

    def __init__(self, enemyImages, pos, screen, speed, hp, tag):
        self.screen = screen
        self.speed = speed
        self.hp = hp
        self.tag = tag
        self.enemyImages = enemyImages
        self.image = self.enemyImages[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.i = 0  # 计时 7帧播放一个画面
        self.imgsIndex = 0
        enemyList.append(self)

    def __str__(self):
        return "敌机"

    def Move(self):
        if self.hp > 0:
            self.rect = self.rect.move(0, self.speed)
            self.screen.blit(self.enemyImages[self.imgsIndex], self.rect)

            # 超过画面销毁敌机
            if self.rect.y >= 760:
                if self in enemyList:
                    enemyList.remove(self)
        else:
            self.Death()

    def Death(self):
        # 播放死亡动画
        self.i += 1
        self.screen.blit(self.enemyImages[self.imgsIndex], self.rect)
        if self.i % 10 == 0:
            self.i = 0
            self.imgsIndex += 1
            # 不能立马消失
            if self in enemyList and self.imgsIndex == len(self.enemyImages):  # 把飞机被毁的图片都显示完成
                AllSounds.PlaySound(2)
                if self.tag == "enemy1":
                    hero.score += 1
                elif self.tag == "enemy2":
                    hero.score += 3
                else:
                    hero.score += 10
                enemyList.remove(self)  # 图片都显示过之后，摧毁对象

    @staticmethod
    def RandomCreateEnemy(screen):

        Enemy.CreateIndex += 1
        if Enemy.CreateIndex % 100 == 0:
            Enemy.CreateIndex = 0
            randNum = random.randint(1, 100)
            if randNum <= 70:
                Enemy(enemy0, (random.randint(0, 429), -250), screen, 3, 1, "enemy1")
            elif randNum <= 90:
                Enemy(enemy1, (random.randint(0, 411), -250), screen, 2, 3, "enemy2")
            else:
                Enemy(enemy2, (random.randint(0, 315), -250), screen, 1, 10, "enemy3")

    @staticmethod
    def AllEnemyMove():
        for i in enemyList:
            if i != None and isinstance(i, Enemy):
                i.Move()

# 音效类
class AllSounds:
    @staticmethod
    def PlaySound(num, loop=0):
        sounds[num].play(loops=loop)
        return sounds[num]

def Listener():
    global isPlay
    for event in pygame.event.get():
        # 退出事件
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            startButton = pygame.Rect(190, 300, 100, 125)  # 获得开始按钮的位置
            if startButton.collidepoint(pygame.mouse.get_pos()):
                FontDisplay.StartUpateHistory()
                enemyList.clear()
                bulletList.clear()
                hero.rect.topleft = (200, 500)
                isPlay = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # 全屏爆炸
                for i in enemyList:
                    AllSounds.PlaySound(3)
                    i.hp = 0
            if event.key == pygame.K_ESCAPE:
                enemyList.clear()
                bulletList.clear()
                hero.rect.topleft = (190, 560)
                hero.hp = 3
                # heroPlane.score = 0
                isPlay = False
            if event.key == pygame.K_UP:
                heroPlane.up = True
            if event.key == pygame.K_DOWN:
                heroPlane.down = True
            if event.key == pygame.K_LEFT:
                heroPlane.left = True
            if event.key == pygame.K_RIGHT:
                heroPlane.right = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                heroPlane.up = False
            if event.key == pygame.K_DOWN:
                heroPlane.down = False
            if event.key == pygame.K_LEFT:
                heroPlane.left = False
            if event.key == pygame.K_RIGHT:
                heroPlane.right = False


playBack = playBackPanel(playBackImages, screen, 2)
hero = heroPlane(heroImages, screen, 5, 3, 0)


class FontDisplay:
    history = 0  # 历史成绩

    def __init__(self, font, size, screen):
        self.font = font
        self.size = size
        self.screen = screen

    def Show(self, pos, strA):
        tempFont = pygame.font.Font(self.font, self.size)  # 创建字体
        fontSurface = tempFont.render(strA, True, pygame.Color("black"))  # 将文本转为 surface
        self.screen.blit(fontSurface, pos)  # 渲染出来

    @staticmethod
    def StartUpateHistory(path="score.txt"):  # 每次开始都知道 历史成绩
        if os.path.exists(path):
            with open(path, "r") as f_r:
                FontDisplay.history = int(f_r.read())
        else:
            with open(path, "w") as f_w:
                f_w.write("0")
                FontDisplay.history = 0

    @staticmethod
    def Update(score, path="score.txt"):  # 更新历史成绩
        if score > FontDisplay.history:
            # 更新
            with open(path, "w") as f_w:
                f_w.write(str(score))


fontDisplay = FontDisplay("sources/segoesc.ttf", 25, screen)


def Main():
    global isPlay
    start = startPanel(startBackImg, startBottomImg, startCenterImg, screen)  # 创建窗口
    # bullet = Bullet(bulletImage, screen, 5)
    while True:
        Listener()
        if isPlay == False:
            start.startShow()  # 绘制start
        else:
            playBack.Show()  # 绘制运行界面
            hero.Move()
            Bullet.AllButtetMove()
            # bullet.Fly()  # 若这样进行则只有一颗子弹,故在飞机渲染的时候每一帧产生子弹
            Enemy.RandomCreateEnemy(screen)
            Enemy.AllEnemyMove()
            fontDisplay.Show((10, 10), "HP:%s" % hero.hp)
            fontDisplay.Show((10, 35), "Score:%s" % hero.score)
            fontDisplay.Show((10, 65), "History:%s" % FontDisplay.history)
        pygame.display.update()  # 更新窗口


if __name__ == '__main__':
    Main()
