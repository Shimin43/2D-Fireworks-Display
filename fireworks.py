from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import random

width, height = 500, 500
panel_height = 110
rockets = []
particles = []
stars = []
running = False
started = False
frame = 0
pattern = 1

for i in range(100):
    x = random.randint(0, width)
    y = random.randint(panel_height, height)
    stars.append([x, y])


def drawText(x, y, text):

    glColor3f(1, 1, 1)
    glRasterPos2f(x, y)

    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(ch))


def rectangle(x1, y1, x2, y2, color):

    glColor3f(color[0], color[1], color[2])

    glBegin(GL_QUADS)

    glVertex2f(x1, y1)
    glVertex2f(x2, y1)
    glVertex2f(x2, y2)
    glVertex2f(x1, y2)

    glEnd()


def circle(x, y, r, color):

    glColor3f(color[0], color[1], color[2])

    glBegin(GL_TRIANGLE_FAN)

    glVertex2f(x, y)

    for i in range(31):
        angle = 2 * math.pi * i / 30

        glVertex2f(
            x + r * math.cos(angle),
            y + r * math.sin(angle)
        )

    glEnd()


def background():

    rectangle(0, panel_height, width, height, (0, 0, 0.05))

    glPointSize(2)
    glColor3f(1, 1, 1)

    glBegin(GL_POINTS)

    for s in stars:
        glVertex2f(s[0], s[1])

    glEnd()


def launchRocket(x=None, target=None):

    if x is None:
        x = random.randint(30, width - 30)

    if target is None:
        target = random.randint(220, 450)

    color = random.choice([
        (1, 0.2, 0.1),
        (1, 0.7, 0),
        (0, 0.7, 1),
        (1, 0, 0.8),
        (0.2, 1, 0.3),
        (1, 1, 0)
    ])

    rockets.append([
        x, panel_height, target,
        random.uniform(3, 5), color
    ])


def explosion(x, y, color):

    total = 120

    for i in range(total):

        if pattern == 1:

            angle = 2 * math.pi * i / total
            speed = random.uniform(2, 4.5)

        elif pattern == 2:

            rays = 10

            angle = 2 * math.pi * (i % rays) / rays
            angle += random.uniform(-0.06, 0.06)

            if (i // rays) % 2 == 0:
                speed = random.uniform(4, 5)
            else:
                speed = random.uniform(1.5, 2.5)

        else:

            arm = i % 3
            step = i // 3

            angle = step * 0.22 + arm * (2 * math.pi / 3)
            speed = 1.5 + step * 0.045

        dx = math.cos(angle) * speed
        dy = math.sin(angle) * speed

        size = random.uniform(2.5, 3.5)

        particles.append([
            x, y, dx, dy, 120, size, color
        ])


def drawRockets():

    for r in rockets:

        glColor3f(r[4][0], r[4][1], r[4][2])

        glLineWidth(3)

        glBegin(GL_LINES)

        glVertex2f(r[0], r[1] - 15)
        glVertex2f(r[0], r[1])

        glEnd()

        circle(r[0], r[1], 4, r[4])


def drawParticles():

    for p in particles:

        size = p[5] * (p[4] / 120)

        circle(
            p[0], p[1],
            max(size, 1),
            p[6]
        )


def update(value):

    global frame

    if running:

        frame += 1

        if frame % 65 == 1:
            launchRocket()

        for r in rockets[:]:

            r[1] += r[3]

            if r[1] >= r[2]:

                explosion(r[0], r[1], r[4])
                rockets.remove(r)

        for p in particles[:]:

            p[0] += p[2]
            p[1] += p[3]

            p[3] -= 0.035

            p[4] -= 1

            if p[4] <= 0:
                particles.remove(p)

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)


def controlPanel():

    rectangle(
        0, 0, width, panel_height,
        (0.12, 0.12, 0.16)
    )

    rectangle(10, 10, 125, 42, (0, 0.65, 0.15))
    drawText(47, 23, "START")

    rectangle(135, 10, 250, 42, (0.85, 0.05, 0.05))
    drawText(176, 23, "STOP")

    rectangle(260, 10, 375, 42, (0, 0.25, 0.9))
    drawText(296, 23, "LAUNCH")

    rectangle(385, 10, 490, 42, (0.95, 0.35, 0))
    drawText(420, 23, "RESET")

    drawText(10, 79, "PATTERN:")

    color1 = (0, 0.55, 0.85) if pattern == 1 else (0.30, 0.30, 0.38)

    rectangle(85, 62, 215, 98, color1)
    drawText(126, 75, "CIRCLE")
    color2 = (0, 0.55, 0.85) if pattern == 2 else (0.30, 0.30, 0.38)
    rectangle(225, 62, 345, 98, color2)
    drawText(267, 75, "STAR")
    color3 = (0, 0.55, 0.85) if pattern == 3 else (0.30, 0.30, 0.38)
    rectangle(355, 62, 490, 98, color3)
    drawText(395, 75, "SPIRAL")

def panelClick(x, mouse_y):
    global running, started, frame, pattern
    if 10 <= x <= 125 and 10 <= mouse_y <= 42:
        running = True
        started = True
    elif 135 <= x <= 250 and 10 <= mouse_y <= 42:
        running = False
    elif 260 <= x <= 375 and 10 <= mouse_y <= 42:
        if started and running:
            launchRocket()
    elif 385 <= x <= 490 and 10 <= mouse_y <= 42:
        running = False
        started = False
        rockets.clear()
        particles.clear()

        frame = 0
    elif 85 <= x <= 215 and 62 <= mouse_y <= 98:
        pattern = 1
    elif 225 <= x <= 345 and 62 <= mouse_y <= 98:
        pattern = 2
    elif 355 <= x <= 490 and 62 <= mouse_y <= 98:
        pattern = 3
def mouseclick(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        mouse_y = height - y
        if mouse_y <= panel_height:
            panelClick(x, mouse_y)
        elif started and running:
            launchRocket(
                x,
                max(panel_height + 40, mouse_y)
            )
    glutPostRedisplay()

def normalkey(key, x, y):
    global running, started, frame, pattern
    if key == b's':
        running = True
        started = True
    elif key == b'p':
        running = False
    elif key == b'r':
        running = False
        started = False
        rockets.clear()
        particles.clear()
        frame = 0
    elif key == b' ' and started and running:
        launchRocket()
    elif key == b'1':
        pattern = 1
    elif key == b'2':
        pattern = 2
    elif key == b'3':
        pattern = 3

def main():

    background()
    drawRockets()
    drawParticles()
    controlPanel()

def showScreen():

    glClear(GL_COLOR_BUFFER_BIT)
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 500, 0, 500, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    main()
    glFlush()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)
glutCreateWindow(b"2D Fireworks Display")
glClearColor(0, 0, 0.05, 1)
glutDisplayFunc(showScreen)
glutMouseFunc(mouseclick)
glutKeyboardFunc(normalkey)
glutTimerFunc(16, update, 0)
glutMainLoop()
