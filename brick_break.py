from PIL.Image import MODES
import pygame
import time
import random
from datetime import datetime
import keyboard
import pyautogui


pygame.init()
pygame.mixer.init()

size=[1000, 600]
screen=pygame.display.set_mode(size)
title="brick break"
pygame.display.set_caption(title)

clock=pygame.time.Clock()



black=(0,0,0)
white=(255,255,255)



class Object:
    def __init__(self):
        self.x=0
        self.y=0
        self.move=0
    def put_img(self,address):
        if address[-3:]=="png":
            self.image=pygame.image.load(address).convert_alpha()
        else:
            self.image=pygame.image.load(address)
        self.sx,self.sy=self.image.get_size()
    def change_size(self,sx,sy):
        self.image=pygame.transform.scale(self.image, (sx,sy))
        self.sx,self.sy=self.image.get_size()
    def show(self):
        screen.blit(self.image, (self.x,self.y))

def crash(a,b):
    if a.x-b.sx <= b.x <= a.x+a.sx and\
     a.y-b.sy <= b.y <= a.y+a.sy:
        return True
    else:
        return False


class Sound:
    def play(self,address):
        self.sound=pygame.mixer.music.load(address)
        pygame.mixer.music.play(-1)
    def stop(self):
        pygame.mixer.music.stop()

mode=0
def waiting_display():
    global mode
    while True:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    mode=0
                    return game()
                if keyboard.is_pressed("Enter"):
                    mode=1
                    return game()



        screen.fill(black)

        font=pygame.font.Font("C:\\Windows\\Fonts\\tahomabd.ttf",30)
        text_start=font.render("- choice controller -",True,(white))
        screen.blit(text_start,(size[0]/2-150,size[1]/2+50))
        font=pygame.font.Font("C:\\Windows\\Fonts\\vga949.fon",100)
        text_keyboard=font.render("mouse : press space_key",True,(white))
        screen.blit(text_keyboard,(200,size[1]/2+150))
        font=pygame.font.Font("C:\\Windows\\Fonts\\vga949.fon",100)
        text_mouse=font.render("keyboard : press enter_key",True,(white))
        screen.blit(text_mouse,(600,size[1]/2+150))
        font=pygame.font.Font("C:\\Windows\\Fonts\\tahomabd.ttf",60)
        text_brick_break=font.render("Brick Break",True,(white))
        screen.blit(text_brick_break,(327,size[1]/2-50))
        
        pygame.display.flip()

level=1
def game():
    background=Sound()
    background.play("C:\\Users\\user\\Downloads\\021914bgm2(happytune).mp3")

    stick=Object()
    stick.put_img("C:\\Users\\user\\Pictures\\Saved Pictures\\paddle.png")
    stick.change_size(250,30)
    stick.x=size[0]/2-stick.sx/2
    stick.y=size[1]-stick.sy
    stick.move=10
    ball=Object()
    ball.put_img("C:\\Users\\user\\Pictures\\Saved Pictures\\ball.png")
    ball.change_size(50,50)
    ball.x=size[0]/2-ball.sx/2
    ball.y=size[1]-80
    SB=0
    loading="loading"
    global level
    speed=10*+1
    next_level=40
    breaked=0
    while SB<4:
        clock.tick(60)
        SB+=1
        
        loading=loading+"."
        time.sleep(0.4)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()

        

        screen.fill(black)
        font=pygame.font.Font("C:\\Windows\\Fonts\\vga949.fon",100)
        text_lv=font.render("- LEVEL {} -".format(level),True,(white))
        screen.blit(text_lv,(size[0]/2-50,size[1]/2-20))

        font=pygame.font.Font("C:\\Windows\\Fonts\\vga949.fon",100)
        text_loading=font.render("{}".format(loading),True,(white))
        screen.blit(text_loading,(size[0]/2-50,size[1]/2+20))


        pygame.display.flip()


    start_time=datetime.now()



    brick_list=[]
    for i in range(0,4):
            for j in range(0,10):
                brick=Object()
                brick.put_img("C:\\Users\\user\\Pictures\\Saved Pictures\\벽돌.png")
                brick.change_size(100,40)
                brick.x=0+j*100
                brick.y=0+i*40
                brick_list.append(brick)


    left_go=False
    right_go=False
    r=0
    y=0
    tick=0

    now_position=pyautogui.position()
    next_position=0


    while True:
        clock.tick(120)
        now_time=datetime.now()
        delta_time=round((now_time-start_time).total_seconds())
        global mode
        if mode==0:
            if tick==0:
                tick=1
            else:
                tick=0

            now_position=pyautogui.position()[0]*2.5
            if tick==1:
                next_position=pyautogui.position()[0]*2.5
            stick.x-=next_position-now_position
            if stick.x<=0:
                stick.x=0
            if stick.x>=size[0]-stick.sx:
                stick.x=size[0]-stick.sx


        else:
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    left_go=True
                if event.key==pygame.K_RIGHT:
                    right_go=True
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_LEFT:
                    left_go=False
                if event.key==pygame.K_RIGHT:
                    right_go=False

            if left_go==True:
                stick.x-=stick.move
                if stick.x<=0:
                        stick.x=0
            elif right_go==True:
                stick.x+=stick.move
                if stick.x>=size[0]-stick.sx:
                    stick.x=size[0]-stick.sx

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()

        if crash(ball,stick)==True:
            r=random.randrange(-(speed-5),speed-5)     
            y=1
        db_list=[]
        if ball.y>=0:
            if y==1:
                ball.y-=speed-abs(r)
                ball.x+=r
                for i in range(len(brick_list)):
                    b=brick_list[i]
                    if crash(ball,b)==True:
                        y=0
                        db_list.append(i)

                db_list=list(set(db_list))
                db_list.reverse()
                try:
                    for db in db_list:
                        del brick_list[db]
                        breaked+=1
                        if breaked>=40:
                            level+=1
                            return game()
                except:
                    pass
                    

                if ball.x<=0:
                    r=-r
                elif ball.x>=size[0]-ball.sx:
                    r=-r      
        else:
            y=0
        if y==0:
            db_list=[]
            for i in range(len(brick_list)):
                b=brick_list[i]
                if crash(ball,b)==True:
                    y=0
                    db_list.append(i)

            db_list=list(set(db_list))
            db_list.reverse()
            try:
                for db in db_list:
                    del brick_list[db]
                    breaked+=1
                    if breaked>=40:
                        level+=1
                        return game()
            except:
                pass
            if ball.x<=0:
                    r=-r
            elif ball.x>=size[0]-ball.sx:
                r=-r
            ball.y+=speed-abs(r)
            ball.x+=r
            if ball.y+ball.sy>=size[1]:
                gameover()


        screen.fill(black)
        for b in brick_list:
            b.show()
        ball.show()
        stick.show()

        font=pygame.font.Font("C:\\Windows\\Fonts\\vga949.fon",20)
        text_breaked=font.render("breaked:{}/{}".format(breaked,next_level),True,(255,255,255))
        screen.blit(text_breaked,(size[0]-120,0))
        font=pygame.font.Font("C:\\Windows\\Fonts\\vga949.fon",20)
        text_level=font.render("level:{}".format(level),True,(255,255,255))
        screen.blit(text_level,(size[0]-200,0))
        font=pygame.font.Font("C:\\Windows\\Fonts\\vga949.fon",20)
        text_time=font.render("time:{}".format(delta_time),True,(255,255,255))
        screen.blit(text_time,(10,0))


        pygame.display.flip()


def gameover():
    sadness=Sound()
    sadness.play("C:\\Users\\user\\Downloads\\Sadness.ogg")
    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()

            if keyboard.is_pressed("Enter"):
                level=1
                sadness.stop()
                return game()
            

        font=pygame.font.Font("C:\\Windows\\Fonts\\tahomabd.ttf",40)
        text_go=font.render("- GAME OVER -",True,(white))
        screen.blit(text_go,(size[0]/2-150,size[1]/2-20))


        font=pygame.font.Font("C:\\Windows\\Fonts\\vga949.fon",20)
        text_re=font.render("PRESS THE ENTER KEY TO PLAY THE GAME AGAIN",True,(255,255,255))
        screen.blit(text_re,(size[0]/2-173,size[1]/2+50))

        pygame.display.flip()

waiting_display()