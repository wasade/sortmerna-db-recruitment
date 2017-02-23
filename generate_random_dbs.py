import numpy as np
import click


@click.command()
@click.option('--fasta', type=click.Path(exists=True), required=True)
@click.option('--iterations', type=int, default=10)
@click.option('--holdout-fraction', type=float, default=0.2)
@click.option('--output-basename', type=str, required=True)
def random_subsets(fasta, iterations, holdout_fraction, output_basename):
    outputs = {i: open("%s-%d.fasta" % (output_basename, i), 'w')
               for i in range(iterations)}

    fraction_to_keep = (1 - holdout_fraction)
    with open(fasta) as fp:
        # horribly assumes seqs are on a single line
        ids = iter(fp)
        seqs = iter(fp)

        while True:
            try:
                id_ = next(ids)
            except StopIteration:
                break
            seq = next(seqs)

            rands = np.random.uniform(0, 1, iterations) < fraction_to_keep
            for idx in rands.nonzero()[0]:
                outputs[idx].write("%s%s" % (id_, seq))

    for v in outputs.values():
        v.close()


if __name__ == '__main__':
    random_subsets()
