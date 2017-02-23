import click
import pandas as pd
import glob
import matplotlib.pyplot as plt


@click.command()
@click.option('--trim', type=int, default=None)
def summarize(trim):
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

        plt.figure()
        plt.hist(results[c].values, bins=100)
        ax = plt.gca()
        ax.set_yscale('log')
        plt.savefig("%s-%s.png" % (trim if trim != '*' else 'all', c))


if __name__ == '__main__':
    summarize()
