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

def fac(n):
    return n*fac(n-1) if n else 1

def n_choose_k(n,k):
    return fac(n)//(fac(k)*fac(n-k))

def get_B(p,L,variables):
    pd,_ = polynomial2dict(p,variables)
    V = len(variables)
    out = []
    for i in range(L**V):
        cur = []
        for j in range(V):
            cur.append((i//(L**j))%L)
        out.append(pd[tuple(cur)])
    return out

def get_A(q,r,L,l,variables):
    qd,_ = polynomial2dict(parse(q.to_string().replace('k','(k+1)')),variables)
    rd,_ = polynomial2dict(r,variables)
    kvar_index = variables.index('k')
    V = len(variables)
    A = [[0]*(l**V) for _ in range(L**V)]
    #Adding to A due to factor q_{k+1}f_k.
    for row in range(L**V):
        i = [(row//L**s)%L for s in range(V)]
        for col in range(l**V):
            j = [(col//l**s)%l for s in range(V)]
            jq = [i[s]-j[s] for s in range(V)]
            A[row][col] += qd[tuple(jq)]
    #Filling in A due to factor r_k f_{k-1}.
    for row in range(L**V):
        i = [(row//L**s)%L for s in range(V)]
        for col in range(l**V):
            j = [(col//l**s)%l for s in range(V)]
            jr = [i[s]-j[s] for s in range(V)]
            a = j[kvar_index]
            for s in range(a,l):
                A[row][col+(s-a)*l**kvar_index] -= rd[tuple(jr)]*pow(-1,s-a)*n_choose_k(s,a)
    return A

def to_polynomial(x,l,variables):
    out = []
    V = len(variables)
    for i in range(l**V):
        if x[i] == 0: continue
        out2 = ['(',x[i]]
        for j in range(V):
            a = (i//(l**j)) % l
            out2.append('{}{}{}'.format(variables[j] if a > 0 else '',
                                        '^' if a > 1 else '',
                                        a if a > 1 else ''))
        out2.append(')')
        out.append(''.join(map(str,out2)))
    return parse('+'.join(out))

def get_degree(p):
    if type(p) == type(constant(0)): return 0
    return max(p.degree,max(get_degree(c) for c in p.coefficients))

#Takes p(k),q(k),r(k) as inputs. Returns f(k)
#such that p(k)=q(k+1)f(k)-r(k)f(k-1)
#max_degree is the maximal degree in any variable for f.
def get_f(p,q,r,max_degree=5):
    l = max_degree + 1
    L = l + max(get_degree(q),get_degree(r))
    assert L >= get_degree(p)+1, 'Does not work to get f because to low degree: {}'.format(max_degree)
    B = get_B(p,L,variables)
    A = get_A(q,r,L,l,variables)
    x = gauss(A,B)
    return to_polynomial(x,l,variables)

if __name__ == '__main__':
    p1 = parse('1+xy+xy^2+x^2+y')
    x = [1,0,1,1,1,0,0,1,0]
    p2 = to_polynomial(x,3,['x','y'])
    p1.PRINT()
    p2.PRINT()
    print(p1.equals(p2))
    print(get_B(p1,4,['x','y']))
    p1 = parse('1+k+k^2+ky+k^2y')
    A = get_A(p1,p1,4,3,['k','y'])
    for a in A: print('\t'.join(map(str,a)))
    print('=====================================')
    p = parse('2k-n-1')
    q = parse('n+2-k')
    r = parse('k')
    A = get_A(q,r,3,2,['k','n'])
    for a in A: print('\t'.join(map(str,a)))
    print('-------------------')
    print(get_B(p,3,['k','n']))
    print('=====================================')
    p = parse('(n+1)^3-2(n+1-k)^2(2n+1)')
    q = parse('(n+2-k)^2')
    r = parse('k^2')
    A = get_A(q,r,4,2,['k','n'])
    for a in A: print('\t'.join(map(str,a)))
    print('-------------------')
    print(get_B(p,4,['k','n']))
    B2 = []
    x = [-1,2,-3,0]
    for i in range(16):
        B2.append(sum([A[i][j]*x[j] for j in range(4)]))
    print(B2)

    print('TESTING GET DEGREE')
    print(get_degree(parse('x^2+y+x^3y+x')))
    print(get_degree(parse('y^2+x+y^3x+y')))
    print(get_degree(parse('a^4b^3c^2d')))
    print(get_degree(parse('e^4b^3c^2d')))
