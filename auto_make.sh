#!/bin/sh
#
#sh for miui patchrom
#usage:
#. make.sh $1 $2
#$1 == Device
#$2 == BUILD_NUMBER
#$3 == Last_Target.zip
echo "******************"
echo "*Init Environment*"
echo "******************"
cd ..
. build/envsetup.sh
cd -
pwd
echo "******************"
echo "*     Clean      *"
echo "******************"
make clean
echo "******************"
echo "*     Fullota    *"
echo "******************"
make fullota BUILD_NUMBER=$2
echo "******************"
echo "*Copy Fullota.zip*"
echo "******************"
cp out/fullota.zip $2-fullota.zip
echo "******************"
echo "*      OTA       *"
echo "******************"
echo "------------------"
echo "    make ota?     "
echo "------------------"
read
../tools/releasetools/ota_from_target_files -k ../build/security/testkey -i $3 out/target_files.zip OTA-$3-$2.zip
cp out/target_files.zip $2-target.zip
echo "******************"
echo "*     Done!      *"
echo "******************"
