if $# != 1
then
  echo "Number of arguments has to be 1."
  exit 1
else
  pdflatex "texs/"$1".tex"
  rm *.out
  rm *.aux
  rm *.log
  rm *.bcf
  rm *.xml
  open $1".pdf"
fi
