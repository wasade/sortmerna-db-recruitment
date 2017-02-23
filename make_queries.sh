set -e

srcpath=$1

qiime tools import --type FeatureData[Sequence] --input-path $srcpath --output-path srcdb.qza
qiime feature-classifier extract-reads --i-sequences srcdb.qza --p-f-primer GTGYCAGCMGCCGCGGTAA --p-r-primer GGACTACNVGGGTWTCTAAT --o-reads EMP-V4.queries

unzip EMP-V4.queries.qza
uuid=$(qiime tools peek EMP-V4.queries.qza | grep UUID | awk '{ print $2 }')
queries_file=${uuid}/data/dna-sequences.fasta

final_queries_base=EMP-V4-$(basename $srcpath .fasta)
for trim in {100,150,250}
do
    cut -c 1-${trim} ${queries_file} > ${final_queries_base}.${trim}.queries
done
