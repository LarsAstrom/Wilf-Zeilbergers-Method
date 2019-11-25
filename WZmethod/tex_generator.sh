if $# != 1
then
  echo "Number of arguments has to be 1."
  exit 1
else
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
  rm texs/*.thm
  rm texs/*.toc
  rm texs/*.out
  rm texs/*.aux
  rm texs/*.log
  rm texs/*.bcf
  rm texs/*.xml
  rm texs/*.fls
  rm texs/*.bbl
  rm texs/*.blg
  rm texs/*.dvi
  rm texs/*latexmk
  latexmk -pdf -shell-escape "texs/"$add_string$1".tex"
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
  rm texs/*.thm
  rm texs/*.toc
  rm texs/*.out
  rm texs/*.aux
  rm texs/*.log
  rm texs/*.bcf
  rm texs/*.xml
  rm texs/*.fls
  rm texs/*.bbl
  rm texs/*.blg
  rm texs/*.dvi
  rm texs/*latexmk
  open $1".pdf"
fi
