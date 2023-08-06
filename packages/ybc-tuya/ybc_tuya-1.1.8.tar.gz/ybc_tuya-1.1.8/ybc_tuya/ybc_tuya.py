#coding: utf-8
from turtle import *
from PIL import ImageGrab

def rgb(r=255,g=255,b=255):
    if r > 255:
        r = 255
    if g > 255:
        g = 255
    if b > 255:
        b = 255
    list = [r,g,b]
    output = "#"
    for x in list: 
     intx = int(x)
     if intx < 16:
      output = output + '0' + hex(intx)[2:]
     else:
      output = output + hex(intx)[2:] 
    return output


# def rbg10to16(rbg='255,255,255'):
#     list= rbg.split(',')
#     if len(list) != 3:
#         list = [255,255,255]
#     output = "#"
#     for x in list: 
#      intx = int(x)
#      if intx < 16:
#       output = output + '0' + hex(intx)[2:]
#      else:
#       output = output + hex(intx)[2:] 
#     return output


def canvas(bg=rgb(255,255,255)):
	screensize(400,300,bg)
	setup(800,600)

def ruler(size=100,color='#F0F0F0'):
	pencolor(color)
	speed(0)
	x = -398
	y = 298
	right(90)
	while x < 400 + size:
		penup()
		goto(x,298)
		pendown()
		forward(600)
		x = x + size
	left(90)
	while y > -300 - size:
		penup()
		goto(-398,y)
		pendown()
		forward(800)
		y = y - size
	speed(3)
	pencolor('black')

def my_goto(x, y):
	x = x - 398
	if y <= 298:
		y = 298 - y
	else:
		y = -(y-298)
	penup()
	goto(x, y)
	pendown()

def hide():
	hideturtle()

def clean():
	reset()
# def show():
# 	showturtle()

def stop():
	hide()
	mainloop()


def pen_size(x=6):
    pensize(x)

def pen_color(color='black'):
	pencolor(color)

def pen_speed(x=3):
	speed(x)


def draw_circle(x,y,size):
	y = y + size
	my_goto(x,y)
	circle(size)

def fill_circle(x=400,y=300,size=40,bg='gray'):
	fillcolor(bg)
	_beginf()
	y = y + size
	my_goto(x,y)
	circle(size)
	_endf()
	hide()

def draw_rect(x,y,width,height):

	my_goto(x,y)
	forward(width)
	right(90)
	forward(height)
	right(90)
	forward(width)
	right(90)
	forward(height)
	right(90)

def fill_rect(x=360, y=260, width=80, height=80,bg='gray'):
	fillcolor(bg)
	_beginf()
	my_goto(x,y)
	forward(width)
	right(90)
	forward(height)
	right(90)
	forward(width)
	right(90)
	forward(height)
	right(90)
	_endf()
	hide()

def fill_color(color='white'):
	fillcolor(color)

def _beginf():
	begin_fill()

def _endf():
	end_fill()




#####################################
###############截图#################
#####################################

def save(name='1.png'):
	pic = ImageGrab.grab()
	pic.save(name)

#####################################
###############机器猫#################
#####################################

# 无轨迹跳跃
def mao_goto(x, y):
    penup()
    goto(x, y)
    pendown()

# 眼睛
def eyes():
    fillcolor("#ffffff")
    begin_fill()

    tracer(False)
    a = 2.5
    for i in range(120):
        if 0 <= i < 30 or 60 <= i < 90:
            a -= 0.05
            lt(3)
            fd(a)
        else:
            a += 0.05
            lt(3)
            fd(a)
    tracer(True)
    end_fill()


# 胡须
def beard():
    mao_goto(-32, 135)
    seth(165)
    fd(60)

    mao_goto(-32, 125)
    seth(180)
    fd(60)

    mao_goto(-32, 115)
    seth(193)
    fd(60)

    mao_goto(37, 135)
    seth(15)
    fd(60)

    mao_goto(37, 125)
    seth(0)
    fd(60)

    mao_goto(37, 115)
    seth(-13)
    fd(60)

# 嘴巴
def mouth():
    mao_goto(5, 148)
    seth(270)
    fd(100)
    seth(0)
    circle(120, 50)
    seth(260)
    circle(-120, 100)

# 围巾
def scarf():
    fillcolor('#e70010')
    begin_fill()
    seth(0)
    fd(200)
    circle(-5, 90)
    fd(10)
    circle(-5, 90)
    fd(207)
    circle(-5, 90)
    fd(10)
    circle(-5, 90)
    end_fill()

# 鼻子
def nose():
    mao_goto(-10, 158)
    seth(315)
    fillcolor('#e70010')
    begin_fill()
    circle(20)
    end_fill()

# 黑眼睛
def black_eyes():
    seth(0)
    mao_goto(-20, 195)
    fillcolor('#000000')
    begin_fill()
    circle(13)
    end_fill()

    pensize(6)
    mao_goto(20, 205)
    seth(75)
    circle(-10, 150)
    pensize(3)

    mao_goto(-17, 200)
    seth(0)
    fillcolor('#ffffff')
    begin_fill()
    circle(5)
    end_fill()
    mao_goto(0, 0)



# 脸
def face():

    fd(183)
    lt(45)
    fillcolor('#ffffff')
    begin_fill()
    circle(120, 100)
    seth(180)
    # print(pos())
    fd(121)
    pendown()
    seth(215)
    circle(120, 100)
    end_fill()
    mao_goto(63.56,218.24)
    seth(90)
    eyes()
    seth(180)
    penup()
    fd(60)
    pendown()
    seth(90)
    eyes()
    penup()
    seth(180)
    fd(64)

# 头型
def head():
    mao_goto(0, 0)
    penup()
    circle(150, 40)
    pendown()
    fillcolor('#00a0de')
    begin_fill()
    circle(150, 280)
    end_fill()

# 画哆啦A梦
def Doraemon():
    # 头部
    head()

    # 围脖
    scarf()

    # 脸
    face()

    # 红鼻子
    nose()

    # 嘴巴
    mouth()

    # 胡须
    beard()

    # 身体
    mao_goto(0, 0)
    seth(0)
    penup()
    circle(150, 50)
    pendown()
    seth(30)
    fd(40)
    seth(70)
    circle(-30, 270)


    fillcolor('#00a0de')
    begin_fill()

    seth(260)
    fd(80)
    seth(90)
    circle(1000, 1)
    seth(-89)
    circle(-1000, 10)

    # print(pos())

    seth(180)
    fd(70)
    seth(90)
    circle(30, 180)
    seth(180)
    fd(70)

    # print(pos())
    seth(100)
    circle(-1000, 9)

    seth(-86)
    circle(1000, 2)
    seth(260)
    fd(40)

    # print(pos())


    circle(-30, 260)
    seth(45)
    fd(81)
    seth(0)
    fd(203)
    circle(5, 90)
    fd(10)
    circle(5, 90)
    fd(7)
    seth(40)
    circle(150, 10)
    seth(30)
    fd(40)
    end_fill()

    # 左手
    seth(70)
    fillcolor('#ffffff')
    begin_fill()
    circle(-30)
    end_fill()

    # 脚
    mao_goto(103.74, -182.59)
    seth(0)
    fillcolor('#ffffff')
    begin_fill()
    fd(15)
    circle(-15, 180)
    fd(90)
    circle(-15, 180)
    fd(10)
    end_fill()

    mao_goto(-96.26, -182.59)
    seth(180)
    fillcolor('#ffffff')
    begin_fill()
    fd(15)
    circle(15, 180)
    fd(90)
    circle(15, 180)
    fd(10)
    end_fill()

    # 右手
    mao_goto(-133.97, -91.81)
    seth(50)
    fillcolor('#ffffff')
    begin_fill()
    circle(30)
    end_fill()

    # 口袋
    mao_goto(-103.42, 15.09)
    seth(0)
    fd(38)
    seth(260)
    begin_fill()
    circle(90, 260)
    end_fill()

    mao_goto(5, -40)
    seth(0)
    fd(70)
    seth(-90)
    circle(-70, 180)
    seth(0)
    fd(70)

    #铃铛
    mao_goto(-103.42, 15.09)
    fd(90)
    seth(70)
    fillcolor('#ffd200')
    # print(pos())
    begin_fill()
    circle(-20)
    end_fill()
    seth(170)
    fillcolor('#ffd200')
    begin_fill()
    circle(-2, 180)
    seth(10)
    circle(-100, 22)
    circle(-2, 180)
    seth(180-10)
    circle(100, 22)
    end_fill()
    goto(-13.42, 15.09)
    seth(250)
    circle(20, 110)
    seth(90)
    fd(15)
    dot(10)
    mao_goto(0, -150)

    # 画眼睛
    black_eyes()

def jiqimao():
    # screensize(800,600, "#f0f0f0")
    pensize(3)  # 画笔宽度
    speed(9)    # 画笔速度
    Doraemon()
    mao_goto(100, -260)
    write('BY YBC', font=("Bradley Hand ITC", 30, "bold"))
    stop()


#####################################
###############小猪佩奇#################
#####################################


def nose_xzpq(x=-100,y=100,pc='#FF9BC0',fc='#A0522D'):#鼻子
    pu()
    goto(x,y)
    pd()
    seth(-30)
    begin_fill()
    a=0.4
    for i in range(120):
        if 0<=i<30 or 60<=i<90:
            a=a+0.08
            lt(3) #向左转3度
            fd(a) #向前走a的步长
        else:
            a=a-0.08
            lt(3)
            fd(a)
    end_fill()

    pu()
    seth(90)
    fd(25)
    seth(0)
    fd(10)
    pd()
    pencolor(pc)
    seth(10)
    begin_fill()
    circle(5)
    color(fc)
    end_fill()

    pu()
    seth(0)
    fd(20)
    pd()
    pencolor(pc)
    seth(10)
    begin_fill()
    circle(5)
    color(fc)
    end_fill()


def head_xzpq(x=-69,y=167,pc='#FF9BC0',fc='pink'):#头
    color(pc,fc)
    pu()
    goto(x,y)
    seth(0)
    pd()
    begin_fill()
    seth(180)
    circle(300,-30)
    circle(100,-60)
    circle(80,-100)
    circle(150,-20)
    circle(60,-95)
    seth(161)
    circle(-300,15)
    pu()
    goto(-100,100)
    pd()
    seth(-30)
    a=0.4
    for i in range(60):
        if 0<=i<30 or 60<=i<90:
            a=a+0.08
            lt(3) #向左转3度
            fd(a) #向前走a的步长
        else:
            a=a-0.08
            lt(3)
            fd(a)
    end_fill()


def ears_xzpq(x=0,y=160,pc='#FF9BC0',fc='pink'): #耳朵
    color(pc,fc)
    pu()
    goto(x,y)
    pd()
    begin_fill()
    seth(100)
    circle(-50,50)
    circle(-10,120)
    circle(-50,54)
    end_fill()

    pu()
    seth(90)
    fd(-12)
    seth(0)
    fd(30)
    pd()
    begin_fill()
    seth(100)
    circle(-50,50)
    circle(-10,120)
    circle(-50,56)
    end_fill()


def eyes_xzpq(x=0,y=140,pc='#FF9BC0',fc='black'):#眼睛
    color(pc,'white')
    pu()
    seth(90)
    fd(-20)
    seth(0)
    fd(-95)
    pd()
    begin_fill()
    circle(15)
    end_fill()

    color(fc)
    pu()
    seth(90)
    fd(12)
    seth(0)
    fd(-3)
    pd()
    begin_fill()
    circle(3)
    end_fill()

    color(pc,'white')
    pu()
    seth(90)
    fd(-25)
    seth(0)
    fd(40)
    pd()
    begin_fill()
    circle(15)
    end_fill()

    color(fc)
    pu()
    seth(90)
    fd(12)
    seth(0)
    fd(-3)
    pd()
    begin_fill()
    circle(3)
    end_fill()


def cheek_xzpq(x=80,y=10,pc='#FF9BC0',fc='#FF9BC0'):#腮
    color(pc,fc)
    pu()
    goto(x,y)
    pd()
    seth(0)
    begin_fill()
    circle(30)
    end_fill()


def mouth_xzpq(x=-20,y=30,pc='#EF4513'): #嘴
    color(pc)
    pu()
    goto(x,y)
    pd()
    seth(-80)
    circle(30,40)
    circle(40,80)


def body_xzpq(x=-32,y=-8,pc='red',fc='#FF6347'):#身体
    color(pc,fc)
    pu()
    goto(x,y)
    pd()
    begin_fill()
    seth(-130)
    circle(100,10)
    circle(300,30)
    seth(0)
    fd(260)
    seth(90)
    circle(300,30)
    circle(100,3)
    color((255,155,192),(255,100,100))
    seth(-135)
    circle(-80,63)
    circle(-150,24)
    end_fill()


def hands_xzpq(x=-56,y=-45,pc='#FF9BC0',fc='#FF9BC0'):#手
    color(pc,fc)
    pu()
    goto(x,y)
    pd()
    seth(-160)
    circle(300,15)
    pu()
    seth(90)
    fd(15)
    seth(0)
    fd(0)
    pd()
    seth(-10)
    circle(-20,90)

    pu()
    seth(90)
    fd(30)
    seth(0)
    fd(237)
    pd()
    seth(-20)
    circle(-300,15)
    pu()
    seth(90)
    fd(20)
    seth(0)
    fd(0)
    pd()
    seth(-170)
    circle(20,90)

def foot_xzpq(x=2,y=-177,pc='#F08080',fc='#black'):#脚
    pensize(10)
    color(pc)
    pu()
    goto(x,y)
    pd()
    seth(-90)
    fd(40)
    seth(-180)
    color(fc)
    pensize(15)
    fd(20)

    pensize(10)
    color(pc)
    pu()
    seth(90)
    fd(40)
    seth(0)
    fd(90)
    pd()
    seth(-90)
    fd(40)
    seth(-180)
    color(fc)
    pensize(15)
    fd(20)

def tail_xzpq(x=148,y=-155,pc='#FF9BC0',fc='#FF9BC0'):#尾巴
    pensize(4)
    color(pc,fc)
    pu()
    goto(x,y)
    pd()
    seth(0)
    circle(70,20)
    circle(10,330)
    circle(70,30)

def setting(fc='pink'):          #参数设置
    pensize(4)
    hideturtle()
    colormode(255)
    color((255,155,192),fc)
    # setup(840,500)
    speed(6)


def xzpq_nose(color='pink'):
    setting(fc=color)          
    nose_xzpq(fc=color)      

def xzpq_head(color='pink'):
    head_xzpq(fc=color)    

def xzpq_ears(color='pink'):
    ears_xzpq(fc=color) 

def xzpq_eyes(color='black'):
    eyes_xzpq(fc=color) 

def xzpq_cheek(color='#FF9BC0'):
    cheek_xzpq(fc=color) 

def xzpq_mouth(color='#EF4513'):
    mouth_xzpq(pc=color) 

def xzpq_body(color='#FF6347'):
    body_xzpq(fc=color) 

def xzpq_hands(color='#FF9BC0'):
    hands_xzpq(fc=color) 

def xzpq_foot(color='black'):
    foot_xzpq(fc=color) 

def xzpq_tail(color='#FF9BC0'):
    tail_xzpq(fc=color) 

#小猪佩奇
def xzpq():
    xzpq_nose()      #鼻子
    xzpq_head()       #头
    xzpq_ears()         #耳朵
    xzpq_eyes()         #眼睛
    xzpq_cheek()        #腮
    xzpq_mouth()       #嘴
    xzpq_body()        #身体
    xzpq_hands()      #手
    xzpq_foot()        #脚
    xzpq_tail()      #尾巴
    done()              #结束


#####################################
###############美国队长盾牌############
#####################################

def shield_c1(c='red'):
    # 第一个圆
    color(c)
    fillcolor()
    begin_fill()
    r = 190
    penup()
    right(90)
    forward(r)
    pendown()
    left(90)
    circle(r)
    end_fill()
    penup()
    left(90)
    forward(r)
    right(90)    

def shield_c2(c='white'):
    # 第二个圆
    color(c)
    fillcolor()
    begin_fill()
    r = 147
    penup()
    right(90)
    forward(r)
    pendown()
    left(90)
    circle(r)
    end_fill()
    penup()
    left(90)
    forward(r)
    right(90)  

def shield_c3(c='red'):
    # 第三个圆
    color(c)
    fillcolor()
    begin_fill()
    r = 106.5
    penup()
    right(90)
    forward(r)
    pendown()
    left(90)
    circle(r)
    end_fill()
    penup()
    left(90)
    forward(r)
    right(90)  

def shield_c4(c='blue'):
    # 第三个圆
    color(c)
    fillcolor()
    begin_fill()
    r = 62
    penup()
    right(90)
    forward(r)
    pendown()
    left(90)
    circle(r)
    end_fill()
    penup()
    left(90)
    forward(r)
    right(90)  

def shield_star(c='white'):
    # 完成五角星
    r = 62
    penup()
    left(90)
    forward(r)
    right(90)
    left(288)
    pendown()
    long_side = 45.05
    color(c)
    fillcolor()
    begin_fill()
    for i in range(10):
        forward(long_side)
        if i % 2 == 0:
            left(72)
        else:
            right(144)
    end_fill()
    penup()
    hideturtle() 

#美国队长盾牌
def shield():
    shield_c1()   
    shield_c2()
    shield_c3()
    shield_c4()
    shield_star()
    stop()

#####################################
###############彩虹###################
#####################################


def rainbow_c1(c='red'):
    # speed('fastest')

    penup()
    forward(300)
    pendown()

    color(c)
    left(90)
    begin_fill()
    circle(300,180)
    end_fill()   

def rainbow_c2(c='orange'):
    left(90)
    forward(20)
    left(90)
    color(c)
    begin_fill()
    circle(-280,180)
    end_fill() 

def rainbow_c3(c='yellow'):
    right(90)
    forward(20)
    right(90)
    color(c)
    begin_fill()
    circle(260,180)
    end_fill() 

def rainbow_c4(c='green'):
    left(90)
    forward(20)
    left(90)
    color(c)
    begin_fill()
    circle(-240,180)
    end_fill() 

def rainbow_c5(c='cyan'):
    right(90)
    forward(20)
    right(90)
    color(c)
    begin_fill()
    circle(220,180)
    end_fill() 

def rainbow_c6(c='blue'):
    left(90)
    forward(20)
    left(90)
    color(c)
    begin_fill()
    circle(-200,180)
    end_fill() 

def rainbow_c7(c='purple'):
    right(90)
    forward(20)
    right(90)
    color(c)
    begin_fill()
    circle(180,180)
    end_fill() 

def rainbow_c8(c='white'):
    left(90)
    forward(20)
    left(90)
    color(c)
    begin_fill()
    circle(-160,180)
    end_fill()

#彩虹
def rainbow():
    rainbow_c1()
    rainbow_c2()
    rainbow_c3()
    rainbow_c4()
    rainbow_c5()
    rainbow_c6()
    rainbow_c7()
    rainbow_c8()
    stop()

#####################################
###############机器人#################
#####################################

def robot_head(color='black'):
    pen_color()
    fill_circle(400,150,150,color)

def robot_body(color='black'):
    fill_rect(320,300,160,180,color)

def robot_hands(color='black'):
    fill_rect(260,320,40,80,color)
    fill_rect(500,320,40,80,color)

def robot_foot(color='black'):
    fill_rect(300,500,80,80,color)
    fill_rect(420,500,80,80,color)

def robot_face(color='gold'):
    fill_rect(280,100,240,100,color)

def robot_eyes(color='white'):
    fill_rect(300,120,60,60,color)
    fill_rect(440,120,60,60,color)

def robot_mouth(color='red'):
    fill_rect(350,250,100,5,color)

def robot():
    robot_head()
    robot_body()
    robot_hands()
    robot_foot()
    robot_face()
    robot_eyes()
    robot_mouth()
    stop()

#####################################
###############钻石###################
#####################################


#钻石
def diamond():
    pensize(30)
    penup()
    right(90)
    forward(50)
    pendown()
    color('#CFD0D1')
    right(90)
    circle(100)
    left(180)
    pensize(1)
    right(90)
    penup()
    forward(50)
    pendown()
    color('#D105DF')
    begin_fill()
    goto(170,70)
    goto(130,70)
    goto(0,-100)
    end_fill()
    color('#B100BE')
    begin_fill()
    goto(0,70)
    goto(130,70)
    end_fill()
    color('#E016F1')
    begin_fill()
    goto(170,70)
    goto(130,102)
    goto(130,70)
    end_fill()
    color('#EC26F8')
    begin_fill()
    goto(65,102)
    goto(0,70)
    goto(130,70)
    end_fill()
    color('#F865FF')
    begin_fill()
    goto(65,102)
    goto(80,130)
    goto(130,102)
    end_fill()
    color('#EA27F7')
    begin_fill()
    goto(90,130)
    goto(80,130)
    end_fill()
    color('#FBA7FE')
    begin_fill()
    goto(0,130)
    goto(65,102)
    end_fill()
    color('#F641FF')
    begin_fill()
    goto(0,70)
    goto(-65,102)
    goto(0,130)
    end_fill()
    color('#FBA7FE')
    begin_fill()
    goto(-80,130)
    goto(-65,102)
    end_fill()
    color('#F865FE')
    begin_fill()
    goto(-130,70)
    goto(-130,102)
    goto(-80,130)
    end_fill()
    color('#FBC7FF')
    begin_fill()
    goto(-90,130)
    goto(-130,102)
    end_fill()
    color('#FBBBFF')
    begin_fill()
    goto(-170,69)
    goto(-130,69)
    end_fill()
    color('#EC26F8')
    begin_fill()
    goto(0,70)
    goto(-65,102)
    goto(-130,69)
    end_fill()
    color('#EB95F2')
    begin_fill()
    goto(-170,69)
    goto(0,-100)
    goto(-130,69)
    end_fill()
    color('#D105DF')
    begin_fill()
    goto(0,69)
    goto(0,-100)
    end_fill()
    stop()

#####################################
###############花####################
#####################################


def rectangle(base,height):
  for i in range(2):
    forward(base)
    right(90)
    forward(height)
    right(90)

def leaf(scale):
  length=0.6*scale
  left(45)
  forward(length)
  right(45)
  forward(length)
  right(135)
  forward(length)
  right(45)
  forward(length)
  right(180)
  
def moveAround(relX,relY,back):
  if back:
    relX = -1 * relX
    relY = -1 * relY
  forward(relX)
  right(90)
  forward(relY)
  left(90)


def filledCircle(radius,col):
  color(col)
  pendown()
  begin_fill()
  circle(radius)
  end_fill()
  penup()


def petals(radius,bloomDiameter,noOfPetals,col):
  penup()
  color(col)
  petalFromEye=1.5*radius
  relY = (radius+petalFromEye)/2
  relX = petalFromEye/2
  angle=360/noOfPetals
  moveAround(relX,relY,False)
  for i in range(noOfPetals):
    pendown()
    begin_fill()
    circle(radius)
    end_fill()
    penup()
    left((i+1)*angle)
    forward(petalFromEye)
    right((i+1)*angle)
  moveAround(relX,relY,True)

#茎
def stem(c='#61D836'):
  color(c)
  pendown()
  begin_fill()
  rectangle(10,150)
  moveAround(10,105,False)
  leaf(75)
  moveAround(10,105,True)
  end_fill()
  penup()

#花瓣
def petal(color='#FF1B5F'):
  penup()
  forward(5)
  petals(40,200,6,color)

#花蕊
def stamen(color='#F2D95F'):
  filledCircle(40,color)
  forward(-5)

#花
def flower():
    speed(500)
    stem()
    petal()
    stamen()
    stop() 

#####################################
############flappybird###############
#####################################


from time import time, sleep
from random import randint
from subprocess import Popen
import sys
import glob
import os
import os.path

# data文件夹路径
data_path = os.path.abspath(__file__)
data_path = os.path.split(data_path)[0]+'/data/'

font_name = "Comic Sans MS"
speed_x = 75
ground_line = -200 + 56 + 12
tube_dist = 260
bg_width = 286
PYCON_APAC_AD = """\
   Gmae
   Over
"""
isone = 1

def play_sound(name, vol=100):
    file_name = data_path + name + ".mp3"
    if sys.platform == "darwin":
        cmds = ["afplay"]
    else:
        cmds = ["mplayer", "-softvol", "-really-quiet", "-volume", str(vol)]
    try:
        Popen(cmds + [file_name])
    except:
        pass



def TextTurtle(x, y, color):
    t = Turtle()
    t.hideturtle()
    t.up()
    t.goto(x, y)
    t.speed(0)
    t.color(color)
    return t


def GIFTurtle(fname):
    t = Turtle(data_path + fname + ".gif")
    t.speed(0)
    t.up()
    return t



class Game:
    state = "end"
    score = best = 0
game = Game()


def start_game(game):

    screensize(216, 500)
    setup(288, 512)
    tracer(False, 0)
    hideturtle()
    for f in glob.glob(data_path + "*.gif"):
        addshape(f)



    score_txt = TextTurtle(0, 130, "white")
    best_txt = TextTurtle(90, 180, "white")
    pycon_apac_txt = TextTurtle(0, -270, "white")
    bgpic(data_path + "bg1.gif")
    tubes = [(GIFTurtle("tube1"), GIFTurtle("tube2")) for i in range(3)]
    grounds = [GIFTurtle("ground") for i in range(3)]
    bird = GIFTurtle("bird1")




    game.best = max(game.score, game.best)
    game.tubes_y = [10000] * 3
    game.hit_t, game.hit_y = 0, 0
    game.state = "alive"
    game.tube_base = 0
    game.score = 0
    game.start_time = time()
    pycon_apac_txt.clear()
 

    update_game(game,tubes=tubes,grounds=grounds,bird=bird,score_txt=score_txt,best_txt=best_txt,pycon_apac_txt=pycon_apac_txt)


def compute_y(t, game):
    return game.hit_y - 100 * (t - game.hit_t) * (t - game.hit_t - 1)


def update_game(game,tubes,grounds,bird,score_txt,best_txt,pycon_apac_txt):
    if game.state == "dead":
        play_sound("clickclick")
        pycon_apac_txt.write(
            PYCON_APAC_AD,
            align="center",
            font=(font_name, 24, "bold")
        )

        sleep(2)
        
        # game.state = "end"
        
        return
    t = time() - game.start_time
    bird_y = compute_y(t, game)
    if bird_y <= ground_line:
        bird_y = ground_line
        game.state = "dead"
    x = int(t * speed_x)
    tube_base = -(x % tube_dist) - 40
    if game.tube_base < tube_base:
        if game.tubes_y[2] < 1000:
            game.score += 5
            play_sound("bip")
        game.tubes_y = game.tubes_y[1:] + [randint(-100, 50)]
    game.tube_base = tube_base
    for i in range(3):
        tubes[i][0].goto(
            tube_base + tube_dist * (i - 1), 250 + game.tubes_y[i])
        tubes[i][1].goto(
            tube_base + tube_dist * (i - 1), -150 + game.tubes_y[i])
    if game.tubes_y[2] < 1000:
        tube_left = tube_base + tube_dist - 28
        tube_right = tube_base + tube_dist + 28
        tube_upper = game.tubes_y[2] + 250 - 160
        tube_lower = game.tubes_y[2] - 150 + 160
        center = Vec2D(0, bird_y - 2)
        lvec = Vec2D(tube_left, tube_upper) - center
        rvec = Vec2D(tube_right, tube_upper) - center
        if (tube_left < 18 and tube_right > -18) and bird_y - 12 <= tube_lower:
            game.state = "dead"
        if (tube_left <= 8 and tube_right >= -8) and bird_y + 12 >= tube_upper:
            game.state = "dead"
        if abs(lvec) < 14 or abs(rvec) < 14:
            game.state = "dead"
    bg_base = -(x % bg_width)
    for i in range(3):
        grounds[i].goto(bg_base + bg_width * (i - 1), -200)
    bird.shape(data_path + "bird%d.gif" % abs(int(t * 4) % 4 - 1))
    bird.goto(0, bird_y)
    score_txt.clear()
    score_txt.write(
        "%s" % (game.score), align="center", font=(font_name, 80, "bold"))
    if game.best:
        best_txt.clear()
        best_txt.write(
            "BEST: %d" % (game.best), align="center", font=(font_name, 14, "bold"))

    update()
    ontimer(lambda: update_game(game,tubes=tubes,grounds=grounds,bird=bird,score_txt=score_txt,best_txt=best_txt,pycon_apac_txt=pycon_apac_txt), 10)


def fly(game=game):



    if game.state == "end":
        start_game(game)
        return

    t = time() - game.start_time
    bird_y = compute_y(t, game)
    if bird_y > ground_line:
        game.hit_t, game.hit_y = t, bird_y
        play_sound("tack", 20)

def flappy():


    onkey(fly, "space")
    listen()
    mainloop()

    sys.exit(1)

#####################################
###############螺旋###################
#####################################
import turtle
import math
import random

#画螺旋线图形
def screw():
    wn = turtle.Screen()
    wn.bgcolor('white')
    speed(0)
    # color('white')
    # for i in range(10):
    #     size = 100
    #     for i in range(10):
    #         circle(size)
    #         size=size-4
    #     right(360/10)
    color('yellow')
    for i in range(10):
        size = 100
        for i in range(4):
            circle(size)
            size=size-10
        right(360/10)
    color('blue')
    for i in range(10):
        size = 100
        for i in range(4):
            circle(size)
            size=size-5
        right(360/10)
    color('orange')
    for i in range(10):
        size = 100
        for i in range(4):
            circle(size)
            size=size-19
        right(360/10)
    color('pink')
    for i in range(10):
        size = 100
        for i in range(4):
            circle(size)
            size=size-20
        right(360/10)
    stop()

#####################################
###############LOGO###################
#####################################

def logo():
    canvas()
    pen_speed(6)
    pen_color('#FD5C09')
    fill_rect(350,250,100,100,'#FD5C09')
    pen_color('black')
    fill_circle(400,300,40,'black')
    pen_color('#FEB084')
    fill_circle(387,293,15,'#FEB084')
    fill_circle(413,293,15,'#FEB084')
    fill_circle(400,313,15,'#FEB084')   
    stop() 

#####################################
###############汽车###################
#####################################

def car_head(c='#FFA500'):
    fill_rect(100,100,100,100,c)

def car_body(c='#FF6147'):
    fill_rect(100,200,350,100,c)

def car_wheel1(c='#FFD601'):
    fill_circle(200,300,50,c)

def car_wheel2(c='#FFD601'):
    fill_circle(350,300,50,c)

def car():
    car_head()
    car_body()
    car_wheel1()
    car_wheel2()
    stop()

#####################################
###############贪吃蛇#################
#####################################

import turtle
import random

register_shape(data_path+'gold.gif')

class Snake(turtle.Turtle):
    number = 0
    bodyPos = []
    torwarding = 0

    def __init__(self, color):
        turtle.Turtle.__init__(self)
        self.ht()
        self.length = 3
        self.color(color)
        self.speed(10)

    def draw(self):
        self.up()
        self.shape("circle")
        # self.shape(data_path+'bird1.gif')
        self.shapesize(0.5)
        self.keyListening()
        self.move()

    def keyListening(self):
        turtle.onkeypress(self.turnUp, "Up")
        turtle.onkeypress(self.turnLeft, "Left")
        turtle.onkeypress(self.turnRight, "Right")
        turtle.onkeypress(self.turnDown, "Down")
        turtle.listen()

    def turnUp(self):
        if self.torwarding == 270:
            pass
        else:
            self.torwarding = 90

    def turnDown(self):
        if self.torwarding == 90:
            pass
        else:
            self.torwarding = 270

    def turnLeft(self):
        if self.torwarding == 0:
            pass
        else:
            self.torwarding = 180

    def turnRight(self):
        if self.torwarding == 180:
            pass
        else:
            self.torwarding = 0

    def move(self):
        self.up()
        self.color = 'red'
        self.setheading(self.torwarding)
        self.fd(10)
        self.stamp()
        x = round(self.xcor())
        y = round(self.ycor())
        if self.number > self.length:
            self.clearstamps(1)
            self.bodyPos.append([x, y])
            self.bodyPos.pop(0)
        else:
            self.bodyPos.append([x, y])
            self.number += 1
        turtle.ontimer(self.move, 80)


class bonus(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.hideturtle()
        self.shape(data_path+'gold.gif')
        # self.shapesize(2.5)
        # self.color("orange")
        self.penup()

    def gen(self):
        x = random.randrange(-200, 200, 10)
        y = random.randrange(-200, 200, 10)
        self.goto(x, y)
        return [self.stamp(), x, y]


class border:
    def draw(self):
        turtle.ht()
        turtle.clear()
        turtle.pu()
        turtle.speed(0)
        turtle.pensize(20)
        turtle.color("grey")
        turtle.goto(-260, 260)
        turtle.pd()
        turtle.goto(260, 260)
        turtle.goto(260, -260)
        turtle.goto(-260, -260)
        turtle.goto(-260, 260)
        turtle.pu()
        turtle.goto(0, 0)


class game:
    state = 'null'
    bonusList = []

    def welcome(self):
        self.state = "welcome"
        turtle.clear()
        turtle.hideturtle()
        turtle.up()
        turtle.pensize(1)
        colors = ["#FFAA00", "#BF8F30", "#A66F00", "#FFBF40", "#FFD073", "#3914AF",
                  "#3914AF", "#412C84", "#200772", "#6A48D7", "#876ED7", "#009999",
                  "#1D7373", "#412C84", "#006363", "#5CCCCC", "#33CCCC"]
        turtle.setposition(-150, 20)
        turtle.tracer(False)
        turtle.pd()
        for x in range(60):
            turtle.fd(x/4)
            turtle.dot(15)

            turtle.color(colors[random.randrange(0, 15, 1)])
            turtle.left(15)

        turtle.setposition(75, -30)
        turtle.write("Welcome to Snake Game\n\nPress G to begin", align="center",
                     font=("Arial", 20, "bold"))
        self.keyListening()

    def start(self):
        turtle.onkey(None, key="g")
        self.state = "started"
        turtle.clear()
        self.border = border()
        self.bonus = bonus()
        self.snake = Snake('green')
        self.border.draw()
        self.snake.draw()
        self.isOver()
        self.genBonus()
        self.eatBonus()

    def overScene(self):
        self.state = 'over'
        turtle.clear()
        self.snake.clear()
        self.bonus.clear()
        self.bonusList.clear()
        turtle.setposition(0, 0)
        turtle.write("Game over\nPress G to restart", align="center",
                     font=("Arial", 20, "bold"))
        self.keyListening()

    def isOver(self):
        x = self.snake.xcor()
        y = self.snake.ycor()
        if(x < -240 or x > 240 or
           y > 240 or y < -240):
            self.overScene()
        for i in self.snake.bodyPos:
            if self.snake.bodyPos.count(i) > 1:
                self.overScene()
        if self.state == 'started':
            turtle.ontimer(self.isOver, 20)

    def eatBonus(self):
        # print(self.bonusList[0])
        # print([self.snake.xcor(),self.snake.ycor()])
        if (len(self.bonusList) > 0 and self.snake.xcor() < self.bonusList[0][1]+20 and self.snake.xcor() > self.bonusList[0][1] - 20 and self.snake.ycor() < self.bonusList[0][2] + 20 and self.snake.ycor() > self.bonusList[0][2] - 20):
            self.snake.length += 1
            id = self.bonusList.pop()[0]
            self.bonus.clearstamp(id)

        turtle.ontimer(self.eatBonus, 20)

    def genBonus(self):
        if len(self.bonusList) == 0 and self.state == "started":
            self.bonusList.append(self.bonus.gen())
        if self.state == 'started':
            turtle.ontimer(self.genBonus, 20)

    def keyListening(self):
        if(self.state == 'welcome' or self.state == 'over'):
            turtle.onkey(self.start, "g")
            turtle.listen()
        else:
            turtle.onkey(None, key="g")


def snake():
    game_snake = game()
    game_snake.welcome()
    turtle.done()



#####################################
###############表####################
#####################################

from datetime import datetime

def jump(distanz, winkel=0):
    penup()
    right(winkel)
    forward(distanz)
    left(winkel)
    pendown()

def hand(laenge, spitze):
    fd(laenge*1.15)
    rt(90)
    fd(spitze/2.0)
    lt(120)
    fd(spitze)
    lt(120)
    fd(spitze)
    lt(120)
    fd(spitze/2.0)

def make_hand_shape(name, laenge, spitze):
    reset()
    jump(-laenge*0.15)
    begin_poly()
    hand(laenge, spitze)
    end_poly()
    hand_form = get_poly()
    register_shape(name, hand_form)

def clockface(radius):
    reset()
    pensize(7)
    for i in range(60):
        jump(radius)
        if i % 5 == 0:
            fd(25)
            jump(-radius-25)
        else:
            dot(3)
            jump(-radius)
        rt(6)

def setup():
    global second_hand, minute_hand, hour_hand, writer
    mode("logo")
    make_hand_shape("second_hand", 125, 25)
    make_hand_shape("minute_hand",  130, 25)
    make_hand_shape("hour_hand", 90, 25)
    clockface(160)
    second_hand = Turtle()
    second_hand.shape("second_hand")
    second_hand.color("gray20", "gray80")
    minute_hand = Turtle()
    minute_hand.shape("minute_hand")
    minute_hand.color("blue1", "red1")
    hour_hand = Turtle()
    hour_hand.shape("hour_hand")
    hour_hand.color("blue3", "red3")
    for hand in second_hand, minute_hand, hour_hand:
        hand.resizemode("user")
        hand.shapesize(1, 1, 3)
        hand.speed(0)
    ht()
    writer = Turtle()
    #writer.mode("logo")
    writer.ht()
    writer.pu()
    writer.bk(85)

def wochentag(t):
    wochentag = ["Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"]
    wochentag = ["星期一", "星期二", "星期三",
        "星期四", "星期五", "星期六", "星期日"]
    return wochentag[t.weekday()]

def datum(z):
    # monat = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June",
    #          "July", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."]
    monat = ["01.", "02.", "03.", "04.", "05.", "06.",
             "07.", "08.", "09.", "10.", "11.", "12."]
    j = z.year
    m = monat[z.month - 1]
    t = z.day
    return "%s %d %d" % (m, t, j)

def tick():
    t = datetime.today()
    sekunde = t.second + t.microsecond*0.000001
    minute = t.minute + sekunde/60.0
    stunde = t.hour + minute/60.0
    try:
        tracer(False)  # Terminator can occur here
        writer.clear()
        writer.home()
        writer.forward(65)
        writer.write(wochentag(t),
                     align="center", font=("Courier", 14, "bold"))
        writer.back(150)
        writer.write(datum(t),
                     align="center", font=("Courier", 14, "bold"))
        writer.forward(85)
        tracer(True)
        second_hand.setheading(6*sekunde)  # or here
        minute_hand.setheading(6*minute)
        hour_hand.setheading(30*stunde)
        tracer(True)
        ontimer(tick, 100)
    except Terminator:
        pass  # turtledemo user pressed STOP

def clock():
    mode("logo")
    tracer(False)
    setup()
    tracer(True)
    tick()
    stop()


#####################################
############Python画画################
#####################################


def computer(): #start from the most northwest corner of the computer.
    pensize(4)
    pencolor('blue')
    seth(10)
    circle(-500,16)
    rt(90)
    fd(10)
    rt(90)
    circle(500,14)
    lt(85)
    fd(85)
    rt(90)
    fd(15)
    rt(90)
    fd(90)
    rt(120)
    fd(90)
    seth(265)
    circle(500,8)
    lt(88)
    circle(550,9)
    seth(90)
    fd(60)
    lt(85)
    circle(500,10)
    pu()
    seth(40)
    fd(79)
    seth(-63)
    pd()
    fd(52)
    pu()
    seth(-160)
    fd(147)
    seth(-22)
    pd()
    fd(63)
    pu()
    bk(20)
    seth(-120)
    pd()
    circle(17,60)
    lt(30)
    circle(50,50)
    lt(30)
    circle(17,60)
    pu()
    lt(180)
    circle(-17,60)
    seth(-40)
    pd()
    circle(-50,40)
    seth(-160)
    circle(-100,42)
    seth(90)
    circle(-50,40)
    pu()
    left(180)
    circle(-50,10)
    seth(-39)
    pd()
    circle(50,70)
def square(): #the key on the keyboard,start from the most southeast corner of the computer.
    seth(110)
    fd(7)
    lt(90)
    fd(9)
    lt(90)
    fd(7)
    lt(90)
    fd(9) 
def keyboard(): #start from the most southeast corner of the computer.
    pencolor('red')
    seth(110)
    fd(20)
    lt(90)
    fd(120)
    lt(110)
    fd(40)
    lt(73)
    fd(100)
    seth(100)
    pu()
    fd(5)
    pd()
    square()
    bk(9)
    square()
    bk(9)
    square()
    bk(9)
    square()
    bk(9)
    square()
    bk(9)
    square()
    bk(9)
    fd(45+9)
    lt(90)
    fd(7)
    square()
    bk(9)
    square()
    bk(9)
    square()
    pu()
    bk(18)
    lt(90)
    fd(7)
    pd()
    fd(7)
    lt(90)
    fd(35)
    lt(90)
    fd(7)
    lt(90)
    fd(35)
    pu()
    bk(44)
    pd()
    square()
    bk(9)
    square()
    fd(9)
    rt(90)
    fd(7)
    square()
    bk(9)
    square()
    fd(9)
    rt(90)
    fd(7)
    square()
    bk(9)
    square()  
def programmer(): #start from the most southeast corner of the programmer.
    pencolor('purple')
    seth(90)
    fd(50)
    seth(45)
    circle(70,10)
    pu()
    circle(70,58)
    pd()
    circle(70,202)
    seth(-100)
    circle(500,10)
    pu()
    seth(70)
    fd(170)
    pd()
    seth(-90)
    fd(15)
    rt(80)
    fd(10)
    seth(25)
    pu()
    fd(45)
    pd()
    seth(-70)
    fd(15)
    seth(10)
    fd(10)
    pu()
    seth(-100)
    fd(15)
    seth(-175)
    pd()
    pensize(8)
    fd(1)
    pu()
    fd(40)
    pd()
    fd(1)
    pensize(4)
    seth(-30)
    pu()
    fd(20)
    pd()
    seth(-40)
    circle(13,50)
def questionmark(theta): #the beginning angle is theta
    pd()
    pensize(4)
    seth(theta)
    fd(6)
    circle(-8,180)
    lt(60)
    pu()
    fd(12)
    pd()
    pensize(5)
    fd(1)
    pu()
    
def painting():
    tracer(10)
    computer()
    pu()
    seth(-170)
    fd(65)
    pd()
    pensize(3)
    keyboard()
    pu()
    seth(180)
    fd(130)
    pd()
    pensize(3)
    pencolor('black')
    seth(20)
    fd(237)
    pu()
    fd(114)
    pd()
    fd(40)
    rt(50)
    fd(60)
    pu()
    bk(60)
    rt(130)
    fd(220)
    pd()
    programmer()
    pu()
    seth(105)
    fd(120)
    questionmark(30)
    seth(40)
    fd(30)
    questionmark(15)
    seth(1)
    fd(30)
    questionmark(1)
    seth(145)
    fd(135)
    seth(90)
    fd(80)
    pd()
    pencolor('black')
    write('Python还能画画？？',move=False,align="left",font=("华文彩云",23,'normal'))
    ht()
    update()
    sleep(2)
    seth(270)
    fd(60)
    write('当然可以！！',move=False,align="left",font=("华文彩云",40,'normal'))
    stop()



if __name__ == '__main__':
    # canvas()

    # pen_speed(6)
    # flappy()
    # diamond()
    # xzpq()
    # car()
    # rainbow()
    # clock()
    # snake()
    painting()


