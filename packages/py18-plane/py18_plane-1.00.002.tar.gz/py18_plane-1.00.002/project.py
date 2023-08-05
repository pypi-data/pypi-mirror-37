from typing import Any

import pygame
import sys,math,random,os


pygame.init()

pygame.display.init()

screen=pygame.display.set_mode((510,800))
pygame.display.set_caption("1808LKK飞机大战")
icon=pygame.image.load("image\icon.png")
pygame.display.set_icon(icon)
pygame.mixer.music.load("music/BGM.mp3")
pygame.mixer.music.play(-1)
#开始界面
starImage=[
    pygame.transform.scale(pygame.image.load("image/background.jpg"),(510,800)),
    pygame.transform.scale(pygame.image.load("image/icon02.png"),(80,120)),
    pygame.transform.scale(pygame.image.load("image/icon01.png"),(80,120)),
    pygame.image.load("image/name.png"),
    pygame.image.load("image/loading.png"),
    pygame.transform.scale(pygame.image.load("image/leveldesign01.png"),(130,60)),
    pygame.transform.scale(pygame.image.load("image/leveldesign02.png"),(130,60)),
    pygame.transform.scale(pygame.image.load("image/leveldesign03.png"),(130,60)),
    pygame.transform.scale(pygame.image.load("image/startbutton.png"),(175,65))


    ]
#游戏界面图片列表
Gameimage=[
    pygame.transform.scale(pygame.image.load("image/img_bg_level_1.jpg"),(510,800)),
    pygame.transform.scale(pygame.image.load("image/img_bg_level_1.jpg"),(510,800))

]

#玩家飞机图片列表
palyerplane=[
    pygame.transform.scale(pygame.image.load("image\planeimage01.png"),(200,150)),
    pygame.transform.scale(pygame.image.load("image\planeimage02.png"),(170,120))


]

palyerDeath=[
    pygame.transform.scale(pygame.image.load("image\planeimage3.png"),(170,120))
]

#子弹图片列表
bullet=[
    pygame.transform.scale(pygame.image.load("image/bullet01.png"),(25,60)),
    pygame.transform.scale(pygame.image.load("image/bullet01.png"),(25,60)),
    pygame.transform.scale(pygame.image.load("image/bullet02.png"),(25,60)),
    pygame.transform.scale(pygame.image.load("image/bullet03.png"),(25,60)),
    pygame.transform.scale(pygame.image.load("image/bullet04.png"),(25,60)),
    pygame.image.load("image/feidan.png")
]
bullet_list=[]
#开始界面图片列表
startBottomImage=[
    pygame.image.load("image/game_loading1.png"),
    pygame.image.load("image/background.png"),
    pygame.image.load("image/game_loading3.png")
]


enemy1=[
    pygame.transform.scale(pygame.image.load("image/enemy04.png"),(100,60)),
    pygame.image.load("image/xiaoshi.png")

]


enemy2=[
    pygame.transform.scale(pygame.image.load("image/enemy01.png"),(150,100)),
    pygame.image.load("image/xiaoshi.png")
]
enemy3=[
    pygame.transform.scale(pygame.image.load("image/enemy03.png"),(250,300)),
    pygame.image.load("image/xiaoshi.png")
]
sounds=[
    pygame.mixer.Sound("sound/bullet01.wav"),
    # pygame.mixer.Sound("sound/shibai.wav"),
    pygame.mixer.Sound("sound/boom.ogg")
]

#生产飞机列表
enemy_list=[]
#定义开始面板类
class StarPanel:
    def __init__(self,starImage,startBottomImgs,screen):
        self.starImage=starImage
        self.startBottomImgs=startBottomImgs
        self.screen=screen
        self.titleY=0
        self.icon01=0
        self.icon02=0
        self.buttonIndex=0
        self.i=0
        self.isInRect=False#鼠标是否在按钮内部
    #绘制屏幕
    def Show(self):
        self.screen.blit(self.starImage[0],(0,0))
        self.icon01+=3
        self.screen.blit(self.starImage[1], (420, self.icon01))
        self.icon02 += 3
        self.screen.blit(self.starImage[2], (10, 680 - self.icon02))

        self.titleY+=0.05
        self.screen.blit(self.starImage[3],(50,100+60*math.sin(self.titleY)))
        self.screen.blit(self.starImage[4],(0,150))
        self.screen.blit(self.starImage[5],(190,275))
        self.screen.blit(self.starImage[6],(190,375))
        self.screen.blit(self.starImage[7],(190,475))
        self.screen.blit(self.starImage[8],(170,575))


        self.i+=1
        if self.buttonIndex==3:
            self.buttonIndex=0
        self.screen.blit(self.startBottomImgs[self.buttonIndex],(150,680))
        if self.i%20==0:
            self.buttonIndex+=1
            self.i=0
#进入游戏界面类
class GamePanel:

    def __init__(self,Gameimage,screen):
        self.Gameimage=Gameimage
        self.screen=screen
        self.Move1=0
        self.Move2=0
        self.Imageindex=0
    def gameShow(self):
        self.Move1 += 1
        self.screen.blit(self.Gameimage[self.Imageindex],(0,-800+self.Move1))
        self.Move2+=1
        self.screen.blit(self.Gameimage[self.Imageindex],(0,0+self.Move2))
        if self.Move2>=799:
            self.Move2=self.Move1-799
        if self.Move1>=799:
            self.Move1=self.Move2
        # mousepos=pygame.mouse.get_pos()
        # endpos=(pygame.mouse.get_pos()[0]-self.palyerplane[0].get_rect().centerx,pygame.mouse.get_pos()[1]-self.palyerplane[0].get_rect().centery)

#角色类
class Hero_Role(pygame.sprite.Sprite):
    up = False
    down = False
    left = False
    right = False


    # 属性： 图片，屏幕，速度，血量 ，分数,初始化位置
    def __init__(self,imgs,screen,speed,hp,score,pos):
        self.imgs=imgs
        self.image=imgs[1]
        self.rect = self.image.get_rect()#获得图片的矩形对象
        self.rect.topleft = pos
        self.screen=screen
        self.speed=speed
        self.hp=hp
        self.score=score
        self.pos = pos
        self.i = 0
        self.imgDisply = True
        self.bulletSound = Sound.PlaySound(0, -1)
        self.bulletSound.set_volume(0)
        self.deathImgIndex = 0
    def Move(self):
        global isPlay
        if isPlay:
            self.bulletSound.set_volume(1)
        else:
            self.bulletSound.set_volume(0)
        if self.hp>0:
            if Hero_Role.down:
                self.rect=self.rect.move(0,self.speed)
            if Hero_Role.up:
                self.rect = self.rect.move(0, -self.speed)
            if Hero_Role.right:
                self.rect = self.rect.move(self.speed,0)
            if Hero_Role.left:
                self.rect = self.rect.move(-self.speed,0)

            #约束飞机的移动区间
            if self.rect.x<=0:
                self.rect.x=0
            if self.rect.x>=340:
                self.rect.x=340
            if self.rect.y<=0:
                self.rect.y=0
            if self.rect.y>=680:
                self.rect.y=680

            self.screen.blit(self.imgs[1], self.rect)
            self.i += 1
            if self.i % 15 == 0:
                self.i = 0
                Bullets(bullet[0], (self.rect.x+50,self.rect.y), self.screen,10)
                Bullets(bullet[1], (self.rect.x+120,self.rect.y), self.screen,10)

        # 实时监测 碰撞
            self.Collide()
        else:
            self.bulletSound.set_volume(0)
            # 播放死亡动画
            self.i += 1
            self.screen.blit(palyerDeath[self.deathImgIndex], self.rect)
            if self.i % 15 == 0:
                self.i = 0
                self.deathImgIndex += 1
                if self.deathImgIndex == len(palyerDeath):
                    self.deathImgIndex = 0
                    FontDisplay.Update(self.score)
                    self.score = 0  # 分数归零
                    self.hp = 3  # 血量还原
                    pygame.time.wait(200)
                    isPlay = False  # 游戏结束，回到开始界面
    def Death(self):
        pass

    def Collide(self):
        global isPlay
        temp = pygame.sprite.spritecollideany(self, enemy_list, collided=pygame.sprite.collide_mask)
        if temp != None:
            temp.hp=0  # 敌机死亡
            self.hp-=1  # 主角 减血
            if self.hp!= 0:
                self.rect.topleft = self.pos

            #子弹类
class Bullets(pygame.sprite.Sprite):
    """
    属性： 图片，屏幕，速度，
    """
    def __init__(self,image,pos,screen,speed):
        self.image=image
        self.rect = image.get_rect()
        self.rect.center = pos
        self.screen=screen
        self.speed=speed
        bullet_list.append(self)# 把自己产生的对象添加到子弹列表中
    #定义让子弹运动的方法
    def Move(self):
        self.rect = self.rect.move(0, -self.speed)
        self.screen.blit(self.image, self.rect)
        # 如果子弹飞出屏幕外  让列表中的子弹对象删除自己
        if self.rect.y < -10:
            if self in bullet_list:
                bullet_list.remove(self)
         #移动时的碰撞检测
        self.Collide()
    def Collide(self):
        temp=pygame.sprite.spritecollideany(self,enemy_list,collided=pygame.sprite.collide_mask)
        if temp!=None:
            if self in bullet_list:
                bullet_list.remove(self)
            temp.hp -= 1
            #敌机死亡
            # if temp in enemy_list:
            #     enemy_list.remove(temp)
    #定义一个关于子弹的类内静态函数，让所有的子弹都移动
    @staticmethod
    def BulletMove():
        for i in bullet_list:
            if i != None and isinstance(i, Bullets): #如果子弹列表内不为空且属于子弹对象
                i.Move()




class Enemy(pygame.sprite.Sprite):
    enemyIndex=0  #用于产生敌机的变量
    def __init__(self,imgs,pos,screen,speed,hp,label) :
        self.imgs=imgs
        self.image = imgs[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.screen = screen
        self.speed = speed
        self.hp = hp
        self.label = label
        self.i=0
        self.imgsIndex = 0
        enemy_list.append(self)  #与子弹同理


    def Move(self):
        if self.hp>0:
            self.rect=self.rect.move(0,self.speed)
            self.screen.blit(self.image,self.rect)

        #超过画面销毁敌机
            if self.rect.y>=950:
                if self in enemy_list:
                    enemy_list.remove(self)
        else:
            self.Death()



    def Collide(self):
        pass
    def Death(self):
        self.i += 1
        self.screen.blit(self.imgs[self.imgsIndex], self.rect)
        if self.i % 7 == 0:
            self.i = 0
            self.imgsIndex += 1
            # 不能立马消失
            if self in enemy_list and self.imgsIndex == len(self.imgs):
                Sound.PlaySound(0)
                if self.label == "enemy1":
                    Player.score += 1
                elif self.label == "enemy2":
                    Player.score += 3
                else:
                    Player.score += 10
                enemy_list.remove(self)

    @staticmethod
    def RandomEnemy(screen):

        Enemy.enemyIndex += 1
        if Enemy.enemyIndex % 17 == 0:
            Enemy.enemyIndex = 0
            randNum = random.randint(1, 100)  #分配产生不同敌机概率
            if randNum <= 70:
                Enemy(enemy1, (random.randint(0, 410), -250), screen, 7, 1, "enemy1")
            elif randNum <= 95:
                Enemy(enemy2, (random.randint(0, 360), -250), screen, 5, 3, "enemy2")
            else:
                Enemy(enemy3, (random.randint(0, 310), -250), screen, 1, 10, "enemy3")

    @staticmethod#敌机静态函数
    def EnemyMove():
        for i in enemy_list:
            if i != None and isinstance(i, Enemy):
                i.Move()



    #开始界面的对象


class Sound:
    @staticmethod
    def PlaySound(num,loop=0):
        sounds[num].play(loops=loop)
        return sounds[num]


class FontDisplay:
    history = 0#定义初始历史分

    def __init__(self,Font,size,screen):
        self.Font = Font
        self.size = size
        self.screen = screen


    def Show(self,pos,strA):
        tempFont=pygame.font.Font(self.Font,self.size) #创建字体
        fontSurface=tempFont.render(strA,True,pygame.Color("pink"))#将文本转为 surface
        self.screen.blit(fontSurface,pos) #渲染出来

    @staticmethod
    def UpateHistory(path="score.txt"): #每次开始都知道 历史成绩
        if os.path.exists(path):
            with open(path,"r") as f_r:
                FontDisplay.history=int(f_r.read())
        else:
            with open(path,"w") as f_w:
                f_w.write("0")
                FontDisplay.history =0


    @staticmethod
    def Update(score,path="score.txt"): #更新历史成绩
        if score>FontDisplay.history:
            #更新
            with open(path,"w") as f_w:
                f_w.write(str(score))
#创建字体对象
fontDisplay=FontDisplay("font/Marker Felt.ttf",25,screen)
starPanel=StarPanel(starImage,startBottomImage,screen)
#游戏界面对象
gamePanel=GamePanel(Gameimage,screen)
#玩家飞机对象
Player=Hero_Role(palyerplane,screen,4,3,0,(170,580))
    # self.screen.blit(self.palyerplane[1],(170,580))
    # self.screen.blit(self.bullet[0],(255,550))
#全局变量。是否开始游戏
isPlay=False
#全局变量。是否播放音效
musicplay=True

clock=pygame.time.Clock()

def Event():
    global isPlay ,musicplay # 全局变量 isPlay
    # 所有的事件
    for event in pygame.event.get():
        # 退出事件
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # 鼠标
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # 判断 鼠标位置 是否在 按钮里面
                starPanel.isInRect = pygame.Rect(190, 275, 130, 60).collidepoint(pygame.mouse.get_pos())
                if starPanel.isInRect:
                    FontDisplay.UpateHistory()
                    enemy_list.clear()
                    bullet_list.clear()
                    Player.rect.topleft = (170, 580)
                    isPlay = True
            if event.button == 1:
                # 判断 鼠标位置 是否在 按钮里面
                starPanel.isInRect = pygame.Rect(190, 375, 130, 60).collidepoint(pygame.mouse.get_pos())
            if starPanel.isInRect:
                FontDisplay.UpateHistory()
                enemy_list.clear()
                bullet_list.clear()
                Player.rect.topleft = (170, 580)
                isPlay = True
            if event.button == 1:
                # 判断 鼠标位置 是否在 按钮里面
                starPanel.isInRect = pygame.Rect(190, 475, 130, 60).collidepoint(pygame.mouse.get_pos())
            if starPanel.isInRect:
                FontDisplay.UpateHistory()
                enemy_list.clear()
                bullet_list.clear()
                Player.rect.topleft = (170, 580)
                isPlay = True
        # 键盘
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                enemy_list.clear()
                bullet_list.clear()
                Player.rect.topleft = (200, 500)
                Player.hp = 3
                Player.score = 0
                isPlay = False
            if event.key == pygame.K_SPACE:
                # 全屏爆炸
                for i in enemy_list:
                    Sound.PlaySound(1)
                    i.hp = 0

            if event.key == pygame.K_w or event.key==pygame.K_UP:
                Hero_Role.up = True
            if event.key == pygame.K_s or event.key==pygame.K_DOWN:
                Hero_Role.down = True
            if event.key == pygame.K_a or event.key==pygame.K_LEFT:
                Hero_Role.left = True
            if event.key == pygame.K_d or event.key==pygame.K_RIGHT:
                Hero_Role.right = True

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_w or event.key==pygame.K_UP:
                Hero_Role.up=False
            if event.key==pygame.K_s or event.key==pygame.K_DOWN:
                Hero_Role.down=False
            if event.key==pygame.K_a  or event.key==pygame.K_LEFT:
                Hero_Role.left=False
            if event.key==pygame.K_d or event.key==pygame.K_RIGHT:
                Hero_Role.right=False

def Main():
    while True:
        Event()
        if isPlay==False:
            starPanel.Show()

        else:
            gamePanel.gameShow()
            Hero_Role.Move(Player)
            Bullets.BulletMove()
            Enemy.RandomEnemy(screen)
            Enemy.EnemyMove()

            #显示字体
            fontDisplay.Show((10, 10), "HP:%s" % Player.hp)
            fontDisplay.Show((10, 35), "Score:%s" % Player.score)
            fontDisplay.Show((10, 65), "History:%s" % FontDisplay.history)
        pygame.display.update()
        clock.tick(60)

if __name__=="__main__":
    Main()