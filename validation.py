#
# http://scalaz.googlecode.com/svn/continuous/latest/browse.sxr/scalaz/example/ExampleValidation.scala.html
# http://stackoverflow.com/questions/2545248/function-syntax-puzzler-in-scalaz/2546400#2546400
# http://blog.tmorris.net/posts/automated-validation-with-applicatives-and-semigroups-for-sanjiv/
# http://blog.tmorris.net/posts/automated-validation-with-applicatives-and-semigroups-part-2-java/
# http://dl.dropboxusercontent.com/u/7810909/docs/applicative-errors-scala/chunk-html/ar01s06s03.html
#

class Person(object):
    def __init__(self, name, age):
        self.name =name
        self.age = age

    def __eq__(self, other):
        return self.name == other.name and self.age == other.age

    def __str__(self):
        return "name=%s;age=%d" % (self.name, self.age)

class Validation(object):
    # applicative functor

    def __init__(self, v, is_fail = False):
        self.value = v
        self.is_fail = is_fail

    def __str__(self):
        return "is_fail="+str(self.is_fail)+";value="+str(self.value)

    def __eq__(self, other):
        return other.value == self.value and other.is_fail == self.is_fail

    def fmap(self, f):
        if not self.is_fail:
            return Success(f(self.value))
        else:
            return self

    # Make Validator an applicative functor 
    def __rshift__(self, other):
        if self.is_fail and other.is_fail:
            return Fail(self.value + other.value)
        if self.is_fail and (not other.is_fail):
            return Fail(self.value)
        if (not self.is_fail) and other.is_fail:
            return Fail(other.value)
        return Success( other.value (self.value ))

    # Make Validator an applicative functor  - another variation in usage
    def x__lshift__(self, other):
        if self.is_fail and other.is_fail:
            return Fail(self.value + other.value)
        if self.is_fail and (not other.is_fail):
            return Fail(self.value)
        if (not self.is_fail) and other.is_fail:
            return Fail(other.value)
        return Success( self.value (other.value ))

    def __lshift__(self, other):
        if self.is_fail and other.is_fail:
            return Fail(self.value + other.value)
        elif self.is_fail and (not other.is_fail):
            return Fail(self.value)
        elif (not self.is_fail) and other.is_fail:
            return Fail(other.value)
        else:
            return other.bind(lambda w: Success( self.value(w)  ) )

    # Bind operation - makes this into a monad
    def bind(self, f_a_mb):
        if not self.is_fail:
            return f_a_mb(self.value)
        else:
            return self

def Fail(e): return Validation(e, True)
def Success(a): return Validation(a, False)

def name(s):
    if s[0].isupper(): return Success(s)
    else: return Fail(["Name must start with a capital letter"])

def age(s):
    a =  int(s)
    if a > 0 and a < 131: return Success(a)
    else: return Fail(["Age must be between 0 and 131 (exclusive)"])

assert name("sai") == Fail(["Name must start with a capital letter"])
assert name("Sai") == Success("Sai")

def mk_person(n, a):
    from curry import curry
    #return name(n) >> ( age(a) >> Success(curry(lambda ag, nm: Person(nm, ag))))
    return Success(curry(lambda ag, nm: Person(nm, ag))) << age(a) << name(n)
    # You can try implementing above logic using bind given below, but if age(a) fails, the function passed to bind is not exeucted
    #  age(a).bind(...)  if age(a) returns Fail, bind will not call function passed to it - so no way you can accumulate results
    # See http://stackoverflow.com/questions/2545248/function-syntax-puzzler-in-scalaz/2546400#2546400


assert mk_person("Sai", 100).value == Person("Sai", 100)
assert mk_person("sai", 100).value ==  ['Name must start with a capital letter']
assert mk_person("sai", 150).value == ['Age must be between 0 and 131 (exclusive)','Name must start with a capital letter']
