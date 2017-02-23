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
    mishit_counts.sort_values(ascending=False)
    print("Mishit summary: ")
    print("  QUERY(n=MISHIT-COUNT; m=TIMES-AS-QUERY): LINEAGE")

    for query, count in zip(mishit_counts.index, mishit_counts.values):
        print('  %s(n=%d; m=%d): %s' % (query, count, total_counts.loc[query],
                                        taxonomy.loc[query].Lineage))

    print("\nSubsequent summaries based off of only those which recruit.")
    hitresults = results[results['subject'] != '*']
    for c in ['%id', 'e-value', 'bit-score', 'coverage']:
        hitresults[c] = hitresults[c].astype(float)
        desc = hitresults[c].describe()
        print("Category: %s" % c)
        print(desc)
        print()

        plt.figure()
        plt.hist(hitresults[c].values, bins=100)
        ax = plt.gca()
        ax.set_yscale('log')
        plt.savefig("%s-%s.png" % (trim if trim != '*' else 'all', c))

    lowcov = hitresults['coverage'] < 50
    lowcov_queries = hitresults[lowcov].copy()
    lowcov_queries.sort_values('coverage', inplace=True)

    # my pandas is showwing. the sort wasn't being maintained from what i
    # could tell with the groupby
    details = []
    for id_, grp in lowcov_queries.groupby('query'):
        details.append((grp['coverage'].mean(), (id_, grp['coverage'].mean(),
                                                len(grp),
                                                total_counts.loc[id_],
                                                taxonomy.loc[id_].Lineage)))

    print("Total below 50%% coverage: %d" % sum(lowcov))
    print("Fraction below 50%% coverage: %0.4f" % (sum(lowcov) / len(lowcov)))
    print("Lineage information:")
    print("  QUERY(cov=MEAN-COVERAGE; n=BELOW-COVERAGE; m=TIMES-AS-QUERY): LINEAGE")
    for _, detail in sorted(details):
        print("  %s(cov=%d; n=%d; m=%d): %s" % detail)


if __name__ == '__main__':
    summarize()
