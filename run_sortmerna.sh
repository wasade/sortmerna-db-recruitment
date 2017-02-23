set -e

threads=$1

for q in *.queries
do
    qbase=$(basename ${q} .queries)
    for f in *.fasta
    do
        fbase=$(basename ${f} .fasta)
        sortmerna --reads ${q} --ref ${f},${fbase}.idx --aligned ${qbase}-${fbase} --blast 3 --best 1 --print_all_reads -v -a ${threads}
    done
done
