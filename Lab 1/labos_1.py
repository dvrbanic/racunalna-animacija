import io
import math
import numpy as np
from numpy.linalg import norm
from pyglet.gl import *
import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *


def ucitaj_iz_obj(file_name):
    with io.open(file_name, 'r', encoding="utf-8") as f:
        vrhovi_lista = []
        poligoni_lista = []
        while True:
            line = f.readline()
            if not line:
                break
            if line.startswith('v') or line.startswith('f'):
                if line[0] == 'v':
                    pom = line.split()
                    vrhovi_lista.append((float(pom[1]), float(pom[2]), float(pom[3])))
                if line[0] == 'f':
                    pom = line.split()
                    poligoni_lista.append((int(pom[1]), int(pom[2]), int(pom[3])))
    return vrhovi_lista, poligoni_lista


# Ucitavanje zadanog tijela iz datoteke i niza tocaka koje odreduju aproksimacijsku uniformnu kubnu B-splajn krivulju
vrhovi, poligoni = ucitaj_iz_obj('bird.obj')
b_spline_vrhovi, _ = ucitaj_iz_obj('b_spline.obj')

# print("ucitani vrhovi:", vrhovi)
# print("ucitani poligoni:", poligoni)
# print("b-spline vrhovi krivulje:", b_spline_vrhovi)

array_B = np.array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 0, 3, 0], [1, 4, 1, 0]])
array_B_der = np.array([[-1, 3, -3, 1], [2, -4, 2, 0], [-1, 0, 1, 0]])

sve_pi = []  # potrebna translacija objekta
sve_pi_der = []  # ciljna orijentacija
sve_os = []  # os rotacije
sve_phi = []  # kut rotacije
s = [0, 0, 1]  # pocetna orijentacija

for i in range(len(b_spline_vrhovi) - 3):
    r1 = b_spline_vrhovi[i]
    r2 = b_spline_vrhovi[i + 1]
    r3 = b_spline_vrhovi[i + 2]
    r4 = b_spline_vrhovi[i + 3]

    for t in np.arange(0, 1, 0.01):
        # ciljna orijentacija objekta = tangenta
        array_t_der = np.array([math.pow(t, 2), t, 1]).reshape((1, 3))
        array_tB_der = np.matmul(array_t_der / 2, array_B_der)

        pi_x_der = array_tB_der[0][0] * r1[0] + array_tB_der[0][1] * r2[0] + array_tB_der[0][2] * r3[0] + \
                   array_tB_der[0][3] * r4[0]
        pi_y_der = array_tB_der[0][0] * r1[1] + array_tB_der[0][1] * r2[1] + array_tB_der[0][2] * r3[1] + \
                   array_tB_der[0][3] * r4[1]
        pi_z_der = array_tB_der[0][0] * r1[2] + array_tB_der[0][1] * r2[2] + array_tB_der[0][2] * r3[2] + \
                   array_tB_der[0][3] * r4[2]
        p_i_der = (pi_x_der, pi_y_der, pi_z_der)
        sve_pi_der.append(p_i_der)

        # os rotacije; vektorski produkt pocetne (s) i ciljne (e) orijentacije
        os_x = s[1] * p_i_der[2] - p_i_der[1] * s[2]
        os_y = -(s[0] * p_i_der[2] - p_i_der[0] * s[2])
        os_z = s[0] * p_i_der[1] - s[1] * p_i_der[0]
        os = (os_x, os_y, os_z)
        sve_os.append(os)

        # kut rotacije; skalarni produkt pocetne (s) i ciljne (e) orijentacije podijeljen s normama tih vektora
        scalar_os = s[0] * p_i_der[0] + s[1] * p_i_der[1] + s[2] * p_i_der[2]
        phi_rad = math.acos(scalar_os / (norm(s) * norm(p_i_der)))
        phi_deg = phi_rad * 180 / math.pi
        sve_phi.append(phi_deg)

        # tocka krivulje
        array_t = np.array([math.pow(t, 3), math.pow(t, 2), t, 1]).reshape((1, 4))
        array_tB = np.matmul(array_t / 6, array_B)

        pi_x = array_tB[0][0] * r1[0] + array_tB[0][1] * r2[0] + array_tB[0][2] * r3[0] + array_tB[0][3] * r4[0]
        pi_y = array_tB[0][0] * r1[1] + array_tB[0][1] * r2[1] + array_tB[0][2] * r3[1] + array_tB[0][3] * r4[1]
        pi_z = array_tB[0][0] * r1[2] + array_tB[0][1] * r2[2] + array_tB[0][2] * r3[2] + array_tB[0][3] * r4[2]
        p_i = (pi_x, pi_y, pi_z)
        sve_pi.append(p_i)

        # print("p_i =", p_i)
        # print("p_i_der =", p_i_der)


def krivulja():
    glBegin(GL_LINE_STRIP)
    for i in sve_pi:
        glVertex3fv(i)
    glEnd()


def tangenta(i):
    glBegin(GL_LINES)
    # if i % 10 == 0:
    glVertex3f(sve_pi[i][0], sve_pi[i][1], sve_pi[i][2])
    glVertex3f(sve_pi[i][0] + sve_pi_der[i][0] / 2, sve_pi[i][1] + sve_pi_der[i][1] / 2,
               sve_pi[i][2] + sve_pi_der[i][2] / 2)
    glEnd()


def objekt(i):
    glTranslatef(sve_pi[i][0], sve_pi[i][1], sve_pi[i][2])
    glRotatef(sve_phi[i], sve_os[i][0], sve_os[i][1], sve_os[i][2])
    glBegin(GL_LINES)
    for poligon in poligoni:
        for vrh in poligon:
            glVertex3fv(vrhovi[vrh - 1])
    glEnd()


def main():
    pg.init()
    display = (1500, 750)
    pg.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(30, (display[0] / display[1]), 0.1, 500)

    glTranslatef(-18, -14, -60)
    glRotatef(45, 0, 0.5, 0.5)

    i = 0
    while i < len(sve_pi):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        krivulja()
        tangenta(i)
        glPushMatrix()
        objekt(i)
        glPopMatrix()

        i += 1
        pg.display.flip()
        # pg.time.wait(1)


if __name__ == "__main__":
    main()
