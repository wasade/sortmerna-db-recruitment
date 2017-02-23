set -e

threads=$1

for q in *.queries
do
    qbase=$(basename ${q} .queries)
    grep "^>" ${q} | sort - > .qids
    for f in *.fasta
    do
        grep "^>" ${f} | sort - > .fids
        grep -w -v -A 1 -F -f .fids .qids | grep -v "\-\-" > .holdoutids  # --no-group-separator isn't on BSD grep :/
        grep -w -A 1 -F -f .holdoutids ${q} | grep -v "\-\-" > .query_holdouts
        fbase=$(basename ${f} .fasta)
        sortmerna --reads .query_holdouts --ref ${f},${fbase}.idx --aligned ${qbase}-${fbase} --blast 3 --best 1 --print_all_reads -v -a ${threads}
    done
done
