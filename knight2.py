class KnightPos(object):

    class MyList(list):
        # monad move = bind
        def move(self):
            r  = []
            for i in self:
                r = r + i.move()

            return KnightPos.MyList(r)

    def __init__(self, x, y):
        self.x  = x
        self.y  = y

    def __str__(self):
        return "x=%d;y=%d" % (self.x,self.y)

    def unit(self):
        return KnightPos.MyList([self])
    
    def move(self):
        r = []
        r.append( (self.x-1,self.y+2) )
        r.append( (self.x-1,self.y-2) )
        r.append( (self.x+1,self.y+2) )
        r.append( (self.x+1,self.y-2) )
        r.append( (self.x-2,self.y+1) )
        r.append( (self.x-2,self.y-1) )
        r.append( (self.x+2,self.y+1) )
        r.append( (self.x+2,self.y-1) )

        r = [(a,b) for a,b in r if a>0 and b>0 and a < 9 and b < 9]

        return KnightPos.MyList( [KnightPos(a,b) for a,b in r] )

u = KnightPos(6,2).unit()

for x in  u.move().move().move():
    print "hi", x
