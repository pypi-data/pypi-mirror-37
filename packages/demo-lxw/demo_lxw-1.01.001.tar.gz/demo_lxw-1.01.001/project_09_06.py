#开始界面：
#       0：背景图片  image.load()
#       1：浮动标题   image.load() >screen.blit(img,【x，y+sin()】)>>
#       2. 开始按钮   image.load() >mouse  event
#       3.下部喷气飞机 [image.load()......] >>screen.blit(img[index],【x，y】)
#       4.背景音乐

#游戏界面

#      0：背景 ： #属性： 图片，屏幕       方法：循环移动
#      1：主角 ： #属性： 图片，屏幕，速度，血量 ，分数  方法： 移动 ， 碰撞 ，  死亡
#      1.1：主角的子弹： #属性： 图片，屏幕，速度，  方法： 移动 ， 碰撞 ，
#      2：敌机 ：#属性： 图片，屏幕，速度，血量  方法： 移动 ， 碰撞 ，  死亡
#      3：敌机工厂：静态-产生敌机（几率 产生敌机）
#      4：分数显示：  当前分  历史分
#      5：音效类

#结束界面 ：显示结果


import pygame
import sys
import math
import random,os

        #初始化pygame
pygame.init()
        #初始化pygame.display
pygame.display.init()
        #创建窗口
xxx=480
yyy=850
screen=pygame.display.set_mode((xxx,yyy))

        #开始界面的图片

listscreen=[pygame.image.load("image/background.png"),
            pygame.transform.scale(pygame.image.load("image/loading.png"),(xxx,xxx)),
            pygame.image.load("image/name.png"),
            pygame.image.load("image/icon72x72.png")]

listbottom=[pygame.image.load("image/game_loading1.png"),
            pygame.image.load("image/game_loading2.png"),
            pygame.image.load("image/game_loading3.png")]

#游戏界面的图片
        #游戏底图

gameload=pygame.transform.scale(pygame.image.load("image/gameload.jpg"),(480,900))

        #主角战机

listgame=pygame.transform.scale(pygame.image.load("image/a4-1.png"),(100,80))

        #子弹

    #蓝色子弹。0  触发
bulletimage=pygame.transform.scale(pygame.image.load("image/wsparticle_27.png"),(50,50))
    #火箭弹。  1  触发
bulletimage2=pygame.transform.scale(pygame.image.load("image/feidan.png"),(20,50))

        #随机物品

randomimage1=pygame.transform.scale(pygame.image.load("image/random.png"),(88,64))


        #敌机
x=50
enemyimage1=[pygame.transform.scale(pygame.image.load("image/uiPlane0.png"),(x,x)),
            pygame.transform.scale(pygame.image.load("image/wsparticle_smoke03.png"), (x,x)),
            pygame.transform.scale(pygame.image.load("image/wsparticle_smoke07.png"), (x,x)),
            pygame.transform.scale(pygame.image.load("image/wsparticle_smoke09.png"), (x,x))
             ]
xx=100
enemyimage2=[pygame.transform.scale(pygame.image.load("image/img_plane_boss2_副本.png"),(xx,xx)),
            pygame.transform.scale(pygame.image.load("image/wsparticle_smoke03.png"),(xx,xx)),
            pygame.transform.scale(pygame.image.load("image/wsparticle_smoke07.png"),(xx,xx)),
            pygame.transform.scale(pygame.image.load("image/wsparticle_smoke09.png"),(xx,xx))
]
zzz=200
enemyimage3=[pygame.transform.scale(pygame.image.load("image/img_plane_boss6_副本.png"),(zzz,zzz)),
            pygame.transform.scale(pygame.image.load("image/wsparticle_smoke03.png"),(zzz,zzz)),
            pygame.transform.scale(pygame.image.load("image/wsparticle_smoke07.png"),(zzz,zzz)),
            pygame.transform.scale(pygame.image.load("image/wsparticle_smoke09.png"),(zzz,zzz))
]
enemyimage4=[pygame.transform.scale(pygame.image.load("image/uiPlane1.png"),(x,x)),
            pygame.transform.scale(pygame.image.load("image/wsparticle_smoke03.png"), (x,x)),
            pygame.transform.scale(pygame.image.load("image/wsparticle_smoke07.png"), (x,x)),
            pygame.transform.scale(pygame.image.load("image/wsparticle_smoke09.png"), (x,x))]
enemyimage5=[pygame.transform.scale(pygame.image.load("image/uiPlane2.png"),(x,x)),
            pygame.transform.scale(pygame.image.load("image/wsparticle_smoke03.png"), (x,x)),
            pygame.transform.scale(pygame.image.load("image/wsparticle_smoke07.png"), (x,x)),
            pygame.transform.scale(pygame.image.load("image/wsparticle_smoke09.png"), (x,x))]

        #开始界面的类
class startface:

    def __init__(self,listscreen,listbottom,screen):
        self.listscreen=listscreen
        self.listboom=listbottom
        self.screen=screen
        self.starty=1
        self.i=1
        self.listboomindex=0
        self.icon=pygame.image.load("image/a2-2.png")

    def setstart_face(self):
        self.screen.blit(self.listscreen[0],(0,0))
        self.screen.blit(self.listscreen[1],(0,200))
        self.starty+=0.05
        self.screen.blit(self.listscreen[2],(25,100+50*math.sin(self.starty)))
        self.screen.blit(self.listscreen[3],(210,400))

        self.i+=1
        if self.listboomindex==3:
            self.listboomindex=0
        self.screen.blit(self.listboom[self.listboomindex],(180,700))
        if self.i%18==0:
            self.listboomindex+=1
            self.i=0
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption("飞机大战！")

        #游戏界面的类
class gameface:

    def __init__(self,gameload,screen,listgame,speed):
        self.gameload1=gameload
        self.rect1=self.gameload1.get_rect()
        self.gameload2=self.gameload1.copy()
        self.rect2=self.gameload2.get_rect()
        self.rect2.topleft=(0,-900)
        self.screen=screen
        self.listgame=listgame
        self.speed=speed


    def show(self):
        global gamemouse
        global b
        global mouseA
        self.rect1=self.rect1.move(0,self.speed)
        self.rect2=self.rect2.move(0,self.speed)

        if self.rect1.y>850:
            self.rect1.y=self.rect2.y-900
        if self.rect2.y>850:
            self.rect2.y=self.rect1.y-900

        self.screen.blit(self.gameload1,self.rect1)
        self.screen.blit(self.gameload2,self.rect2)

#主角类
# class heroA:
#
#     def __init__(self,listgame,speed,hp,mouseA,score,screen):
#         self.listgame=listgame
#         self.rect=self.listgame.get_rect()
#         self.rect.topleft=mouseA
#         self.speed=speed
#         self.hp=hp
#         self.start=mouseA
#         self.score=score
#         self.screen=screen
#
#     def heromove(self):
#         global gamemouse
#         global countA
#         if b == 1:
#             self.rect = (pygame.mouse.get_pos()[0] - listgame.get_rect().centerx,pygame.mouse.get_pos()[1] - listgame.get_rect().centery)
#         elif b == 0:
#             self.rect = (gamemouse[0] - listgame.get_rect().centerx, gamemouse[1] - listgame.get_rect().centery)
#
#         if gamemouse[0]<=listgame.get_rect().centerx:
#             gamemouse=(listgame.get_rect().centerx,gamemouse[1])
#         if gamemouse[0]>=xxx-listgame.get_rect().centerx:
#             gamemouse=(xxx-listgame.get_rect().centerx,gamemouse[1])
#         if gamemouse[1]<=listgame.get_rect().centery:
#             gamemouse=(gamemouse[0],listgame.get_rect().centery)
#         if gamemouse[1]>=yyy-listgame.get_rect().centery:
#             gamemouse=(gamemouse[0],yyy-listgame.get_rect().centery)
#
#
#         self.screen.blit(listgame, self.rect)

#背景音乐
pygame.mixer.music.load("music/game_music.ogg")
pygame.mixer.music.play(-1)

sounds=[pygame.mixer.Sound("music/big_spaceship_flying.ogg"),
        pygame.mixer.Sound("music/button.ogg"),
        pygame.mixer.Sound("music/game_over.ogg"),
        pygame.mixer.Sound("music/get_bomb.ogg")
        ]

        #音效类
class Allsounds:
    @staticmethod
    def playsound(num,loop=0):
        sounds[num].play(loops=loop)
        return sounds[num]

listrandom=[]
        #随机事件类
class random_eat(pygame.sprite.Sprite):
    sss = 1
    x=0

    def __init__(self,image,start,speed,screen):
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.topleft=start
        self.start=start
        self.speed=speed
        self.screen=screen
        listrandom.append(self)

    #产生的随机物品设置移动。
    def move_random(self):
        self.rect=self.rect.move(0,self.speed)
        self.screen.blit(self.image,self.rect)

        if self.rect.x>500:
            listrandom.remove(self)

    # 随机产生奖励物品
    @staticmethod
    def create_random(screen):
        random_eat.x+=1
        if random_eat.x%600==0:
            random_eat(randomimage1,(random.randint(0,400),-50),5,screen)
            random_eat.x=0

    #所有随机物品，调用移动
    @staticmethod
    def all_randommove():
        for i in listrandom:
            if i in listrandom and isinstance(i,random_eat):
                i.move_random()
                i.collide()

    def collide(self):
        global randomeatA
        temp = pygame.sprite.spritecollideany(self, herolist, collided=pygame.sprite.collide_mask)
        if temp!=None:
            listrandom.remove(self)
            randomeatA=1
        #主角类
class hero(pygame.sprite.Sprite):
    up=False
    down=False
    left=False
    right=False

    def __init__(self,image,speed,hp,mouseA,score,screen):
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.topleft=mouseA
        self.speed=speed
        self.hp=hp
        self.start=mouseA
        self.score=score
        self.screen=screen
        herolist.append(self)
        self.bulletSound = Allsounds.playsound(1,-1)
        self.bulletSound.set_volume(0)

    #主角移动
    def heromove(self):
        global mousepanduan
        global xxx
        global yyy
        global countA
        global randomeatA

        #子弹音效声音
        if self.hp>0:
            if mousepanduan:
                self.bulletSound.set_volume(1)
            else:
                self.bulletSound.set_volume(0)

            if heroA.down:
                self.rect=self.rect.move(0,self.speed)
            if heroA.up:
                self.rect=self.rect.move(0,-self.speed)
            if heroA.left:
                self.rect=self.rect.move(-self.speed,0)
            if heroA.right:
                self.rect=self.rect.move(self.speed,0)

            if self.rect.x<=0:
                self.rect.x=0
            if self.rect.x>=xxx-self.image.get_rect()[2]:
                self.rect.x=xxx-self.image.get_rect()[2]
            if self.rect.y<=0:
                self.rect.y=0
            if self.rect.y>=yyy-self.image.get_rect()[3]:
                self.rect.y=yyy-self.image.get_rect()[3]

            self.screen.blit(self.image,self.rect)
            self.Collide()#实时监控碰撞

            #发射子弹
            if randomeatA==0:
                if countA==10:
                    bullet(bulletimage,7,self.screen,self.rect.midtop)
                    countA=0
                countA+=1
            elif randomeatA==1:
                if countA==10:
                    bullet(bulletimage2,7,self.screen,(self.rect.midtop[0]-32,self.rect.midtop[1]))
                    bullet(bulletimage, 7, self.screen, self.rect.midtop)
                    bullet(bulletimage2,7,self.screen,(self.rect.midtop[0]+35,self.rect.midtop[1]))
                    countA=0
                countA+=1

        else:
            if mousepanduan:
                self.bulletSound.set_volume(0)
            else:
                self.bulletSound.set_volume(1)
            fontdisplay.Update(self.score)
            self.hp = 3
            self.score = 0
            self.rect.topleft = self.start
            pygame.time.wait(200)
            mousepanduan = False

    #主角碰撞
    def Collide(self):
        global randomeatA
        temp=pygame.sprite.spritecollideany(self,enemylist,collided=pygame.sprite.collide_mask)
        if temp!=None:
            temp.hp=0 #敌机死亡
            self.hp-=1 #英雄减血
            if self.hp!=0:
                self.rect.topleft = self.start
            # self.rect.topleft=self.start


        #子弹的类
bulletlist=[]
class bullet(pygame.sprite.Sprite):
    # 属性： 图片，屏幕，速度，  方法： 移动 ， 碰撞 ，
    def __init__(self,image,speed,screen,start):
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.center=start
        self.speed=speed
        self.screen=screen
        self.start=start
        bulletlist.append(self)

    #子弹移动
    def bulletmove(self):
        self.rect=self.rect.move(0,-self.speed)
        self.screen.blit(self.image,self.rect)

        if self.rect.y<0:
            if self in bulletlist:
                bulletlist.remove(self)
        #实时检测碰撞
        self.bullet_enemy()
    #子弹碰撞敌机
    def bullet_enemy(self):
        temp=pygame.sprite.spritecollideany(self,enemylist,pygame.sprite.collide_mask)
        if temp!=None:
            if self in bulletlist:
                bulletlist.remove(self)
            temp.hp-=1


    #所有子弹移动
    @staticmethod
    def allbulletmove():
        for i in bulletlist:
            i.bulletmove()

    def Collide(self):
        pass

        #敌机类
enemylist=[]
class enemy(pygame.sprite.Sprite):

    enemynum=0

    # 属性： 图片，屏幕，速度，血量
    def __init__(self,imgs,screen,speed,hp,start,tag):
        self.imgs=imgs
        self.image=imgs[0]
        self.rect=self.image.get_rect()
        self.rect.topleft=start
        self.screen=screen
        self.speed=speed
        self.hp=hp
        self.start=start
        self.tag=tag
        enemylist.append(self)
        self.x1=0
        self.x2=0
        self.x3=0
        self.index=1

    #敌机移动
    def enemy_move(self):
        if self.hp>0:
            self.rect=self.rect.move(0,self.speed)
            self.screen.blit(self.image,self.rect)
            #超出画面，销毁敌机
            if self.rect.y>900:
                if self in enemylist:
                    enemylist.remove(self)
        else:
            self.enemy_death()

    #随机产生敌机
    @staticmethod
    def random_enemy(screen):
        enemy.enemynum+=1
        if enemy.enemynum==50:
            enemy.enemynum=0
            ennum=random.randint(1,100)
            if ennum<=70:
                ttt=random.randint(1,3)
                if ttt==1:
                    enemy(enemyimage1,screen,5,1,(random.randint(0,400),-50),"enemy1")
                elif ttt==2:
                    enemy(enemyimage4,screen,5,1,(random.randint(0,400),-50),"enemy1")
                else:
                    enemy(enemyimage5,screen,5,1,(random.randint(0,400),-50),"enemy1")
            elif ennum<=90:
                enemy(enemyimage2,screen,4,3,(random.randint(0,350),-100),"enemy2")
            else:
                enemy(enemyimage3,screen,3,5,(random.randint(0,300),-200),"enemy3")

    @staticmethod
    def allenemy_movie():
        for i in enemylist:
            if i!=None and isinstance(i,enemy):
                i.enemy_move()

    def enemy_death(self):
        #死亡动画
        #积分累计
        if self in enemylist:
            self.x1+=1
            self.x2+=1
            self.x3+=1
            self.screen.blit(self.imgs[self.index],self.rect)
            if self.x1 % 17 == 0:
                self.index += 1
                self.x1 = 0
            if self.tag=="enemy1":
                heroA.score += 1
                enemylist.remove(self)
            elif self.tag=="enemy2":
                heroA.score += 3
                enemylist.remove(self)
            else:
                heroA.score += 10
                enemylist.remove(self)

        #字体类
class fontdisplay:
    history=0

    def __init__(self,font,size,screen):
        self.font=font
        self.size=size
        self.screen=screen

    def show_font(self,start,strA):
        tampFont=pygame.font.Font(self.font,self.size)
        fontSurface=tampFont.render(strA,True,pygame.Color("white"))
        self.screen.blit(fontSurface,start)

    @staticmethod
    def score_history(path="score.txt"):
        if os.path.exists(path):
            with open(path,"r") as f_r:
                fontdisplay.history=int(f_r.read())
        else:
            with open(path,"w") as f_w:
                f_w.write("0")
                fontdisplay.history=0

    @staticmethod
    def Update(score,path="score.txt"):
        if score>fontdisplay.history:
            with open(path,"w") as f_w:
                f_w.write(str(score))


        #全局变量
mousepanduan=False
gamemouse=(0,0)
b=0
mouseA=(170,700)
numzidan=0
countA=0
randomeatA=0

        #事件
def Event():
    global mousepanduan
    global gamemouse
    global b
    for event in pygame.event.get():
        #退出事件
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #判断鼠标
        if event.type==pygame.MOUSEBUTTONUP:
            # if pygame.mouse.get_pos()[0]<listgame.get_rect().centerx:

            gamemouse=pygame.mouse.get_pos()
            b=0
        if event.type==pygame.MOUSEBUTTONDOWN:
            if event.button==1:
                b=1
                a=pygame.Rect(210,400,72,72).collidepoint(pygame.mouse.get_pos())
                if a:
                    print("游戏开始")
                    fontdisplay.score_history()
                    enemylist.clear()
                    bulletlist.clear()
                    mousepanduan=True

        #判断键盘,键盘按下
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                mousepanduan=False

            if event.key==pygame.K_DOWN:
                heroA.down=True
            if event.key==pygame.K_UP:
                heroA.up=True
            if event.key==pygame.K_LEFT:
                heroA.left=True
            if event.key==pygame.K_RIGHT:
                heroA.right=True
        #判断键盘，键盘松开。
        if event.type==pygame.KEYUP:

            if event.key==pygame.K_DOWN:
                heroA.down=False
            if event.key==pygame.K_UP:
                heroA.up=False
            if event.key==pygame.K_LEFT:
                heroA.left=False
            if event.key==pygame.K_RIGHT:
                heroA.right=False

        #创建字体对象
Fontdisplay=fontdisplay("font/aassdd.ttf",25,screen)

        #创建开始界面对象
start=startface(listscreen,listbottom,screen)

        #创建游戏界面对象
game=gameface(gameload,screen,listgame,2)

        #创建英雄对象
herolist=[]
heroA=hero(listgame,7,3,mouseA,0,screen)



        #pygame时间计时
clock=pygame.time.Clock()

        #主流程
def main():
    global mousepanduan
    while True:

        Event()

        if mousepanduan==False:
            start.setstart_face()
        else:
            screen.fill(pygame.Color("Green"))
            #游戏界面
            game.show()
            #英雄移动
            heroA.heromove()
            #子弹发射
            bullet.allbulletmove()
            #敌机产生
            enemy.random_enemy(screen)
            #敌机全部移动
            enemy.allenemy_movie()
            Fontdisplay.show_font((10,10),"HP:%s"%heroA.hp)
            Fontdisplay.show_font((10,40),"分数:%s"%heroA.score)
            Fontdisplay.show_font((10,70),"历史最高:%s"%fontdisplay.history)
            #随机奖品产生
            random_eat.create_random(screen)
            random_eat.all_randommove()

        #重复画面
        pygame.display.update()
        clock.tick(60)
main()



