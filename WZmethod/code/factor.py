import polynomial

def fac(n):
    return n*fac(n-1) if n else 1

'''Methods for checking which type a factor has'''
def is_polynomial(x):
    return type(x) in [polynomial.constant,polynomial.polynomial]

def is_factorial(x):
    return type(x) == factorial

def is_power(x):
    return type(x) == power

def is_factor(x):
    return (is_polynomial(x) or is_factorial(x) or is_power(x))

'''A class to store factorials. Can (sometimes) be divided by other factorial.'''
class factorial:
    def __init__(self,value):
        self.value = value
        assert is_polynomial(self.value), 'Value has to be polynomial.polynomial, not {}'.format(type(self.value))

    def divide(self,other):
        if is_positive_constant(self.value.subtract(other.value)):
            out = polynomial.polynomial([polynomial.constant(1)],self.value.variables[0])
            to_mult = other.value
            while not to_mult.equals(self.value):
                to_mult = to_mult.add(to_mult.get_constant(1))
                out = out.multiply(to_mult)
            return out,polynomial.constant(1)
        elif is_positive_constant(other.value.subtract(self.value)):
            den,num = other.divide(self)
            return num,den
        return None

    def is_divisible(self,other):
        return self.divide(other) != None

    def to_string(self):
        return '({})!'.format(self.value.to_string())

    def PRINT(self):
        print(self.to_string())

'''Class to store a integer to the power of a polynomial.'''
class power:
    def __init__(self,base,exponent):
        self.base = base
        self.exponent = polynomial.polynomial_parser(exponent.to_string())
        assert type(self.base) == int, 'Base has to be int, not {}'.format(type(self.base))
        assert is_polynomial(self.exponent), 'Exponent has to be polynomial.polynomial, not {}'.format(type(self.exponent))

    def inverse(self):
        return power(self.base,self.exponent.negate())

    def multiply(self,other):
        if self.base == other.base:
            exp = self.exponent.add(other.exponent)
            if is_positive_constant(exp):
                return polynomial.constant(pow(self.base,polynomial.polynomial_parser(exp.to_string()).coefficients[0]))
            return power(self.base,exp)
        elif self.exponent.equals(other.exponent):
            return power(self.base*other.base,self.exponent)
        return None

    def divide(self,other):
        return self.multiply(other.inverse())

    def is_divisible(self,other):
        return self.divide(other) != None

    def to_string(self):
        return '{}{}{}^({})'.format('(' if self.base < 0 else '',
                                    self.base,
                                    ')' if self.base < 0 else '',
                                    self.exponent.to_string())

    def PRINT(self):
        print(self.to_string())

'''
Returns f such that f divides a and b.
(f is the largest factor of b that divides a.)
'''
def try_divide(a,b):
    if type(a) != type(b):
        return None
    if is_polynomial(a):
        return a.gcd(b)
    if is_factorial(a):
        if is_positive_constant(a.value.subtract(b.value)):
            return b
        elif is_positive_constant(b.value.subtract(a.value)):
            return a
        return polynomial.constant(1)
    if is_power(a):
        if a.divide(b) != None:
            return b
        return polynomial.constant(1)

'''
Returns True if polynomial.polynomial p is a constant, that is positive, otherwise False.
'''
def is_positive_constant(p):
    c = polynomial.polynomial_parser(p.to_string())
    return type(c) == polynomial.constant and c.coefficients[0] >= 0
