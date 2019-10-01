class addend():
    def __init__(self,constant,exponents):
        self.constant = constant
        self.exponents = exponents
        self.num_var = len(exponents)

    def multiply(self,other):
        assert self.num_var == other.num_var, 'Addends need to have same number of variables'
        return addend(self.constant*other.constant,
                [self.exponents[i] + other.exponents[i] for i in range(self.num_var)])

    def divide(self,other):
        assert self.num_var == other.num_var, 'Addends need to have same number of variables'
        return addend(self.constant*other.constant,
                [self.exponents[i] + other.exponents[i] for i in range(self.num_var)])

    def power(self,pow):
        return addend(self.constant**pow,[exp * pow for exp in self.exponents])

    def equals(self,other):
        assert self.num_var == other.num_var, 'Addends need to have same number of variables'
        if self.constant != other.constant: return False
        for i in range(self.num_var):
            if self.exponents[i] != other.exponents[i]: return False
        return True

    def greater(self,other):
        assert self.num_var == other.num_var, 'Addends need to have same number of variables'
        for i in range(self.num_var):
            if self.exponents[i] != other.exponents[i]: return False
        if self.constant < other.constant: return False
        return True

    def multiply_constant(self,constant):
        return addend(self.constant * constant, self.exponents)

    def PRINT(self):
        print('Constant: {}, Exponents: {}'.format(self.constant,self.exponents))

def amgm(ls,rs):
    ls,rs = clean_up(ls,rs)
    _,rs = multiply_equation(ls,rs,1/len(ls))
    print('ls addends:')
    for l in ls: l.PRINT()
    print('rs addends:')
    for r in rs: r.PRINT()
    ls_mult = multiply_addends(ls)
    print('ls_mult')
    ls_mult.PRINT()
    ls_amgm = ls_mult.power(1/len(ls))
    print('ls_amgm')
    ls_amgm.PRINT()
    return ls_amgm.greater(rs[0])

def clean_up(ls,rs):
    LS = []
    for x in ls:
        torem = None
        for y in rs:
            if x.equals(y):
                torem = y
        if torem != None:
            rs.remove(y)
        else:
            LS.append(x)
    return LS,rs

def multiply_addends(addends):
    out = addends[0]
    for x in addends[1:]:
        out = out.multiply(x)
    return out

def multiply_equation(ls,rs,fac):
    ls_out = [lso.multiply_constant(fac) for lso in ls]
    rs_out = [rso.multiply_constant(fac) for rso in rs]
    return ls_out,rs_out

def main():
    ls = [addend(1,[2,0]),addend(1,[0,2])]
    rs = [addend(2,[1,1])]
    print(amgm(ls,rs))

if __name__ == '__main__':
    main()
