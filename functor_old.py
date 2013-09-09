# http://adit.io/posts/2013-04-17-functors,_applicatives,_and_monads_in_pictures.html
# http://gabrielsw.blogspot.com/2011/08/functors-applicative-functors-and.html

from functools import partial

# a function
def adder(a, b):
    return a+b

# a partial function
add3 = partial(adder, 3)

# test it

assert add3(20) == 23

# FUNCTOR: A box to store value(s) with associated fmap that knows how to unbox value, apply given function, put in a different box of same kind

# why do you want to box: for example lazy evaluation

# a type, a box for storing Just a value or Nothing
class Maybe(object):
    def __init__(self, value):
        self.value = value

    # Maybe (box) defines how it can take a function and then: unbox its value, apply function, box result in the same type
    # Hurray! Now I am a functor!
    def fmap(self, fn):
        if self.value is not None:
            return Maybe(fn(self.value))
        return Maybe(None)

    def __str__(self):
        return "Maybe(%s)" % (self.value,)

    def __eq__(self, other):
        return isinstance(other, Maybe) and ((self.value is None and other.value is None) or (self.value == other.value))

class Just(Maybe):
    pass

class Nothing(Maybe):
    def __init__(self):
        super(Nothing, self).__init__(None)


# some tests
x = Just(2)
y = x.fmap(add3)
assert y == Just(5)

n = Nothing()
yn = n.fmap(add3)
assert yn == Nothing()

# practical use-case
def get_post_by_id(title_id):
    if title_id < 10:
        return Just({"title" : "Title-%s" % (title_id, ), "subject" : "my first post", "body" : "how are you?" })
    else:
        return Nothing()

def get_post_title(post):
    return post['title']

assert get_post_by_id(9).fmap(get_post_title)  == Just("Title-9")
assert get_post_by_id(11).fmap(get_post_title) == Nothing()

# List is also a functor

# for example it boxes more than one item
l = [2, 3, 4, 5]

# and provides an fmap (=map) that takes each, applies a function and generates a new List of results

l3 = map(add3, l )
assert l3 == [5, 6, 7, 8]

# functions are also functors! fmap is just composition!

add5 = partial(adder, 5)

def fmap_adder(a1, a2):
    def x(v):
        v2 = a2(v)
        v3 = a1(v2)
        return v3

    return x

add8 = fmap_adder(add3, add5)

assert add8(10) == 18



# On to applicative:
# APPLICATIVE, just like FUNCTOR except that the function passed to fmap itself is wrapped in another box, and it is not called fmap anymore, but lt_star_gt

just_add3 = Just(add3)

def lt_star_gt_adder( fn, value):
    return Just(fn.value(value.value))


assert lt_star_gt_adder(just_add3, Just(5)) == Just(8)

print lt_star_gt_adder(Just(partial(adder, 5)), Just(3))


# On to Monads:

def bind_maybe(a, f ):

    if isinstance(a, Nothing): return Nothing()
    else: return f(a.value)

def half(v):
    if v % 2 == 0:
        return Just(v/2)
    else:
        return Nothing()

assert bind_maybe(Just(6), half) == Just(3)

assert bind_maybe(bind_maybe(Just(6), half), half) == Nothing()

