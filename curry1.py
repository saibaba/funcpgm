# Coded by Massimiliano Tomassoli, 2012.
#
# - Thanks to b49P23TIvg for suggesting that I should use a set operation
#     instead of repeated membership tests.
# - Thanks to Ian Kelly for pointing out that
#     - "minArgs = None" is better than "minArgs = -1",
#     - "if args" is better than "if len(args)", and
#     - I should use "isdisjoint".
#
def genCur(func, unique = True, minArgs = None):
    """ Generates a 'curried' version of a function. """
    def g(*myArgs, **myKwArgs):
        def f(*args, **kwArgs):
            if args or kwArgs:                  # some more args!
                # Allocates data to assign to the next 'f'.
                newArgs = myArgs + args
                newKwArgs = dict.copy(myKwArgs)
 
                # If unique is True, we don't want repeated keyword arguments.
                if unique and not set(kwArgs.keys()).isdisjoint(newKwArgs):
                    raise ValueError("Repeated kw arg while unique = True")
 
                # Adds/updates keyword arguments.
                newKwArgs.update(kwArgs)
 
                # Checks whether it's time to evaluate func.
                if minArgs is not None and minArgs <= len(newArgs) + len(newKwArgs):
                    return func(*newArgs, **newKwArgs)  # time to evaluate func
                else:
                    return g(*newArgs, **newKwArgs)     # returns a new 'f'
            else:                               # the evaluation was forced
                return func(*myArgs, **myKwArgs)
        return f
    return g
 
def cur(f, minArgs = None):
    return genCur(f, True, minArgs)
 
def curr(f, minArgs = None):
    return genCur(f, False, minArgs)
 
def curry2(x, argc=None):
    if argc is None:
        argc = x.func_code.co_argcount
    def p(*a):
        if len(a) == argc:
            return x(*a)
        def q(*b):
            return x(*(a + b))
        return curry2(q, argc - len(a))
    return p
