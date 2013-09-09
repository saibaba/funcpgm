#
# http://blog.tmorris.net/posts/monads-do-not-compose/
# what are the uses of functor? see http://en.wikibooks.org/wiki/Haskell/The_Functor_class
#
from functools import partial
from curry import curry

# a function
def adder(a, b):
    return a+b

# a partial function
add3 = partial(adder, 3)

def maybe_f(value):
    def g(fn):
        if value is not None:
            return maybe_f(fn(value))
        else:
            return maybe_f(value)
    return g

def fmap(fn, value):
    return value(fn)

def pret(value):
    print "Printing...", value
    return value

fmap(pret, fmap(add3, maybe_f(5)))
fmap(pret, fmap(add3, maybe_f(None)))

# fmap as lifting  a function a -> b to f a -> f b where f is any context (E.g.,  Maybe)
madd3 = curry(fmap)(add3)
fmap(pret, madd3(maybe_f(5)))

# Functor laws for maybe_f

# First, a couple of utils
def aret(match, value):
    assert value == match
    return value

def compose(f, g):
    def fg(*args, **kwargs):
        return f(g(*args, **kwargs))
    return fg


# law 1: f id = id
fmap(partial(aret, 3), fmap(lambda x : x, maybe_f(3)))
# law 2: fmap(f . g) = fmap f . fmap g 
f = lambda y: y+1
g = lambda x: 2*x
fg = compose(f, g)

# RHS:
fmap(partial(aret, 7), fmap(f, fmap(g, maybe_f(3)) ) )
# LHS:
fmap(partial(aret, 7), fmap(fg, maybe_f(3)))

# An ordinary function is also a functor, i.e., fmap of value  = g, in above call to fmap will lead to composition of fn and g
# but in python it is tough to make fmap behave as compose, only when value is callable - because we use maybe_f as function, every
# value is callable, not just functions. If we implement maybe_f as a class, we could manage to make it.So, redefine g:
g = lambda fn : lambda x: fn(x) * 2
x = fmap(f, g)
print x(10)
