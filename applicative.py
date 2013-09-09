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
    def fmap_old(self, fn):
        if self.value is not None:
            return Maybe(fn(self.value))
        return Maybe()

    def fmap(self, fn):
        return Maybe(fn).ap(self)

    def fmap2(self, fn):
        if self.value is not None:
            def ifn(v1, v2):
                if v2.value is not None:
                    return Maybe(fn(v1.value, v2.value))
                else:
                    return Maybe()
            return (lambda y: ifn(self, y) )

        else:
            return Maybe()

    # make Maybe a Monad, for implementing iffy/miffy challenge
    def bind(self, f):
        if self.value is not None:
            return f(self.value)
        else:
            return Maybe()
        # now ap can simply forward to bind as: self.bind(wfn.value)

    def __str__(self):
        return "Maybe(%s)" % (self.value,)

    def __eq__(self, other):
        return isinstance(other, Maybe) and ((self.value is None and other.value is None) or (self.value == other.value))

    # make Maybe an Applicative
    def ap(self, arg = None):
        if arg is not None and self.value is not None and arg.value is not None:
            return Maybe(partial(self.value, arg.value))
        elif arg is None and self.value is not None:
            return Maybe(self.value())
        else:
            return Maybe()
        # fmap can be a simply a forward to this now as self.ap(Maybe(fn))

def fmap(f, a):
    return a.fmap(f)

def ap(mfn, mv = None):
    if mv is None:
        return mfn.ap()
    else:
        return mfn.ap(mv)

def fmap2(f, a, b):
    return a.fmap2(f)(b)

class MyList(list):

    def fmap(self, f):
        return MyList(map(f, self))

    @classmethod
    def pure(cls, x):
        # TODO return infinite list of x
        pass

    """
        ap ( MyList([add3]),  MyList([1,2,3]) ) == MyList[4, 5, 6]
    """
    def zip_list(self, l2):
        return MyList([ f(e) for f in self for e in l2])

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

def applicative_client():

    mult_by_two = lambda x : 2 * x

    # Let's say that you want to operate on Maybe integer with the mult_by_two function instead of integer directly,
    # (why do you want to do this, see functor.py for the details)
    # like mult_by_two(Maybe(15) - obviously you can't do it directly - but you can use functor!

    fmap(mult_by_two, Maybe(15)) == Maybe(30)

    # That is great, but, let's say you have a two argument function

    mul = lambda x, y: x * y

    # and you want to mult not on ints but Maybe ints
    # you can do something like fmap2 

    fmap2(mul, Maybe(5), Maybe(13)) == Maybe(65)


    # now, let's say you have a 3 argument function

    mul3 = lambda x, y, z: x*y*z

    #and again, you want to operate on Maybe instead of integers directly

    # you have to build fmap3 - and so on for each argument - not a generic solution
    # print fmap3(mul3, Maybe(2), Maybe(3), Maybe(4))

    #
    # Alternatively, if you do, 
    # fmap(mul3, Maybe(2)) 
    # the result is partial of mul3 with first argument applied - unfortunately the output (partial) function is wrapped in Maybe
    # So, what we need something that can take the boxed function, boxed variable, open the function and variable and apply to
    # create a new partial (or result), rebox the result and return it
    # Now that is "ap" operation, or Applicative Functor!
    #


    # Note extra ap call in below examples with 1 arg - this is to invoke final partial to get result
    # This is particularly useful if you have fun with optional arguments
    ap(ap(ap(Maybe(mul), Maybe(5)),  Maybe(13))) == 65 
    ap(ap(ap(Maybe(mul), Maybe()),  Maybe(13))) == Maybe()
    ap(ap(fmap(mul, Maybe(17)), Maybe(6))) == 102
    ap(ap(ap(fmap(mul3, Maybe(2)), Maybe(3)), Maybe(4))) == Maybe(24)

    # real advantage, you see when one of arguments is Nothing, answer is Nothing and you do this without if statement
    ap(ap(ap(fmap(mul3, Maybe(2)), Maybe()), Maybe(4))) == Maybe()

    MyList([mult_by_two]).zip_list(MyList([1,2,3]) ) == MyList([2,4,6])

    mulab = lambda a: lambda b: a * b  # curried version of 'def mul(a,b): return a*b'
    assert MyList([mulab]).zip_list(MyList([1,2,3]) ).zip_list(MyList([10,20,30])) == MyList([10, 20, 30, 20, 40, 60, 30, 60, 90])

    # also do iffy/miffy problem
    # http://stackoverflow.com/questions/17409260/what-advantage-does-monad-give-us-over-an-applicative
    # http://www.haskell.org/pipermail/haskell-cafe/2009-May/059649.html
   
    condf = lambda c, x, y: x if x else y
    
    print "ifA ..." , ap (ap (ap( ap(Maybe(condf), Maybe(True)), Maybe(1) ), Maybe(2)))
    print "ifA ..." , ap (ap (ap( ap(Maybe(condf), Maybe(True)), Maybe(1) ), Maybe()))

    # TODO now with miffy
    ifM = lambda c, x, y: Maybe(c).bind(lambda z: x if z else y)

    print "ifM ...", ifM(True, Maybe(1), Maybe(2))
    print "ifM ...", ifM(True, Maybe(1), Maybe())

    
applicative_client()
