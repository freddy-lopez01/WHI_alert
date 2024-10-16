## Exporting conda environment into a environment.yml file
conda env export | grep -v "^prefix: " > environment.yml

