set -e

base=/Users/mcdonadt/ResearchWork/greengenes_release/gg_13_8_otus/rep_set/70_otus.fasta
obase=gg70
python generate_random_dbs.py --fasta ${base} --output-basename ${obase}

total=$(grep -c "^>" /Users/mcdonadt/ResearchWork/greengenes_release/gg_13_8_otus/rep_set/70_otus.fasta)
echo "Total number of seqs: ${total}"

echo "Expect each generated file to have approximately 80% of total"
grep -c "^>" ${obase}*.fasta

echo "Expect each generated file to have a different md5 of IDs contained"
for f in ${obase}*.fasta
do
    echo $(grep "^>" ${f} | sort - | md5)
done

echo "Expect sequence and IDs to be identical with source"
for f in ${obase}*.fasta
do
    for i in $(grep "^>" ${f} | head)
    do
        expected=$(grep -A 1 "^${i}$" ${base} | md5)
        observed=$(grep -A 1 "^${i}$" ${f} | md5)
        if [[ "${observed}" != "${expected}" ]];
        then
            echo "Not identical; $f; $i"
            exit 1
        fi
    done
done
echo "...if we reached here then sequences and IDs are identical"
