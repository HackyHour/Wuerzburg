# get hamlet and warandpeace from project gutenberg (and remove header and footer)
# * Hamlet: https://gutenberg.org/ebooks/27761.txt.utf-8
# * War and Peace: https://gutenberg.org/cache/epub/2600/
# The License of Project Gutenberg applies
cat hamlet.txt | sed 's/--/\n/g' | tr " " "\n" | tr -d ".,:[]_?\!;0-9()\"" | grep "." | tr A-Z a-z >stream_hamlet.txt
cat warandpeace.txt | sed 's/--/\n/g' | tr " " "\n" | tr -d ".,:[]_?\!;0-9()\"" | grep "." | tr A-Z a-z >stream_warandpeace.txt
