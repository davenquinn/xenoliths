function prepare-crossref {
  sed -r "s/\[((@(fig|eq|sec|tbl):[A-Za-z0-9_\|]+;? ?)*)\]/\\\[\1\\\]/g" \
  | sed -r "s/(@(fig|tbl):\w+)\|/\1‌/g" \
  | sed -r "s/@sec:model_supplement/Supplementary Materials/g"
}

bibfile="source/references.bib"
