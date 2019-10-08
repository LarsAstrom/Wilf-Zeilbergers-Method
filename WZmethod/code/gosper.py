from polynomial_general import *

def gosper(num,den,variable):
    q,r = num,den
    p = polynomial([constant(1)],'n')
    rj = parse(r.to_string().replace(variable,'({}+j)'.format(variable)))
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
        print('MAX',MAX)
        print(r.to_string().replace(variable,'({}+{})'.format(variable,MAX)))
        parse(r.to_string().replace(variable,'({}+{})'.format(variable,MAX))).PRINT()
        g = q.gcd(parse(r.to_string().replace(variable,'({}+{})'.format(variable,MAX))))
        g.PRINT()
        q = q.divide(g)[0]
        r = r.divide(parse(g.to_string().replace(variable,'({}-{})'.format(variable,MAX))))[0]
        q.PRINT()
        r.PRINT()
        for i in range(MAX):
            p.PRINT()
            parse(g.to_string().replace(variable,'({}-{})'.format(variable,i))).PRINT()
            p = p.multiply(parse(g.to_string().replace(variable,'({}-{})'.format(variable,i))))
        rj = parse(r.to_string().replace(variable,'({}+j)'.format(variable)))
    return q,r,p

if __name__ == '__main__':
    p1 = parse('(2k-n-1)(n+2-k)')
    p2 = parse('k(2k-n-3)')
    p1.PRINT()
    p2.PRINT()
    print('---------GOSPER STARTED---------')
    q,r,p = gosper(p1,p2,'k')
    print('----------GOSPER ENDED----------')
    q.PRINT()
    r.PRINT()
    p.PRINT()
