#!/bin/bash

IMAGE=$1
EMAIL_PATTERN="[\s<][A-Za-z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}[\s>]"

if [ -z $IMAGE ]
then
    echo "ERROR: No image file given."
    exit
fi

if [ ! -f $IMAGE ]
then
    echo "ERROR: File does not exists."
    exit
fi


function search_pattern {
    OUT="$(strings -t d $IMAGE | grep -iE "$1")"; printf '%s\n' "$OUT"
}

function main {
    search_pattern $MAIL_PATTERN
}

# strings -t d $IMAGE | grep -iE $EMAIL_PATTERN > offsets.txt
# 3285377403
OFFSETS=( 1329972336 1329996933 1330013454 )
STARTS=($(mmls $IMAGE | awk -F '[[:space:]][[:space:]]+' '{ if ($3 != "") print $3; }'))
LENGTHS=($(mmls $IMAGE | awk -F '[[:space:]][[:space:]]+' '{ if ($5 != "") print $5; }'))
# DESCRIPTIONS="$(mmls $IMAGE | awk -F '[[:space:]][[:space:]]+' 'BEGIN{RS="\n"} { if ($6 != "") print $6; }')"
# echo ${#LENGTHS[@]}
echo ${LENGTHS[@]}
echo ${STARTS[@]}

CURRENT_FILE_SYSTEM=3
echo  [ ${STARTS[$CURRENT_FILE_SYSTEM]}  ]


bin=$(echo ${STARTS[CURRENT_FILE_SYSTEM]} | sed 's/^0*//')
bin="$(( $bin * 512 ))"
echo $bin
echo ${STARTS[$CURRENT_FILE_SYSTEM]}
exit
for offset in "${OFFSETS[@]}"
do
    bin=$(echo ${STARTS[CURRENT_FILE_SYSTEM]} | sed 's/^0*//')
    bin="$(( $bin * 512 ))"
    if (( $offset - $(( ${STARTS[CURRENT_FILE_SYSTEM]} * 512 )) -gt ${LENGTHS[CURRENT_FILE_SYSTEM]} ))
    then
        echo "TO SMALL"
        ((CURRENT_FILE_SYSTEM=CURRENT_FILE_SYSTEM+1))
    else
        echo "FOUND"
    fi
done