import functools
from datetime import datetime


def get_callable_name(func):
    if isinstance(func, functools.partial):
        return func.func.__func__.__name__
    else:
        return func.__name__


class TimeStamper:
    """
    A time stamper class
    """
    log = []
    indent_level = 0
    indent_increment = '  '
    
    def __init__(self):
        self.start_stamp = datetime.now()
        self.previous_stamp = self.start_stamp
        print("Initial timestamp:", str(self.start_stamp))
    
    def stamp(self, msg=None):
        tmp_stamp = datetime.now()
        
        time_elapsed = tmp_stamp - self.previous_stamp
        
        if self.indent_level:
            indent = self.indent_increment * self.indent_level
        else:
            indent = ''
        
        if msg:
            msg = "%sTime elapsed: %s | %s" % (indent, time_elapsed, msg)
        else:
            msg = "%sTime elapsed: %s" % (indent, time_elapsed)
        
        print(msg)
        self.log.append(msg)
        
        self.previous_stamp = tmp_stamp
        return tmp_stamp
    
    def run(self, func):
        
        name = get_callable_name(func)
        
        start = datetime.now()
        print('%s: starting %s' % (start, name))
        
        self.indent_level += 1
        
        func()
        
        finish = datetime.now()
        print('%s: finished in %s: %s' % (finish.now(), finish - start, name))
        
        self.indent_level -= 1
        
        self.previous_stamp = finish
    
    def __del__(self):
        tmp_stamp = self.stamp("\nTimerStamper is being destroyed.")
        print("Current timestamp:", str(tmp_stamp))
        print("Time since beginning of time:", str(tmp_stamp - self.start_stamp))
