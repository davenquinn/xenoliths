function prepare-crossref {
  sed -r "s/\[((@(fig|eq|sec|tbl):\w+;? ?)*)\]/\\\[\1\\\]/g" \
  | sed "s/\(@(fig|tbl):\(\w\+\)\)|/\1‌/g"
}

bibfile="source/references.bib"
