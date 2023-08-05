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

if __name__ == '__main__':
	canvas()

	pen_speed(6)

	fill_circle()
	fill_rect()



	stop()

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


def nose_xzpq(x,y):#鼻子
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
    pencolor(255,155,192)
    seth(10)
    begin_fill()
    circle(5)
    color(160,82,45)
    end_fill()

    pu()
    seth(0)
    fd(20)
    pd()
    pencolor(255,155,192)
    seth(10)
    begin_fill()
    circle(5)
    color(160,82,45)
    end_fill()


def head_xzpq(x,y):#头
    color((255,155,192),"pink")
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


def ears_xzpq(x,y): #耳朵
    color((255,155,192),"pink")
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


def eyes_xzpq(x,y):#眼睛
    color((255,155,192),"white")
    pu()
    seth(90)
    fd(-20)
    seth(0)
    fd(-95)
    pd()
    begin_fill()
    circle(15)
    end_fill()

    color("black")
    pu()
    seth(90)
    fd(12)
    seth(0)
    fd(-3)
    pd()
    begin_fill()
    circle(3)
    end_fill()

    color((255,155,192),"white")
    pu()
    seth(90)
    fd(-25)
    seth(0)
    fd(40)
    pd()
    begin_fill()
    circle(15)
    end_fill()

    color("black")
    pu()
    seth(90)
    fd(12)
    seth(0)
    fd(-3)
    pd()
    begin_fill()
    circle(3)
    end_fill()


def cheek_xzpq(x,y):#腮
    color((255,155,192))
    pu()
    goto(x,y)
    pd()
    seth(0)
    begin_fill()
    circle(30)
    end_fill()


def mouth_xzpq(x,y): #嘴
    color(239,69,19)
    pu()
    goto(x,y)
    pd()
    seth(-80)
    circle(30,40)
    circle(40,80)


def body_xzpq(x,y):#身体
    color("red",(255,99,71))
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


def hands_xzpq(x,y):#手
    color((255,155,192))
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

def foot_xzpq(x,y):#脚
    pensize(10)
    color((240,128,128))
    pu()
    goto(x,y)
    pd()
    seth(-90)
    fd(40)
    seth(-180)
    color("black")
    pensize(15)
    fd(20)

    pensize(10)
    color((240,128,128))
    pu()
    seth(90)
    fd(40)
    seth(0)
    fd(90)
    pd()
    seth(-90)
    fd(40)
    seth(-180)
    color("black")
    pensize(15)
    fd(20)

def tail_xzpq(x,y):#尾巴
    pensize(4)
    color((255,155,192))
    pu()
    goto(x,y)
    pd()
    seth(0)
    circle(70,20)
    circle(10,330)
    circle(70,30)

def setting():          #参数设置
    pensize(4)
    hideturtle()
    colormode(255)
    color((255,155,192),"pink")
    # setup(840,500)
    speed(6)

def xzpq():
    setting()           #画布、画笔设置
    nose_xzpq(-100,100)      #鼻子
    head_xzpq(-69,167)       #头
    ears_xzpq(0,160)         #耳朵
    eyes_xzpq(0,140)         #眼睛
    cheek_xzpq(80,10)        #腮
    mouth_xzpq(-20,30)       #嘴
    body_xzpq(-32,-8)        #身体
    hands_xzpq(-56,-45)      #手
    foot_xzpq(2,-177)        #脚
    tail_xzpq(148,-155)      #尾巴
    # done()              #结束
