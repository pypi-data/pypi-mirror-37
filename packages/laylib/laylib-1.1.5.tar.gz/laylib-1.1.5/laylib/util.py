import math
import pygame as pg
from pygame.math import Vector2 as vect2d


"""
util Desc file: n (0.2):
lib for rapid prototyping games,
contain some useful functions like distance between two vectors.
Date:       12/07/2017
Author:     Amardjia Amine (Goutted)
"""


def dist(v1, v2):
    """ distance between two vectors. """
    d = ((v2.x - v1.x)**2 + (v2.y - v1.y)**2) ** 0.5
    return d


def rad2deg(rad):
    """ from radian to degree """
    return rad * 180 / math.pi


def deg2rad(deg):
    """ from degree to radian """
    return deg * math.pi / 180


def rotate(v, angle):
    """ rotates a point p around the point origin.
    The angle is in radian.
    """
    vector = ((v.x * math.cos(angle) - v.y * math.sin(angle)),
              (v.x * math.sin(angle) + v.y * math.cos(angle)))
    return vector


def rotate2p(v1, v2, angle):
    """
    this function rotates a point p1
    around the point p0 with a certain angle.
    The angle is in radian.
    """
    dx = v2.x - v1.x
    dy = v2.y - v1.y
    vector = vect2d((dx * math.cos(angle) - dy * math.sin(angle)),
                    (dx * math.sin(angle) + dy * math.cos(angle)))
    vector += v1

    return vector


# graphics stuffs : to test

def rotateDeg(image, angle):
    """ rotate an image while keeping its center and size"""
    angle %= 360.0
    orig_rect = image.get_rect()
    rot_image = pg.transform.rotate(image, angle)
    orig_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(orig_rect).copy()
    return rot_image
