import turtle

__Pen = turtle.Pen()


def 太极():
    t = turtle.Pen()
    t.pencolor('gray')
    #灰色画笔方向朝左
    t.right(180)
    t.fillcolor('gray')
    __Pen.fillcolor("#000000")
    __Pen.pencolor("#000000")
    __Pen.speed(0)
    t.speed(0)
    for __count in range(360):
        __Pen.begin_fill()
        #黑色画笔向上画一个圆
        __Pen.circle(50)
        #黑色画笔左拐一度
        __Pen.left(1)
        __Pen.end_fill()
        t.begin_fill()
        #灰色画笔向下画一个圆
        t.circle(50)
        #灰色画笔左拐一度
        t.left(1)
        t.end_fill()
    turtle.done()

#开始进入Python的世界
太极()
