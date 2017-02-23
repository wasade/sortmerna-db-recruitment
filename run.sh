set -e

db=$1
threads=$2

tag=$(basename $db .fasta)
python generate_random_dbs.py --fasta $db --output-basename $tag
sh run_indexdb_rna.sh &
sh make_queries.sh ${db} &
wait
sh run_sortmerna.sh ${threads}

echo "TRIM LENGTH 100"
python summarize.py --glob-pattern="*.100-*blast"
echo "******************************\n"
echo "TRIM LENGTH 150"
python summarize.py --glob-pattern="*.150-*blast"
echo "******************************\n"
echo "TRIM LENGTH 250"
python summarize.py --glob-pattern="*.250-*blast"
echo "******************************\n"
