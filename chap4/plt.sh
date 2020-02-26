#!/bin/bash

set -ue

if [ $# -lt 1 ]; then
    echo "usage: $0 [logfile]"
    exit 1
fi

log=$1

png="${log/.txt/.png}"

gnuplot << EOS
set key
set xlabel "elapsed time[ms]"
set ylabel "progress[%]"
set xtics nomirror
set ytics nomirror
set terminal png
set output "${png}"
plot "${log}" index 0 using 2:3 w p pt 7 ps 1 lc "red" title "task 0", \
"${log}" index 1 using 2:3 w p pt 7 ps 1 lc "blue" title "task 1", \
"${log}" index 2 using 2:3 w p pt 7 ps 1 lc "green" title "task 2", \
"${log}" index 3 using 2:3 w p pt 7 ps 1 lc "orange" title "task 3"
EOS

