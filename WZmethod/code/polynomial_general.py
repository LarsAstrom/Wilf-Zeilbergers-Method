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
        self.is_constant = True
        self.is_one = (value == 1)

    def convert_polynomial(self,variables):
        return parse(self.to_string(),variables)

    def evaluate(self,variable,value):
        return self.coefficients[0]

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
        if self.variables == other.variables:
            return self.equals_simple(other)
        vars = self.get_common_variables(other)
        return self.convert_polynomial_vars(vars).equals(other.convert_polynomial(vars))
    def equals_simple(self,other):
        assert self.variables == other.variables, 'Trying to check equality polynomials of different variables.'
        return self.coefficients[0] == other.coefficients[0]

    def add(self,other):
        if self.variables == other.variables:
            return self.add_simple(other)
        return self.convert_polynomial(other.variables).add(other)
    def add_simple(self,other):
        assert self.variables == other.variables, 'Trying to add polynomials of different variables.'
        return constant(self.coefficients[0]+other.coefficients[0])

    def multiply(self,other):
        if self.variables == other.variables:
            return self.multiply_simple(other)
        return self.convert_polynomial(other.variables).multiply(other)
    def multiply_simple(self,other):
        assert self.variables == other.variables, 'Trying to multiply polynomials of different variables.'
        return constant(self.coefficients[0]*other.coefficients[0])

    def divide(self,other):
        if self.variables == other.variables:
            return self.divide_simple(other)
        return self.convert_polynomial(other.variables).divide(other)
    def divide_simple(self,other):
        # Returns (q,r,f) such that f*self/other = q + r/other. (f is a constant)
        assert self.variables == other.variables, 'Trying to divide polynomials of different variables.'
        return (constant(self.coefficients[0]//other.coefficients[0]),
                constant(self.coefficients[0]%other.coefficients[0]),
                constant(1))

    def modulo(self,other):
        if self.variables == other.variables:
            return self.modulo_simple(other)
        return self.convert_polynomial(other.variables).modulo(other)
    def modulo_simple(self,other):
        assert self.variables == other.variables, 'Trying to modulo polynomials of different variables.'
        q,r,f = self.divide(other)
        return r

    def gcd(self,other):
        if self.variables == other.variables:
            return self.gcd_simple(other)
        return self.convert_polynomial(other.variables).gcd(other)
    def gcd_simple(self,other):
        assert self.variables == other.variables, 'Trying to gcd polynomials of different variables. {} {}'.format(self.variables,other.variables)
        if other.is_zero: return self
        return other.gcd(self.modulo(other))

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
        self.is_constant = (self.degree==0 and self.coefficients[0].is_constant)
        self.is_one = (self.degree==0 and self.coefficients[0].is_one)

    def get_zeros(self,variable):
        assert variable in self.variables, 'Not possible to find zeros with variable {}, because the variables are {}'.format(variable,self.variables)
        if variable != self.variables[-1]:
            new_variable_list = list(self.variables)
            new_variable_list.remove(variable)
            new_variable_list.append(variable)
            return self.convert_polynomial(new_variable_list).get_zeros(variable)
        if len(self.variables) == 1:
            if self.degree == 0:
                return 'all_values' if self.is_zero else []
            if self.degree == 1:
                a, b  = self.coefficients[1].coefficients[0],\
                        self.coefficients[0].coefficients[0]
                return [b//a] if (b%a==0) else []
            if self.degree == 2:
                a,b,c = self.coefficients[2].coefficients[0],\
                        self.coefficients[1].coefficients[0],\
                        self.coefficients[0].coefficients[0]
                out = []
                if b**2 < 4*a*c: return out
                if (-b+(b**2-4*a*c)**0.5)/(2*a) == int((-b+(b**2-4*a*c)**0.5)/(2*a)):
                    out.append(int((-b+(b**2-4*a*c)**0.5)/(2*a)))
                if (-b-(b**2-4*a*c)**0.5)/(2*a) == int((-b-(b**2-4*a*c)**0.5)/(2*a)):
                    out.append(int((-b-(b**2-4*a*c)**0.5)/(2*a)))
                return out
            out = []
            for value in range(-100,101):
                if self.evaluate(variable,value).is_zero:
                    out.append(value)
            return out if out else 'high_degree'
        i = 0
        while i < self.degree + 1:
            if type(self.coefficients[i].get_zeros(variable)) == list:
                break
            else:
                i += 1
        if i == self.degree + 1:
            L = []
            for value in range(-100,101):
                if self.evaluate(variable,value).is_zero:
                    L.append(value)
            if not L: return 'high_degree'
        else:
            L = self.coefficients[i].get_zeros(variable)
        out = []
        for l in L:
            if self.evaluate(variable,l).is_zero:
                out.append(l)
        return out

    def evaluate(self,variable,value):
        if variable == self.variables[0]:
            out = self.coefficients[0]
            for i in range(1,self.degree+1):
                out = out.add(self.coefficients[i].multiply(constant(value).power(i)))
            return out
        return polynomial([c.evaluate(variable,value) for c in self.coefficients],
                            self.variables[0])

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
        raise Exception('simplify not checked')
        g = self.gcd_list()
        return polynomial([c.divide(g)[0] for c in self.coefficients],self.variables[0])

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
            coeff_string = c.to_string()
            negative = coeff_string[0] == '-'
            if negative: coeff_string = c.negate().to_string()
            if i or negative: out.append('-' if negative else '+')
            out.append('{}{}{}{}{}{}'.format('(' if len(self.variables)>1 else '',
                                    coeff_string if (len(self.variables)>1 or coeff_string!='1' or i==self.degree) else '',
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
        if self.variables == other.variables:
            return self.equals_simple(other)
        vars = self.get_common_variables(other)
        return self.convert_polynomial_vars(vars).equals(other.convert_polynomial(vars))
    def equals_simple(self,other):
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
    '''
    def gcd_simple(self,other):
        #print('GCD\n{}\n{}\n'.format(self.to_string(),other.to_string()))
        if other.is_zero: return self
        q,r,f = self.divide(other)
        if f.is_one: return other.gcd(r)
        return (self.multiply(f)).gcd(other).multiply(self.gcd(f)).divide(other.gcd(f))[0]
    '''
    def gcd_simple(self,other):
        assert self.variables == other.variables, 'Trying to gcd polynomials of different variables.'
        if other.is_zero: return self
        g = other.gcd(self.modulo(other))
        return g.multiply(self.gcd_list().gcd(other.gcd_list())).divide(g.gcd_list())[0]
        #return other.gcd(self.modulo(other))

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
    else:
        for var in get_variables(s):
            assert var in variables, 'Missing variable {} for parsing.'.format(var)
    def simplify(stack):
        if len(stack) == 1: return stack
        if stack[-2] == '(': return stack
        if stack[-1] == '(':
            stack.append(constant_with_value(0))
            return stack
        #print_stack(stack)
        b,op,a = stack.pop(),stack.pop(),stack.pop()
        if a == '(':
            stack.append(a)
            assert op == '-', 'Something is weird.'
            stack.append(b.negate())
            return simplify(stack)
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
    stack = [constant_with_value(0)]
    if s[0] != '-': stack.append('+')
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
    '''
    s = '-7x + (x+1)(y^2+2y+4)(z-7) + 8xy'
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
    print('============================')
    p1 = parse('(2k-n-1)(n+2-k)')
    p2 = parse('k(2k-n+2j-3)')
    p1.PRINT()
    p2.PRINT()
    g = p1.gcd(p2)
    g.PRINT()
    g.evaluate('j',1).PRINT()
    print(g.evaluate('j',1).is_zero)
    print('============================')
    p1 = parse('(2k-n-1)(n+2-k)')
    p2 = parse('(k+j)(2k-n+2j-3)')
    p1.PRINT()
    p2.PRINT()
    g = p1.gcd(p2)
    g.PRINT()
    g.evaluate('j',1).PRINT()
    print(g.evaluate('j',1).is_zero)
    print('============================')
    p1 = parse('0x+0*(x+y)')
    p1.PRINT()
    p1 = parse('x^2y')
    p1.multiply(constant(2)).PRINT()
    p1.multiply(constant(2)).evaluate('x',1).PRINT()
    p1.multiply(constant(2)).evaluate('x',2).PRINT()
    p1.multiply(constant(2)).evaluate('y',2).PRINT()
    print('==============================')
    p1 = parse('x+2')
    p1.PRINT()
    p1.evaluate('x',1).PRINT()
    print(p1.evaluate('x',1).is_zero)
    print('==============================')
    p1 = parse('x^2+2x+1')
    print(p1.get_zeros('x'))
    p2 = parse('2x+6')
    print(p2.get_zeros('x'))
    p3 = parse('3x+4')
    print(p3.get_zeros('x'))
    p4 = parse('0',['x'])
    print(p4.get_zeros('x'))
    p5 = parse('1',['x'])
    print(p5.get_zeros('x'))
    p6 = parse('x^3+1')
    print(p6.get_zeros('x'))
    print('==============================')
    p1 = parse('(x-1)(x-2)(x-3)(y-3)(y-4)(z-5)(z-6)')
    p1.PRINT()
    print(p1.get_zeros('x'))
    print(p1.get_zeros('y'))
    print(p1.get_zeros('z'))
    print('==============================')
    p1 = parse('x-3')
    p2 = parse('x-2')
    p1.gcd(p2).PRINT()
    print(type(p1.gcd(p2)))
    print('==============================')
    p1 = parse('-x^2')
    p1.PRINT()
    print('==============================')
    p1 = parse('(k+1)(2k-n-1)')
    p2 = parse('(2k-n-1)(n+2-k)')
    g1 = p1.gcd(p2)
    g2 = p2.gcd(p1)
    p1.PRINT()
    p2.PRINT()
    g1.PRINT()
    g2.PRINT()
    q,r,f = p2.divide(p1)
    q.PRINT()
    r.PRINT()
    f.PRINT()
    p1.gcd(f).PRINT()
    p2.gcd(p1).multiply(p2.gcd(f)).divide(f.gcd(p1))[0].PRINT()
    print('==============================')
    p1 = parse('(k+1)(n+1)(m+1)')
    p2 = parse('(k+1)(n+1)')
    p1.gcd(p2).PRINT()
    print('==============================')

    p1 = parse('(k+j)(2k+2j-3)')
    p2 = parse('(2k-1)(2-k)')
    a,b,c = p1.divide(p2)
    a.PRINT()
    b.PRINT()
    c.PRINT()
    a,b,c = p2.divide(b)
    a.PRINT()
    b.PRINT()
    c.PRINT()
    #p1.gcd(p2).PRINT()

    a,b,c = p1.divide(p2)
    a.PRINT()
    b.PRINT()
    c.PRINT()
    p3 = p1.multiply(c)
    p3.PRINT()
    p3.gcd(p2).PRINT()
    p1.gcd(c).PRINT()
    p2.gcd(c).PRINT()
    p1.gcd(p2).PRINT()

    p1 = parse('10x^2+10x')
    p2 = parse('6x')
    p1.PRINT()
    p2.PRINT()
    g = p1.gcd(p2)
    g = g.multiply(p1.gcd_list().gcd(p2.gcd_list())).divide(g.gcd_list())[0]
    g.PRINT()
    '''

    p1 = parse('(x+1)(y+1)(z+1)')
    p2 = parse('(z+1)(y+1)')
    p1.PRINT()
    p2.PRINT()
    p1.gcd(p2).PRINT()
