bash clean.sh
if [ "$#" != "1" ];
then
  if [ "$#" != "2" ];
  then
    echo "Number of arguments has to be 1."
    exit 1
  else
    latexmk -pdf -shell-escape $2"/"$1".tex"
    open $1".pdf"
  fi
else
  latexmk -pdf -shell-escape "texs/"$1".tex"
  open $1".pdf"
fi
bash clean.sh
