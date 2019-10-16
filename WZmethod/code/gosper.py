from polynomial_general import *
import sys
sys.setrecursionlimit(10**6)

def gosper(num,den,variable):
    q,r = num,den
    p = polynomial([constant(1)],'n')
    zero = get_common_factor(q,r,variable)
    while zero != None:
        g = q.gcd(parse(r.to_string().replace(variable,'({}+{})'.format(variable,zero))))
        q = q.divide(g)[0]
        r = r.divide(parse(g.to_string().replace(variable,'({}-{})'.format(variable,zero))))[0]
        for i in range(zero):
            p = p.multiply(parse(g.to_string().replace(variable,'({}-{})'.format(variable,i))))
        zero = get_common_factor(q,r,variable)
    return q,r,p

def get_common_factor(q,r,variable):
    rj = parse(r.to_string().replace(variable,'({}+j)'.format(variable)))
    #Want to find j such that gcd between q and rj is not 1.
    return find_zeros(q,rj)

def find_zeros(q,rj):
    if rj.is_zero: return None
    zeros = rj.get_zeros('j')
    if zeros and max(zeros) >= 0: return max(zeros)
    return find_zeros(rj,q.modulo(rj))

def test_gosper(num,den,variable='k'):
    if num == '' or den == '':
        print('==============================')
        print('Testing Gosper does not work for numerator and denominator\n{}\n{}'.format(num,den))
        print('==============================')
        return
    print('======TESTING GOSPER======')
    p1,p2 = parse(num),parse(den)
    print(num)
    print(den)
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

def test_get_common_factor(s1,s2):
    print(get_common_factor(parse(s1),parse(s2),'k'))

if __name__ == '__main__':
    #01#$\sum_{k=0}^n \binom{n}{k} = 2^n$
    s01 = '(2k-n-1)(n+2-k)'
    s02 = 'k(2k-n-3)'
    #02#$\sum_{k=0}^n (-1)^k\binom{n}{k}\binom{2k}{k}4^{n-k}=\binom{2n}{n}$
    s03 = '-(2k-1)(2nk+n+k+1)(n+2-k)'
    s04 = '2k^2(2nk-n+k)'
    #03#$\sum_{k=0}^n \binom{n}{k}^2 = \binom{2n}{n}$
    s05 = '(n+2-k)^2((n+1)^3-2(n+1-k)^2(2n+1))'
    s06 = 'k^2((n+1)^3-2(n+2-k)^2(2n+1))'
    #04#$\sum_{k=-n}^n (-1)^k\binom{2n}{n+k}^3 = \frac{(3n)!}{n!}$
    s07 = ''
    s08 = ''
    #05#$\sum_{k=0}^n 2^k\binom{n}{k} = 3^n$
    s09 = '2(3k-2n-2)(n+2-k)'
    s10 = 'k(3k-2n-5)'
    #06#$\sum_{k=0}^n k\binom{n}{k} = n2^{n-1}$
    s11 = '(n+2-k)(2k-n-2)'
    s12 = '(k-1)(2k-n-4)'
    #07#$\sum_{k=1}^n \frac{1}{k(k-1)} = 1-\frac{1}{n}$
    s13 = 'k-1'
    s14 = 'k+1'
    #08#$\sum_{k=0}^n \binom{k}{c} = \binom{n+1}{c+1}$
    s15 = 'k'
    s16 = 'k-c'
    #09#$\sum_{k=0}^n \binom{r+k}{k} = \binom{r+n+1}{n}$
    s17 = 'r+k'
    s18 = 'k'
    #10#$\sum_{k=0}^n \binom{m-k}{n-k} = \binom{m+1}{n}$
    s19 = '(kn+1-km-k-n)(n+2-k)'
    s20 = '(kn+2+m-km-k-2n)(m+1-k)'
    #11$\sum_{k=0}^n \binom{n}{k}c^k = (c+1)^n$
    s21 = '(k+kc-nc-c)(n+2-k)'
    s22 = 'k(k-1+kc-nc-2c)'

    '''
    What are these?!?!?!
    s3 = '(n+2-k)^2((n+1)^3-2(n+1-k)^2(2n+1))'
    s4 = 'k^2((n+1)^3-2(n+2-k)^2(2n+1))'
    '''
    tests = [(s01,s02),(s03,s04),(s05,s06),(s07,s08),(s09,s10),\
            (s11,s12),(s13,s14),(s15,s16),(s17,s18),(s19,s20),(s21,s22)]

    for test in tests:
        try:
            test_get_common_factor(*test)
        except:
            print('==============================')
            print(test[0])
            print(test[1])
            print('DOES NOT WORK GET COMMON FACTOR')
            print('==============================')

    for test in tests:
        try:
            test_gosper(*test)
        except:
            print('==============================')
            print(test[0])
            print(test[1])
            print('DOES NOT WORK GOSPER')
            print('==============================')

    exit()
    test_gosper(s1,s2)
    #test_gosper(s3,s4)
    test_gosper(s5,s6)
    test_gosper(s7,s8)
