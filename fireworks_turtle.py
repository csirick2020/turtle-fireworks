# fireworks_turtle.py

import turtle
import random
import math


# Setup screen
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Turtle Fireworks 🎆")
screen.tracer(0)

# UI drawer
ui_pen = turtle.Turtle()
ui_pen.hideturtle()
ui_pen.speed(0)

# Firework history stack (for undo)
firework_history = []

# Button registry
buttons = {
    "Clear": (347, -375, 447, -325),
    "Quit": (347, -315, 447, -265),
    "Auto": (347, -255, 447, -205)
}

# Auto show state
auto_running = False
auto_count = 0
auto_limit = 20


def random_color():
    return (random.random(), random.random(), random.random())


def draw_button(label, x1, y1, x2, y2):
    ui_pen.penup()
    ui_pen.goto(x1, y1)
    ui_pen.setheading(0)
    ui_pen.color("white", "gray20")
    ui_pen.begin_fill()
    for _ in range(2):
        ui_pen.forward(x2 - x1)
        ui_pen.left(90)
        ui_pen.forward(y2 - y1)
        ui_pen.left(90)
    ui_pen.end_fill()
    ui_pen.penup()
    ui_pen.goto(x1 + 27, y1 + 15)
    ui_pen.color("white")
    ui_pen.write(label, font=("Arial", 14, "bold"))


def draw_buttons():
    ui_pen.clear()
    for label, (x1, y1, x2, y2) in buttons.items():
        draw_button(label, x1, y1, x2, y2)


# Firework patterns
def draw_radial_lines(p, x, y, size):
    p.color(random_color())
    for angle in range(0, 360, 15):
        p.penup()
        p.goto(x, y)
        p.pendown()
        p.setheading(angle)
        p.forward(size)


def draw_circle_dots(p, x, y, size):
    p.color(random_color())
    for angle in range(0, 360, 15):
        p.penup()
        p.goto(x + size * math.cos(math.radians(angle)),
               y + size * math.sin(math.radians(angle)))
        p.dot(6)


def draw_spiral(p, x, y, size):
    p.color(random_color())
    p.penup()
    p.goto(x, y)
    p.pendown()
    for i in range(size - random.randint(10, 25)):
        p.forward(i * 2)
        p.left(20)


def draw_star(p, x, y, size):
    p.color(random_color())
    p.penup()
    p.goto(x, y)
    p.pendown()
    for _ in range(5):
        p.forward(size)
        p.right(144)


def draw_concentric_circles(p, x, y, size):
    p.color(random_color())
    for r in range(20, size, 20):
        p.penup()
        p.goto(x, y - r)
        p.pendown()
        p.circle(r)


def draw_square_burst(p, x, y, size):
    p.color(random_color())
    for i in range(4):
        p.penup()
        p.goto(x, y)
        p.pendown()
        p.setheading(90 * i)
        for _ in range(4):
            p.forward(size)
            p.right(90)


def draw_cross_burst(p, x, y, size):
    p.color(random_color())
    for angle in [0, 90, 45, 135]:
        p.penup()
        p.goto(x, y)
        p.pendown()
        p.setheading(angle)
        p.forward(size)


def draw_random_scatter(p, x, y, size):
    p.color(random_color())
    for _ in range(30):
        angle = random.randint(0, 360)
        dist = random.randint(10, size)
        p.penup()
        p.goto(x + dist * math.cos(math.radians(angle)),
               y + dist * math.sin(math.radians(angle)))
        p.dot(4)


def draw_flower(p, x, y, size):
    p.color(random_color())
    for angle in range(0, 360, 60):
        p.penup()
        p.goto(x, y)
        p.setheading(angle)
        p.forward(size // 2)
        p.pendown()
        p.circle(size // 2)


def draw_double_explosion(p, x, y, size):
    draw_radial_lines(p, x, y, size)
    draw_circle_dots(p, x, y, size // 2)


# All patterns
fireworks = [
    draw_radial_lines,
    draw_circle_dots,
    draw_spiral,
    draw_star,
    draw_concentric_circles,
    # draw_square_burst,  - Not a big fan of this one.
    # draw_cross_burst,  - Not a big fan of this one.
    draw_random_scatter,
    draw_flower,
    draw_double_explosion
]


def make_firework(x=None, y=None):
    fw_pen = turtle.Turtle()
    fw_pen.hideturtle()
    fw_pen.speed(0)
    fw_pen.pensize(2)

    if x is None or y is None:
        x = random.randint(-300, 200)
        y = random.randint(-200, 250)

    size = random.randint(50, 150)
    design = random.choice(fireworks)
    design(fw_pen, x, y, size)

    firework_history.append(fw_pen)

    # Keep buttons on top
    draw_buttons()

    screen.update()


def auto_firework():
    global auto_count, auto_running
    if not auto_running:
        return
    if auto_count >= auto_limit:
        auto_running = False
        return
    make_firework()
    auto_count += 1
    screen.ontimer(auto_firework, 250)  # 1/4 sec


def left_click_action(x, y):
    global auto_running, auto_count

    # Button check always allowed
    for label, (x1, y1, x2, y2) in buttons.items():
        if x1 <= x <= x2 and y1 <= y <= y2:
            if label == "Quit":  # Always allowed
                screen.bye()
            elif not auto_running:  # Only allow if not auto
                if label == "Clear":
                    for fw in firework_history:
                        fw.clear()
                        fw.hideturtle()
                    firework_history.clear()
                    draw_buttons()
                    screen.update()
                elif label == "Auto":
                    if not auto_running:
                        auto_running = True
                        auto_count = 0
                        auto_firework()
            return

    # Normal fireworks only if not auto
    if not auto_running:
        make_firework(x, y)


def right_click_action(x, y):
    if auto_running:  # Ignore undo while auto running
        return
    if firework_history:
        last_fw = firework_history.pop()
        last_fw.clear()
        last_fw.hideturtle()
        draw_buttons()  # Keep buttons on top
        screen.update()


# Draw initial buttons
draw_buttons()
screen.update()

# Bind events
screen.onscreenclick(left_click_action, 1)  # Left click = fireworks / buttons
screen.onscreenclick(right_click_action, 3)  # Right click = undo last
screen.mainloop()
