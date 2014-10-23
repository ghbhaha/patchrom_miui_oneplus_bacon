#usage: ./MakeClean
# !/bin/sh
echo 正在清理工作目录。。。
cd ..
. build/envsetup.sh 
cd -
make clean
echo 清理完成!


