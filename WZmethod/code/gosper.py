from polynomial_general import *
import sys
sys.setrecursionlimit(10**6)

def gosper(num,den,variable):
    q,r = num,den
    p = polynomial([constant(1)],'n')
    rj = parse(r.to_string().replace(variable,'({}+j)'.format(variable)))
    q.gcd(rj).PRINT()
    while not q.gcd(rj).is_constant:
        g = q.gcd(rj)
        zeros = g.get_zeros('j')
        if type(zeros) == str:
            break
        if not zeros:
            break
        MAX = max(zeros)
        if MAX < 0:
            break
        rmax = parse(r.to_string().replace(variable,'({}+{})'.format(variable,MAX)))
        if not q.divide(rmax)[1].is_zero:
            break
        g = q.gcd(rmax).divide(q.divide(rmax)[2])[0]
        q = q.divide(g)[0]
        r = r.divide(parse(g.to_string().replace(variable,'({}-{})'.format(variable,MAX))))[0]
        for i in range(MAX):
            p = p.multiply(parse(g.to_string().replace(variable,'({}-{})'.format(variable,i))))
        rj = parse(r.to_string().replace(variable,'({}+j)'.format(variable)))
    return q,r,p

def test_gosper(num,den,variable='k'):
    print('======TESTING GOSPER======')
    p1,p2 = parse(num),parse(den)
    print('Numerator: {}'.format(p1.to_string()))
    print('Denominator: {}'.format(p2.to_string()))
    q,r,p = gosper(p1,p2,variable)
    print('Now we have:')
    print('q =',q.to_string())
    print('r =',r.to_string())
    print('p =',p.to_string())
    print('such that p(n)*q(n)/(p(n-1)*r(n))')
    print('==========================')
    print()

def print_break():
    print('========================================')

if __name__ == '__main__':
    '''
    s7 = '2(3k-2n-2)(n+2-k)'
    s8 = 'k(3k-2n-5)'
    test_gosper(s7,s8)

    s5 = 'k-1'
    s6 = 'k+1'
    test_gosper(s5,s6)
    '''
    s1 = '(2k-n-1)(n+2-k)'
    s2 = 'k(2k-n-3)'
    p1 = parse(s1)
    p2 = parse(s2)
    p3 = parse(s2.replace('k','(k+1)'))
    p4 = parse(s2.replace('k','(k+j)'))
    p1.PRINT()
    p2.PRINT()
    p3.PRINT()
    p4.PRINT()
    p1.gcd(p2).PRINT()
    p1.gcd(p3).PRINT()
    p1.gcd(p4).PRINT()
    p2.gcd(p3).PRINT()
    p2.gcd(p4).PRINT()
    p3.gcd(p4).PRINT()
    print_break()
    a,b,c = p1.divide(p4)
    a.PRINT()
    b.PRINT()
    c.PRINT()
    print_break()
    a,b,c = p4.divide(b)
    a.PRINT()
    b.PRINT()
    c.PRINT()
    test_gosper(s1,s2)
    '''
    s3 = '(n+2-k)^2((n+1)^3-2(n+1-k)(2n+1))'
    s4 = 'k^2((n+1)^3-2(n+2-k)^2(2n+1))'
    #test_gosper(s3,s4)

    p1, p2 = parse(s3), parse(s4)
    p3 = parse(s4.replace('k','(k+j)'))
    p1.PRINT()
    p3.PRINT()
    print_break()
    a,b,c = p1.divide(p3)
    a.PRINT()
    b.PRINT()
    c.PRINT()
    print_break()
    p3.PRINT()
    b.PRINT()
    print_break()
    a,b,c = p3.divide(b)
    a.PRINT()
    b.PRINT()
    c.PRINT()
    '''
