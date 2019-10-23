if $# != 1
then
  echo "Number of arguments has to be 1."
  exit 1
else
  latexmk -pdf "texs/"$add_string$1".tex"
  rm *.thm
  rm *.toc
  rm *.out
  rm *.aux
  rm *.log
  rm *.bcf
  rm *.xml
  rm *.fls
  rm *.bbl
  rm *.blg
  rm *.dvi
  rm *latexmk
  open $1".pdf"
fi
