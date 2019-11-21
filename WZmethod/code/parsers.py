import factor
import expressions
import polynomial

'''Parses an expression on latex format'''
def parse_rel_part(s):
    def get_next_part_end(s,i):
        if s[i+1] == '{':
            j = i+1
            parcount = 1
            while parcount:
                j += 1
                if s[j] == '{': parcount += 1
                elif s[j]=='}': parcount -= 1
            return j
        if s[i+1].isdigit():
            j = i+1
            while j < len(s) - 1 and s[j+1].isdigit(): j += 1
            return j
        return i+1
    def get_prev_part_start(s,i):
        if s[i-1] == ']':
            j = i-1
            while s[j] != '[': j -= 1
            return j-1
        if s[i-1] == ')':
            j = i-1
            parcount = -1
            while parcount:
                j -= 1
                if s[j] == '(': parcount += 1
                elif s[j]==')': parcount -= 1
            return j
        if s[i-1].isdigit():
            j = i-1
            while j > 0 and s[j-1].isdigit(): j -= 1
            return j
        return i-1
    # print(s)
    i = s.find('\\binom')
    while i != -1:
        i0 = s.find('{',i)
        i1 = s.find('}',i0)
        i2 = s.find('{',i1)
        i3 = s.find('}',i2)
        s = s[:i] + 'B[{},{}]'.format(parse_rel_part(s[i0+1:i1]),
                    parse_rel_part(s[i2+1:i3])) + s[i3+1:]
        i = s.find('\\binom')
    i = s.find('\\frac')
    # print(s)
    while i != -1:
        i0 = s.find('{',i)
        i1 = s.find('}',i0)
        i2 = s.find('{',i1)
        i3 = s.find('}',i2)
        s = s[:i] + '({})/({})'.format(parse_rel_part(s[i0+1:i1]),
                    parse_rel_part(s[i2+1:i3])) + s[i3+1:]
        i = s.find('\\frac')
    i = s.find('!')
    # print(s)
    while i != -1:
        j = get_prev_part_start(s,i)
        s = s[:j] + 'F[{}]'.format(s[j:i]) + s[i+1:]
        i = s.find('!')
    # print(s)
    i = s.find('^')
    while i != -1:
        j2 = get_next_part_end(s,i)
        if all(ch.isdigit() for ch in s[i+1:j2+1]):
            j1 = get_prev_part_start(s,i)
            s = s[:j1] + s[j1:i]*int(s[i+1:j2+1]) + s[j2+1:]
        else:
            j1 = get_prev_part_start(s,i)
            if j2 == i+1:
                s = s[:j1] + 'P[{},{}]'.format(polynomial.polynomial_parser(s[j1:i]).to_string(),
                                    s[i+1:j2+1]) + s[j2+1:]
            else:
                s = s[:j1] + 'P[{},{}]'.format(polynomial.polynomial_parser(s[j1:i]).to_string(),
                                    s[i+2:j2]) + s[j2+1:]
        i = s.find('^')
    # print(s)
    return s

'''Gets A from a latex identity'''
def get_A(s):
    part = s.split('=')[0]
    part.replace(' ','')
    return parse_rel_part(part)

'''Gets B from a latex identity'''
def get_B(s):
    part = s.split('=')[1]
    part.replace(' ','')
    return parse_rel_part(part)

'''Gets F from a latex identity'''
def get_F(s):
    s = s.replace(' ','')
    assert s[:4] == '\\sum', 'Weird string {}'.format(s)
    s = s[4:]
    if s[0] == '_':
        if s[1] == '{':
            i = 2
            while s[i] != '}': i += 1
            s = s[i+1:]
        else:
            s = s[2:]
        if s[0] == '^':
            if s[1] == '{':
                i = 2
                while s[i] != '}': i += 1
                s = s[i+1:]
            else:
                s = s[2:]
    return '({})/({})'.format(get_A(s),get_B(s))

'''Gets ak from F'''
def get_ak(F):
    return '({})-({})'.format(F.replace('n','(n+1)'),F)

'''Gets a quotient string from ak'''
def get_quotient_string(ak):
    return '({})/({})'.format(ak,ak.replace('k','(k-1)'))

'''Assumes something on the form \\sum{k=a(n)}^b(n) A(n,k) = B(n)'''
def latex2equation_parser(s):
    F = get_F(s)
    ak = get_ak(F)
    ak_poly_part = expressions.expression_parser('({})/({})-1'.format(F.replace('n','(n+1)'),F))
    ak_poly_part.simplify_complete()
    ak_rest_part = F
    quotient_string = get_quotient_string(ak)
    quotient = expressions.expression_parser(quotient_string)
    quotient.simplify_complete()
    assert type(quotient) == expressions.expression_rat, \
            'Quotient type has to be expression_rat, not {}'.format(type(quotient))
    assert len(quotient.num.addends) == 1 and len(quotient.den.addends) == 1, \
            'Numerator and denominator has to have length 1, not {}, {}'.\
            format(len(quotient.num.addends),len(quotient.den.addends))
    assert len(quotient.num.addends[0].factors) == 1 and len(quotient.den.addends[0].factors) == 1,\
            'Numerator and denominator factors have to have length 1, not {}, {}'.\
            format(len(quotient.num.addends[0].factors),len(quotient.den.addends[0].factors))
    assert factor.is_polynomial(quotient.num.addends[0].factors[0]) and \
            factor.is_polynomial(quotient.den.addends[0].factors[0]), \
            'type of numerator and denominator has to be polynomial, not {} {}'.\
            format(type(quotient.num.addends[0].factors[0]),type(quotient.den.addends[0].factors[0]))
    return F,(ak_poly_part,ak_rest_part),quotient.num.addends[0].factors[0],quotient.den.addends[0].factors[0]

if __name__ == '__main__':
    print(parse_rel_part('\\frac{n+k}{k}\\binom{n}{k}k!(n^2)4^k(n+2)!12^n'))
    s01 = '\\sum_{k=0}^n \\binom{n}{k} = 2^n'
    s02 = '\\sum_{k=0}^n (-1)^k\\binom{n}{k}\\binom{2k}{k}4^{n-k}=\\binom{2n}{n}'
    s03 = '\\sum_{k=0}^n \\binom{n}{k}^2 = \\binom{2n}{n}'
    s04 = '\\sum_{k=-n}^n (-1)^k\\binom{2n}{n+k}^3 = \\frac{(3n)!}{n!}'
    s05 = '\\sum_{k=0}^n 2^k\\binom{n}{k} = 3^n'
    s06 = '\\sum_{k=0}^n k\\binom{n}{k} = n2^{n-1}'
    s07 = '\\sum_{k=1}^n \\frac{1}{k(k-1)} = 1-\\frac{1}{n}'
    s08 = '\\sum_{k=0}^n \\binom{k}{c} = \\binom{n+1}{c+1}'
    s09 = '\\sum_{k=0}^n \\binom{r+k}{k} = \\binom{r+n+1}{n}'
    s10 = '\\sum_{k=0}^n \\binom{m-k}{n-k} = \\binom{m+1}{n}'
    s11 = '\\sum_{k=n}^{\\infty} \\frac{1}{\\binom{k}{n}}=\\frac{n}{n-1}'
    s = [s01,s02,s03,s05,s06,s07,s08,s09,s10,s11]#,s04]
    for i,ss in enumerate(s):
        print('TEST {}'.format(i+1))
        print(ss)
        F,(ak_p,ak_r),num,den = latex2equation_parser(ss)
        print(F)
        ak_p.PRINT()
        print(ak_r)
        num.PRINT()
        den.PRINT()
        print('=====================================')
