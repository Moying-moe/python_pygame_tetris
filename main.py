from random import randint
import sys
import os
import pygame
from pygame.locals import *
#辣鸡pygame就决定是你了！
import pickle as pkl

__author__ = '墨滢'


#############################################
C_BLACK = 0,0,0
C_WHITE = 255,255,255
C_RED = 255,0,0
C_GREEN = 0,255,0
C_BLUE = 0,0,255
C_YELLOW = 255,255,0

S_MENU = 1
S_GAME = 2
S_SCORE = 3
S_AUTHOR = 4
#############################################


def deepcopy(listname):
    #深度复制list
    temp = []
    for each in listname:
        if isinstance(each, list):
            temp.append(deepcopy(each))
        else:
            temp.append(each)
    return temp


##############################################

def moveabs(d):
    data = deepcopy(d)
    #管他用不用deep 上来先搞一发
    i = -1
    while True:#复杂条件
        i += 1
        if data[i][0] < 0:
            #x有负数
            for e in range(len(data)):
                data[e] = data[e][0] + 1, data[e][1]
            i = -1
            continue
        if data[i][1] < 0:
            #y有负数
            for e in range(len(data)):
                data[e] = data[e][0], data[e][1] + 1
            i = -1
            continue
        if i == len(data) - 1:
            break
    return data

def roll(d, times):
    data = deepcopy(d)
    for i in range(times):
        #规定为 逆时针旋转 试图套用旋转矩阵公式
        temp = []
        for each in data:
            x = each[1]
            y = -each[0]
            temp.append((x,y))
        data = deepcopy(temp)
    return moveabs(data)

def drSqua(color):
    #一个方块大概25x25(px)
    surtemp = pygame.Surface((25,25))
    surtemp.fill(color)
    pygame.draw.lines(surtemp, C_BLACK, True, [(0,0), (23,0), (23,23), (0,23)], 2)
    return surtemp

'''
moveabs  把整体移动让它没有负数
roll     总之就是转转转
'''


            
#I(1x4) J L O T S Z
class Shape:
    def __init__(self, pos, coll):
        self.pos = pos
        self.coll = coll
        xmax = 0
        ymax = 0
        for each in coll:
            if each[0] > xmax:
                xmax = each[0]
            if each[1] > ymax:
                ymax = each[1]
        surtemp = pygame.Surface((25*(xmax+1), 25*(ymax+1)))
        surtemp.fill(C_WHITE)
        temp = drSqua(C_GREEN)
        for each in self.coll:
            surtemp.blit(temp, (25*each[0], 25*each[1]))
        surtemp.set_colorkey(C_WHITE)
        self.pic = surtemp

    def judcoll(self, x, y):
        newpos = self.pos[0] + x, self.pos[1] + y
        for c in self.coll:
            x = newpos[0] + c[0]
            y = newpos[1] + c[1]
            if not(0 <= x <= 9 and 0 <= y <= 19):
                #出界
                return True
            elif maps[y][x] != 0:
                #碰撞
                return True
        return False

    def rolls(self, times):
        self.coll = roll(self.coll, times)
        return None

    def addmap(self):
        'pos为左上角坐标 coll储存着每一个方块相对于左上角坐标的相对坐标'
        '那么 pos+coll(each) 就是他的绝对坐标了'
        temp = []
        for each in self.coll:
            x, y  = self.pos[0] + each[0], self.pos[1] + each[1]
            temp.append((x,y))
        return temp

    
class Ishape(Shape):
    def __init__(self, pos):
        super().__init__(pos, [(0,0), (0,1), (0,2), (0,3)])

class Jshape(Shape):
    def __init__(self, pos):
        super().__init__(pos, [(1,0), (1,1), (1,2), (0,2)])
        
class Lshape(Shape):
    def __init__(self, pos):
        super().__init__(pos, [(0,0), (0,1), (0,2), (1,2)])

class Oshape(Shape):
    def __init__(self, pos):
        super().__init__(pos, [(0,0), (0,1), (0,2), (1,2)])

class Tshape(Shape):
    def __init__(self, pos):
        super().__init__(pos, [(0,0), (1,0), (2,0), (1,1)])

class Sshape(Shape):
    def __init__(self, pos):
        super().__init__(pos, [(1,0), (2,0), (0,1), (1,1)])

class Zshape(Shape):
    def __init__(self, pos):
        super().__init__(pos, [(0,0), (1,0), (1,1), (2,1)])


tran = (Ishape, Jshape, Lshape ,Oshape ,Tshape ,Sshape ,Zshape)


#类应该写好了 接下来试试看写主体
#因为调试比较困难 到时候出BUG再说_(:3」∠)_

#如果没有存档就创建一个
if not os.path.exists('score.dat'):
    with open('score.dat', 'wb') as f:
        pkl.dump([0]*10, f)

pygame.init()
screen = pygame.display.set_mode((400, 550))
pygame.display.set_caption('俄罗斯方块 - demo')
clock = pygame.time.Clock()

b_sta = pygame.Surface((100,65))
b_sta.fill(C_WHITE)
pygame.draw.lines(b_sta, C_BLACK, True, ((3,3), (97,3), (97,62), (3,62)), 3)
pygame.draw.polygon(b_sta, C_GREEN, ((35,15), (35,50), (70,33)), 0)
br_sta = b_sta.get_rect()
br_sta.center = 120, 330

b_exit = pygame.Surface((100,65))
b_exit.fill(C_WHITE)
pygame.draw.lines(b_exit, C_BLACK, True, ((3,3), (97,3), (97,62), (3,62)), 3)
pygame.draw.line(b_exit, C_RED, (32,15), (67,50), 5)
pygame.draw.line(b_exit, C_RED, (32,50), (67,15), 5)
br_exit = b_exit.get_rect()
br_exit.center = 280, 330


font = pygame.font.Font('simhei.ttf', 30)
nextt = font.render('NEXT', True, C_BLACK)
nexttr = nextt.get_rect()
nexttr.center = 328, 65

scoret = font.render('SCORE', True, C_BLACK)
scoretr = scoret.get_rect()
scoretr.center = 328, 205

font = pygame.font.Font('simhei.ttf', 15)
newre = font.render('NEW RECORD!', True, C_WHITE)
temp = newre.get_rect()
w, h = temp.width+10, temp.height+6
temp = pygame.Surface((temp.width+10, temp.height+6))
temp.fill(C_RED)
pygame.draw.lines(temp, C_YELLOW, True,\
                  ((1,1), (w-2,1), (w-2,h-2), (1,h-2)), 3)
temp.blit(newre, (8,3))
newre = temp.convert_alpha()
del temp

font = pygame.font.Font('simhei.ttf', 50)
title = font.render('俄罗斯方块', True, C_BLACK)
titr = title.get_rect()
titr.center = 200, 130

gmov = font.render('GAME OVER', True, C_WHITE)
gmovr = gmov.get_rect()
gmovr.center = 200, 130

pause = pygame.Surface((400, 550))
pause.fill(C_WHITE)
temp = font.render('PAUSE', True, C_BLACK)
tempr = temp.get_rect()
tempr.center = 200, 250
pause.blit(temp, tempr)
pause.set_alpha(200)

font = pygame.font.Font('simhei.ttf', 25)
font2 = pygame.font.Font('simhei.ttf', 30)
#是画方格还是用png资源……  还是画吧
#完成了pic部分 接下来做游戏体


'变量'
maps = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
droping = False
dropt = None
delay = 0
score = 0
nexti = randint(0, 6)
spddown = False
newr = False
run = 1
state = S_MENU  #用state变量标注当前处于的阶段 啊啊啊就这么理解！


'主体'
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and state == S_GAME:
            if event.key == K_q:
                pygame.quit()
                sys.exit()
            elif event.key == K_UP and run:
                dropt.coll = roll(dropt.coll, 1)
                if dropt.judcoll(0,0):
                    dropt.coll = roll(dropt.coll, 3)
                    #打扰了
                else:
                    dropt.pic = pygame.transform.rotate(dropt.pic, 90)
            elif event.key == K_DOWN and run:
                spddown = True
                delay = 59
            elif event.key == K_LEFT and run:
                if dropt != None:
                    if not dropt.judcoll(-1,0):
                        dropt.pos[0] -= 1
            elif event.key == K_RIGHT and run:
                if dropt != None:
                    if not dropt.judcoll(1,0):
                        dropt.pos[0] += 1
            elif event.key == K_SPACE:
                if run:
                    run = 0
                else:
                    run = 1
        elif event.type == KEYUP and state == S_GAME:
            if event.key == K_DOWN:
                spddown = False
        elif event.type == MOUSEBUTTONDOWN and state == S_MENU:
            if br_sta.left <= event.pos[0] <= br_sta.right and \
               br_sta.top <= event.pos[1] <= br_sta.bottom:
                state = S_GAME
                newr = False
            elif br_exit.left <= event.pos[0] <= br_exit.right and \
                 br_exit.top <= event.pos[1] <= br_sta.bottom:
                pygame.quit()
                sys.exit()
        elif event.type == MOUSEBUTTONDOWN and state == S_SCORE:
            if br_sta.left <= event.pos[0] <= br_sta.right and \
               br_sta.top <= event.pos[1] <= br_sta.bottom:
                maps = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
                droping = False
                dropt = None
                delay = 0
                score = 0
                nexti = randint(0, 6)
                spddown = False
                newr = False
                state = S_GAME
            elif br_exit.left <= event.pos[0] <= br_exit.right and \
                 br_exit.top <= event.pos[1] <= br_sta.bottom:
                pygame.quit()
                sys.exit()
            #print(event.pos)

    screen.fill(C_WHITE)
    if state == S_MENU:
        screen.blit(title, titr)
        screen.blit(b_sta, br_sta)
        screen.blit(b_exit, br_exit)
        

    elif state == S_SCORE:
        pygame.draw.lines(screen, C_BLACK, True, [(0,0), (250,0), (250,500), (0,500)], 2)
        screen.blit(dropt.pic, (dropt.pos[0] * 25, dropt.pos[1] * 25))
        for y in range(len(maps)):
            for x in range(len(maps[y])):
                if maps[y][x] == 1:
                    #有方块
                    screen.blit(drSqua(C_BLUE), (25 * x, 25 * y))
        screen.blit(b_sta, br_sta)
        screen.blit(b_exit, br_exit)
        pygame.draw.polygon(screen, C_BLACK, \
            ((gmovr.left,gmovr.top),(gmovr.left,gmovr.bottom),\
             (gmovr.right,gmovr.bottom),(gmovr.right,gmovr.top)), 0)
        screen.blit(gmov, gmovr)
        pygame.draw.polygon(screen, C_BLACK, \
            ((overscore_r.left,overscore_r.top),(overscore_r.left,overscore_r.bottom),\
             (overscore_r.right,overscore_r.bottom),(overscore_r.right,overscore_r.top)), 0)
        screen.blit(overscore, overscore_r)
        temp = newre.get_rect()
        temp.center = overscore_r.center
        temp.top = overscore_r.bottom+10
        screen.blit(newre, temp)
    
    elif state == S_GAME:
        delay += run
        
        if spddown and not(delay%6):
            delay = 60

        if not droping:
            #生成新的方块
            dropt = tran[nexti]([4,0])
            nexti = randint(0, 6)
            droping = True

        if delay == 60:
            delay = 0
                
            if dropt.judcoll(0,1):
                #判断game over
                if dropt.pos[1] == 0:#一出来就
                    with open('score.dat', 'rb') as f:
                        top10 = pkl.load(f)
                    if score > min(top10):
                        for i in range(len(top10)):
                            if score >= top10[i]:
                                top10.insert(i, score)
                                del top10[10]
                                break
                        with open('score.dat', 'wb') as f:
                            pkl.dump(top10, f)
                        newr = True
                    overscore = font2.render('SCORE:%s'%score, True, C_WHITE)
                    overscore_r = overscore.get_rect()
                    overscore_r.center = 200, 200
                    state = S_SCORE
                    #暂时直接退出 后面做结算画面
                    
                #落到面上了
                for each in dropt.addmap():
                    maps[each[1]][each[0]] = 1

                #判断是否有一整行
                dellist = []
                for l in range(20):
                    #print(maps[l],flag)
                    if maps[l] == [1]*10:
                        dellist.append(l)
                        score += 1
                for each in dellist:
                    del maps[each]
                    maps.insert(0, [0,0,0,0,0,0,0,0,0,0])
                

                droping = False
            else:
                dropt.pos[1] += 1
            #print(dropt.pos)

        #边框
        pygame.draw.lines(screen, C_BLACK, True, [(0,0), (250,0), (250,500), (0,500)], 2)
        pygame.draw.lines(screen, C_BLACK, True, [(265,50), (390,50), (390,185), (265,185)], 2)
        pygame.draw.line(screen, C_BLACK, (265,80), (390,80), 1)
        screen.blit(nextt, nexttr)

        pygame.draw.lines(screen, C_BLACK, True, [(265,190), (390,190), (390,250), (265,250)], 2)
        screen.blit(scoret, scoretr)

        sct = font.render(str(score), True, C_BLACK)
        sctr = sct.get_rect()
        sctr.center = 328, 230
        screen.blit(sct, sctr)
        
        temp = tran[nexti]((0,0)).pic
        tempr = temp.get_rect()
        tempr.center = 328, 132
        screen.blit(temp, tempr)
        del temp, tempr
        
        screen.blit(dropt.pic, (dropt.pos[0] * 25, dropt.pos[1] * 25))
        for y in range(len(maps)):
            for x in range(len(maps[y])):
                if maps[y][x] == 1:
                    #有方块
                    screen.blit(drSqua(C_BLUE), (25 * x, 25 * y))
            #screen.blit(each.pic, (each.pos[0] * 25, each.pos[1] * 25))
        if not run:
            screen.blit(pause, (0,0))
    pygame.display.flip()
    clock.tick(60)





pass
