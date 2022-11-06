#!/bin/bash

pandoc readme.src.md -o readme.ipynb
jupyter nbconvert readme.ipynb --execute --to markdown
rm readme.ipynb
pandoc -s --toc --metadata title="Pattern Cutting Python Library" readme.md --css style.css --css https://gist.githubusercontent.com/dashed/6714393/raw/ae966d9d0806eb1e24462d88082a0264438adc50/github-pandoc.css -o readme.html


# shhh, dont look at this
if [ "$(uname)" == "Darwin" ]; then
  open readme.html -g
fi
