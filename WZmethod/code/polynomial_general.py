'''Imports'''
from random import randint as RI

'''Constant class'''
class constant:
    def __init__(self,value,variable=None):
        self.coefficients = [value]
        self.degree = 0
        self.is_zero = (value == 0)
        self.variables = []

    def equals(self,other):
        if other.variables != self.variables: return False
        return self.coefficients[0] == other.coefficients[0]

    def simplify(self):
        return self

    def add(self,other):
        assert self.variables == other.variables, 'Trying to add polynomials of different variables.'
        return constant(self.coefficients[0]+other.coefficients[0])

    def multiply(self,other):
        assert self.variables == other.variables, 'Trying to multiply polynomials of different variables.'
        return constant(self.coefficients[0]*other.coefficients[0])

    def power(self,n):
        return constant(pow(self.coefficients[0],n))

    def negate(self):
        return constant(-self.coefficients[0])

    # Returns (q,r,f) such that f*self/other = q + r/other. (f is a constant)
    def divide(self,other):
        assert self.variables == other.variables, 'Trying to divide polynomials of different variables.'
        return (constant(self.coefficients[0]//other.coefficients[0]),
                constant(self.coefficients[0]%other.coefficients[0]),
                constant(1))

    def modulo(self,other):
        assert self.variables == other.variables, 'Trying to modulo polynomials of different variables.'
        q,r,f = self.divide(other)
        return r

    def gcd(self,other):
        assert self.variables == other.variables, 'Trying to gcd polynomials of different variables. {} {}'.format(self.variables,other.variables)
        if other.is_zero: return self
        return other.gcd(self.modulo(other))

    def to_string(self):
        return str(self.coefficients[0])

    def PRINT(self):
        print(self.to_string())

'''Polynomial class'''
class polynomial:
    def __init__(self,coefficients,variable):
        self.coefficients = coefficients
        while len(self.coefficients) > 1 and self.coefficients[-1].is_zero:
            self.coefficients.pop()
        self.degree = len(self.coefficients) - 1
        self.is_zero = (self.degree==0 and self.coefficients[0].is_zero)
        assert variable not in self.coefficients[0].variables, 'Duplicate variable name.'
        self.variables = [variable] + self.coefficients[0].variables

    def equals(self,other):
        assert self.variables == other.variables, 'Trying to check equality polynomials of different variables.'
        if self.degree != other.degree: return False
        for i in range(self.degree+1):
            if not self.coefficients[i].equals(other.coefficients[i]):
                return False
        return True

    def get_constant(self,value):
        cur = constant(value)
        for x in self.variables[::-1]:
            cur = polynomial([cur],x)
        return cur

    def get_prev_constant(self,value):
        cur = constant(value)
        for x in self.variables[-1:0:-1]:
            cur = polynomial([cur],x)
        return cur

    def simplify(self):
        raise Exception('simplify not implemented')
        g = self.gcd_list()
        return polynomial([c.divide(g) for c in self.coefficients])

    def add(self,other):
        assert self.variables == other.variables, 'Trying to add polynomials of different variables.'
        c = [self.get_prev_constant(0) for _ in range(max(self.degree,other.degree)+1)]
        for i in range(self.degree+1):
            c[i] = c[i].add(self.coefficients[i])
        for i in range(other.degree+1):
            c[i] = c[i].add(other.coefficients[i])
        return polynomial(c,self.variables[0])

    def multiply(self,other):
        assert self.variables == other.variables, 'Trying to multiply polynomials of different variables.'
        c = [self.get_prev_constant(0) for _ in range(self.degree+other.degree+1)]
        for i in range(self.degree+1):
            for j in range(other.degree+1):
                c[i+j] = c[i+j].add(self.coefficients[i].multiply(other.coefficients[j]))
        return polynomial(c,self.variables[0])

    def power(self,n):
        if n == 0:
            return self.get_constant(1)
        return self.power(n-1).multiply(self)

    def negate(self):
        return polynomial([c.negate() for c in self.coefficients],self.variables[0])

    # Returns (q,r,f) such that f*self/other = q + r/other. (f is a constant)
    def divide(self,other):
        assert self.variables == other.variables, 'Trying to divide polynomials of different variables.'
        '''This if statement is not optimal'''
        if other.degree == 0:
            if other.coefficients[0].is_zero:
                raise Exception('Polynomial divided by 0')
            g = self.gcd_list().gcd(other.coefficients[0])
            return (polynomial([c.divide(g)[0] for c in self.coefficients],self.variables[0]),
                    self.get_constant(0),
                    other.coefficients[0].divide(g)[0])
        if self.degree < other.degree:
            return (self.get_constant(0),self,self.get_prev_constant(1))
        f0 = other.coefficients[-1]
        deg = self.degree-other.degree
        q0 = polynomial([self.get_prev_constant(0) for _ in range(deg)]+[self.coefficients[-1]],self.variables[0])
        r0 = self.multiply(polynomial([f0],self.variables[0])).add(q0.multiply(other).negate())
        q1,r1,f1 = r0.divide(other)
        q,r,f = q0.multiply(polynomial([f1],self.variables[0])).add(q1),r1,f0.multiply(f1)
        #return (q0.multiply(polynomial([f1],self.variables[0])).add(q1),r1,f0.multiply(f1))
        g = q.gcd_list().gcd(f).gcd(r.gcd_list())
        for i in range(q.degree+1):
            q.coefficients[i] = q.coefficients[i].divide(g)[0]
        for i in range(r.degree+1):
            r.coefficients[i] = r.coefficients[i].divide(g)[0]
        f = f.divide(g)[0]
        return (q,r,f)

    def modulo(self,other):
        assert self.variables == other.variables, 'Trying to modulo polynomials of different variables.'
        q,r,f = self.divide(other)
        return r

    def gcd(self,other):
        assert self.variables == other.variables, 'Trying to gcd polynomials of different variables.'
        if other.is_zero: return self#.simplify()
        return other.gcd(self.modulo(other))

    def gcd_list(self):
        if self.degree == 0: return self.coefficients[0]
        out = self.coefficients[0].gcd(self.coefficients[1])
        for x in self.coefficients[2:]:
            out = out.gcd(x)
        return out

    def to_string(self):
        out = []
        for i,c in enumerate(reversed(self.coefficients)):
            if c.is_zero and self.degree > 0: continue
            if i: out.append('+')
            out.append('{}{}{}{}{}{}'.format('(' if len(self.variables)>1 else '',
                                    c.to_string() if (len(self.variables)>1 or c.to_string()!='1' or i==self.degree) else '',
                                    ')' if len(self.variables)>1 else '',
                                    self.variables[0] if i<self.degree else '',
                                    '^' if i<self.degree-1 else '',
                                    self.degree-i if i<self.degree-1 else ''))
        return ''.join(out)

    def PRINT(self):
        print(self.to_string())

'''Help functions
def gcd(a,b):
    if a < 0 or b < 0: return gcd(abs(a),abs(b))
    return gcd(b,a%b) if b else a

def gcd_list(l):
    l_copy = list(l)
    while len(l_copy) > 1:
        l_copy.append(gcd(l_copy.pop(),l_copy.pop()))
    return l_copy[0]

def lcm(a,b):
    return a*b//gcd(a,b)

def sign(a):
    if a < 0: return -1
    elif a == 0: return 0
    else: return 1
'''

'''TESTING'''
if __name__ == '__main__':
    c0 = constant(0)
    c1 = constant(1)
    c2 = constant(2)
    c3 = constant(3)
    c4 = constant(4)
    c0.PRINT()
    c1.PRINT()
    c2.PRINT()
    c3.PRINT()
    c4.PRINT()
    p1 = polynomial([c1,c2,c1],'x')
    p1.PRINT()
    p2 = polynomial([c1,c1],'x')
    p2.PRINT()
    p3 = polynomial([p1,p2],'y')
    p3.PRINT()
    p3.multiply(p3).PRINT()
    p3.power(2).PRINT()
    p4 = polynomial([c0,c0,c1,c0,c1],'z')
    p4.PRINT()
    p5 = p3.power(2)
    print('-----------------------------------')
    p3.PRINT()
    p5.PRINT()
    q,r,f = p5.divide(p3)
    q.PRINT()
    r.PRINT()
    f.PRINT()
    q2,r2,f2 = q.coefficients[1].divide(f)
    q2.PRINT()
    r2.PRINT()
    f2.PRINT()
    print('-----------------------')
    p1.PRINT()
    p2.PRINT()
    print(p2.power(2).equals(p1))
    p6 = polynomial([p3,p5],'z')
    p6.PRINT()
    print('------------------------------------')
    p7 = polynomial([constant(0),constant(1)],'x')
    p8 = polynomial([constant(13),constant(-3)],'x')
    p9,q9,f9 = p8.divide(p7)
    p7.PRINT()
    p8.PRINT()
    p9.PRINT()
    q9.PRINT()
    f9.PRINT()
    print('-------------------------------------')
    p10 = polynomial([constant(0),constant(1)],'x')
    p11 = polynomial([constant(0),constant(0),constant(1)],'x')
    p12 = polynomial([constant(0),constant(0),constant(-1)],'x')
    p13 = polynomial([constant(0)],'x')
    p14 = polynomial([p12,p11,p10],'y')
    p15 = polynomial([p13,p10],'y')
    p16,q16,f16 = p14.divide(p15)
    p16.PRINT()
    q16.PRINT()
    f16.PRINT()
    print('============================')
    p1 = polynomial([c1,c1],'x')
    p2 = polynomial([p1],'y')
    p3 = polynomial([p1,p1],'y')
    q,r,f = p3.divide(p2)
    print('p2')
    p2.PRINT()
    print('p3')
    p3.PRINT()
    print('q')
    q.PRINT()
    print('r')
    r.PRINT()
    print('f')
    f.PRINT()
