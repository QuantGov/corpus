VERBOSE_FLAG=-v # Set to empty for less info or to -q for quiet

# Canned recipe for running python scripts. The script should be the first
# dependency, and the other dependencies should be positional arguments in
# order. The script should allow you to specify the output file with a -o flag,
# and to specify verbosity with a -v flag. If you're using a Python script that
# doesn't follow this pattern, you can of course write the recipe directly.
# Additional explicit arguments can be added after the canned recipe if needed.

define py
python $^ -o $@ $(VERBOSE_FLAG)
endef

# List all the csv files you want as part of the metadata here
METADATA = data/wordcount.csv

data/metadata.csv: scripts/combine_datasets.py $(METADATA)
	$(py)

data/wordcount.csv: scripts/count_words.py driver.py
	$(py)

data/restrictions.csv: scripts/count_restrictions.py driver.py
	$(py)

driver.py: data/clean
	touch $@
