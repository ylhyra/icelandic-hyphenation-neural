#!/bin/bash
cd "$(dirname "$0")"

rm -f wordlist.txt

# cat real_data/*.txt junk_data/*.txt \
#   | awk '!/[^abcdefghijklmnoprstuvwxyzáæéíðóöúýþ\|\.\-]/' \
#   | awk '{print int(rand()*100000) "," $0}' | sort -n | awk -F, '{print $2}' \
#   | awk 'NF' \
#   > wordlist.txt

cat real_data/*.txt junk_data/*.txt \
  > wordlist.txt


for i in {1..7}; do 
  cat real_data/hyphenation.txt >> wordlist.txt
done


node --max-old-space-size=4096 randomize.js
