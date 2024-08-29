#!/bin/bash

tree -H '.' \
    -L 1 \
    --noreport \
    --dirsfirst \
    --charset utf-8 \
    --ignore-case \
    -I "index.html" \
    -T 'Pizza Orders' \
    -P "*.html" \
    -o index.html

