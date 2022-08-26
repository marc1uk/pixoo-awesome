#!/bin/bash
if [ $# -ne 16 ]; then
   echo "need 16 args, got $#"
   exit -1
fi
. /home/marc/LinuxSystemFiles/bitbash/bmplib.sh
pixels=()
curcol=(00 00 00 ff)
init_bmp 5 16 16
curcol=(ff ff ff ff)
for i in `seq 0 15`; do
   point $i $1   # set next point
   shift         # Shift all arguments to the left (original $1 gets lost)
done
output_bmp > /tmp/plot.bmp


