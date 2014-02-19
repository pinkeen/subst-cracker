#!/usr/bin/env bash

gnuplot -persist << EOF
set key autotitle columnhead
plot "test_stats.txt" using 1:2 with linespoints, "" using 1:3 with lines, "" using 1:4 with lines, "" using 1:5 with lines
EOF
