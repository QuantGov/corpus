import datetime
from pathlib import Path

# Note: snakemake and Python 3.6 f-strings use similar "{bracket syntax}" to 
# inject variables into strings. Be cognizant of the presence of 'f' before some
# strings in this file.

TODAY = str(datetime.date.today())
VERBOSITY = '-v' # Set to empty for less info or to -q for quiet

#### UPDATE TIMESTAMP ##########################################################
## This section performs a "touch" on "driver.py", updating the timestamp on
## that file so that snakemake is aware of your most recent run. 

rule update_timestamp:
	input:
		"driver.py"
	shell:
		"touch {input}"

#### ANALYSIS ##################################################################
## This section handles analysis, which by default includes generating a
## wordcount, a restriction count, and a metadata that combines the two. Your
## project may have different aims and thus may employ different scripts.

rule create_wordcount:
	input:
		"driver.py"
	output:
		"wordcount.csv"
	shell:
		"python scripts/count_words.py {input} -o {output} {VERBOSITY}"

rule create_restrictions:
	input:
		"driver.py"
	output:
		"restrictions.csv"
	shell:
		"python scripts/count_restrictions.py {input} -o {output} {VERBOSITY}"

rule create_metadata:
    input:
        "wordcount.csv",
        "restrictions.csv"
    output:
        "metadata.csv"
    shell:
        "python scripts/combine_datasets.py {input} -o {output} {VERBOSITY}"
