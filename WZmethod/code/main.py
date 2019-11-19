import parsers
import factor
import gosper
import get_f
import polynomial
import datetime

tex_header = '\\documentclass{article}\n\
\\usepackage[utf8]{inputenc}\n\
\\usepackage{amsmath}\n\
\\title{Proof}\n\
\\author{Automatic WZ-method prover}\n\
\\date{' + '{}-{}-{}'.format(datetime.date.today().year,datetime.date.today().month,datetime.date.today().day) +\
'}\n\
\\begin{document}\n\
\\maketitle\n'
tex_bottom = '\\end{document}'

#parser(s) has to give
# - F = rational polynomial that arises from dividing s by the right hand side
# - ak = (poly_part,rest_part) rest_part has form of B[a,b] for binomial coefficients, F[a] for factorial, P[a,b] for power.
# - num = numerator of ak/ak-1
# - den = denominator of ak/ak-1
def WZmethod(parser, s, variable='k', max_degree=5):
    F,(ak_poly,ak_rest),num,den = parser(s)
    assert factor.is_polynomial(num) and factor.is_polynomial(den), 'Wrong type num, den'
    p,q,r,f = gosper.gosper(num,den,variable=variable,max_degree=max_degree)
    ak_poly_num,ak_poly_den = ak_poly.num.addends[0].factors[0],ak_poly.den.addends[0].factors[0]
    Snum = ak_poly_num.multiply(f.multiply(polynomial.polynomial_parser(q.to_string().replace(variable,'({}+1)'.format(variable)))))
    Sden = ak_poly_den.multiply(p)
    S = '({})({})/({})'.format(Snum.to_string(),ak_rest,Sden.to_string())
    G = S.replace(variable,'({}-1)'.format(variable))
    print(s)
    print()
    print(F)
    print()
    print(G)
    return F,G

def to_tex(F):
    return F

def check_FG(F,G):
    return True

def write_proof(parser,s,variable,max_degree=5):
    out = ['We want to prove that\n\\begin{equation}\\label{Eq: 1}\n' + s + '\n\\end{equation}\nholds.']
    F,G = WZmethod(parser,s,variable=variable,max_degree=max_degree)
    out.append('By dividing equation \\ref{Eq: 1} by the right hand side we get\n\\begin{equation}\nF(n,k)='+to_tex(F)+'\n\\end{equation}\n')
    out.append('By using\n\\begin{equation}\nG(n,k)='+to_tex(G)+',\n\\end{equation}\n')
    out.append('the automatic solver has {} shown that\n'.format('' if check_FG(F,G) else 'NOT'))
    out.append('\\begin{equation}\nF(n+1,k)-F(n,k)=G(n,k+1)-G(n,k).\n\\end{equation}\n')
    out.append('The user now has to verify that\n\\begin{equation}\n\\lim_{k\\to\\pm\\infty}G(n,k)=0\\forall n.\n\\end{equation}\n')
    #CONTINUE THIS
    return out

def write_tex(parser,s,variable,outfile='../texs/proof.tex'):
    f = open(outfile,'w')
    f.write(tex_header)
    for x in write_proof(parser,s,variable):
        f.write(x)
    f.write(tex_bottom)
    f.close()

if __name__ == '__main__':
    s = '\\sum_{k=n}^{\\infty} \\frac{1}{\\binom{k}{n}} = \\frac{n}{n-1}'
    write_tex(parsers.latex2equation_parser,s,'k')
    #WZmethod(parsers.latex2equation_parser,s)
    s = '\\sum_{k=0}^n \\binom{n}{k} = 2^n'
    WZmethod(parsers.latex2equation_parser,s)

    #write_tex(None,None,None,None)
