from collections import defaultdict
from polynomial_general import *
from gosper import *

def polynomial2dict(p,variables=None):
    if variables != None:
        d,v = polynomial2dict(p)
        for var in v:
            assert var in variables, 'Not possible to convert {} to variables {} because {} is missing'.format(p,variables,var)
        d2 = defaultdict(int)
        for x in d:
            k = [0]*len(variables)
            for var in v:
                k[variables.index(var)] = x[v.index(var)]
            d2[tuple(k)] = d[x]
        return d2,variables

    assert type(p) == type(polynomial([constant(0)],'x')), 'Cannot convert {} to dict'.format(p)
    if type(p.coefficients[0]) == type(constant(0)):
        d = defaultdict(int)
        for i in range(p.degree+1):
            c = p.coefficients[i]
            if not c.is_zero: d[(i,)] = c.coefficients[0]
        return d,p.variables
    d = defaultdict(int)
    for i in range(p.degree+1):
        d2 = polynomial2dict(p.coefficients[i])[0]
        for x in d2:
            d[tuple([i]+list(x))] = d2[x]
    return d,p.variables

def dict2polynomial(d,v):
    out = []
    for x in d:
        if d[x] == 0: continue
        out2 = ['(',d[x]]
        for i in range(len(v)):
            out2.append('{}{}{}'.format(v[i] if x[i] > 0 else '',
                                        '^' if x[i] > 1 else '',
                                        x[i] if x[i] > 1 else ''))
        out2.append(')')
        out.append(''.join(map(str,out2)))
    s = '+'.join(out)
    return parse(s)

def get_B(p,L,variables):
    pass

def get_A(q,r,L,l,variables):
    pass

def to_polynomial(x,L,variables):
    pass

#Takes p(k),q(k),r(k) as inputs. Returns f(k)
#such that p(k)=q(k+1)f(k)-r(k)f(k-1)
#max_degree is the maximal degree in any variable for f.
def get_f(p,q,r,max_degree=5):
    B = get_B(p,L,variables)
    A = get_A(q,r,L,l,variables)
    x = gauss(A,B)
    return to_polynomial(x,L,variables)

if __name__ == '__main__':
    p1 = parse('x^2+x+1')
    print(polynomial2dict(p1))
    p1 = parse('-xy-y^2-x^2')
    d1,v1 = polynomial2dict(p1,['k','x','y'])
    print(d1,v1)
    p2 = dict2polynomial(d1,v1)
    p1.PRINT()
    p2.PRINT()
    print(p1.equals(p2))
