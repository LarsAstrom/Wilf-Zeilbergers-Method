'''Imports'''
from random import randint as RI

'''Polynomial class'''
class polynomial:
    def __init__(self,coefficients):
        self.coefficients = coefficients
        while len(self.coefficients) > 1 and self.coefficients[-1] == 0:
            self.coefficients.pop()
        self.degree = len(self.coefficients) - 1
        self.is_zero = (self.degree==0 and self.coefficients[0]==0)

    def simplify(self):
        g = gcd_list(self.coefficients)
        return polynomial([c//g for c in self.coefficients])

    def add(self,other):
        c = [0]*max(len(self.coefficients),len(other.coefficients))
        for i in range(len(self.coefficients)):
            c[i] += self.coefficients[i]
        for i in range(len(other.coefficients)):
            c[i] += other.coefficients[i]
        return polynomial(c)

    def multiply(self,other):
        c = [0]*(len(self.coefficients)+len(other.coefficients)-1)
        for i in range(len(self.coefficients)):
            for j in range(len(other.coefficients)):
                c[i+j] += self.coefficients[i]*other.coefficients[j]
        return polynomial(c)

    def power(self,n):
        if n == 0:
            return polynomial([1])
        return self.power(n-1).multiply(self)

    def negate(self):
        return polynomial([-c for c in self.coefficients])

    # Returns (q,r,f) such that f*self/other = q + r/other. (f is a constant)
    def divide(self,other):
        if other.degree == 0:
            if other.coefficients[0] == 0:
                raise Exception('Polynomial divided by 0')
            return (self,polynomial([0]),other.coefficients[0])
        if self.degree < other.degree:
            return (polynomial([0]),self,1)
        f0 = lcm(self.coefficients[-1],other.coefficients[-1])//self.coefficients[-1]
        deg = self.degree-other.degree
        q0 = polynomial([0]*deg+[lcm(self.coefficients[-1],other.coefficients[-1])//other.coefficients[-1]])
        r0 = self.multiply(polynomial([f0])).add(q0.multiply(other).negate())
        q1,r1,f1 = r0.divide(other)
        return (q0.multiply(polynomial([f1*sign(f0*f1)])).add(q1),r1,f0*f1*sign(f0*f1))

    def modulo(self,other):
        q,r,f = self.divide(other)
        return r

    def gcd(self,other):
        if other.is_zero: return self.simplify()
        return other.gcd(self.modulo(other))

    def PRINT(self,variable='x'):
        for i,c in enumerate(reversed(self.coefficients)):
            if c == 0 and self.degree > 0: continue
            if i or c < 0: print('{}'.format('+' if c > 0 else '-'),end='')
            print('{}{}{}{}'.format(abs(c) if (abs(c)!=1 or i==self.degree) else '',
                                    variable if i<self.degree else '',
                                    '^' if i<self.degree-1 else '',
                                    self.degree-i if i<self.degree-1 else ''),end='')
        print()

'''Help functions'''
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

'''TESTING'''
if __name__ == '__main__':
    p1 = polynomial([2,2])
    p2 = polynomial([1,2,1])
    p3 = polynomial([1,1]).power(3)
    p4 = polynomial([-1,0,1])
    p5 = polynomial([2,4,2])
    p6 = polynomial([-1,-2,-1])
    p7 = polynomial([-1,-1])
    p1.PRINT()
    p2.PRINT()
    p3.PRINT()
    p4.PRINT()
    p5.PRINT()
    p6.PRINT()
    p7.PRINT()
    for num in [p1,p2,p3,p4,p5,p6,p7]:
        for den in [p1,p2,p3,p4,p5,p6,p7]:
            print('----------------------------')
            print('NUMERATOR:')
            num.PRINT()
            print()
            print('DENOMINATOR:')
            den.PRINT()
            print()
            q,r,f = num.divide(den)
            print('QUOTIENT:')
            q.PRINT()
            print('REMAINDER:')
            r.PRINT()
            print('FACTOR: {}'.format(f))
            print('----------------------------')

    g = p1.gcd(p2)
    g.PRINT()

    q1 = polynomial([-1,1])
    q2 = polynomial([-265692,3])
    q3 = polynomial([-11,13])
    q4 = polynomial([73,-37])
    q = [q1,q2,q3,q4]
    qs = [[q[i].multiply(q[j]) for j in range(4)] for i in range(4)]
    for _ in range(10):
        i1,j1,i2,j2 = RI(0,3),RI(0,3),RI(0,3),RI(0,3)
        print('===================')
        q[i1].PRINT()
        q[j1].PRINT()
        q[i2].PRINT()
        q[j2].PRINT()
        qs[i1][j1].gcd(qs[i2][j2]).PRINT()
        print('===================')
