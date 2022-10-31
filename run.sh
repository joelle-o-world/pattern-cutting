pandoc readme.src.md -o readme.ipynb
jupyter nbconvert readme.ipynb --execute --to markdown 
rm readme.ipynb
pandoc readme.md -o readme.html
open readme.html
