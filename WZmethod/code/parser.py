def get_F(s):
    pass

def get_ak(F):
    return '({})-({})'.format(F.replace('n','(n+1)'),F)

def get_quotient(ak):
    return '({})/({})'.format(ak,ak.replace('k','(k-1)'))

def parser(s):
    F = get_F(s)
    ak = get_ak(F)
    quotient = get_quotient(ak)
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
