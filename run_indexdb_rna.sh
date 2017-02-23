set -e

for f in *.fasta
do
    indexdb_rna --ref ${f},$(basename ${f} .fasta).idx &
done
wait
