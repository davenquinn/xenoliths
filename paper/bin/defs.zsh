function prepare-crossref {
  sed -r "s/\[((@(fig|eq|sec|tab):\w+;? ?)*)\]/\\\[\1\\\]/g" \
  | sed "s/\(@fig:\(\w\+\)\)|/\1‌/g"
}

bibfile="source/references.bib"
