import parsers
import gosper
import get_f
import polynomial
import datetime

tex_header = '\\documentclass{article}\n\
\\usepackage[utf8]{inputenc}\n\
\\title{Proof}\n\
\\author{Automatic WZ-method prover}\n\
\\date{' + '{}-{}-{}'.format(datetime.date.today().year,datetime.date.today().month,datetime.date.today().day) +\
'}\n\
\\begin{document}\n\
\\maketitle\n'
tex_bottom = '\\end{document}'

def WZmethod(parser, s, quotifier, variable):
    pass

def write_proof(parser,s,quotifier,variable):
    #out = 'We want to prove that\n\\begin{equation}\n{}\n\\end{equation}\nholds.'.format(s)
    return 'Hejsan\n'

def write_tex(parser,s,quotifier,variable,outfile='proof.tex'):
    f = open(outfile,'w')
    f.write(tex_header)
    for x in write_proof(parser,s,quotifier,variable):
        f.write(x)
    f.write(tex_bottom)
    f.close()

if __name__ == '__main__':
    write_tex(None,None,None,None)
