#
# http://blog.tmorris.net/posts/monads-do-not-compose/
# what are the uses of functor? see http://en.wikibooks.org/wiki/Haskell/The_Functor_class
#
from functools import partial

# a function
def adder(a, b):
    return a+b

# a partial function
add3 = partial(adder, 3)


class Maybe(object):
    def __init__(self, value = None):
        self.value = value

    # Make Maybe a Functor
    def fmap(self, fn):
        if self.value is not None:
            return Maybe(fn(self.value))
        return Maybe()

    def __str__(self):
        return "Maybe(%s)" % (self.value,)

    def __eq__(self, other):
        return isinstance(other, Maybe) and ((self.value is None and other.value is None) or (self.value == other.value))


# some tests
x = Maybe(2)
y = x.fmap(add3)
assert y == Maybe(5)

# check functor rule 1: fmap id = id
Maybe(23).fmap(lambda x: x) == Maybe(23)
# check functor rule 2: fmap (p . q) = fmap p . fmap q
Maybe(30).fmap(lambda x : 2*x).fmap(lambda x : x-1) == Maybe(30).fmap ( lambda y : 2*y-1)

n = Maybe()
yn = n.fmap(add3)
assert yn == Maybe()

# client programs using functors do not care whether the functor is list, maybe, tree, etc., and can use fmap generically
def fmap(f, a):
    return a.fmap(f)

class MyList(list):
    def fmap(self, f):
        return MyList(map(f, self))

class TreeMap(object):
    def __init__(self, left, right, v, is_leaf):
        self.left = left
        self.right = right
        self.is_leaf = is_leaf
        self.value = v

    def fmap(self, f):
        # you can simplify all of these using Maybe!
        if self.is_leaf:
            return leaf(f(self.value))
        else:
            fl = None
            if self.left is not None:
                fl = self.left.fmap(f)
            fr = None
            if self.right is not None:
                fr = self.right.fmap(f)
            return branch(fl, fr)

    def __eq__(self, other):
        s =  (self.value is None and other.value is None) or (self.value is not None and other.value is not None and self.value == other.value)
        if not s: return s
        s = (self.left is None and self.right is None) or (self.left is not None and other.left is not None and self.left == other.left)
        if not s: return s
        s = (self.right is None and self.right is None) or (self.right is not None and other.right is not None and self.right == other.right)
        return s

      
    def __str__(self):
        s = ""
        if self.value is not None:
            s = s + "value=" + str( self.value)
        if self.left is not None:
            s  =  s + ";left=" + str(self.left)
        if self.right is not None:
            s  =  s + ";right=" + str(self.right)
        return s

def branch(l, r):
    return TreeMap(l, r, None, False)

def leaf(v):
    return TreeMap(None, None, v, True)

def functor_client():

    mult_by_two = lambda x : 2 * x
    l  = MyList([3, 4, 5])

    assert fmap(mult_by_two, Maybe(20)) == Maybe(40)
    assert fmap(mult_by_two, l) == MyList([6, 8, 10])

    #fmult_by_two = lambda fx: fmap(mult_by_two, fx)   # partial function
    fmult_by_two = partial(fmap, mult_by_two)

    fl = MyList([Maybe(1), Maybe(2), Maybe(3), Maybe()])
    assert  fmap(fmult_by_two, fl) == MyList([Maybe(2), Maybe(4), Maybe(6), Maybe()])

    tree1 = branch(branch(leaf(1),  leaf(2)), branch(leaf(3), leaf(4)))
    tree2 = branch(branch(leaf(2),  leaf(4)), branch(leaf(6), leaf(8)))
    assert fmap(mult_by_two, tree1) == tree2

functor_client()
