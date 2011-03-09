# -*- coding:utf-8 -*-

class Data( object ): pass

def propagate_down( f ):
  def decorated( *args ):
    result = f( *args )
    if hasattr( args[0], "children" ):
      for c in args[0].children:
        if hasattr( c, f.func_name ):
          r = getattr( c, f.func_name )( *args[1:] )
          if r > result:
            result = r
    return result
  return decorated


