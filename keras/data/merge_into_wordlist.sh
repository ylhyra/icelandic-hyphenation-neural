#!/bin/bash
cd "$(dirname "$0")"

rm -f wordlist.txt
rm -f wordlist-real.txt

# cat real_data/*.txt junk_data/*.txt \
#   | awk '!/[^abcdefghijklmnoprstuvwxyzáæéíðóöúýþ\|\.\-]/' \
#   | awk '{print int(rand()*100000) "," $0}' | sort -n | awk -F, '{print $2}' \
#   | awk 'NF' \
#   > wordlist.txt

cat real_data/*.txt junk_data/*.txt \
  > wordlist.txt


for i in {1..20}; do
  cat real_data/hyphenation.txt >> wordlist.txt
done
for i in {1..10}; do
  cat real_data/guessed_from_bin.txt >> wordlist.txt
  cat real_data/guessed_from_bin_more.txt >> wordlist.txt
done


# node --max-old-space-size=18096 randomize.js
# gshuf wordlist_tmp.txt -o wordlist.txt
./terashuf < wordlist_tmp.txt  > wordlist.txt


# cat real_data/hyphenation.txt  real_data/guessed_from_bin.txt real_data/guessed_from_bin_more.txt >> wordlist-real.txt
