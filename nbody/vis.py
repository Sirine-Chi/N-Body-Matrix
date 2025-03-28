import pygame
from pygame.locals import *
import esper

# print(esper.list_worlds())

# FIXME grid, axes
# FIXME zoom
# FIXME propper scaling


from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

points = [
    (1.0, 2.0, 3.0),
    (4.0, 5.0, 6.0),
    (7.0, 8.0, 9.0),
]

def draw_points(points):
    glColor3f(1, 1, 1)
    glEnable(GL_POINT_SMOOTH)
    glPointSize(5.0)

    glBegin(GL_POINTS)
    for point in points: # FIXME here integrate color
        glVertex3f(point[0], point[1], point[2])
    glEnd()

def draw_axis(angles: list[float] ):
    d: float = 0.005
    glPushMatrix()
    glRotatef(angles[0], angles[1], angles[2], 1)
    glBegin(GL_LINES)

    # FIXME 2f -> 3f
    glVertex3f(1, 0, 0)
    glVertex3f(-1, 0, 0)

    glEnd()
    glPopMatrix()

def draw_axes():
    glLoadIdentity()

    glLineWidth(2)
    glColor3f(1, 0, 0)
    draw_axis([0, 0, 0])
    glColor3f(0, 1, 0)
    draw_axis([90, 0, 0])
    glColor3f(0, 0, 1)
    draw_axis([0, 0, 90])


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

def Cube():

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

def window_resize(window, width, height):
    glViewport(0, 0, width, height)

def key_callback(window, key, scandone, action, mode):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

def movement(event):
    if event.type == pygame.KEYDOWN:
        if event.key == (pygame.K_LEFT or pygame.K_a):
            print(" '<' pressed")
        if event.key == (pygame.K_RIGHT or pygame.K_d):
            print(" '>' pressed")
        if event.key == (pygame.K_UP or pygame.K_w):
            print(" '/\ ' pressed")
        if event.key == (pygame.K_DOWN or pygame.K_s):
            print(" '\/' pressed")

def zoom(event):
    if event.type == pygame.MOUSEWHEEL: # FIXME some bug
        zoom = event.y
        glTranslatef(zoom, zoom, zoom)
        # glScale(zoom, zoom, zoom)

class viswind():
    def __init__(self):
        pygame.init()
        display = (800,600)
        pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial" , 18 , bold = True)

        gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
        glTranslatef(0.0,0.0, -10)
    
# if event.type == pygame.MOUSEBUTTONDOWN:
        #     pygame.mouse.set_cursor = pygame.SYSTEM_CURSOR_HAND
        #     if event.type == pygame.MOUSEMOTION:
        #         pos = event.pos
        #         glTranslatef(0.1*pos[0], 0.1*pos[1], 0)


    def window_tick(self, points):

        # def fps_in_window(self):
        #     fps = str(int(self.clock.get_fps()))
        #     fps_t = self.font.render(fps , 1, pygame.Color("RED"))
        #     window.blit(fps_t,(0,0))

        for event in pygame.event.get():
            movement(event)
            zoom(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            
        # glScale(2, 2, 2)
        glRotatef(1, 3, 1, 1)
        # self.clock.tick()
        # print(f"fps: {int(self.clock.get_fps())}")

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        # draw_axes()
        draw_points(points)
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)


# v = viswind()
# while True:
#     v.window_tick(points)
