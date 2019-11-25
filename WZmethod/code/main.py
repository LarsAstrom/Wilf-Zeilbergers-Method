import parsers
import factor
import gosper
import polynomial
import expressions
import datetime

tex_header = '\\documentclass{article}\n\
\\usepackage[utf8]{inputenc}\n\
\\usepackage{amsmath}\n\
\\let\\oldforall\\forall\n\
\\renewcommand{\\forall}{\\hspace*{2mm}\\oldforall\\hspace*{1mm}}\n\
\\title{Proof}\n\
\\author{Automatic WZ-method prover}\n\
\\date{' + '{}-{}-{}'.format(datetime.date.today().year,datetime.date.today().month,datetime.date.today().day) +\
'}\n\
\\begin{document}\n\
\\maketitle\n'
tex_bottom = '\\end{document}\n'

'''
WZmethod is a method that performs WZ's method. It takes a parser and a string
and returns F,G,R.
parser is a function which takes a string s has to give
    - F = rational polynomial that arises from dividing s by the right hand side
    - ak = (poly_part,rest_part) rest_part has form of B[a,b] for binomial coefficients, F[a] for factorial, P[a,b] for power.
            poly_part is the polynomial part of ak. In general this should be F(n+1,k)/F(n,k)-1.
    - num = numerator of ak/ak-1
    - den = denominator of ak/ak-1
'''
def WZmethod(parser, s, variable='k', max_degree=5):
    F,(ak_poly,ak_rest),num,den = parser(s)
    assert factor.is_polynomial(num) and factor.is_polynomial(den), 'Wrong type num, den'
    p,q,r,f = gosper.gosper(num,den,variable=variable,max_degree=max_degree)
    # p.PRINT()
    # q.PRINT()
    # r.PRINT()
    if f == None: return None
    ak_poly_num,ak_poly_den = ak_poly.num.addends[0].factors[0],ak_poly.den.addends[0].factors[0]
    Snum = ak_poly_num.multiply(f.multiply(polynomial.polynomial_parser(q.to_string().replace(variable,'({}+1)'.format(variable)))))
    Sden = ak_poly_den.multiply(p)
    g = Snum.gcd(Sden)
    Snum = Snum.divide(g)[0]
    Sden = Sden.divide(g)[0]
    Snum1 = polynomial.polynomial_parser(Snum.to_string().replace(variable,'({}-1)'.format(variable)))
    Sden1 = polynomial.polynomial_parser(Sden.to_string().replace(variable,'({}-1)'.format(variable)))
    S = '(({})/({}))({})'.format(Snum.to_string(),Sden.to_string(),ak_rest)
    R = '({})/({})'.format(Snum1.to_string(),Sden1.to_string())
    G = '(({})/({}))({})'.format(Snum1.to_string(),Sden1.to_string(),ak_rest.replace(variable,'({}-1)'.format(variable)))
    # print(s)
    # print()
    # print(F)
    # print()
    # print(G)
    return F,G,R

'''Converts a thing on the form used in program to tex.'''
def to_tex(F):
    F = F.replace('*','\\cdot')
    def get_next_part_end(s,i):
        if s[i+1] == '(':
            j = i+1
            parcount = 1
            while parcount:
                j += 1
                if s[j] == '(': parcount += 1
                elif s[j]==')': parcount -= 1
            return j
        if s[i+1].isdigit():
            j = i+1
            while j < len(s) - 1 and s[j+1].isdigit(): j += 1
            return j
        if s[i+1] in ['B','P','F']:
            return s.find(']',i)
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
        if s[i-1] == '}':
            j = i-5
            while s[j:j+5] != '\\frac': j -= 1
            return j
        if s[i-1].isdigit():
            j = i-1
            while j > 0 and s[j-1].isdigit(): j -= 1
            return j
        return i-1
    i = F.find('/')
    while i != -1:
        j1 = get_prev_part_start(F,i)
        j2 = get_next_part_end(F,i)
        to_replace_with = '\\frac{'+to_tex(F[j1:i])+'}{'+to_tex(F[i+1:j2+1])+'}'
        F = F[:j1] + to_replace_with + F[j2+1:]
        i = j1
        j = i + len(to_replace_with) - 1
        while i > 0 and j < len(F)-1 and F[i-1] == '(' and F[j+1] == ')':
            F = F[:i-1] + F[i:j+1] + F[j+2:]
            i,j = i-1,j-1
        i = F.find('/')
    i = F.find('B[')
    while i != -1:
        j1 = F.find(',',i)
        j2 = F.find(']',i)
        to_replace_with = '\\binom{'+to_tex(F[i+2:j1])+'}{'+to_tex(F[j1+1:j2])+'}'
        F = F[:i] + to_replace_with +F[j2+1:]
        j = i + len(to_replace_with) - 1
        while i > 0 and j < len(F)-1 and F[i-1] == '(' and F[j+1] == ')':
            F = F[:i-1] + F[i:j+1] + F[j+2:]
            i,j = i-1,j-1
        i = F.find('B[')
    i = F.find('F[')
    while i != -1:
        j = F.find(']',i)
        to_replace_with = '({})!'.format(to_tex(F[i+2:j]))
        F = F[:i] + to_replace_with +F[j+1:]
        j = i + len(to_replace_with) - 1
        while i > 0 and j < len(F)-1 and F[i-1] == '(' and F[j+1] == ')':
            F = F[:i-1] + F[i:j+1] + F[j+2:]
            i,j = i-1,j-1
        i = F.find('F[')
    i = F.find('P[')
    while i != -1:
        j1 = F.find(',',i)
        j2 = F.find(']',i)
        use_paran = j1-(i+2) > 1
        to_replace_with = '{}{}{}^'.format('(' if use_paran else '',to_tex(F[i+2:j1]),')' if use_paran else '') + '{' + to_tex(F[j1+1:j2]) + '}'
        F = F[:i] + to_replace_with +F[j2+1:]
        j = i + len(to_replace_with) - 1
        while i > 0 and j < len(F)-1 and F[i-1] == '(' and F[j+1] == ')':
            F = F[:i-1] + F[i:j+1] + F[j+2:]
            i,j = i-1,j-1
        i = F.find('B[')
    while F and F[0] == '(' and get_opposite_paran(F,0) == len(F)-1:
        F = F[1:-1]
    return F

def get_opposite_paran(s,i):
    par = 1
    for j in range(i+1,len(s)):
        if s[j] == '(': par += 1
        if s[j] == ')': par -= 1
        if par == 0: return j

'''Checks that F(n+1,k)-F(n,k)=G(n,k+1)-G(n,k).'''
def check_FG(F,G):
    diff = expressions.expression_parser('(({})-({}))-(({})-({}))'.format(F.replace('n','(n+1)'),F,G.replace('k','(k+1)'),G))
    diff.simplify_complete()
    # diff.PRINT()
    return len(diff.num.addends) == 0 or diff.num.is_zero()

'''Writes a proof of the identity'''
def write_proof(parser,s,variable,max_degree=5):
    out = ['We want to prove that\n\\begin{equation}\\label{Eq: 1}\n' + s + '\n\\end{equation}\nholds. ']
    ans = WZmethod(parser,s,variable=variable,max_degree=max_degree)
    if ans == None:
        out.append('This equation was not possible to solve by the automatic Wilf-Zeilberger method solver.')
        return out
    else:
        F,G,R = ans
    checkfg = check_FG(F,G)
    out.append('By dividing equation \\ref{Eq: 1} by the right hand side we get\n\\begin{equation}\nF(n,k)='+to_tex(F)+'\n\\end{equation}\n')
    out.append('We use proof certificate\n\\begin{equation}\nR(n,k)='+to_tex(R)+',\n\\end{equation}\n')
    out.append('which is the same as using\n\\begin{equation}\nG(n,k)='+to_tex(G)+',\n\\end{equation}\n')
    out.append('the automatic solver has {} verified that\n'.format('' if checkfg else 'NOT'))
    out.append('\\begin{equation}\\label{Eq: WZ1}\nF(n+1,k)-F(n,k)=G(n,k+1)-G(n,k).\n\\end{equation}\n')
    if not checkfg:
        out.append('Therefore the user has to verify that equation \\ref{Eq: WZ1} is fulfilled.')
    out.append('Thereafter user now has to verify that\n\\begin{equation}\n\\lim_{k\\to\\pm\\infty}G(n,k)=0\\forall n.\n\\end{equation}\n')
    out.append('Then we get\n\\begin{equation}\n\\sum_'+variable+' F(n+1,k)-F(n,k)=\\sum_'+variable+' G(n,k+1)-G(n,k)=0\\end{equation}')
    out.append('Lastly equation \\ref{Eq: 1} needs to be verified for some $n$, for instance $n=0$. Thereafter the identity is shown.\n')
    #CONTINUE THIS
    return out

'''This is the main program. Produces a tex-file with the proof.'''
def main(parser,s,variable,outfile='../texs/proofs/proof.tex'):
    f = open(outfile,'w')
    f.write(tex_header)
    for x in write_proof(parser,s,variable):
        f.write(x)
    f.write(tex_bottom)
    f.close()

if __name__ == '__main__':

    s01 = '\\sum \\binom{n}{k} = 2^n'
    s02 = '\\sum (-1)^k\\cdot\\binom{n}{k}\\binom{2k}{k}4^{n-k}=\\binom{2n}{n}'
    s03 = '\\sum \\binom{n}{k}^2 = \\binom{2n}{n}'
    s04 = '\\sum 2^k\\binom{n}{k} = 3^n'
    s05 = '\\sum k\\binom{n}{k} = n2^{n-1}'
    s06 = '\\sum \\frac{1}{k(k-1)} = 1-\\frac{1}{n}'
    s07 = '\\sum \\binom{k}{c} = \\binom{n+1}{c+1}'
    s08 = '\\sum \\binom{r+k}{k} = \\binom{r+n+1}{n}'
    s09 = '\\sum \\binom{m-k}{n-k} = \\binom{m+1}{n}'
    s10 = '\\sum \\frac{1}{\\binom{k}{n}}=\\frac{n}{n-1}'
    s_train = [s01,s02,s03,s04,s05,s06,s07,s08,s09,s10]
    print('TESTING PROGRAM ON TRAINING DATA')
    for i,ss in enumerate(s_train):
        num = str(i+1)
        if len(num) == 1: num = '0'+num
        print('================TEST {} STARTED==============='.format(num))
        main(parsers.latex2equation_parser,ss,'k','../texs/proofs/proof{}.tex'.format(num))
        print('==============================================')

    print('TESTING PROGRAM ON TEST DATA')
    s11 = '\\sum 3^k\\binom{n}{k} = 4^n'
    s12 = '\\sum 4^k\\binom{n}{k} = 5^n'
    s13 = '\\sum \\binom{n}{2k} = 2^{n-1}'
    s14 = '\\sum \\frac{1}{k\\binom{k+n}{k}} = \\frac{1}{n}'
    s15 = '\\sum 2^{-k}\\binom{n+k}{k} = 2^{n+1}'
    s16 = '\\sum \\frac{\\binom{n}{k}}{\\binom{2n-1}{k}} = 2'
    s17 = '\\sum k\\frac{\\binom{n}{k}}{\\binom{2n-1}{k}} = 2\\frac{n}{n+1}'
    s18 = '\\sum (-1)^{k-1}\\frac{k}{\\binom{2n}{k}} = \\frac{n}{n+1}'
    s19 = '\\sum \\binom{2n+1}{k} = 2^{2n}'
    s20 = '\\sum (-1)^k\\binom{n-k}{k}\\frac{2^{2n-2k}}{n-k} = \\frac{2^{n+1}}{n}'
    s_test = [s11,s12,s13,s14,s15,s16,s17,s18,s19,s20]
    for i,ss in enumerate(s_test):
        num = str(i+1+len(s_train))
        if len(num) == 1: num = '0'+num
        print('================TEST {} STARTED==============='.format(num))
        main(parsers.latex2equation_parser,ss,'k','../texs/proofs/test_data/proof{}.tex'.format(num))
        print('==============================================')
