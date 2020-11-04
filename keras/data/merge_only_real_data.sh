#!/bin/bash
cd "$(dirname "$0")"

rm -f wordlist-real.txt

cat real_data/*.txt  \
  | awk '!/[^abcdefghijklmnoprstuvwxyzáæéíðóöúýþ\|\.\-]/' \
  | awk '{print int(rand()*100000) "," $0}' | sort -n | awk -F, '{print $2}' \
  | awk 'NF' \
  > wordlist-real.txt
