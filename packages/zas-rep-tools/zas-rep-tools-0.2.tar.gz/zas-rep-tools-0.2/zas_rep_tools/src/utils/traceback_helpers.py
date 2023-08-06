#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# : TraceBack Handling
# Author:
# c(Developer) ->     {'Egor Savin'}
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

###Programm Info######


import sys
import traceback
from zas_rep_tools.src.utils.debugger import p

def print_exc_plus(  ):
    """
    Print the usual traceback information, followed by a listing of all the
    local variables in each frame.
    """
    p("START Extended Traceback", "!!!")
    tb = sys.exc_info(  )[2]
    while 1:
        if not tb.tb_next:
            break
        tb = tb.tb_next
    stack = []
    f = tb.tb_frame
    while f:
        stack.append(f)
        f = f.f_back
    stack.reverse(  )
    traceback.print_exc(  )
    print "Locals by frame, innermost last"
    for frame in stack:
        print
        print "Frame %s in %s at line %s" % (frame.f_code.co_name,
                                             frame.f_code.co_filename,
                                             frame.f_lineno)
        for key, value in frame.f_locals.items(  ):
            print "\t%20s = " % key,
            # We have to be VERY careful not to cause a new error in our error
            # printer! Calling str(  ) on an unknown object could cause an
            # error we don't want, so we must use try/except to catch it --
            # we can't stop it from happening, but we can and should
            # stop it from propagating if it does happen!
            try:
                print value
            except:
                print "<ERROR WHILE PRINTING VALUE>"

    p("END Extended Traceback", "!!!")


def raising_code_info():
    ## could be deleted
    code_info = ''
    try:    
        frames = inspect.trace()
        p(frames)
        #print frames
        # for fr in frames:
        #     print fr
        if(len(frames)):
            full_method_name = frames[0][4][0].rstrip('\n\r').strip()
            line_number      = frames[1][2]
            module_name      = frames[0][0].f_globals['__name__']
            if(module_name == '__main__'):
                module_name = os.path.basename(sys.argv[0]).replace('.py','')
            class_name = ''
            obj_name_dot_method = full_method_name.split('.', 1)
            if len(obj_name_dot_method) > 1:
                obj_name, full_method_name = obj_name_dot_method
                try:
                    class_name = frames[0][0].f_locals[obj_name].__class__.__name__
                except:
                    pass
            method_name = module_name + '.'
            if len(class_name) > 0:
                method_name += class_name + '.'
            method_name += full_method_name
            code_info = '%s, line %d' % (method_name, line_number)
    finally:
        del frames
        sys.exc_clear()
    return (code_info,frames)
