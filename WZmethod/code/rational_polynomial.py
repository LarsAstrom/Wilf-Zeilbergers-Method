from polynomial_general import *
class rational_polynomial:
    def __init__(self,numerator,denominator):
        variables = numerator.get_common_variables(denominator)
        self.num = numerator.convert_polynomial(variables)
        self.den = denominator.convert_polynomial(variables)
        self.simplify()

    '''Methods only using self'''
    def invert(self):
        return rational_polynomial(self.den,self.num)

    def negate(self):
        return rational_polynomial(self.num.negate(),self.den)

    def power(self,n):
        return rational_polynomial(self.num.power(n),self.den.power(n))

    def simplify(self):
        g = self.num.gcd(self.den)
        self.num = self.num.divide(g)[0]
        self.den = self.den.divide(g)[0]

    def to_string(self):
        return '({})/({})'.format(self.num.to_string(),self.den.to_string())

    def PRINT(self):
        print self.to_string()

    '''Methods using other'''
    def add(self,other):
        n1,d1 = self.num,self.den
        n2,d2 = other.num,other.den
        return rational_polynomial(n1.multiply(d2).add(n2.multiply(d1)),
                                    d1.multiply(d2))

    def multiply(self,other):
        n1,d1 = self.num,self.den
        n2,d2 = other.num,other.den
        return rational_polynomial(n1.multiply(n2),d1.multiply(d2))

    def divide(self,other):
        return self.multiply(other.invert())
