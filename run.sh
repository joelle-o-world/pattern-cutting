pandoc readme.md -o notebook.ipynb
jupyter nbconvert notebook.ipynb --execute --to notebook --inplace
jupyter notebook notebook.ipynb
