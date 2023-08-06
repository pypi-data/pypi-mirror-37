#!/usr/bin/bash

echo "Removing old files"
rm brython.js
rm brython_stdlib.js
rm brython_modules.js
echo "Downloading new files"
wget http://brython.info/src/brython.js
wget http://brython.info/src/brython_stdlib.js
echo "Done"
 
