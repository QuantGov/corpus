# The QuantGov Corpus

## Official QuantGov Corpora

This repository is for those who would like to create new datasets using the QuantGov platform. If you would like to find data that has been produced using the QuantGov platform, please visit http://www.quantgov.org/data.

This repository contains all official QuantGov corpora, with each corpus stored in its own branch.

## The Generic Corpus

The `master` branch of this repository is the Generic Corpus, which serves all files in the data/clean folder, with the file path as the index. Scripts for wordcount and regulatory restriction count are included; however, only the wordcount is included in the data/metadata.csv by default. See the `makefile` for more details.

## Using this Corpus

To use or modify this corpus, clone it using git or download the archive from the [QuantGov Site](http://www.quantgov.org/platform) and unzip it on your computer.

## Requirements

Using this corpus requires Python >= 3.5 and the `make` utility. 

If you are using the Anaconda Python distribution (recommended), navigate to the corpus folder and use the command `conda install --file conda-requirements.txt`, then the command `pip install -r requirements.txt`. If you are on windows, also use the command `conda install --file conda-requirements-windows.txt`, which will install the `make` utility. 

If you are not using Anaconda, use the command `pip install requirements.txt`. You must ensure that `make` is install separately.

