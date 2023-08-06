#作者:SO2

def run():
    print("hxf lib test--run")

import turtle
import time

def heart():
    t = turtle.Turtle()
    turtle.title("何雄飞作品")
    t.hideturtle()
    t.getscreen().bgcolor("#f0f0f0")
    t.color("#c1e6c6", "red")
    t.pensize(2)
    t.speed(2)
    t.up()
    t.goto(0, -150)

    t.down()
    t.begin_fill()
    t.goto(0, -150)
    t.goto(-175.12, -8.59)
    t.left(140)
    pos = []
    for i in range(19):
        t.right(10)
        t.forward(20)
        pos.append((-t.pos()[0], t.pos()[1]))
    for item in pos[::-1]:
        t.goto(item)
    t.goto(175.12, -8.59)
    t.goto(0, -150)
    t.left(50)
    t.end_fill()

    t.color("black")
    t.up()
    t.goto(0, 220)
    t.write("我爱你", font=(u"方正舒体", 36, "normal"), align="center")
    t.goto(200, -250)
    t.write("by 何雄飞", font=(u"方正舒体", 10, "bold"))
    time.sleep(260)
    turtle.done()