set -e

db=$1
taxonomy=$2
threads=$3

tag=$(basename $db .fasta)
python generate_random_dbs.py --fasta $db --output-basename $tag
sh run_indexdb_rna.sh > /dev/null 2> /dev/null & 
sh make_queries.sh ${db} > /dev/null 2> /dev/null & 
wait
sh run_sortmerna.sh ${threads} > /dev/null 2> /dev/null

echo "TRIM LENGTH 100"
python summarize.py --trim 100 --taxonomy $taxonomy
echo "******************************"
echo "TRIM LENGTH 150"
python summarize.py --trim 150 --taxonomy $taxonomy
echo "******************************"
echo "TRIM LENGTH 250"
python summarize.py --trim 250 --taxonomy $taxonomy
echo "******************************"
echo "ALL"
python summarize.py --taxonomy $taxonomy
