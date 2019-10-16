from collections import defaultdict
from polynomial_general import *
from gosper import *

def polynomial2dict(p):
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
    print(s)
    return parse(s)


if __name__ == '__main__':
    p1 = parse('x^2+x+1')
    print(polynomial2dict(p1))
    p1 = parse('-xy-y^2-x^2')
    d1,v1 = polynomial2dict(p1)
    p2 = dict2polynomial(d1,v1)
    p1.PRINT()
    p2.PRINT()
    print(p1.equals(p2))
