import pygame

import random as r

import math,sys,time,os



# print(pygame.ver)

# 初始化pygame
pygame.init()

# 显示初始化pygame
pygame.display.init()

# 设置游戏开始窗口
screen=pygame.display.set_mode((480,750))

# 开始界面所需照片
startImgs=[
    pygame.image.load('plane/img_bg_level_2.jpg'),   #背景屏幕
    pygame.transform.scale(pygame.image.load('plane/image/loading.png'),(480,480)),   # 覆盖图画
    pygame.image.load('plane/image/name.png'),       # 字照片
    pygame.image.load('plane/openlet_peek.png'),    # 开始照片
    pygame.image.load('plane/bg_5_480x800.jpg')
]
# 底部动画照片导入
startBottomImgs=[
    pygame.image.load('plane/image/game_loading1.png'),
    pygame.image.load('plane/image/game_loading2.png'),
    pygame.image.load('plane/image/game_loading3.png')
]
# 开始界面类：
class startPanel:
    def __init__(self, startImgs, startBottomImgs, screen):
        self.startImgs = startImgs   # 开始界面图片
        self.startBottomImgs = startBottomImgs   # 底部三个动画
        self.screen = screen     # 背景屏幕
        self.bottomIndex = 0     # self.startBottomImgs(底部照片)的索引下标
        self.nameY = 0     # 字体浮动函数 sin()的变量
        self.i = 0           # 底部照片的帧数的初始值
        self.isInRect=False

    def Show(self):

        # 渲染背景
        self.screen.blit(self.startImgs[0],(0,0))     # 背景定义坐标

        # 渲染圆环
        self.screen.blit(self.startImgs[1], (0, 150))

        # 渲染浮动字体
        self.nameY+=0.05
        self.screen.blit(self.startImgs[2],\
                         (25, 100+50*math.sin(self.nameY)))
        # 渲染开始照片
        self.screen.blit(self.startImgs[3], (160,350))

        # 渲染底部三张照片
        self.i += 1
        if self.bottomIndex == 3:
            self.bottomIndex = 0     # 三张底图的索引
        self.screen.blit(self.startBottomImgs\
                             [self.bottomIndex],(150,630))
        if self.i % 17 == 0:      # 每个17个图画进入下一个画面
            self.bottomIndex += 1
            self.i = 0

# 游戏背景类：**************************

class BackGround:
    def __init__(self,img,screen,speed):
        self.img1=img    # 背景图片
        self.rect1=self.img1.get_rect()  # 获得背景1图的矩形区域
        self.img2=self.img1.copy()      # 复制一副新图
        self.rect2=self.img2.get_rect()   # 获得背景1图的矩形区域
        self.rect2.topleft=(0,-800)     # 替换的初始坐标
        self.screen=screen    # 背景屏幕
        self.speed=speed      # 背景速度
        self.isInRect = False

    # 方法： 移动*******

    def Move(self):
            # 背景移动：
        self.rect1=self.rect1.move(0,self.speed)     # 背景图沿x轴正方向运动
        self.rect2 = self.rect2.move(0, self.speed)

            # 两幅背景图交替：
        if self.rect1.y>=760:                # 1图的topleft坐标
            self.rect1.y=self.rect2.y-800    # 一图交替到二图后(0,self.rect2.y-852)的位置
        if self.rect2.y>=760:                # 2图的topleft坐标
            self.rect2.y = self.rect1.y - 800

            # 渲染交替背景图片
        self.screen.blit(self.img1,self.rect1)
        self.screen.blit(self.img2, self.rect2)

# 英雄图片导入：

heroImgs=[
    pygame.image.load("plane/image/hero1.png"),
    pygame.image.load("plane/image/hero2.png")
]
# 英雄死亡图片导入：

heroDeathImgs=[
    pygame.image.load("plane/image/hero_blowup_n1.png"),
    pygame.image.load("plane/image/hero_blowup_n2.png"),
    pygame.image.load("plane/image/hero_blowup_n3.png"),
    pygame.image.load("plane/image/hero_blowup_n4.png")
]

# 主角类:*************************************

class Hero(pygame.sprite.Sprite):
    up = False
    down = False
    left = False
    right = False

    def __init__(self, imgs, pos, screen, speed, hp, score):

        self.imgs = imgs
        self.image = imgs[0]                # 默认第一幅图
        self.rect = self.image.get_rect()   # 获得英雄图片的矩形对象
        self.rect.topleft = pos             # 设置初始位置
        self.pos=pos
        self.screen = screen
        self.speed = speed
        self.hp = hp
        self.score = score

        self.i = 0              # 计时：
        self.imgDisply = True   # 是否播放图片：
        self.deathImgIndex = 0  # 死亡图片索引

        self.bulletSound = AllSounds.PlaySound(1, -1)
        self.bulletSound.set_volume(0)

           # 方法：移动  碰撞  死亡
    def Move(self):

        global isPlay

        # 子弹音效声音
        if isPlay:
            self.bulletSound.set_volume(1)
        else:
            self.bulletSound.set_volume(0)

        if self.hp > 0:

            # 移动
            if Hero.down:
                self.rect = self.rect.move(0, self.speed)
            if Hero.up:
                self.rect = self.rect.move(0, -self.speed)
            if Hero.right:
                self.rect = self.rect.move(self.speed, 0)
            if Hero.left:
                self.rect = self.rect.move(-self.speed, 0)

            # 约束区间
            if self.rect.x <= 0:
                self.rect.x = 0
            if self.rect.x >= 380:
                self.rect.x = 380
            if self.rect.y <= 0:
                self.rect.y = 0
            if self.rect.y >= 625:
                self.rect.y = 625

            # 切换喷气图片
            self.i += 1           # 计时：
            if self.i % 3 == 0:   # 每三帧换一幅图片
                self.i = 0
                self.imgDisply = not self.imgDisply    # 是否播放图片

                # 发射一颗子弹
                Bullet(bulletImgs[3], self.rect.midtop, self.screen, 15)

            # 切换喷气图片
            if self.imgDisply:
                self.screen.blit(self.imgs[0], self.rect)
            else:
                self.screen.blit(self.imgs[1], self.rect)

            # 实时监测 碰撞
            self.Collide()


        else:
            self.bulletSound.set_volume(0)
            # 播放死亡动画
            self.i += 1
            self.screen.blit(heroDeathImgs[self.deathImgIndex], self.rect)
            if self.i % 7 == 0:
                self.i = 0
                self.deathImgIndex += 1
                if self.deathImgIndex == len(heroDeathImgs):
                    self.deathImgIndex = 0
                    FontDisplay.Update(self.score)
                    self.score = 0  # 分数归零
                    self.hp = 50     # 血量还原
                    pygame.time.wait(200)   # 延迟ms
                    isPlay = False  # 游戏结束，回到开始界面

    def Collide(self):     # 碰撞
        global isPlay
        temp = pygame.sprite.spritecollideany(self, enemyList, collided=pygame.sprite.collide_mask)
        if temp != None:
            temp.hp = 0        # 敌机死亡
            self.hp -= 1       # 主角减血
            if self.hp != 0:
                self.rect.topleft = self.pos  # 主角还原初始位置

# 子弹列表：
bulletList = []

# 导入子弹图片：
bulletImgs=[
    pygame.image.load('plane/image/bullet.png'),
    pygame.image.load('plane/image/bullet1.png'),
    pygame.image.load('plane/image/bullet2.png'),
    pygame.image.load('plane/p-f03.png')
]

# 子弹类 ：*****************************

class Bullet(pygame.sprite.Sprite):

    def __init__(self, image, pos, screen, speed):
        self.image = image
        self.rect = image.get_rect()     # 获得图片矩形范围
        self.rect.center = pos           # 子弹产生时的初始位置
        self.screen = screen
        self.speed = speed
        bulletList.append(self)

    def Move(self):
        self.rect=self.rect.move(0, -self.speed)     # 子弹移动
        self.screen.blit(self.image, self.rect)

        # 超出画面，消除子弹
        if self.rect.y < -50:
            if self in bulletList:
                bulletList.remove(self)

        # 移动时检测碰撞
        self.Collide()


    # 子弹碰撞敌机
    def Collide(self):
        temp = pygame.sprite.spritecollideany\
            (self, enemyList, collided=pygame.sprite.collide_mask)
        if temp != None:
            if self in bulletList:
                bulletList.remove(self)
            temp.hp -= 1
            # 敌机死亡
            # if temp in enemyList:
            #     enemyList.remove(temp)

    # 所有的子弹移动
    @staticmethod
    def AllButtetMove():
        for i in bulletList:
            if i != None and isinstance(i, Bullet):
                i.Move()

# 敌机：列表
enemyList = []

# 敌机图片
enemy1 = [
    pygame.image.load("plane/image/enemy0.png"),
    pygame.image.load("plane/image/enemy0_down1.png"),
    pygame.image.load("plane/image/enemy0_down2.png"),
    pygame.image.load("plane/image/enemy0_down3.png"),
    pygame.image.load("plane/image/enemy0_down4.png"),
]
enemy2 = [
    pygame.image.load("plane/image/enemy1.png"),
    pygame.image.load("plane/image/enemy1_down1.png"),
    pygame.image.load("plane/image/enemy1_down2.png"),
    pygame.image.load("plane/image/enemy1_down3.png"),
    pygame.image.load("plane/image/enemy1_down4.png"),

]
enemy3 = [
    pygame.image.load("plane/image/enemy2.png"),
    pygame.image.load("plane/image/enemy2_down1.png"),
    pygame.image.load("plane/image/enemy2_down2.png"),
    pygame.image.load("plane/image/enemy2_down3.png"),
    pygame.image.load("plane/image/enemy2_down4.png"),
    pygame.image.load("plane/image/enemy2_down5.png"),
    pygame.image.load("plane/image/enemy2_down6.png")
]

# 敌机类：********************

class Enemy(pygame.sprite.Sprite):
    CreateIndex = 0  # 用于产生敌机的变量

    def __init__(self, imgs, pos, screen, speed, hp, tag):
        self.imgs = imgs
        self.image = imgs[0]    # 默认第一幅敌机图
        self.rect=self.image.get_rect()    # 获得敌机图片矩形的对象
        self.rect.topleft = pos    # 设置初始位置
        self.screen = screen
        self.speed = speed
        self.hp = hp
        self.tag = tag

        self.i = 0                  # 计时：每7帧播放一个画面
        self.imgsIndex = 0          # 敌机死亡动画的索引
        enemyList.append(self)      # 将对象自己放入列表

    def __str__(self):
        return "敌机"

    # 方法： 移动 ，碰撞 ，死亡
    def Move(self):

        if self.hp > 0:       # 敌机血量
            self.rect = self.rect.move(0, self.speed)   # 敌机沿x轴移动
            self.screen.blit(self.image, self.rect)     # 渲染敌机图片和位置

            # 超过画面销毁敌机
            if self.rect.y >= 760:
                if self in enemyList:
                    enemyList.remove(self)

        else:
            self.Death()

    def Collide(self):
        pass
    def Death(self):
        # 播放死亡动画
        self.i += 1
        self.screen.blit(self.imgs[self.imgsIndex], self.rect)
        if self.i % 2 == 0:    # 2帧一副图
            self.i = 0
            self.imgsIndex += 1

            # 不能立马消失
            if self in enemyList and self.imgsIndex == len(self.imgs):
                AllSounds.PlaySound(2)
                if self.tag == "enemy1":
                    hero.score += 1
                elif self.tag == "enemy2":
                    hero.score += 3
                else:
                    hero.score += 10
                enemyList.remove(self)

    @staticmethod
    def RandomCreateEnemy(screen):

        Enemy.CreateIndex += 1
        if Enemy.CreateIndex%10 == 0:     # 控制敌机产生的间隔（10帧一架）
            Enemy.CreateIndex = 0
            randNum = r.randint(1, 100)
            if randNum <= 70:
                Enemy(enemy1, (r.randint(0, 429), -250), screen, 7, 1, "enemy1")
            elif randNum <= 90:
                Enemy(enemy2, (r.randint(0, 411), -250), screen, 5, 3, "enemy2")
            else:
                Enemy(enemy3, (r.randint(0,315), -250), screen, 1, 10, "enemy3")

    @staticmethod
    def AllEnemyMove():
        for i in enemyList:
            if i != None and isinstance(i, Enemy):
                i.Move()

# 音效：
sounds=[
    pygame.mixer.Sound("plane/sound/button.ogg"),       # 按钮音效
    pygame.mixer.Sound("plane/sound/bullet.wav"),       # 子弹音效
    pygame.mixer.Sound("plane/sound/enemy0_down.wav"),  # 敌机死亡音效
    pygame.mixer.Sound("plane/sound/use_bomb.ogg")      # 英雄死亡音效
]

# 音效类：***************

class AllSounds:
    @staticmethod
    def PlaySound(num, loop=0):
        sounds[num].play(loops=loop)     # Loops音效播放次数（是否循环）
        return sounds[num]

# 字体类：****************

class FontDisplay:

    history = 0   # 历史成绩

    def __init__(self, font, size, screen):
        self.font = font     # 字体
        self.size = size     # 字体大小
        self.screen = screen

    def Show(self, pos, strA):
        tempFont = pygame.font.Font(self.font, self.size)  # 创建字体
        fontSurface = tempFont.render(strA, True, pygame.Color("black"))  # 将文本转为 surface
        self.screen.blit(fontSurface, pos)  # 渲染字体图片

    @staticmethod
    def StartUpateHistory(path="score.txt"):  # 每次开始都知道历史成绩
        if os.path.exists(path):    # 判断路径是否存在
            with open(path, "r") as f_r:   # 读取路径内的历史内容
                FontDisplay.history = int(f_r.read())
        else:
            with open(path, "w") as f_w:    # 写入历史成绩
                f_w.write("0")
                FontDisplay.history = 0

        # 更新历史成绩
    @staticmethod  # 静态方法
    def Update(score, path="score.txt"):
        if score > FontDisplay.history:
            with open(path, "w") as f_w:     # 更新
                f_w.write(str(score))


# 创建开始界面类的对象：
startPanel = startPanel(startImgs, startBottomImgs, screen)

# 设置背景音乐：*******

pygame.mixer.music.load('plane/sound/game_music.mp3')      # 插入背景音乐
pygame.mixer.music.play(-1)     # 音乐无限播放
pygame.mixer.music.set_volume(0.1)     # 设置音乐的音量（为最大音量的1/10）

# 设置游戏图标及名称：*******

icon=pygame.image.load("plane/plane_.ico")   # 设置游戏图标
pygame.display.set_icon(icon)                # 显示游戏图标
pygame.display.set_caption('飞机大战')        # 设置并显示游戏名称

# 创建游戏背景对象：
backGround = BackGround(startImgs[4], screen, 3)

# 创建英雄类对象：
hero = Hero(heroImgs, (200, 500), screen, 5, 50, 0)

# 创建字体对象：
fontDisplay = FontDisplay("plane/font/Marker Felt.ttf", 25, screen)

# 全局变量：是否开始游戏？
isPlay = False

# 添加时间变量：
clock = pygame.time.Clock()

def Event():

    global isPlay  # 全局变量 isPlay

    # 所有的事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:    # 退出事件
            pygame.quit()
            sys.exit()
        # 鼠标
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # 判断鼠标位置是否在按钮里面
                startPanel.isInRect = pygame.Rect(160, 350,161, 67)\
                    .collidepoint(pygame.mouse.get_pos())
                if startPanel.isInRect:
                    print("开始游戏")
                    FontDisplay.StartUpateHistory()
                    enemyList.clear()
                    bulletList.clear()
                    hero.rect.topleft = (200, 500)
                    isPlay = True
        # 键盘
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                enemyList.clear()
                bulletList.clear()
                hero.rect.topleft = (200, 500)
                hero.hp = 3
                hero.score = 0
                isPlay = False
            if event.key == pygame.K_SPACE:
                #全屏爆炸
                for i in enemyList:
                    AllSounds.PlaySound(3)
                    i.hp = 0
            if event.key == pygame.K_w:
                Hero.up=True
            if event.key == pygame.K_s:
                Hero.down = True
            if event.key == pygame.K_a:
                Hero.left = True
            if event.key == pygame.K_d:
                Hero.right = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                Hero.up = False
            if event.key == pygame.K_s:
                Hero.down = False
            if event.key == pygame.K_a:
                Hero.left = False
            if event.key == pygame.K_d:
                Hero.right = False

def Main():

    global isPlay      # 全局变量 isPlay

    while True:

        Event()      # 处理所有事件：

        # 开始画面渲染：
        if isPlay == False:
            startPanel.Show()
        else:
            screen.fill(pygame.Color("Green"))

            # 背景移动
            backGround.Move()

            # 产生英雄
            hero.Move()

            # 移动所有子弹
            Bullet.AllButtetMove()

            # 产生敌机并移动：
            Enemy.RandomCreateEnemy(screen)
            Enemy.AllEnemyMove()

            # 显示字体
            fontDisplay.Show((10, 10), "HP:%s" % hero.hp)
            fontDisplay.Show((10, 35), "Score:%s" % hero.score)
            fontDisplay.Show((10, 65), "History:%s" % FontDisplay.history)

        pygame.display.update()

        # 设置时间帧频
        clock.tick(60)   # 每秒几个画面

if __name__  ==  '__main__' :

    Main()