#!/usr/bin/python
# -*- coding: utf-8 -*-

import pig
from demo.intro_scene    import *
from demo.platform_scene import *
from demo.upwards_scene  import *
from demo.jump_scene     import *

#Create a game in a 640x400 pixel windows, with title "P.I.G" 
#and running at 30 fps
g = pig.Game( 640, 400, "P.I.G.", 60 )

#The game will start with the first defined scene
intro    = g.addScene( IntroScene( 640, 400 ) )
platform = g.addScene( PlatformScene( 640, 400 ) )
upwards  = g.addScene( UpwardsScene( 640, 400 ) )
jump     = g.addScene( JumpScene( 640, 400 ) )

#If the intro update method returns 1, test scene will be activated
g.setTransition( 1, intro, platform )
g.setTransition( 1, platform, upwards )
g.setTransition( 2, platform, jump )

#Execute the main loop
g.run()
