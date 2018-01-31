from pathlib import Path

def outpath(path):
    """Ensure Cross-Platform functionality for files in subdirectories"""
    return os.path.sep.join(os.path.split(path))


#### CORPUS DRIVER #############################################################
## This section updates the corpus's time stamp every time the clean
## folder is re-created. This is appropriate when the clean folder is deleted
## and re-created every time it changes.

rule prepare_corpus:
    input: 'driver.py', 'data/clean'
    output: touch('timestamp')

#### ANALYSIS ##################################################################
## This section handles analysis, which by default includes generating a
## wordcount, a restriction count, and a metadata that combines the two. Your
## project may have different aims and thus may employ different scripts or 
## commands.

rule create_wordcount:
    input: 'timestamp'
    output: outpath('data/wordcount.csv')
    shell: 'quantgov corpus count_words {input} -o {output}'

rule create_restriction_count:
    input: 'timestamp'
    output: outpath('data/restrictions.csv')
    shell: 'quantgov corpus count_occurrences {input} shall must "may not" required prohibited -o {output}'

rule create_metadata:
    input:
        rules.create_wordcount.output,
        rules.create_restriction_count.output
    output:
        outpath('data/metadata.csv')
    run:
        import pandas as pd
        df = pd.read_csv(input[0])
        for i in input[1:]:
            df = df.merge(pd.read_csv(i), how='left')
        df.to_csv(output[0], index=False)
