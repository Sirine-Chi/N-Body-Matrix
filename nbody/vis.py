import pygame
from pygame.locals import *
import esper

# print(esper.list_worlds())

# FIXME zoom
# FIXME propper scaling

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def draw_points(points):
    glEnable(GL_POINT_SMOOTH)
    glPointSize(5.0)

    glBegin(GL_POINTS)
    for point in points:
        clr = point[1]
        glColor4f(clr[0], clr[1], clr[2], 1.0)
        pos = point[0]
        glVertex3f(pos[0], pos[1], pos[2])
    glEnd()

def draw_axis(angle, vec: list[float] ):
    d: float = 0.005
    glPushMatrix()
    glRotatef(angle, vec[0], vec[1], vec[2])
    glBegin(GL_LINES)
    glVertex3f(100, 0, 0)
    glVertex3f(-100, 0, 0)
    glEnd()
    glPopMatrix()

def draw_axes(alpha=0.9):
    glLineWidth(2)

    glColor4f(1, 0, 0, alpha)
    draw_axis(0, [1, 0, 0])

    glColor4f(0, 1, 0, alpha)
    draw_axis(90, [0, 0, 1])

    glColor4f(0, 0, 1, alpha)
    draw_axis(90, [0, 1, 0])

def draw_units_XYZ(alpha=0.5):
    glPointSize(5.0)
    glBegin(GL_POINTS)

    glColor4f(1, 0, 0, alpha)
    glVertex3f(1, 0, 0)

    glColor4f(0, 1, 0, alpha)
    glVertex3f(0, 1, 0)

    glColor4f(0, 0, 1, alpha)
    glVertex3f(0, 0, 1)

    glEnd()

def draw_grid_ZX(size=10, step=1, alpha=0.5):
    glLineWidth(0.5)
    glBegin(GL_LINES)
    glColor4f(0.5, 0.5, 0.5, alpha)

    for i in range(-size, size + 1, step):
        glVertex3f(i, 0, -size)
        glVertex3f(i, 0,  size)
        glVertex3f(-size, 0, i)
        glVertex3f( size, 0, i)

    glEnd()

def draw_grid_XY(size=10, step=1, alpha=0.5):
    glLineWidth(0.5)
    glBegin(GL_LINES)
    glColor4f(0.5, 0.5, 0.5, alpha)
    
    for i in range(-size, size + 1, step):
        glVertex3f(-size, i, 0)
        glVertex3f( size, i, 0)
        glVertex3f(i, -size, 0)
        glVertex3f(i,  size, 0)
    glEnd()

def draw_grid_ZY(size=10, step=1, alpha=0.5):
    glLineWidth(0.5)
    glBegin(GL_LINES)
    glColor4f(0.5, 0.5, 0.5, alpha)

    for i in range(-size, size+1, step):
        glVertex3f(0, i, -size)
        glVertex3f(0, i,  size)
        glVertex3f(0, -size, i)
        glVertex3f(0,  size, i)
    glEnd()

def draw_grid_XYZ(size=10, step=1, alpha=0.5):
    draw_grid_XY(size, step, alpha)
    draw_grid_ZX(size, step, alpha)
    draw_grid_ZY(size, step, alpha)

# TODO add: color, size
def draw_text(position, text_string):
    font = pygame.font.Font(None, 16)
    textSurface = font.render(text_string, True, (255,255,255,255), (0,0,0,255))
    text_data = pygame.image.tostring(textSurface, "RGBA", True)
    glRasterPos3d(*position)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)

def draw_cube():
    verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

    edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

    glColor4f(1.0, 1.0, 1.0, 0.0)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

def window_resize(window, width, height):
    glViewport(0, 0, width, height)

# --- --- --- --- --- CAMERA CONTROLLER

# WASD, or ARROWS - movement
# SPACE - up
# L_SHIFT - down
# scrollwheel - zoom
# space + mouse movement - rotation

def movement():
    pressed = pygame.key.get_pressed()

    if (pressed[K_LEFT] or pressed[K_a]):
        # print(" '<' pressed")
        glTranslatef(0.1, 0, 0)
    if (pressed[K_RIGHT] or pressed[K_d]):
        # print(" '>' pressed")
        glTranslatef(-0.1, 0, 0)

    if (pressed[K_UP] or pressed[K_w]):
        # print(" '/\' pressed")
        glTranslatef(0, 0, 0.1)
    if (pressed[K_DOWN] or pressed[K_s]):
        # print(" '\/' pressed")
        glTranslatef(0, 0, -0.1)
    if (pressed[K_SPACE]):
        # print(" 'SPACE' pressed")
        glTranslatef(0, -0.1, 0)
    if (pressed[K_LSHIFT] or pressed[K_RSHIFT]):
        # print(" 'SHIFT' pressed")
        glTranslatef(0, 0.1, 0)

def zoom(event):
    if event.type == pygame.MOUSEWHEEL: # FIXME some bug
        zoom = event.y
        glTranslatef(0, 0, zoom)
        # glScale(zoom, zoom, zoom)

def rotation(event):
    if pygame.mouse.get_pressed()[0]:
        # print("L mouse pressed")
        if event.type == pygame.MOUSEMOTION:
            dis_center = glGetIntegerv(GL_VIEWPORT)
            mouseMove = [event.pos[0]- dis_center[0], event.pos[1] - dis_center[1] ]
            glRotatef(mouseMove[0]*0.001, 0.0, mouseMove[1]*0.001, 0.0)
    if pygame.mouse.get_pressed()[2]:
        # print("R mouse pressed")
        pass

def resize(event, display):
    if event.type == pygame.VIDEORESIZE:
            glViewport(0, 0, event.w, event.h)

# --- --- --- --- --- VISUALISATOR CLASS

class viswind():
    def __init__(self):
        pygame.init()
        self.display = (800,600)
        pygame.display.set_mode(self.display, RESIZABLE|DOUBLEBUF|OPENGL)
        glMatrixMode(GL_MODELVIEW)
        gluLookAt(0, -8, 0, 0, 0, 0, 0, 0, 1)
        viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        glLoadIdentity()
        self.clock = pygame.time.Clock()

        gluPerspective(45, (self.display[0]/self.display[1]), 0.1, 50.0)
        glTranslatef(0.0,0.0, -10)

    def window_tick(self, points):

        for event in pygame.event.get():
            movement()
            zoom(event)
            rotation(event)
            resize(event, self.display)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        # glScale(2, 2, 2)
        # glRotatef(1, 3, 1, 1)
        # self.clock.tick()
        # print(f"fps: {int(self.clock.get_fps())}")

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glDisable(GL_LIGHTING)
        glEnable( GL_BLEND )
        glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )
        draw_grid_XYZ(10, 1, 0.4)
        draw_units_XYZ(0.8)
        draw_text((1, 0, 0), "x = 1")
        draw_text((0, 1, 0), "y = 1")
        # draw_text((0, 0, 1), "z = 1")
        draw_axes()
        draw_points(points)
        glDisable(GL_BLEND)
        # draw_cube()
        pygame.display.flip()
        pygame.time.wait(0)
