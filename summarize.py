import click
import pandas as pd
import glob
import matplotlib.pyplot as plt
from collections import Counter


@click.command()
@click.option('--trim', type=int, default=None)
@click.option('--taxonomy', type=click.Path(exists=True), required=True)
def summarize(trim, taxonomy):
    if trim is None:
        trim = "*"
    glob_pattern = "*.%s-*blast" % str(trim)

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

    taxonomy = pd.read_csv(taxonomy, sep='\t', names=['GGID', 'Lineage'], dtype=str)
    taxonomy.set_index('GGID', inplace=True)

    print("Total queries run: %d" % len(results))
    print("Total not hitting: %d" % ((results['subject'] == "*").sum()))
    print("Fraction not hitting: %0.4f" % ((results['subject'] == "*").sum() / len(results)))

    mishits = results[results['subject'] == '*']
    total_counts = results['query'].value_counts()
    mishit_counts = mishits['query'].value_counts()
    mishit_counts.sort(ascending=False)
    print("Mishit summary: ")
    print("  QUERY(n=MISHIT-COUNT; m=TIMES-AS-QUERY): LINEAGE")

    for query, count in zip(mishit_counts.index, mishit_counts.values):
        print('  %s(n=%d; m=%d): %s' % (query, count, total_counts.loc[query],
                                        taxonomy.loc[query].Lineage))

    print("\nSubsequent summaries based off of only those which recruit.")
    results = results[results['subject'] != '*']
    for c in ['%id', 'e-value', 'bit-score', 'coverage']:
        results[c] = results[c].astype(float)
        desc = results[c].describe()
        print("Category: %s" % c)
        print(desc)
        print()

        plt.figure()
        plt.hist(results[c].values, bins=100)
        ax = plt.gca()
        ax.set_yscale('log')
        plt.savefig("%s-%s.png" % (trim if trim != '*' else 'all', c))


if __name__ == '__main__':
    summarize()
