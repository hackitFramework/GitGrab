mkdir contents
cd contents
httrack $1
echo $1...
grep -o -Ril $2 ./
cd ..
rm -rf contents
