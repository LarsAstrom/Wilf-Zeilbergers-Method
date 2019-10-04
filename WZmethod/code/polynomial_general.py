'''Imports'''
from random import randint as RI

'''Constant class'''
class constant:
    '''Methods only using self'''
    def __init__(self,value,variable=None):
        self.coefficients = [value]
        self.degree = 0
        self.is_zero = (value == 0)
        self.variables = []

    def get_constant(self,value):
        return constant(value)

    def get_prev_constant(self,value):
        raise Exception('Not possible to get prev constant for a constant')

    def simplify(self):
        return self

    def power(self,n):
        return constant(pow(self.coefficients[0],n))

    def negate(self):
        return constant(-self.coefficients[0])

    def to_string(self):
        return str(self.coefficients[0])

    def PRINT(self):
        print(self.to_string())

    '''Methods using other'''
    def get_common_variables(self,other):
        return other.variables

    def equals(self,other):
        if other.variables != self.variables: return False
        return self.coefficients[0] == other.coefficients[0]

    def add(self,other):
        assert self.variables == other.variables, 'Trying to add polynomials of different variables.'
        return constant(self.coefficients[0]+other.coefficients[0])
    def add_simple(self,other): return self.add(other)

    def multiply(self,other):
        assert self.variables == other.variables, 'Trying to multiply polynomials of different variables.'
        return constant(self.coefficients[0]*other.coefficients[0])
    def multiply_simple(self,other): return self.multiply(other)

    def divide(self,other):
        # Returns (q,r,f) such that f*self/other = q + r/other. (f is a constant)
        assert self.variables == other.variables, 'Trying to divide polynomials of different variables.'
        return (constant(self.coefficients[0]//other.coefficients[0]),
                constant(self.coefficients[0]%other.coefficients[0]),
                constant(1))
    def divide_simple(self,other): return self.divide(other)

    def modulo(self,other):
        assert self.variables == other.variables, 'Trying to modulo polynomials of different variables.'
        q,r,f = self.divide(other)
        return r
    def modulo_simple(self,other): return self.modulo(other)

    def gcd(self,other):
        assert self.variables == other.variables, 'Trying to gcd polynomials of different variables. {} {}'.format(self.variables,other.variables)
        if other.is_zero: return self
        return other.gcd(self.modulo(other))
    def gcd_simple(self,other): return self.gcd(other)

'''Polynomial class'''
class polynomial:
    '''Methods only using self'''
    def __init__(self,coefficients,variable):
        self.coefficients = coefficients
        while len(self.coefficients) > 1 and self.coefficients[-1].is_zero:
            self.coefficients.pop()
        self.degree = len(self.coefficients) - 1
        self.is_zero = (self.degree==0 and self.coefficients[0].is_zero)
        assert variable not in self.coefficients[0].variables, 'Duplicate variable name.'
        self.variables = [variable] + self.coefficients[0].variables

    def convert_polynomial(self,variables):
        for var in self.variables:
            assert var in variables, 'Cannot convert {} to {}, because {} is missing.'\
                                        .format(self.to_string(),variables,var)
        return parse(self.to_string(),variables)

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

    def power(self,n):
        if n == 0:
            return self.get_constant(1)
        return self.power(n-1).multiply_simple(self)

    def negate(self):
        return polynomial([c.negate() for c in self.coefficients],self.variables[0])

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

    '''Methods using other'''
    def get_common_variables(self,other):
        return sorted(list(set(self.variables)|set(other.variables)))[::-1]

    def equals(self,other):
        assert self.variables == other.variables, 'Trying to check equality polynomials of different variables.'
        if self.degree != other.degree: return False
        for i in range(self.degree+1):
            if not self.coefficients[i].equals(other.coefficients[i]):
                return False
        return True

    def add(self,other):
        if self.variables == other.variables:
            return self.add_simple(other)
        vars = self.get_common_variables(other)
        return self.convert_polynomial(vars).add(other.convert_polynomial(vars))
    def add_simple(self,other):
        assert self.variables == other.variables, 'Trying to add polynomials of different variables.'
        c = [self.get_prev_constant(0) for _ in range(max(self.degree,other.degree)+1)]
        for i in range(self.degree+1):
            c[i] = c[i].add(self.coefficients[i])
        for i in range(other.degree+1):
            c[i] = c[i].add(other.coefficients[i])
        return polynomial(c,self.variables[0])

    def multiply(self,other):
        if self.variables == other.variables:
            return self.multiply_simple(other)
        vars = self.get_common_variables(other)
        return self.convert_polynomial(vars).multiply(other.convert_polynomial(vars))
    def multiply_simple(self,other):
        assert self.variables == other.variables, 'Trying to multiply polynomials of different variables.'
        c = [self.get_prev_constant(0) for _ in range(self.degree+other.degree+1)]
        for i in range(self.degree+1):
            for j in range(other.degree+1):
                c[i+j] = c[i+j].add(self.coefficients[i].multiply_simple(other.coefficients[j]))
        return polynomial(c,self.variables[0])

    def divide(self,other):
        if self.variables == other.variables:
            return self.divide_simple(other)
        vars = self.get_common_variables(other)
        return self.convert_polynomial(vars).divide(other.convert_polynomial(vars))
    def divide_simple(self,other):
        # Returns (q,r,f) such that f*self/other = q + r/other. (f is of same type as coefficients)
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
        if self.variables == other.variables:
            return self.modulo_simple(other)
        vars = self.get_common_variables(other)
        return self.convert_polynomial(vars).modulo(other.convert_polynomial(vars))
    def modulo_simple(self,other):
        assert self.variables == other.variables, 'Trying to modulo polynomials of different variables.'
        q,r,f = self.divide(other)
        return r

    def gcd(self,other):
        if self.variables == other.variables:
            return self.gcd_simple(other)
        vars = self.get_common_variables(other)
        return self.convert_polynomial(vars).gcd(other.convert_polynomial(vars))
    def gcd_simple(self,other):
        assert self.variables == other.variables, 'Trying to gcd polynomials of different variables.'
        if other.is_zero: return self#.simplify()
        return other.gcd(self.modulo(other))

def print_stack(stack):
    print('---------PRINT STACK----------')
    for a in stack:
        if type(a) == type(polynomial([constant(0)],'x')):
            print(a.variables,a.to_string())
        else:
            print(a)
    print('------------------------------')

def parse(s,variables = None):
    #raise Exception('parse not implemented')
    if variables == None: variables = get_variables(s)
    def simplify(stack):
        if len(stack) == 1: return stack
        if stack[-2] == '(': return stack
        b,op,a = stack.pop(),stack.pop(),stack.pop()
        if op == '+':
            stack.append(a.add(b))
        elif op == '-':
            stack.append(a.add(b.negate()))
        elif op == '*':
            stack.append(a.multiply(b))
        elif op == '/':
            raise Exception('parse with divide not implemented')
            #stack.append(a.divide())
        return simplify(stack)

    def constant_with_value(val):
        cur = constant(val)
        for var in variables[::-1]:
            cur = polynomial([cur],var)
        return cur
    def poly_from_char(ch):
        cur = constant(1)
        for var in variables[::-1]:
            if var == ch:
                cur = polynomial([cur.get_constant(0), cur],var)
            else:
                cur = polynomial([cur],var)
        return cur
    stack = []
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == ' ':
            i += 1
            continue
        elif ch == ')':
            stack = simplify(stack)
            stack = stack[:-2] + [stack[-1]]
        elif ch == '+' or ch == '-':
            stack = simplify(stack)
            stack.append(ch)
        elif ch == '*' or ch == '/':
            stack.append(ch)
        elif ch == '(':
            if stack and type(stack[-1]) == type(polynomial([constant(0)],'x')):
                 stack.append('*')
            stack.append(ch)
        elif ch == '^':
            stack.append(ch)
        elif ch.isdigit():
            st = i
            while i+1 < len(s) and s[i+1].isdigit(): i += 1
            n = int(s[st:i+1])
            if stack and stack[-1] == '^':
                stack[-2] = stack[-2].power(n)
                stack.pop()
            elif stack and type(stack[-1]) == type(polynomial([constant(0)],'x')):
                stack.append('*')
                stack.append(constant_with_value(n))
            else:
                stack.append(constant_with_value(n))
        elif ch.isalpha():
            if stack and type(stack[-1]) == type(polynomial([constant(0)],'x')):
                stack.append('*')
            stack.append(poly_from_char(ch))
        else:
            raise Exception('parse not implemented for character {}.'.format(ch))
        i += 1
    stack = simplify(stack)
    return stack[0]

def get_variables(s):
    return (sorted(list(set([ch for ch in s if ch.isalpha()])))[::-1])

'''TESTING'''
if __name__ == '__main__':
    s = '7x + (x+1)(y^2+2y+4)(z-7) + 8xy'
    print(s)
    p = parse(s,['z','y','x'])
    p.PRINT()
    s1 = 'x^2+2x+1'
    s2 = '2xy'
    p1 = parse(s1)
    p2 = parse(s2)
    p3 = p1.add(p2)
    p4 = p1.multiply(p2)
    p1.PRINT()
    p2.PRINT()
    p3.PRINT()
    p4.PRINT()
