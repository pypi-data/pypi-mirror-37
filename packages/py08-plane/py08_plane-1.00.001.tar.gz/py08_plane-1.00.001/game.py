import pygame
from pygame.locals import *
from random import randint
import sys,math,os

# 定义窗口的分辨率
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 750

# 定义画面帧率
FRAME_RATE = 60

# 定义动画周期(帧数)
ANIMATE_CYCLE = 30

pygame.init()
pygame.display.init()
pygame.display.set_caption("飞机大战")

# 开始界面用到的图片
startImgs = [
    pygame.image.load("plane/image1/stageBg.jpg"),
    pygame.transform.scale(pygame.image.load("plane/image/loading.png"),(480,480)),
    pygame.image.load("plane/image1/LOGO.png"),
    pygame.image.load("plane/image1/start_menu.png")
]
# 开始界面 底部三张图
startBottomImgs = [
    pygame.image.load("plane/image1/stageBossClass0.png"),
    pygame.image.load("plane/image1/stageBossClass1.png"),
    pygame.image.load("plane/image1/stageBossClass2.png")
]

# 开始界面类【图片，屏幕】
class StartPanel:
    def __init__(self,startImgs,startBottomImgs,screen):
        self.startImgs = startImgs
        self.startBottomImgs = startBottomImgs
        self.screen = screen

        self.nameY = 0  # 浮动图片的sin()
        self.bottomIndex = 0 # 底部图片 索引
        self.times = 0 # 计数
        self.isRect = False # 鼠标 是否 在按钮里

    def Show(self):
        # 渲染背景
        self.screen.blit(self.startImgs[0],(0,0))
        # 渲染圆环
        self.screen.blit(self.startImgs[1],(0,120))
        # 渲染 浮动 标题
        self.nameY += 0.05
        self.screen.blit(self.startImgs[2],((SCREEN_WIDTH - self.startImgs[2].get_width())//2,90+80*math.sin(self.nameY)))
        # 渲染按钮
        self.screen.blit(self.startImgs[3],((SCREEN_WIDTH - self.startImgs[3].get_width())//2,350))

        # 渲染底部三张图片
        self.times += 1
        if self.bottomIndex == 3: # 当显示到第三张图片时，
            self.bottomIndex = 0  # 继续重新从第一张开始，实现循环出现
        self.screen.blit(self.startBottomImgs[self.bottomIndex],((SCREEN_WIDTH - self.startBottomImgs[self.bottomIndex].get_width())//2,600))
        if self.times%17 == 0:    # 每17帧换下一张图片
            self.times = 0        # 重新计数
            self.bottomIndex += 1 # 换下一张

# 背景类
class BackGround:
    def __init__(self,image,screen,speed):
        self.screen = screen
        self.image1 = image
        self.rect1 = self.image1.get_rect()
        self.image2 = self.image1.copy()  # 复制一张新的图像
        self.rect2 = self.image2.get_rect()
        self.rect2.topleft = (0,-self.rect1.h)
        self.speed =speed
    # 移动
    def Move(self):
        # 矩形移动
        self.rect1 = self.rect1.move(0,self.speed)
        self.rect2 = self.rect2.move(0,self.speed)
        # 交替
        if self.rect1.y > SCREEN_HEIGHT+10:
            self.rect1.y = -self.rect1.h+self.rect2.y
        if self.rect2.y > SCREEN_HEIGHT+10:
            self.rect2.y = -self.rect1.h + self.rect1.y
        # 渲染图像
        self.screen.blit(self.image1,self.rect1)
        self.screen.blit(self.image2, self.rect2)

# 玩家图片
heroImgs = [
    pygame.image.load("plane/image1/me0.png"),
    pygame.image.load("plane/image1/me0.1.png")
]
heroDeathImgs = [
    pygame.image.load("plane/image/hero_blowup_n1.png"),
    pygame.image.load("plane/image/hero_blowup_n2.png"),
    pygame.image.load("plane/image/hero_blowup_n3.png"),
    pygame.image.load("plane/image/hero_blowup_n4.png")
]
# 玩家开始的位置
hero_pos = [200, 600]
# 玩家位置的控制字典
offset = {pygame.K_LEFT: False, pygame.K_RIGHT: False, pygame.K_UP: False, pygame.K_DOWN: False}
# 玩家类
 #属性： 图片，位置，屏幕，速度，血量 ，分数
class Hero(pygame.sprite.Sprite):
    hero_down_index = 0
    def __init__(self,heroImgs, hero_init_pos,screen,speed,hp,score):
        pygame.sprite.Sprite.__init__(self)
        self.images = heroImgs
        self.image = heroImgs[0]
        # 获得图片的矩形对象
        self.rect = self.image.get_rect()
        # 设置玩家对象的初始位置
        self.rect.topleft = hero_init_pos
        self.screen = screen
        self.speed = speed
        self.hp = hp
        self.init_pos = hero_init_pos
        self.score = score

        self.i = 0
        self.deathimgsIndex = 0
        # 子弹1 的Group
        self.bullets1 = pygame.sprite.Group()
    '''# 方法： 射击，移动 ， 碰撞 ，死亡'''
    # 射击
    def Shoot(self,bulletImg,speed):
        # 产生一个子弹对象 并添加到Group中
        Sounds.PlaySound(1).set_volume(1)
        bullet1 = Bullet(bulletImg,(self.rect.midtop[0]-25,self.rect.midtop[1]),speed)
        self.bullets1.add(bullet1)
        bullet2 = Bullet(bulletImg, self.rect.midtop, speed)
        self.bullets1.add(bullet2)
        bullet3 = Bullet(bulletImg, (self.rect.midtop[0]+25,self.rect.midtop[1]), speed)
        self.bullets1.add(bullet3)

    # 移动
    def Move(self,offset,ticks):
        # 渲染 并 交替出现图片
        if self.hp > 0:
            Sounds.PlaySound(2).set_volume(0.1)
            self.image = self.images[ticks // (ANIMATE_CYCLE // 2)]
            self.screen.blit(self.image, self.rect)

            if offset[pygame.K_LEFT]:
                self.rect = self.rect.move(-self.speed,0)
            if offset[pygame.K_RIGHT]:
                self.rect = self.rect.move(self.speed,0)
            if offset[pygame.K_DOWN]:
                self.rect = self.rect.move(0,self.speed)
            if offset[pygame.K_UP]:
                self.rect = self.rect.move(0,-self.speed)

            # 约束区间
            if self.rect.x <= 0:
                self.rect.x = 0
            elif self.rect.x > SCREEN_WIDTH - self.rect.w:
                self.rect.x = SCREEN_WIDTH - self.rect.w

            if self.rect.y <= 0:
                self.rect.y = 0
            elif self.rect.y > SCREEN_HEIGHT - self.rect.h:
                self.rect.y = SCREEN_HEIGHT - self.rect.h

            self.Collide(ticks)
        else:
            self.Death()

    # 碰撞
    def Collide(self,ticks):
        temp = pygame.sprite.spritecollideany(self, enemy_group, collided=pygame.sprite.collide_mask)
        if temp != None:
            # 测试Group 是否包含self
            # 敌机 主角 减血
            temp.hp -= 1
            self.hp -= 1
            # 主角回到原始位置
            if self.hp != 0:
                self.rect.topleft = self.init_pos
    # 死亡
    def Death(self):
        global isPlay
        self.i += 1
        Sounds.PlaySound(4).set_volume(0.5)
        # 不能立刻消失 改变当前主角的状态
        self.image = heroDeathImgs[self.deathimgsIndex]
        # self.screen.blit(self.imgs[self.imgsIndex],self.rect)
        if self.i % 7 == 0:
            self.i = 0
            self.deathimgsIndex += 1
            if self.deathimgsIndex == len(heroDeathImgs):
                self.deathimgsIndex = 0
                Font.UpdateHistory(self.score)
                self.score = 0 # 分数归零
                self.hp = 3    # 血量还原
                pygame.time.wait(200)
                self.kill()
                isPlay = False

# 子弹图片
bulletImgs = [
    pygame.image.load("plane/image1/bullet0_1.png"),
    pygame.image.load("plane/image1/bullet1_1.png"),
    pygame.image.load("plane/image1/bullet1_1.png")
]
# 子弹类
class Bullet(pygame.sprite.Sprite):
    # 属性： 图片，位置，屏幕，速度，
    def __init__(self,image,bullet_init_pos,speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.rect.center = bullet_init_pos
        self.screen = screen
        self.speed = speed

    # 方法： 移动 ， 碰撞 ，
    # 跟新 子弹 重写父类方法
    def update(self):
        # 移动 并 渲染
        self.rect = self.rect.move(0,-self.speed)
        # self.screen.blit(self.image,self.rect)
        # 超出画面 销毁子弹
        if self.rect.y - self.rect.h < 0:
            self.kill()

        self.Collide()

    # 碰撞
    def Collide(self):
        temp = pygame.sprite.spritecollideany(self,enemy_group,collided=pygame.sprite.collide_mask)
        if temp != None:
            # 测试Group 是否包含self
            if hero.bullets1.has(self):
                hero.bullets1.remove(self)
            if enemy_group.has(temp):
                temp.hp -= 1

# 敌机图片
enemy1 = [
    pygame.image.load("plane/image/e1.png"),
    pygame.image.load("plane/image/e1_down1.png"),
    pygame.image.load("plane/image/e1_down2.png"),
    pygame.image.load("plane/image/e1_down3.png"),
    pygame.image.load("plane/image/e1_down4.png"),
]
enemy2=[
    pygame.image.load("plane/image/e2.png"),
    pygame.image.load("plane/image/e2_down1.png"),
    pygame.image.load("plane/image/e2_down2.png"),
    pygame.image.load("plane/image/e2_down3.png"),
    pygame.image.load("plane/image/e2_down4.png"),

]
enemy3=[
    pygame.image.load("plane/image/enemy0_0.png"),
    pygame.image.load("plane/image/enemy1_20.png"),
    pygame.image.load("plane/image/enemy1_21.png"),
    pygame.image.load("plane/image/enemy1_22.png"),
    pygame.image.load("plane/image/enemy1_23.png"),
    pygame.image.load("plane/image/enemy1_24.png")
]
# 创建一个敌机Group
enemy_group = pygame.sprite.Group()
# 敌机类
class Enemy(pygame.sprite.Sprite):
    # 属性： 图片，位置，屏幕，速度，血量,标签
    def __init__(self,enemyImgs, enemy_init_pos,screen,speed,hp,tag):
        pygame.sprite.Sprite.__init__(self)
        self.imgs = enemyImgs
        self.image = enemyImgs[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = enemy_init_pos
        self.screen = screen
        self.speed = speed
        self.hp = hp
        self.tag = tag
        self.i = 0
        self.imgsIndex = 1
        enemy_group.add(self)

    # 移动 并 更新 Group
    def update(self):
        # hp 不为 0
        if self.hp > 0:
            self.rect = self.rect.move(0,self.speed)
            # self.screen.blit(self.image,self.rect)
            if self.rect.y >= SCREEN_HEIGHT:
                self.kill()
        else:
            self.Death()
    # 碰撞
    def Collide(self):
        pass
    # 死亡
    def Death(self):
        self.i += 1
        # 不能立刻消失 改变当前敌机的状态
        self.image = self.imgs[self.imgsIndex]
        # self.screen.blit(self.imgs[self.imgsIndex],self.rect)
        if self.i%5 == 0:
            self.i = 0
            self.imgsIndex += 1
            Sounds.PlaySound(3).set_volume(0.5)
            if enemy_group.has(self) and self.imgsIndex == len(self.imgs):
                if self.tag == "enemy1":
                    hero.score += 1
                elif self.tag == "enemy2":
                    hero.score += 3
                else:
                    hero.score += 10
                enemy_group.remove(self)
    # 创建敌机对象【随机】
    @staticmethod
    def RandomCreateEnemy(screen,ticks):
        if ticks%30 == 0:
            randNum = randint(1,100)
            if randNum <= 70:
                Enemy(enemy1,(randint(0,SCREEN_WIDTH-enemy1[0].get_rect().w),-enemy1[0].get_rect().h),screen,5,3,"enemy1")
            elif randNum <= 90:
                Enemy(enemy2,(randint(0, SCREEN_WIDTH - enemy2[0].get_rect().w), -enemy2[0].get_rect().h),screen, 3, 7,"enemy2")
            else:
                Enemy(enemy3,(randint(0, SCREEN_WIDTH - enemy3[0].get_rect().w), -enemy3[0].get_rect().h),screen,1, 10,"enemy3")

# 音效列表
sounds = [
    pygame.mixer.Sound("plane/sound/button.ogg"),
    pygame.mixer.Sound("plane/sound/bullet.wav"),
    pygame.mixer.Sound("plane/sound/big_spaceship_flying.ogg"),
    pygame.mixer.Sound("plane/sound/enemy1_down.ogg"),
    pygame.mixer.Sound("plane/sound/use_bomb.ogg")
]
# 音效类
class Sounds:
    @staticmethod
    def PlaySound(num,loop = 0):
        sounds[num].play(loops=loop)
        return sounds[num]

# 字体类
class Font:
    # 历史成绩
    history = 0
    def __init__(self,font,size,screen):
        self.font = font
        self.size = size
        self.screen = screen

    def Show(self,pos,content):
        # 创建字体
        tempFont = pygame.font.Font(self.font,self.size)
        # 将文本 转为 surface
        fontSurface = tempFont.render(content,True,pygame.Color("black"))
        # 渲染
        self.screen.blit(fontSurface,pos)

    # 更新screen 上的历史成绩
    @staticmethod
    def StartUpdateHistory(path = "score.txt"):
        if os.path.exists(path):
            with open(path,'r') as f_r:
                Font.history = int(f_r.read())

        else:
            with open(path,'w') as f_w:
                f_w.write("0")
                Font.history = 0

    # 更新历史成绩
    @staticmethod
    def UpdateHistory(score,path = "score.txt"):
        if score > Font.history:
            # 更新
            with open(path,'w') as f_w:
                f_w.write(str(score))
# 背景音乐
pygame.mixer.music.load("plane/sound/game_music.ogg")
pygame.mixer.music.play(-1)
#添加时间控制
clock = pygame.time.Clock()
# 设置窗口
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
# 创建开始界面对象
startPanel = StartPanel(startImgs,startBottomImgs,screen)

# 设置背景的初始位置
# 创建背景类
backGround = BackGround(pygame.image.load("plane/image1/background2.jpg"),screen,2)

# 创建玩家对象
hero = Hero(heroImgs,hero_pos,screen,6,3,0)

# 创建字体对象
font = Font("plane/font/Marker Felt.ttf",30,screen)

# 全局变量 是否开始游戏
isPlay = False
# 计数
ticks = 0
def Event():
    global isPlay
    # 退出事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # 开始游戏
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # 判断鼠标是否在按钮里
                startPanel.isInRect = pygame.Rect(210, 350, 72, 72).collidepoint(pygame.mouse.get_pos())
                if startPanel.isInRect:
                    print("开始游戏")
                    Sounds.PlaySound(0)
                    Font.StartUpdateHistory() # 更新历史成绩
                    enemy_group.empty()   # 清空Group
                    hero.bullets1.empty() # # 清空Group
                    hero.rect.topleft = hero_pos
                    isPlay = True

        # 返回开始界面
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isPlay = False
            if event.key in offset:
                offset[event.key] = True

        if event.type == pygame.KEYUP:
            if event.key in offset:
                offset[event.key] = False

def Main():
    global isPlay
    global ticks
    while True:
         # 控制游戏的最大帧率
        clock.tick(FRAME_RATE)
        # 控制玩家图片的交替
        if ticks >= ANIMATE_CYCLE:
             ticks = 0
        # 处理所有时间
        Event()
        # 控制游戏是否开始
        if isPlay == False:
            # 开始界面
            startPanel.Show()
        else:
            # 背景移动
            backGround.Move()
            # 玩家移动
            hero.Move(offset,ticks)
            # 控制子弹的射击频率
            if ticks%10 == 0:
                hero.Shoot(bulletImgs[1],8)
            # 更新 Group
            hero.bullets1.update()
            # 将Group 绘制到screen上
            hero.bullets1.draw(screen)
            # 创建敌机
            Enemy.RandomCreateEnemy(screen,ticks)
            # 更新 enemy Group
            enemy_group.update()
            # 将 enemy Group 绘制到screen上
            enemy_group.draw(screen)

            # 显示字体
            font.Show((10,10),"HP:%s"%hero.hp)
            font.Show((10, 40), "Score:%s" % hero.score)
            font.Show((10, 70), "History:%s" % Font.history)

        # 计数
        ticks += 1
        # 刷新 屏幕
        pygame.display.update()


if __name__ == '__main__':
    Main()






















