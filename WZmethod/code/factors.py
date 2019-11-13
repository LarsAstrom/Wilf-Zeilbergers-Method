from polynomial import *
from gosper import *
from get_f import *
def fac(n):
    return n*fac(n-1) if n else 1

def is_polynomial(x):
    return type(x) in [constant,polynomial]

def is_factorial(x):
    return type(x) == factorial

def is_power(x):
    return type(x) == power

def is_factor(x):
    return (is_polynomial(x) or is_factorial(x) or is_power(x))

class factorial:
    def __init__(self,value):
        self.value = value
        assert is_polynomial(self.value), 'Value has to be polynomial, not {}'.format(type(self.value))

    def divide(self,other):
        if is_positive_constant(self.value.subtract(other.value)):
            out = polynomial([constant(1)],self.value.variables[0])
            to_mult = other.value
            while not to_mult.equals(self.value):
                to_mult = to_mult.add(to_mult.get_constant(1))
                out = out.multiply(to_mult)
            return out,constant(1)
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

class power:
    def __init__(self,base,exponent):
        self.base = base
        self.exponent = parse(exponent.to_string())
        assert type(self.base) == int, 'Base has to be int, not {}'.format(type(self.base))
        assert is_polynomial(self.exponent), 'Exponent has to be polynomial, not {}'.format(type(self.exponent))

    def inverse(self):
        return power(self.base,self.exponent.negate())

    def multiply(self,other):
        if self.base == other.base:
            exp = self.exponent.add(other.exponent)
            if is_positive_constant(exp):
                return constant(pow(self.base,parse(exp.to_string()).coefficients[0]))
            return power(self.base,exp)
        elif self.exponent.equals(other.exponent):
            return power(self.base*other.base,self.exponent)
        return None

    def divide(self,other):
        return self.multiply(other.inverse())

    def is_divisible(self,other):
        return self.divide(other) != None

    def to_string(self):
        return '{}^({})'.format(self.base,self.exponent.to_string())

    def PRINT(self):
        print(self.to_string())

class expression_mult:
    def __init__(self,factors):
        self.factors = factors
        assert type(self.factors) == list, 'Factors need to be a list, not {}'.format(type(self.factors))
        for factor in self.factors:
            assert is_factor(factor), 'Factor cannot be {}'.format(type(factor))
        self.simplify()

    ''' Collect all terms '''
    def simplify(self):
        facs = []
        include_1 = True
        for f in self.factors:
            if not (is_polynomial(f) and f.equals(constant(1))):
                include_1 = False
        for f in self.factors:
            if is_factorial(f):
                facs.append(f)
                continue
            if is_polynomial(f) and f.equals(constant(1)) and (not include_1):
                continue
            done = False
            for i in range(len(facs)):
                if is_polynomial(f) and is_polynomial(facs[i]):
                    facs[i] = facs[i].multiply(f)
                    done = True
                    break
                if is_power(f) and is_power(facs[i]):
                    if facs[i].multiply(f) != None:
                        facs[i] = facs[i].multiply(f)
                        done = True
                        break
            if not done: facs.append(f)
        self.factors = facs

    def is_polynomial(self):
        self.simplify()
        return len(self.factors) == 1 and is_polynomial(self.factors[0])

    def negate(self):
        return expression_mult(self.factors+[constant(-1)])

    def multiply(self,other):
        return expression_mult(self.factors+other.factors)

    # Returns f such that f is a factor of factor and divides self.
    def is_divisible(self,factor):
        left,out = factor,[]
        factors = list(self.factors)
        change = True
        while change:
            change = False
            for i in range(len(factors)):
                d = try_divide(factors[i],left)
                if d == None: continue
                if type(d) != constant and not (type(d) == polynomial and d.equals(parse('1'))):
                    changed = True
                    if is_polynomial(factors[i]) or is_factorial(factors[i]):
                        factors[i] = factors[i].divide(d)[0]
                    else:
                        factors[i] = factors[i].divide(d)
                    if is_polynomial(left) or is_factorial(left):
                        left = left.divide(d)[0]
                    else:
                        left = left.divide(d)
                    out.append(d)
        return out

    # Requires self is divisible by other.
    def divide(self,other):
        left = other
        factors = list(self.factors)
        while not (is_polynomial(left) and left.equals(constant(1))):
            for i in range(len(factors)):
                d = try_divide(factors[i],left)
                if d == None: continue
                if type(d) != constant and not (type(d) == polynomial and d.equals(parse('1'))):
                    if type(factors[i]) in [polynomial,factorial]:
                        factors[i] = factors[i].divide(d)[0]
                    else:
                        factors[i] = factors[i].divide(d)
                    if type(left) in [polynomial,factorial]:
                        left = left.divide(d)[0]
                    else:
                        left = left.divide(d)
        return expression_mult(factors)

    def to_string(self):
        out = ['(']
        for i,x in enumerate(self.factors):
            out.append('{}({})'.format('*' if i else '',x.to_string()))
        out.append(')')
        return ''.join(out)

    def PRINT(self):
        print(self.to_string())

class expression_add:
    def __init__(self,addends):
        self.addends = addends
        assert type(self.addends) == list, 'Addends need to be a list, not {}'.format(type(self.addends))
        for addend in self.addends:
            assert type(addend) == expression_mult,\
                    'Addends need to be expression_mult, not {}'.format(type(addend))
        self.simplify()

    ''' Collect all terms '''
    def simplify(self):
        addends = []
        polynomial_id = None
        for addend in self.addends:
            if addend.is_polynomial():
                if polynomial_id != None:
                    addends[polynomial_id] = expression_mult([addends[polynomial_id].factors[0]\
                                                                .add(addend.factors[0])])
                else:
                    polynomial_id = len(addends)
                    addends.append(addend)
            else:
                addends.append(addend)
        self.addends = addends

    def negate(self):
        return expression_add([addend.negate() for addend in self.addends])

    def add(self,other):
        return expression_add(self.addends+other.addends)

    def subtract(self,other):
        return self.add(other.negate())

    def multiply(self,other):
        addends = []
        for addend1 in self.addends:
            for addend2 in other.addends:
                addends.append(addend1.multiply(addend2))
        return expression_add(addends)

    def to_string(self):
        out = ['(']
        for i,x in enumerate(self.addends):
            if i:
                out.append(' + ')
            out.append(x.to_string())
        out.append(')')
        return ''.join(out)

    def PRINT(self):
        print(self.to_string())

class expression_rat:
    def __init__(self,num,den):
        self.num = num
        self.den = den
        assert type(self.num) == expression_add,\
                'Numerator needs to be expression_add, not {}'.format(type(self.num))
        assert type(self.den) == expression_add,\
                'Denominator needs to be expression_add, not {}'.format(type(self.den))
        self.simplify()

    def simplify(self):
        # self.PRINT()
        self.num.simplify()
        self.den.simplify()
        candidates = [factor for factor in self.den.addends[0].factors]
        for expr_m in self.num.addends:
            candidates2 = []
            for cand in candidates:
                new_cands = expr_m.is_divisible(cand)
                for new_cand in new_cands:
                    if (not is_polynomial(new_cand)) or (not new_cand.equals(constant(1))):
                        candidates2.append(new_cand)
            candidates = candidates2
        for expr_m in self.den.addends:
            candidates2 = []
            for cand in candidates:
                new_cands = expr_m.is_divisible(cand)
                for new_cand in new_cands:
                    if (not is_polynomial(new_cand)) or (not new_cand.equals(constant(1))):
                        candidates2.append(new_cand)
            candidates = candidates2
        if not candidates: return
        d = candidates[0]
        # print('PRINTING DIVISOR')
        # d.PRINT()
        # print('=====================================')
        for i in range(len(self.num.addends)):
            self.num.addends[i] = self.num.addends[i].divide(d)
        for i in range(len(self.den.addends)):
            self.den.addends[i] = self.den.addends[i].divide(d)
        self.simplify()

    def negate(self):
        return expression_rat(self.num.negate(),self.den)

    def add(self,other):
        num = self.num.multiply(other.den).add(self.den.multiply(other.num))
        den = self.den.multiply(other.den)
        return expression_rat(num,den)

    def subtract(self,other):
        return self.add(other.negate())

    def multiply(self,other):
        return expression_rat(self.num.multiply(other.num),\
                            self.den.multiply(other.den))

    def divide(self,other):
        return self.multiply(expression_rat(other.den,other.num))

    def to_string(self):
        num_string,den_string = self.num.to_string(),self.den.to_string()
        min_len,max_len = min(len(num_string),len(den_string)),\
                            max(len(num_string),len(den_string))
        while len(num_string) < max_len: num_string = ' ' + num_string + ' '
        while len(den_string) < max_len: den_string = ' ' + den_string + ' '
        return '\nPRINTING RATIONAL EXPRESSION\n{}\n{}\n{}\nPRINTING RATIONAL EXPRESSION\n'.\
                                format(num_string,
                                '-'*max(len(num_string),len(den_string)),
                                den_string)

    def PRINT(self):
        print(self.to_string())

# Returns f such that f divides a and b.
# (f is the largest factor of b that divides a.)
def try_divide(a,b):
    if type(a) != type(b):
        return None
    if type(a) == polynomial:
        return a.gcd(b)
    if type(a) == factorial:
        if is_positive_constant(a.value.subtract(b.value)):
            return b
        elif is_positive_constant(b.value.subtract(a.value)):
            return a
        return constant(1)
    if type(a) == power:
        if a.divide(b) != None:
            return b
        return constant(1)

# Returns True if polynomial p is a constant, that is positive, otherwise False.
def is_positive_constant(p):
    c = parse(p.to_string())
    return type(c) == constant and c.coefficients[0] >= 0

def binom(n,k):
    if type(n) == str: n = parse(n)
    if type(k) == str: k = parse(k)
    num = expression_add([expression_mult([factorial(n)])])
    den = expression_add([expression_mult([factorial(k),factorial(parse('{}-({})'.format(n.to_string(),k.to_string())))])])
    return expression_rat(num,den)

def to_expr_r(x):
    if type(x) == expression_rat:
        return x
    if is_factor(x):
        num = expression_add([expression_mult([x])])
    if type(x) == expression_mult:
        num = expression_add([x])
    if type(x) == expression_add:
        num = x
    den = expression_add([expression_mult([constant(1)])])
    return expression_rat(num,den)

def parse_general(s):
    def simplify(stack):
        if len(stack) == 1: return stack
        if stack[-2] == '(': return stack
        if stack[-1] == '(':
            stack.append(to_expr_r(constant(0)))
            return stack
        b,op,a = stack.pop(),stack.pop(),stack.pop()
        if a == '(':
            stack.append(a)
            assert op == '-', 'Something is weird'
            stack.append(b.negate())
            return simplify(stack)
        if op == '+':
            stack.append(a.add(b))
        elif op == '-':
            stack.append(a.subtract(b))
        elif op == '*':
            stack.append(a.multiply(b))
        elif op == '/':
            stack.append(a.divide(b))
        else:
            print('SOMETHING IS GOING WRONG')
            print('TRYING TO SIMPLIFY AND HAVE a, op, b AS')
            try:
                print(type(a))
                a.PRINT()
            except:
                print(a)
            try:
                print(type(op))
                op.PRINT()
            except:
                print(op)
            try:
                print(type(b))
                b.PRINT()
            except:
                print(b)
            raise Exception('Parse general error')
        return simplify(stack)

    to_split = ['B[','F[','P[',']',',','/','*','+','-','(',')']
    s = s.replace(' ','')
    for x in to_split:
        s = s.replace(x,' {} '.format(x))
    parts = s.split()
    #print(list(zip(parts,list(range(0,len(parts))))))
    stack = []
    i = 0
    while i < len(parts):
        #print(i)
        part = parts[i]
        if len(part) == 0:
            i += 1
            continue
        assert part != ',' and part != ']', 'Parse general error for string {}'.format(s)
        if part == '(':
            if stack and type(stack[-1]) == expression_rat:
                stack.append('*')
            stack.append('(')
            i += 1
        elif part == ')':
            stack = simplify(stack)
            stack = stack[:-2] + stack[-1:]
            i += 1
        #DONE TO HERE.
        elif part == 'B[':
            if stack and type(stack[-1]) == expression_rat:
                stack.append('*')
            j = i+1
            while parts[j] != ',': j += 1
            n = parse(''.join(parts[i+1:j]))
            i = j
            j = i+1
            while parts[j] != ']': j += 1
            k = parse(''.join(parts[i+1:j]))
            stack.append(to_expr_r(binom(n,k)))
            i = j+1
        elif part == 'F[':
            if stack and type(stack[-1]) == expression_rat:
                stack.append('*')
            j = i+1
            while parts[j] != ']': j += 1
            stack.append(to_expr_r(factorial(parse(''.join(parts[i+1:j])))))
            i = j+1
        elif part == 'P[':
            if stack and type(stack[-1]) == expression_rat:
                stack.append('*')
            j = i+1
            while parts[j] != ',': j += 1
            a = int(''.join(parts[i+1:j]))
            i = j
            j = i+1
            while parts[j] != ']': j += 1
            n = parse(''.join(parts[i+1:j]))
            stack.append(to_expr_r(power(a,n)))
            i = j+1
        elif part in ['/','*']:
            stack.append(part)
            i += 1
        elif part in ['+','-']:
            stack = simplify(stack)
            stack.append(part)
            i += 1
        else:
            if stack and type(stack[-1]) == expression_rat:
                stack.append('*')
            stack.append(to_expr_r(parse(part)))
            i += 1
    # print('\n'*10 + 'PARSE DONE' + '\n'*10)
    # print(len(stack))
    # for x in stack:
    #     try: x.PRINT()
    #     except: print(x)
    # print('\n'*10 + 'PARSE DONE' + '\n'*10)
    stack = simplify(stack)
    return stack[0]

def get_quotient(fnk):
    num_string = '({})-({})'.format(fnk.replace('n','(n+1)'),fnk)
    den_string = num_string.replace('k','(k-1)')
    quot_string = '({})/({})'.format(num_string,den_string)
    print(quot_string)
    return parse_general(quot_string)

if __name__ == '__main__':
    '''
    p1 = parse('mn+k^2')
    f1 = factorial(parse('n'))
    p2 = parse('m^2n^2+k')
    f2 = factorial(parse('n+m'))
    em1 = expression_mult([p1,f1])
    em2 = expression_mult([p1,f2])
    em3 = expression_mult([p2,f1])
    em4 = expression_mult([p2,f2])
    ea1 = expression_add([em1,em2])
    ea2 = expression_add([em3,em4])
    er1 = expression_rat(ea1,ea2)
    p1.PRINT()
    f1.PRINT()
    p2.PRINT()
    f2.PRINT()
    em1.PRINT()
    em2.PRINT()
    em3.PRINT()
    em4.PRINT()
    ea1.PRINT()
    ea2.PRINT()
    er1.PRINT()
    #WRITE TESTCASES.

    f1 = factorial(parse('n+2'))
    f2 = factorial(parse('n'))
    n,d = f1.divide(f2)
    n.PRINT()
    d.PRINT()
    p1 = power(2,parse('n'))
    p2 = power(2,parse('m'))
    p3 = power(3,parse('n'))
    p4 = p1.multiply(p2)
    p5 = p1.multiply(p3)
    p1.PRINT()
    p2.PRINT()
    p3.PRINT()
    p4.PRINT()
    p5.PRINT()
    c1 = constant(1)
    p1 = parse('n+m+1')
    c1.add(p1).PRINT()
    p1.add(c1).PRINT()

    f1 = factorial(parse('n'))
    f2 = factorial(parse('n+2'))
    n,d = f1.divide(f2)
    f1.PRINT()
    f2.PRINT()
    n.PRINT()
    d.PRINT()
    n,d = f2.divide(f1)
    n.PRINT()
    d.PRINT()
    print(factorial(parse('n')).divide(factorial(parse('m'))))
    f1 = factorial(parse('n'))
    f2 = factorial(parse('n+2'))
    try_divide(f1,f2).PRINT()
    try_divide(f2,f1).PRINT()
    p1,_ = f2.divide(f1)
    p2,_ = f2.divide(factorial(parse('n+1')))
    p1.PRINT()
    p2.PRINT()
    try_divide(p1,p2).PRINT()
    try_divide(p2,p1).PRINT()
    po1 = power(2,parse('n'))
    po2 = power(2,parse('2n'))
    po3 = power(3,parse('n'))
    try_divide(po1,po2).PRINT()
    try_divide(po1,po3).PRINT()
    L = [parse('n^2+2n+1'),parse('n^2+3n+2')]
    L2 = list(L)
    L2[0] = L2[0].divide(parse('n+1'))[0]
    print('L')
    for l in L: l.PRINT()
    print('L2')
    for l in L2: l.PRINT()

    em1 = expression_mult([factorial(parse('n')),parse('n^2+3n+2')])
    f1 = factorial(parse('n+2'))
    em1.PRINT()
    f1.PRINT()
    em1.is_divisible(f1).PRINT()

    em1 = expression_mult([parse('(n+1)(n+2)'),parse('(n+2)(n+3)'),parse('(n+4)(n+5)')])
    p1 = parse('(n+1)(n+3)')
    p2 = parse('(n+3)^2')
    #em1.is_divisible(p1).PRINT()
    #em1.is_divisible(p2).PRINT()

    em1 = expression_mult([factorial(parse('(n-1)')),parse('(n+2)(n+3)'),parse('(n+4)(n+5)')])
    f1 = factorial(parse('n'))
    L = em1.is_divisible(f1)
    print(len(L))
    for l in L: l.PRINT()

    f1 = factorial(parse('n-k+1'))
    f2 = factorial(parse('n-k'))
    n,d = f1.divide(f2)
    n.PRINT()
    d.PRINT()


    nck = binom('n','k')
    nck.PRINT()
    nck1 = binom('n','k-1')
    nck1.PRINT()
    print('\n\n\n\n\n\n\n\n\n\n')
    nck.divide(nck1).PRINT()
    nck1.divide(nck).PRINT()

    em = expression_mult([factorial(parse('n')),factorial(parse('n-k+1'))])
    d = em.is_divisible(factorial(parse('n-k')))
    print(len(d))
    for dd in d: dd.PRINT()

    d = try_divide(factorial(parse('n-k+1')),factorial(parse('n-k')))
    d.PRINT()

    p1 = parse('n-k+1')
    p1.PRINT()

    print('TESTING TESTING TESTING')
    b1 = binom('n+1','k')
    b2 = binom('n','k')
    b3 = binom('n+1','k-1')
    b4 = binom('n','k-1')
    p1 = to_expr_r(power(2,parse('n+1')))
    p2 = to_expr_r(power(2,parse('n')))
    t1 = b1.divide(p1)
    t2 = b2.divide(p2)
    t3 = b3.divide(p1)
    t4 = b4.divide(p2)
    t1.PRINT()
    t2.PRINT()
    t3.PRINT()
    t4.PRINT()
    print('\n\n\n\n\n\n\n\n\n\n')
    ak = t1.subtract(t2)
    ak.PRINT()
    #exit()
    out = t1.subtract(t2).divide(t3.subtract(t4))
    out.PRINT()

    q,r,p = gosper(out.num.addends[0].factors[0],out.den.addends[0].factors[0],'k')
    f = get_f(p,q,r)
    p.PRINT()
    q.PRINT()
    r.PRINT()
    f.PRINT()
    ak.PRINT()


    num = expression_add([expression_mult([factorial(parse('n+1')),power(2,parse('n'))]),
                            expression_mult([parse('-n+k-1'),factorial(parse('n')),power(2,parse('n+1'))])])
    for em in num.addends:
        d = em.divide(power(2,parse('2n+1')))
        d.PRINT()

    a = parse_general('B[n,k](n^2+kn)/(B[n,k-1](n+kn^2))')
    a.PRINT()
    a = parse_general('(B[n,k]n)/B[n,k-1]')
    a.PRINT()
    a = parse_general('(B[n,k]n)')
    a.PRINT()
    a = parse_general('(n)')
    a.PRINT()
    '''


    s1 = 'B[n,k]/P[2,n]'
    s2 = '(P[-1,k]B[n,k]B[2k,k]P[4,n-k])/B[2n,n]'
    s3 = '(B[n,k]B[n,k])/B[2n,n]'
    s4 = '(P[-1,k]B[2n,n+k])/(F[3n]/F[n])'
    s5 = '(P[2,k]B[n,k])/P[3,n]'
    s6 = '(kB[n,k])/(nP[2,n-1])'
    s7 = '(1/(k(k-1)))/(1-1/n)'
    s8 = 'B[k,c]/B[n+1,c+1]'
    s9 = 'B[r+k,k]/B[r+n+1,n]'
    s10= 'B[m-k,n-k]/B[m+1,n]'
    s11= 'B[n,k]P[3,k]/P[4,n]'
    s12= 'B[n,k]P[4,k]/P[5,n]'

    s = [s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12]
    # s = [s2]
    for i,ss in enumerate(s):
        print('TEST {}'.format(i+1))
        print(ss)
        q = get_quotient(ss)
        q.PRINT()
        print('=============================================\n\n\n\n\n')
