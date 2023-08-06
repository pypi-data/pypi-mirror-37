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
    seth(230)
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

    seth(230)
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
    seth(230)
    fd(40)

    # print(pos())


    circle(-30, 230)
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
    seth(230)
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
    # mainloop()


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
    fd(230)
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
tube_dist = 230
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

if __name__ == '__main__':
    # canvas()

    # pen_speed(6)
    flappy()
    # diamond()
    # xzpq()
    # car()
    # rainbow()
    stop()


