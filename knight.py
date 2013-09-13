class MyList(list):
    # monad move = bind
    def map(self, fn):
        r  = []
        for i in self:
            r = r + fn(i)

        return MyList(r)

    def __rshift__(self, fn):
        return self.map(fn)

class KnightPos(object):

    def __init__(self, x, y):
        self.x  = x
        self.y  = y

    def __str__(self):
        return "x=%d;y=%d" % (self.x,self.y)

    def unit(self):
        return MyList([self])
    
def move_knight(k):
    r = []
    r.append( (k.x-1,k.y+2) )
    r.append( (k.x-1,k.y-2) )
    r.append( (k.x+1,k.y+2) )
    r.append( (k.x+1,k.y-2) )
    r.append( (k.x-2,k.y+1) )
    r.append( (k.x-2,k.y-1) )
    r.append( (k.x+2,k.y+1) )
    r.append( (k.x+2,k.y-1) )

    r = [(a,b) for a,b in r if a>0 and b>0 and a < 9 and b < 9]

    return MyList( [KnightPos(a,b) for a,b in r] )

u = KnightPos(6,2).unit()

for x in  u >> move_knight >> move_knight >> move_knight:
    print "hi", x
