#!/bin/bash

parse_string () {
    echo "$1" | cut -d$2 -f$3
}

SQL_PATH=$1

for file in ${SQL_PATH}/*.sql ; do
    # MODEL=$(parse_string ${file} '/' '9')
    echo "Formating ${file} ..."
    sqlformat ${file} \
        -i "lower" \
        -k "lower" \
        -o ${file}
done
