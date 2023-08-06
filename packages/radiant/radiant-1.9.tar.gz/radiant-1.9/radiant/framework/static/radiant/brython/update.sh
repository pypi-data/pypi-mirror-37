#!/usr/bin/bash

echo "Removing old files"
mkdir old
mv brython.js old/
mv brython_stdlib.js old/
mv brython_modules.js old/


echo "Downloading new files"
rm -r tmp
mkdir tmp
cd tmp
python -m brython --install --modules
cd ../
cp tmp/brython.js brython.js
cp tmp/brython_stdlib.js  brython_stdlib.js
cp tmp/brython_modules.js brython_modules.js
rm -r tmp
echo "Done"
