# -*- coding: utf-8 -*-

from movable import *
from camera  import *
import pygame
from math import floor

class FlatCamera( Camera ):
  def __init__( self, layers, width, height, zoom = 1, isometric = False ):
    Camera.__init__( self, layers, width, height, 0, zoom, isometric )
