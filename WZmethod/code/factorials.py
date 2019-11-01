from polynomial_general import *
def fac(n):
    return n*fac(n-1) if n else 1

class factorial:
    def __init__(self,value):
        if type(value) == str:
            self.value = parse(value)
        else:
            self.value = value

    def divide(self,other):
        if self.value.subtract(other.value).is_constant and constant_positive(self.value.subtract(other.value)):
            out = polynomial([constant(1)],self.value.variables[0])
            to_mult = other.value
            while not to_mult.equals(self.value):
                to_mult = to_mult.add(to_mult.get_constant(1))
                out = out.multiply(to_mult)
            c = parse(self.value.subtract(other.value).to_string()).coefficients[0]
            return out,constant(fac(c))
        elif other.value.subtract(self.value).is_constant:
            den,num = other.divide(self)
            return num,den
        return None

    def to_string(self):
        return '({})!'.format(self.value.to_string())

    def PRINT(self):
        print(self.to_string())

class expression_mult:
    def __init__(self,val=None):
        if val == None:
            self.val = [constant(1)]
        elif type(val) == list:
            self.val = val
        else:
            self.val = [val]

    def to_string(self):
        out = ['(']
        for i,x in enumerate(self.val):
            if i:
                out.append('*')
            out.append('(')
            out.append(x.to_string())
            out.append(')')
        out.append(')')
        return ''.join(out)

    def PRINT(self):
        print(self.to_string())

class expression_add:
    def __init__(self,val=None):
        if val == None:
            self.val = [expression_mult(constant(0))]
        elif type(val) == list:
            self.val = val
        else:
            self.val = [val]
        for i in range(len(self.val)):
            if type(self.val[i]) != type(expression_mult()):
                self.val[i] = expression_mult(self.val[i])

    def to_string(self):
        out = ['(']
        for i,x in enumerate(self.val):
            if i:
                out.append('+')
            out.append(x.to_string())
        out.append(')')
        return ''.join(out)

    def PRINT(self):
        print(self.to_string())

class expression_rat:
    def __init__(self,num=None,den=None):
        if num == None:
            self.num = expression_add()
        elif type(num) != type(expression_add):
            self.num = expression_add(num)
        else:
            self.num = num
        if den == None:
            self.den = expression_add()
        elif type(den) != type(expression_add):
            self.den = expression_add(den)
        else:
            self.den = den

    def to_string(self):
        return self.num.to_string() + '/' + self.den.to_string()

    def PRINT(self):
        print(self.to_string())

def simplify_divide(a,b):
    if type(a) != type(b): return a,b
    if type(a) == type(b) == type(factorial('a')):
        ans = a.divide(b)
        if ans == None: return a,b
        return ans[0],ans[1]
    if type(a) == type(b) == type(polynomial([constant(0)],'a')):
        g = a.gcd(b)
        return a.divide(g)[0],b.divide(g)[0]
    return a,b

def constant_positive(p):
    c = parse(p.to_string()).coefficients[0]
    return c >= 0

def binom(n,k):
    if type(n) == type(k) == int:
        return constant(fac(n)/(fac(n-k)*fac(k)))
    if type(n) == int:


if __name__ == '__main__':
    p1 = expression_mult()
    p2 = expression_mult(parse('k'))
    p3 = expression_mult([parse('k'),parse('n')])
    p1.PRINT()
    p2.PRINT()
    p3.PRINT()
    p4 = parse(p3.to_string())
    p4.PRINT()
    p5 = expression_add([parse('k'),parse('n')])
    p6 = expression_add([p3,p2])
    p5.PRINT()
    p6.PRINT()
    p7 = expression_mult([factorial('n'),factorial('k')])
    p8 = expression_add([p7,p3])
    p7.PRINT()
    p8.PRINT()
    p9 = expression_rat(p2,p3)
    p9.PRINT()
    f1 = factorial('n')
    f2 = factorial('n+3')
    a,b = simplify_divide(f1,f2)
    a.PRINT()
    b.PRINT()
