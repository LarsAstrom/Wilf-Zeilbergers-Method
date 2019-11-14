import factor
import expressions
import polynomial

def get_A(s):
    pass

def get_B(s):
    pass

def get_F(s):
    return '({})/({})'.format(get_A(s),get_B(s))

def get_ak(F):
    return '({})-({})'.format(F.replace('n','(n+1)'),F)

def get_quotient(ak):
    return '({})/({})'.format(ak,ak.replace('k','(k-1)'))

#Assumes something on the form \sum{k=a(n)}^b(n) A(n,k) = B(n)
def latex2equation_parser(s):
    raise Exception('NOT DONE IMPLEMENTED')
    F = get_F(s)
    ak = get_ak(F)
    quotient_string = get_quotient(ak)
    quotient = expressions.get_quotient(quotient_string)
    assert type(quotient) == expression_rat, 'Quotient type has to be expression_rat, not {}'.format(type(quotient))
    assert len(quotient.num.addends) == 1 and len(quotient.den.addends) == 1,\
            'Numerator and denominator has to have length 1, not {}, {}'.\
            format(len(quotient.num.addends),len(quotient.den.addends))
    assert len(quotient.num.addends[0].factors) == 1 and len(quotient.den.addends[0].factors) == 1,\
            'Numerator and denominator factors have to have length 1, not {}, {}'.\
            format(len(quotient.num.addends[0].factors),len(quotient.den.addends[0].factors))
    assert type(quotient.num.addends[0].factors[0]) in [constant,polynomial] and \
            type(quotient.den.addends[0].factors[0]) in [constant,polynomial],\
            'type of numerator and denominator has to be polynomial, not {} {}'.\
            format(type(quotient.num.addends[0].factors[0]),type(quotient.den.addends[0].factors[0]))
    return ak,quotient.num.addends[0].factors[0],quotient.den.addends[0].factors[0]
