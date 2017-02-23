import click
import pandas as pd
import glob


@click.command()
@click.option('--glob-pattern', type=str, default='*.blast')
def summarize(glob_pattern):
    blast3_header = ['query', 'subject', '%id', 'aln-length', 'mismatches',
                     'gap-openings', 'query-start', 'query-end',
                     'subject-start', 'subject-end', 'e-value', 'bit-score',
                     'cigar', 'coverage', 'ignored_b']

    results = []
    for f in glob.glob(glob_pattern):
        r = pd.read_csv(f, sep='\t', dtype=str, index_col=False)
        r.columns = blast3_header
        results.append(r)
    results = pd.concat(results)

    print("Total queries run: %d" % len(results))
    print("Total not hitting: %d" % ((results['subject'] == "*").sum()))
    print("Fraction not hitting: %0.4f" % ((results['subject'] == "*").sum() / len(results)))

    print("\nSubsequent summaries based off of only those which recruit.")
    results = results[results['subject'] != '*']
    for c in ['%id', 'e-value', 'bit-score', 'coverage']:
        results[c] = results[c].astype(float)
        desc = results[c].describe()
        print("Category: %s" % c)
        print(desc)
        print()


if __name__ == '__main__':
    summarize()
