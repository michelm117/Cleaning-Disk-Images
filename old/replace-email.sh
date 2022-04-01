#!/bin/bash

#sed -i 's/^(.*? |)[^@]+@[^ ]+/xxx@xxx.xxx/g' $1
sed "s/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/xxx@xxx.xxx/g" $1
#awk '{gsub(/[A-Za-z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/, "XXXXXXXX@XXXXXX.XXXXXX")}1' test.pdf > out.pdf

