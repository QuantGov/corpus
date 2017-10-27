from pathlib import Path

# Note: snakemake and Python 3.6 f-strings use similar '{bracket syntax}' to 
# inject variables into strings. Be cognizant of the presence of 'f' before some
# strings in this file.

rule all:
    input: 'data/metadata.csv'


#### UPDATE TIMESTAMP ##########################################################
## This section performs a 'touch' on 'driver.py', updating the timestamp on
## that file so that snakemake is aware of your most recent run. 

rule update_timestamp:
    input: 'data/clean'
    output: 'driver.py'
    run:
        Path(output[0]).touch()

#### ANALYSIS ##################################################################
## This section handles analysis, which by default includes generating a
## wordcount, a restriction count, and a metadata that combines the two. Your
## project may have different aims and thus may employ different scripts or 
## commands.

rule create_wordcount:
    input: 'driver.py'
    output: 'data/wordcount.csv'
    shell: 'quantgov corpus count_words {input} -o {output}'

rule create_restrictions:
    input: 'driver.py'
    output: 'data/restrictions.csv'
    shell: 'quantgov corpus count_occurrences {input} shall must "may not" required prohibited -o {output}'

rule create_metadata:
    input:
        'data/wordcount.csv',
        'data/restrictions.csv'
    output:
        'data/metadata.csv'
    run:
        import pandas as pd
        df = pd.read_csv(input[0])
        for i in input[1:]:
            df = df.merge(pd.read_csv(i), how='left')
        df.to_csv(output[0], index=False)
