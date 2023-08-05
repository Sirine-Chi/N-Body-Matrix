from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

w, h = 500, 500


def square():
    # We have to declare the points in this sequence: bottom left, bottom right, top right, top left
    glBegin(GL_QUADS)  # Begin the sketch
    glVertex2f(100, 100)
    glVertex2f(200, 100)
    glVertex2f(200, 200)
    glVertex2f(100, 200)
    glEnd()  # Mark the end of drawing


def showScreen():
    glClear(
        GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT
    )  # Remove everything from screen (i.e. displays all white)
    glLoadIdentity()  # Reset all graphic/shape's position
    square()  # Draw a square using our function
    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA)  # Set the display mode to be colored
glutInitWindowSize(500, 500)  # Set the w and h of your window
glutInitWindowPosition(0, 0)  # Set the position at which this windows should appear
wind = glutCreateWindow("OpenGL Coding Practice")  # Set a window title
glutDisplayFunc(showScreen)
glutIdleFunc(showScreen)  # Keeps the window open
glutMainLoop()  # Keeps the above created window displaying/running in a loop
