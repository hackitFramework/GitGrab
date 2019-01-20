git clone $1 &> /dev/null
cd $2
echo
echo $2...
grep -o -Ril $3 ./
cd ..
rm -rf $2
